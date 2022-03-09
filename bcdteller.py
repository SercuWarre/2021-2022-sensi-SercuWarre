from RPi import GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    resultaat=0
def lees_bcd():
     knop1= not GPIO.input(18)
     knop2 = not GPIO.input(17)
     knop3 = not GPIO.input(27) 
     knop4 = not GPIO.input(22)

     resultaat=knop1
     resultaat=resultaat|(knop2<<1)
     resultaat=resultaat|(knop3<<2)
     resultaat=resultaat|(knop4<<3)
     print(resultaat)

try:
     setup()
     while True:
         lees_bcd()
         time.sleep(1)
except KeyboardInterrupt as e:
    print(e)
finally:
    print("stop")
    GPIO.cleanup()
