# ESP8266 MicroPython Cookbook

![Micropython-logo svg](https://user-images.githubusercontent.com/44191076/79063718-e5975580-7cd5-11ea-90a2-6f350adfb0cd.png)

I publish ESP8266/ESP32 MicroPyton projects from time to time on [Hackster.io](https://www.hackster.io/alankrantas). Here I have some smaller project/scripts I wrote forMicroPython, in which I tried to make the code as simple as possible and only use built-in modules.

-- Alan Wang

## ESP8266 Boards

As far as I can tell, most ESP8266 boards basically functions the same. A NodeMCU V2 (not V3), WeMos D1 (Arduino Uno-style) or WeMos D1 mini is probably your best choise.

## Timer-Based Simple Web Clock on SSD1306 OLED Display

<i>File: [SimpleWebClockWithTimer.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/SimpleWebClockWithTimer.py)</i>

A mini web clock that update system RTC time every 15 minutes via NTP server. It uses two <b>machine.timer</b>s instead of a while loop, reducing the code down to less than 40 actual lines. Change the SSID and PW to your own WiFi AP.

### SSD1306 OLED Display

SSD1306 is a monochrome display, either in 128x64 (0.96") or 128x32 (0.91"), might be blue and/or yellow or white. MicroPython for ESP8266 has a built-in display module with 8x8 fonts from the framebuf module.

Here I use the I2C version with 4 pins:

* Vcc -> 3V3 or 5V
* Gnd -> G
* SCL -> D1 (GPIO 5)
* SDA -> D2 (GPIO 4)

Beware that some Chinese-made SSD1306s do not return I2C ACK signals and will not work for MicroPython.

## Web JSON Query Template

<i>File: [WebJSONQuery_Template.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/WebJSONQuery_Template.py)</i>

A template for querying a API and get its JSON response. The JSON response would be a dictionary object, in which you can extract data that you need.

Note: if you see SSL error (like "TLS buffer overflow" and/or "ssl_handshake_status: -xxx"), either your WiFi is unstable or the API is not supported by MicroPython.

## WS2812 NeoPixel Rainbow/Rotation Effect

<i>File: [WS2812_NeoPixelRainbow.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/WS2812_NeoPixelRainbow.py)</i>

Generate rainbow colors on multiple NeoPixel leds and rotate them (clockwise or else). The number of LEDs and brightness level can be adjusted.

## Conway's Game of Life on SSD1306 OLED Display

<i>File: [ConwayGameOfLife_SSD1306.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/ConwayGameOfLife_SSD1306.py)</i>

Run the simulation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) on OLED. The rules and the size of cell matrix can both be adjusted. 
