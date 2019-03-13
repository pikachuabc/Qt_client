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

  #  ClientThread = None       #MQTT客户端线程

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

        self.QoS = QtWidgets.QLineEdit(self.subscribe_box)
        self.QoS.setGeometry(QtCore.QRect(100, 110, 113, 21))
        self.QoS.setObjectName("QoS")

        self.UserName = QtWidgets.QLineEdit(self.subscribe_box)
        self.UserName.setGeometry(QtCore.QRect(100, 140, 113, 21))
        self.UserName.setObjectName("UserName")

        self.label_1 = QtWidgets.QLabel(self.subscribe_box)
        self.label_1.setGeometry(QtCore.QRect(20, 50, 81, 16))
        self.label_1.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.subscribe_box)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 60, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.subscribe_box)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 31, 16))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.subscribe_box)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 81, 16))
        self.label_4.setObjectName("label_4")

        self.subscribe = QtWidgets.QPushButton(self.subscribe_box)
        self.subscribe.setGeometry(QtCore.QRect(10, 190, 101, 32))
        self.subscribe.setObjectName("subscribe")

        self.unsubscribe = QtWidgets.QPushButton(self.subscribe_box)
        self.unsubscribe.setGeometry(QtCore.QRect(120, 190, 101, 32))
        self.unsubscribe.setObjectName("unsubscribe")

        self.clear = QtWidgets.QPushButton(self.subscribe_box)
        self.clear.setGeometry(QtCore.QRect(10, 220, 101, 32))
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
        self.label_1.setText(_translate("MainWindow", "IP Adress"))
        self.label_2.setText(_translate("MainWindow", "Sub Topic"))
        self.label_3.setText(_translate("MainWindow", "Qos"))
        self.label_4.setText(_translate("MainWindow","User Name"))
        self.subscribe.setText(_translate("MainWindow", "subscribe"))
        self.unsubscribe.setText(_translate("MainWindow", "unsubscribe"))
        self.clear.setText(_translate("MainWindow", "clear"))

        self.server_IP.setText("120.78.172.153")
        self.topic.setText("$SYS/#")
        self.QoS.setText("0")

    '''按下subscribe后执行动作'''
    def NewClient(self):
        if self.QosCheck():
            pass
        else:
            return
        try:
            self.ClientThread.client.unsubscribe(self.topic.text()) #如果用户重复点击订阅的话先取消之前的订阅并订阅新主题
            self.receive_box.clear()
            self.ClientThread.client.subscribe(topic=self.topic.text(),qos = int(self.QoS.text()))
            self.receive_box.append("订阅主题{0},订阅质量为Qos{1}".format(self.topic.text(),self.QoS.text()))
            self.receive_box.repaint()
        except:
            self.receive_box.clear()
            self.ClientThread = thread.Client_RunThread(IP_number=self.server_IP.text(),topic_content=self.topic.text(),User_Name=self.UserName.text(),Qos_number=self.QoS.text())
            self.ClientThread.signal.connect(self.Refresh)    #将子线程的信号连接到主线程的刷新函数上
            self.ClientThread.start()

        self.UserName.setEnabled(False)     #阻止用户再次修改内容
        self.QoS.setEnabled(False)
        self.topic.setEnabled(False)
        self.server_IP.setEnabled(False)

    def Unsubscribe(self):
        try:
            self.ClientThread.client.unsubscribe(self.topic.text())
            self.receive_box.append("您已取消主题：{}的订阅".format(self.topic.text()))
            self.receive_box.repaint()
        except:
            self.receive_box.append("当前未订阅任何主题")
            self.receive_box.repaint()

        self.UserName.setEnabled(True)
        self.QoS.setEnabled(True)
        self.topic.setEnabled(True)
        self.server_IP.setEnabled(True)

    """
    用于将接收到的消息显示于窗体中
    """
    def Refresh(self,msg):
        self.receive_box.append(msg)    #将收到的消息显示在接受框中

    """
    清屏
    """
    def Clear(self):
        self.receive_box.clear()
        self.receive_box.repaint()

    """
    Qos参数检测
    """
    def QosCheck(self):
        if int(self.QoS.text())==0 or int(self.QoS.text())==1 or int(self.QoS.text())==2:
            return True
        else:
            self.receive_box.append("Qos等级为0-2！")
            self.receive_box.repaint()
            return False
