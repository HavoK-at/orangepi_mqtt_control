import os
import sys
from datetime import datetime
from pyA20.gpio import gpio
from pyA20.gpio import port


# Check if root cause we need root for access to the pins
if not os.getegid() == 0:
    sys.exit('Script must be run as root')

# set variables to the pins we want to change
led = port.PA12
button = port.PA11

# init the gpio pins
gpio.init()
gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(button, gpio.INPUT)
gpio.pullup(button, gpio.PULLUP)

led_light = 0
checked = False

try:
    print("Press CTRL+C to exit")
    while True:
        date_time = datetime.now()
        time_check = int(date_time.microsecond / 1000)
        if time_check % 10 == 0:
            state = gpio.input(button)
            if state == 0 and not checked:
                print("Toggled")
                checked = True
                led_light = (led_light + 1) % 2

            if state == 1 and checked:
                checked = False
        gpio.output(led, led_light)
except KeyboardInterrupt:
    print("Goodbye.")
