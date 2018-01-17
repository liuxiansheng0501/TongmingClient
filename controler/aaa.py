#-*- coding:utf-8 -*-
#pyqt4 label 控件设置label图标，获取点击事件
####label本身是没有点击功能的，因此我们需要将其重载,重载，我们也可以给他加上别的功能
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
###########tooltip 所需要的
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class myLabel(QLabel):
    def __init__(self,parent = None):
        super(myLabel,self).__init__(parent)

    def mousePressEvent(self, e):##重载一下鼠标点击事件
        print "you clicked the label"

    def mouseReleaseEvent(self, QMouseEvent):
        print 'you have release the mouse'

class MyWindow(QDialog,QWidget):
    def __init__(self,parent = None):
        super(MyWindow,self).__init__(parent)
        self.resize(400,400)
        self.mainlayout = QGridLayout(self)
        self.myLabelEx = myLabel()
        #self.myLabelEx.setText(u"点击标签")
        self.mainlayout.addWidget(self.myLabelEx)
        self.myLabelEx.setPixmap(QPixmap("help.png"))#####设置标签图片
        self.myLabelEx.setToolTip(_translate("MainWindow", u"点我试试~", None))


if __name__ == "__main__":

    app=QApplication(sys.argv)
    window=MyWindow()
    window.show()
    app.exec_()