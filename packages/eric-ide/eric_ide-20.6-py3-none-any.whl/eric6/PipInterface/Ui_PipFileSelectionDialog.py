# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/PipInterface/PipFileSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipFileSelectionDialog(object):
    def setupUi(self, PipFileSelectionDialog):
        PipFileSelectionDialog.setObjectName("PipFileSelectionDialog")
        PipFileSelectionDialog.resize(600, 114)
        PipFileSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(PipFileSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileLabel = QtWidgets.QLabel(PipFileSelectionDialog)
        self.fileLabel.setObjectName("fileLabel")
        self.verticalLayout.addWidget(self.fileLabel)
        self.filePicker = E5PathPicker(PipFileSelectionDialog)
        self.filePicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.filePicker.setObjectName("filePicker")
        self.verticalLayout.addWidget(self.filePicker)
        self.userCheckBox = QtWidgets.QCheckBox(PipFileSelectionDialog)
        self.userCheckBox.setObjectName("userCheckBox")
        self.verticalLayout.addWidget(self.userCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(PipFileSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PipFileSelectionDialog)
        self.buttonBox.accepted.connect(PipFileSelectionDialog.accept)
        self.buttonBox.rejected.connect(PipFileSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PipFileSelectionDialog)

    def retranslateUi(self, PipFileSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        PipFileSelectionDialog.setWindowTitle(_translate("PipFileSelectionDialog", "Select File"))
        self.fileLabel.setText(_translate("PipFileSelectionDialog", "File Name:"))
        self.userCheckBox.setToolTip(_translate("PipFileSelectionDialog", "Select to install to the Python user install directory"))
        self.userCheckBox.setText(_translate("PipFileSelectionDialog", "Install into User Directory"))
from E5Gui.E5PathPicker import E5PathPicker
