from PyQt5.QtWidgets import QApplication
from function.ui_function.ui_dialog_readXfile import ChildWin


def main():
    import sys
    app = QApplication(sys.argv)
    window = ChildWin()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
