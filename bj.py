from RPi import GPIO
from subprocess import check_output
import time
import serial
import spidev
import threading

#pinnen ----------------------------------------

#LCD-pinnen
RS = 21 #out
E = 20 #out

#rgb-pinnen
red = 17    #out
green = 27  #out
blue = 22   #out

#shiftregister-pinnen
DS = 23     #out
OE = 24     #out
ST_CP = 25  #out
SH_CP = 12  #out
MR = 16     #out

#arduino
# txpin = 14
# rxpin = 15

#joystick-pinnen
Switch_JS = 5



# global variables --------------------------
delay = 0.001
# ser = serial.Serial('/dev/serial0') #open serial port
# ser = ""
spi = spidev.SpiDev()
# spi = ""
page = 0

#functions ------------------------------------------------------


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([RS,E], GPIO.OUT) #LCD
    GPIO.setup([red,green,blue], GPIO.OUT) #RGB
    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)
    GPIO.setup([DS,OE,ST_CP,SH_CP,MR], GPIO.OUT, initial=GPIO.LOW) #Shiftregister
    GPIO.output(MR, GPIO.HIGH) #set MR high
    # GPIO.setup(txpin,GPIO.OUT) #arduino(out)
    # GPIO.setup(rxpin, GPIO.IN) #arduino(in)
    GPIO.setup(Switch_JS, GPIO.IN,GPIO.PUD_UP)
    GPIO.add_event_detect(Switch_JS, GPIO.FALLING, bouncetime=200)
    


# LCD & shiftregister
def init_shiftreg():
    reset_shiftreg()
    GPIO.output(OE, GPIO.LOW)

def init_LCD():
    function_set = 0x38 # 0b00111000
    display_on = 0x0C   # 0b00001100
    CD_and_CH = 0x01    # 0b00000001
    send_instruction(function_set)
    send_instruction(display_on)
    send_instruction(CD_and_CH)


