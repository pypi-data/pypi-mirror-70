# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/EditorGeneralPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorGeneralPage(object):
    def setupUi(self, EditorGeneralPage):
        EditorGeneralPage.setObjectName("EditorGeneralPage")
        EditorGeneralPage.resize(559, 771)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(EditorGeneralPage)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.headerLabel = QtWidgets.QLabel(EditorGeneralPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_4.addWidget(self.headerLabel)
        self.line2 = QtWidgets.QFrame(EditorGeneralPage)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setObjectName("line2")
        self.verticalLayout_4.addWidget(self.line2)
        self.groupBox_5 = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.TextLabel13_3 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel13_3.setObjectName("TextLabel13_3")
        self.gridlayout.addWidget(self.TextLabel13_3, 0, 0, 1, 1)
        self.tabwidthSlider = QtWidgets.QSlider(self.groupBox_5)
        self.tabwidthSlider.setMinimum(1)
        self.tabwidthSlider.setMaximum(20)
        self.tabwidthSlider.setProperty("value", 4)
        self.tabwidthSlider.setOrientation(QtCore.Qt.Horizontal)
        self.tabwidthSlider.setTickInterval(1)
        self.tabwidthSlider.setObjectName("tabwidthSlider")
        self.gridlayout.addWidget(self.tabwidthSlider, 0, 1, 1, 1)
        self.tabwidthLCD = QtWidgets.QLCDNumber(self.groupBox_5)
        self.tabwidthLCD.setDigitCount(2)
        self.tabwidthLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.tabwidthLCD.setProperty("value", 4.0)
        self.tabwidthLCD.setObjectName("tabwidthLCD")
        self.gridlayout.addWidget(self.tabwidthLCD, 0, 2, 1, 1)
        self.TextLabel13_2_3 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel13_2_3.setObjectName("TextLabel13_2_3")
        self.gridlayout.addWidget(self.TextLabel13_2_3, 1, 0, 1, 1)
        self.indentwidthSlider = QtWidgets.QSlider(self.groupBox_5)
        self.indentwidthSlider.setMinimum(1)
        self.indentwidthSlider.setMaximum(20)
        self.indentwidthSlider.setProperty("value", 4)
        self.indentwidthSlider.setOrientation(QtCore.Qt.Horizontal)
        self.indentwidthSlider.setTickInterval(1)
        self.indentwidthSlider.setObjectName("indentwidthSlider")
        self.gridlayout.addWidget(self.indentwidthSlider, 1, 1, 1, 1)
        self.indentwidthLCD = QtWidgets.QLCDNumber(self.groupBox_5)
        self.indentwidthLCD.setDigitCount(2)
        self.indentwidthLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.indentwidthLCD.setProperty("value", 4.0)
        self.indentwidthLCD.setObjectName("indentwidthLCD")
        self.gridlayout.addWidget(self.indentwidthLCD, 1, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridlayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.languageOverrideWidget = QtWidgets.QTreeWidget(self.groupBox_5)
        self.languageOverrideWidget.setAlternatingRowColors(True)
        self.languageOverrideWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.languageOverrideWidget.setRootIsDecorated(False)
        self.languageOverrideWidget.setItemsExpandable(False)
        self.languageOverrideWidget.setObjectName("languageOverrideWidget")
        self.languageOverrideWidget.headerItem().setText(3, " ")
        self.horizontalLayout.addWidget(self.languageOverrideWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.addButton = QtWidgets.QToolButton(self.groupBox_5)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_2.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QToolButton(self.groupBox_5)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout_2.addWidget(self.deleteButton)
        self.editButton = QtWidgets.QToolButton(self.groupBox_5)
        self.editButton.setObjectName("editButton")
        self.verticalLayout_2.addWidget(self.editButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.autoindentCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.autoindentCheckBox.setObjectName("autoindentCheckBox")
        self.gridLayout_2.addWidget(self.autoindentCheckBox, 0, 0, 1, 1)
        self.tabforindentationCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.tabforindentationCheckBox.setObjectName("tabforindentationCheckBox")
        self.gridLayout_2.addWidget(self.tabforindentationCheckBox, 0, 1, 1, 1)
        self.tabindentsCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.tabindentsCheckBox.setObjectName("tabindentsCheckBox")
        self.gridLayout_2.addWidget(self.tabindentsCheckBox, 1, 0, 1, 1)
        self.converttabsCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.converttabsCheckBox.setObjectName("converttabsCheckBox")
        self.gridLayout_2.addWidget(self.converttabsCheckBox, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.comment0CheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.comment0CheckBox.setObjectName("comment0CheckBox")
        self.gridLayout.addWidget(self.comment0CheckBox, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(EditorGeneralPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.vsSelectionCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.vsSelectionCheckBox.setObjectName("vsSelectionCheckBox")
        self.verticalLayout.addWidget(self.vsSelectionCheckBox)
        self.vsUserCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.vsUserCheckBox.setObjectName("vsUserCheckBox")
        self.verticalLayout.addWidget(self.vsUserCheckBox)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        spacerItem2 = QtWidgets.QSpacerItem(535, 101, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.TextLabel13_3.setBuddy(self.tabwidthSlider)
        self.TextLabel13_2_3.setBuddy(self.indentwidthSlider)

        self.retranslateUi(EditorGeneralPage)
        self.tabwidthSlider.valueChanged['int'].connect(self.tabwidthLCD.display)
        self.indentwidthSlider.valueChanged['int'].connect(self.indentwidthLCD.display)
        QtCore.QMetaObject.connectSlotsByName(EditorGeneralPage)
        EditorGeneralPage.setTabOrder(self.tabwidthSlider, self.indentwidthSlider)
        EditorGeneralPage.setTabOrder(self.indentwidthSlider, self.languageOverrideWidget)
        EditorGeneralPage.setTabOrder(self.languageOverrideWidget, self.addButton)
        EditorGeneralPage.setTabOrder(self.addButton, self.deleteButton)
        EditorGeneralPage.setTabOrder(self.deleteButton, self.editButton)
        EditorGeneralPage.setTabOrder(self.editButton, self.autoindentCheckBox)
        EditorGeneralPage.setTabOrder(self.autoindentCheckBox, self.tabforindentationCheckBox)
        EditorGeneralPage.setTabOrder(self.tabforindentationCheckBox, self.tabindentsCheckBox)
        EditorGeneralPage.setTabOrder(self.tabindentsCheckBox, self.converttabsCheckBox)
        EditorGeneralPage.setTabOrder(self.converttabsCheckBox, self.comment0CheckBox)
        EditorGeneralPage.setTabOrder(self.comment0CheckBox, self.vsSelectionCheckBox)
        EditorGeneralPage.setTabOrder(self.vsSelectionCheckBox, self.vsUserCheckBox)

    def retranslateUi(self, EditorGeneralPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorGeneralPage", "<b>Configure general editor settings</b>"))
        self.groupBox_5.setTitle(_translate("EditorGeneralPage", "Tabs && Indentation"))
        self.TextLabel13_3.setText(_translate("EditorGeneralPage", "Tab width:"))
        self.tabwidthSlider.setToolTip(_translate("EditorGeneralPage", "Move to set the tab width."))
        self.tabwidthLCD.setToolTip(_translate("EditorGeneralPage", "Displays the selected tab width."))
        self.TextLabel13_2_3.setText(_translate("EditorGeneralPage", "Indentation width:"))
        self.indentwidthSlider.setToolTip(_translate("EditorGeneralPage", "Move to set the indentation width."))
        self.indentwidthLCD.setToolTip(_translate("EditorGeneralPage", "Displays the selected indentation width."))
        self.languageOverrideWidget.headerItem().setText(0, _translate("EditorGeneralPage", "Language"))
        self.languageOverrideWidget.headerItem().setText(1, _translate("EditorGeneralPage", "Tab Width"))
        self.languageOverrideWidget.headerItem().setText(2, _translate("EditorGeneralPage", "Indent Width"))
        self.addButton.setToolTip(_translate("EditorGeneralPage", "Press to add a language specific override"))
        self.deleteButton.setToolTip(_translate("EditorGeneralPage", "Press to delete the selected language specific override"))
        self.editButton.setToolTip(_translate("EditorGeneralPage", "Press to edit the selected language specific override"))
        self.autoindentCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether autoindentation shall be enabled"))
        self.autoindentCheckBox.setText(_translate("EditorGeneralPage", "Auto indentation"))
        self.tabforindentationCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether tab characters are used for indentations."))
        self.tabforindentationCheckBox.setText(_translate("EditorGeneralPage", "Use tabs for indentations"))
        self.tabindentsCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether pressing the tab key indents."))
        self.tabindentsCheckBox.setText(_translate("EditorGeneralPage", "Tab key indents"))
        self.converttabsCheckBox.setToolTip(_translate("EditorGeneralPage", "Select whether tabs shall be converted upon opening the file"))
        self.converttabsCheckBox.setText(_translate("EditorGeneralPage", "Convert tabs upon open"))
        self.groupBox.setTitle(_translate("EditorGeneralPage", "Comments"))
        self.comment0CheckBox.setToolTip(_translate("EditorGeneralPage", "Select to insert the comment sign at column 0"))
        self.comment0CheckBox.setWhatsThis(_translate("EditorGeneralPage", "<b>Insert comment at column 0</b><p>Select to insert the comment sign at column 0. Otherwise, the comment sign is inserted at the first non-whitespace position.</p>"))
        self.comment0CheckBox.setText(_translate("EditorGeneralPage", "Insert comment at column 0"))
        self.groupBox_2.setTitle(_translate("EditorGeneralPage", "Virtual Space"))
        self.label.setText(_translate("EditorGeneralPage", "Virtual space is the space after the last character of a line. It is not allocated unless some text is entered or copied into it. Usage of virtual space can be configured with these selections."))
        self.vsSelectionCheckBox.setToolTip(_translate("EditorGeneralPage", "Select to enable a rectangular selection to extend into virtual space"))
        self.vsSelectionCheckBox.setText(_translate("EditorGeneralPage", "Selection may access virtual space"))
        self.vsUserCheckBox.setToolTip(_translate("EditorGeneralPage", "Select to allow the cursor to be moved into virtual space"))
        self.vsUserCheckBox.setText(_translate("EditorGeneralPage", "Cursor can move into virtual space"))
