# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/EditorAutocompletionPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorAutocompletionPage(object):
    def setupUi(self, EditorAutocompletionPage):
        EditorAutocompletionPage.setObjectName("EditorAutocompletionPage")
        EditorAutocompletionPage.resize(506, 498)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditorAutocompletionPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(EditorAutocompletionPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line6 = QtWidgets.QFrame(EditorAutocompletionPage)
        self.line6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line6.setObjectName("line6")
        self.verticalLayout.addWidget(self.line6)
        self.groupBox = QtWidgets.QGroupBox(EditorAutocompletionPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setVerticalSpacing(9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.acReplaceWordCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.acReplaceWordCheckBox.setObjectName("acReplaceWordCheckBox")
        self.gridLayout_2.addWidget(self.acReplaceWordCheckBox, 0, 1, 1, 1)
        self.acCaseSensitivityCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.acCaseSensitivityCheckBox.setObjectName("acCaseSensitivityCheckBox")
        self.gridLayout_2.addWidget(self.acCaseSensitivityCheckBox, 0, 0, 1, 1)
        self.acReversedCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.acReversedCheckBox.setObjectName("acReversedCheckBox")
        self.gridLayout_2.addWidget(self.acReversedCheckBox, 1, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setSpacing(9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.acLinesSlider = QtWidgets.QSlider(self.groupBox)
        self.acLinesSlider.setMinimum(1)
        self.acLinesSlider.setMaximum(20)
        self.acLinesSlider.setPageStep(2)
        self.acLinesSlider.setProperty("value", 6)
        self.acLinesSlider.setOrientation(QtCore.Qt.Horizontal)
        self.acLinesSlider.setObjectName("acLinesSlider")
        self.gridLayout_3.addWidget(self.acLinesSlider, 0, 1, 1, 1)
        self.lcdNumber = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber.setDigitCount(3)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 6)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout_3.addWidget(self.lcdNumber, 0, 2, 1, 1)
        self.acCharSlider = QtWidgets.QSlider(self.groupBox)
        self.acCharSlider.setMinimum(10)
        self.acCharSlider.setMaximum(100)
        self.acCharSlider.setProperty("value", 40)
        self.acCharSlider.setOrientation(QtCore.Qt.Horizontal)
        self.acCharSlider.setObjectName("acCharSlider")
        self.gridLayout_3.addWidget(self.acCharSlider, 1, 1, 1, 1)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.groupBox)
        self.lcdNumber_2.setDigitCount(3)
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("intValue", 40)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.gridLayout_3.addWidget(self.lcdNumber_2, 1, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.acEnabledGroupBox = QtWidgets.QGroupBox(EditorAutocompletionPage)
        self.acEnabledGroupBox.setCheckable(True)
        self.acEnabledGroupBox.setObjectName("acEnabledGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.acEnabledGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textLabel1_2 = QtWidgets.QLabel(self.acEnabledGroupBox)
        self.textLabel1_2.setObjectName("textLabel1_2")
        self.gridLayout_4.addWidget(self.textLabel1_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.acEnabledGroupBox)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.acThresholdSlider = QtWidgets.QSlider(self.acEnabledGroupBox)
        self.acThresholdSlider.setMaximum(10)
        self.acThresholdSlider.setProperty("value", 2)
        self.acThresholdSlider.setOrientation(QtCore.Qt.Horizontal)
        self.acThresholdSlider.setTickInterval(1)
        self.acThresholdSlider.setObjectName("acThresholdSlider")
        self.horizontalLayout.addWidget(self.acThresholdSlider)
        self.lCDNumber4 = QtWidgets.QLCDNumber(self.acEnabledGroupBox)
        self.lCDNumber4.setDigitCount(3)
        self.lCDNumber4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lCDNumber4.setProperty("value", 2.0)
        self.lCDNumber4.setObjectName("lCDNumber4")
        self.horizontalLayout.addWidget(self.lCDNumber4)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.acTimeoutSpinBox = QtWidgets.QSpinBox(self.acEnabledGroupBox)
        self.acTimeoutSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.acTimeoutSpinBox.setMaximumSize(QtCore.QSize(70, 16777215))
        self.acTimeoutSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.acTimeoutSpinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.acTimeoutSpinBox.setMinimum(0)
        self.acTimeoutSpinBox.setMaximum(1000)
        self.acTimeoutSpinBox.setSingleStep(50)
        self.acTimeoutSpinBox.setObjectName("acTimeoutSpinBox")
        self.gridLayout_4.addWidget(self.acTimeoutSpinBox, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.acEnabledGroupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(EditorAutocompletionPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.acScintillaCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.acScintillaCheckBox.setObjectName("acScintillaCheckBox")
        self.verticalLayout_2.addWidget(self.acScintillaCheckBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.acWatchdogDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.acWatchdogDoubleSpinBox.setEnabled(False)
        self.acWatchdogDoubleSpinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.acWatchdogDoubleSpinBox.setMaximumSize(QtCore.QSize(70, 16777215))
        self.acWatchdogDoubleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.acWatchdogDoubleSpinBox.setAccelerated(True)
        self.acWatchdogDoubleSpinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.acWatchdogDoubleSpinBox.setDecimals(1)
        self.acWatchdogDoubleSpinBox.setMaximum(10.0)
        self.acWatchdogDoubleSpinBox.setSingleStep(0.5)
        self.acWatchdogDoubleSpinBox.setObjectName("acWatchdogDoubleSpinBox")
        self.horizontalLayout_2.addWidget(self.acWatchdogDoubleSpinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.acCacheGroup = QtWidgets.QGroupBox(EditorAutocompletionPage)
        self.acCacheGroup.setCheckable(True)
        self.acCacheGroup.setObjectName("acCacheGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.acCacheGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.acCacheGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.acCacheSizeSpinBox = QtWidgets.QSpinBox(self.acCacheGroup)
        self.acCacheSizeSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.acCacheSizeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.acCacheSizeSpinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.acCacheSizeSpinBox.setMinimum(0)
        self.acCacheSizeSpinBox.setMaximum(1000)
        self.acCacheSizeSpinBox.setSingleStep(10)
        self.acCacheSizeSpinBox.setObjectName("acCacheSizeSpinBox")
        self.gridLayout.addWidget(self.acCacheSizeSpinBox, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(271, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.acCacheGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.acCacheTimeSpinBox = QtWidgets.QSpinBox(self.acCacheGroup)
        self.acCacheTimeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.acCacheTimeSpinBox.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.acCacheTimeSpinBox.setMinimum(0)
        self.acCacheTimeSpinBox.setMaximum(3600)
        self.acCacheTimeSpinBox.setSingleStep(60)
        self.acCacheTimeSpinBox.setObjectName("acCacheTimeSpinBox")
        self.gridLayout.addWidget(self.acCacheTimeSpinBox, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.acCacheGroup)
        spacerItem2 = QtWidgets.QSpacerItem(456, 51, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(EditorAutocompletionPage)
        self.acThresholdSlider.valueChanged['int'].connect(self.lCDNumber4.display)
        self.acScintillaCheckBox.toggled['bool'].connect(self.acWatchdogDoubleSpinBox.setEnabled)
        self.acLinesSlider.valueChanged['int'].connect(self.lcdNumber.display)
        self.acCharSlider.valueChanged['int'].connect(self.lcdNumber_2.display)
        QtCore.QMetaObject.connectSlotsByName(EditorAutocompletionPage)
        EditorAutocompletionPage.setTabOrder(self.acCaseSensitivityCheckBox, self.acReplaceWordCheckBox)
        EditorAutocompletionPage.setTabOrder(self.acReplaceWordCheckBox, self.acReversedCheckBox)
        EditorAutocompletionPage.setTabOrder(self.acReversedCheckBox, self.acLinesSlider)
        EditorAutocompletionPage.setTabOrder(self.acLinesSlider, self.acCharSlider)
        EditorAutocompletionPage.setTabOrder(self.acCharSlider, self.acEnabledGroupBox)
        EditorAutocompletionPage.setTabOrder(self.acEnabledGroupBox, self.acThresholdSlider)
        EditorAutocompletionPage.setTabOrder(self.acThresholdSlider, self.acTimeoutSpinBox)
        EditorAutocompletionPage.setTabOrder(self.acTimeoutSpinBox, self.acScintillaCheckBox)
        EditorAutocompletionPage.setTabOrder(self.acScintillaCheckBox, self.acWatchdogDoubleSpinBox)
        EditorAutocompletionPage.setTabOrder(self.acWatchdogDoubleSpinBox, self.acCacheGroup)
        EditorAutocompletionPage.setTabOrder(self.acCacheGroup, self.acCacheSizeSpinBox)
        EditorAutocompletionPage.setTabOrder(self.acCacheSizeSpinBox, self.acCacheTimeSpinBox)

    def retranslateUi(self, EditorAutocompletionPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorAutocompletionPage", "<b>Configure Completion Support</b>"))
        self.groupBox.setTitle(_translate("EditorAutocompletionPage", "General"))
        self.acReplaceWordCheckBox.setToolTip(_translate("EditorAutocompletionPage", "Select this, if the word to the right should be replaced by the selected entry"))
        self.acReplaceWordCheckBox.setText(_translate("EditorAutocompletionPage", "Replace word"))
        self.acCaseSensitivityCheckBox.setToolTip(_translate("EditorAutocompletionPage", "Select this to have case sensitive auto-completion lists"))
        self.acCaseSensitivityCheckBox.setText(_translate("EditorAutocompletionPage", "Case sensitive"))
        self.acReversedCheckBox.setToolTip(_translate("EditorAutocompletionPage", "Select to show completions of type \'public\' first"))
        self.acReversedCheckBox.setText(_translate("EditorAutocompletionPage", "Show \'public\' completions first"))
        self.label_6.setText(_translate("EditorAutocompletionPage", "Maximum visible characters:"))
        self.label_5.setText(_translate("EditorAutocompletionPage", "Maximum visible lines: "))
        self.acLinesSlider.setToolTip(_translate("EditorAutocompletionPage", "Move to set the maximum number of lines shown in a autocomplete list."))
        self.lcdNumber.setToolTip(_translate("EditorAutocompletionPage", "Displays the maximum number of lines."))
        self.acCharSlider.setToolTip(_translate("EditorAutocompletionPage", "Move to set the maximum number of characters visible in one line."))
        self.lcdNumber_2.setToolTip(_translate("EditorAutocompletionPage", "Displays the approximate number of characters per line."))
        self.acEnabledGroupBox.setToolTip(_translate("EditorAutocompletionPage", "Select this to enable autocompletion"))
        self.acEnabledGroupBox.setWhatsThis(_translate("EditorAutocompletionPage", "<b>Autocompletion Enabled</b><p>Select to enable autocompletion. In order to get autocompletion from alternative autocompletion providers (if installed), these have to be enabled on their respective configuration page. Only one alternative provider might be enabled.</p>"))
        self.acEnabledGroupBox.setTitle(_translate("EditorAutocompletionPage", "Automatic Completion Enabled"))
        self.textLabel1_2.setText(_translate("EditorAutocompletionPage", "Threshold:"))
        self.label.setText(_translate("EditorAutocompletionPage", "Time to start completion:"))
        self.acThresholdSlider.setToolTip(_translate("EditorAutocompletionPage", "Move to set the threshold for display of an autocompletion list"))
        self.lCDNumber4.setToolTip(_translate("EditorAutocompletionPage", "Displays the selected autocompletion threshold"))
        self.acTimeoutSpinBox.setToolTip(_translate("EditorAutocompletionPage", "Enter the time in milliseconds after which a list with completion proposals shall be shown"))
        self.acTimeoutSpinBox.setSuffix(_translate("EditorAutocompletionPage", " ms"))
        self.groupBox_3.setTitle(_translate("EditorAutocompletionPage", "Plug-In Behavior"))
        self.acScintillaCheckBox.setToolTip(_translate("EditorAutocompletionPage", "Select to show QScintilla provided completions, if the selected plug-ins fail"))
        self.acScintillaCheckBox.setWhatsThis(_translate("EditorAutocompletionPage", "QScintilla provided completions are shown, if this option is enabled and completions shall be provided by plug-ins (see completions sub-page of the plug-in) and the plugin-ins don\'t deliver any completions."))
        self.acScintillaCheckBox.setText(_translate("EditorAutocompletionPage", "Show QScintilla completions, if plug-ins fail"))
        self.label_4.setText(_translate("EditorAutocompletionPage", "Maximum time to wait:"))
        self.acWatchdogDoubleSpinBox.setToolTip(_translate("EditorAutocompletionPage", "Enter the time in seconds after which QSintilla should be used"))
        self.acWatchdogDoubleSpinBox.setSuffix(_translate("EditorAutocompletionPage", " s"))
        self.acCacheGroup.setToolTip(_translate("EditorAutocompletionPage", "Select to enable caching of completion results"))
        self.acCacheGroup.setTitle(_translate("EditorAutocompletionPage", "Completions Cache"))
        self.label_2.setText(_translate("EditorAutocompletionPage", "Size:"))
        self.acCacheSizeSpinBox.setToolTip(_translate("EditorAutocompletionPage", "Enter the maximum number of entries to be kept in the completions cache"))
        self.acCacheSizeSpinBox.setSuffix(_translate("EditorAutocompletionPage", " entries"))
        self.label_3.setText(_translate("EditorAutocompletionPage", "Timeout:"))
        self.acCacheTimeSpinBox.setToolTip(_translate("EditorAutocompletionPage", "Enter the time in seconds after which a cached completion entry should be removed from the completions cache"))
        self.acCacheTimeSpinBox.setSuffix(_translate("EditorAutocompletionPage", " s"))
