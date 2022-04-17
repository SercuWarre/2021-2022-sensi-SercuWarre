from re import split
from RPi import GPIO 
import time
from subprocess import check_output
pins=[16,12,25,24,23,26,19,13]
rsPin=21
Epin=20
displayON=0b00001100
functionSet=0b00111000
clearDisplay=0b00000001
teversturenwaarde=0b01000001
teller=0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rsPin, GPIO.OUT)
    GPIO.setup(Epin, GPIO.OUT)
    GPIO.output(Epin,GPIO.HIGH)

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
    time.sleep(0.5)


def write_message(message):
    teller=0
    # for letter in message:
    #     print (ord(letter))
    #     send_character(ord(letter))
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

   
try:
    message=f"{check_output(['hostname','--all-ip-addresses'])}"
    ip=message.replace("b", "")
    setup()
    send_instruction(functionSet)
    send_instruction(displayON)
    send_instruction(clearDisplay)
    # send_character(65)
    write_message(ip[1:30])
    time.sleep(30)
except KeyboardInterrupt as e:
    print(e)
    #for i in range(0,7):
    GPIO.output(pins,GPIO.LOW)
        
finally:
    print("script stopped")
    GPIO.cleanup()