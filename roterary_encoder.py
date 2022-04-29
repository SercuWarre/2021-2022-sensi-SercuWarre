import time
import RPi.GPIO as GPIO

class Rotary:
    def __init__(self, clk=13, dt=19, sw=26):
        self.dt = dt
        self.clk = clk
        self.sw = sw

        self.clkLastState = 0
        self.counter = 0
        self.switchState = 0

        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.clk, GPIO.BOTH, self.rotation_decode, 1)
        GPIO.add_event_detect(self.sw, GPIO.FALLING, self.pushed, 200)


    def rotation_decode(self, pin):
        dt_value = GPIO.input(self.dt)
        clk_value = GPIO.input(self.clk)
        
        if clk_value != self.clkLastState and clk_value == False:
            if dt_value != clk_value:
                print("Rechts")
                self.counter += 1
            else:
                print("Links")
                self.counter -= 1
            print(self.counter)
        self.clkLastState = clk_value

    def pushed(self, sw):
        print("Druk")

if __name__ == "__main__":
    rotary = Rotary(13, 19, 26)
    try:
        print("script gestart!")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        print("Script gestopt")