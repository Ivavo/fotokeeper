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
        value = False
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
        progres = 0
        while True:
            name = visualizer('File_Name')
            size = visualizer('Size')
            current_size = keeper.size_check(name)
            if current_size == 0:
                time.sleep(1)
                pass
            else:
                piese_of_progres = (int(current_size)/int(size)) * 100
                self.signal.emit(piese_of_progres)
            if progres >= 100:
                os.environ.pop('File_Name')
                os.environ.pop('Size')
            time.sleep(1)


    def stop(self):
        self.is_running = False
        self.terminate()
        self.quit()


class Worker(QThread):
    signal_count = QtCore.pyqtSignal(int)
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
            keeper.main(r_Path)
            self.signal_count.emit(cont)
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

    #def setborder(self):
    #    self.ui.pushButton_3.setStyleSheet("""
    #    QWidget {
    #        border: 1px solid green;
    #        border-radius: 10px;
    #        background-color: rgb(90, 90, 90);
    #        }
    #    """)

    def launch_thread(self):
        self.ui.pushButton_3.setStyleSheet("""
                QWidget {
                    border: 1px solid green;
                    border-radius: 10px;
                    background-color: rgb(90, 90, 90);
                    }
                """)
        self.ui.lcdNumber.setStyleSheet("""
            QLCDNumber{color:rgb(20, 201, 208);
            background-color:rgb(50, 50, 50);
            border: 1px solid green;
            border-radius: 8px;}""")
        self.thread[1] = self.Worker_inst
        self.thread[1].start()
        self.thread[1].signal_count.connect(self.lcd_func)
        self.thread[2] = self.Worker2_inst
        self.thread[2].start()
        self.thread[2].signal.connect(self.progresbar_func)

    #def launch_thread2(self, run):
    #    run = run
    #    if run == 1:


    def stop(self):
        self.ui.pushButton_3.setStyleSheet("""
                        QWidget {
                            border: 1px solid red;
                            border-radius: 10px;
                            background-color: rgb(90, 90, 90);
                            }
                        """)
        self.ui.lcdNumber.setStyleSheet("""
                    QLCDNumber{color:rgb(0, 0, 0);
                    background-color:rgb(50, 50, 50);
                    border: 1px solid black;
                    border-radius: 8px;}""")
        self.Worker_inst.stop()
        self.Worker2_inst.stop()

    def progresbar_func(self, piece_of_progres):
        piece = int(piece_of_progres)
        self.ui.progressBar.setValue(piece)
        if piece == 100:
            piece = 0
            self.ui.progressBar.setValue(piece)


    def lcd_func(self, count):
        count = count
        self.ui.lcdNumber.display(count)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    application = My_app()
    application.show()
    sys.exit(app.exec_())


