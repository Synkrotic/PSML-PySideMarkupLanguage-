from PySide6.QtWidgets import QApplication
import sys, configparser

app = QApplication(sys.argv)
transpiler = None
window = None

config = configparser.ConfigParser()
config.read("config.cfg")


# Config
export = config.getboolean("Settings", "export")
fullscreen = config.getboolean("Settings", "fullscreen")