
from time import sleep
from time import ticks_ms
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

# sleep_time = 0.5

last_out = None

_OUT_KEY = 'NONE'
_OUT_KEY_TIME = ticks_ms()


def key_waiter():
    global _OUT_KEY
    global _OUT_KEY_TIME
    last_out = None
    while True:
        out = read_infrared_signal_code()
        if not out:
            out = last_out
        last_out = out
        _OUT_KEY = out
        _OUT_KEY_TIME = ticks_ms()

def test_key_waiter():
    global _OUT_KEY
    while True:
        print(_OUT_KEY)
        sleep(1)


_thread.start_new_thread(key_waiter, ())

def main():
    global _OUT_KEY
    global _OUT_KEY_TIME
    for i in range(4):
        led_main.value(1)
        sleep(0.3)
        led_main.value(0)
        sleep(0.3)
    
    while True:
        sleep(0.05)
        
        out=_OUT_KEY
        time_press = _OUT_KEY_TIME
        time_now = ticks_ms()
        
        if (time_now-time_press) > 250:
            engines_stop()
            continue
            
        
        if out == BUTTON_1: 
            engine_right(+1)
            engine_left(0)
        elif out == BUTTON_2:  
            engine_right(+1)
            engine_left(+1)
        elif out == BUTTON_3:
            engine_right(0)
            engine_left(+1)
        elif out == BUTTON_4: 
            engine_right(+1)
            engine_left(-1)
        elif out == BUTTON_5: 
            engines_stop()
        elif out == BUTTON_6: 
            engine_right(-1)
            engine_left(+1)
        elif out == BUTTON_7:
            engine_right(-1)
            engine_left(0)
        elif out == BUTTON_8:  
            engine_right(-1)
            engine_left(-1)
        elif out == BUTTON_9: 
            engine_right(0)
            engine_left(-1)


main()
# test_key_waiter()