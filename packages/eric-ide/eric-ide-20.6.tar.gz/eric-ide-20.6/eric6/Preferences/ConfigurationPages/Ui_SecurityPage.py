# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/SecurityPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SecurityPage(object):
    def setupUi(self, SecurityPage):
        SecurityPage.setObjectName("SecurityPage")
        SecurityPage.resize(400, 434)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SecurityPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerLabel = QtWidgets.QLabel(SecurityPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.line1 = QtWidgets.QFrame(SecurityPage)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setObjectName("line1")
        self.verticalLayout_3.addWidget(self.line1)
        self.groupBox = QtWidgets.QGroupBox(SecurityPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.savePasswordsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.savePasswordsCheckBox.setObjectName("savePasswordsCheckBox")
        self.verticalLayout.addWidget(self.savePasswordsCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.masterPasswordCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.masterPasswordCheckBox.setObjectName("masterPasswordCheckBox")
        self.horizontalLayout.addWidget(self.masterPasswordCheckBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.masterPasswordButton = QtWidgets.QPushButton(self.groupBox)
        self.masterPasswordButton.setEnabled(False)
        self.masterPasswordButton.setObjectName("masterPasswordButton")
        self.horizontalLayout.addWidget(self.masterPasswordButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.certificateErrorsGroup = QtWidgets.QGroupBox(SecurityPage)
        self.certificateErrorsGroup.setObjectName("certificateErrorsGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.certificateErrorsGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.alwaysRejectCheckBox = QtWidgets.QCheckBox(self.certificateErrorsGroup)
        self.alwaysRejectCheckBox.setObjectName("alwaysRejectCheckBox")
        self.verticalLayout_2.addWidget(self.alwaysRejectCheckBox)
        self.verticalLayout_3.addWidget(self.certificateErrorsGroup)
        spacerItem1 = QtWidgets.QSpacerItem(20, 113, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.retranslateUi(SecurityPage)
        QtCore.QMetaObject.connectSlotsByName(SecurityPage)
        SecurityPage.setTabOrder(self.savePasswordsCheckBox, self.masterPasswordCheckBox)
        SecurityPage.setTabOrder(self.masterPasswordCheckBox, self.masterPasswordButton)

    def retranslateUi(self, SecurityPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("SecurityPage", "<b>Configure security settings</b>"))
        self.groupBox.setTitle(_translate("SecurityPage", "Passwords"))
        self.savePasswordsCheckBox.setToolTip(_translate("SecurityPage", "Select to save passwords"))
        self.savePasswordsCheckBox.setText(_translate("SecurityPage", "Save passwords"))
        self.masterPasswordCheckBox.setToolTip(_translate("SecurityPage", "Select to use a master password"))
        self.masterPasswordCheckBox.setText(_translate("SecurityPage", "Use Master Password"))
        self.masterPasswordButton.setToolTip(_translate("SecurityPage", "Press to change the master password"))
        self.masterPasswordButton.setText(_translate("SecurityPage", "Change Master Password..."))
        self.certificateErrorsGroup.setTitle(_translate("SecurityPage", "Certificate Errors"))
        self.alwaysRejectCheckBox.setToolTip(_translate("SecurityPage", "Select to always reject web pages with certificate issues"))
        self.alwaysRejectCheckBox.setText(_translate("SecurityPage", "Always reject URLs with certificate errors"))
