# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/EditorDocViewerPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorDocViewerPage(object):
    def setupUi(self, EditorDocViewerPage):
        EditorDocViewerPage.setObjectName("EditorDocViewerPage")
        EditorDocViewerPage.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(EditorDocViewerPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerLabel = QtWidgets.QLabel(EditorDocViewerPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_2.addWidget(self.headerLabel)
        self.line2 = QtWidgets.QFrame(EditorDocViewerPage)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setObjectName("line2")
        self.verticalLayout_2.addWidget(self.line2)
        self.viewerGroupBox = QtWidgets.QGroupBox(EditorDocViewerPage)
        self.viewerGroupBox.setCheckable(True)
        self.viewerGroupBox.setObjectName("viewerGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.viewerGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parenthesisCheckBox = QtWidgets.QCheckBox(self.viewerGroupBox)
        self.parenthesisCheckBox.setObjectName("parenthesisCheckBox")
        self.verticalLayout.addWidget(self.parenthesisCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.viewerGroupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.providerComboBox = QtWidgets.QComboBox(self.viewerGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.providerComboBox.sizePolicy().hasHeightForWidth())
        self.providerComboBox.setSizePolicy(sizePolicy)
        self.providerComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.providerComboBox.setObjectName("providerComboBox")
        self.horizontalLayout.addWidget(self.providerComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.viewerGroupBox)
        self.infoLabel = QtWidgets.QLabel(EditorDocViewerPage)
        self.infoLabel.setText("")
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout_2.addWidget(self.infoLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 167, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(EditorDocViewerPage)
        QtCore.QMetaObject.connectSlotsByName(EditorDocViewerPage)
        EditorDocViewerPage.setTabOrder(self.viewerGroupBox, self.parenthesisCheckBox)
        EditorDocViewerPage.setTabOrder(self.parenthesisCheckBox, self.providerComboBox)

    def retranslateUi(self, EditorDocViewerPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorDocViewerPage", "<b>Configure Documentation Viewer Settings</b>"))
        self.viewerGroupBox.setToolTip(_translate("EditorDocViewerPage", "Select to enable the display of code documentation"))
        self.viewerGroupBox.setTitle(_translate("EditorDocViewerPage", "Enable Documentation Viewer"))
        self.parenthesisCheckBox.setToolTip(_translate("EditorDocViewerPage", "Select to show documentation when entering a \'(\' character"))
        self.parenthesisCheckBox.setText(_translate("EditorDocViewerPage", "Show documentation upon \'(\'"))
        self.label.setText(_translate("EditorDocViewerPage", "Documentation Provider:"))
        self.providerComboBox.setToolTip(_translate("EditorDocViewerPage", "Select the documentation provider to be used"))
