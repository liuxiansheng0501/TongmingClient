#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : Main.py 
    Time    : 2018/01/14 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""


from datetime import datetime,time,timedelta
from time import sleep
import sys
import time
import pandas as pd
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import configparser
import requests
from ui.main import Ui_main
from ui.login import Ui_login
import urls

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

weekday={0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期日"}

class Login(QDialog, Ui_login): #登录
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.intial_login_setting()

    def intial_login_setting(self):
        conf = configparser.ConfigParser()
        conf.read("../config")
        if 'user' in conf.sections():
            if int(conf.get('login', 'auto_login')) == 1: # 如果记录自动登录
                self.input_username.setText(conf.get('user', 'id'))
                self.input_passwd.setText(conf.get('user', 'password'))
                self.input_passwd.setEchoMode(QLineEdit.Password)
                self.checkBox_rem_passwd.setChecked(True)
                self.checkBox_auto_login.setChecked(True)
                # TODO:自动登录还没实现
            elif int(conf.get('login', 'remember_passwd'))==1: # 只选择了记住密码
                self.input_username.setText(conf.get('user', 'id'))
                self.input_passwd.setText(conf.get('user', 'password'))
                self.input_passwd.setEchoMode(QLineEdit.Password)
                self.checkBox_rem_passwd.setChecked(True)
            else: # 两项均没有选择
                self.input_username.setText(conf.get('user', 'id'))
                self.input_passwd.setEchoMode(QLineEdit.Password)
        else:
            self.input_passwd.setEchoMode(QLineEdit.Password)
            pass

    def update_login_setting(self):
        conf = configparser.ConfigParser()
        conf.read("../config")
        indicator_list = conf.sections()
        node = "user"
        key = "user_ip"
        value = "192.168.1.102"
        conf.set(node, key, value)
        fh = open("../config", 'w')
        conf.write(fh)  # 把要修改的节点的内容写到文件中
        fh.close()

    @pyqtSlot()
    def on_btn_login_clicked(self): # 点击登录
        # if 'user' not in conf.sections(): #用户手册登录，与远端服务器验证
        if self.verification_login_remote():
            self.update_setting_login()
            self.accept()
        else:
            pass

    def verification_login_remote(self):# 首次远程登录验证
        if self.verify_user_passwd():
            return False
        else:
            payload = (('account', self.input_username.text()), ('passwd', self.input_passwd.text()))
            try:
                res = requests.post(urls.doc_login, data=payload)
                if res.ok:
                    res=res.json()
                    conf = configparser.ConfigParser()
                    conf.read("../config")
                    if 'user' not in conf.sections():
                        conf.add_section('user')
                    conf.set('user', 'id', res['account'])
                    conf.set('user', 'name', res['name'])
                    conf.set('user', 'hospital', res['hospital'])
                    conf.set('user', 'type', res['type'])
                    conf.set('user', 'title', res['title'])
                    conf.set('user', 'password', res['passwd'])
                    fh = open("../config", 'w')
                    conf.write(fh)  # 把要修改的节点的内容写到文件中
                    fh.close()
                    return True
                else:
                    res=res.json()
                    self.label_login_tips.setText(res['message'])
                    self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
                    return False
            except:
                self.label_login_tips.setText(u"网络服务故障！")
                self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
                return False

    def verification_login_local(self):# 本地登录验证
        if self.verify_user_passwd():
            return False
        else:
            conf = configparser.ConfigParser()
            conf.read("../config")
            if self.input_username.text()==conf.get('user', 'id') and self.input_passwd.text()==conf.get('user', 'password'):
                return True
            elif self.input_username.text()==conf.get('user', 'id') and self.input_passwd.text()!=conf.get('user', 'password'):
                self.label_login_tips.setText(u"密码错误，请重新输入！")
                self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
                return False
            elif self.input_username.text()!=conf.get('user', 'id') and self.input_passwd.text()==conf.get('user', 'password'):
                self.label_login_tips.setText(u"用户名错误，请重新输入！")
                self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
                return False

    def verify_user_passwd(self):
        if len(self.input_username.text())==0 and len(self.input_passwd.text())>0:
            self.label_login_tips.setText(u"请输入用户名！")
            self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
            return True
        elif len(self.input_passwd.text())==0 and len(self.input_username.text())>0:
            self.label_login_tips.setText(u"请输入密码！")
            self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
            return True
        elif len(self.input_username.text())==0 and len(self.input_passwd.text())==0:
            self.label_login_tips.setText(u"请输入用户名和密码！")
            self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
            return True
        else:
            return False

    def update_setting_login(self):
        conf = configparser.ConfigParser()
        conf.read("../config")
        if self.checkBox_rem_passwd.isChecked():
            conf.set('login', 'remember_passwd', '1')
        else:
            conf.set('login', 'remember_passwd', '0')
        if self.checkBox_auto_login.isChecked():
            conf.set('login', 'auto_login', '1')
        else:
            conf.set('login', 'auto_login', '0')
        fh = open("../config", 'w')
        conf.write(fh)  # 把要修改的节点的内容写到文件中
        fh.close()

class Main(QMainWindow, Ui_main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.initial_user()

    def initial_user(self):
        conf = configparser.ConfigParser()
        conf.read("../config")
        self.label_user_name.setText(conf.get('user', 'name'))
        self.label_user_hospital.setText(conf.get('user', 'hospital'))
        self.label_user_title.setText(conf.get('user', 'title'))
        self.label_user_name.setStyleSheet("font: 12pt \"Agency FB\";\n"
                                            "background-color: rgba(46, 187, 150, 125);")
        self.label_user_hospital.setStyleSheet("font: 12pt \"Agency FB\";\n"
                                            "background-color: rgba(46, 187, 150, 125);")
        self.label_user_title.setStyleSheet("font: 12pt \"Agency FB\";\n"
                                            "background-color: rgba(46, 187, 150, 125);")
        self.label_head=myLabel()
        self.setHead()
        self.timer = timeGenerate()
        self.timer.datetimeSignal.connect(self.setDateTimer)
        self.timer.weekdaySignal.connect(self.setWeekdayer)
        self.timer.start()

    def setDateTimer(self, timestr):
        self.label_datetime.setText(timestr)

    def setWeekdayer(self,timestr):
        self.label_weekday.setText(timestr)

    def setHead(self):
        self.label_head.setGeometry(QtCore.QRect(40, 20, 90, 90))
        self.label_head.setText("rvrv")
        self.label_head.setPixmap(QtGui.QPixmap("../../../../../myself/项目/朱总(北京同明眼科)/png/done.png"))
        self.label_head.setObjectName("label_head")

class timeGenerate(QtCore.QThread): # 时钟
    datetimeSignal = QtCore.pyqtSignal(str)
    weekdaySignal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)

    def run(self):
        while True:
            self.weekdaySignal.emit(weekday[datetime.now().weekday()])
            self.datetimeSignal.emit(datetime.now().strftime(DATETIME_FORMAT))
            sleep(1)

class myLabel(QLabel):
    def __init__(self,parent = None):
        super(myLabel,self).__init__(parent)

    def mousePressEvent(self, e):##重载一下鼠标点击事件
        print("you clicked the label")

    def mouseReleaseEvent(self, QMouseEvent):
        print('you have release the mouse')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow=Login()
    loginWindow.show()
    if loginWindow.exec_():
        mainWindow = Main()
        mainWindow.show()
    sys.exit(app.exec_())