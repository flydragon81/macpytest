# """
#     Project Dialog
# """
from PyQt5.QtWidgets import QDialog
from ui.dialog_input_one import Ui_Dialog
from configure import config
from PyQt5 import QtCore
from PyQt5.QtCore import QThreadPool
from function.file_function import filefunction
from function.app_function import read_xfile
import os
import logging
from importlib import reload


class ChildWin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()

        self.ui.input_btn.clicked.connect(self.open_file)
        self.ui.run_btn.clicked.connect(self.run)
        self.ui.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.from_file = None
        self.output_file = None

    def open_file(self):
        from_file = self.from_file
        self.from_file = filefunction.file_open(self, from_file, config.x_file_pattern)
        self.ui.in_lbl.setText(self.from_file)
        if self.from_file:
            self.output_file = os.path.splitext(self.from_file)[0] + '_output' + os.path.splitext(self.from_file)[1]
        self.__prepare_logging()

    def run(self):
        worker = read_xfile.ReadXFile(self.from_file, self.output_file)

        self.threadpool.start(worker)
        worker.signals.start.connect(self.__btn_enable)
        worker.signals.error.connect(self.__error)
        worker.signals.process.connect(self.__progresss)
        worker.signals.finished.connect(self.__btn_enable)

    def __prepare_logging(self):
        logging.shutdown()
        reload(logging)
        log_filename = os.path.splitext(self.from_file)[0] + '.log'
        log_format = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=log_filename, filemode='a', format=log_format, level=logging.NOTSET)
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    @staticmethod
    def __log(msg: str):
        logging.info(msg)

    def __error(self, err: str):
        self.__log(err)

    def __progresss(self, count: int):
        self.__log(str(count))

    def __btn_enable(self, stat: bool):
        self.ui.input_btn.setEnabled(stat)
        self.ui.run_btn.setEnabled(stat)
        self.ui.quit_btn.setEnabled(stat)
