# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PK.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLCDNumber


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(304, 430)
        MainWindow.setMinimumSize(QtCore.QSize(304, 410))
        MainWindow.setMaximumSize(QtCore.QSize(304, 410))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
        QWidget {
            background-color: rgb(80, 80, 80);
            }
        """)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 50, 75, 20))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("""QWidget {
            border: 1px solid black;
            border-radius: 7px;
            background-color: rgb(100, 100, 100);
            }
            """)
        #self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        #self.lineEdit.setGeometry(QtCore.QRect(10, 20, 201, 20))
        #self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 200, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setStyleSheet("""QWidget {
            border: 1px solid grey;
            border-radius: 7px;
            background-color: rgb(50, 50, 50);
            color: rgb(20, 201, 208)
            }""")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(210, 290, 51, 22))
        self.spinBox.setObjectName("spinBox")
        self.time_add = QtWidgets.QPushButton(self.centralwidget)
        self.time_add.setGeometry(QtCore.QRect(260, 289, 24, 24))
        self.time_add.setObjectName("time_add")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 270, 61, 20))
        self.label.setObjectName("label")
        self.label.setStyleSheet("""QWidget{color: rgb(20, 201, 208)}""")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(120, 340, 51, 31))
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setStyleSheet("""QLCDNumber{color:rgb(0, 0, 0);
                                        background-color:rgb(50, 50, 50);
                                        border: 1px solid grey;
                                        border-radius: 8px;}""")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 332, 71, 50))
        self.pushButton_3.setStyleSheet("""
        QWidget {
            border: 1px solid black;
            border-radius: 10px;
            background-color: rgb(90, 90, 90);
            }
        """)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330, 61, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
                QWidget {
            border: 1px solid red;
            border-radius: 10px;
            background-color: rgb(90, 90, 90);
            }
                """)
        #self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        #self.radioButton.setGeometry(QtCore.QRect(10, 280, 201, 31))
        #self.radioButton.setObjectName("radioButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(98, 100, 108, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("""QWidget{
                                    border: 1px solid grey;
                                    color: rgb(20, 201, 208);
                                    background-color: rgb(50, 50, 50);
                                    border-radius: 8px}""")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 281, 121))
        self.textBrowser.setStyleSheet("""
        QWidget {
            border: 1px solid grey;
            border-radius: 10px;
            background-color: rgb(50, 50, 50);
            }
        """)
        self.textBrowser.setTextColor(QColor(20, 201, 208))
        self.textBrowser.setObjectName("textBrowser")
        #self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        #self.pushButton.setGeometry(QtCore.QRect(220, 20, 75, 23))
        #self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 250, 281, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet("""
QProgressBar{
    border: 1px solid grey;
    background-color: rgb(50, 50, 50);
    border-radius: 8px;
    text-align: bottom;
    color: rgb(20, 201, 208)
}

QProgressBar::chunk {
    background-color: rgb(20, 201, 210);
    text-color: rgb(20, 201, 210)
}
""")
        MainWindow.setCentralWidget(self.centralwidget)
        #self.statusBar = QtWidgets.QStatusBar(MainWindow)
        #self.statusBar.setObjectName("statusBar")
        #self.statusBar.setWindowIconText('sssss')
        #self.statusBar.setStyleSheet("""QWidget {
        #    background-color: rgb(20, 20, 20);
        #    }
        #""")
        #MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "НАС"))
        self.label.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Період сек.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "Старт"))
        self.pushButton_4.setText(_translate("MainWindow", "Стоп"))
        #self.radioButton.setText(_translate("MainWindow", "Видаляти архіви після\n"
#"копіювання:"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        #self.pushButton.setText(_translate("MainWindow", "Папка"))
        self.time_add.setText("OK")
        self.label_2.setText(' Об`єкти в сховищі')