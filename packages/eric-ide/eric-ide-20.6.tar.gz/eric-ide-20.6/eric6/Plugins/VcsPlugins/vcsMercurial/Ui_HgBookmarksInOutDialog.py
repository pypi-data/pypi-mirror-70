# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsMercurial/HgBookmarksInOutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgBookmarksInOutDialog(object):
    def setupUi(self, HgBookmarksInOutDialog):
        HgBookmarksInOutDialog.setObjectName("HgBookmarksInOutDialog")
        HgBookmarksInOutDialog.resize(520, 494)
        HgBookmarksInOutDialog.setWindowTitle("")
        HgBookmarksInOutDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(HgBookmarksInOutDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.bookmarksList = QtWidgets.QTreeWidget(HgBookmarksInOutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.bookmarksList.sizePolicy().hasHeightForWidth())
        self.bookmarksList.setSizePolicy(sizePolicy)
        self.bookmarksList.setAlternatingRowColors(True)
        self.bookmarksList.setRootIsDecorated(False)
        self.bookmarksList.setItemsExpandable(False)
        self.bookmarksList.setObjectName("bookmarksList")
        self.vboxlayout.addWidget(self.bookmarksList)
        self.errorGroup = QtWidgets.QGroupBox(HgBookmarksInOutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.vboxlayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgBookmarksInOutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(HgBookmarksInOutDialog)
        QtCore.QMetaObject.connectSlotsByName(HgBookmarksInOutDialog)
        HgBookmarksInOutDialog.setTabOrder(self.bookmarksList, self.errors)
        HgBookmarksInOutDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, HgBookmarksInOutDialog):
        _translate = QtCore.QCoreApplication.translate
        self.bookmarksList.setWhatsThis(_translate("HgBookmarksInOutDialog", "<b>Bookmarks List</b>\n"
"<p>This shows a list of the bookmarks.</p>"))
        self.bookmarksList.setSortingEnabled(True)
        self.bookmarksList.headerItem().setText(0, _translate("HgBookmarksInOutDialog", "Name"))
        self.bookmarksList.headerItem().setText(1, _translate("HgBookmarksInOutDialog", "Changeset"))
        self.errorGroup.setTitle(_translate("HgBookmarksInOutDialog", "Errors"))
