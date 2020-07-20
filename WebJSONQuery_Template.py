# ESP8266 Web JSON Query Template

import network, urequests, utime
from machine import reset

# user info
wifi_ssid = 'FlagTest' # change this to your WiFi AP name
wifi_pw   = '0233110330'   # change this to your WiFi AP password

# API url
api_url   = 'http://api.open-notify.org/iss-now.json'

# connecting to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_pw)

print('ESP8266 connecting to WiFi:', wifi_ssid)
while not wifi.isconnected():
    pass
print('Connected.')
print('IP:', wifi.ifconfig()[0], '\n')

while True:
    
    # reboot device if WiFi connectio is lost
    if not wifi.isconnected():
        print('WiFi connection lost. Rebooting...')
        reset()
    
    try:
        
        # send HTTP GET request to the API
        print('Querying API:', api_url)
        response = urequests.get(api_url)
        
        if response.status_code == 200:
            print('Query successful. JSON response:')
            # return a dict object containing the JSON data
            parsed = response.json()
            print(parsed) # you can access data by using parsed[key]
   
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
    utime.sleep(15)
