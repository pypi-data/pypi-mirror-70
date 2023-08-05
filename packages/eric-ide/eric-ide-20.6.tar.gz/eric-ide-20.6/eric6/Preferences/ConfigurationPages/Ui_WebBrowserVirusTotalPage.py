# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/WebBrowserVirusTotalPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WebBrowserVirusTotalPage(object):
    def setupUi(self, WebBrowserVirusTotalPage):
        WebBrowserVirusTotalPage.setObjectName("WebBrowserVirusTotalPage")
        WebBrowserVirusTotalPage.resize(485, 409)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WebBrowserVirusTotalPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerLabel = QtWidgets.QLabel(WebBrowserVirusTotalPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_2.addWidget(self.headerLabel)
        self.line17 = QtWidgets.QFrame(WebBrowserVirusTotalPage)
        self.line17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line17.setObjectName("line17")
        self.verticalLayout_2.addWidget(self.line17)
        self.vtEnabledCheckBox = QtWidgets.QCheckBox(WebBrowserVirusTotalPage)
        self.vtEnabledCheckBox.setObjectName("vtEnabledCheckBox")
        self.verticalLayout_2.addWidget(self.vtEnabledCheckBox)
        self.groupBox = QtWidgets.QGroupBox(WebBrowserVirusTotalPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.vtServiceKeyEdit = QtWidgets.QLineEdit(self.groupBox)
        self.vtServiceKeyEdit.setObjectName("vtServiceKeyEdit")
        self.verticalLayout.addWidget(self.vtServiceKeyEdit)
        self.testResultLabel = QtWidgets.QLabel(self.groupBox)
        self.testResultLabel.setText("")
        self.testResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.testResultLabel.setWordWrap(True)
        self.testResultLabel.setObjectName("testResultLabel")
        self.verticalLayout.addWidget(self.testResultLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.testButton = QtWidgets.QPushButton(self.groupBox)
        self.testButton.setEnabled(False)
        self.testButton.setObjectName("testButton")
        self.horizontalLayout.addWidget(self.testButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.vtSecureCheckBox = QtWidgets.QCheckBox(WebBrowserVirusTotalPage)
        self.vtSecureCheckBox.setObjectName("vtSecureCheckBox")
        self.verticalLayout_2.addWidget(self.vtSecureCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 74, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)

        self.retranslateUi(WebBrowserVirusTotalPage)
        QtCore.QMetaObject.connectSlotsByName(WebBrowserVirusTotalPage)
        WebBrowserVirusTotalPage.setTabOrder(self.vtEnabledCheckBox, self.vtServiceKeyEdit)
        WebBrowserVirusTotalPage.setTabOrder(self.vtServiceKeyEdit, self.testButton)
        WebBrowserVirusTotalPage.setTabOrder(self.testButton, self.vtSecureCheckBox)

    def retranslateUi(self, WebBrowserVirusTotalPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("WebBrowserVirusTotalPage", "<b>Configure VirusTotal Interface</b>"))
        self.vtEnabledCheckBox.setToolTip(_translate("WebBrowserVirusTotalPage", "Select to enable the VirusTotal interface"))
        self.vtEnabledCheckBox.setText(_translate("WebBrowserVirusTotalPage", "Enable VirusTotal"))
        self.groupBox.setTitle(_translate("WebBrowserVirusTotalPage", "Service Key"))
        self.label.setText(_translate("WebBrowserVirusTotalPage", "Enter your personal VirusTotal service key (s. <a href=\"http://virustotal.com\">VirusTotal &copy;</a> for details):"))
        self.vtServiceKeyEdit.setToolTip(_translate("WebBrowserVirusTotalPage", "Enter the VirusTotal service key"))
        self.testButton.setToolTip(_translate("WebBrowserVirusTotalPage", "Press to test the validity of the service key"))
        self.testButton.setText(_translate("WebBrowserVirusTotalPage", "Test Service Key"))
        self.vtSecureCheckBox.setToolTip(_translate("WebBrowserVirusTotalPage", "Select to use a secure (https) connection"))
        self.vtSecureCheckBox.setText(_translate("WebBrowserVirusTotalPage", "Use secure (https) connections"))
