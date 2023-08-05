# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Plugins/VcsPlugins/vcsMercurial/HgBookmarksListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgBookmarksListDialog(object):
    def setupUi(self, HgBookmarksListDialog):
        HgBookmarksListDialog.setObjectName("HgBookmarksListDialog")
        HgBookmarksListDialog.resize(634, 494)
        HgBookmarksListDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(HgBookmarksListDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.bookmarksList = QtWidgets.QTreeWidget(HgBookmarksListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.bookmarksList.sizePolicy().hasHeightForWidth())
        self.bookmarksList.setSizePolicy(sizePolicy)
        self.bookmarksList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.bookmarksList.setAlternatingRowColors(True)
        self.bookmarksList.setRootIsDecorated(False)
        self.bookmarksList.setItemsExpandable(False)
        self.bookmarksList.setObjectName("bookmarksList")
        self.vboxlayout.addWidget(self.bookmarksList)
        self.errorGroup = QtWidgets.QGroupBox(HgBookmarksListDialog)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(HgBookmarksListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(HgBookmarksListDialog)
        QtCore.QMetaObject.connectSlotsByName(HgBookmarksListDialog)
        HgBookmarksListDialog.setTabOrder(self.bookmarksList, self.errors)
        HgBookmarksListDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, HgBookmarksListDialog):
        _translate = QtCore.QCoreApplication.translate
        HgBookmarksListDialog.setWindowTitle(_translate("HgBookmarksListDialog", "Mercurial Bookmarks"))
        HgBookmarksListDialog.setWhatsThis(_translate("HgBookmarksListDialog", "<b>Mercurial Bookmarks</b>\n"
"<p>This dialog shows a list of the projects bookmarks.</p>"))
        self.bookmarksList.setWhatsThis(_translate("HgBookmarksListDialog", "<b>Bookmarks List</b>\n"
"<p>This shows a list of the projects bookmarks.</p>"))
        self.bookmarksList.setSortingEnabled(True)
        self.bookmarksList.headerItem().setText(0, _translate("HgBookmarksListDialog", "Revision"))
        self.bookmarksList.headerItem().setText(1, _translate("HgBookmarksListDialog", "Changeset"))
        self.bookmarksList.headerItem().setText(2, _translate("HgBookmarksListDialog", "Status"))
        self.bookmarksList.headerItem().setText(3, _translate("HgBookmarksListDialog", "Name"))
        self.errorGroup.setTitle(_translate("HgBookmarksListDialog", "Errors"))
