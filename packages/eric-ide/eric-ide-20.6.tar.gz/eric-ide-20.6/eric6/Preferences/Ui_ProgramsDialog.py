# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ProgramsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgramsDialog(object):
    def setupUi(self, ProgramsDialog):
        ProgramsDialog.setObjectName("ProgramsDialog")
        ProgramsDialog.resize(700, 570)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgramsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.programsList = QtWidgets.QTreeWidget(ProgramsDialog)
        self.programsList.setRootIsDecorated(False)
        self.programsList.setObjectName("programsList")
        self.verticalLayout.addWidget(self.programsList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ProgramsDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.showComboBox = QtWidgets.QComboBox(ProgramsDialog)
        self.showComboBox.setObjectName("showComboBox")
        self.horizontalLayout.addWidget(self.showComboBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(ProgramsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProgramsDialog)
        self.buttonBox.accepted.connect(ProgramsDialog.close)
        self.buttonBox.rejected.connect(ProgramsDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ProgramsDialog)

    def retranslateUi(self, ProgramsDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgramsDialog.setWindowTitle(_translate("ProgramsDialog", "External Tools"))
        self.programsList.setSortingEnabled(True)
        self.programsList.headerItem().setText(0, _translate("ProgramsDialog", "Path"))
        self.programsList.headerItem().setText(1, _translate("ProgramsDialog", "Version"))
        self.label.setText(_translate("ProgramsDialog", "Show:"))
        self.showComboBox.setToolTip(_translate("ProgramsDialog", "Select the kind of tools to show"))
