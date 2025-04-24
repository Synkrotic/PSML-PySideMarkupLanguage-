from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
from transpiler import Transpiler
import sys



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layout Example")
        self.transpiler = Transpiler()
        self.transpiler.run('main.psml')
        self.setGeometry(1500, 750, 100, 300)

        if self.transpiler.root is None:
            raise ValueError("Root element not found in the PSML file.")

        self.setLayout(self.transpiler.root.load(None))
        loadStyleSheet("style.qss")



def loadStyleSheet(filePath) -> None:
    if filePath is None:
        return;

    if not "styling/" in filePath:
        filePath = "styling/" + filePath

    with open(filePath, "r") as file:
        style = file.read()
    app.setStyleSheet(style)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
