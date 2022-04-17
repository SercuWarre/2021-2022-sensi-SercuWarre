import time
import RPi.GPIO as GPIO
from klasseMCP import MCPclass


klasse = MCPclass()

GPIO.setmode(GPIO.BCM)


try:
  while True:
    # x = klasse.read_channel(0)
    # print(x)
    # xlist = x[2]
    # print(xlist)
    # y = klasse.read_channel(1)
    # print(y)
    # ylist = y[2]
    # print(ylist)
    # waardepot = (potUitList/255) *3.3
    # print("Waarde potentiometer= {} Volt".format(round(waardepot,2)))
    time.sleep(1)

 
except KeyboardInterrupt:
  klasse.closespi()
  GPIO.cleanup()
finally:
  print("Script gestopt")