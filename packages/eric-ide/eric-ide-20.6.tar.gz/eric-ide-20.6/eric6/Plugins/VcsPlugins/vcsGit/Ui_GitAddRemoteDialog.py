# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitAddRemoteDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitAddRemoteDialog(object):
    def setupUi(self, GitAddRemoteDialog):
        GitAddRemoteDialog.setObjectName("GitAddRemoteDialog")
        GitAddRemoteDialog.resize(700, 185)
        GitAddRemoteDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitAddRemoteDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitAddRemoteDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(GitAddRemoteDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitAddRemoteDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.urlEdit = QtWidgets.QLineEdit(GitAddRemoteDialog)
        self.urlEdit.setObjectName("urlEdit")
        self.gridLayout.addWidget(self.urlEdit, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(GitAddRemoteDialog)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(GitAddRemoteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GitAddRemoteDialog)
        self.buttonBox.accepted.connect(GitAddRemoteDialog.accept)
        self.buttonBox.rejected.connect(GitAddRemoteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitAddRemoteDialog)

    def retranslateUi(self, GitAddRemoteDialog):
        _translate = QtCore.QCoreApplication.translate
        GitAddRemoteDialog.setWindowTitle(_translate("GitAddRemoteDialog", "Git Add Remote"))
        self.label.setText(_translate("GitAddRemoteDialog", "Name:"))
        self.nameEdit.setToolTip(_translate("GitAddRemoteDialog", "Enter the remote name"))
        self.label_2.setText(_translate("GitAddRemoteDialog", "URL:"))
        self.urlEdit.setToolTip(_translate("GitAddRemoteDialog", "Enter the remote URL"))
        self.groupBox.setTitle(_translate("GitAddRemoteDialog", "Credentials"))
        self.label_3.setText(_translate("GitAddRemoteDialog", "Username:"))
        self.userEdit.setToolTip(_translate("GitAddRemoteDialog", "Enter the user name for the remote repository"))
        self.label_4.setText(_translate("GitAddRemoteDialog", "Password:"))
        self.passwordEdit.setToolTip(_translate("GitAddRemoteDialog", "Enter the password for the remote repository"))
