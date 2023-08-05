# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/IconsPreviewDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IconsPreviewDialog(object):
    def setupUi(self, IconsPreviewDialog):
        IconsPreviewDialog.setObjectName("IconsPreviewDialog")
        IconsPreviewDialog.resize(596, 541)
        IconsPreviewDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(IconsPreviewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(IconsPreviewDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.directoryCombo = QtWidgets.QComboBox(IconsPreviewDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directoryCombo.sizePolicy().hasHeightForWidth())
        self.directoryCombo.setSizePolicy(sizePolicy)
        self.directoryCombo.setObjectName("directoryCombo")
        self.horizontalLayout.addWidget(self.directoryCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.iconView = QtWidgets.QListWidget(IconsPreviewDialog)
        self.iconView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.iconView.setMovement(QtWidgets.QListView.Free)
        self.iconView.setFlow(QtWidgets.QListView.LeftToRight)
        self.iconView.setGridSize(QtCore.QSize(100, 50))
        self.iconView.setViewMode(QtWidgets.QListView.IconMode)
        self.iconView.setObjectName("iconView")
        self.verticalLayout.addWidget(self.iconView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.invertButton = QtWidgets.QPushButton(IconsPreviewDialog)
        self.invertButton.setCheckable(True)
        self.invertButton.setObjectName("invertButton")
        self.horizontalLayout_2.addWidget(self.invertButton)
        self.refreshButton = QtWidgets.QPushButton(IconsPreviewDialog)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(IconsPreviewDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(IconsPreviewDialog)
        self.buttonBox.rejected.connect(IconsPreviewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IconsPreviewDialog)
        IconsPreviewDialog.setTabOrder(self.directoryCombo, self.iconView)
        IconsPreviewDialog.setTabOrder(self.iconView, self.invertButton)
        IconsPreviewDialog.setTabOrder(self.invertButton, self.refreshButton)

    def retranslateUi(self, IconsPreviewDialog):
        _translate = QtCore.QCoreApplication.translate
        IconsPreviewDialog.setWindowTitle(_translate("IconsPreviewDialog", "Icons Preview"))
        self.label.setText(_translate("IconsPreviewDialog", "Directory:"))
        self.directoryCombo.setToolTip(_translate("IconsPreviewDialog", "Select the icons directory to be shown"))
        self.invertButton.setToolTip(_translate("IconsPreviewDialog", "Select to invert the background color"))
        self.invertButton.setText(_translate("IconsPreviewDialog", "Invert Background"))
        self.refreshButton.setToolTip(_translate("IconsPreviewDialog", "Select to refresh the icons display"))
        self.refreshButton.setText(_translate("IconsPreviewDialog", "Refresh"))
