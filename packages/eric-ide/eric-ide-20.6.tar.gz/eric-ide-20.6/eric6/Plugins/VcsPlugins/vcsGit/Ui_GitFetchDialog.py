# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitFetchDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitFetchDialog(object):
    def setupUi(self, GitFetchDialog):
        GitFetchDialog.setObjectName("GitFetchDialog")
        GitFetchDialog.resize(400, 350)
        GitFetchDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitFetchDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitFetchDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.remotesComboBox = QtWidgets.QComboBox(GitFetchDialog)
        self.remotesComboBox.setObjectName("remotesComboBox")
        self.gridLayout.addWidget(self.remotesComboBox, 0, 1, 1, 1)
        self.remoteEdit = QtWidgets.QLineEdit(GitFetchDialog)
        self.remoteEdit.setReadOnly(True)
        self.remoteEdit.setObjectName("remoteEdit")
        self.gridLayout.addWidget(self.remoteEdit, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(GitFetchDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.updateButton = QtWidgets.QPushButton(GitFetchDialog)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout.addWidget(self.updateButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.remoteBranchesList = QtWidgets.QListWidget(GitFetchDialog)
        self.remoteBranchesList.setAlternatingRowColors(True)
        self.remoteBranchesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.remoteBranchesList.setObjectName("remoteBranchesList")
        self.gridLayout.addWidget(self.remoteBranchesList, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(GitFetchDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.localBranchComboBox = QtWidgets.QComboBox(GitFetchDialog)
        self.localBranchComboBox.setEditable(True)
        self.localBranchComboBox.setObjectName("localBranchComboBox")
        self.gridLayout.addWidget(self.localBranchComboBox, 3, 1, 1, 1)
        self.pruneCheckBox = QtWidgets.QCheckBox(GitFetchDialog)
        self.pruneCheckBox.setObjectName("pruneCheckBox")
        self.gridLayout.addWidget(self.pruneCheckBox, 4, 0, 1, 2)
        self.tagsCheckBox = QtWidgets.QCheckBox(GitFetchDialog)
        self.tagsCheckBox.setObjectName("tagsCheckBox")
        self.gridLayout.addWidget(self.tagsCheckBox, 5, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitFetchDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)

        self.retranslateUi(GitFetchDialog)
        self.buttonBox.accepted.connect(GitFetchDialog.accept)
        self.buttonBox.rejected.connect(GitFetchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitFetchDialog)
        GitFetchDialog.setTabOrder(self.remotesComboBox, self.remoteEdit)
        GitFetchDialog.setTabOrder(self.remoteEdit, self.remoteBranchesList)
        GitFetchDialog.setTabOrder(self.remoteBranchesList, self.updateButton)
        GitFetchDialog.setTabOrder(self.updateButton, self.localBranchComboBox)
        GitFetchDialog.setTabOrder(self.localBranchComboBox, self.pruneCheckBox)
        GitFetchDialog.setTabOrder(self.pruneCheckBox, self.tagsCheckBox)

    def retranslateUi(self, GitFetchDialog):
        _translate = QtCore.QCoreApplication.translate
        GitFetchDialog.setWindowTitle(_translate("GitFetchDialog", "Git Fetch"))
        self.label.setText(_translate("GitFetchDialog", "Remote Repository:"))
        self.remotesComboBox.setToolTip(_translate("GitFetchDialog", "Select the remote repository to fetch from"))
        self.label_2.setText(_translate("GitFetchDialog", "Remote Branches:"))
        self.updateButton.setToolTip(_translate("GitFetchDialog", "Press to update the list of remote branches"))
        self.updateButton.setText(_translate("GitFetchDialog", "Update"))
        self.remoteBranchesList.setToolTip(_translate("GitFetchDialog", "Select the remote branches to be fetched"))
        self.label_3.setText(_translate("GitFetchDialog", "Local Branch:"))
        self.localBranchComboBox.setToolTip(_translate("GitFetchDialog", "Select the local branch to fetch into"))
        self.pruneCheckBox.setToolTip(_translate("GitFetchDialog", "Select to remove non-existing tracking references "))
        self.pruneCheckBox.setText(_translate("GitFetchDialog", "Prune obsolete tracking references"))
        self.tagsCheckBox.setToolTip(_translate("GitFetchDialog", "Select to fetch tags as well"))
        self.tagsCheckBox.setText(_translate("GitFetchDialog", "Include tags"))
