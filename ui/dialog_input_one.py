# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_input_one.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.input_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.input_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.input_btn.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.input_btn.setFont(font)
        self.input_btn.setObjectName("input_btn")
        self.gridLayout.addWidget(self.input_btn, 0, 0, 1, 1)
        self.in_lbl = QtWidgets.QLabel(self.gridLayoutWidget)
        self.in_lbl.setMinimumSize(QtCore.QSize(0, 100))
        self.in_lbl.setObjectName("in_lbl")
        self.gridLayout.addWidget(self.in_lbl, 0, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(9, 190, 381, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.run_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.run_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.run_btn.setSizeIncrement(QtCore.QSize(0, 20))
        self.run_btn.setBaseSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        self.run_btn.setFont(font)
        self.run_btn.setObjectName("run_btn")
        self.gridLayout_2.addWidget(self.run_btn, 0, 0, 1, 1)
        self.quit_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.quit_btn.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.quit_btn.setFont(font)
        self.quit_btn.setObjectName("quit_btn")
        self.gridLayout_2.addWidget(self.quit_btn, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.input_btn.setText(_translate("Dialog", "Input"))
        self.in_lbl.setText(_translate("Dialog", "input"))
        self.run_btn.setText(_translate("Dialog", "Run"))
        self.quit_btn.setText(_translate("Dialog", "Quit"))
