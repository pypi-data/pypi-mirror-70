# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/MicroPython/MicroPythonFileManagerWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MicroPythonFileManagerWidget(object):
    def setupUi(self, MicroPythonFileManagerWidget):
        MicroPythonFileManagerWidget.setObjectName("MicroPythonFileManagerWidget")
        MicroPythonFileManagerWidget.resize(675, 338)
        self.gridLayout = QtWidgets.QGridLayout(MicroPythonFileManagerWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(MicroPythonFileManagerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(MicroPythonFileManagerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.deviceConnectedLed = E5Led(MicroPythonFileManagerWidget)
        self.deviceConnectedLed.setObjectName("deviceConnectedLed")
        self.horizontalLayout_3.addWidget(self.deviceConnectedLed)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 2, 1, 1)
        self.localFileTreeWidget = QtWidgets.QTreeWidget(MicroPythonFileManagerWidget)
        self.localFileTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.localFileTreeWidget.setAlternatingRowColors(True)
        self.localFileTreeWidget.setRootIsDecorated(False)
        self.localFileTreeWidget.setItemsExpandable(False)
        self.localFileTreeWidget.setObjectName("localFileTreeWidget")
        self.localFileTreeWidget.header().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.localFileTreeWidget, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 26, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.syncButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.syncButton.setObjectName("syncButton")
        self.verticalLayout.addWidget(self.syncButton)
        self.putButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.putButton.setObjectName("putButton")
        self.verticalLayout.addWidget(self.putButton)
        self.putAsButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.putAsButton.setObjectName("putAsButton")
        self.verticalLayout.addWidget(self.putAsButton)
        self.getButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.getButton.setObjectName("getButton")
        self.verticalLayout.addWidget(self.getButton)
        self.getAsButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.getAsButton.setObjectName("getAsButton")
        self.verticalLayout.addWidget(self.getAsButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 26, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.deviceFileTreeWidget = QtWidgets.QTreeWidget(MicroPythonFileManagerWidget)
        self.deviceFileTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.deviceFileTreeWidget.setAlternatingRowColors(True)
        self.deviceFileTreeWidget.setRootIsDecorated(False)
        self.deviceFileTreeWidget.setItemsExpandable(False)
        self.deviceFileTreeWidget.setObjectName("deviceFileTreeWidget")
        self.deviceFileTreeWidget.header().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.deviceFileTreeWidget, 1, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.localCwd = QtWidgets.QLineEdit(MicroPythonFileManagerWidget)
        self.localCwd.setReadOnly(True)
        self.localCwd.setObjectName("localCwd")
        self.horizontalLayout.addWidget(self.localCwd)
        self.localUpButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.localUpButton.setObjectName("localUpButton")
        self.horizontalLayout.addWidget(self.localUpButton)
        self.localReloadButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.localReloadButton.setObjectName("localReloadButton")
        self.horizontalLayout.addWidget(self.localReloadButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.deviceCwd = QtWidgets.QLineEdit(MicroPythonFileManagerWidget)
        self.deviceCwd.setReadOnly(True)
        self.deviceCwd.setObjectName("deviceCwd")
        self.horizontalLayout_2.addWidget(self.deviceCwd)
        self.deviceUpButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.deviceUpButton.setObjectName("deviceUpButton")
        self.horizontalLayout_2.addWidget(self.deviceUpButton)
        self.deviceReloadButton = QtWidgets.QToolButton(MicroPythonFileManagerWidget)
        self.deviceReloadButton.setObjectName("deviceReloadButton")
        self.horizontalLayout_2.addWidget(self.deviceReloadButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)

        self.retranslateUi(MicroPythonFileManagerWidget)
        QtCore.QMetaObject.connectSlotsByName(MicroPythonFileManagerWidget)
        MicroPythonFileManagerWidget.setTabOrder(self.localFileTreeWidget, self.deviceFileTreeWidget)
        MicroPythonFileManagerWidget.setTabOrder(self.deviceFileTreeWidget, self.syncButton)
        MicroPythonFileManagerWidget.setTabOrder(self.syncButton, self.putButton)
        MicroPythonFileManagerWidget.setTabOrder(self.putButton, self.putAsButton)
        MicroPythonFileManagerWidget.setTabOrder(self.putAsButton, self.getButton)
        MicroPythonFileManagerWidget.setTabOrder(self.getButton, self.getAsButton)
        MicroPythonFileManagerWidget.setTabOrder(self.getAsButton, self.localCwd)
        MicroPythonFileManagerWidget.setTabOrder(self.localCwd, self.localUpButton)
        MicroPythonFileManagerWidget.setTabOrder(self.localUpButton, self.localReloadButton)
        MicroPythonFileManagerWidget.setTabOrder(self.localReloadButton, self.deviceCwd)
        MicroPythonFileManagerWidget.setTabOrder(self.deviceCwd, self.deviceUpButton)
        MicroPythonFileManagerWidget.setTabOrder(self.deviceUpButton, self.deviceReloadButton)

    def retranslateUi(self, MicroPythonFileManagerWidget):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MicroPythonFileManagerWidget", "Local Files"))
        self.label_2.setText(_translate("MicroPythonFileManagerWidget", "Device Files"))
        self.localFileTreeWidget.setSortingEnabled(True)
        self.localFileTreeWidget.headerItem().setText(0, _translate("MicroPythonFileManagerWidget", "Name"))
        self.localFileTreeWidget.headerItem().setText(1, _translate("MicroPythonFileManagerWidget", "Mode"))
        self.localFileTreeWidget.headerItem().setText(2, _translate("MicroPythonFileManagerWidget", "Size"))
        self.localFileTreeWidget.headerItem().setText(3, _translate("MicroPythonFileManagerWidget", "Time"))
        self.syncButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to sync the local directory to the device directory"))
        self.putButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to copy the selected file to the device"))
        self.putAsButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to copy the selected file to the device with a new name"))
        self.getButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to copy the selected file from the device"))
        self.getAsButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to copy the selected file from the device with a new name"))
        self.deviceFileTreeWidget.setSortingEnabled(True)
        self.deviceFileTreeWidget.headerItem().setText(0, _translate("MicroPythonFileManagerWidget", "Name"))
        self.deviceFileTreeWidget.headerItem().setText(1, _translate("MicroPythonFileManagerWidget", "Mode"))
        self.deviceFileTreeWidget.headerItem().setText(2, _translate("MicroPythonFileManagerWidget", "Size"))
        self.deviceFileTreeWidget.headerItem().setText(3, _translate("MicroPythonFileManagerWidget", "Time"))
        self.localUpButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to move one directory level up"))
        self.localReloadButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to reload the list"))
        self.deviceUpButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to move one directory level up"))
        self.deviceReloadButton.setToolTip(_translate("MicroPythonFileManagerWidget", "Press to reload the list"))
from E5Gui.E5Led import E5Led
