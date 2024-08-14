from cx_Freeze import setup, Executable

setup(
    name="VideoCompressor",
    version="1.0",
    description="A simple video compressor",
    executables=[Executable("main.py", base="Win32GUI")],
)
