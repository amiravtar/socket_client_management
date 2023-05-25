# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(800, 600)
        self.acnScan = QAction(mainWindow)
        self.acnScan.setObjectName(u"acnScan")
        self.acnQuit = QAction(mainWindow)
        self.acnQuit.setObjectName(u"acnQuit")
        self.acnAdd_by_ip = QAction(mainWindow)
        self.acnAdd_by_ip.setObjectName(u"acnAdd_by_ip")
        self.acnStart = QAction(mainWindow)
        self.acnStart.setObjectName(u"acnStart")
        self.widget = QWidget(mainWindow)
        self.widget.setObjectName(u"widget")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 20, 321, 341))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listClients = QListWidget(self.groupBox)
        self.listClients.setObjectName(u"listClients")

        self.horizontalLayout.addWidget(self.listClients)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(340, 20, 105, 196))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnRestart = QPushButton(self.groupBox_2)
        self.btnRestart.setObjectName(u"btnRestart")

        self.gridLayout.addWidget(self.btnRestart, 0, 0, 1, 1)

        self.btnDisconnect = QPushButton(self.groupBox_2)
        self.btnDisconnect.setObjectName(u"btnDisconnect")

        self.gridLayout.addWidget(self.btnDisconnect, 3, 0, 1, 1)

        self.btnShutdown = QPushButton(self.groupBox_2)
        self.btnShutdown.setObjectName(u"btnShutdown")

        self.gridLayout.addWidget(self.btnShutdown, 1, 0, 1, 1)

        self.btnSceenshot = QPushButton(self.groupBox_2)
        self.btnSceenshot.setObjectName(u"btnSceenshot")

        self.gridLayout.addWidget(self.btnSceenshot, 2, 0, 1, 1)

        mainWindow.setCentralWidget(self.widget)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(mainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 30))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAction = QMenu(self.menuBar)
        self.menuAction.setObjectName(u"menuAction")
        mainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuFile.addAction(self.acnStart)
        self.menuFile.addAction(self.acnScan)
        self.menuFile.addAction(self.acnQuit)
        self.menuAction.addAction(self.acnAdd_by_ip)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Server - Main Window", None))
        self.acnScan.setText(QCoreApplication.translate("mainWindow", u"Scan", None))
        self.acnQuit.setText(QCoreApplication.translate("mainWindow", u"Quit", None))
        self.acnAdd_by_ip.setText(QCoreApplication.translate("mainWindow", u"Add by ip", None))
        self.acnStart.setText(QCoreApplication.translate("mainWindow", u"Start", None))
        self.groupBox.setTitle(QCoreApplication.translate("mainWindow", u"Clients", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("mainWindow", u"Actions", None))
        self.btnRestart.setText(QCoreApplication.translate("mainWindow", u"Restart", None))
        self.btnDisconnect.setText(QCoreApplication.translate("mainWindow", u"Disconnect", None))
        self.btnShutdown.setText(QCoreApplication.translate("mainWindow", u"Shutdown", None))
        self.btnSceenshot.setText(QCoreApplication.translate("mainWindow", u"Screen Shot", None))
        self.menuFile.setTitle(QCoreApplication.translate("mainWindow", u"File", None))
        self.menuAction.setTitle(QCoreApplication.translate("mainWindow", u"Action", None))
    # retranslateUi

