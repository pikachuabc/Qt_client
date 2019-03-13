import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test")



def on_message(client, userdata, msg):
    print(msg.payload.decode())


i=0
client= mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('120.78.172.153')
client.loop_start()
while True:
    client.publish("test",i)
    client.publish("test1",i)
    i+=1
    time.sleep(2)



