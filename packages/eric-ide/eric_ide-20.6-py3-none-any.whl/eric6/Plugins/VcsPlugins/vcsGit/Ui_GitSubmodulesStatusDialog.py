# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitSubmodulesStatusDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitSubmodulesStatusDialog(object):
    def setupUi(self, GitSubmodulesStatusDialog):
        GitSubmodulesStatusDialog.setObjectName("GitSubmodulesStatusDialog")
        GitSubmodulesStatusDialog.resize(700, 400)
        GitSubmodulesStatusDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitSubmodulesStatusDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.statusList = QtWidgets.QTreeWidget(GitSubmodulesStatusDialog)
        self.statusList.setAlternatingRowColors(True)
        self.statusList.setRootIsDecorated(False)
        self.statusList.setItemsExpandable(False)
        self.statusList.setObjectName("statusList")
        self.verticalLayout.addWidget(self.statusList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.indexCheckBox = QtWidgets.QCheckBox(GitSubmodulesStatusDialog)
        self.indexCheckBox.setObjectName("indexCheckBox")
        self.horizontalLayout.addWidget(self.indexCheckBox)
        self.recursiveCheckBox = QtWidgets.QCheckBox(GitSubmodulesStatusDialog)
        self.recursiveCheckBox.setObjectName("recursiveCheckBox")
        self.horizontalLayout.addWidget(self.recursiveCheckBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.errorGroup = QtWidgets.QGroupBox(GitSubmodulesStatusDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitSubmodulesStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitSubmodulesStatusDialog)
        self.buttonBox.accepted.connect(GitSubmodulesStatusDialog.accept)
        self.buttonBox.rejected.connect(GitSubmodulesStatusDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitSubmodulesStatusDialog)
        GitSubmodulesStatusDialog.setTabOrder(self.statusList, self.indexCheckBox)
        GitSubmodulesStatusDialog.setTabOrder(self.indexCheckBox, self.recursiveCheckBox)
        GitSubmodulesStatusDialog.setTabOrder(self.recursiveCheckBox, self.errors)

    def retranslateUi(self, GitSubmodulesStatusDialog):
        _translate = QtCore.QCoreApplication.translate
        GitSubmodulesStatusDialog.setWindowTitle(_translate("GitSubmodulesStatusDialog", "Submodules Status"))
        self.statusList.headerItem().setText(0, _translate("GitSubmodulesStatusDialog", "Submodule"))
        self.statusList.headerItem().setText(1, _translate("GitSubmodulesStatusDialog", "Status"))
        self.statusList.headerItem().setText(2, _translate("GitSubmodulesStatusDialog", "Commit ID"))
        self.statusList.headerItem().setText(3, _translate("GitSubmodulesStatusDialog", "Info"))
        self.indexCheckBox.setToolTip(_translate("GitSubmodulesStatusDialog", "Select to show the status for the index"))
        self.indexCheckBox.setText(_translate("GitSubmodulesStatusDialog", "Show Status for Index"))
        self.recursiveCheckBox.setToolTip(_translate("GitSubmodulesStatusDialog", "Perform a recursive operation"))
        self.recursiveCheckBox.setText(_translate("GitSubmodulesStatusDialog", "Recursive"))
        self.errorGroup.setTitle(_translate("GitSubmodulesStatusDialog", "Errors"))
