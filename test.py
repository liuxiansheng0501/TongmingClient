#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : test.py 
    Time    : 2018/02/02 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    icon = QIcon("icon.png")
    w.setWindowIcon(icon)
    w.resize(400, 300)
    w.move(400, 300)
    w.setWindowTitle('hello world')
    w.show()

    sys.exit(app.exec())