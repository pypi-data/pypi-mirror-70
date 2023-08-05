# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitCherryPickDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitCherryPickDialog(object):
    def setupUi(self, GitCherryPickDialog):
        GitCherryPickDialog.setObjectName("GitCherryPickDialog")
        GitCherryPickDialog.resize(450, 300)
        GitCherryPickDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GitCherryPickDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(GitCherryPickDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.commitsEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.commitsEdit.setTabChangesFocus(True)
        self.commitsEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.commitsEdit.setObjectName("commitsEdit")
        self.verticalLayout.addWidget(self.commitsEdit)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.appendCheckBox = QtWidgets.QCheckBox(GitCherryPickDialog)
        self.appendCheckBox.setChecked(True)
        self.appendCheckBox.setObjectName("appendCheckBox")
        self.verticalLayout_2.addWidget(self.appendCheckBox)
        self.signoffCheckBox = QtWidgets.QCheckBox(GitCherryPickDialog)
        self.signoffCheckBox.setObjectName("signoffCheckBox")
        self.verticalLayout_2.addWidget(self.signoffCheckBox)
        self.nocommitCheckBox = QtWidgets.QCheckBox(GitCherryPickDialog)
        self.nocommitCheckBox.setObjectName("nocommitCheckBox")
        self.verticalLayout_2.addWidget(self.nocommitCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitCherryPickDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(GitCherryPickDialog)
        self.buttonBox.accepted.connect(GitCherryPickDialog.accept)
        self.buttonBox.rejected.connect(GitCherryPickDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitCherryPickDialog)
        GitCherryPickDialog.setTabOrder(self.commitsEdit, self.appendCheckBox)
        GitCherryPickDialog.setTabOrder(self.appendCheckBox, self.signoffCheckBox)
        GitCherryPickDialog.setTabOrder(self.signoffCheckBox, self.nocommitCheckBox)

    def retranslateUi(self, GitCherryPickDialog):
        _translate = QtCore.QCoreApplication.translate
        GitCherryPickDialog.setWindowTitle(_translate("GitCherryPickDialog", "Git Cherry-pick"))
        self.groupBox.setTitle(_translate("GitCherryPickDialog", "Commits"))
        self.commitsEdit.setToolTip(_translate("GitCherryPickDialog", "Enter commits by id, branch or tag one per line"))
        self.appendCheckBox.setToolTip(_translate("GitCherryPickDialog", "Select to append cherry-pick info to the commit message"))
        self.appendCheckBox.setText(_translate("GitCherryPickDialog", "Append Cherry-pick &Info"))
        self.signoffCheckBox.setToolTip(_translate("GitCherryPickDialog", "Select to add a \'Signed-off-by\' line to the commit message"))
        self.signoffCheckBox.setText(_translate("GitCherryPickDialog", "Append \'&Signed-off-by\' line"))
        self.nocommitCheckBox.setToolTip(_translate("GitCherryPickDialog", "Select to not commit the cherry-pick"))
        self.nocommitCheckBox.setText(_translate("GitCherryPickDialog", "Don\'t &commit"))
