from xml.dom import pulldom
from RPi import GPIO
from numpy import binary_repr
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
totaal = 0

try:
    while True:
        knop1 = not GPIO.input(18)
        knop2 = not GPIO.input(17)
        knop3 = not GPIO.input(27)
        knop4 = not GPIO.input(22)

        totaal = knop1
        totaal = totaal | (knop2 << 1)
        totaal = totaal | (knop3 << 2)
        totaal = totaal | (knop4 << 3)
        print(totaal)
        time.sleep(1)

except KeyboardInterrupt as e:
    print(e)
finally:
    print("stop")
    GPIO.cleanup()
