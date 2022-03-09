from RPi import GPIO
import time

ledR1 = 24
ledR2 = 23
ledW = 25
knop = 12

oudvalue = 0
spoorwegstate = 0
i = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledR1, GPIO.OUT)
GPIO.setup(ledR2, GPIO.OUT)
GPIO.setup(ledW, GPIO.OUT)
GPIO.setup(knop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(ledR2, GPIO.LOW)
GPIO.output(ledR1, GPIO.LOW)
GPIO.output(ledW, GPIO.LOW)
print("script is running")

try:
    while True:
        knop_status = GPIO.input(knop)
        oudvalue = knop_status
        if(oudvalue == 0 and knop_status == 0):
            spoorwegstate = not spoorwegstate

        GPIO.output(ledR2, GPIO.LOW)
        GPIO.output(ledR1, GPIO.LOW)
        if spoorwegstate == 0:
            GPIO.output(ledW, GPIO.LOW)
            time.sleep(1)
            GPIO.output(ledW, GPIO.HIGH)

        else:
            GPIO.output(ledW, GPIO.LOW)
            i += 1

            GPIO.output(ledR1, GPIO.LOW)
            GPIO.output(ledR2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(ledR1, GPIO.HIGH)
            GPIO.output(ledR2, GPIO.LOW)

            knop_status = GPIO.input(knop)
            oudvalue = knop_status
            if(oudvalue == 0 and knop_status == 0 or i == 7):
                spoorwegstate = 0
                i = 0

        time.sleep(1)

except KeyboardInterrupt as e:
    print(e)
    GPIO.output(ledR2, GPIO.LOW)
    GPIO.output(ledR1, GPIO.LOW)
    GPIO.output(ledW, GPIO.LOW)
    # pass
finally:
    GPIO.cleanup()
    print("script has stopped")
