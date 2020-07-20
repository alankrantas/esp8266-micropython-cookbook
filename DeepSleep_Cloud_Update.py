# ESP8266 Deep Sleep/Cloud Data Update

# Upload this script onto the board as main.py, then remember to
# connect D0 (GPIO 16) and RST with a jumper wire in order to
# wake the board from deep sleep.

# You can also maunally wake it up by pressing the RST button or
# pull RST low with an external switch.

# After that, you may need to re-flash the firmware to reset ESP8266.

import network, urequests, machine, utime, dht

# user info
wifi_ssid = 'your_wifi_ssid'     # change this to your WiFi AP name
wifi_pw   = 'your_wifi_password' # change this to your WiFi AP password

# IFTTT Webhook key/event name
# see: https://ifttt.com/maker_webhooks
webhook_key        = 'your_ifttt_webhook_key'
webhook_event_name = 'your_ifttt_webhook_event_name'

webhook_url        = 'https://maker.ifttt.com/trigger/' + \
                     webhook_event_name + '/with/key/' + webhook_key


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('ESP8266 woken from a deep sleep...')


# light up onboard LED
led = machine.Pin(2, machine.Pin.OUT, value=0)


# connecting to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

wifi.connect(wifi_ssid, wifi_pw)
while not wifi.isconnected():
    pass


# get readings from DHT11 (connected to D5)
dht = dht.DHT11(machine.Pin(14))
dht.measure()


# Upload data via IFTTT
query_url = '{}?value1={}&value2={}&value3={}'.format(
    webhook_url, 'Temp(*C)/Humid(%)',
    dht.temperature(), dht.humidity())

response = None

try:
    print('Upload data...')
    response = urequests.get(query_url)
except:
    pass

if not response == None and response.status_code == 200:
    print('Upload successful')
     # led flashing quickly
    for _ in range(10):
        led.value(1)
        utime.sleep_ms(25)
        led.value(0)
        utime.sleep_ms(25)
else:
    print('Upload failed')
     # led flashing slowly
    led.value(1)
    utime.sleep_ms(250)
    led.value(0)
    utime.sleep_ms(250)

# led off
led.value(1)


# Go to deep sleep and wake up after a period of time
print('Go to deep sleep...')
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 30000)
machine.deepsleep()
