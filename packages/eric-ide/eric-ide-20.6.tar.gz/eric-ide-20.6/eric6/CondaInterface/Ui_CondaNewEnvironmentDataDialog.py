# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/CondaInterface/CondaNewEnvironmentDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CondaNewEnvironmentDataDialog(object):
    def setupUi(self, CondaNewEnvironmentDataDialog):
        CondaNewEnvironmentDataDialog.setObjectName("CondaNewEnvironmentDataDialog")
        CondaNewEnvironmentDataDialog.resize(500, 132)
        CondaNewEnvironmentDataDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(CondaNewEnvironmentDataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(CondaNewEnvironmentDataDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.nameEdit = E5ClearableLineEdit(CondaNewEnvironmentDataDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(CondaNewEnvironmentDataDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.condaNameEdit = E5ClearableLineEdit(CondaNewEnvironmentDataDialog)
        self.condaNameEdit.setObjectName("condaNameEdit")
        self.gridLayout.addWidget(self.condaNameEdit, 1, 1, 1, 1)
        self.requirementsLabel = QtWidgets.QLabel(CondaNewEnvironmentDataDialog)
        self.requirementsLabel.setObjectName("requirementsLabel")
        self.gridLayout.addWidget(self.requirementsLabel, 2, 0, 1, 1)
        self.requirementsFilePicker = E5PathPicker(CondaNewEnvironmentDataDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requirementsFilePicker.sizePolicy().hasHeightForWidth())
        self.requirementsFilePicker.setSizePolicy(sizePolicy)
        self.requirementsFilePicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.requirementsFilePicker.setObjectName("requirementsFilePicker")
        self.gridLayout.addWidget(self.requirementsFilePicker, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(CondaNewEnvironmentDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(CondaNewEnvironmentDataDialog)
        self.buttonBox.accepted.connect(CondaNewEnvironmentDataDialog.accept)
        self.buttonBox.rejected.connect(CondaNewEnvironmentDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CondaNewEnvironmentDataDialog)

    def retranslateUi(self, CondaNewEnvironmentDataDialog):
        _translate = QtCore.QCoreApplication.translate
        CondaNewEnvironmentDataDialog.setWindowTitle(_translate("CondaNewEnvironmentDataDialog", "New Conda Environment"))
        self.label_2.setText(_translate("CondaNewEnvironmentDataDialog", "Logical Name:"))
        self.nameEdit.setToolTip(_translate("CondaNewEnvironmentDataDialog", "Enter a unique name for the virtual environment to register it with the Virtual Environment Manager"))
        self.nameEdit.setPlaceholderText(_translate("CondaNewEnvironmentDataDialog", "Name for registration of the virtual environment"))
        self.label.setText(_translate("CondaNewEnvironmentDataDialog", "Conda Name:"))
        self.condaNameEdit.setToolTip(_translate("CondaNewEnvironmentDataDialog", "Enter the name of the virtual environment in Conda"))
        self.condaNameEdit.setPlaceholderText(_translate("CondaNewEnvironmentDataDialog", "Name of the virtual environment in Conda"))
        self.requirementsLabel.setText(_translate("CondaNewEnvironmentDataDialog", "Requirements File:"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
from E5Gui.E5PathPicker import E5PathPicker