def reset_shiftreg():
    GPIO.output(MR, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(MR, GPIO.HIGH)


def send_bit_LCD(bit):
    GPIO.output(DS, bit)
    time.sleep(delay)
    GPIO.output(SH_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SH_CP, GPIO.LOW)
    time.sleep(delay)


def send_byte_LCD(byte):
    GPIO.output(E,GPIO.HIGH)
    mask = 0x80 # 0b10000000
    for x in range(0,8):
        bit = ((byte << x) & mask) #normaal met "> 0" erna maar in python hoeft dit niet bij bitoperaties
        send_bit_LCD(bit)
    copy_to_storage_register()
    GPIO.output(E,GPIO.LOW)
    #reset_shiftreg()

def copy_to_storage_register():
    GPIO.output(ST_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(ST_CP, GPIO.LOW)
    time.sleep(delay)
    #print("storage clock aan en uit zetten")

def send_char(char):
    GPIO.output(RS, GPIO.HIGH)
    send_byte_LCD(char)
    time.sleep(delay)

def send_instruction(instruction):
    GPIO.output(RS, GPIO.LOW)
    send_byte_LCD(instruction)
    time.sleep(delay)

def next_page_LCD():
    global page
    print("pushed")
    print(page)
    instruction = 0x18 # 0b00011000 (goes 1 cell to the right)
    if page == 2: #goto page 0
        send_instruction(2) #0b00000010 (back to page 1)
        write_page0()
        page = 0
    else:
        if page == 0: #goto page 1
            for x in range(0,16):
                send_instruction(instruction)
            set_cursor(1,2,1)
            write_text("X")
        else: #page == 1 #goto page 2
            set_cursor(1,2,1)
            write_text("Y")
        page += 1

def write_text(text):
    for char in text:
        send_char(ord(char))

def init_page1and2(): #writes inital code for page 0 of the LCD
    set_cursor(1,0,1) #row 2, pos 1,page 2
    write_text("VRX =>  ")

# def init_page2(): #writes inital code for page 0 of the LCD
#     set_cursor(1,0,1) #row 2, pos 1,page 3
#     write_text("VRY =>  ")
    


def write_page0(): #ip's
    ip = str(check_output(['hostname','--all-ip-addresses']))
    ip = ip[2:17]
    print(ip)
    set_cursor(0,0,0)
    write_text(ip)


def write_page1(): #vrx
    vrx = get_data_JS(0)
    #write bar
    write_bar(vrx)

    #write numbers
    vrx = str(vrx)
    print(f"vrx: {vrx}")
    vrx = vrx + "   "
    set_cursor(1,7,1)
    write_text(vrx)

def write_page2(): #vry
    vry = get_data_JS(1)
    #write bar
    write_bar(vry)


    #write numbers
    vry = str(vry)
    print(f"vry: {vry}")
    vry = vry + "   "
    set_cursor(1,7,1)
    write_text(vry)

def write_bar(data):
    bars = round(data / 1023 * 16)
    set_cursor(0,0,1)
    for x in range(0,bars):
        send_char(0xFF)
    for x in range(0,(16-bars)):
        send_char(ord(" "))




def set_cursor(row, position, page):
    hexrow1 = 0x00 | (page) << 4
    hexrow2 = 0x40 | (page) << 4
    coords = 0
    if row == 0:
        coords = hexrow1 | (position)
    else:
        coords = hexrow2 | (position)
    send_instruction(coords | 0x80)





#arduino & 4*7 segmentdisplay
def init_serial():
    global ser
    ser = serial.Serial("/dev/serial0") #open serial port

def write_serialport():
    ser.write(b'hello world\n')


def read_serialport():
    print(ser.name)
    if ser.in_waiting > 0:
        line = ser.readline().rstrip()
        print(line)



#joystick & MCP3008

def init_spidev():
    global spi
    spi = spidev.SpiDev()

# def sw_JS_pressed(Switch_JS):
#     valueSW = GPIO.input(Switch_JS)
#     if valueSW == 1:
#         next_page_LCD()

def get_data_JS(slave):
    spi.open(0,0)
    spi.max_speed_hz = 10 ** 5
    bytes_out = [1,(0x80 | (slave << 4)),0]
    bytes_in = spi.xfer(bytes_out)
    data = (bytes_in[1] & 3) << 8 | bytes_in[2]
    spi.close()
    return data


#RGB
def color_RGB(channel, frequency, MCP_channel):
    p = GPIO.PWM(channel, frequency)
    p.start(0)
    dutyCycle = 0
    while True:
        if MCP_channel == 2:
            dutyCycle = (get_data_JS(0) + get_data_JS(1)) / 2
        else:
            dutyCycle  = get_data_JS(MCP_channel)
        dutyCycle = dutyCycle / 1023 * 100
        #print(f"{channel}: {dutyCycle}")
        p.ChangeDutyCycle(dutyCycle)
        time.sleep(0.1)

# def color_RGB_thread():
#     threads = []
#     threads.append(threading.Thread(target=color_RGB, args=(red, 300, 0)))
#     threads.append(threading.Thread(target=color_RGB, args=(green, 300, 1)))
#     threads.append(threading.Thread(target=color_RGB, args=(blue, 300, 2)))
#     for t in threads:
#         t.daemon = True
#         t.start()
#     for t in threads:
#         t.join()


#threads
def LCD_thread():
    while True:
        #LCD
        if page == 1:
            write_page1()
        elif page == 2:
            write_page2()

        if GPIO.event_detected(Switch_JS):
            next_page_LCD()
            print("hi")
        time.sleep(delay)

def thread_main():
    threads = []
    threads.append(threading.Thread(target=color_RGB, args=(red, 300, 0)))
    threads.append(threading.Thread(target=color_RGB, args=(green, 300, 1)))
    threads.append(threading.Thread(target=color_RGB, args=(blue, 300, 2)))
    threads.append(threading.Thread(target=LCD_thread))
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()




#main code -----------------------------

try:
    #code for 4*7 segment display
    while True:
        write_serialport()

    #endcode ----------------------------
    #setups
    setup()
    init_shiftreg()

    #inits LCD
    init_LCD()
    write_page0()
    init_page1and2()
    # send_instruction(2) #sets cursor & shifts display back to the beginning

    # init_RBG()
    init_spidev()

    # threads
    thread_main()




except Exception as e:
    print(e)
finally:
    GPIO.cleanup()
    # ser.close()
    spi.close()
