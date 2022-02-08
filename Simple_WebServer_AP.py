ssid  = 'ESP8266'  # AP name 
pw    = '12345678' # AP password
port  = 80 # server port
conns = 1  # number of channels


from machine import Pin
import network, usocket

led = Pin(2, Pin.OUT, value=1)


# webpage template
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ESP8266 Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="data:," />
        <style>
            body {
            background-color: Moccasin;
            }
            h1 {
            color: SaddleBrown;
            }
            h2 {
            color: Olive;
            }
        </style>
    </head>
    <body>
        <center>
            <h1>ESP8266 Web Server</h1>
            <h2>LED status: <!--led_status--></h2>
            <form methon="GET" action="">
                <p><input id="led_on" type="submit" name="led" value="On" /></p>
                <p><input id="led_off" type="submit" name="led" value="Off" /></p>
            </form>
        </center>
    </body>
</html>
"""

# add HTTP response headers
http_resp = 'HTTP/1.1 200 OK\r\n' + \
    'Content-Type: text/html\r\n' + \
    'Connection: close\r\n\r\n'

# parse html to a single string
html = http_resp + ''.join([line.strip() for line in html.split('\n')])


# generated webpage to be sent to user
def web_page():
    led_status = 'ON' if led.value() == 0 else 'OFF'
    return html.replace('<!--led_status-->', led_status)

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
print('Web server started on AP',
      '<{}> (local ip: http://{}:{})'.format(ssid, wifi.ifconfig()[0], port))


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
