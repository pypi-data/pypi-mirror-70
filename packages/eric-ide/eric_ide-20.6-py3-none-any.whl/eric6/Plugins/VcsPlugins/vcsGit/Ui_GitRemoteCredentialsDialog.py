# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitRemoteCredentialsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitRemoteCredentialsDialog(object):
    def setupUi(self, GitRemoteCredentialsDialog):
        GitRemoteCredentialsDialog.setObjectName("GitRemoteCredentialsDialog")
        GitRemoteCredentialsDialog.resize(700, 185)
        GitRemoteCredentialsDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitRemoteCredentialsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitRemoteCredentialsDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(GitRemoteCredentialsDialog)
        self.nameEdit.setToolTip("")
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitRemoteCredentialsDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.urlEdit = QtWidgets.QLineEdit(GitRemoteCredentialsDialog)
        self.urlEdit.setToolTip("")
        self.urlEdit.setReadOnly(True)
        self.urlEdit.setObjectName("urlEdit")
        self.gridLayout.addWidget(self.urlEdit, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(GitRemoteCredentialsDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.userEdit = QtWidgets.QLineEdit(self.groupBox)
        self.userEdit.setObjectName("userEdit")
        self.horizontalLayout.addWidget(self.userEdit)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.passwordEdit = QtWidgets.QLineEdit(self.groupBox)
        self.passwordEdit.setEnabled(False)
        self.passwordEdit.setObjectName("passwordEdit")
        self.horizontalLayout.addWidget(self.passwordEdit)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitRemoteCredentialsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GitRemoteCredentialsDialog)
        self.buttonBox.accepted.connect(GitRemoteCredentialsDialog.accept)
        self.buttonBox.rejected.connect(GitRemoteCredentialsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitRemoteCredentialsDialog)

    def retranslateUi(self, GitRemoteCredentialsDialog):
        _translate = QtCore.QCoreApplication.translate
        GitRemoteCredentialsDialog.setWindowTitle(_translate("GitRemoteCredentialsDialog", "Git Remote Credentials"))
        self.label.setText(_translate("GitRemoteCredentialsDialog", "Name:"))
        self.label_2.setText(_translate("GitRemoteCredentialsDialog", "URL:"))
        self.groupBox.setTitle(_translate("GitRemoteCredentialsDialog", "Credentials"))
        self.label_3.setText(_translate("GitRemoteCredentialsDialog", "Username:"))
        self.userEdit.setToolTip(_translate("GitRemoteCredentialsDialog", "Enter the user name for the remote repository"))
        self.label_4.setText(_translate("GitRemoteCredentialsDialog", "Password:"))
        self.passwordEdit.setToolTip(_translate("GitRemoteCredentialsDialog", "Enter the password for the remote repository"))
