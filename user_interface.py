import sys
import time
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTimer
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

def visualizer(name = 'Images'):
    if name in os.environ:
        item = os.environ[name]
    else:
        item = 'None'
    return item


def run_visualizer(text):
    v = My_app()
    v.ui.textBrowser.setText(text)


class Worker2(QThread):
    signal = QtCore.pyqtSignal(int)
    def __init__(self, mainwindow, parent = None):
        super().__init__()
        self.mainwindow = mainwindow
        self.is_running = True

    def run(self):
        count = 0
        progres = 0
        while True:

            name = visualizer('File_Name')
            size = visualizer('Size')

            time.sleep(0.5)
            current_size = keeper.size_check(name, size)


            if current_size == 0:
                continue
            else:

                piese_of_progres = (int(current_size)/int(size)) * 100
                self.signal.emit(piese_of_progres)
            if progres >= 100:
                self.signal.emit(0)
                pass


    def stop(self):
        self.is_running = False
        self.terminate()
        self.quit()


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
        self.quit()


class My_app(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(My_app, self).__init__()
        self.thread={}
        self.ui = Ui_MainWindow()
        self.timer = QTimer()
        self.ui.setupUi(self)
        self.timer.timeout.connect(self.updater)
        self.timer.start(10000)
        self.ui.pushButton_2.clicked.connect(self.set_target_folder)
        self.ui.pushButton_3.clicked.connect(self.launch_thread)
        self.ui.pushButton_4.clicked.connect(self.stop)
        self.ui.lineEdit_2.setText(init_settings()[1])
        self.ui.time_add.clicked.connect(self.time_sellector)
        self.ui.spinBox.setValue(1)
        self.Worker_inst = Worker(mainwindow=self)
        self.Worker2_inst = Worker2(mainwindow=self)
    def updater(self):
        self.ui.textBrowser.setText(visualizer())

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
        self.thread[1] = self.Worker_inst
        self.thread[1].start()
        self.thread[2] = self.Worker2_inst
        self.thread[2].start()
        self.thread[2].signal.connect(self.progresbar_func)

    def stop(self):
        self.Worker_inst.stop()
        self.Worker2_inst.stop()

    def progresbar_func(self, piece_of_progres):
        piece = int(piece_of_progres)
        print(piece)
        self.ui.progressBar.setValue(piece)
        if piece == 100:
            self.ui.progressBar.setValue(piece)
            time.sleep(0.5)
            self.ui.progressBar.setValue(0)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    application = My_app()
    application.show()
    sys.exit(app.exec_())


