# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/WizardPlugins/DotDesktopWizard/DotDesktopListSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DotDesktopListSelectionDialog(object):
    def setupUi(self, DotDesktopListSelectionDialog):
        DotDesktopListSelectionDialog.setObjectName("DotDesktopListSelectionDialog")
        DotDesktopListSelectionDialog.resize(450, 400)
        DotDesktopListSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DotDesktopListSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(DotDesktopListSelectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.entriesList = QtWidgets.QListWidget(DotDesktopListSelectionDialog)
        self.entriesList.setAlternatingRowColors(True)
        self.entriesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.entriesList.setObjectName("entriesList")
        self.verticalLayout.addWidget(self.entriesList)
        self.subList = QtWidgets.QListWidget(DotDesktopListSelectionDialog)
        self.subList.setAlternatingRowColors(True)
        self.subList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.subList.setObjectName("subList")
        self.verticalLayout.addWidget(self.subList)
        self.buttonBox = QtWidgets.QDialogButtonBox(DotDesktopListSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DotDesktopListSelectionDialog)
        self.buttonBox.accepted.connect(DotDesktopListSelectionDialog.accept)
        self.buttonBox.rejected.connect(DotDesktopListSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DotDesktopListSelectionDialog)
        DotDesktopListSelectionDialog.setTabOrder(self.entriesList, self.subList)
        DotDesktopListSelectionDialog.setTabOrder(self.subList, self.buttonBox)

    def retranslateUi(self, DotDesktopListSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        DotDesktopListSelectionDialog.setWindowTitle(_translate("DotDesktopListSelectionDialog", "Select Entries"))
        self.label.setText(_translate("DotDesktopListSelectionDialog", "Select applicable entries:"))
        self.entriesList.setSortingEnabled(True)
        self.subList.setSortingEnabled(True)
