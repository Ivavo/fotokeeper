import sys
import time
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import os
import keeper
from PyQt5 import QtWidgets, QtCore
from pk import Ui_MainWindow
import pathlib

def init_settings():
    r_Path = None
    timer = None
    if 'Timer' not in os.environ:
        timer = 1
    else:
        timer = os.environ['Timer']
    if 'r_Path' not in os.environ:
        items = pathlib.Path().iterdir()
        for item in items:
            name = str(item)
            if name == 'settings.bin':
                r_Path = keeper.bin_reader('settings.bin')
                break
            else:
                r_Path = 'Виберіть цільову директорію'
    else:
        r_Path = os.environ['r_Path']
    return timer, r_Path


class Worker(QThread):

    def __init__(self, mainwindow, parent = None):
        super().__init__()
        self.mainwindow = mainwindow
        self.is_running = True

    def run(self):
        cont = 0
        timer, r_Path = init_settings()
        while True:
            self.is_running = True
            cont += 1
            print(cont)
            keeper.main(r_Path)
            time.sleep(int(timer))

    def stop(self):
        self.is_running = False
        self.terminate()


class My_app(QtWidgets.QMainWindow, Ui_MainWindow):

    data_signal = pyqtSignal(str)

    def __init__(self):
        super(My_app, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.set_target_folder)
        self.ui.pushButton_3.clicked.connect(self.launch_thread)

        self.ui.pushButton_4.clicked.connect(self.stop)
        self.ui.lineEdit_2.setText(init_settings()[1])
        self.ui.time_add.clicked.connect(self.time_sellector)
        self.ui.textBrowser.setText('run')
        self.ui.spinBox.setValue(1)
        self.Worker_inst = Worker(mainwindow=self)

    def set_target_folder(self):
        target_directory = QFileDialog.getExistingDirectory()
        self.ui.lineEdit_2.setText(os.path.join(target_directory))
        os.environ['r_Path'] = target_directory
        return target_directory

    def time_sellector(self):
        sellected_time = self.ui.spinBox.value()

        os.environ['Timer'] = str(sellected_time)
        print(type(os.environ['Timer']))
        print(os.environ['Timer'])
        return sellected_time

    def launch_thread(self):
        self.Worker_inst.start()

    def stop(self):
        self.Worker_inst.stop()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    application = My_app()
    application.show()
    sys.exit(app.exec_())


