# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/MicroPythonPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MicroPythonPage(object):
    def setupUi(self, MicroPythonPage):
        MicroPythonPage.setObjectName("MicroPythonPage")
        MicroPythonPage.resize(476, 869)
        self.verticalLayout = QtWidgets.QVBoxLayout(MicroPythonPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(MicroPythonPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line9_3 = QtWidgets.QFrame(MicroPythonPage)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setObjectName("line9_3")
        self.verticalLayout.addWidget(self.line9_3)
        self.groupBox_2 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.timeoutSpinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.timeoutSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeoutSpinBox.setMinimum(1)
        self.timeoutSpinBox.setMaximum(30)
        self.timeoutSpinBox.setObjectName("timeoutSpinBox")
        self.gridLayout_2.addWidget(self.timeoutSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(195, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.syncTimeCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncTimeCheckBox.sizePolicy().hasHeightForWidth())
        self.syncTimeCheckBox.setSizePolicy(sizePolicy)
        self.syncTimeCheckBox.setObjectName("syncTimeCheckBox")
        self.gridLayout_2.addWidget(self.syncTimeCheckBox, 1, 0, 1, 3)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.colorSchemeComboBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorSchemeComboBox.sizePolicy().hasHeightForWidth())
        self.colorSchemeComboBox.setSizePolicy(sizePolicy)
        self.colorSchemeComboBox.setObjectName("colorSchemeComboBox")
        self.gridLayout.addWidget(self.colorSchemeComboBox, 0, 1, 1, 1)
        self.replWrapCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.replWrapCheckBox.setObjectName("replWrapCheckBox")
        self.gridLayout.addWidget(self.replWrapCheckBox, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_7 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self.groupBox_7)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.chartThemeComboBox = QtWidgets.QComboBox(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartThemeComboBox.sizePolicy().hasHeightForWidth())
        self.chartThemeComboBox.setSizePolicy(sizePolicy)
        self.chartThemeComboBox.setObjectName("chartThemeComboBox")
        self.horizontalLayout_3.addWidget(self.chartThemeComboBox)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.groupBox_3 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.mpyCrossPicker = E5PathPicker(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpyCrossPicker.sizePolicy().hasHeightForWidth())
        self.mpyCrossPicker.setSizePolicy(sizePolicy)
        self.mpyCrossPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.mpyCrossPicker.setObjectName("mpyCrossPicker")
        self.horizontalLayout.addWidget(self.mpyCrossPicker)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.dfuUtilPathPicker = E5PathPicker(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dfuUtilPathPicker.sizePolicy().hasHeightForWidth())
        self.dfuUtilPathPicker.setSizePolicy(sizePolicy)
        self.dfuUtilPathPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.dfuUtilPathPicker.setObjectName("dfuUtilPathPicker")
        self.horizontalLayout_2.addWidget(self.dfuUtilPathPicker)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)
        self.micropythonFirmwareUrlLineEdit = E5ClearableLineEdit(self.groupBox_6)
        self.micropythonFirmwareUrlLineEdit.setObjectName("micropythonFirmwareUrlLineEdit")
        self.gridLayout_4.addWidget(self.micropythonFirmwareUrlLineEdit, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)
        self.circuitpythonFirmwareUrlLineEdit = E5ClearableLineEdit(self.groupBox_6)
        self.circuitpythonFirmwareUrlLineEdit.setObjectName("circuitpythonFirmwareUrlLineEdit")
        self.gridLayout_4.addWidget(self.circuitpythonFirmwareUrlLineEdit, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_6)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)
        self.microbitFirmwareUrlLineEdit = E5ClearableLineEdit(self.groupBox_6)
        self.microbitFirmwareUrlLineEdit.setObjectName("microbitFirmwareUrlLineEdit")
        self.gridLayout_4.addWidget(self.microbitFirmwareUrlLineEdit, 2, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 3, 0, 1, 1)
        self.calliopeFirmwareUrlLineEdit = E5ClearableLineEdit(self.groupBox_6)
        self.calliopeFirmwareUrlLineEdit.setObjectName("calliopeFirmwareUrlLineEdit")
        self.gridLayout_4.addWidget(self.calliopeFirmwareUrlLineEdit, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.groupBox_4 = QtWidgets.QGroupBox(MicroPythonPage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.micropythonDocuUrlLineEdit = E5ClearableLineEdit(self.groupBox_4)
        self.micropythonDocuUrlLineEdit.setObjectName("micropythonDocuUrlLineEdit")
        self.gridLayout_3.addWidget(self.micropythonDocuUrlLineEdit, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.circuitpythonDocuUrlLineEdit = E5ClearableLineEdit(self.groupBox_4)
        self.circuitpythonDocuUrlLineEdit.setObjectName("circuitpythonDocuUrlLineEdit")
        self.gridLayout_3.addWidget(self.circuitpythonDocuUrlLineEdit, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.microbitDocuUrlLineEdit = E5ClearableLineEdit(self.groupBox_4)
        self.microbitDocuUrlLineEdit.setObjectName("microbitDocuUrlLineEdit")
        self.gridLayout_3.addWidget(self.microbitDocuUrlLineEdit, 2, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 3, 0, 1, 1)
        self.calliopeDocuUrlLineEdit = E5ClearableLineEdit(self.groupBox_4)
        self.calliopeDocuUrlLineEdit.setObjectName("calliopeDocuUrlLineEdit")
        self.gridLayout_3.addWidget(self.calliopeDocuUrlLineEdit, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 252, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(MicroPythonPage)
        QtCore.QMetaObject.connectSlotsByName(MicroPythonPage)
        MicroPythonPage.setTabOrder(self.timeoutSpinBox, self.syncTimeCheckBox)
        MicroPythonPage.setTabOrder(self.syncTimeCheckBox, self.colorSchemeComboBox)
        MicroPythonPage.setTabOrder(self.colorSchemeComboBox, self.replWrapCheckBox)
        MicroPythonPage.setTabOrder(self.replWrapCheckBox, self.chartThemeComboBox)
        MicroPythonPage.setTabOrder(self.chartThemeComboBox, self.mpyCrossPicker)
        MicroPythonPage.setTabOrder(self.mpyCrossPicker, self.dfuUtilPathPicker)
        MicroPythonPage.setTabOrder(self.dfuUtilPathPicker, self.micropythonFirmwareUrlLineEdit)
        MicroPythonPage.setTabOrder(self.micropythonFirmwareUrlLineEdit, self.circuitpythonFirmwareUrlLineEdit)
        MicroPythonPage.setTabOrder(self.circuitpythonFirmwareUrlLineEdit, self.microbitFirmwareUrlLineEdit)
        MicroPythonPage.setTabOrder(self.microbitFirmwareUrlLineEdit, self.calliopeFirmwareUrlLineEdit)
        MicroPythonPage.setTabOrder(self.calliopeFirmwareUrlLineEdit, self.micropythonDocuUrlLineEdit)
        MicroPythonPage.setTabOrder(self.micropythonDocuUrlLineEdit, self.circuitpythonDocuUrlLineEdit)
        MicroPythonPage.setTabOrder(self.circuitpythonDocuUrlLineEdit, self.microbitDocuUrlLineEdit)
        MicroPythonPage.setTabOrder(self.microbitDocuUrlLineEdit, self.calliopeDocuUrlLineEdit)

    def retranslateUi(self, MicroPythonPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("MicroPythonPage", "<b>Configure MicroPython</b>"))
        self.groupBox_2.setTitle(_translate("MicroPythonPage", "Serial Link"))
        self.label_2.setText(_translate("MicroPythonPage", "Timeout for Serial Link Communication:"))
        self.timeoutSpinBox.setToolTip(_translate("MicroPythonPage", "Enter the timout value"))
        self.timeoutSpinBox.setSuffix(_translate("MicroPythonPage", " s"))
        self.syncTimeCheckBox.setToolTip(_translate("MicroPythonPage", "Select to synchronize the time after connection is established"))
        self.syncTimeCheckBox.setText(_translate("MicroPythonPage", "Synchronize Time at Connect"))
        self.groupBox.setTitle(_translate("MicroPythonPage", "REPL Pane"))
        self.label.setText(_translate("MicroPythonPage", "Color Scheme for ANSI Escape Codes:"))
        self.colorSchemeComboBox.setToolTip(_translate("MicroPythonPage", "Select the color scheme to be applied for ANSI color escape codes"))
        self.replWrapCheckBox.setToolTip(_translate("MicroPythonPage", "Select to wrap long line in the REPL pane"))
        self.replWrapCheckBox.setText(_translate("MicroPythonPage", "Wrap long lines"))
        self.groupBox_7.setTitle(_translate("MicroPythonPage", "Chart Pane"))
        self.label_11.setText(_translate("MicroPythonPage", "Color Theme:"))
        self.chartThemeComboBox.setToolTip(_translate("MicroPythonPage", "Select the color scheme of the chart"))
        self.groupBox_3.setTitle(_translate("MicroPythonPage", "MPY Cross Compiler"))
        self.label_3.setText(_translate("MicroPythonPage", "Program:"))
        self.mpyCrossPicker.setToolTip(_translate("MicroPythonPage", "Enter the path of the cross compiler executable"))
        self.groupBox_5.setTitle(_translate("MicroPythonPage", "PyBoard"))
        self.label_7.setText(_translate("MicroPythonPage", "dfu-util Path:"))
        self.dfuUtilPathPicker.setToolTip(_translate("MicroPythonPage", "Enter the path of the dfu-util flashing executable"))
        self.groupBox_6.setTitle(_translate("MicroPythonPage", "Firmware"))
        self.label_8.setText(_translate("MicroPythonPage", "MicroPython:"))
        self.micropythonFirmwareUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the MicroPython firmware for PyBoard, ESP8266 and ESP32"))
        self.label_10.setText(_translate("MicroPythonPage", "CircuitPython:"))
        self.circuitpythonFirmwareUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the CircuitPython firmware"))
        self.label_9.setText(_translate("MicroPythonPage", "BBC micro:bit:"))
        self.microbitFirmwareUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the BBC micro:bit Firmware"))
        self.label_13.setText(_translate("MicroPythonPage", "Calliope mini:"))
        self.calliopeFirmwareUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the Callope mini Firmware"))
        self.groupBox_4.setTitle(_translate("MicroPythonPage", "Documentation"))
        self.label_4.setText(_translate("MicroPythonPage", "MicroPython:"))
        self.micropythonDocuUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the MicroPython documentation"))
        self.label_5.setText(_translate("MicroPythonPage", "CircuitPython:"))
        self.circuitpythonDocuUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the CircuitPython documentation"))
        self.label_6.setText(_translate("MicroPythonPage", "BBC micro:bit:"))
        self.microbitDocuUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the BBC micro:bit MicroPython documentation"))
        self.label_12.setText(_translate("MicroPythonPage", "Calliope mini:"))
        self.calliopeDocuUrlLineEdit.setToolTip(_translate("MicroPythonPage", "Enter the URL for the Calliope mini MicroPython documentation"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
from E5Gui.E5PathPicker import E5PathPicker
