#! bin/python
# sudo minicom -o -D /dev/ttyACM0 -S led25_test.py
# Create at 02.11.2022 10:20:02

from time import sleep
from machine import Pin

led = Pin(25, Pin.OUT)

for a in range(5):
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)


# assert 8 not in [8, 1]

led.value(0)

