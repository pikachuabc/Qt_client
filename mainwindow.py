# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
import threading


class Ui_MainWindow(object):
    Qos_number = 0
    IP_number = " "
    topic_content = " "
    display = " "
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(632, 409)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.subscribe_box = QtWidgets.QGroupBox(self.centralWidget)
        self.subscribe_box.setGeometry(QtCore.QRect(50, 100, 531, 201))
        self.subscribe_box.setObjectName("subscribe_box")
        self.server_IP = QtWidgets.QLineEdit(self.subscribe_box)
        self.server_IP.setGeometry(QtCore.QRect(100, 50, 113, 21))
        self.server_IP.setObjectName("server_IP")
        self.topic = QtWidgets.QLineEdit(self.subscribe_box)
        self.topic.setGeometry(QtCore.QRect(100, 80, 113, 21))
        self.topic.setObjectName("topic")
        self.label = QtWidgets.QLabel(self.subscribe_box)
        self.label.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.subscribe_box)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.subscribe_box)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 31, 16))
        self.label_3.setObjectName("label_3")
        self.QoS = QtWidgets.QLineEdit(self.subscribe_box)
        self.QoS.setGeometry(QtCore.QRect(100, 110, 113, 21))
        self.QoS.setObjectName("QoS")
        self.subscribe = QtWidgets.QPushButton(self.subscribe_box)
        self.subscribe.setGeometry(QtCore.QRect(70, 150, 101, 32))
        self.subscribe.setObjectName("subscribe")
        self.receive_box = QtWidgets.QTextBrowser(self.subscribe_box)
        self.receive_box.setGeometry(QtCore.QRect(270, 40, 241, 141))
        self.receive_box.setObjectName("receive_box")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.subscribe.clicked.connect(self.subscribe_submit)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.subscribe_box.setTitle(_translate("MainWindow", "订阅信息"))
        self.label.setText(_translate("MainWindow", "服务器IP地址"))
        self.label_2.setText(_translate("MainWindow", "订阅主题"))
        self.label_3.setText(_translate("MainWindow", "Qos"))
        self.subscribe.setText(_translate("MainWindow", "subscribe"))


    def subscribe_submit(self):
        self.receive_box.clear()
        self.Qos_number = self.QoS.text()
        self.IP_number = self.server_IP.text()
        self.topic_content = self.topic.text()
        print(self.Qos_number)
        print(self.IP_number)
        print(self.topic_content)
        t1 = threading.Thread(target=self.connect)
        t1.setDaemon(True)
        t1.start()
        self.timer = QTimer()     #这里需要self，否则只执行一次
        self.timer.start(1000)
        self.timer.timeout.connect(self.refresh)


    def connect(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.IP_number, 1883, 60)
        client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        #client.subscribe("$SYS/#")
        client.subscribe(self.topic_content)


    def on_message(self,client, userdata, msg):
        print(msg.topic + ":" + msg.payload.decode())
        self.display = msg.topic + ":" + msg.payload.decode()

    def refresh(self):
        self.receive_box.append(self.display)