from PyQt5.QtCore import *
import time
import paho.mqtt.client as mqtt


'''
继承Qthread，实现在子线程中修改主线程UI，传入参数为服务器IP地址，订阅主题
'''
class Client_RunThread(QThread):
    signal = pyqtSignal(str) #slot信号
    Qos_number = 0      #Qos质量
    IP_number = " "     #连接服务器的IP地址
    topic_content = " " #订阅主题名称
    client = mqtt.Client()  #客户端实例

    def __init__(self,IP_number,topic_content):
        super(Client_RunThread,self).__init__()
        self.IP_number = IP_number
        self.topic_content = topic_content


    '''override原run函数'''
    def run(self):
        self.connect()  #创建mqtt线程

    '''创建pahomqtt实例，并尝试连接'''
    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.IP_number, 1883, 60)
        self.client.loop_forever()

    '''连接状态回调函数'''
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        #client.subscribe("$SYS/#")
        self.client = client
        client.subscribe(self.topic_content)
        self.signal.emit(rc)


    '''接受消息的回调函数'''
    def on_message(self,client, userdata, msg):
        #print(msg.topic + ":" + msg.payload.decode())
        self.signal.emit(msg.topic + ":" + msg.payload.decode())
