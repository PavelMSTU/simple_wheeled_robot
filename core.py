"""
Core script for vehicle robot
"""

from machine import Pin
import utime

# -----------------------------
# GP PIN-s in Raspberry Pi Pico
# https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
# see Figure 2. "The pinout of the Raspberry Pi Pico Rev3 board"
# You CAN change it in core.py 

pinnum_engine_en1 = pinnum_engine_en2 = 19
pinnum_engine_in1=5
pinnum_engine_in2=2
pinnum_engine_in3=3
pinnum_engine_in4=4
pinnum_infrared_signal_out=16


# -----------------------------

core_busy_pins = [ pinnum_engine_en1,
    pinnum_engine_en2,
    pinnum_engine_in1,
    pinnum_engine_in2,
    pinnum_engine_in3,
    pinnum_engine_in4,
    pinnum_infrared_signal_out,
]

    
pin_en1 = Pin(pinnum_engine_en1, Pin.OUT)
pin_en2 = Pin(pinnum_engine_en2, Pin.OUT)
pin_en1.value(0)
pin_en2.value(0)

pin_in1 = Pin(pinnum_engine_in1, Pin.OUT)
pin_in2 = Pin(pinnum_engine_in2, Pin.OUT)
pin_in3 = Pin(pinnum_engine_in3, Pin.OUT)
pin_in4 = Pin(pinnum_engine_in4, Pin.OUT)
    
pin_in1.value(0)
pin_in2.value(0)
pin_in3.value(0)
pin_in4.value(0)
    
pin_infrared_signal = Pin(pinnum_infrared_signal_out, Pin.IN, Pin.PULL_UP)
    
# ------------------------------------------------------
# infrared_signal


def read_infrared_signal_code():
    # See here:
    #     https://github.com/bartoszadamczyk/pico-ir/blob/main/pico_ir/read_code.py
    # -------------------------
    
    pin = pin_infrared_signal
    
    raw = []

    # Signal is inverted:
    # 0 - high signal
    # 1 - low signal

    # wait for the leading pulse
    while pin.value() == 1:
        pass

    # 9ms leading pulse
    # 4.5ms space
    utime.sleep_us(13500)

    # Sample signal every 562.5µs
    # Time sensitive
    for i in range(1000):
        raw.append(pin.value())
        utime.sleep_us(56)

    code = ""
    count = 0

    for sample in raw:
        if sample == 1:
            # count low signal
            count += 1
        else:
            # ignore high signal
            if count > 0:
                # if low signal is longer than 562.5µs it 1 otherwise 0
                code += "1" if count > 10 else "0"
                count = 0

    # trim message transmission and repeat codes
    return code[0:32]

# -----------------------------------------------
# Control of two engines.
# (Or four, joined in pairs)

def engines_stop():
    # en.value(0)
    pin_en1.value(0)
    pin_en2.value(0)
    pin_in1.value(0)
    pin_in2.value(0)
    pin_in3.value(0)
    pin_in4.value(0)

def engine_right(speed):
    if speed == 0:
        pin_in1.value(0)
        pin_in2.value(0)
    if speed == +1:
        pin_en1.value(1)
        pin_in1.value(1)
        pin_in2.value(0)
    if speed == -1:
        pin_en1.value(1)
        pin_in1.value(0)
        pin_in2.value(1)


def engine_left(speed):
    if speed == 0:
        pin_in3.value(0)
        pin_in4.value(0)
    if speed == +1:
        pin_in3.value(1)
        pin_in4.value(0)
        pin_en2.value(1)
    if speed == -1:
        pin_in3.value(0)
        pin_in4.value(1)
        pin_en2.value(1)