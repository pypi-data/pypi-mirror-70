# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/VirtualEnv/VirtualenvNameDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VirtualenvNameDialog(object):
    def setupUi(self, VirtualenvNameDialog):
        VirtualenvNameDialog.setObjectName("VirtualenvNameDialog")
        VirtualenvNameDialog.resize(400, 450)
        VirtualenvNameDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(VirtualenvNameDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.envsList = QtWidgets.QListWidget(VirtualenvNameDialog)
        self.envsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.envsList.setAlternatingRowColors(True)
        self.envsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.envsList.setObjectName("envsList")
        self.verticalLayout.addWidget(self.envsList)
        self.label = QtWidgets.QLabel(VirtualenvNameDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.nameEdit = E5ClearableLineEdit(VirtualenvNameDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout.addWidget(self.nameEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(VirtualenvNameDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VirtualenvNameDialog)
        self.buttonBox.accepted.connect(VirtualenvNameDialog.accept)
        self.buttonBox.rejected.connect(VirtualenvNameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VirtualenvNameDialog)
        VirtualenvNameDialog.setTabOrder(self.envsList, self.nameEdit)

    def retranslateUi(self, VirtualenvNameDialog):
        _translate = QtCore.QCoreApplication.translate
        VirtualenvNameDialog.setWindowTitle(_translate("VirtualenvNameDialog", "Virtualenv Name"))
        self.envsList.setSortingEnabled(True)
        self.label.setText(_translate("VirtualenvNameDialog", "Enter a logical name for the virtual environment:"))
        self.nameEdit.setToolTip(_translate("VirtualenvNameDialog", "Enter a unique name for the virtual environment"))
        self.nameEdit.setPlaceholderText(_translate("VirtualenvNameDialog", "Name for the virtual environment"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
