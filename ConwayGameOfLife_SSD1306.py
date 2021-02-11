# Conway's Game of Life on 128x64 SSD1306 OLED and ESP8266 (by Alan Wang)

# game rule
B = '3'  # number of nearby cells to give birth of a new cell
S = '23' # number of nearby cells to sustain an existing cell 
matrix_factor = 3 # matrix factor (3 -> 128/3 x 64/3 -> 42 x 21)
random_bit_num = 2 # initial randomize factor (2 = 2^2 (1/4 chance))

# ------------------------------------------------------------

import urandom, gc
from machine import Pin, I2C, ADC, freq
from ssd1306 import SSD1306_I2C

freq(160000000) # set cpu to 160 MHz
gc.enable()


# randomize seed from floating analog readings
adc = ADC(0)
seed = 0
for _ in range(1000):
    seed += adc.read()
seed *= 10
urandom.seed(seed * 10)

B_list = [int(b) for b in B]
S_list = [int(s) for s in S]
matrix_size_x = 128 // matrix_factor
matrix_size_y = 64 // matrix_factor

matrix = [bytearray(urandom.getrandbits(random_bit_num) == 0
                    for _ in range(matrix_size_y))
          for _ in range(matrix_size_x)]

print('Conway\'s Game of Life: matrix size {} x {}'.format(
    matrix_size_x, matrix_size_y))

oled = SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))
generation = 0


# calculate next generation
def calculate_next_gen():
    global matrix
    matrix_buf = [bytearray([0] * matrix_size_y)
                  for _ in range(matrix_size_x)]
    for i in range(matrix_size_x):
        for j in range(matrix_size_y):
            cell_count = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if not (k == 0 and l == 0):
                        x = i + k
                        y = j + l
                        if x < 0:
                            x = matrix_size_x - 1
                        elif x >= matrix_size_x:
                            x = 0
                        if y < 0:
                            y = matrix_size_y - 1
                        elif y >= matrix_size_y:
                            y = 0
                        if matrix[x][y]:
                            cell_count += 1
            if not matrix[i][j]:
                if cell_count in B_list:
                    matrix_buf[i][j] = 1
            else:
                if cell_count in S_list:
                    matrix_buf[i][j] = 1
    matrix = matrix_buf
    del matrix_buf


# display cells on OLED
def display_matrix():
    oled.fill(0)
    for i in range(matrix_size_x):
        for j in range(matrix_size_y):
            if matrix[i][j]:
                oled.fill_rect(i * matrix_factor, j * matrix_factor,
                               matrix_factor, matrix_factor, 1)
    oled.show()


# start game of life
while True:
    generation += 1
    cell_count = sum(map(sum, matrix))
    print('Generation {}: {} cell(s)'.format(generation, cell_count))
    display_matrix()
    calculate_next_gen()
    gc.collect()
