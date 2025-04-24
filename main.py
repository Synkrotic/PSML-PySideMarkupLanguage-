from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
from transpiler import Transpiler
import sys, os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layout Example")
        self.transpiler = Transpiler()
        self.transpiler.run('main.psml')
        self.centerWindow()
        self.fullscreenWindow()
        self.setObjectName("main_window")

        if self.transpiler.root is None:
            raise ValueError("Root element not found in the PSML file.")

        self.setLayout(self.transpiler.root.load(None))
        self.setStyleSheet(loadStyleSheet("style.qss"))

    def centerWindow(self):
        screen = app.primaryScreen()
        screenGeometry = screen.availableGeometry()
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2
        self.move(x, y)

    def fullscreenWindow(self):
        screen = app.primaryScreen()
        screenGeometry = screen.availableGeometry()
        self.setGeometry(screenGeometry)
        self.showFullScreen()



def loadStyleSheet(filePath) -> None:
    if filePath is None:
        return;

    if not "styling/" in filePath:
        filePath = "styling/" + filePath

    with open(filePath, "r") as file:
        style = file.read()
    return style



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
