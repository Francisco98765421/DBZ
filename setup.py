import cx_Freeze
from cx_Freeze import setup, Executable

executables = [
    Executable(script="main.py", icon="assets/favicon.ico", base="Win32GUI")
]

build_options = {
    "packages": ["pygame", "os", "random", "tkinter", "pyttsx3", "json", "speech_recognition"],
    "include_files": ["assets/", "recursos/", "base.atitus"]
}

setup(
    name="DBZ",
    version="1.0",
    description="Jogo Dragon Blast Z",
    options={"build_exe": build_options},
    executables=executables
)