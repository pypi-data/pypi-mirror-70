# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/GraphicsPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GraphicsPage(object):
    def setupUi(self, GraphicsPage):
        GraphicsPage.setObjectName("GraphicsPage")
        GraphicsPage.resize(440, 334)
        self.verticalLayout = QtWidgets.QVBoxLayout(GraphicsPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(GraphicsPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line7 = QtWidgets.QFrame(GraphicsPage)
        self.line7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line7.setObjectName("line7")
        self.verticalLayout.addWidget(self.line7)
        self.groupBox_2 = QtWidgets.QGroupBox(GraphicsPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsFontButton = QtWidgets.QPushButton(self.groupBox_2)
        self.graphicsFontButton.setObjectName("graphicsFontButton")
        self.horizontalLayout.addWidget(self.graphicsFontButton)
        self.graphicsFontSample = QtWidgets.QLineEdit(self.groupBox_2)
        self.graphicsFontSample.setFocusPolicy(QtCore.Qt.NoFocus)
        self.graphicsFontSample.setAlignment(QtCore.Qt.AlignHCenter)
        self.graphicsFontSample.setReadOnly(True)
        self.graphicsFontSample.setObjectName("graphicsFontSample")
        self.horizontalLayout.addWidget(self.graphicsFontSample)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(GraphicsPage)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.automaticButton = QtWidgets.QRadioButton(self.groupBox)
        self.automaticButton.setChecked(True)
        self.automaticButton.setObjectName("automaticButton")
        self.horizontalLayout_2.addWidget(self.automaticButton)
        self.blackWhiteButton = QtWidgets.QRadioButton(self.groupBox)
        self.blackWhiteButton.setObjectName("blackWhiteButton")
        self.horizontalLayout_2.addWidget(self.blackWhiteButton)
        self.whiteBlackButton = QtWidgets.QRadioButton(self.groupBox)
        self.whiteBlackButton.setObjectName("whiteBlackButton")
        self.horizontalLayout_2.addWidget(self.whiteBlackButton)
        spacerItem = QtWidgets.QSpacerItem(53, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(GraphicsPage)
        QtCore.QMetaObject.connectSlotsByName(GraphicsPage)
        GraphicsPage.setTabOrder(self.graphicsFontButton, self.blackWhiteButton)
        GraphicsPage.setTabOrder(self.blackWhiteButton, self.whiteBlackButton)

    def retranslateUi(self, GraphicsPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("GraphicsPage", "<b>Configure graphics settings</b>"))
        self.groupBox_2.setTitle(_translate("GraphicsPage", "Font"))
        self.graphicsFontButton.setToolTip(_translate("GraphicsPage", "Press to select the font for the graphic items"))
        self.graphicsFontButton.setText(_translate("GraphicsPage", "Graphics Font"))
        self.graphicsFontSample.setText(_translate("GraphicsPage", "Graphics Font"))
        self.groupBox.setTitle(_translate("GraphicsPage", "Drawing Mode"))
        self.automaticButton.setToolTip(_translate("GraphicsPage", "Select to determine the drawing mode automatically"))
        self.automaticButton.setText(_translate("GraphicsPage", "Automatic"))
        self.blackWhiteButton.setToolTip(_translate("GraphicsPage", "Select to draw black shapes on a white background"))
        self.blackWhiteButton.setText(_translate("GraphicsPage", "Black On White"))
        self.whiteBlackButton.setToolTip(_translate("GraphicsPage", "Select to draw white shapes on a black background"))
        self.whiteBlackButton.setText(_translate("GraphicsPage", "White On Black"))
