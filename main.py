from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layout Example")

        self.label = QLabel("Hello, world!")
        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.on_button_click)

        inner_layout = QHBoxLayout()
        inner_layout.addWidget(self.label)
        inner_layout.addWidget(self.button)

        group_box = QGroupBox("Group of Widgets")
        group_box.setLayout(inner_layout)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(group_box)

        self.setLayout(outer_layout)

    def on_button_click(self):
        self.label.setText("Button clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
