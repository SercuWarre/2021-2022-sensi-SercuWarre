import time
from RPi import GPIO
txpin=21

GPIO.setmode(GPIO.BCM)
GPIO.setup(txpin,GPIO.OUT)
text="hello"


def verstuur(tekst):
    for i in range (0,8):
        if (tekst&0x80)==0x80:
            print("1")
            GPIO.output(txpin, GPIO.HIGH)
        else:
            print("0")
            GPIO.output(txpin, GPIO.LOW)

        tekst=tekst<<1
        time.sleep(0.02)

for i in text:
    verstuur(ord(i))
