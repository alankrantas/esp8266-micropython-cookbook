ssid  = 'ESP8266'  # AP name
pw    = '12345678' # AP password
port  = 80 # server port
conns = 4  # number of channels


from machine import Pin
import network, usocket

led = Pin(2, Pin.OUT, value=1)


# webpage template
html  = r'HTTP/1.1 200 OK' + '\r\n'
html += r'Content-Type: text/html' + '\r\n'
html += r'Connection: close' + '\r\n\r\n'
html += r'<!DOCTYPE html>'
html += r'<html>'
html += r'<head>'
html += r'<title>ESP8266 Web Server</title>'
html += r'<meta name="viewport" content="width=device-width, initial-scale=1">'
html += r'<link rel="icon" href="data:,">'
html += r'<style>body {background-color: Moccasin;} h1 {color: SaddleBrown;} h2 {color: Olive;} </style>'
html += r'</head>'
html += r'<body><center>'
html += r'<h1>ESP8266 Web Server</h1>'
html += r'<h2>LED status: {led_status}</h2>'
html += r'<form methon="GET" action="">'
html += r'<p><input id="led_on" type="submit" name="led" value="On"></p>'
html += r'<p><input id="led_off" type="submit" name="led" value="Off"></p>'
html += r'</form></center></body>'
html += r'</html>'


# generated webpage to be sent to user
def web_page():
    led_status = 'ON' if led.value() == 0 else 'OFF'
    return html.replace('{led_status}', led_status)


# extract any number of parameter names and values from HTTP response
def get_paras(get_str):
    para_dict = {}
    q_pos = get_str.find('/?')
    if q_pos > 0:
        http_pos = get_str.find('HTTP/')
        para_list = get_str[q_pos + 2 : http_pos - 1].split('&')
        for para in para_list:
            para_tmp = para.split('=')
            para_dict.update({para_tmp[0] : para_tmp[1]})
    return para_dict


# start server
print('Starting server...')
wifi = network.WLAN(network.AP_IF)
wifi.config(essid=ssid, password=pw, channel=conns,
            authmode=network.AUTH_WPA_WPA2_PSK)
wifi.active(True)

s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind(('', port))
s.listen(conns)
print('Web server started on', '{} (local ip: http://{}:{})'.format(ssid, wifi.ifconfig()[0], port))


while True:

    # wait for client
    client, addr = s.accept()
    print('Client connected from', addr[0])
    request = client.recv(1024)
    
    # extract url parameters
    request_text = request.decode('utf-8')
    paras = get_paras(request_text)
    
    # control the led
    led_status = paras.get('led', None)
    if led_status == 'On':
        led.value(0)
    else:
        led.value(1)
    
    # send response (web page) to user
    response = web_page()
    client.send(response)
    client.close()
