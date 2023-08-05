# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/CondaInterface/CondaExecDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CondaExecDialog(object):
    def setupUi(self, CondaExecDialog):
        CondaExecDialog.setObjectName("CondaExecDialog")
        CondaExecDialog.resize(750, 600)
        CondaExecDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(CondaExecDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.messagesGroup = QtWidgets.QGroupBox(CondaExecDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.messagesGroup.sizePolicy().hasHeightForWidth())
        self.messagesGroup.setSizePolicy(sizePolicy)
        self.messagesGroup.setObjectName("messagesGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.messagesGroup)
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
        self.progressLabel = QtWidgets.QLabel(CondaExecDialog)
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout_3.addWidget(self.progressLabel)
        self.progressBar = QtWidgets.QProgressBar(CondaExecDialog)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.errorGroup = QtWidgets.QGroupBox(CondaExecDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.errorGroup)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(CondaExecDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(CondaExecDialog)
        self.buttonBox.accepted.connect(CondaExecDialog.accept)
        self.buttonBox.rejected.connect(CondaExecDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CondaExecDialog)
        CondaExecDialog.setTabOrder(self.contents, self.errors)

    def retranslateUi(self, CondaExecDialog):
        _translate = QtCore.QCoreApplication.translate
        CondaExecDialog.setWindowTitle(_translate("CondaExecDialog", "Conda Execution"))
        self.messagesGroup.setTitle(_translate("CondaExecDialog", "Messages"))
        self.contents.setWhatsThis(_translate("CondaExecDialog", "<b>conda Execution</b>\n"
"<p>This shows the output of the conda command.</p>"))
        self.errorGroup.setTitle(_translate("CondaExecDialog", "Errors"))
        self.errors.setWhatsThis(_translate("CondaExecDialog", "<b>conda Execution</b>\n"
"<p>This shows the errors of the conda command.</p>"))
