# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/QScintilla/SearchWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        SearchWidget.setObjectName("SearchWidget")
        SearchWidget.resize(973, 26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearchWidget.sizePolicy().hasHeightForWidth())
        SearchWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SearchWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeButton = QtWidgets.QToolButton(SearchWidget)
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.label = QtWidgets.QLabel(SearchWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.findtextCombo = QtWidgets.QComboBox(SearchWidget)
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
        self.findPrevButton = QtWidgets.QToolButton(SearchWidget)
        self.findPrevButton.setObjectName("findPrevButton")
        self.horizontalLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtWidgets.QToolButton(SearchWidget)
        self.findNextButton.setObjectName("findNextButton")
        self.horizontalLayout.addWidget(self.findNextButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.caseCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout_2.addWidget(self.caseCheckBox)
        self.wordCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.wordCheckBox.setObjectName("wordCheckBox")
        self.horizontalLayout_2.addWidget(self.wordCheckBox)
        self.regexpCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.regexpCheckBox.setObjectName("regexpCheckBox")
        self.horizontalLayout_2.addWidget(self.regexpCheckBox)
        self.wrapCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.wrapCheckBox.setObjectName("wrapCheckBox")
        self.horizontalLayout_2.addWidget(self.wrapCheckBox)
        self.selectionCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.selectionCheckBox.setObjectName("selectionCheckBox")
        self.horizontalLayout_2.addWidget(self.selectionCheckBox)
        self.label.setBuddy(self.findtextCombo)

        self.retranslateUi(SearchWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchWidget)
        SearchWidget.setTabOrder(self.findtextCombo, self.caseCheckBox)
        SearchWidget.setTabOrder(self.caseCheckBox, self.wordCheckBox)
        SearchWidget.setTabOrder(self.wordCheckBox, self.regexpCheckBox)
        SearchWidget.setTabOrder(self.regexpCheckBox, self.wrapCheckBox)
        SearchWidget.setTabOrder(self.wrapCheckBox, self.selectionCheckBox)
        SearchWidget.setTabOrder(self.selectionCheckBox, self.findNextButton)
        SearchWidget.setTabOrder(self.findNextButton, self.findPrevButton)
        SearchWidget.setTabOrder(self.findPrevButton, self.closeButton)

    def retranslateUi(self, SearchWidget):
        _translate = QtCore.QCoreApplication.translate
        SearchWidget.setWindowTitle(_translate("SearchWidget", "Find"))
        self.closeButton.setToolTip(_translate("SearchWidget", "Press to close the window"))
        self.label.setText(_translate("SearchWidget", "&Find:"))
        self.findPrevButton.setToolTip(_translate("SearchWidget", "Press to find the previous occurrence"))
        self.findNextButton.setToolTip(_translate("SearchWidget", "Press to find the next occurrence"))
        self.caseCheckBox.setText(_translate("SearchWidget", "&Match case"))
        self.wordCheckBox.setText(_translate("SearchWidget", "Whole &word"))
        self.regexpCheckBox.setText(_translate("SearchWidget", "Rege&xp"))
        self.wrapCheckBox.setText(_translate("SearchWidget", "Wrap &around"))
        self.selectionCheckBox.setText(_translate("SearchWidget", "&Selection only"))
