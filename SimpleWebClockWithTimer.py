# Timer-based simple clock with SSD1306 oled display (by Alan Wang)

SSID = ''           # WiFi ssid
PW   = ''           # WiFi password
TMZ_HOUR_OFFSET = 0 # timezone hour offset

import network, ntptime, utime, ssd1306
from machine import Pin, I2C, Timer

# dictionary for weekday names
weekday = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# setup oled display (SCL -> D1, SDA -> D2)
display = ssd1306.SSD1306_I2C(128, 64, I2C(scl=Pin(5), sda=Pin(4)))

# setup and connect WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PW)
while not wifi.isconnected():
    pass

# time update function
def ntpUpdate(timer):
    while True:
        try:
            ntptime.settime() # query NTP server and update system time
            break
        except:
            utime.sleep(5) # try again if failed

# display update function
def clockUpdate(timer):
    localTime = utime.localtime(utime.time() + TMZ_HOUR_OFFSET * 3600)
    display.fill(0)
    display.text(weekday[localTime[6]], 8, 8)
    display.text('{0:04d}-{1:02d}-{2:02d}'.format(*localTime), 8, 24)
    display.text('{3:02d}:{4:02d}:{5:02d}'.format(*localTime), 8, 40)
    display.show() # display clock

# update time for the first time
ntpUpdate(None)

# start timers (coroutines)
timer_ntp, timer_display = Timer(-1), Timer(-1)
timer_ntp.init(mode=Timer.PERIODIC, period=900000, callback=ntpUpdate)
timer_display.init(mode=Timer.PERIODIC, period=100, callback=clockUpdate)
