import sys
from cx_Freeze import setup, Executable

included_files = ["config.txt"]

build_exe_options = {
    "include_files": included_files
}

base = None
'''if (sys.platform == "win32"):
    base = "Win32GUI"    # Tells the build script to hide the console.'''

setup(
    name="Oblivion Override Map Screenshotter",
    version="1.1",
    description="Oblivion Override Map Screenshotter",
    options={"build_exe": build_exe_options},
    executables=[Executable("oblivion_screenshotter.pyw", base=base)],
)