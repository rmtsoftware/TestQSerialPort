# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(200, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_connect = QPushButton(self.centralwidget)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(10, 20, 181, 24))
        self.btn_disconnect = QPushButton(self.centralwidget)
        self.btn_disconnect.setObjectName(u"btn_disconnect")
        self.btn_disconnect.setGeometry(QRect(10, 50, 181, 24))
        self.btn_get_gps = QPushButton(self.centralwidget)
        self.btn_get_gps.setObjectName(u"btn_get_gps")
        self.btn_get_gps.setGeometry(QRect(10, 100, 181, 24))
        self.btn_get_imu = QPushButton(self.centralwidget)
        self.btn_get_imu.setObjectName(u"btn_get_imu")
        self.btn_get_imu.setGeometry(QRect(10, 130, 181, 24))
        self.btn_write_man = QPushButton(self.centralwidget)
        self.btn_write_man.setObjectName(u"btn_write_man")
        self.btn_write_man.setGeometry(QRect(10, 160, 181, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 200, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c", None))
        self.btn_disconnect.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c", None))
        self.btn_get_gps.setText(QCoreApplication.translate("MainWindow", u"gps", None))
        self.btn_get_imu.setText(QCoreApplication.translate("MainWindow", u"imu", None))
        self.btn_write_man.setText(QCoreApplication.translate("MainWindow", u"man", None))
    # retranslateUi

