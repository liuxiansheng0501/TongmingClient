
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------------------
    Project : TongmingClient
    File    : setup.py 
    Time    : 2018/01/29 
    Author  : liulijun
    Site    : https://github.com/markliu666/
------------------------------------------------------
"""

from cx_Freeze import setup, Executable
import sys
base = 'WIN32GUI' if sys.platform == "win32" else None


executables = [Executable("./contorler/Main.py", base=base, icon='./source/eye_72px_1197872_easyicon.ico')]

packages = []
include_files=['./source/timg.jpg']
options = {
    'build_exe': {
        'packages':packages,
        'include_files': include_files
    },

}

setup(
    name = "prog",
    options = options,
    version = "1.0",
    description = 'desc of program',
    executables = executables
)