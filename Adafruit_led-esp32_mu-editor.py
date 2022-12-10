from machine import Pin
import network
from time import sleep
import sys
from umqtt.simple import MQTTClient

LED = Pin(2,Pin.OUT)

SSID = 'WiFi Name'
PASS = 'WiFi Password'

CLIENT_ID = 'Random Client_ID'
SERVER = 'io.adafruit.com'
USERNAME = 'Adafruit IO_Username'
PASSWORD = 'Adafruit IO_Key'

client = MQTTClient(client_id = CLIENT_ID,
                    server = SERVER,
                    user = USERNAME,
                    password = PASSWORD)

FEED_KEY = 'led'

topic = USERNAME + '/feeds/'  + FEED_KEY

topic = bytes(topic,'utf-8')

def cb(topic,msg):
    print('Topic=',topic, 'Msg=', msg)
    msg=str(msg,'utf-8')
    print(type(msg))
    if (msg=='1'):
        LED.value(1)
        print('LED ON')
    else:
        LED.value(0)
        print('LED OFF')
        

def connectWifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(False)
    sleep(0.5)
    wifi.active(True)
    wifi.connect(SSID, PASS)
    sleep(2)
    if (wifi.isconnected()):
        print('Connected')
    else:
        print('Not Connected')
        sys.exit()
        
connectWifi()

try:
    client.connect()
except:
    print('Not Connected to MQTT Broker')
    sys.exit()

client.set_callback(cb)
client.subscribe(topic)

while True:
    client.check_msg()
