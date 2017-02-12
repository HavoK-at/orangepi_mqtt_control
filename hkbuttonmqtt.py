import os
import sys
from pyA20.gpio import port
from hkbuttonhandler import *
import time
import paho.mqtt.client as mqtt


class hkButtonMqtt:

    __HK_MQTT_CLIENT = None
    __HK_BUTTON_HANDLER = None

    __hk_host = None
    __hk_password = None
    __hk_username = None
    __hk_port = None
    __hk_heartbeat_count = 0
    __hk_heartbeat_on = 600

    def main(self):
        # Check if root cause we need root for access to the pins
        if not os.getegid() == 0:
            sys.exit('Script must be run as root')

        self.check_args(sys.argv)

        try:
            self.__HK_MQTT_CLIENT = mqtt.Client()

            self.__HK_MQTT_CLIENT.username_pw_set(username=self.__hk_username, password=self.__hk_password)
            self.__HK_MQTT_CLIENT.connect(self.__hk_host, int(self.__hk_port), 60)
        except:
            print("Could not set up MQTT client", sys.exc_info()[0])
            exit(1)

        # set variables to the pins we want to change
        button = port.PA11

        # init the gpio pins
        config = {button: (self.callback, True)}

        # generate button handler
        self.__HK_BUTTON_HANDLER = hkButtonHandler(config)

        # get start time
        start_time = time.perf_counter() * 1000.0
        try:
            print("Press CTRL+C to exit")
            # check inputs
            while True:
                self.__HK_BUTTON_HANDLER.check_inputs()
                time.sleep(0.05 - ((time.perf_counter() - start_time) % 0.05))

                # heartbeat for mqtt
                self.heart_beat()

        except KeyboardInterrupt:
            print("Exiting")

    def check_args(self, argv):
        argc = len(argv)
        if argc != 5:
            self.usage()
            exit(1)

        self.__hk_host = argv[1]
        self.__hk_port = argv[2]
        self.__hk_username = argv[3]
        self.__hk_password = argv[4]

    def callback(self, values):
        print("CALLED BY", values[hkButtonEnum.HK_GPIO],
              values[hkButtonEnum.HK_OUTPUT_SET])
        self.__HK_MQTT_CLIENT.publish("cmnd/pi/button1", payload=values[hkButtonEnum.HK_OUTPUT_SET])

    def heart_beat(self):
        if self.__hk_heartbeat_count == self.__hk_heartbeat_on:
            self.__hk_heartbeat_count = 0
            self.__HK_MQTT_CLIENT.publish("status/pi/heartbeat")
        self.__hk_heartbeat_count += 1

    @staticmethod
    def usage():
        print("Usage: sudo python3 hkbuttonmqtt.py <host> <port> <username> <password>")

if __name__ == "__main__":
    program = hkButtonMqtt()
    program.main()
