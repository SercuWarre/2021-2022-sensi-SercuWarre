from RPi import GPIO
import serial
import time

knop1 = 24
knop2 = 25


def potmeter(string):
    print("Get sensor waarde 1:")
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0)
    ser.write(b'sensor1')
    a = ser.readline()
    time.sleep(2)
    print(a)
    print(a.decode(encoding='utf-8'))
    print()
    ser.close()


def lichtmeter(string):
    print("Get sensor waarde 2:")
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=3.0)
    ser.write(b'sensor2')
    a = ser.readline()
    time.sleep(2)
    print(a)
    print(a.decode(encoding='utf-8'))
    print()
    ser.close()


def setup(knop1, knop2):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(knop1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(knop2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(knop1, GPIO.FALLING, potmeter, bouncetime=170)
    GPIO.add_event_detect(knop2, GPIO.FALLING, lichtmeter, bouncetime=200)
    print("script is running")


try:
    setup(knop1, knop2)
    while True:
        potmeter()
        lichtmeter()
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()
    print("Script stopped")
