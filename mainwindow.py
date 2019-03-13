# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
import threading
import thread

"""
窗体类
"""
class Ui_MainWindow(object):
    Qos_number = 0      #Qos质量
    IP_number = " "     #连接服务器的IP地址
    topic_content = " " #订阅主题名称
    display = " "       #返回内容
    ClientThread = None       #MQTT客户端线程
    client = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(632, 409)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        #创建容器
        self.centralWidget.setObjectName("centralWidget")

        self.subscribe_box = QtWidgets.QGroupBox(self.centralWidget)
        self.subscribe_box.setGeometry(QtCore.QRect(50, 50, 531, 301))
        self.subscribe_box.setObjectName("subscribe_box")

        self.server_IP = QtWidgets.QLineEdit(self.subscribe_box)
        self.server_IP.setGeometry(QtCore.QRect(100, 50, 113, 21))
        self.server_IP.setObjectName("server_IP")

        self.topic = QtWidgets.QLineEdit(self.subscribe_box)
        self.topic.setGeometry(QtCore.QRect(100, 80, 113, 21))
        self.topic.setObjectName("topic")

        self.label = QtWidgets.QLabel(self.subscribe_box)
        self.label.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.subscribe_box)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 60, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.subscribe_box)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 31, 16))
        self.label_3.setObjectName("label_3")

        self.QoS = QtWidgets.QLineEdit(self.subscribe_box)
        self.QoS.setGeometry(QtCore.QRect(100, 110, 113, 21))
        self.QoS.setObjectName("QoS")

        self.subscribe = QtWidgets.QPushButton(self.subscribe_box)
        self.subscribe.setGeometry(QtCore.QRect(10, 150, 101, 32))
        self.subscribe.setObjectName("subscribe")

        self.unsubscribe = QtWidgets.QPushButton(self.subscribe_box)
        self.unsubscribe.setGeometry(QtCore.QRect(120, 150, 101, 32))
        self.unsubscribe.setObjectName("unsubscribe")

        self.clear = QtWidgets.QPushButton(self.subscribe_box)
        self.clear.setGeometry(QtCore.QRect(10, 180, 101, 32))
        self.clear.setObjectName("clear")

        self.receive_box = QtWidgets.QTextBrowser(self.subscribe_box)
        self.receive_box.setGeometry(QtCore.QRect(270, 40, 241, 241))
        self.receive_box.setObjectName("receive_box")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        '''逻辑功能'''
        self.subscribe.clicked.connect(self.NewClient)
        self.unsubscribe.clicked.connect(self.Unsubscribe)
        self.clear.clicked.connect(self.Clear)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.subscribe_box.setTitle(_translate("MainWindow", "Client Interface"))
        self.label.setText(_translate("MainWindow", "IP Adress"))
        self.label_2.setText(_translate("MainWindow", "Sub Topic"))
        self.label_3.setText(_translate("MainWindow", "Qos"))
        self.subscribe.setText(_translate("MainWindow", "subscribe"))
        self.unsubscribe.setText(_translate("MainWindow", "unsubscribe"))
        self.clear.setText(_translate("MainWindow", "clear"))

        self.server_IP.setText("120.78.172.153")
        self.topic.setText("$SYS/#")

    '''按下subscribe后执行动作'''
    def NewClient(self):
        try:
            self.ClientThread.client.unsubscribe(self.topic_content) #再次点击先取消之前的订阅并订阅新主题
            self.receive_box.clear()
            self.topic_content = self.topic.text()
            self.ClientThread.client.subscribe(self.topic_content)
        except:
            self.receive_box.clear()
            self.Qos_number = self.QoS.text()
            self.IP_number = self.server_IP.text()
            self.topic_content = self.topic.text()
            # print(self.Qos_number)
            # print(self.IP_number)
            # print(self.topic_content)
            self.ClientThread = thread.Client_RunThread(IP_number=self.IP_number,topic_content=self.topic_content)
            self.ClientThread.signal.connect(self.Refresh)    #将子线程的信号连接到主线程的刷新函数上
            self.ClientThread.start()

    def Unsubscribe(self):
        try:
            self.ClientThread.client.unsubscribe(self.topic_content)
        except:
            self.receive_box.append("当前未订阅任何主题")
            self.receive_box.repaint()

    def Refresh(self,msg):
        self.receive_box.append(msg)    #将收到的消息显示在接受框中

    def Clear(self):
        self.receive_box.clear()
        self.receive_box.repaint()
