# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitListDialog(object):
    def setupUi(self, GitListDialog):
        GitListDialog.setObjectName("GitListDialog")
        GitListDialog.resize(400, 300)
        GitListDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitListDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GitListDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.selectionList = QtWidgets.QListWidget(GitListDialog)
        self.selectionList.setAlternatingRowColors(True)
        self.selectionList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.selectionList.setObjectName("selectionList")
        self.verticalLayout.addWidget(self.selectionList)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitListDialog)
        self.buttonBox.accepted.connect(GitListDialog.accept)
        self.buttonBox.rejected.connect(GitListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitListDialog)

    def retranslateUi(self, GitListDialog):
        _translate = QtCore.QCoreApplication.translate
        GitListDialog.setWindowTitle(_translate("GitListDialog", "Git Select"))
        self.label.setText(_translate("GitListDialog", "Select from the list:"))
