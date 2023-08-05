# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitStatusDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitStatusDialog(object):
    def setupUi(self, GitStatusDialog):
        GitStatusDialog.setObjectName("GitStatusDialog")
        GitStatusDialog.resize(900, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitStatusDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.actionsButton = QtWidgets.QToolButton(GitStatusDialog)
        self.actionsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.actionsButton.setObjectName("actionsButton")
        self.horizontalLayout_2.addWidget(self.actionsButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(GitStatusDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.statusFilterCombo = QtWidgets.QComboBox(GitStatusDialog)
        self.statusFilterCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.statusFilterCombo.setObjectName("statusFilterCombo")
        self.horizontalLayout_2.addWidget(self.statusFilterCombo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.vDiffSplitter = QtWidgets.QSplitter(GitStatusDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.vDiffSplitter.sizePolicy().hasHeightForWidth())
        self.vDiffSplitter.setSizePolicy(sizePolicy)
        self.vDiffSplitter.setOrientation(QtCore.Qt.Vertical)
        self.vDiffSplitter.setObjectName("vDiffSplitter")
        self.statusList = QtWidgets.QTreeWidget(self.vDiffSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.statusList.sizePolicy().hasHeightForWidth())
        self.statusList.setSizePolicy(sizePolicy)
        self.statusList.setAlternatingRowColors(True)
        self.statusList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.statusList.setRootIsDecorated(False)
        self.statusList.setObjectName("statusList")
        self.hDiffSplitter = QtWidgets.QSplitter(self.vDiffSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.hDiffSplitter.sizePolicy().hasHeightForWidth())
        self.hDiffSplitter.setSizePolicy(sizePolicy)
        self.hDiffSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.hDiffSplitter.setChildrenCollapsible(False)
        self.hDiffSplitter.setObjectName("hDiffSplitter")
        self.lDiffWidget = QtWidgets.QWidget(self.hDiffSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.lDiffWidget.sizePolicy().hasHeightForWidth())
        self.lDiffWidget.setSizePolicy(sizePolicy)
        self.lDiffWidget.setObjectName("lDiffWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.lDiffWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.lDiffWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.lDiffEdit = QtWidgets.QTextEdit(self.lDiffWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lDiffEdit.sizePolicy().hasHeightForWidth())
        self.lDiffEdit.setSizePolicy(sizePolicy)
        self.lDiffEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lDiffEdit.setTabChangesFocus(True)
        self.lDiffEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.lDiffEdit.setReadOnly(True)
        self.lDiffEdit.setAcceptRichText(False)
        self.lDiffEdit.setObjectName("lDiffEdit")
        self.verticalLayout_4.addWidget(self.lDiffEdit)
        self.rDiffWidget = QtWidgets.QWidget(self.hDiffSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.rDiffWidget.sizePolicy().hasHeightForWidth())
        self.rDiffWidget.setSizePolicy(sizePolicy)
        self.rDiffWidget.setObjectName("rDiffWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.rDiffWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.rDiffWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.rDiffEdit = QtWidgets.QTextEdit(self.rDiffWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rDiffEdit.sizePolicy().hasHeightForWidth())
        self.rDiffEdit.setSizePolicy(sizePolicy)
        self.rDiffEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.rDiffEdit.setTabChangesFocus(True)
        self.rDiffEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.rDiffEdit.setReadOnly(True)
        self.rDiffEdit.setAcceptRichText(False)
        self.rDiffEdit.setObjectName("rDiffEdit")
        self.verticalLayout_2.addWidget(self.rDiffEdit)
        self.verticalLayout.addWidget(self.vDiffSplitter)
        self.errorGroup = QtWidgets.QGroupBox(GitStatusDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(GitStatusDialog)
        self.inputGroup.setObjectName("inputGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.inputGroup)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem1 = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self.gridlayout.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self.gridlayout.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.statusFilterCombo)

        self.retranslateUi(GitStatusDialog)
        QtCore.QMetaObject.connectSlotsByName(GitStatusDialog)
        GitStatusDialog.setTabOrder(self.actionsButton, self.statusFilterCombo)
        GitStatusDialog.setTabOrder(self.statusFilterCombo, self.statusList)
        GitStatusDialog.setTabOrder(self.statusList, self.lDiffEdit)
        GitStatusDialog.setTabOrder(self.lDiffEdit, self.rDiffEdit)
        GitStatusDialog.setTabOrder(self.rDiffEdit, self.errors)
        GitStatusDialog.setTabOrder(self.errors, self.input)
        GitStatusDialog.setTabOrder(self.input, self.passwordCheckBox)
        GitStatusDialog.setTabOrder(self.passwordCheckBox, self.sendButton)

    def retranslateUi(self, GitStatusDialog):
        _translate = QtCore.QCoreApplication.translate
        GitStatusDialog.setWindowTitle(_translate("GitStatusDialog", "Git Status"))
        GitStatusDialog.setWhatsThis(_translate("GitStatusDialog", "<b>Git Status</b>\n"
"<p>This dialog shows the status of the selected file or project.</p>"))
        self.actionsButton.setToolTip(_translate("GitStatusDialog", "Select action from menu"))
        self.label.setText(_translate("GitStatusDialog", "&Filter on Status:"))
        self.statusFilterCombo.setToolTip(_translate("GitStatusDialog", "Select the status of entries to be shown"))
        self.statusList.setSortingEnabled(True)
        self.statusList.headerItem().setText(0, _translate("GitStatusDialog", "Commit"))
        self.statusList.headerItem().setText(1, _translate("GitStatusDialog", "Status (Work)"))
        self.statusList.headerItem().setText(2, _translate("GitStatusDialog", "Status (Staging)"))
        self.statusList.headerItem().setText(3, _translate("GitStatusDialog", "Path"))
        self.label_2.setText(_translate("GitStatusDialog", "Difference Working to Staging"))
        self.label_3.setText(_translate("GitStatusDialog", "Difference Staging to HEAD"))
        self.errorGroup.setTitle(_translate("GitStatusDialog", "Errors"))
        self.inputGroup.setTitle(_translate("GitStatusDialog", "Input"))
        self.sendButton.setToolTip(_translate("GitStatusDialog", "Press to send the input to the git process"))
        self.sendButton.setText(_translate("GitStatusDialog", "&Send"))
        self.sendButton.setShortcut(_translate("GitStatusDialog", "Alt+S"))
        self.input.setToolTip(_translate("GitStatusDialog", "Enter data to be sent to the git process"))
        self.passwordCheckBox.setToolTip(_translate("GitStatusDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("GitStatusDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("GitStatusDialog", "Alt+P"))
