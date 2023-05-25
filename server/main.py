import logging
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QInputDialog,
    QMessageBox,
    QLabel,
    QDialog,
)
from PySide6.QtGui import QPixmap, Qt

from window_getter import MainWindow
from settings import LOG_FILENAME
from sockets import ser_sock
import pdb

MSG_FADE_TIME = 4000
sock: ser_sock = ser_sock()
app = QApplication(sys.argv)
window: MainWindow = MainWindow()
logger = logging.basicConfig(
    filename=LOG_FILENAME,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


def add_signals():
    # Scan Action
    window.acnScan.triggered.connect(acn_scan_click)

    # Add ip Action
    window.acnAdd_by_ip.triggered.connect(acn_add_ip)

    # Disconnect Action
    window.btnDisconnect.clicked.connect(btn_disconnect)

    # Screenshot Action
    window.btnSceenshot.clicked.connect(btn_screenshot)

    # shutown and reset Action
    window.btnRestart.clicked.connect(btn_restart)
    window.btnShutdown.clicked.connect(btn_shutdown)

    app.aboutToQuit.connect(about_to_quit)
    window.acnQuit.triggered.connect(acn_quit)
    window.acnStart.triggered.connect(acn_start_click)


def acn_quit():
    window.close()


def btn_restart():
    i = window.listClients.currentItem()
    if not i:
        window.statusbar.showMessage("No active clients", MSG_FADE_TIME)
    sock.send_reset(i.text())


def btn_shutdown():
    i = window.listClients.currentItem()
    if i is None:
        window.statusbar.showMessage("No active clients", MSG_FADE_TIME)
    sock.send_shutdown(i.text())


def about_to_quit():
    sock.close()


def btn_screenshot():
    i = window.listClients.currentItem()
    if i is None:
        window.statusbar.showMessage("No active clients", MSG_FADE_TIME)
    if sock.get_screen(i.text(), show_screenshot):
        window.statusbar.showMessage(
            f"getting screenshot from {i.text()}", MSG_FADE_TIME
        )
    else:
        window.statusbar.showMessage("error", MSG_FADE_TIME)


def btn_disconnect():
    i = window.listClients.currentItem()
    if i is None:
        window.statusbar.showMessage("No active clients", MSG_FADE_TIME)
    if sock.close_client(i.text()):
        window.statusbar.showMessage("Disconnected", MSG_FADE_TIME)
    else:
        window.statusbar.showMessage("Error", MSG_FADE_TIME)


def acn_scan_click():
    text, ok = QInputDialog.getText(window, "IP class", "Enter IP class")
    if ok:
        if sock.scan_network(text):
            window.statusbar.showMessage("Done", MSG_FADE_TIME)
        else:
            window.statusbar.showMessage("Error", MSG_FADE_TIME)


def acn_start_click():
    global sock
    text, ok = QInputDialog.getText(window, "listen ip", "Enter IP address")
    if ok:
        if sock.start_listen(text, update_clients=update_clients):
            window.statusbar.showMessage("Listening", MSG_FADE_TIME)
        else:
            window.statusbar.showMessage("Error", MSG_FADE_TIME)


def update_clients(clients: list[str]):
    window.listClients.clear()
    for c in clients:
        window.listClients.addItem(c)


class ImagePopup(QDialog):
    def __init__(self, imagePath):
        super().__init__()
        # Create a QLabel for displaying the image
        self.imageLabel = QLabel(self)
        # Load the image into a QPixmap and set it as the label's pixmap
        pixmap = QPixmap(imagePath)
        self.imageLabel.setPixmap(pixmap)
        # Resize the dialog based on the size of the loaded image
        self.resize(pixmap.width(), pixmap.height())


def show_screenshot(path: str):
    popup = ImagePopup(path)
    popup.exec_()
    # msg_box = QMessageBox()
    # msg_box.setWindowTitle("Image Popup")
    # label = QLabel()
    # pixmap = QPixmap(path)

    # label.setPixmap(pixmap)
    # # label.setScaledContents(True)  # Scale the image to fit the label
    # msg_box.layout().addWidget(label)
    # # Set the pixmap as the message box's icon
    # msg_box.setWindowIcon(pixmap)
    # # Set the pixmap as the message box's main content
    # msg_box.setText("")
    # # msg_box.setIconPixmap(pixmap.scaled(pixmap.width(), pixmap.height()))
    # width = app.screens()[0].size().width()
    # height = app.screens()[0].size().height()
    # label.setFixedSize(width, height)
    # msg_box.setFixedSize(width, height)
    # msg_box.setFixedSize(width, height)
    # msg_box.exec()


def acn_add_ip():
    global sock
    text, ok = QInputDialog.getText(window, "Add ip", "Enter IP address")
    if ok:
        if sock.add_ip(text):
            window.statusbar.showMessage("Added", MSG_FADE_TIME)
        else:
            window.statusbar.showMessage("Error", MSG_FADE_TIME)


if __name__ == "__main__":
    add_signals()
    window.show()
    app.exec()
