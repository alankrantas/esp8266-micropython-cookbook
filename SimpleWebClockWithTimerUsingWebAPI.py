# Timer-based clock with SSD1306 oled display (by Alan Wang),
# RTC and World Time API version (automatic timezone)

SSID = '' # WiFi ssid
PW   = '' # WiFi password
SCL  = 5
SDA  = 4

import network, urequests, utime, ssd1306, gc
from machine import Pin, SoftI2C, Timer, RTC

gc.enable()

# weekday names
weekday = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

# setup oled display (SCL -> D1, SDA -> D2)
display = ssd1306.SSD1306_I2C(128, 64, SoftI2C(scl=Pin(SCL), sda=Pin(SDA)))

# inernal RTC
rtc = RTC()

# setup and connect WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PW)
while not wifi.isconnected():
    pass

sec_prev = 0

# time update function
def rtcUpdate(timer):
    while True:
        try:
            response = urequests.get('http://worldtimeapi.org/api/ip')
            if response.status_code == 200:
                parsed = response.json()
                # parsed['unixtime']: local unixtime since 1970/01/01 00:00:00)
                # parsed['raw_offset']: timezone hour offset
                # 946684800: unixtime of 2020/01/01 00:00:00 (system start time on MicroPython)
                # generate datetime tuple based on these information
                dt = utime.localtime(parsed['unixtime'] + parsed['raw_offset'] - 946684800)
                # rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))
                rtc.datetime((dt[0], dt[1], dt[2], dt[6], dt[3], dt[4], dt[5], 0))
                break
        except:
            utime.sleep(10) # try again if failed

# display update function
def clockUpdate(timer):
    global sec_prev
    dt = rtc.datetime()
    if dt[6] != sec_prev:
        display.fill(0)
        display.text(weekday[dt[3]], 8, 8)
        display.text('{0:04d}-{1:02d}-{2:02d}'.format(*dt), 8, 24)
        display.text('{4:02d}:{5:02d}:{6:02d}'.format(*dt), 8, 40)
        display.show() # display clock
    sec_prev = dt[6]

# update time for the first time
rtcUpdate(None)

# start timers
timer_ntp, timer_display = Timer(-1), Timer(-1)
timer_ntp.init(mode=Timer.PERIODIC, period=900000, callback=rtcUpdate)
timer_display.init(mode=Timer.PERIODIC, period=100, callback=clockUpdate)
