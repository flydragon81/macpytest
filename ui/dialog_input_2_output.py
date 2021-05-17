# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_input_2_output.ui'
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.input1_lbl = QtWidgets.QLabel(self.gridLayoutWidget)
        self.input1_lbl.setObjectName("input1_lbl")
        self.gridLayout.addWidget(self.input1_lbl, 0, 1, 1, 1)
        self.input1_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.input1_btn.setObjectName("input1_btn")
        self.gridLayout.addWidget(self.input1_btn, 0, 0, 1, 1)
        self.input2_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.input2_btn.setObjectName("input2_btn")
        self.gridLayout.addWidget(self.input2_btn, 1, 0, 1, 1)
        self.input2_lbl = QtWidgets.QLabel(self.gridLayoutWidget)
        self.input2_lbl.setObjectName("input2_lbl")
        self.gridLayout.addWidget(self.input2_lbl, 1, 1, 1, 1)
        self.output_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.output_btn.setObjectName("output_btn")
        self.gridLayout.addWidget(self.output_btn, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(9, 200, 381, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.quit_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.quit_btn.setObjectName("quit_btn")
        self.gridLayout_2.addWidget(self.quit_btn, 0, 2, 1, 1)
        self.run_btn = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.run_btn.setObjectName("run_btn")
        self.gridLayout_2.addWidget(self.run_btn, 0, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.checkBox.setEnabled(True)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.input1_lbl.setText(_translate("Dialog", "input 1"))
        self.input1_btn.setText(_translate("Dialog", "Input 1"))
        self.input2_btn.setText(_translate("Dialog", "Input 2"))
        self.input2_lbl.setText(_translate("Dialog", "input 2"))
        self.output_btn.setText(_translate("Dialog", "Output"))
        self.label.setText(_translate("Dialog", "Output"))
        self.quit_btn.setText(_translate("Dialog", "Quit"))
        self.run_btn.setText(_translate("Dialog", "Run"))
        self.checkBox.setText(_translate("Dialog", "First time"))
