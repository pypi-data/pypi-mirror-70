# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitPatchStatisticsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitPatchStatisticsDialog(object):
    def setupUi(self, GitPatchStatisticsDialog):
        GitPatchStatisticsDialog.setObjectName("GitPatchStatisticsDialog")
        GitPatchStatisticsDialog.resize(550, 450)
        GitPatchStatisticsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitPatchStatisticsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GitPatchStatisticsDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.changesTreeWidget = QtWidgets.QTreeWidget(GitPatchStatisticsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.changesTreeWidget.sizePolicy().hasHeightForWidth())
        self.changesTreeWidget.setSizePolicy(sizePolicy)
        self.changesTreeWidget.setAlternatingRowColors(True)
        self.changesTreeWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.changesTreeWidget.setRootIsDecorated(False)
        self.changesTreeWidget.setItemsExpandable(False)
        self.changesTreeWidget.setObjectName("changesTreeWidget")
        self.verticalLayout.addWidget(self.changesTreeWidget)
        self.label_2 = QtWidgets.QLabel(GitPatchStatisticsDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.summaryEdit = QtWidgets.QPlainTextEdit(GitPatchStatisticsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.summaryEdit.sizePolicy().hasHeightForWidth())
        self.summaryEdit.setSizePolicy(sizePolicy)
        self.summaryEdit.setTabChangesFocus(True)
        self.summaryEdit.setReadOnly(True)
        self.summaryEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.summaryEdit.setObjectName("summaryEdit")
        self.verticalLayout.addWidget(self.summaryEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitPatchStatisticsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitPatchStatisticsDialog)
        self.buttonBox.accepted.connect(GitPatchStatisticsDialog.accept)
        self.buttonBox.rejected.connect(GitPatchStatisticsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitPatchStatisticsDialog)

    def retranslateUi(self, GitPatchStatisticsDialog):
        _translate = QtCore.QCoreApplication.translate
        GitPatchStatisticsDialog.setWindowTitle(_translate("GitPatchStatisticsDialog", "Patch Statistics"))
        self.label.setText(_translate("GitPatchStatisticsDialog", "Insertions and Deletions:"))
        self.changesTreeWidget.setSortingEnabled(True)
        self.changesTreeWidget.headerItem().setText(0, _translate("GitPatchStatisticsDialog", "# Insertions"))
        self.changesTreeWidget.headerItem().setText(1, _translate("GitPatchStatisticsDialog", "# Deletions"))
        self.changesTreeWidget.headerItem().setText(2, _translate("GitPatchStatisticsDialog", "File"))
        self.label_2.setText(_translate("GitPatchStatisticsDialog", "Summary Information:"))
