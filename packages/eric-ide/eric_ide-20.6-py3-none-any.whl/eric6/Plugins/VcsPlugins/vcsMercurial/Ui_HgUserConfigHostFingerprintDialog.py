# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsMercurial/HgUserConfigHostFingerprintDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgUserConfigHostFingerprintDialog(object):
    def setupUi(self, HgUserConfigHostFingerprintDialog):
        HgUserConfigHostFingerprintDialog.setObjectName("HgUserConfigHostFingerprintDialog")
        HgUserConfigHostFingerprintDialog.resize(600, 144)
        HgUserConfigHostFingerprintDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(HgUserConfigHostFingerprintDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(HgUserConfigHostFingerprintDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.hostEdit = E5ClearableLineEdit(HgUserConfigHostFingerprintDialog)
        self.hostEdit.setObjectName("hostEdit")
        self.gridLayout.addWidget(self.hostEdit, 0, 1, 1, 1)
        self.hashLabel = QtWidgets.QLabel(HgUserConfigHostFingerprintDialog)
        self.hashLabel.setObjectName("hashLabel")
        self.gridLayout.addWidget(self.hashLabel, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hashComboBox = QtWidgets.QComboBox(HgUserConfigHostFingerprintDialog)
        self.hashComboBox.setObjectName("hashComboBox")
        self.horizontalLayout.addWidget(self.hashComboBox)
        spacerItem = QtWidgets.QSpacerItem(178, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(HgUserConfigHostFingerprintDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.fingerprintEdit = E5ClearableLineEdit(HgUserConfigHostFingerprintDialog)
        self.fingerprintEdit.setObjectName("fingerprintEdit")
        self.gridLayout.addWidget(self.fingerprintEdit, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgUserConfigHostFingerprintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(HgUserConfigHostFingerprintDialog)
        self.buttonBox.accepted.connect(HgUserConfigHostFingerprintDialog.accept)
        self.buttonBox.rejected.connect(HgUserConfigHostFingerprintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HgUserConfigHostFingerprintDialog)
        HgUserConfigHostFingerprintDialog.setTabOrder(self.hostEdit, self.hashComboBox)
        HgUserConfigHostFingerprintDialog.setTabOrder(self.hashComboBox, self.fingerprintEdit)

    def retranslateUi(self, HgUserConfigHostFingerprintDialog):
        _translate = QtCore.QCoreApplication.translate
        HgUserConfigHostFingerprintDialog.setWindowTitle(_translate("HgUserConfigHostFingerprintDialog", "Host Fingerprint"))
        self.label.setText(_translate("HgUserConfigHostFingerprintDialog", "Host:"))
        self.hostEdit.setToolTip(_translate("HgUserConfigHostFingerprintDialog", "Enter the host name"))
        self.hostEdit.setPlaceholderText(_translate("HgUserConfigHostFingerprintDialog", "Enter Hostname"))
        self.hashLabel.setText(_translate("HgUserConfigHostFingerprintDialog", "Hash Type:"))
        self.label_2.setText(_translate("HgUserConfigHostFingerprintDialog", "Fingerprint:"))
        self.fingerprintEdit.setToolTip(_translate("HgUserConfigHostFingerprintDialog", "Enter the host fingerprint"))
        self.fingerprintEdit.setPlaceholderText(_translate("HgUserConfigHostFingerprintDialog", "Enter Fingerprint"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
