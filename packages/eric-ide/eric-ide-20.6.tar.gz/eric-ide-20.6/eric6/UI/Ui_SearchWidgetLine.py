# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/UI/SearchWidgetLine.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchWidgetLine(object):
    def setupUi(self, SearchWidgetLine):
        SearchWidgetLine.setObjectName("SearchWidgetLine")
        SearchWidgetLine.resize(606, 52)
        self.verticalLayout = QtWidgets.QVBoxLayout(SearchWidgetLine)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeButton = QtWidgets.QToolButton(SearchWidgetLine)
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.label = QtWidgets.QLabel(SearchWidgetLine)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.findtextCombo = QtWidgets.QComboBox(SearchWidgetLine)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findtextCombo.sizePolicy().hasHeightForWidth())
        self.findtextCombo.setSizePolicy(sizePolicy)
        self.findtextCombo.setMinimumSize(QtCore.QSize(200, 0))
        self.findtextCombo.setEditable(True)
        self.findtextCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.findtextCombo.setDuplicatesEnabled(False)
        self.findtextCombo.setObjectName("findtextCombo")
        self.horizontalLayout_2.addWidget(self.findtextCombo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.findPrevButton = QtWidgets.QToolButton(SearchWidgetLine)
        self.findPrevButton.setObjectName("findPrevButton")
        self.horizontalLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtWidgets.QToolButton(SearchWidgetLine)
        self.findNextButton.setObjectName("findNextButton")
        self.horizontalLayout.addWidget(self.findNextButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.caseCheckBox = QtWidgets.QCheckBox(SearchWidgetLine)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout_2.addWidget(self.caseCheckBox)
        self.wordCheckBox = QtWidgets.QCheckBox(SearchWidgetLine)
        self.wordCheckBox.setObjectName("wordCheckBox")
        self.horizontalLayout_2.addWidget(self.wordCheckBox)
        self.regexpCheckBox = QtWidgets.QCheckBox(SearchWidgetLine)
        self.regexpCheckBox.setObjectName("regexpCheckBox")
        self.horizontalLayout_2.addWidget(self.regexpCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.statusLabel = QtWidgets.QLabel(SearchWidgetLine)
        self.statusLabel.setText("")
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout.addWidget(self.statusLabel)

        self.retranslateUi(SearchWidgetLine)
        QtCore.QMetaObject.connectSlotsByName(SearchWidgetLine)
        SearchWidgetLine.setTabOrder(self.findtextCombo, self.caseCheckBox)
        SearchWidgetLine.setTabOrder(self.caseCheckBox, self.wordCheckBox)
        SearchWidgetLine.setTabOrder(self.wordCheckBox, self.regexpCheckBox)
        SearchWidgetLine.setTabOrder(self.regexpCheckBox, self.findPrevButton)
        SearchWidgetLine.setTabOrder(self.findPrevButton, self.findNextButton)
        SearchWidgetLine.setTabOrder(self.findNextButton, self.closeButton)

    def retranslateUi(self, SearchWidgetLine):
        _translate = QtCore.QCoreApplication.translate
        SearchWidgetLine.setWindowTitle(_translate("SearchWidgetLine", "Find"))
        self.closeButton.setToolTip(_translate("SearchWidgetLine", "Press to close the window"))
        self.label.setText(_translate("SearchWidgetLine", "Find:"))
        self.findPrevButton.setToolTip(_translate("SearchWidgetLine", "Press to find the previous occurrence"))
        self.findNextButton.setToolTip(_translate("SearchWidgetLine", "Press to find the next occurrence"))
        self.caseCheckBox.setText(_translate("SearchWidgetLine", "Match case"))
        self.wordCheckBox.setText(_translate("SearchWidgetLine", "Whole word"))
        self.regexpCheckBox.setText(_translate("SearchWidgetLine", "Regexp"))
