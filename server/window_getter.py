from typing import Optional
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget, QMainWindow
from PySide6.QtCore import QFile, QIODevice

from ui_mainWindow import Ui_mainWindow
import sys


def mainWindow_loader() -> QWidget:
    ui_file_name = "untitled.ui"
    ui_file = QFile(ui_file_name)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    return window


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
