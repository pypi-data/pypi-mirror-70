# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/PipInterface/PipPackagesInputDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipPackagesInputDialog(object):
    def setupUi(self, PipPackagesInputDialog):
        PipPackagesInputDialog.setObjectName("PipPackagesInputDialog")
        PipPackagesInputDialog.resize(600, 130)
        PipPackagesInputDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(PipPackagesInputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(PipPackagesInputDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.packagesEdit = QtWidgets.QLineEdit(PipPackagesInputDialog)
        self.packagesEdit.setObjectName("packagesEdit")
        self.verticalLayout.addWidget(self.packagesEdit)
        self.userCheckBox = QtWidgets.QCheckBox(PipPackagesInputDialog)
        self.userCheckBox.setObjectName("userCheckBox")
        self.verticalLayout.addWidget(self.userCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(PipPackagesInputDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PipPackagesInputDialog)
        self.buttonBox.accepted.connect(PipPackagesInputDialog.accept)
        self.buttonBox.rejected.connect(PipPackagesInputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PipPackagesInputDialog)

    def retranslateUi(self, PipPackagesInputDialog):
        _translate = QtCore.QCoreApplication.translate
        PipPackagesInputDialog.setWindowTitle(_translate("PipPackagesInputDialog", "Packages "))
        self.label_2.setText(_translate("PipPackagesInputDialog", "Package Specifications (separated by whitespace):"))
        self.userCheckBox.setToolTip(_translate("PipPackagesInputDialog", "Select to install to the Python user install directory"))
        self.userCheckBox.setText(_translate("PipPackagesInputDialog", "Install into User Directory"))
