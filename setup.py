# coding:utf-8
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

project = "pygame-plane"
version = "0.0.2"
build_exe_options = {}
build_exe_options["packages"]      = ["pygame"]
build_exe_options["include_files"] = ["assets/"]
build_exe_options["excludes"]      = ["tkinter", "socket", "multiprocessing", "ssl"]

setup(
    name=project,
    version=version,
    # packages=[''],
    url='https://github.com/cupen/pygame-plane',
    author='cupen',
    author_email='cupen@foxmail.com',
    description='It‘s a plane game demo written in pygame ',
    options = {"build_exe": build_exe_options},
    executables = [Executable("lancher.py", base = base)]
)