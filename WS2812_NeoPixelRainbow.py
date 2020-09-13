# WS2812 NeoPixel LED Rainbow/Rotation Effect (by Alan Wang)

from machine import Pin
from neopixel import NeoPixel
import utime

# NeoPixel setup
neopixel_pin          = 5   # pin for NeoPixel
neopixel_num          = 12  # number of leds
neopixel_maxlevel     = 128 # max brightness level (0-255)
neopixel_rotate_delay = 50  # delay for rotating leds (ms)

# NeoPixel object
np = NeoPixel(Pin(neopixel_pin, Pin.OUT), neopixel_num)

# set NeoPixel to rainbow colors
def neoPixelRanbow():
    change = int(neopixel_maxlevel / (np.n / 3))
    peak_index = (0, int(np.n / 3), int(np.n / 3 * 2))
    for i in range(np.n):
        color = [0, 0, 0]
        for j in range(3):
            if abs(i - peak_index[j]) <= peak_index[1]:
                color[j] = neopixel_maxlevel - abs(i - peak_index[j]) * change
            elif i >= peak_index[2]:
                color[0] = neopixel_maxlevel - (np.n - i) * change
        np[i] = tuple(color)
    np.write()

# rotate NeoPixel leds
def neoPixelRotate(clockwise=True):
    tmp = tuple(np)
    tmp = (tmp[-1:] + tmp[:-1]) if clockwise else (tmp[1:] + tmp[:1])
    for i, t in enumerate(tmp):
        np[i] = t
    np.write()

# ----------------------------------------------------------------------

neoPixelRanbow()

while True:
    neoPixelRotate(clockwise=True)
    utime.sleep_ms(neopixel_rotate_delay)
