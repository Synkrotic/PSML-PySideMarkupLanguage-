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
    "cont": QGroupBox,
    "container": QGroupBox,
    "node": QWidget,
    "nd": QWidget,

    "btn": QPushButton,
    "button": QPushButton,

    "lbl": QLabel,
    "label": QLabel,
}