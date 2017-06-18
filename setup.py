import sys
from cx_Freeze import setup, Executable

setup(
    name = "GameOfLife",
    version = "0.1",
    description = "Game of life",
    executables = [Executable("GameOfLife.py", base="Win32GUI")]
)