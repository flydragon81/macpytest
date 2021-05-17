from function.file_function.SpsParser import Sps21Parser
from configure import sps_output
from function.file_function import check
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
import time


class ReadXFile(QRunnable):
    def __init__(self, input_file, output_file):
        super().__init__()
        self.output_file = output_file
        self.input_file = input_file
        self.signals = WorkerSignal()
        self.parser = Sps21Parser()
        self.commit_every = 100000

    @pyqtSlot()
    def run(self):
        self.signals.start.emit(False)
        start_time = time.time()
        line_numbers = check.iter_count(self.input_file)
        self.signals.process_max.emit(line_numbers)
        self.commit_every = int(line_numbers / 50)
        counter = 0
        sn = 0
        try:
            with open(self.input_file) as fr:
                with open(self.output_file, 'w') as ft:
                    for line in fr:
                        counter += 1
                        parsed = self.parser.parse_relation(line)
                        if parsed:
                            chan = parsed[9] - parsed[8] + 1
                            sn += chan
                            parsed[2] = (parsed[2] + 6000000)
                            outx = sps_output.format_relation(parsed)
                            ft.write((outx))
                            ft.write('\n')
                        if counter % self.commit_every == 0:
                            self.signals.process.emit(counter)

            self.signals.process.emit(counter)
            self.signals.process.emit(sn)
            self.signals.finished.emit(True)
        except Exception as e:
            self.signals.error.emit(str(e))
        end_time = time.time()
        self.signals.process.emit(int(end_time - start_time))


class WorkerSignal(QObject):
    start = pyqtSignal(bool)
    process = pyqtSignal(int)
    process_max = pyqtSignal(int)
    message = pyqtSignal(tuple)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
