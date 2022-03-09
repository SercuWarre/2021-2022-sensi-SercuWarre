def my_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s' % channel)
    print('This is run in a different thread to your main program')


GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback)
# add rising edge detection on a channel ...the rest of your program...
# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(channel, GPIO.RISING,
                      callback=my_callback, bouncetime=200)
GPIO.add_event_callback(channel, my_callback, bouncetime=200)
GPIO.remove_event_detect(channel)
