# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsMercurial/HgOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgOptionsDialog(object):
    def setupUi(self, HgOptionsDialog):
        HgOptionsDialog.setObjectName("HgOptionsDialog")
        HgOptionsDialog.resize(565, 78)
        HgOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextLabel5 = QtWidgets.QLabel(HgOptionsDialog)
        self.TextLabel5.setObjectName("TextLabel5")
        self.horizontalLayout.addWidget(self.TextLabel5)
        self.vcsLogEdit = QtWidgets.QLineEdit(HgOptionsDialog)
        self.vcsLogEdit.setObjectName("vcsLogEdit")
        self.horizontalLayout.addWidget(self.vcsLogEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.TextLabel5.setBuddy(self.vcsLogEdit)

        self.retranslateUi(HgOptionsDialog)
        self.buttonBox.accepted.connect(HgOptionsDialog.accept)
        self.buttonBox.rejected.connect(HgOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HgOptionsDialog)

    def retranslateUi(self, HgOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        HgOptionsDialog.setWindowTitle(_translate("HgOptionsDialog", "Initial Commit"))
        HgOptionsDialog.setWhatsThis(_translate("HgOptionsDialog", "<b>Initial Commit Dialog</b>\n"
"<p>Enter the message for the initial commit.</p>"))
        self.TextLabel5.setText(_translate("HgOptionsDialog", "Commit &Message:"))
        self.vcsLogEdit.setToolTip(_translate("HgOptionsDialog", "Enter the log message for the new project."))
        self.vcsLogEdit.setWhatsThis(_translate("HgOptionsDialog", "<b>Log Message</b>\n"
"<p>Enter the log message to be used for the new project.</p>"))
        self.vcsLogEdit.setText(_translate("HgOptionsDialog", "new project started"))
