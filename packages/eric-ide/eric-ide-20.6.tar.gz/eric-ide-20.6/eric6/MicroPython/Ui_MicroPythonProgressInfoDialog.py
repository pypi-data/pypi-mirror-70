# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/MicroPython/MicroPythonProgressInfoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MicroPythonProgressInfoDialog(object):
    def setupUi(self, MicroPythonProgressInfoDialog):
        MicroPythonProgressInfoDialog.setObjectName("MicroPythonProgressInfoDialog")
        MicroPythonProgressInfoDialog.resize(500, 400)
        MicroPythonProgressInfoDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(MicroPythonProgressInfoDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressEdit = QtWidgets.QPlainTextEdit(MicroPythonProgressInfoDialog)
        self.progressEdit.setTabChangesFocus(True)
        self.progressEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.progressEdit.setReadOnly(True)
        self.progressEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.progressEdit.setObjectName("progressEdit")
        self.verticalLayout.addWidget(self.progressEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(MicroPythonProgressInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MicroPythonProgressInfoDialog)
        self.buttonBox.accepted.connect(MicroPythonProgressInfoDialog.accept)
        self.buttonBox.rejected.connect(MicroPythonProgressInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MicroPythonProgressInfoDialog)

    def retranslateUi(self, MicroPythonProgressInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        MicroPythonProgressInfoDialog.setWindowTitle(_translate("MicroPythonProgressInfoDialog", "Progress Information"))
