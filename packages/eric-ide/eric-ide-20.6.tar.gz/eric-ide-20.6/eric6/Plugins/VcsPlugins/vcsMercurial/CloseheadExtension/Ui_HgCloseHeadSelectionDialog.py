# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsMercurial/CloseheadExtension/HgCloseHeadSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgCloseHeadSelectionDialog(object):
    def setupUi(self, HgCloseHeadSelectionDialog):
        HgCloseHeadSelectionDialog.setObjectName("HgCloseHeadSelectionDialog")
        HgCloseHeadSelectionDialog.resize(532, 402)
        HgCloseHeadSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgCloseHeadSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(HgCloseHeadSelectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.headsList = QtWidgets.QTreeWidget(HgCloseHeadSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.headsList.sizePolicy().hasHeightForWidth())
        self.headsList.setSizePolicy(sizePolicy)
        self.headsList.setAlternatingRowColors(True)
        self.headsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.headsList.setRootIsDecorated(False)
        self.headsList.setObjectName("headsList")
        self.verticalLayout.addWidget(self.headsList)
        self.label_2 = QtWidgets.QLabel(HgCloseHeadSelectionDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.logEdit = QtWidgets.QTextEdit(HgCloseHeadSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.logEdit.sizePolicy().hasHeightForWidth())
        self.logEdit.setSizePolicy(sizePolicy)
        self.logEdit.setTabChangesFocus(True)
        self.logEdit.setAcceptRichText(False)
        self.logEdit.setObjectName("logEdit")
        self.verticalLayout.addWidget(self.logEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgCloseHeadSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgCloseHeadSelectionDialog)
        self.buttonBox.accepted.connect(HgCloseHeadSelectionDialog.accept)
        self.buttonBox.rejected.connect(HgCloseHeadSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HgCloseHeadSelectionDialog)
        HgCloseHeadSelectionDialog.setTabOrder(self.headsList, self.logEdit)

    def retranslateUi(self, HgCloseHeadSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        HgCloseHeadSelectionDialog.setWindowTitle(_translate("HgCloseHeadSelectionDialog", "Close Heads"))
        self.label.setText(_translate("HgCloseHeadSelectionDialog", "Select heads to be closed:"))
        self.headsList.headerItem().setText(0, _translate("HgCloseHeadSelectionDialog", "Revision"))
        self.headsList.headerItem().setText(1, _translate("HgCloseHeadSelectionDialog", "Branch"))
        self.label_2.setText(_translate("HgCloseHeadSelectionDialog", "Commit Message:"))
