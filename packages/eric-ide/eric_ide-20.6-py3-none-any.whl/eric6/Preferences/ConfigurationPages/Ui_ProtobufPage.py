# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/ProtobufPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProtobufPage(object):
    def setupUi(self, ProtobufPage):
        ProtobufPage.setObjectName("ProtobufPage")
        ProtobufPage.resize(589, 490)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProtobufPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(ProtobufPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line13 = QtWidgets.QFrame(ProtobufPage)
        self.line13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line13.setObjectName("line13")
        self.verticalLayout.addWidget(self.line13)
        self.groupBox_2 = QtWidgets.QGroupBox(ProtobufPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.protocPicker = E5PathPicker(self.groupBox_2)
        self.protocPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.protocPicker.setObjectName("protocPicker")
        self.verticalLayout_2.addWidget(self.protocPicker)
        self.textLabel1_5 = QtWidgets.QLabel(self.groupBox_2)
        self.textLabel1_5.setObjectName("textLabel1_5")
        self.verticalLayout_2.addWidget(self.textLabel1_5)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(ProtobufPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.grpcPythonPicker = E5PathPicker(self.groupBox_3)
        self.grpcPythonPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.grpcPythonPicker.setObjectName("grpcPythonPicker")
        self.verticalLayout_3.addWidget(self.grpcPythonPicker)
        self.textLabel1_6 = QtWidgets.QLabel(self.groupBox_3)
        self.textLabel1_6.setObjectName("textLabel1_6")
        self.verticalLayout_3.addWidget(self.textLabel1_6)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem = QtWidgets.QSpacerItem(20, 81, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ProtobufPage)
        QtCore.QMetaObject.connectSlotsByName(ProtobufPage)

    def retranslateUi(self, ProtobufPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("ProtobufPage", "<b>Configure Protobuf support</b>"))
        self.groupBox_2.setTitle(_translate("ProtobufPage", "Protobuf Compiler"))
        self.protocPicker.setToolTip(_translate("ProtobufPage", "Enter the path to the protobuf compiler."))
        self.textLabel1_5.setText(_translate("ProtobufPage", "<b>Note:</b> Leave this entry empty to use the default value (protoc or protoc.exe)."))
        self.groupBox_3.setTitle(_translate("ProtobufPage", "gRPC Compiler"))
        self.grpcPythonPicker.setToolTip(_translate("ProtobufPage", "Enter the path of the Python interpreter containing the gRPC compiler."))
        self.textLabel1_6.setText(_translate("ProtobufPage", "<b>Note:</b> Leave this entry empty to use the Python interpreter of eric."))
from E5Gui.E5PathPicker import E5PathPicker
