# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitSubmodulesSyncDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesSyncDialog(object):
    def setupUi(self, GitSubmodulesSyncDialog):
        GitSubmodulesSyncDialog.setObjectName("GitSubmodulesSyncDialog")
        GitSubmodulesSyncDialog.resize(400, 300)
        GitSubmodulesSyncDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesSyncDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GitSubmodulesSyncDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.submodulesList = QtWidgets.QListWidget(GitSubmodulesSyncDialog)
        self.submodulesList.setAlternatingRowColors(True)
        self.submodulesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.submodulesList.setObjectName("submodulesList")
        self.verticalLayout.addWidget(self.submodulesList)
        self.recursiveCheckBox = QtWidgets.QCheckBox(GitSubmodulesSyncDialog)
        self.recursiveCheckBox.setObjectName("recursiveCheckBox")
        self.verticalLayout.addWidget(self.recursiveCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesSyncDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesSyncDialog)
        self.buttonBox.accepted.connect(GitSubmodulesSyncDialog.accept)
        self.buttonBox.rejected.connect(GitSubmodulesSyncDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesSyncDialog)

    def retranslateUi(self, GitSubmodulesSyncDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesSyncDialog.setWindowTitle(_translate("GitSubmodulesSyncDialog", "Synchronize Submodule URLs"))
        self.label.setText(_translate("GitSubmodulesSyncDialog", "Selected Submodules:"))
        self.submodulesList.setToolTip(_translate("GitSubmodulesSyncDialog", "Select the submodules to be synchronized"))
        self.recursiveCheckBox.setToolTip(_translate("GitSubmodulesSyncDialog", "Select to perform a recursive synchronization"))
        self.recursiveCheckBox.setText(_translate("GitSubmodulesSyncDialog", "Recursive Operation"))
