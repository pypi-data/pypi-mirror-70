# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/E5Network/E5SslCertificateSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_E5SslCertificateSelectionDialog(object):
    def setupUi(self, E5SslCertificateSelectionDialog):
        E5SslCertificateSelectionDialog.setObjectName("E5SslCertificateSelectionDialog")
        E5SslCertificateSelectionDialog.resize(760, 440)
        E5SslCertificateSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5SslCertificateSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(E5SslCertificateSelectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.certificatesTree = QtWidgets.QTreeWidget(E5SslCertificateSelectionDialog)
        self.certificatesTree.setObjectName("certificatesTree")
        self.verticalLayout.addWidget(self.certificatesTree)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.viewButton = QtWidgets.QPushButton(E5SslCertificateSelectionDialog)
        self.viewButton.setEnabled(False)
        self.viewButton.setObjectName("viewButton")
        self.horizontalLayout.addWidget(self.viewButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5SslCertificateSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5SslCertificateSelectionDialog)
        self.buttonBox.accepted.connect(E5SslCertificateSelectionDialog.accept)
        self.buttonBox.rejected.connect(E5SslCertificateSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(E5SslCertificateSelectionDialog)

    def retranslateUi(self, E5SslCertificateSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        E5SslCertificateSelectionDialog.setWindowTitle(_translate("E5SslCertificateSelectionDialog", "SSL Certificate Selection"))
        self.label.setText(_translate("E5SslCertificateSelectionDialog", "Select a SSL certificate:"))
        self.certificatesTree.headerItem().setText(0, _translate("E5SslCertificateSelectionDialog", "Certificate name"))
        self.certificatesTree.headerItem().setText(1, _translate("E5SslCertificateSelectionDialog", "Expiry Date"))
        self.viewButton.setToolTip(_translate("E5SslCertificateSelectionDialog", "Press to view the selected certificate"))
        self.viewButton.setText(_translate("E5SslCertificateSelectionDialog", "&View..."))
