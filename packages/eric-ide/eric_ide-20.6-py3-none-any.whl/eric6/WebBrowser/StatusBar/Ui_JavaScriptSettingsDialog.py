# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/WebBrowser/StatusBar/JavaScriptSettingsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_JavaScriptSettingsDialog(object):
    def setupUi(self, JavaScriptSettingsDialog):
        JavaScriptSettingsDialog.setObjectName("JavaScriptSettingsDialog")
        JavaScriptSettingsDialog.resize(400, 209)
        JavaScriptSettingsDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(JavaScriptSettingsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.javaScriptGroup = QtWidgets.QGroupBox(JavaScriptSettingsDialog)
        self.javaScriptGroup.setCheckable(True)
        self.javaScriptGroup.setObjectName("javaScriptGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.javaScriptGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.jsOpenWindowsCheckBox = QtWidgets.QCheckBox(self.javaScriptGroup)
        self.jsOpenWindowsCheckBox.setObjectName("jsOpenWindowsCheckBox")
        self.verticalLayout.addWidget(self.jsOpenWindowsCheckBox)
        self.jsActivateWindowsCheckBox = QtWidgets.QCheckBox(self.javaScriptGroup)
        self.jsActivateWindowsCheckBox.setObjectName("jsActivateWindowsCheckBox")
        self.verticalLayout.addWidget(self.jsActivateWindowsCheckBox)
        self.jsClipboardCheckBox = QtWidgets.QCheckBox(self.javaScriptGroup)
        self.jsClipboardCheckBox.setObjectName("jsClipboardCheckBox")
        self.verticalLayout.addWidget(self.jsClipboardCheckBox)
        self.jsPasteCheckBox = QtWidgets.QCheckBox(self.javaScriptGroup)
        self.jsPasteCheckBox.setObjectName("jsPasteCheckBox")
        self.verticalLayout.addWidget(self.jsPasteCheckBox)
        self.verticalLayout_2.addWidget(self.javaScriptGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(JavaScriptSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(JavaScriptSettingsDialog)
        self.buttonBox.accepted.connect(JavaScriptSettingsDialog.accept)
        self.buttonBox.rejected.connect(JavaScriptSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(JavaScriptSettingsDialog)

    def retranslateUi(self, JavaScriptSettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        JavaScriptSettingsDialog.setWindowTitle(_translate("JavaScriptSettingsDialog", "JavaScript Settings"))
        self.javaScriptGroup.setToolTip(_translate("JavaScriptSettingsDialog", "Select to enable JavaScript support"))
        self.javaScriptGroup.setTitle(_translate("JavaScriptSettingsDialog", "Enable JavaScript"))
        self.jsOpenWindowsCheckBox.setToolTip(_translate("JavaScriptSettingsDialog", "Select to allow JavaScript to open windows"))
        self.jsOpenWindowsCheckBox.setText(_translate("JavaScriptSettingsDialog", "Allow to open windows"))
        self.jsActivateWindowsCheckBox.setToolTip(_translate("JavaScriptSettingsDialog", "Select to allow JavaScript to activate windows"))
        self.jsActivateWindowsCheckBox.setText(_translate("JavaScriptSettingsDialog", "Allow to activate windows"))
        self.jsClipboardCheckBox.setToolTip(_translate("JavaScriptSettingsDialog", "Select to allow JavaScript to access the clipboard"))
        self.jsClipboardCheckBox.setText(_translate("JavaScriptSettingsDialog", "Allow to access the clipboard"))
        self.jsPasteCheckBox.setToolTip(_translate("JavaScriptSettingsDialog", "Select to allow JavaScript to paste from the clipboard (this needs access to the clipboard)"))
        self.jsPasteCheckBox.setText(_translate("JavaScriptSettingsDialog", "Allow to paste from the clipboard"))
