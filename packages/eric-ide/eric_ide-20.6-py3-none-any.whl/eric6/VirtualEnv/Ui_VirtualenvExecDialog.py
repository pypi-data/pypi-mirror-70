# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/VirtualEnv/VirtualenvExecDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VirtualenvExecDialog(object):
    def setupUi(self, VirtualenvExecDialog):
        VirtualenvExecDialog.setObjectName("VirtualenvExecDialog")
        VirtualenvExecDialog.resize(750, 600)
        VirtualenvExecDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(VirtualenvExecDialog)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.messagesGroup = QtWidgets.QGroupBox(VirtualenvExecDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.messagesGroup.sizePolicy().hasHeightForWidth())
        self.messagesGroup.setSizePolicy(sizePolicy)
        self.messagesGroup.setObjectName("messagesGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.messagesGroup)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contents = QtWidgets.QTextBrowser(self.messagesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.contents.sizePolicy().hasHeightForWidth())
        self.contents.setSizePolicy(sizePolicy)
        self.contents.setObjectName("contents")
        self.verticalLayout.addWidget(self.contents)
        self.verticalLayout_3.addWidget(self.messagesGroup)
        self.errorGroup = QtWidgets.QGroupBox(VirtualenvExecDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.errors = QtWidgets.QTextBrowser(self.errorGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errors.sizePolicy().hasHeightForWidth())
        self.errors.setSizePolicy(sizePolicy)
        self.errors.setObjectName("errors")
        self.verticalLayout_2.addWidget(self.errors)
        self.verticalLayout_3.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(VirtualenvExecDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(VirtualenvExecDialog)
        QtCore.QMetaObject.connectSlotsByName(VirtualenvExecDialog)
        VirtualenvExecDialog.setTabOrder(self.contents, self.errors)
        VirtualenvExecDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, VirtualenvExecDialog):
        _translate = QtCore.QCoreApplication.translate
        VirtualenvExecDialog.setWindowTitle(_translate("VirtualenvExecDialog", "Virtualenv Creation"))
        self.messagesGroup.setTitle(_translate("VirtualenvExecDialog", "Messages"))
        self.contents.setWhatsThis(_translate("VirtualenvExecDialog", "<b>virtualenv Execution</b>\n"
"<p>This shows the output of the virtualenv command.</p>"))
        self.errorGroup.setTitle(_translate("VirtualenvExecDialog", "Errors"))
        self.errors.setWhatsThis(_translate("VirtualenvExecDialog", "<b>virtualenv Execution</b>\n"
"<p>This shows the errors of the virtualenv command.</p>"))
