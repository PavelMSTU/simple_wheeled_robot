
from time import sleep
from machine import Pin

import _thread

from core import read_infrared_signal_code
from core import engines_stop, engine_left, engine_right
# from core import core_busy_pins

from button_codes import BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4, BUTTON_5, \
     BUTTON_6, BUTTON_7, BUTTON_8, BUTTON_9


pinnum_led_main = 25
# assert pinnum_led_main not in core_busy_pins
led_main = Pin(pinnum_led_main, Pin.OUT)
led_main.value(0)

sleep_time = 0.5

last_out = None

_OUT_KEY = 'NONE'


def key_waiter():
    global _OUT_KEY
    last_out = None
    while True:
        out = read_infrared_signal_code()
        if not out:
            out = last_out
        last_out = out
        _OUT_KEY = out

def test_key_waiter():
    global _OUT_KEY
    while True:
        print(_OUT_KEY)
        sleep(1)


_thread.start_new_thread(key_waiter, ())

def main():
    while True:
        sleep(0.05)
        # engines_stop()
        # led_main.value(1)
        # out = read_infrared_signal_code()
        # led_main.value(0)
        # if not out:
        #     out = last_out
        # last_out = out
        out=_OUT_KEY
        
        if out == BUTTON_1: 
            engine_right(+1)
            engine_left(0)
            sleep(sleep_time)
        elif out == BUTTON_2:  
            engine_right(+1)
            engine_left(+1)
            sleep(sleep_time)
        elif out == BUTTON_3:
            engine_right(0)
            engine_left(+1)
            sleep(sleep_time)
        elif out == BUTTON_4: 
            engine_right(+1)
            engine_left(-1)
            sleep(sleep_time)
        elif out == BUTTON_5: 
            engines_stop()
            sleep(sleep_time)
        elif out == BUTTON_6: 
            engine_right(-1)
            engine_left(+1)
            sleep(sleep_time)
        elif out == BUTTON_7:
            engine_right(-1)
            engine_left(0)
            sleep(sleep_time)
        elif out == BUTTON_8:  
            engine_right(-1)
            engine_left(-1)
            sleep(sleep_time)
        elif out == BUTTON_9: 
            engine_right(0)
            engine_left(-1)
            sleep(sleep_time)
        
        # led_main.value(0)
        # print(out)
        # print(type(out))
        # print('-------')

main()
# test_key_waiter()