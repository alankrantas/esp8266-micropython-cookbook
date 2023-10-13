# WS2812 NeoPixel LED Rainbow/Rotation Effect (based on Adafruit example)

neo_pin      = 5    # pin for NeoPixel
neo_num      = 12   # number of leds
neo_maxlevel = 0.3  # max brightness level (0.0-1.0)


from machine import Pin
from neopixel import NeoPixel
import time


class NeoPixelRainbow():
    
    def __init__(self, pin, num=0, brightness=0.0):
        self._np = NeoPixel(Pin(pin, Pin.OUT), num)
        self._buffer = [(0, 0, 0)] * num
        self._brightness = brightness
    
    def __getitem__(self, key):
        return self._buffer[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._buffer[key] = tuple(value)
        elif isinstance(key, slice):
            self._buffer[key] = [tuple(color) for color in value]

    def __len__(self):
        return len(self._buffer)
    
    @property
    def n(self):
        return len(self._buffer)
    
    def _color(self, color):
        return tuple([round(c * self._brightness) for c in color])
    
    def wheel(self, pos):
        r, g, b = 0, 0, 0
        if pos < 0 or pos > 255:
            pass
        elif pos < 85:
            r, g, b = 255 - pos * 3, pos * 3, 0
        elif pos < 170:
            pos -= 85
            r, g, b = 0, 255 - pos * 3, pos * 3
        else:
            pos -= 170
            r, g, b = pos * 3, 0, 255 - pos * 3
        return (r, g, b)
    
    def fill(self, color):
        self[:] = [color] * self.n
        
    def clear(self, color):
        self.fill((0, 0, 0))

    def rainbowCycle(self, cycle=0):
        for i in range(len(self._buffer)):
            self[i] = self.wheel((round(i * 255 / self.n) + cycle) & 255)
            
    def rotate(self, clockwise=True):
        self[:] = (self[-1:] + self[:-1]) if clockwise else (self[1:] + self[:1])
    
    def write(self):
        for i in range(self.n):
            self._np[i] = self._color(self[i])
        self._np.write()


np = NeoPixelRainbow(pin=neo_pin,
                     num=neo_num,
                     brightness=neo_maxlevel)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, BLACK)

for color in COLORS:       
    np.fill(color)
    np.write()
    time.sleep_ms(200)

for color in COLORS:       
    for i in range(np.n):
        np[i] = color
        np.write()
        time.sleep_ms(25)

np.rainbowCycle()

for _ in range(np.n * 3):
        np.rotate(clockwise=True)
        np.write()
        time.sleep_ms(25)

cycle = 0
while True:
    np.rainbowCycle(cycle)
    np.write()
    cycle = (cycle + 1) & 255
