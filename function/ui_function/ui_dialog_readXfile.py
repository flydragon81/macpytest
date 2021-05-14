# """
#     Project Dialog
# """
from PyQt5.QtWidgets import QDialog
from ui.dialog_input_one import Ui_Dialog
from configure import config
from PyQt5 import QtCore
from PyQt5.QtCore import QThreadPool
from function.db_function.dbrawsql import DbLoad
from function.file_function import filefunction
from function.app_function import read_xfile
import os
import time


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

    def run(self):
        worker = read_xfile.ReadXFile(self.from_file, self.output_file)

        self.threadpool.start(worker)
        # worker.signals.start.connect(self.btn_disable)
        # worker.signals.process_max.connect(self.progress_max)
        # worker.signals.process.connect(self.progress)
        # worker.signals.finished.connect(self.btn_disable)
