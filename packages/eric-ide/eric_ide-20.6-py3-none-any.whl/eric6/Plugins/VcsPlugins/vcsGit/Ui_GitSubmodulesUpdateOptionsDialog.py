# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitSubmodulesUpdateOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesUpdateOptionsDialog(object):
    def setupUi(self, GitSubmodulesUpdateOptionsDialog):
        GitSubmodulesUpdateOptionsDialog.setObjectName("GitSubmodulesUpdateOptionsDialog")
        GitSubmodulesUpdateOptionsDialog.resize(400, 458)
        GitSubmodulesUpdateOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesUpdateOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(GitSubmodulesUpdateOptionsDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkoutButton = QtWidgets.QRadioButton(self.groupBox)
        self.checkoutButton.setChecked(True)
        self.checkoutButton.setObjectName("checkoutButton")
        self.horizontalLayout.addWidget(self.checkoutButton)
        self.rebaseButton = QtWidgets.QRadioButton(self.groupBox)
        self.rebaseButton.setObjectName("rebaseButton")
        self.horizontalLayout.addWidget(self.rebaseButton)
        self.mergeButton = QtWidgets.QRadioButton(self.groupBox)
        self.mergeButton.setObjectName("mergeButton")
        self.horizontalLayout.addWidget(self.mergeButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.initCheckBox = QtWidgets.QCheckBox(GitSubmodulesUpdateOptionsDialog)
        self.initCheckBox.setObjectName("initCheckBox")
        self.verticalLayout.addWidget(self.initCheckBox)
        self.remoteCheckBox = QtWidgets.QCheckBox(GitSubmodulesUpdateOptionsDialog)
        self.remoteCheckBox.setObjectName("remoteCheckBox")
        self.verticalLayout.addWidget(self.remoteCheckBox)
        self.nofetchCheckBox = QtWidgets.QCheckBox(GitSubmodulesUpdateOptionsDialog)
        self.nofetchCheckBox.setEnabled(False)
        self.nofetchCheckBox.setObjectName("nofetchCheckBox")
        self.verticalLayout.addWidget(self.nofetchCheckBox)
        self.label = QtWidgets.QLabel(GitSubmodulesUpdateOptionsDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.submodulesList = QtWidgets.QListWidget(GitSubmodulesUpdateOptionsDialog)
        self.submodulesList.setAlternatingRowColors(True)
        self.submodulesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.submodulesList.setObjectName("submodulesList")
        self.verticalLayout.addWidget(self.submodulesList)
        self.forceCheckBox = QtWidgets.QCheckBox(GitSubmodulesUpdateOptionsDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.verticalLayout.addWidget(self.forceCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesUpdateOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesUpdateOptionsDialog)
        self.buttonBox.accepted.connect(GitSubmodulesUpdateOptionsDialog.accept)
        self.buttonBox.rejected.connect(GitSubmodulesUpdateOptionsDialog.reject)
        self.remoteCheckBox.toggled['bool'].connect(self.nofetchCheckBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesUpdateOptionsDialog)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.checkoutButton, self.rebaseButton)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.rebaseButton, self.mergeButton)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.mergeButton, self.initCheckBox)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.initCheckBox, self.remoteCheckBox)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.remoteCheckBox, self.nofetchCheckBox)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.nofetchCheckBox, self.submodulesList)
        GitSubmodulesUpdateOptionsDialog.setTabOrder(self.submodulesList, self.forceCheckBox)

    def retranslateUi(self, GitSubmodulesUpdateOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesUpdateOptionsDialog.setWindowTitle(_translate("GitSubmodulesUpdateOptionsDialog", "Submodule Update Options"))
        self.groupBox.setTitle(_translate("GitSubmodulesUpdateOptionsDialog", "Update Procedure"))
        self.checkoutButton.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to perform a \'checkout\' procedure"))
        self.checkoutButton.setText(_translate("GitSubmodulesUpdateOptionsDialog", "checkout"))
        self.rebaseButton.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to perform a \'rebase\' procedure"))
        self.rebaseButton.setText(_translate("GitSubmodulesUpdateOptionsDialog", "rebase"))
        self.mergeButton.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to perform a \'merge\' procedure"))
        self.mergeButton.setText(_translate("GitSubmodulesUpdateOptionsDialog", "merge"))
        self.initCheckBox.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to initialize submodules before the update"))
        self.initCheckBox.setText(_translate("GitSubmodulesUpdateOptionsDialog", "Initialize before Update"))
        self.remoteCheckBox.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Fetch remote changes before updating"))
        self.remoteCheckBox.setText(_translate("GitSubmodulesUpdateOptionsDialog", "Synchronize with remote"))
        self.nofetchCheckBox.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to not fetch the remote"))
        self.nofetchCheckBox.setText(_translate("GitSubmodulesUpdateOptionsDialog", "Don\'t Fetch"))
        self.label.setText(_translate("GitSubmodulesUpdateOptionsDialog", "Selected Submodules:"))
        self.submodulesList.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select the submodules to be updated"))
        self.forceCheckBox.setToolTip(_translate("GitSubmodulesUpdateOptionsDialog", "Select to enforce the update"))
        self.forceCheckBox.setText(_translate("GitSubmodulesUpdateOptionsDialog", "Enforce Operation"))
