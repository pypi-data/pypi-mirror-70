# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/PluginManagerPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginManagerPage(object):
    def setupUi(self, PluginManagerPage):
        PluginManagerPage.setObjectName("PluginManagerPage")
        PluginManagerPage.resize(528, 436)
        self.verticalLayout = QtWidgets.QVBoxLayout(PluginManagerPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(PluginManagerPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line9_2 = QtWidgets.QFrame(PluginManagerPage)
        self.line9_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_2.setObjectName("line9_2")
        self.verticalLayout.addWidget(self.line9_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(PluginManagerPage)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.downloadDirPicker = E5PathPicker(PluginManagerPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadDirPicker.sizePolicy().hasHeightForWidth())
        self.downloadDirPicker.setSizePolicy(sizePolicy)
        self.downloadDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.downloadDirPicker.setObjectName("downloadDirPicker")
        self.horizontalLayout_2.addWidget(self.downloadDirPicker)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(PluginManagerPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.generationsSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.generationsSpinBox.setMinimum(1)
        self.generationsSpinBox.setMaximum(9)
        self.generationsSpinBox.setObjectName("generationsSpinBox")
        self.horizontalLayout_4.addWidget(self.generationsSpinBox)
        spacerItem = QtWidgets.QSpacerItem(252, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.keepHiddenCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.keepHiddenCheckBox.setObjectName("keepHiddenCheckBox")
        self.verticalLayout_2.addWidget(self.keepHiddenCheckBox)
        self.startupCleanupCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.startupCleanupCheckBox.setObjectName("startupCleanupCheckBox")
        self.verticalLayout_2.addWidget(self.startupCleanupCheckBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.TextLabel1_2_2_2_3 = QtWidgets.QLabel(PluginManagerPage)
        self.TextLabel1_2_2_2_3.setObjectName("TextLabel1_2_2_2_3")
        self.verticalLayout.addWidget(self.TextLabel1_2_2_2_3)
        self.activateExternalPluginsCheckBox = QtWidgets.QCheckBox(PluginManagerPage)
        self.activateExternalPluginsCheckBox.setObjectName("activateExternalPluginsCheckBox")
        self.verticalLayout.addWidget(self.activateExternalPluginsCheckBox)
        self.groupBox_2 = QtWidgets.QGroupBox(PluginManagerPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.noCheckRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.noCheckRadioButton.setObjectName("noCheckRadioButton")
        self.horizontalLayout_3.addWidget(self.noCheckRadioButton)
        self.alwaysCheckRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.alwaysCheckRadioButton.setObjectName("alwaysCheckRadioButton")
        self.horizontalLayout_3.addWidget(self.alwaysCheckRadioButton)
        self.dailyCheckRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.dailyCheckRadioButton.setObjectName("dailyCheckRadioButton")
        self.horizontalLayout_3.addWidget(self.dailyCheckRadioButton)
        self.weeklyCheckRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.weeklyCheckRadioButton.setObjectName("weeklyCheckRadioButton")
        self.horizontalLayout_3.addWidget(self.weeklyCheckRadioButton)
        self.monthlyCheckRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.monthlyCheckRadioButton.setObjectName("monthlyCheckRadioButton")
        self.horizontalLayout_3.addWidget(self.monthlyCheckRadioButton)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.downloadedOnlyCheckBox = QtWidgets.QCheckBox(PluginManagerPage)
        self.downloadedOnlyCheckBox.setObjectName("downloadedOnlyCheckBox")
        self.verticalLayout.addWidget(self.downloadedOnlyCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(PluginManagerPage)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.repositoryUrlEdit = QtWidgets.QLineEdit(PluginManagerPage)
        self.repositoryUrlEdit.setReadOnly(True)
        self.repositoryUrlEdit.setObjectName("repositoryUrlEdit")
        self.horizontalLayout.addWidget(self.repositoryUrlEdit)
        self.repositoryUrlEditButton = QtWidgets.QPushButton(PluginManagerPage)
        self.repositoryUrlEditButton.setCheckable(True)
        self.repositoryUrlEditButton.setObjectName("repositoryUrlEditButton")
        self.horizontalLayout.addWidget(self.repositoryUrlEditButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(435, 121, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(PluginManagerPage)
        QtCore.QMetaObject.connectSlotsByName(PluginManagerPage)
        PluginManagerPage.setTabOrder(self.downloadDirPicker, self.generationsSpinBox)
        PluginManagerPage.setTabOrder(self.generationsSpinBox, self.keepHiddenCheckBox)
        PluginManagerPage.setTabOrder(self.keepHiddenCheckBox, self.startupCleanupCheckBox)
        PluginManagerPage.setTabOrder(self.startupCleanupCheckBox, self.activateExternalPluginsCheckBox)
        PluginManagerPage.setTabOrder(self.activateExternalPluginsCheckBox, self.noCheckRadioButton)
        PluginManagerPage.setTabOrder(self.noCheckRadioButton, self.alwaysCheckRadioButton)
        PluginManagerPage.setTabOrder(self.alwaysCheckRadioButton, self.dailyCheckRadioButton)
        PluginManagerPage.setTabOrder(self.dailyCheckRadioButton, self.weeklyCheckRadioButton)
        PluginManagerPage.setTabOrder(self.weeklyCheckRadioButton, self.monthlyCheckRadioButton)
        PluginManagerPage.setTabOrder(self.monthlyCheckRadioButton, self.downloadedOnlyCheckBox)
        PluginManagerPage.setTabOrder(self.downloadedOnlyCheckBox, self.repositoryUrlEdit)
        PluginManagerPage.setTabOrder(self.repositoryUrlEdit, self.repositoryUrlEditButton)

    def retranslateUi(self, PluginManagerPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("PluginManagerPage", "<b>Configure plugin manager</b>"))
        self.label.setText(_translate("PluginManagerPage", "Plugins download directory:"))
        self.downloadDirPicker.setToolTip(_translate("PluginManagerPage", "Enter the plugins download directory"))
        self.groupBox.setTitle(_translate("PluginManagerPage", "Download Housekeeping"))
        self.label_2.setText(_translate("PluginManagerPage", "No. of generations to keep:"))
        self.generationsSpinBox.setToolTip(_translate("PluginManagerPage", "Enter the number of generations to keep for each plugin"))
        self.keepHiddenCheckBox.setToolTip(_translate("PluginManagerPage", "Select to keep generations of hidden plugins"))
        self.keepHiddenCheckBox.setText(_translate("PluginManagerPage", "Keep generations of hidden plugins"))
        self.startupCleanupCheckBox.setToolTip(_translate("PluginManagerPage", "Select to cleanup the plugins download area during startuo"))
        self.startupCleanupCheckBox.setText(_translate("PluginManagerPage", "Cleanup during startup"))
        self.TextLabel1_2_2_2_3.setText(_translate("PluginManagerPage", "<font color=\"#FF0000\"><b>Note:</b> The following settings are activated at the next startup of the application.</font>"))
        self.activateExternalPluginsCheckBox.setToolTip(_translate("PluginManagerPage", "Select to enable external plugins to be loaded"))
        self.activateExternalPluginsCheckBox.setText(_translate("PluginManagerPage", "Load external plugins"))
        self.groupBox_2.setTitle(_translate("PluginManagerPage", "Check for plugin updates"))
        self.noCheckRadioButton.setToolTip(_translate("PluginManagerPage", "Select to disable update checking"))
        self.noCheckRadioButton.setText(_translate("PluginManagerPage", "Never"))
        self.alwaysCheckRadioButton.setToolTip(_translate("PluginManagerPage", "Select to check for updates whenever eric is started"))
        self.alwaysCheckRadioButton.setText(_translate("PluginManagerPage", "Always"))
        self.dailyCheckRadioButton.setToolTip(_translate("PluginManagerPage", "Select to check for updates once a day"))
        self.dailyCheckRadioButton.setText(_translate("PluginManagerPage", "Daily"))
        self.weeklyCheckRadioButton.setToolTip(_translate("PluginManagerPage", "Select to check for updates once a week"))
        self.weeklyCheckRadioButton.setText(_translate("PluginManagerPage", "Weekly"))
        self.monthlyCheckRadioButton.setToolTip(_translate("PluginManagerPage", "Select to check for updates once a month"))
        self.monthlyCheckRadioButton.setText(_translate("PluginManagerPage", "Monthly"))
        self.downloadedOnlyCheckBox.setToolTip(_translate("PluginManagerPage", "Select to check only already installed plugins for updates"))
        self.downloadedOnlyCheckBox.setText(_translate("PluginManagerPage", "Check only installed plugins for updates"))
        self.label_4.setText(_translate("PluginManagerPage", "Repository URL:"))
        self.repositoryUrlEdit.setToolTip(_translate("PluginManagerPage", "Shows the repository URL"))
        self.repositoryUrlEditButton.setToolTip(_translate("PluginManagerPage", "Press to edit the plugin repository URL"))
        self.repositoryUrlEditButton.setText(_translate("PluginManagerPage", "Edit URL"))
from E5Gui.E5PathPicker import E5PathPicker
