# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Tasks/TaskFilterConfigDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TaskFilterConfigDialog(object):
    def setupUi(self, TaskFilterConfigDialog):
        TaskFilterConfigDialog.setObjectName("TaskFilterConfigDialog")
        TaskFilterConfigDialog.resize(562, 405)
        TaskFilterConfigDialog.setSizeGripEnabled(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(TaskFilterConfigDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(TaskFilterConfigDialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.summaryGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.summaryGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.summaryGroup.setCheckable(True)
        self.summaryGroup.setObjectName("summaryGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.summaryGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.summaryEdit = QtWidgets.QLineEdit(self.summaryGroup)
        self.summaryEdit.setObjectName("summaryEdit")
        self.verticalLayout.addWidget(self.summaryEdit)
        self.verticalLayout_4.addWidget(self.summaryGroup)
        self.filenameGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.filenameGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.filenameGroup.setCheckable(True)
        self.filenameGroup.setObjectName("filenameGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.filenameGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filenameEdit = QtWidgets.QLineEdit(self.filenameGroup)
        self.filenameEdit.setObjectName("filenameEdit")
        self.verticalLayout_2.addWidget(self.filenameEdit)
        self.verticalLayout_4.addWidget(self.filenameGroup)
        self.typeGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.typeGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.typeGroup.setCheckable(True)
        self.typeGroup.setObjectName("typeGroup")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.typeGroup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.typeCombo = QtWidgets.QComboBox(self.typeGroup)
        self.typeCombo.setObjectName("typeCombo")
        self.verticalLayout_3.addWidget(self.typeCombo)
        self.verticalLayout_4.addWidget(self.typeGroup)
        self.scopeGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.scopeGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.scopeGroup.setCheckable(True)
        self.scopeGroup.setObjectName("scopeGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scopeGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.globalRadioButton = QtWidgets.QRadioButton(self.scopeGroup)
        self.globalRadioButton.setObjectName("globalRadioButton")
        self.horizontalLayout.addWidget(self.globalRadioButton)
        self.projectRadioButton = QtWidgets.QRadioButton(self.scopeGroup)
        self.projectRadioButton.setObjectName("projectRadioButton")
        self.horizontalLayout.addWidget(self.projectRadioButton)
        self.verticalLayout_4.addWidget(self.scopeGroup)
        self.statusGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.statusGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.statusGroup.setCheckable(True)
        self.statusGroup.setObjectName("statusGroup")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.statusGroup)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uncompletedRadioButton = QtWidgets.QRadioButton(self.statusGroup)
        self.uncompletedRadioButton.setObjectName("uncompletedRadioButton")
        self.horizontalLayout_2.addWidget(self.uncompletedRadioButton)
        self.completedRadioButton = QtWidgets.QRadioButton(self.statusGroup)
        self.completedRadioButton.setObjectName("completedRadioButton")
        self.horizontalLayout_2.addWidget(self.completedRadioButton)
        self.verticalLayout_4.addWidget(self.statusGroup)
        self.priorityGroup = QtWidgets.QGroupBox(TaskFilterConfigDialog)
        self.priorityGroup.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.priorityGroup.setCheckable(True)
        self.priorityGroup.setObjectName("priorityGroup")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.priorityGroup)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.priorityHighCheckBox = QtWidgets.QCheckBox(self.priorityGroup)
        self.priorityHighCheckBox.setObjectName("priorityHighCheckBox")
        self.horizontalLayout_3.addWidget(self.priorityHighCheckBox)
        self.priorityNormalCheckBox = QtWidgets.QCheckBox(self.priorityGroup)
        self.priorityNormalCheckBox.setObjectName("priorityNormalCheckBox")
        self.horizontalLayout_3.addWidget(self.priorityNormalCheckBox)
        self.priorityLowCheckBox = QtWidgets.QCheckBox(self.priorityGroup)
        self.priorityLowCheckBox.setObjectName("priorityLowCheckBox")
        self.horizontalLayout_3.addWidget(self.priorityLowCheckBox)
        self.verticalLayout_4.addWidget(self.priorityGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(TaskFilterConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(TaskFilterConfigDialog)
        self.buttonBox.accepted.connect(TaskFilterConfigDialog.accept)
        self.buttonBox.rejected.connect(TaskFilterConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TaskFilterConfigDialog)
        TaskFilterConfigDialog.setTabOrder(self.summaryGroup, self.summaryEdit)
        TaskFilterConfigDialog.setTabOrder(self.summaryEdit, self.filenameGroup)
        TaskFilterConfigDialog.setTabOrder(self.filenameGroup, self.filenameEdit)
        TaskFilterConfigDialog.setTabOrder(self.filenameEdit, self.typeGroup)
        TaskFilterConfigDialog.setTabOrder(self.typeGroup, self.typeCombo)
        TaskFilterConfigDialog.setTabOrder(self.typeCombo, self.scopeGroup)
        TaskFilterConfigDialog.setTabOrder(self.scopeGroup, self.globalRadioButton)
        TaskFilterConfigDialog.setTabOrder(self.globalRadioButton, self.projectRadioButton)
        TaskFilterConfigDialog.setTabOrder(self.projectRadioButton, self.statusGroup)
        TaskFilterConfigDialog.setTabOrder(self.statusGroup, self.uncompletedRadioButton)
        TaskFilterConfigDialog.setTabOrder(self.uncompletedRadioButton, self.completedRadioButton)
        TaskFilterConfigDialog.setTabOrder(self.completedRadioButton, self.priorityGroup)
        TaskFilterConfigDialog.setTabOrder(self.priorityGroup, self.priorityHighCheckBox)
        TaskFilterConfigDialog.setTabOrder(self.priorityHighCheckBox, self.priorityNormalCheckBox)
        TaskFilterConfigDialog.setTabOrder(self.priorityNormalCheckBox, self.priorityLowCheckBox)
        TaskFilterConfigDialog.setTabOrder(self.priorityLowCheckBox, self.buttonBox)

    def retranslateUi(self, TaskFilterConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        TaskFilterConfigDialog.setWindowTitle(_translate("TaskFilterConfigDialog", "Task filter configuration"))
        self.label.setText(_translate("TaskFilterConfigDialog", "Select the categories, the tasks list should be filtered on. Within each category, enter the selection criteria. The enabled categories are combined using an \"<b>and</b>\" operation."))
        self.summaryGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task summary"))
        self.summaryGroup.setTitle(_translate("TaskFilterConfigDialog", "Summary"))
        self.summaryEdit.setToolTip(_translate("TaskFilterConfigDialog", "Enter the summary filter as a regular expression."))
        self.filenameGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task filename"))
        self.filenameGroup.setTitle(_translate("TaskFilterConfigDialog", "Filename"))
        self.filenameEdit.setToolTip(_translate("TaskFilterConfigDialog", "Enter the filename filter as a wildcard expression."))
        self.typeGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task type"))
        self.typeGroup.setTitle(_translate("TaskFilterConfigDialog", "Type"))
        self.typeCombo.setToolTip(_translate("TaskFilterConfigDialog", "Select the task type to be shown"))
        self.scopeGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task scope"))
        self.scopeGroup.setTitle(_translate("TaskFilterConfigDialog", "Scope"))
        self.globalRadioButton.setToolTip(_translate("TaskFilterConfigDialog", "Select to show global tasks only"))
        self.globalRadioButton.setText(_translate("TaskFilterConfigDialog", "Global tasks"))
        self.projectRadioButton.setToolTip(_translate("TaskFilterConfigDialog", "Select to show project tasks only"))
        self.projectRadioButton.setText(_translate("TaskFilterConfigDialog", "Project tasks"))
        self.statusGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task completion status"))
        self.statusGroup.setTitle(_translate("TaskFilterConfigDialog", "Completion status"))
        self.uncompletedRadioButton.setToolTip(_translate("TaskFilterConfigDialog", "Select to show uncompleted tasks only"))
        self.uncompletedRadioButton.setText(_translate("TaskFilterConfigDialog", "Uncompleted tasks"))
        self.completedRadioButton.setToolTip(_translate("TaskFilterConfigDialog", "Select to show completed tasks only"))
        self.completedRadioButton.setText(_translate("TaskFilterConfigDialog", "Completed tasks"))
        self.priorityGroup.setToolTip(_translate("TaskFilterConfigDialog", "Select to filter on the task priority"))
        self.priorityGroup.setTitle(_translate("TaskFilterConfigDialog", "Priority"))
        self.priorityHighCheckBox.setToolTip(_translate("TaskFilterConfigDialog", "Select to show high priority tasks"))
        self.priorityHighCheckBox.setText(_translate("TaskFilterConfigDialog", "High priority tasks"))
        self.priorityNormalCheckBox.setToolTip(_translate("TaskFilterConfigDialog", "Select to show normal priority tasks"))
        self.priorityNormalCheckBox.setText(_translate("TaskFilterConfigDialog", "Normal priority tasks"))
        self.priorityLowCheckBox.setToolTip(_translate("TaskFilterConfigDialog", "Select to show low priority tasks"))
        self.priorityLowCheckBox.setText(_translate("TaskFilterConfigDialog", "Low priority tasks"))
