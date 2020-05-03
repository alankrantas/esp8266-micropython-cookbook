from machine import Pin, I2C
import utime, dht, ssd1306

# DHT11 sensor (Pin D5)
dht = dht.DHT11(Pin(14))

# SSD1306 OLED display (SCL: D1, SDA: D2)
display = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))

# template string for formatting
template_str = '\nTemperature:\n {} *C  \n\nHumidity:\n {} % '
    
while True:
    
    # get readings from DHT11
    dht.measure()
    
    # generate formatted string
    output_str = template_str.format(dht.temperature(), dht.humidity())
    
    # print output without \n (new line) character
    print(output_str.replace('\n', ''))

    # print output on oled
    display.fill(0)
    for index, line in enumerate(output_str.split('\n')):
        display.text(line, 8, index * 8)
    display.show()
    
    # wait for 2 seconds
    utime.sleep(2)
