# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Project/IdlCompilerDefineNameDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IdlCompilerDefineNameDialog(object):
    def setupUi(self, IdlCompilerDefineNameDialog):
        IdlCompilerDefineNameDialog.setObjectName("IdlCompilerDefineNameDialog")
        IdlCompilerDefineNameDialog.resize(400, 108)
        IdlCompilerDefineNameDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(IdlCompilerDefineNameDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(IdlCompilerDefineNameDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(IdlCompilerDefineNameDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(IdlCompilerDefineNameDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.valueEdit = QtWidgets.QLineEdit(IdlCompilerDefineNameDialog)
        self.valueEdit.setObjectName("valueEdit")
        self.gridLayout.addWidget(self.valueEdit, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(IdlCompilerDefineNameDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(IdlCompilerDefineNameDialog)
        self.buttonBox.accepted.connect(IdlCompilerDefineNameDialog.accept)
        self.buttonBox.rejected.connect(IdlCompilerDefineNameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IdlCompilerDefineNameDialog)
        IdlCompilerDefineNameDialog.setTabOrder(self.nameEdit, self.valueEdit)

    def retranslateUi(self, IdlCompilerDefineNameDialog):
        _translate = QtCore.QCoreApplication.translate
        IdlCompilerDefineNameDialog.setWindowTitle(_translate("IdlCompilerDefineNameDialog", "Define Name"))
        self.label.setText(_translate("IdlCompilerDefineNameDialog", "Name:"))
        self.nameEdit.setToolTip(_translate("IdlCompilerDefineNameDialog", "Enter the variable name"))
        self.label_2.setText(_translate("IdlCompilerDefineNameDialog", "Value:"))
        self.valueEdit.setToolTip(_translate("IdlCompilerDefineNameDialog", "Enter an optional value"))
