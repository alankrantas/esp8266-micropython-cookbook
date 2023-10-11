# Timer-based simple clock with SSD1306 oled display (by Alan Wang)

SSID = ''           # WiFi ssid
PW   = ''           # WiFi password
TMZ_HOUR_OFFSET = 8 # timezone hour offset
SCL  = 5
SDA  = 4

import network, ntptime, time, ssd1306, gc
from machine import Pin, SoftI2C, Timer

gc.enable()

# weekday names
weekday = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# setup oled display (SCL -> D1, SDA -> D2)
display = ssd1306.SSD1306_I2C(128, 64, SoftI2C(scl=Pin(SCL), sda=Pin(SDA)))

# setup and connect WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PW)
while not wifi.isconnected():
    pass

sec_prev = 0

# time update function
def ntpUpdate(timer):
    while True:
        try:
            ntptime.settime() # query NTP server and update system time
            break
        except:
            time.sleep(5) # try again if failed

# display update function
def clockUpdate(timer):
    global sec_prev
    lt = time.localtime(time.time() + TMZ_HOUR_OFFSET * 3600)
    if lt[5] != sec_prev:
        display.fill(0)
        display.text(weekday[lt[6]], 8, 8)
        display.text('{0:04d}-{1:02d}-{2:02d}'.format(*lt), 8, 24)
        display.text('{3:02d}:{4:02d}:{5:02d}'.format(*lt), 8, 40)
        display.show() # display clock
    sec_prev = lt[5]

# update time for the first time
ntpUpdate(None)

# start timers (coroutines)
timer_ntp, timer_display = Timer(-1), Timer(-1)
timer_ntp.init(mode=Timer.PERIODIC, period=900000, callback=ntpUpdate)
timer_display.init(mode=Timer.PERIODIC, period=100, callback=clockUpdate)
