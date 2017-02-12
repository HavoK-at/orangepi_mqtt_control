from pyA20.gpio import gpio
from pyA20.gpio import port

# class will take a dict of entities
# each entity will contain a GPIO Pin, a Function and if its allowed to dim
# The function will be called after a button press on the pin has been detected
# Additionally planned is if dimming is allowed on the pin and the rate of increase/decrease
# All GPIO buttons pins are set to pull up, so the button has to pull towards ground
# dict item is a tuple containing (GPIO_PIN, FUNCTION, DIM) with the gpio additionally as dict key
class hkButtonHandler:

    # dict to store the gpio pins with params and the callback function

    __HK_GPIO = "gpio"
    __HK_CALLBACK = "callback"
    __HK_DIM = "dim"
    __HK_STATE_PRESSED = "state_pressed"
    __HK_OUTPUT_SET = "output_set"

    __HK_PIN_LIST = {}


    def __init__(self, input_list):
        gpio.init()
        for key, tup in self.__HK_PIN_LIST:
            gpio.setcfg(key, gpio.INPUT)
            gpio.pullup(key, gpio.PULLUP)
            self.__hk_add_to_dict(key,tup)


    def __hk_add_to_dict(self, gpio_key, gpio_tuple):
        func, dim = gpio_tuple
        self.__HK_PIN_LIST[gpio_key] = {}
        self.__HK_PIN_LIST[gpio_key][self.__HK_GPIO] = gpio_key
        self.__HK_PIN_LIST[gpio_key][self.__HK_CALLBACK] = func
        self.__HK_PIN_LIST[gpio_key][self.__HK_DIM] = dim
        self.__HK_PIN_LIST[gpio_key][self.__HK_STATE_PRESSED] = False
        self.__HK_PIN_LIST[gpio_key][self.__HK_OUTPUT_SET] = 0

