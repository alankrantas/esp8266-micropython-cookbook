# ESP8266/ESP32 MicroPython Cookbook

I publish ESP8266/ESP32 MicroPyton projects from time to time on [Hackster.io](https://www.hackster.io/alankrantas). Here I have some smaller project/scripts I wrote forMicroPython, in which I tried to make the code as short as possible and only use built-in modules.

-- Alan Wang

## Timer-Based Simple Web Clock on SSD1306 OLED Display

<i>File: [SimpleWebClockWithTimer.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/SimpleWebClockWithTimer.py)</i>

One of my very first MicroPython project was a [Web Clock](https://www.hackster.io/alankrantas/very-simple-micropython-esp8266-esp-12-web-clock-3c5c6f) that would query a API every once in a while and display the time on a 128x64 SSD1306 OLED display.

This version uses the built-in <b>ntptime</b> module to update system time, and use two <b>machine.timer</b> to replace the while-loop. It would mess up REPL but works great, with less than 50 lines of code.

Change the SSID and PW variable to your own WiFi AP.

## WS2812 NeoPixel Rainbow/Rotation Effect

<i>File: [WS2812_NeoPixelRainbow.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/WS2812_NeoPixelRainbow.py)</i>

This is my solution to generate rainbow colors on multiple NeoPixel leds and rotate them. It wouldn't work well if you have fewer than 3 leds.

## Conway's Game of Life on SSD1306 OLED Display

<i>File: [ConwayGameOfLife_SSD1306.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/ConwayGameOfLife_SSD1306.py)</i>

Run the simulation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) on the OLED. The rules and the size of cell matrix can both be adjusted.
