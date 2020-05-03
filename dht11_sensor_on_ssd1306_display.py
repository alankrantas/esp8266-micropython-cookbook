from machine import Pin, I2C
import utime, dht, ssd1306

dht = dht.DHT11(Pin(14))
display = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))
template_str = '\nTemperature:\n {} *C  \n\nHumidity:\n {} % '
    
while True:
    
    dht.measure()
    output_str = template_str.format(dht.temperature(), dht.humidity())
    print(output_str.replace('\n', ''))
    
    display.fill(0)
    for index, line in enumerate(output_str.split('\n')):
        display.text(line, 8, index * 8)
    display.show()
    
    utime.sleep(2)