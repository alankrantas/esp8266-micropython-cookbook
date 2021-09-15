# ESP8266 Web JSON Query Template

import network, urequests, utime, sys

# user info
ssid = '' # change this to your WiFi AP name
pw   = '' # change this to your WiFi AP password

# API url
api_url = 'http://api.open-notify.org/iss-now.json'


# wifi error descriptions
wifi_error = {
    network.STAT_WRONG_PASSWORD: 'wrong password',
    network.STAT_NO_AP_FOUND: 'wifi AP not found',
    -1: 'due to other problems',
    }

# connecting to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)

print('ESP8266 connecting to', ssid, '...')
while wifi.status() == network.STAT_CONNECTING:
    pass
        
if wifi.status() != network.STAT_GOT_IP:
    print('Failed to connect:', wifi_error.get(wifi.status(), wifi_error[-1]))
    sys.exit()

print('Connected.')
print('IP:', wifi.ifconfig()[0], '\n')
utime.sleep(1)


while True:
    
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
    utime.sleep(30)
