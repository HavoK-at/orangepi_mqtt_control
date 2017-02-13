# MQTT Button Control for the OrangePi Zero

This project will use an undefined amount of external buttons and publish a message on a MQTT topic.

Done:
* Get the external button class to work ✔
* Add dimming by holding the button ✔
* Add mqtt features ✔

Plan:
* Create a Linux daemon for easier starting/stopping
* Reviving the mqtt client if it dies
* Create Config file
* Logging to a file
* Enabling debug messages with flag
* If the bulbs dim value has been changed withing openhab get the value 

# Used Resources:

GPIO for the orange pi zero:  
https://forum.armbian.com/index.php/topic/3084-orange-pi-zero-python-gpio-library/  

Thanks to martinayotte for the information on how to modify the library for the OPi Zero!  

Linux Daemon with python:  
https://linuxfollies.blogspot.co.at/2016/11/linux-daemon-using-python-daemon-with.html
