import os
import sys
from datetime import datetime
from pyA20.gpio import port
from hkbuttonhandler import hkButtonHandler

# Check if root cause we need root for access to the pins
if not os.getegid() == 0:
    sys.exit('Script must be run as root')

# set variables to the pins we want to change
button = port.PA11

# init the gpio pins
myDict = {button: (callable, False)}

button_handler = hkButtonHandler(myDict)

try:
    print("Press CTRL+C to exit")
    button_handler.check_inputs()

except KeyboardInterrupt:
    print("Exiting")


def callback():
    pass