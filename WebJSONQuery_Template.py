# ESP8266 Web JSON Query Template

import network, urequests, utime
from machine import reset

wifi_ssid = 'your_wifi_ssid'
wifi_pw = 'your_wifi_pw'
api_url = 'https://official-joke-api.appspot.com/random_joke'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_pw)

print('ESP8266 connecting to WiFi:', wifi_ssid)
while not wifi.isconnected():
    pass
print('Connected.')
print('IP:', wifi.ifconfig()[0], '\n')

while True:
    
    if not wifi.isconnected():
        print('WiFi connection lost. Rebooting...')
        reset()
    
    try:
        print('Querying API:', api_url)
        response = urequests.get(api_url)
        
        if response.status_code == 200:
            print('Query successful. JSON response:')
            parsed = response.json()
            print(parsed)
   
        else:
            print('Query failed. ' + \
                  'Status code:', response.status_code)

        response.close()

    except Exception as e:
        print('Error occurred:', e)
        print('If you see a SSL error above, ' + \
              'either you have unstable Wifi or ' + \
              'the API is not supported by MicroPython.')

    print('')
    utime.sleep(10)
