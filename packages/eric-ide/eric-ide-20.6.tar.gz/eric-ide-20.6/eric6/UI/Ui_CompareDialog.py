# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/UI/CompareDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompareDialog(object):
    def setupUi(self, CompareDialog):
        CompareDialog.setObjectName("CompareDialog")
        CompareDialog.resize(950, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(CompareDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filesGroup = QtWidgets.QGroupBox(CompareDialog)
        self.filesGroup.setFlat(True)
        self.filesGroup.setObjectName("filesGroup")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.filesGroup)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textLabel1 = QtWidgets.QLabel(self.filesGroup)
        self.textLabel1.setObjectName("textLabel1")
        self.horizontalLayout_2.addWidget(self.textLabel1)
        self.file1Picker = E5PathPicker(self.filesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file1Picker.sizePolicy().hasHeightForWidth())
        self.file1Picker.setSizePolicy(sizePolicy)
        self.file1Picker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.file1Picker.setObjectName("file1Picker")
        self.horizontalLayout_2.addWidget(self.file1Picker)
        self.textLabel2 = QtWidgets.QLabel(self.filesGroup)
        self.textLabel2.setObjectName("textLabel2")
        self.horizontalLayout_2.addWidget(self.textLabel2)
        self.file2Picker = E5PathPicker(self.filesGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file2Picker.sizePolicy().hasHeightForWidth())
        self.file2Picker.setSizePolicy(sizePolicy)
        self.file2Picker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.file2Picker.setObjectName("file2Picker")
        self.horizontalLayout_2.addWidget(self.file2Picker)
        self.verticalLayout.addWidget(self.filesGroup)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.file1Label = QtWidgets.QLabel(CompareDialog)
        self.file1Label.setText("")
        self.file1Label.setWordWrap(True)
        self.file1Label.setObjectName("file1Label")
        self.gridLayout.addWidget(self.file1Label, 0, 0, 1, 1)
        self.file2Label = QtWidgets.QLabel(CompareDialog)
        self.file2Label.setText("")
        self.file2Label.setWordWrap(True)
        self.file2Label.setObjectName("file2Label")
        self.gridLayout.addWidget(self.file2Label, 0, 2, 1, 1)
        self.contents_1 = QtWidgets.QTextEdit(CompareDialog)
        self.contents_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.contents_1.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.contents_1.setReadOnly(True)
        self.contents_1.setTabStopWidth(8)
        self.contents_1.setAcceptRichText(False)
        self.contents_1.setObjectName("contents_1")
        self.gridLayout.addWidget(self.contents_1, 1, 0, 1, 1)
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        spacerItem = QtWidgets.QSpacerItem(20, 101, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.firstButton = QtWidgets.QToolButton(CompareDialog)
        self.firstButton.setEnabled(False)
        self.firstButton.setObjectName("firstButton")
        self.vboxlayout.addWidget(self.firstButton)
        self.upButton = QtWidgets.QToolButton(CompareDialog)
        self.upButton.setEnabled(False)
        self.upButton.setObjectName("upButton")
        self.vboxlayout.addWidget(self.upButton)
        self.downButton = QtWidgets.QToolButton(CompareDialog)
        self.downButton.setEnabled(False)
        self.downButton.setObjectName("downButton")
        self.vboxlayout.addWidget(self.downButton)
        self.lastButton = QtWidgets.QToolButton(CompareDialog)
        self.lastButton.setEnabled(False)
        self.lastButton.setObjectName("lastButton")
        self.vboxlayout.addWidget(self.lastButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 101, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.vboxlayout, 1, 1, 1, 1)
        self.contents_2 = QtWidgets.QTextEdit(CompareDialog)
        self.contents_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.contents_2.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.contents_2.setReadOnly(True)
        self.contents_2.setTabStopWidth(8)
        self.contents_2.setAcceptRichText(False)
        self.contents_2.setObjectName("contents_2")
        self.gridLayout.addWidget(self.contents_2, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.synchronizeCheckBox = QtWidgets.QCheckBox(CompareDialog)
        self.synchronizeCheckBox.setChecked(True)
        self.synchronizeCheckBox.setObjectName("synchronizeCheckBox")
        self.verticalLayout.addWidget(self.synchronizeCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.totalLabel = QtWidgets.QLabel(CompareDialog)
        self.totalLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.totalLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.totalLabel.setObjectName("totalLabel")
        self.horizontalLayout.addWidget(self.totalLabel)
        self.changedLabel = QtWidgets.QLabel(CompareDialog)
        self.changedLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.changedLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.changedLabel.setObjectName("changedLabel")
        self.horizontalLayout.addWidget(self.changedLabel)
        self.addedLabel = QtWidgets.QLabel(CompareDialog)
        self.addedLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.addedLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.addedLabel.setObjectName("addedLabel")
        self.horizontalLayout.addWidget(self.addedLabel)
        self.deletedLabel = QtWidgets.QLabel(CompareDialog)
        self.deletedLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.deletedLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.deletedLabel.setObjectName("deletedLabel")
        self.horizontalLayout.addWidget(self.deletedLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(CompareDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textLabel1.setBuddy(self.file1Picker)
        self.textLabel2.setBuddy(self.file2Picker)

        self.retranslateUi(CompareDialog)
        self.buttonBox.rejected.connect(CompareDialog.close)
        QtCore.QMetaObject.connectSlotsByName(CompareDialog)
        CompareDialog.setTabOrder(self.file1Picker, self.file2Picker)
        CompareDialog.setTabOrder(self.file2Picker, self.firstButton)
        CompareDialog.setTabOrder(self.firstButton, self.upButton)
        CompareDialog.setTabOrder(self.upButton, self.downButton)
        CompareDialog.setTabOrder(self.downButton, self.lastButton)
        CompareDialog.setTabOrder(self.lastButton, self.synchronizeCheckBox)

    def retranslateUi(self, CompareDialog):
        _translate = QtCore.QCoreApplication.translate
        CompareDialog.setWindowTitle(_translate("CompareDialog", "File Comparison"))
        self.filesGroup.setTitle(_translate("CompareDialog", "Files to be compared:"))
        self.textLabel1.setText(_translate("CompareDialog", "File &1:"))
        self.file1Picker.setToolTip(_translate("CompareDialog", "Enter the name of the first file"))
        self.textLabel2.setText(_translate("CompareDialog", "File &2:"))
        self.file2Picker.setToolTip(_translate("CompareDialog", "Enter the name of the second file"))
        self.firstButton.setToolTip(_translate("CompareDialog", "Press to move to the first difference"))
        self.upButton.setToolTip(_translate("CompareDialog", "Press to move to the previous difference"))
        self.downButton.setToolTip(_translate("CompareDialog", "Press to move to the next difference"))
        self.lastButton.setToolTip(_translate("CompareDialog", "Press to move to the last difference"))
        self.synchronizeCheckBox.setToolTip(_translate("CompareDialog", "Select, if the horizontal scrollbars should be synchronized"))
        self.synchronizeCheckBox.setText(_translate("CompareDialog", "&Synchronize horizontal scrollbars"))
        self.synchronizeCheckBox.setShortcut(_translate("CompareDialog", "Alt+S"))
from E5Gui.E5PathPicker import E5PathPicker
