# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/HexEdit/HexEditSearchWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HexEditSearchWidget(object):
    def setupUi(self, HexEditSearchWidget):
        HexEditSearchWidget.setObjectName("HexEditSearchWidget")
        HexEditSearchWidget.resize(600, 28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HexEditSearchWidget.sizePolicy().hasHeightForWidth())
        HexEditSearchWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(HexEditSearchWidget)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeButton = QtWidgets.QToolButton(HexEditSearchWidget)
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.label = QtWidgets.QLabel(HexEditSearchWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.findFormatCombo = QtWidgets.QComboBox(HexEditSearchWidget)
        self.findFormatCombo.setObjectName("findFormatCombo")
        self.horizontalLayout_2.addWidget(self.findFormatCombo)
        self.findtextCombo = QtWidgets.QComboBox(HexEditSearchWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findtextCombo.sizePolicy().hasHeightForWidth())
        self.findtextCombo.setSizePolicy(sizePolicy)
        self.findtextCombo.setMinimumSize(QtCore.QSize(300, 0))
        self.findtextCombo.setEditable(True)
        self.findtextCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.findtextCombo.setDuplicatesEnabled(False)
        self.findtextCombo.setObjectName("findtextCombo")
        self.horizontalLayout_2.addWidget(self.findtextCombo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.findPrevButton = QtWidgets.QToolButton(HexEditSearchWidget)
        self.findPrevButton.setObjectName("findPrevButton")
        self.horizontalLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtWidgets.QToolButton(HexEditSearchWidget)
        self.findNextButton.setObjectName("findNextButton")
        self.horizontalLayout.addWidget(self.findNextButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(HexEditSearchWidget)
        QtCore.QMetaObject.connectSlotsByName(HexEditSearchWidget)
        HexEditSearchWidget.setTabOrder(self.findFormatCombo, self.findtextCombo)
        HexEditSearchWidget.setTabOrder(self.findtextCombo, self.findPrevButton)
        HexEditSearchWidget.setTabOrder(self.findPrevButton, self.findNextButton)
        HexEditSearchWidget.setTabOrder(self.findNextButton, self.closeButton)

    def retranslateUi(self, HexEditSearchWidget):
        _translate = QtCore.QCoreApplication.translate
        HexEditSearchWidget.setWindowTitle(_translate("HexEditSearchWidget", "Find"))
        self.closeButton.setToolTip(_translate("HexEditSearchWidget", "Press to close the window"))
        self.label.setText(_translate("HexEditSearchWidget", "Find:"))
        self.findFormatCombo.setToolTip(_translate("HexEditSearchWidget", "Select the data format of the find data field"))
        self.findPrevButton.setToolTip(_translate("HexEditSearchWidget", "Press to find the previous occurrence"))
        self.findNextButton.setToolTip(_translate("HexEditSearchWidget", "Press to find the next occurrence"))
