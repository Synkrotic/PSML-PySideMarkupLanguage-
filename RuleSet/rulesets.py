from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox



elementTypes = [
    "root",

    "cont",
    "container",

    "node",
    "nd",

    "btn",
    "button",

    "lbl",
    "label",
]

psml_widgets = {
    "root": QWidget,

    "cont": QWidget,
    "container": QWidget,
    "node": QWidget,
    "nd": QWidget,
    "box": QWidget,

    "btn": QPushButton,
    "button": QPushButton,

    "lbl": QLabel,
    "label": QLabel,
}