import os
import sys
from pyA20.gpio import port
from hkbuttonhandler import *
import time


def callback(values):
    print("CALLED BY",
          values[hkButtonEnum.HK_GPIO],
          values[hkButtonEnum.HK_OUTPUT_SET])

# Check if root cause we need root for access to the pins
if not os.getegid() == 0:
    sys.exit('Script must be run as root')

# set variables to the pins we want to change
button = port.PA11

# init the gpio pins
myDict = {button: (callback, False)}

# generate button handler
button_handler = hkButtonHandler(myDict)

# get start time
start_time = time.perf_counter() * 1000.0
try:
    print("Press CTRL+C to exit")
    # check inputs
    while True:
        button_handler.check_inputs()
        time.sleep(0.05 - ((time.perf_counter() - start_time) % 0.05))

except KeyboardInterrupt:
    print("Exiting")
