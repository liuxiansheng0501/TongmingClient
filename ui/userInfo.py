# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userInfo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_userInfo(object):
    def setupUi(self, userInfo):
        userInfo.setObjectName("userInfo")
        userInfo.resize(403, 188)
        userInfo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_user_head = QtWidgets.QLabel(userInfo)
        self.label_user_head.setGeometry(QtCore.QRect(40, 40, 81, 91))
        self.label_user_head.setText("")
        self.label_user_head.setPixmap(QtGui.QPixmap("../source/head.png"))
        self.label_user_head.setObjectName("label_user_head")
        self.label_user_name = QtWidgets.QLabel(userInfo)
        self.label_user_name.setGeometry(QtCore.QRect(190, 20, 101, 31))
        self.label_user_name.setObjectName("label_user_name")
        self.label_user_title = QtWidgets.QLabel(userInfo)
        self.label_user_title.setGeometry(QtCore.QRect(300, 20, 81, 31))
        self.label_user_title.setObjectName("label_user_title")
        self.label_user_hospital = QtWidgets.QLabel(userInfo)
        self.label_user_hospital.setGeometry(QtCore.QRect(190, 60, 191, 31))
        self.label_user_hospital.setObjectName("label_user_hospital")
        self.pushButton_user_edit = QtWidgets.QPushButton(userInfo)
        self.pushButton_user_edit.setGeometry(QtCore.QRect(190, 120, 93, 28))
        self.pushButton_user_edit.setObjectName("pushButton_user_edit")
        self.pushButton_user_cancel = QtWidgets.QPushButton(userInfo)
        self.pushButton_user_cancel.setGeometry(QtCore.QRect(290, 120, 93, 28))
        self.pushButton_user_cancel.setObjectName("pushButton_user_cancel")

        self.retranslateUi(userInfo)
        QtCore.QMetaObject.connectSlotsByName(userInfo)

    def retranslateUi(self, userInfo):
        _translate = QtCore.QCoreApplication.translate
        userInfo.setWindowTitle(_translate("userInfo", "我"))
        self.label_user_name.setText(_translate("userInfo", "TextLabel"))
        self.label_user_title.setText(_translate("userInfo", "TextLabel"))
        self.label_user_hospital.setText(_translate("userInfo", "TextLabel"))
        self.pushButton_user_edit.setText(_translate("userInfo", "编辑"))
        self.pushButton_user_cancel.setText(_translate("userInfo", "取消"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_userInfo()
    ui.setupUi(MainWindow)
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    MainWindow.show()
    sys.exit(app.exec_())