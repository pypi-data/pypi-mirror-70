# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/E5Gui/E5ProcessDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_E5ProcessDialog(object):
    def setupUi(self, E5ProcessDialog):
        E5ProcessDialog.setObjectName("E5ProcessDialog")
        E5ProcessDialog.resize(600, 500)
        E5ProcessDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5ProcessDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.outputGroup = QtWidgets.QGroupBox(E5ProcessDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.outputGroup.sizePolicy().hasHeightForWidth())
        self.outputGroup.setSizePolicy(sizePolicy)
        self.outputGroup.setObjectName("outputGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.outputGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.resultbox = QtWidgets.QTextEdit(self.outputGroup)
        self.resultbox.setReadOnly(True)
        self.resultbox.setAcceptRichText(False)
        self.resultbox.setObjectName("resultbox")
        self.vboxlayout.addWidget(self.resultbox)
        self.verticalLayout.addWidget(self.outputGroup)
        self.progressBar = QtWidgets.QProgressBar(E5ProcessDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.statusLabel = QtWidgets.QLabel(E5ProcessDialog)
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout.addWidget(self.statusLabel)
        self.errorGroup = QtWidgets.QGroupBox(E5ProcessDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(E5ProcessDialog)
        self.inputGroup.setObjectName("inputGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.inputGroup)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = E5ClearableLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self.gridlayout.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self.gridlayout.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5ProcessDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5ProcessDialog)
        QtCore.QMetaObject.connectSlotsByName(E5ProcessDialog)
        E5ProcessDialog.setTabOrder(self.resultbox, self.errors)
        E5ProcessDialog.setTabOrder(self.errors, self.input)
        E5ProcessDialog.setTabOrder(self.input, self.passwordCheckBox)
        E5ProcessDialog.setTabOrder(self.passwordCheckBox, self.sendButton)
        E5ProcessDialog.setTabOrder(self.sendButton, self.buttonBox)

    def retranslateUi(self, E5ProcessDialog):
        _translate = QtCore.QCoreApplication.translate
        self.outputGroup.setTitle(_translate("E5ProcessDialog", "Output"))
        self.errorGroup.setTitle(_translate("E5ProcessDialog", "Errors"))
        self.inputGroup.setTitle(_translate("E5ProcessDialog", "Input"))
        self.sendButton.setToolTip(_translate("E5ProcessDialog", "Press to send the input to the running process"))
        self.sendButton.setText(_translate("E5ProcessDialog", "&Send"))
        self.sendButton.setShortcut(_translate("E5ProcessDialog", "Alt+S"))
        self.input.setToolTip(_translate("E5ProcessDialog", "Enter data to be sent to the running process"))
        self.passwordCheckBox.setToolTip(_translate("E5ProcessDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("E5ProcessDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("E5ProcessDialog", "Alt+P"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
