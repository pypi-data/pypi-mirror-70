# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitPullDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitPullDialog(object):
    def setupUi(self, GitPullDialog):
        GitPullDialog.setObjectName("GitPullDialog")
        GitPullDialog.resize(400, 344)
        GitPullDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitPullDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitPullDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.remotesComboBox = QtWidgets.QComboBox(GitPullDialog)
        self.remotesComboBox.setObjectName("remotesComboBox")
        self.gridLayout.addWidget(self.remotesComboBox, 0, 1, 1, 1)
        self.remoteEdit = QtWidgets.QLineEdit(GitPullDialog)
        self.remoteEdit.setReadOnly(True)
        self.remoteEdit.setObjectName("remoteEdit")
        self.gridLayout.addWidget(self.remoteEdit, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(GitPullDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.updateButton = QtWidgets.QPushButton(GitPullDialog)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.remoteBranchesList = QtWidgets.QListWidget(GitPullDialog)
        self.remoteBranchesList.setAlternatingRowColors(True)
        self.remoteBranchesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.remoteBranchesList.setObjectName("remoteBranchesList")
        self.gridLayout.addWidget(self.remoteBranchesList, 2, 1, 1, 1)
        self.pruneCheckBox = QtWidgets.QCheckBox(GitPullDialog)
        self.pruneCheckBox.setObjectName("pruneCheckBox")
        self.gridLayout.addWidget(self.pruneCheckBox, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitPullDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.retranslateUi(GitPullDialog)
        self.buttonBox.accepted.connect(GitPullDialog.accept)
        self.buttonBox.rejected.connect(GitPullDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitPullDialog)
        GitPullDialog.setTabOrder(self.remotesComboBox, self.remoteEdit)
        GitPullDialog.setTabOrder(self.remoteEdit, self.remoteBranchesList)
        GitPullDialog.setTabOrder(self.remoteBranchesList, self.updateButton)
        GitPullDialog.setTabOrder(self.updateButton, self.pruneCheckBox)

    def retranslateUi(self, GitPullDialog):
        _translate = QtCore.QCoreApplication.translate
        GitPullDialog.setWindowTitle(_translate("GitPullDialog", "Git Pull"))
        self.label.setText(_translate("GitPullDialog", "Remote Repository:"))
        self.remotesComboBox.setToolTip(_translate("GitPullDialog", "Select the remote repository to pull from"))
        self.label_2.setText(_translate("GitPullDialog", "Remote Branches:"))
        self.updateButton.setToolTip(_translate("GitPullDialog", "Press to update the list of remote branches"))
        self.updateButton.setText(_translate("GitPullDialog", "Update"))
        self.remoteBranchesList.setToolTip(_translate("GitPullDialog", "Select the remote branches to be pulled"))
        self.pruneCheckBox.setToolTip(_translate("GitPullDialog", "Select to remove non-existing tracking references "))
        self.pruneCheckBox.setText(_translate("GitPullDialog", "Prune obsolete tracking references"))
