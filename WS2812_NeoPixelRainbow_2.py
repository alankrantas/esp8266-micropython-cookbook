# WS2812 NeoPixel LED Rainbow/Rotation Effect 2 (based on Adafruit example)

from machine import Pin
from neopixel import NeoPixel
import utime

# NeoPixel setup
neopixel_pin          = 5   # pin for NeoPixel
neopixel_num          = 12  # number of leds
neopixel_maxlevel     = 128 # max brightness level (0-255)
neopixel_rotate_delay = 0   # delay for rotating leds (ms)


class NeoPixelRainbow(NeoPixel):
    
    def __init__(self, pin, num, brightness):
        super().__init__(pin, num)
        self.num = num
        self.brightness = brightness
        self.cycle = 0
    
    def wheel(self, pos):
        r, g, b = 0, 0, 0
        if pos < 0 or pos > 255:
            r, g, b = 0, 0, 0
        elif pos < 85:
            r, g, b = 255 - pos * 3, pos * 3, 0
        elif pos < 170:
            pos -= 85
            r, g, b = 0, 255 - pos * 3, pos * 3
        else:
            pos -= 170
            r, g, b = pos * 3, 0, 255 - pos * 3
        r = round(r * self.brightness / 255)
        g = round(g * self.brightness / 255)
        b = round(b * self.brightness / 255)
        return (r, g, b)
    
    def rainbowCycle(self):
        for i in range(self.num):
            rc_index = (i * 256 // self.num) + self.cycle
            self[i] = self.wheel(rc_index & 255)
        self.cycle = (self.cycle + 1) if self.cycle < 255 else 0
    

np = NeoPixelRainbow(Pin(neopixel_pin, Pin.OUT), neopixel_num,
                     brightness=neopixel_maxlevel)

while True:
    np.rainbowCycle()
    np.write()
    utime.sleep_ms(neopixel_rotate_delay)
