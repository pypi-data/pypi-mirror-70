# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsGit/GitBranchDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitBranchDialog(object):
    def setupUi(self, GitBranchDialog):
        GitBranchDialog.setObjectName("GitBranchDialog")
        GitBranchDialog.resize(391, 499)
        GitBranchDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitBranchDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tagActionGroup = QtWidgets.QGroupBox(GitBranchDialog)
        self.tagActionGroup.setObjectName("tagActionGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.tagActionGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.createBranchButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.createBranchButton.setChecked(True)
        self.createBranchButton.setObjectName("createBranchButton")
        self.gridLayout.addWidget(self.createBranchButton, 0, 0, 1, 1)
        self.moveBranchButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.moveBranchButton.setObjectName("moveBranchButton")
        self.gridLayout.addWidget(self.moveBranchButton, 0, 1, 1, 1)
        self.deleteBranchButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.deleteBranchButton.setObjectName("deleteBranchButton")
        self.gridLayout.addWidget(self.deleteBranchButton, 0, 2, 1, 1)
        self.createSwitchButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.createSwitchButton.setObjectName("createSwitchButton")
        self.gridLayout.addWidget(self.createSwitchButton, 1, 0, 1, 3)
        self.createTrackingButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.createTrackingButton.setObjectName("createTrackingButton")
        self.gridLayout.addWidget(self.createTrackingButton, 2, 0, 1, 3)
        self.setTrackingButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.setTrackingButton.setObjectName("setTrackingButton")
        self.gridLayout.addWidget(self.setTrackingButton, 3, 0, 1, 3)
        self.unsetTrackingButton = QtWidgets.QRadioButton(self.tagActionGroup)
        self.unsetTrackingButton.setObjectName("unsetTrackingButton")
        self.gridLayout.addWidget(self.unsetTrackingButton, 4, 0, 1, 3)
        self.verticalLayout.addWidget(self.tagActionGroup)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TextLabel1 = QtWidgets.QLabel(GitBranchDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.horizontalLayout_3.addWidget(self.TextLabel1)
        self.branchCombo = QtWidgets.QComboBox(GitBranchDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchCombo.sizePolicy().hasHeightForWidth())
        self.branchCombo.setSizePolicy(sizePolicy)
        self.branchCombo.setEditable(True)
        self.branchCombo.setDuplicatesEnabled(False)
        self.branchCombo.setObjectName("branchCombo")
        self.horizontalLayout_3.addWidget(self.branchCombo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.createBranchGroup = QtWidgets.QGroupBox(GitBranchDialog)
        self.createBranchGroup.setObjectName("createBranchGroup")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.createBranchGroup)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.createBranchGroup)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.revisionEdit = QtWidgets.QLineEdit(self.createBranchGroup)
        self.revisionEdit.setObjectName("revisionEdit")
        self.horizontalLayout_2.addWidget(self.revisionEdit)
        self.verticalLayout.addWidget(self.createBranchGroup)
        self.moveBranchGroup = QtWidgets.QGroupBox(GitBranchDialog)
        self.moveBranchGroup.setEnabled(False)
        self.moveBranchGroup.setObjectName("moveBranchGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.moveBranchGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.moveBranchGroup)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.newBranchNameEdit = QtWidgets.QLineEdit(self.moveBranchGroup)
        self.newBranchNameEdit.setObjectName("newBranchNameEdit")
        self.horizontalLayout.addWidget(self.newBranchNameEdit)
        self.verticalLayout.addWidget(self.moveBranchGroup)
        self.trackingBranchGroup = QtWidgets.QGroupBox(GitBranchDialog)
        self.trackingBranchGroup.setEnabled(False)
        self.trackingBranchGroup.setObjectName("trackingBranchGroup")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.trackingBranchGroup)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.trackingBranchGroup)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.remoteBranchCombo = QtWidgets.QComboBox(self.trackingBranchGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remoteBranchCombo.sizePolicy().hasHeightForWidth())
        self.remoteBranchCombo.setSizePolicy(sizePolicy)
        self.remoteBranchCombo.setObjectName("remoteBranchCombo")
        self.horizontalLayout_4.addWidget(self.remoteBranchCombo)
        self.verticalLayout.addWidget(self.trackingBranchGroup)
        self.forceCheckBox = QtWidgets.QCheckBox(GitBranchDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.verticalLayout.addWidget(self.forceCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitBranchDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitBranchDialog)
        self.buttonBox.accepted.connect(GitBranchDialog.accept)
        self.buttonBox.rejected.connect(GitBranchDialog.reject)
        self.createBranchButton.toggled['bool'].connect(self.createBranchGroup.setEnabled)
        self.moveBranchButton.toggled['bool'].connect(self.moveBranchGroup.setEnabled)
        self.createSwitchButton.toggled['bool'].connect(self.createBranchGroup.setEnabled)
        self.createTrackingButton.toggled['bool'].connect(self.forceCheckBox.setDisabled)
        self.setTrackingButton.toggled['bool'].connect(self.trackingBranchGroup.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GitBranchDialog)
        GitBranchDialog.setTabOrder(self.createBranchButton, self.moveBranchButton)
        GitBranchDialog.setTabOrder(self.moveBranchButton, self.deleteBranchButton)
        GitBranchDialog.setTabOrder(self.deleteBranchButton, self.createSwitchButton)
        GitBranchDialog.setTabOrder(self.createSwitchButton, self.createTrackingButton)
        GitBranchDialog.setTabOrder(self.createTrackingButton, self.setTrackingButton)
        GitBranchDialog.setTabOrder(self.setTrackingButton, self.unsetTrackingButton)
        GitBranchDialog.setTabOrder(self.unsetTrackingButton, self.branchCombo)
        GitBranchDialog.setTabOrder(self.branchCombo, self.revisionEdit)
        GitBranchDialog.setTabOrder(self.revisionEdit, self.newBranchNameEdit)
        GitBranchDialog.setTabOrder(self.newBranchNameEdit, self.remoteBranchCombo)
        GitBranchDialog.setTabOrder(self.remoteBranchCombo, self.forceCheckBox)

    def retranslateUi(self, GitBranchDialog):
        _translate = QtCore.QCoreApplication.translate
        GitBranchDialog.setWindowTitle(_translate("GitBranchDialog", "Git Branch"))
        self.tagActionGroup.setTitle(_translate("GitBranchDialog", "Branch Action"))
        self.createBranchButton.setToolTip(_translate("GitBranchDialog", "Select to create a branch"))
        self.createBranchButton.setWhatsThis(_translate("GitBranchDialog", "<b>Create Branch</b>\n"
"<p>Select this entry in order to create a branch.</p>"))
        self.createBranchButton.setText(_translate("GitBranchDialog", "Create"))
        self.moveBranchButton.setToolTip(_translate("GitBranchDialog", "Select to rename a branch"))
        self.moveBranchButton.setWhatsThis(_translate("GitBranchDialog", "<b>Rename</b>\n"
"<p>Select this entry in order to rename the selected branch.</p>"))
        self.moveBranchButton.setText(_translate("GitBranchDialog", "Rename"))
        self.deleteBranchButton.setToolTip(_translate("GitBranchDialog", "Select to delete a branch"))
        self.deleteBranchButton.setWhatsThis(_translate("GitBranchDialog", "<b>Delete Branch</b>\n"
"<p>Select this entry in order to delete the selected branch.</p>"))
        self.deleteBranchButton.setText(_translate("GitBranchDialog", "Delete"))
        self.createSwitchButton.setToolTip(_translate("GitBranchDialog", "Select to create a new branch and switch to it"))
        self.createSwitchButton.setWhatsThis(_translate("GitBranchDialog", "<b>Create &amp; Switch</b>\\n<p>Select this entry in order to create a new branch and switch the working tree to it.</p>"))
        self.createSwitchButton.setText(_translate("GitBranchDialog", "Create && Switch"))
        self.createTrackingButton.setToolTip(_translate("GitBranchDialog", "Select to create a tracking branch and switch to it"))
        self.createTrackingButton.setWhatsThis(_translate("GitBranchDialog", "<b>Create Tracking Branch &amp; Switch</b>\\n<p>Select this entry in order to create a new branch tracking a remote repository branch. The working tree is switched to it.</p>"))
        self.createTrackingButton.setText(_translate("GitBranchDialog", "Create Tracking Branch && Switch"))
        self.setTrackingButton.setToolTip(_translate("GitBranchDialog", "Select to associate a remote branch"))
        self.setTrackingButton.setText(_translate("GitBranchDialog", "Set Tracking Branch"))
        self.unsetTrackingButton.setToolTip(_translate("GitBranchDialog", "Select to de-associate a remote branch"))
        self.unsetTrackingButton.setText(_translate("GitBranchDialog", "Unset Tracking Branch Information"))
        self.TextLabel1.setText(_translate("GitBranchDialog", "Name:"))
        self.branchCombo.setToolTip(_translate("GitBranchDialog", "Enter the name of the branch"))
        self.branchCombo.setWhatsThis(_translate("GitBranchDialog", "<b>Branch Name</b>\n"
"<p>Enter the name of the branch to be created, deleted or moved.</p>"))
        self.createBranchGroup.setTitle(_translate("GitBranchDialog", "Create Branch"))
        self.label.setText(_translate("GitBranchDialog", "Revision:"))
        self.revisionEdit.setToolTip(_translate("GitBranchDialog", "Enter a revision at which to start the branch"))
        self.moveBranchGroup.setTitle(_translate("GitBranchDialog", "Rename Branch"))
        self.label_2.setText(_translate("GitBranchDialog", "New Name:"))
        self.newBranchNameEdit.setStatusTip(_translate("GitBranchDialog", "Enter a new name for the selected branch"))
        self.trackingBranchGroup.setTitle(_translate("GitBranchDialog", "Set Tracking Branch"))
        self.label_3.setText(_translate("GitBranchDialog", "Remote Branch:"))
        self.remoteBranchCombo.setToolTip(_translate("GitBranchDialog", "Select the remote branch to associate"))
        self.forceCheckBox.setToolTip(_translate("GitBranchDialog", "Select to enforce the create operation"))
        self.forceCheckBox.setText(_translate("GitBranchDialog", "Enforce Operation"))
