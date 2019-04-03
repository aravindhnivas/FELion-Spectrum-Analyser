import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("FELion_GUI_v3.py", base=base, icon="FELion_Icon.ico")]
packages = {"packages":["tkinter","matplotlib", "numpy", "scipy", "os", "ctypes"], "includes":["FELion_sa", "FELion_power", "FELion_normline", "FELion_avgSpec", "FELion_massSpec", "FELion_definitions", "just_plot", "depletion_plot", "timescan_plot"]}

cx_Freeze.setup(
    name = "FELion_GUI",
    options = {"build_exe": packages},
    version = "3.0",
    description = "FELion Spectrum Analyser",
    executables = executables
    )