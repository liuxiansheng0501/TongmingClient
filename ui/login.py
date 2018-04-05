# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(411, 339)
        login.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/source/doctor_64px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        login.setWindowIcon(icon)
        login.setToolTip("")
        login.setStyleSheet("background-color: rgb(245, 245, 245);\n"
"font: 16pt \"新宋体\";\n"
"border-color: rgb(245, 245, 245);")
        self.username = QtWidgets.QLabel(login)
        self.username.setGeometry(QtCore.QRect(60, 110, 101, 31))
        self.username.setStyleSheet("font: 16pt \"新宋体\";")
        self.username.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.username.setObjectName("username")
        self.passwd = QtWidgets.QLabel(login)
        self.passwd.setGeometry(QtCore.QRect(40, 160, 121, 31))
        self.passwd.setStyleSheet("font: 16pt \"新宋体\";")
        self.passwd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.passwd.setObjectName("passwd")
        self.input_username = QtWidgets.QLineEdit(login)
        self.input_username.setGeometry(QtCore.QRect(170, 110, 181, 31))
        self.input_username.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"新宋体\";")
        self.input_username.setText("")
        self.input_username.setObjectName("input_username")
        self.input_passwd = QtWidgets.QLineEdit(login)
        self.input_passwd.setGeometry(QtCore.QRect(170, 160, 181, 31))
        self.input_passwd.setStyleSheet("font: 10pt \"新宋体\";background-color: rgb(255, 255, 255);")
        self.input_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_passwd.setObjectName("input_passwd")
        self.btn_login = QtWidgets.QPushButton(login)
        self.btn_login.setGeometry(QtCore.QRect(70, 250, 281, 41))
        self.btn_login.setStyleSheet("font: 16pt \"新宋体\";\n"
"background-color: rgb(245, 245, 245);")
        self.btn_login.setObjectName("btn_login")
        self.checkBox_rem_passwd = QtWidgets.QCheckBox(login)
        self.checkBox_rem_passwd.setGeometry(QtCore.QRect(70, 210, 131, 31))
        self.checkBox_rem_passwd.setStyleSheet("font: 12pt \"新宋体\";")
        self.checkBox_rem_passwd.setObjectName("checkBox_rem_passwd")
        self.label_login_tips = QtWidgets.QLabel(login)
        self.label_login_tips.setGeometry(QtCore.QRect(70, 300, 281, 20))
        self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);\n"
"font:8pt \"新宋体\";")
        self.label_login_tips.setText("")
        self.label_login_tips.setObjectName("label_login_tips")
        self.label = QtWidgets.QLabel(login)
        self.label.setGeometry(QtCore.QRect(240, 212, 111, 31))
        self.label.setStyleSheet("font: 12pt \"新宋体\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(login)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 71, 71))
        self.label_2.setStyleSheet("image: url(:/source/hospital2.png);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/source/man.png"))
        self.label_2.setObjectName("label_2")
        self.label_2.raise_()
        self.username.raise_()
        self.passwd.raise_()
        self.input_username.raise_()
        self.input_passwd.raise_()
        self.btn_login.raise_()
        self.checkBox_rem_passwd.raise_()
        self.label_login_tips.raise_()
        self.label.raise_()

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "儿童眼保健检查系统"))
        self.username.setText(_translate("login", "用户名:"))
        self.passwd.setText(_translate("login", "密  码:"))
        self.btn_login.setText(_translate("login", "登  录"))
        self.checkBox_rem_passwd.setText(_translate("login", "记住密码"))
        self.label.setToolTip(_translate("login", "请联系该系统的医院管理员！"))
        self.label.setWhatsThis(_translate("login", "<html><head/><body><p><br/></p></body></html>"))
        self.label.setText(_translate("login", "忘记密码"))

from source.image import *
