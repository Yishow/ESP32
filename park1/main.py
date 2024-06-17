import time
import network
from machine import Pin,Timer
from umqtt.simple import MQTTClient

relay1 = Pin(16, Pin.OUT)
relay2 = Pin(17, Pin.OUT)
relay3 = Pin(18, Pin.OUT)
relay4 = Pin(19, Pin.OUT)

print(relay1.value())

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('AX3600', '0986089512')
while not sta_if.isconnected():
    pass
print("connected")

client = MQTTClient(
    client_id="clientXXX", 
    keepalive=600,
    server="192.168.31.121", 
    ssl=False)
client.set_last_will(b'disconnect', b'oh!oh!')
client.connect(False)

state = 0

def get_msg(topic, msg):
    global state
    print('topic: {}'.format(topic),'msg: {}'.format(msg))
    if msg==b"r1_on":
        relay1.value(1)
    elif msg==b"r1_off":
        relay1.value(0)
    elif msg==b"r2_on":
        relay2.value(1)
    elif msg==b"r2_off":
        relay2.value(0)
    elif msg==b"r3_on":
        relay3.value(1)
    elif msg==b"r3_off":
        relay3.value(0)
    elif msg==b"r4_on":
        relay4.value(1)
    elif msg==b"r4_off":
        relay4.value(0)
        
def heartbeat(x):
    client.publish("heartbeat", "alive")

client.set_callback(get_msg)
client.subscribe(b'meebox')
    
tmr1=Timer(1)
tmr1.init(period=300000, mode=Timer.PERIODIC, callback=heartbeat)

counter = 0
while True:
    try:   
        if False:
            client.wait_msg()
        else:
            client.check_msg()          
            #print(counter)
            #counter = counter + 1
            time.sleep(0.2)
    except OSError as e:
        try:
            print("reconnecting...")
            client.connect(False) # 重新連線時也採用 False 不清除會談資料
            client.subscribe(b'meebox')
            print("reconected.")
        except:
            print("waiting for 5 seconds retry...")
            time.sleep(5)
