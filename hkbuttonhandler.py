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
    HK_PRESSED_SINCE = "pressed_since"
    HK_DIM_DOWN = "dim_down"


class hkButtonHandler:

    # dict to store the gpio pins with params and the callback function
    __HK_BUTTON_PRESSED = 0             # button pulls to ground
    __HK_BUTTON_DIM_THRESHOLD = 5     # in cycles
    __HK_DIM_RATE_PER_CYCLE = 3
    __HK_PIN_LIST = {}

    def __init__(self, input_dict):
        gpio.init()
        for key in input_dict:
            tup = input_dict[key]
            gpio.setcfg(key, gpio.INPUT)
            gpio.pullup(key, gpio.PULLUP)
            self.__hk_add_to_dict(key, tup)

    def __hk_add_to_dict(self, gpio_key, gpio_tuple):
        func, dim = gpio_tuple
        self.__HK_PIN_LIST[gpio_key] = {
            hkButtonEnum.HK_GPIO: gpio_key,
            hkButtonEnum.HK_CALLBACK: func,
            hkButtonEnum.HK_DIM: dim,
            hkButtonEnum.HK_STATE_PRESSED: False,
            hkButtonEnum.HK_OUTPUT_SET: 0,
            hkButtonEnum.HK_PRESSED_SINCE: 0,
            hkButtonEnum.HK_DIM_DOWN: False
        }

    def __hk_call_back(self, key):
        values = self.__HK_PIN_LIST[key]
        # check boundaries
        if values[hkButtonEnum.HK_OUTPUT_SET] < 0:
            values[hkButtonEnum.HK_OUTPUT_SET] = 0
        elif values[hkButtonEnum.HK_OUTPUT_SET] > 100:
            values[hkButtonEnum.HK_OUTPUT_SET] = 100
        values[hkButtonEnum.HK_CALLBACK](values)

    def check_inputs(self):
        for key in self.__HK_PIN_LIST:
            values = self.__HK_PIN_LIST[key]
            was_pressed = values[hkButtonEnum.HK_STATE_PRESSED]
            got_pressed = gpio.input(key) == self.__HK_BUTTON_PRESSED

            # button is not pressed but was pressed
            if (not got_pressed) and was_pressed:
                was_long_press = values[hkButtonEnum.HK_PRESSED_SINCE] >= self.__HK_BUTTON_DIM_THRESHOLD

                # if longpress and value was not 100, set to hundred
                # else turn to 0
                if (not was_long_press) and (values[hkButtonEnum.HK_OUTPUT_SET] < 100):
                    values[hkButtonEnum.HK_OUTPUT_SET] = 100
                elif not was_long_press:
                    values[hkButtonEnum.HK_OUTPUT_SET] = 0

                if values[hkButtonEnum.HK_OUTPUT_SET] == 0:
                    values[hkButtonEnum.HK_DIM_DOWN] = False
                else:
                    values[hkButtonEnum.HK_DIM_DOWN] = True

                # send callback
                self.__hk_call_back(key)
                # call function and reset states
                values[hkButtonEnum.HK_PRESSED_SINCE] = 0
                values[hkButtonEnum.HK_STATE_PRESSED] = False

            # button is pressed and was pressed -> stage 2 dim
            elif got_pressed and was_pressed:

                # if dim is allowed and dim threshold has been reached, reduce output by rate and callback
                if values[hkButtonEnum.HK_DIM] and \
                        values[hkButtonEnum.HK_PRESSED_SINCE] > self.__HK_BUTTON_DIM_THRESHOLD:

                    if values[hkButtonEnum.HK_DIM_DOWN] and values[hkButtonEnum.HK_OUTPUT_SET] > 0:
                        values[hkButtonEnum.HK_OUTPUT_SET] -= self.__HK_DIM_RATE_PER_CYCLE
                    elif (not values[hkButtonEnum.HK_DIM_DOWN]) and values[hkButtonEnum.HK_OUTPUT_SET] < 100:
                        values[hkButtonEnum.HK_OUTPUT_SET] += self.__HK_DIM_RATE_PER_CYCLE

                    self.__hk_call_back(key)

                values[hkButtonEnum.HK_PRESSED_SINCE] += 1

            # button is pressed but was not pressed -> call function
            elif got_pressed and (not was_pressed):
                values[hkButtonEnum.HK_STATE_PRESSED] = True
