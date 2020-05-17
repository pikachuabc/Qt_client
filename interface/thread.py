from PyQt5.QtCore import *
import time
import paho.mqtt.client as mqtt
import json
import mysql.connector
from interface import main

config = {"user":"root",
          "host":"127.0.0.1",
          "database":"IIoT"}  #数据连接配置

'''
继承Qthread，实现在mqtt子线程中修改主线程UI，传入参数为服务器IP地址，订阅主题
'''
class Client_RunThread(QThread):

    signal = pyqtSignal(str) #slot信号用于触发接受显示
    signal1 = pyqtSignal(str) #slot信号用于触发图片显示和存储
    signal2 = pyqtSignal(str) #slot信号用于触发音频存储
    err_signal = pyqtSignal(int) #错误提醒
    is_connect = False


    Qos_number = 0      #Qos质量
    IP_number = " "     #连接服务器的IP地址
    topic_content = " " #订阅主题名称
    User_Name = " "     #客户端名称
    client = mqtt.Client()  #客户端实例
    cnx = None      #数据库连接实例
    add_value = ("insert into IIoT.Sensor"
                 "(time,value,sensorType,sensorID)"
                 "values (%s,%s,%s,%s)")   #添加数据形式


    def __init__(self,IP_number,topic_content,User_Name,Qos_number):
        super(Client_RunThread,self).__init__()
        self.IP_number = IP_number
        self.topic_content = topic_content
        self.User_Name = User_Name
        self.Qos_number = Qos_number


    '''override原run函数'''
    def run(self):
        try:
            self.connect()  # 创建mqtt线程
        except:
            self.err_signal.emit(1)


    '''创建pahomqtt实例，并尝试连接'''
    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.IP_number, 1883, 60)
        self.is_connect = True
        self.client.loop_forever()

    '''连接状态回调函数'''
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client = client
        client.subscribe(topic=self.topic_content,qos=int(self.Qos_number))
        self.signal.emit("已订阅主题{0},订阅质量为Qos{1}".format(self.topic_content,self.Qos_number))


    '''接受消息的回调函数'''
    def on_message(self,client, userdata, msg):
        recData = json.loads(msg.payload)
        if recData['type'] == '0':
            try:
                self.cnx = mysql.connector.connect(**config)  # 数据库连接实例
                self.cnx.connect(**config)
                self.curs = self.cnx.cursor()
                data_value = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),recData['value'],recData['sensorType'],recData['sensorID'])
                self.curs.execute(self.add_value,data_value)
                self.cnx.commit()
                self.curs.close()
                self.cnx.close()
            except:
                self.signal.emit("数据库连接失败，以下数据将不会被存入数据库")
            self.signal.emit(msg.topic+":"+recData['value'].replace("\n",''))
        elif recData['type'] == '1':
            self.signal1.emit(recData['picture'])
        elif recData['type'] == '2':
            self.signal2.emit(recData['voice'])
        else:
            self.signal.emit("未知消息格式")
        # if msg.topic =="picture":
        #     self.signal1.emit(msg.payload.decode())
        # elif msg.topic =="voice":
        #     self.signal2.emit(msg.payload.decode())
        # elif msg.topic =="sensor":
        #     try:
        #         self.cnx = mysql.connector.connect(**config)  # 数据库连接实例
        #         self.cnx.connect(**config)
        #         self.curs = self.cnx.cursor()
        #         data_value = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),msg.payload.decode())
        #         self.curs.execute(self.add_value,data_value)
        #         self.cnx.commit()
        #         self.curs.close()
        #         self.cnx.close()
        #     except:
        #         self.signal.emit("数据库连接失败，以下数据将不会被存入数据库")
        #     self.signal.emit(msg.topic + ":" + msg.payload.decode())
        # else:
        #     self.signal.emit(msg.topic + ":" + msg.payload.decode())
            #main.ui.signal.emit(msg.topic + ":" + msg.payload.decode())
