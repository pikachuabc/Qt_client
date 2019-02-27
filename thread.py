from PyQt5.QtCore import *
import time
import paho.mqtt.client as mqtt



class RunThread(QThread):
    signal = pyqtSignal(str)
    Qos_number = 0      #Qos质量
    IP_number = " "     #连接服务器的IP地址
    topic_content = " " #订阅主题名称
    display = " "       #返回内容
    def __init__(self,IP_number,topic_content):
        super(RunThread,self).__init__()
        self.IP_number = IP_number
        self.topic_content = topic_content

    def run(self):
        self.connect()

    '''创建pahomqtt实例，并尝试连接'''
    def connect(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.IP_number, 1883, 60)
        client.loop_forever()

    '''连接状态回调函数'''
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        #client.subscribe("$SYS/#")
        client.subscribe(self.topic_content)
        self.signal.emit(rc)


    '''接受消息的回调函数'''
    def on_message(self,client, userdata, msg):
        print(msg.topic + ":" + msg.payload.decode())
        self.signal.emit(msg.topic + ":" + msg.payload.decode())


