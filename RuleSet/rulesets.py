from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView



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

    #TODO Work in progress
    "loader",
    "webview",
    "embed",
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

    #TODO Work in progress
    "loader": QWebEngineView,
    "webview": QWebEngineView,
    "embed": QWebEngineView,
}