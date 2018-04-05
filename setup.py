from cx_Freeze import setup, Executable
import sys
base = 'WIN32GUI' if sys.platform == "win32" else None

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [Executable("./contorler/Main.py", base=base, icon='./source/eye_72px_1197872_easyicon.ico')]

# buildOptions = dict(excludes = ["tkinter"], includes =["idna.idnadata"], optimize=1)

options = {
    'build_exe': {
        'includes':["idna.idnadata","numpy"]
    },

}

setup(
    name = "TM",
    options = options,
    version = "1.0",
    description = 'desc of program',
    executables = executables
)