#
# used to convert .py to .exe windows executable
#

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "console"

setup(  name = "BenEduAutomation",
    version = "1.0.0",
    description = "Benedu Automated",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base = base)])