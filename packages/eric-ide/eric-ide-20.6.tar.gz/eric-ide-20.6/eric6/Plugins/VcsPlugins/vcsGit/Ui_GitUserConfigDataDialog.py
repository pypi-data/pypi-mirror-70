# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitUserConfigDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitUserConfigDataDialog(object):
    def setupUi(self, GitUserConfigDataDialog):
        GitUserConfigDataDialog.setObjectName("GitUserConfigDataDialog")
        GitUserConfigDataDialog.resize(400, 184)
        GitUserConfigDataDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitUserConfigDataDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(GitUserConfigDataDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.firstNameEdit = E5ClearableLineEdit(self.groupBox)
        self.firstNameEdit.setObjectName("firstNameEdit")
        self.gridLayout.addWidget(self.firstNameEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lastNameEdit = E5ClearableLineEdit(self.groupBox)
        self.lastNameEdit.setObjectName("lastNameEdit")
        self.gridLayout.addWidget(self.lastNameEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.emailEdit = E5ClearableLineEdit(self.groupBox)
        self.emailEdit.setObjectName("emailEdit")
        self.gridLayout.addWidget(self.emailEdit, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitUserConfigDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitUserConfigDataDialog)
        self.buttonBox.accepted.connect(GitUserConfigDataDialog.accept)
        self.buttonBox.rejected.connect(GitUserConfigDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitUserConfigDataDialog)
        GitUserConfigDataDialog.setTabOrder(self.firstNameEdit, self.lastNameEdit)
        GitUserConfigDataDialog.setTabOrder(self.lastNameEdit, self.emailEdit)
        GitUserConfigDataDialog.setTabOrder(self.emailEdit, self.buttonBox)

    def retranslateUi(self, GitUserConfigDataDialog):
        _translate = QtCore.QCoreApplication.translate
        GitUserConfigDataDialog.setWindowTitle(_translate("GitUserConfigDataDialog", "Git User Data"))
        self.groupBox.setTitle(_translate("GitUserConfigDataDialog", "User Data"))
        self.label.setText(_translate("GitUserConfigDataDialog", "First Name:"))
        self.firstNameEdit.setToolTip(_translate("GitUserConfigDataDialog", "Enter the first name"))
        self.label_2.setText(_translate("GitUserConfigDataDialog", "Last Name:"))
        self.lastNameEdit.setToolTip(_translate("GitUserConfigDataDialog", "Enter the last name"))
        self.label_3.setText(_translate("GitUserConfigDataDialog", "Email:"))
        self.emailEdit.setToolTip(_translate("GitUserConfigDataDialog", "Enter the email address"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
