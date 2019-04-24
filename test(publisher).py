import paho.mqtt.client as mqtt
import sqlite3
import base64
import time
import json

pub_topic = "picture"
HOST = '120.78.172.153'
#HOST = '192.168.1.104'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)+",连接成功")
    client.subscribe("picture")


def send_img():
    path= input("请输入发送照片路径")
    base64_data = base64.b64encode(open(path,'rb').read())
    print(base64_data)
    client.publish(pub_topic,base64_data,1)

def send_Vid():
    path = input("请输入发送音频路径")
    base64_data = base64.b64encode(open(path,'rb').read())
    print(base64_data)
    client.publish("voice",base64_data,1)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(HOST)
    client.loop_start()
    
    test = {}
    while True:
        #client.publish("sensor",a)
        # try:
        #     send_img()
        # except:
        #     pass
        client.publish('sensor',)
        #send_Vid()
        # a = input("1：发送图片  2：发送音频 3:文字")
        # if a == 1:
        #     send_img()
        # else:
        #     send_Vid()



