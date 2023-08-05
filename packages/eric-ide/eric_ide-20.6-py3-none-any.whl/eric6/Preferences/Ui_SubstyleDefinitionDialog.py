# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/SubstyleDefinitionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubstyleDefinitionDialog(object):
    def setupUi(self, SubstyleDefinitionDialog):
        SubstyleDefinitionDialog.setObjectName("SubstyleDefinitionDialog")
        SubstyleDefinitionDialog.resize(550, 600)
        SubstyleDefinitionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SubstyleDefinitionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QLabel(SubstyleDefinitionDialog)
        self.header.setText("")
        self.header.setObjectName("header")
        self.verticalLayout.addWidget(self.header)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SubstyleDefinitionDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.descriptionEdit = E5ClearableLineEdit(SubstyleDefinitionDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.horizontalLayout.addWidget(self.descriptionEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(SubstyleDefinitionDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.wordsEdit = QtWidgets.QPlainTextEdit(SubstyleDefinitionDialog)
        self.wordsEdit.setObjectName("wordsEdit")
        self.verticalLayout.addWidget(self.wordsEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resetButton = QtWidgets.QPushButton(SubstyleDefinitionDialog)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_2.addWidget(self.resetButton)
        self.defaultButton = QtWidgets.QPushButton(SubstyleDefinitionDialog)
        self.defaultButton.setObjectName("defaultButton")
        self.horizontalLayout_2.addWidget(self.defaultButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(SubstyleDefinitionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SubstyleDefinitionDialog)
        self.buttonBox.accepted.connect(SubstyleDefinitionDialog.accept)
        self.buttonBox.rejected.connect(SubstyleDefinitionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SubstyleDefinitionDialog)
        SubstyleDefinitionDialog.setTabOrder(self.descriptionEdit, self.wordsEdit)
        SubstyleDefinitionDialog.setTabOrder(self.wordsEdit, self.resetButton)
        SubstyleDefinitionDialog.setTabOrder(self.resetButton, self.defaultButton)

    def retranslateUi(self, SubstyleDefinitionDialog):
        _translate = QtCore.QCoreApplication.translate
        SubstyleDefinitionDialog.setWindowTitle(_translate("SubstyleDefinitionDialog", "Define Sub-Style"))
        self.label.setText(_translate("SubstyleDefinitionDialog", "Description:"))
        self.descriptionEdit.setToolTip(_translate("SubstyleDefinitionDialog", "Enter a short description for the style"))
        self.label_2.setText(_translate("SubstyleDefinitionDialog", "Words (separated by spaces):"))
        self.wordsEdit.setToolTip(_translate("SubstyleDefinitionDialog", "Enter the list of words separated by space"))
        self.resetButton.setToolTip(_translate("SubstyleDefinitionDialog", "Press to reset the data"))
        self.resetButton.setText(_translate("SubstyleDefinitionDialog", "Reset"))
        self.defaultButton.setToolTip(_translate("SubstyleDefinitionDialog", "Press to set the data to default values (if available)"))
        self.defaultButton.setText(_translate("SubstyleDefinitionDialog", "Defaults"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
