# Conway's Game of Life on 128x64 SSD1306 OLED and ESP8266 (by Alan Wang)


BIRTH    = (3, )  # number of nearby cells for a new cell to be born
SURVIVAL = (2, 3) # number of nearby cells for an existing cell to survive
WIDTH    = 128
HEIGHT   = 64
DOT_SIZE = 3      # draw 3x3 dots -> board size 128/3 x 64/3
RAND_BIT = 2      # cell randomize factor (2 = 2^2 (1/4 chance))


from machine import Pin, ADC, SoftI2C, freq
from micropython import const
from ssd1306 import SSD1306_I2C
import urandom, utime, gc


freq(160000000)
gc.enable()
urandom.seed(sum([ADC(0).read() for _ in range(1000)]))  # generate randomize seed from floating analog pin


X      = WIDTH // DOT_SIZE
Y      = HEIGHT // DOT_SIZE
TOTAL  = X * Y
board  = [0 if urandom.getrandbits(RAND_BIT) else 1
          for _ in range(TOTAL)]
gen    = 0


display = SSD1306_I2C(WIDTH, HEIGHT,
                      SoftI2C(scl=Pin(5), sda=Pin(4), freq=400000))
display.fill(0)
display.show()


print('Conway\'s Game of Life: matrix size {} x {}'.format(X, Y))
    

def calculate_next_gen():  # calculate next generation of cells
    global board
    buffer = [0] * TOTAL
    for i in range(TOTAL):
        group = board[i-1:i+2] + \
                board[(i-1-X)%TOTAL:(i+2-X)%TOTAL] + \
                board[(i-1+X)%TOTAL:(i+2+X)%TOTAL]
        cells = sum(group)
        if not board[i]:
            if cells in BIRTH:
                buffer[i] = 1
        else:
            if (cells - 1) in SURVIVAL:
                buffer[i] = 1
    board = buffer


def display_board():  # draw cells on OLED
    display.fill(0)
    for i in range(TOTAL):
        if board[i]:
            display.fill_rect((i % X) * DOT_SIZE,
                              (i // X) * DOT_SIZE,
                              DOT_SIZE, DOT_SIZE, 1)
    display.show()


gen, t_start, t_dur = 0, 0, 0

while True:
    gen += 1
    print('Gen {}: {} cell(s) ({} ms)'.format(gen, sum(board), t_dur))
    display_board()
    t_start = utime.ticks_ms()
    calculate_next_gen()
    t_dur = utime.ticks_diff(utime.ticks_ms(), t_start)
