import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test")





def on_message(client, userdata, msg):
    print(msg.topic + ":" + msg.payload.decode())
    #print(userdata)



i=0
client = mqtt.Client(client_id="nihao")
client.on_message = on_message
client.on_connect = on_connect
client.user_data_set("nihao")
client.connect("120.78.172.153")
client.loop_start()
while True:
    client.publish("test",i)
    time.sleep(2)
    i+=1