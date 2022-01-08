# ESP8266 MicroPython Cookbook

![Micropython-logo svg](https://user-images.githubusercontent.com/44191076/79063718-e5975580-7cd5-11ea-90a2-6f350adfb0cd.png)

I publish ESP8266/ESP32 MicroPyton projects from time to time on [Hackster.io](https://www.hackster.io/alankrantas). Here I have some smaller project/scripts I wrote forMicroPython, in which I tried to make the code as simple as possible and only use built-in modules.

-- Alan Wang

## Hello World (Blinky)

```python
from machine import Pin
import utime

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    utime.sleep_ms(500)
```

or

```python
from machine import Pin, Timer

led = Pin(2, Pin.OUT)

timer = Timer(-1)
timer.init(mode=Timer.PERIODIC, period=500,
           callback=lambda _: led.value(not led.value()))
```

## Simple Timer-Based Simple Web Clock on SSD1306

<i>File: [SimpleWebClockWithTimer.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/SimpleWebClockWithTimer.py)</i>

A simple web clock that update system RTC time every 15 minutes via NTP server. It uses two <b>machine.timer</b>s instead of a while loop, reducing the code down to less than 40 actual lines. Change the SSID and PW to your own WiFi AP.

The <i>[SimpleWebClockWithTimerUsingWebAPI.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/SimpleWebClockWithTimerUsingWebAPI.py)</i> version works the same but use [World Time API](http://worldtimeapi.org/) to query time instead and update it via the machine.RTC module. Since the API can detect your timezone, you don't need to set it in this version.

## Display DHT11 Sensor Readings on SSD1306

<i>File: [DHT11_Sensor_SSD1306.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/DHT11_Sensor_SSD1306.py)</i>

A simple example of displaying DHT11's temperature and humidity readings on SSD1306 OLED as well as printing them in REPL. A very basic weather station.

Change dht.DHT11 to dht.DHT22 if you are using a DHT22 sensor.

## Simple Web Server

<i>File: [Simple_WebServer.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/Simple_WebServer.py)</i>

A simple web server in STA mode (connect to your WiFi and you can access a webpage from a web browser). You'll have to connect the ESP8266 on your computer to read the actual IP it get. This example allows you to turn the onboard LED on or off.

<i>File: [Simple_WebServer_AP.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/Simple_WebServer_AP.py)</i>

This is the AP mode version, which will start its own WiFi AP (works without externam WiFi). Connect the AP (default named "ESP8266") from your device and open http://192.168.4.1 in your browser.

## Web JSON Query Template

<i>File: [WebJSONQuery_Template.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/WebJSONQuery_Template.py)</i>

A template for querying a API and get its JSON response. The JSON response would be a dictionary object, in which you can extract any data you need.

Note: if you get a SSL error (like "TLS buffer overflow" and/or "ssl_handshake_status: -xxx"), either your WiFi is unstable or the API is not fully supported by MicroPython.

## Deep Sleep/Cloud Data Update

<i>File: [DeepSleep_Cloud_Update.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/DeepSleep_Cloud_Update.py)</i>

This use deep sleep to make the board wake up every 30 seconds and upload readings of a DHT11 via IFTTT's Webhook service (in my case the data would be uploaded to a Google Drive spreadsheet).

The script must be uploaded onto the board in order to make deep sleep work. Connect D0 (GPIO 16) and RST before you powering it up. Afterwards the board's REPL may not be responsive and you'll have to re-flash the firmware. 

## WS2812 NeoPixel Rainbow/Rotation Effect

<i>File: [WS2812_NeoPixelRainbow.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/WS2812_NeoPixelRainbow.py)</i>

Based on Adafruit's NeoPixel example code, here I extended the original NeoPixel class to add some convenient methods.

## Conway's Game of Life on SSD1306

<i>File: [ConwayGameOfLife_SSD1306.py](https://github.com/alankrantas/esp8266-micropython-cookbook/blob/master/ConwayGameOfLife_SSD1306.py)</i>

Run the simulation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) on the SSD1306 OLED display. The rules and the size of cell matrix can both be adjusted. Here I use a single-dimension list to simplify the code.
