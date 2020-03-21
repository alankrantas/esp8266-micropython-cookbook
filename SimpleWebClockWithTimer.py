# Timer-based simple clock with SSD1306 oled display (by Alan Wang)

SSID = "your_wifi_ssid"     # WiFi ssid
PW   = "your_wifi_password" # WiFi password

TMZ_HOUR_OFFSET = 0 # timezone hour offset

import network, urequests, utime, ntptime, ssd1306
from machine import Pin, I2C, Timer

# dictionary for weekday names
weekday = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thr", 4:"Fri", 5:"Sat", 6:"Sun"}

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
            ntptime.settime() # query NTP server
            break
        except:
            utime.sleep(5) # try again if failed

# display update function
def clockUpdate(timer):
    localTime = utime.localtime(utime.time() + TMZ_HOUR_OFFSET * 3600)
    display.fill(0)
    display.text("{0:04d}-{1:02d}-{2:02d} ".format(*localTime) +
                 weekday[localTime[6]], 8, 16)
    display.text("{3:02d}:{4:02d}:{5:02d} ".format(*localTime), 32, 40)
    display.show() # display clock

# update time for the first time
ntpUpdate(None)

# start timers
timer_ntp, timer_display = Timer(-1), Timer(-1)
timer_ntp.init(mode=Timer.PERIODIC, period=900000, callback=ntpUpdate)
timer_display.init(mode=Timer.PERIODIC, period=100, callback=clockUpdate)