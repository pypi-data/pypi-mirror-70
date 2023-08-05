# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitTagBranchListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitTagBranchListDialog(object):
    def setupUi(self, GitTagBranchListDialog):
        GitTagBranchListDialog.setObjectName("GitTagBranchListDialog")
        GitTagBranchListDialog.resize(634, 494)
        GitTagBranchListDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(GitTagBranchListDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tagList = QtWidgets.QTreeWidget(GitTagBranchListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tagList.sizePolicy().hasHeightForWidth())
        self.tagList.setSizePolicy(sizePolicy)
        self.tagList.setAlternatingRowColors(True)
        self.tagList.setRootIsDecorated(False)
        self.tagList.setItemsExpandable(False)
        self.tagList.setObjectName("tagList")
        self.vboxlayout.addWidget(self.tagList)
        self.errorGroup = QtWidgets.QGroupBox(GitTagBranchListDialog)
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
        self.vboxlayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(GitTagBranchListDialog)
        self.inputGroup.setObjectName("inputGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.inputGroup)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self.gridlayout.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self.gridlayout.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.vboxlayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitTagBranchListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(GitTagBranchListDialog)
        QtCore.QMetaObject.connectSlotsByName(GitTagBranchListDialog)
        GitTagBranchListDialog.setTabOrder(self.tagList, self.errors)
        GitTagBranchListDialog.setTabOrder(self.errors, self.input)
        GitTagBranchListDialog.setTabOrder(self.input, self.passwordCheckBox)
        GitTagBranchListDialog.setTabOrder(self.passwordCheckBox, self.sendButton)
        GitTagBranchListDialog.setTabOrder(self.sendButton, self.buttonBox)

    def retranslateUi(self, GitTagBranchListDialog):
        _translate = QtCore.QCoreApplication.translate
        GitTagBranchListDialog.setWindowTitle(_translate("GitTagBranchListDialog", "Git Tag List"))
        GitTagBranchListDialog.setWhatsThis(_translate("GitTagBranchListDialog", "<b>Git Tag/Branch List</b>\n"
"<p>This dialog shows a list of the projects tags or branches.</p>"))
        self.tagList.setWhatsThis(_translate("GitTagBranchListDialog", "<b>Tag/Branches List</b>\n"
"<p>This shows a list of the projects tags or branches.</p>"))
        self.tagList.setSortingEnabled(True)
        self.tagList.headerItem().setText(0, _translate("GitTagBranchListDialog", "Commit"))
        self.tagList.headerItem().setText(1, _translate("GitTagBranchListDialog", "Name"))
        self.errorGroup.setTitle(_translate("GitTagBranchListDialog", "Errors"))
        self.inputGroup.setTitle(_translate("GitTagBranchListDialog", "Input"))
        self.sendButton.setToolTip(_translate("GitTagBranchListDialog", "Press to send the input to the git process"))
        self.sendButton.setText(_translate("GitTagBranchListDialog", "&Send"))
        self.sendButton.setShortcut(_translate("GitTagBranchListDialog", "Alt+S"))
        self.input.setToolTip(_translate("GitTagBranchListDialog", "Enter data to be sent to the git process"))
        self.passwordCheckBox.setToolTip(_translate("GitTagBranchListDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("GitTagBranchListDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("GitTagBranchListDialog", "Alt+P"))
