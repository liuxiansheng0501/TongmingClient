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
        login.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../myself/项目/朱总(北京同明眼科)/png/timg.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        login.setWindowIcon(icon)
        login.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.username = QtWidgets.QLabel(login)
        self.username.setGeometry(QtCore.QRect(90, 70, 71, 31))
        self.username.setStyleSheet("font: 12pt \"Agency FB\";")
        self.username.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.username.setObjectName("username")
        self.passwd = QtWidgets.QLabel(login)
        self.passwd.setGeometry(QtCore.QRect(90, 120, 71, 31))
        self.passwd.setStyleSheet("font: 12pt \"Agency FB\";")
        self.passwd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.passwd.setObjectName("passwd")
        self.input_username = QtWidgets.QLineEdit(login)
        self.input_username.setGeometry(QtCore.QRect(170, 70, 141, 31))
        self.input_username.setObjectName("input_username")
        self.input_passwd = QtWidgets.QLineEdit(login)
        self.input_passwd.setGeometry(QtCore.QRect(170, 120, 141, 31))
        self.input_passwd.setObjectName("input_passwd")
        self.btn_login = QtWidgets.QPushButton(login)
        self.btn_login.setGeometry(QtCore.QRect(100, 210, 211, 31))
        self.btn_login.setStyleSheet("font: 12pt \"Agency FB\";\n"
"background-color: rgb(0, 170, 0);")
        self.btn_login.setObjectName("btn_login")
        self.checkBox_rem_passwd = QtWidgets.QCheckBox(login)
        self.checkBox_rem_passwd.setGeometry(QtCore.QRect(100, 170, 91, 19))
        self.checkBox_rem_passwd.setObjectName("checkBox_rem_passwd")
        self.checkBox_auto_login = QtWidgets.QCheckBox(login)
        self.checkBox_auto_login.setGeometry(QtCore.QRect(230, 170, 91, 19))
        self.checkBox_auto_login.setObjectName("checkBox_auto_login")
        self.label_login_tips = QtWidgets.QLabel(login)
        self.label_login_tips.setGeometry(QtCore.QRect(100, 250, 211, 16))
        self.label_login_tips.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_login_tips.setObjectName("label_login_tips")

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "北京同明眼科专家"))
        self.username.setText(_translate("login", "用户名:"))
        self.passwd.setText(_translate("login", "密     码:"))
        self.btn_login.setText(_translate("login", "登    录"))
        self.checkBox_rem_passwd.setText(_translate("login", "记住密码"))
        self.checkBox_auto_login.setText(_translate("login", "自动登录"))
        # self.label_login_tips.setText(_translate("login", "TextLabel"))

