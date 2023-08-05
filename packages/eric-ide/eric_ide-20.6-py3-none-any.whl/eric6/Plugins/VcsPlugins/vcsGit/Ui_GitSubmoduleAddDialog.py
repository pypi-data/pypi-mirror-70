# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitSubmoduleAddDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitSubmoduleAddDialog(object):
    def setupUi(self, GitSubmoduleAddDialog):
        GitSubmoduleAddDialog.setObjectName("GitSubmoduleAddDialog")
        GitSubmoduleAddDialog.resize(562, 202)
        GitSubmoduleAddDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitSubmoduleAddDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.TextLabel2 = QtWidgets.QLabel(GitSubmoduleAddDialog)
        self.TextLabel2.setObjectName("TextLabel2")
        self.gridLayout.addWidget(self.TextLabel2, 0, 0, 1, 1)
        self.submoduleUrlCombo = QtWidgets.QComboBox(GitSubmoduleAddDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submoduleUrlCombo.sizePolicy().hasHeightForWidth())
        self.submoduleUrlCombo.setSizePolicy(sizePolicy)
        self.submoduleUrlCombo.setEditable(True)
        self.submoduleUrlCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.submoduleUrlCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.submoduleUrlCombo.setObjectName("submoduleUrlCombo")
        self.gridLayout.addWidget(self.submoduleUrlCombo, 0, 1, 1, 1)
        self.submoduleUrlButton = QtWidgets.QToolButton(GitSubmoduleAddDialog)
        self.submoduleUrlButton.setObjectName("submoduleUrlButton")
        self.gridLayout.addWidget(self.submoduleUrlButton, 0, 2, 1, 1)
        self.submoduleUrlClearHistoryButton = QtWidgets.QToolButton(GitSubmoduleAddDialog)
        self.submoduleUrlClearHistoryButton.setObjectName("submoduleUrlClearHistoryButton")
        self.gridLayout.addWidget(self.submoduleUrlClearHistoryButton, 0, 3, 1, 1)
        self.TextLabel4 = QtWidgets.QLabel(GitSubmoduleAddDialog)
        self.TextLabel4.setObjectName("TextLabel4")
        self.gridLayout.addWidget(self.TextLabel4, 1, 0, 1, 1)
        self.submoduleDirEdit = QtWidgets.QLineEdit(GitSubmoduleAddDialog)
        self.submoduleDirEdit.setObjectName("submoduleDirEdit")
        self.gridLayout.addWidget(self.submoduleDirEdit, 1, 1, 1, 1)
        self.submoduleDirButton = QtWidgets.QToolButton(GitSubmoduleAddDialog)
        self.submoduleDirButton.setObjectName("submoduleDirButton")
        self.gridLayout.addWidget(self.submoduleDirButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(GitSubmoduleAddDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.branchEdit = QtWidgets.QLineEdit(GitSubmoduleAddDialog)
        self.branchEdit.setObjectName("branchEdit")
        self.gridLayout.addWidget(self.branchEdit, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitSubmoduleAddDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(GitSubmoduleAddDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 3, 1, 1, 1)
        self.forceCheckBox = QtWidgets.QCheckBox(GitSubmoduleAddDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.gridLayout.addWidget(self.forceCheckBox, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmoduleAddDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        self.TextLabel2.setBuddy(self.submoduleUrlCombo)
        self.TextLabel4.setBuddy(self.submoduleDirEdit)
        self.label.setBuddy(self.branchEdit)
        self.label_2.setBuddy(self.nameEdit)

        self.retranslateUi(GitSubmoduleAddDialog)
        self.buttonBox.accepted.connect(GitSubmoduleAddDialog.accept)
        self.buttonBox.rejected.connect(GitSubmoduleAddDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitSubmoduleAddDialog)
        GitSubmoduleAddDialog.setTabOrder(self.submoduleUrlCombo, self.submoduleUrlButton)
        GitSubmoduleAddDialog.setTabOrder(self.submoduleUrlButton, self.submoduleUrlClearHistoryButton)
        GitSubmoduleAddDialog.setTabOrder(self.submoduleUrlClearHistoryButton, self.submoduleDirEdit)
        GitSubmoduleAddDialog.setTabOrder(self.submoduleDirEdit, self.submoduleDirButton)
        GitSubmoduleAddDialog.setTabOrder(self.submoduleDirButton, self.branchEdit)
        GitSubmoduleAddDialog.setTabOrder(self.branchEdit, self.nameEdit)
        GitSubmoduleAddDialog.setTabOrder(self.nameEdit, self.forceCheckBox)

    def retranslateUi(self, GitSubmoduleAddDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmoduleAddDialog.setWindowTitle(_translate("GitSubmoduleAddDialog", "Add Submodule"))
        self.TextLabel2.setText(_translate("GitSubmoduleAddDialog", "&URL:"))
        self.submoduleUrlCombo.setToolTip(_translate("GitSubmoduleAddDialog", "Enter the URL of the repository"))
        self.submoduleUrlButton.setToolTip(_translate("GitSubmoduleAddDialog", "Select the repository URL via a directory selection dialog"))
        self.submoduleUrlClearHistoryButton.setToolTip(_translate("GitSubmoduleAddDialog", "Press to clear the history of entered repository URLs"))
        self.TextLabel4.setText(_translate("GitSubmoduleAddDialog", "Submodule &Directory:"))
        self.submoduleDirEdit.setToolTip(_translate("GitSubmoduleAddDialog", "Enter the directory for the submodule (leave empty to use default)."))
        self.label.setText(_translate("GitSubmoduleAddDialog", "&Branch:"))
        self.branchEdit.setToolTip(_translate("GitSubmoduleAddDialog", "Enter a branch name"))
        self.label_2.setText(_translate("GitSubmoduleAddDialog", "&Logical Name:"))
        self.nameEdit.setToolTip(_translate("GitSubmoduleAddDialog", "Enter a logical name"))
        self.forceCheckBox.setToolTip(_translate("GitSubmoduleAddDialog", "Select to enforce the operation"))
        self.forceCheckBox.setText(_translate("GitSubmoduleAddDialog", "&Force Operation"))
