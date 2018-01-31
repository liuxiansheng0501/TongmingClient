#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : pyinstall.py 
    Time    : 2018/01/29 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""

import  os
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['./contorler/Main.py','-D','-w','--paths=C:\\Users\\llj\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin','--icon=./source/eye_72px_1197872_easyicon.ico']
    run(opts)