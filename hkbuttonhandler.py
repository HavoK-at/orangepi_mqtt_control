from pyA20.gpio import gpio
from pyA20.gpio import port
from enum import Enum

# class will take a dict of entities
# each entity will contain a GPIO Pin, a Function and if its allowed to dim
# The function will be called after a button press on the pin has been detected
# Additionally planned is if dimming is allowed on the pin and the rate of increase/decrease
# All GPIO buttons pins are set to pull up, so the button has to pull towards ground
# Dict item looks like gpio:(func, dimable)


class hkButtonEnum(Enum):
    HK_GPIO = "gpio"
    HK_CALLBACK = "callback"
    HK_DIM = "dim"
    HK_STATE_PRESSED = "state_pressed"
    HK_OUTPUT_SET = "output_set"
    HK_BUTTON_PRESSED = 0           # state if button has been pressed, 0 as pull to ground

class hkButtonHandler:

    # dict to store the gpio pins with params and the callback function
    __HK_PIN_LIST = {}

    def __init__(self, input_list):
        gpio.init()
        for key in input_list:
            tup = input_list[key]
            gpio.setcfg(key, gpio.INPUT)
            gpio.pullup(key, gpio.PULLUP)
            self.__hk_add_to_dict(key, tup)

    def __hk_add_to_dict(self, gpio_key, gpio_tuple):
        func, dim = gpio_tuple
        self.__HK_PIN_LIST[gpio_key] = {}
        self.__HK_PIN_LIST[gpio_key][hkButtonEnum.HK_GPIO] = gpio_key
        self.__HK_PIN_LIST[gpio_key][hkButtonEnum.HK_CALLBACK] = func
        self.__HK_PIN_LIST[gpio_key][hkButtonEnum.HK_DIM] = dim
        self.__HK_PIN_LIST[gpio_key][hkButtonEnum.HK_STATE_PRESSED] = False
        self.__HK_PIN_LIST[gpio_key][hkButtonEnum.HK_OUTPUT_SET] = 0

    def check_inputs(self):
        for key in self.__HK_PIN_LIST:
            values = self.__HK_PIN_LIST[key]
            was_pressed = values[hkButtonEnum.HK_STATE_PRESSED]

            # get button state
            got_pressed = gpio.input(key) == hkButtonEnum.HK_STATE_PRESSED

            if (not got_pressed) and was_pressed:
                values[hkButtonEnum.HK_STATE_PRESSED] = False
            elif got_pressed and was_pressed:
                pass
            elif got_pressed and (not was_pressed):
                values[hkButtonEnum.HK_STATE_PRESSED] = True
                values[hkButtonEnum.HK_CALLBACK](values)
            else:
                pass
