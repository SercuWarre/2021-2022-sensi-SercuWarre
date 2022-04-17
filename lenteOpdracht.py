import serial
import spidev
import threading
from RPi import GPIO 
import time
from subprocess import check_output
from MCP3008 import MCP3008
pins=[16,12,25,24,23,26,19,13]
rsPin=21
Epin=20
displayON=0b00001100
functionSet=0b00111000
clearDisplay=0b00000001
teversturenwaarde=0b01000001
teller=0
knopStatus=1
red = 17    #out
green = 27  #out
blue = 22   #out
Switch_JS=5
# global variables --------------------------
delay = 0.001
# ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0) #open serial port
# ser = ""
spi = spidev.SpiDev()
# spi = ""
page = 0


klasse = MCP3008()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rsPin, GPIO.OUT)
    GPIO.setup(Epin, GPIO.OUT)
    GPIO.output(Epin,GPIO.HIGH)
    GPIO.setup([red,green,blue], GPIO.OUT) #RGB
    GPIO.setup(Switch_JS, GPIO.IN,GPIO.PUD_UP)
    GPIO.add_event_detect(Switch_JS, GPIO.FALLING, bouncetime=200)

    print("script is running")
    for i in range(8):
        GPIO.setup(pins[i], GPIO.OUT)
    
def set_data_bits(value):
    for i in range(8):
        waarde = value >> i & 1
        GPIO.output(pins[i],waarde)
        # print("output", waarde)

def send_instruction(value):
    GPIO.output(rsPin,GPIO.LOW)
    set_data_bits(value)
    GPIO.output(Epin,GPIO.LOW)
    GPIO.output(Epin,GPIO.HIGH)
    time.sleep(0.5)


def send_character(value):
    GPIO.output(rsPin,GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(Epin,GPIO.LOW)
    GPIO.output(Epin,GPIO.HIGH)
    time.sleep(0.1)


def write_message(message):
    teller=0
 
    if len(message)<17:
        send_instruction(0b1000000)
        for letter in message:
            print (ord(letter))
            send_character(ord(letter))
    else:
        for letter in message:
            teller +=1
            if teller>16:
                send_instruction(0b11000000)
                teller=0
            print (ord(letter))
            send_character(ord(letter))
    

def write_bar(data):
    bars = round(data / 1023 * 16)
    send_instruction(0b1000000)
    for x in range(0,bars):
        send_character(0xFE)
    for x in range(0,(16-bars)):
        send_character(ord(" "))
def set_cursor(row, position, page):
    hexrow1 = 0x00 | (page) << 4
    hexrow2 = 0x40 | (page) << 4
    coords = 0
    if row == 0:
        coords = hexrow1 | (position)
    else:
        coords = hexrow2 | (position)
    send_instruction(coords | 0x80)
def status(knopStatus): 
   
    if knopStatus==0:
        message=str(check_output(['hostname','--all-ip-addresses']))
        ip=message
        send_instruction(clearDisplay)
        # send_character(65)
        write_message(ip[2:30])
        time.sleep(.1)
    if knopStatus==1:
        send_instruction(clearDisplay)
        vrx = get_data_JS(0)
        #write bar
        write_bar(vrx)

        #write numbers
        print(f"vrx: {vrx}")
        message=f"VRX => {vrx}"
        write_message(message)


    if knopStatus==2:
        send_instruction(clearDisplay)
        vry = get_data_JS(1)
        #write bar
        write_bar(vry)


        #write numbers
        print(f"vry: {vry}")
        message=f"VRY => {vry}"
        write_message(message)
# 
#arduino & 4*7 segmentdisplay
# def init_serial():
#     global ser
#     ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0) #open serial port

# def write_serialport():
#     ser.write(b'hello world\n')


# def read_serialport():
#     print(ser.name)
#     if ser.in_waiting > 0:
#         line = ser.readline().rstrip()
#         print(line)
#joystick & MCP3008

def init_spidev():
    global spi
    spi = spidev.SpiDev()



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
def LCD_thread():
    while True:
        # #LCD
        # if page == 1:
        #     write_page1()
        # elif page == 2:
        #     write_page2()

        if GPIO.event_detected(Switch_JS):
            global knopStatus
            status(knopStatus)
            print("button pressed {0}".format(knopStatus))
            knopStatus+=1
            if knopStatus==3:
                knopStatus=0
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
try:
    # while True:
        # time.sleep(2)
     #code for 4*7 segment display
    
        # write_serialport()   
    setup()
    send_instruction(functionSet)
    send_instruction(displayON)
    status(0)
    init_spidev()
    thread_main()
    while True:
        time.sleep(2)
     #code for 4*7 segment display
    
        # write_serialport()   
except KeyboardInterrupt as e:
    print(e)
    #for i in range(0,7):
    GPIO.output(pins,GPIO.LOW)
        
finally:
    print("script stopped")
    GPIO.cleanup()