import cx_Freeze, sys, os

os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

# configure includes and excludes

add_mods = ['numpy.array', 'numpy.genfromtxt']
executables = [cx_Freeze.Executable("FELion_GUI_v3.py", base=base, icon="FELion_Icon.ico")]
remove_mods = ['matplotlib', 'scipy', 'numpy', 'PyQt5', 'notebook']
modules = ["FELion_sa", "FELion_power", "FELion_normline", "FELion_avgSpec", "FELion_massSpec", "FELion_definitions", "just_plot", "depletion_plot", "timescan_plot"]

pack = {
		"packages":add_mods, 
		"includes":modules, 
		"excludes":remove_mods
}

cx_Freeze.setup(
    name = "FELion_GUI",
    options = {"build_exe": pack},
    version = "3.0",
    description = "FELion Spectrum Analyser",
    executables = executables
    )