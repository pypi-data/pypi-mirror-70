# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitTagDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitTagDialog(object):
    def setupUi(self, GitTagDialog):
        GitTagDialog.setObjectName("GitTagDialog")
        GitTagDialog.resize(391, 344)
        GitTagDialog.setSizeGripEnabled(True)
        self.gridLayout_3 = QtWidgets.QGridLayout(GitTagDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.TextLabel1 = QtWidgets.QLabel(GitTagDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.gridLayout_3.addWidget(self.TextLabel1, 0, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(GitTagDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagCombo.sizePolicy().hasHeightForWidth())
        self.tagCombo.setSizePolicy(sizePolicy)
        self.tagCombo.setEditable(True)
        self.tagCombo.setDuplicatesEnabled(False)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout_3.addWidget(self.tagCombo, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(GitTagDialog)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.revisionEdit = QtWidgets.QLineEdit(GitTagDialog)
        self.revisionEdit.setObjectName("revisionEdit")
        self.gridLayout_3.addWidget(self.revisionEdit, 1, 1, 1, 1)
        self.tagActionGroup = QtWidgets.QGroupBox(GitTagDialog)
        self.tagActionGroup.setObjectName("tagActionGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tagActionGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.createTagButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.createTagButton.setChecked(True)
        self.createTagButton.setObjectName("createTagButton")
        self.gridLayout_2.addWidget(self.createTagButton, 0, 0, 1, 1)
        self.deleteTagButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.deleteTagButton.setObjectName("deleteTagButton")
        self.gridLayout_2.addWidget(self.deleteTagButton, 0, 1, 1, 1)
        self.verifyTagButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.verifyTagButton.setObjectName("verifyTagButton")
        self.gridLayout_2.addWidget(self.verifyTagButton, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tagActionGroup, 2, 0, 1, 2)
        self.tagTypeGroup = QtWidgets.QGroupBox(GitTagDialog)
        self.tagTypeGroup.setObjectName("tagTypeGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.tagTypeGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.globalTagButton = QtWidgets.QRadioButton(self.tagTypeGroup)
        self.globalTagButton.setChecked(True)
        self.globalTagButton.setObjectName("globalTagButton")
        self.gridLayout.addWidget(self.globalTagButton, 0, 0, 1, 1)
        self.signedTagButton = QtWidgets.QRadioButton(self.tagTypeGroup)
        self.signedTagButton.setObjectName("signedTagButton")
        self.gridLayout.addWidget(self.signedTagButton, 0, 1, 1, 1)
        self.localTagButton = QtWidgets.QRadioButton(self.tagTypeGroup)
        self.localTagButton.setObjectName("localTagButton")
        self.gridLayout.addWidget(self.localTagButton, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.tagTypeGroup, 3, 0, 1, 2)
        self.forceCheckBox = QtWidgets.QCheckBox(GitTagDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.gridLayout_3.addWidget(self.forceCheckBox, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitTagDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.retranslateUi(GitTagDialog)
        self.buttonBox.accepted.connect(GitTagDialog.accept)
        self.buttonBox.rejected.connect(GitTagDialog.reject)
        self.deleteTagButton.toggled['bool'].connect(self.revisionEdit.setDisabled)
        self.verifyTagButton.toggled['bool'].connect(self.revisionEdit.setDisabled)
        self.createTagButton.toggled['bool'].connect(self.tagTypeGroup.setEnabled)
        self.createTagButton.toggled['bool'].connect(self.forceCheckBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GitTagDialog)
        GitTagDialog.setTabOrder(self.tagCombo, self.revisionEdit)
        GitTagDialog.setTabOrder(self.revisionEdit, self.createTagButton)
        GitTagDialog.setTabOrder(self.createTagButton, self.deleteTagButton)
        GitTagDialog.setTabOrder(self.deleteTagButton, self.verifyTagButton)
        GitTagDialog.setTabOrder(self.verifyTagButton, self.globalTagButton)
        GitTagDialog.setTabOrder(self.globalTagButton, self.signedTagButton)
        GitTagDialog.setTabOrder(self.signedTagButton, self.localTagButton)

    def retranslateUi(self, GitTagDialog):
        _translate = QtCore.QCoreApplication.translate
        GitTagDialog.setWindowTitle(_translate("GitTagDialog", "Git Tag"))
        self.TextLabel1.setText(_translate("GitTagDialog", "Name:"))
        self.tagCombo.setToolTip(_translate("GitTagDialog", "Enter the name of the tag"))
        self.tagCombo.setWhatsThis(_translate("GitTagDialog", "<b>Tag Name</b>\n"
"<p>Enter the name of the tag to be created, deleted or verified.</p>"))
        self.label.setText(_translate("GitTagDialog", "Revision:"))
        self.revisionEdit.setToolTip(_translate("GitTagDialog", "Enter a revision to set a tag for"))
        self.tagActionGroup.setTitle(_translate("GitTagDialog", "Tag Action"))
        self.createTagButton.setToolTip(_translate("GitTagDialog", "Select to create a tag"))
        self.createTagButton.setWhatsThis(_translate("GitTagDialog", "<b>Create Tag</b>\n"
"<p>Select this entry in order to create a tag.</p>"))
        self.createTagButton.setText(_translate("GitTagDialog", "Create Tag"))
        self.deleteTagButton.setToolTip(_translate("GitTagDialog", "Select to delete a tag"))
        self.deleteTagButton.setWhatsThis(_translate("GitTagDialog", "<b>Delete Tag</b>\n"
"<p>Select this entry in order to delete the selected tag.</p>"))
        self.deleteTagButton.setText(_translate("GitTagDialog", "Delete Tag"))
        self.verifyTagButton.setToolTip(_translate("GitTagDialog", "Select to verify a tag"))
        self.verifyTagButton.setWhatsThis(_translate("GitTagDialog", "<b>Verify Tag</b>\n"
"<p>Select this entry in order to verify the selected tag.</p>"))
        self.verifyTagButton.setText(_translate("GitTagDialog", "Verify Tag"))
        self.tagTypeGroup.setTitle(_translate("GitTagDialog", "Tag Type"))
        self.globalTagButton.setToolTip(_translate("GitTagDialog", "Select to create/delete/verify a global tag"))
        self.globalTagButton.setText(_translate("GitTagDialog", "Global Tag"))
        self.signedTagButton.setToolTip(_translate("GitTagDialog", "Select to create/delete/verify a signed tag"))
        self.signedTagButton.setText(_translate("GitTagDialog", "Signed Tag"))
        self.localTagButton.setToolTip(_translate("GitTagDialog", "Select to create/delete/verify a local tag"))
        self.localTagButton.setText(_translate("GitTagDialog", "Local Tag"))
        self.forceCheckBox.setToolTip(_translate("GitTagDialog", "Select to enforce the create operation"))
        self.forceCheckBox.setText(_translate("GitTagDialog", "Enforce Operation"))
