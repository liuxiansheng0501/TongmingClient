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
    opts=['./contorler/Main.py','-D','-w','--icon=./source/Doctor.ico']
    run(opts)