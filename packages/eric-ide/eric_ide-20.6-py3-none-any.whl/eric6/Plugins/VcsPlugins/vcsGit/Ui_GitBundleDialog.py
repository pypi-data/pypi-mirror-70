# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitBundleDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitBundleDialog(object):
    def setupUi(self, GitBundleDialog):
        GitBundleDialog.setObjectName("GitBundleDialog")
        GitBundleDialog.resize(450, 184)
        GitBundleDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitBundleDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(GitBundleDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.revisionsButton = QtWidgets.QRadioButton(self.groupBox)
        self.revisionsButton.setChecked(True)
        self.revisionsButton.setObjectName("revisionsButton")
        self.gridLayout.addWidget(self.revisionsButton, 0, 0, 1, 1)
        self.revisionsEdit = QtWidgets.QLineEdit(self.groupBox)
        self.revisionsEdit.setObjectName("revisionsEdit")
        self.gridLayout.addWidget(self.revisionsEdit, 0, 1, 1, 1)
        self.tagButton = QtWidgets.QRadioButton(self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 1, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(self.groupBox)
        self.tagCombo.setEnabled(False)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 1, 1, 1, 1)
        self.branchButton = QtWidgets.QRadioButton(self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 2, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(self.groupBox)
        self.branchCombo.setEnabled(False)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitBundleDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitBundleDialog)
        self.buttonBox.accepted.connect(GitBundleDialog.accept)
        self.buttonBox.rejected.connect(GitBundleDialog.reject)
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled)
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GitBundleDialog)
        GitBundleDialog.setTabOrder(self.tagButton, self.tagCombo)
        GitBundleDialog.setTabOrder(self.tagCombo, self.branchButton)
        GitBundleDialog.setTabOrder(self.branchButton, self.branchCombo)
        GitBundleDialog.setTabOrder(self.branchCombo, self.buttonBox)

    def retranslateUi(self, GitBundleDialog):
        _translate = QtCore.QCoreApplication.translate
        GitBundleDialog.setWindowTitle(_translate("GitBundleDialog", "Git Bundle"))
        self.groupBox.setTitle(_translate("GitBundleDialog", "Revision"))
        self.revisionsButton.setToolTip(_translate("GitBundleDialog", "Select to specify a revision or revision range"))
        self.revisionsButton.setText(_translate("GitBundleDialog", "Revisions:"))
        self.revisionsEdit.setToolTip(_translate("GitBundleDialog", "Enter  revisions or revision range expressions"))
        self.tagButton.setToolTip(_translate("GitBundleDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("GitBundleDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("GitBundleDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("GitBundleDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("GitBundleDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("GitBundleDialog", "Enter a branch name"))
