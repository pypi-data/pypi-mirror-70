# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitSubmodulesListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesListDialog(object):
    def setupUi(self, GitSubmodulesListDialog):
        GitSubmodulesListDialog.setObjectName("GitSubmodulesListDialog")
        GitSubmodulesListDialog.resize(500, 300)
        GitSubmodulesListDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesListDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.submodulesList = QtWidgets.QTreeWidget(GitSubmodulesListDialog)
        self.submodulesList.setAlternatingRowColors(True)
        self.submodulesList.setRootIsDecorated(False)
        self.submodulesList.setItemsExpandable(False)
        self.submodulesList.setExpandsOnDoubleClick(False)
        self.submodulesList.setObjectName("submodulesList")
        self.submodulesList.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.submodulesList)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesListDialog)
        self.buttonBox.accepted.connect(GitSubmodulesListDialog.accept)
        self.buttonBox.rejected.connect(GitSubmodulesListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesListDialog)

    def retranslateUi(self, GitSubmodulesListDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesListDialog.setWindowTitle(_translate("GitSubmodulesListDialog", "Defined Submodules"))
        self.submodulesList.headerItem().setText(0, _translate("GitSubmodulesListDialog", "Name"))
        self.submodulesList.headerItem().setText(1, _translate("GitSubmodulesListDialog", "Path"))
        self.submodulesList.headerItem().setText(2, _translate("GitSubmodulesListDialog", "URL"))
        self.submodulesList.headerItem().setText(3, _translate("GitSubmodulesListDialog", "Branch"))
