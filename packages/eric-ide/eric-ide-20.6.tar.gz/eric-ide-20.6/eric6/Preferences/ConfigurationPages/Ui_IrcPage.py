# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric6/Preferences/ConfigurationPages/IrcPage.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IrcPage(object):
    def setupUi(self, IrcPage):
        IrcPage.setObjectName("IrcPage")
        IrcPage.resize(522, 1022)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(IrcPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerLabel = QtWidgets.QLabel(IrcPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.line3 = QtWidgets.QFrame(IrcPage)
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setObjectName("line3")
        self.verticalLayout_3.addWidget(self.line3)
        self.timestampGroup = QtWidgets.QGroupBox(IrcPage)
        self.timestampGroup.setCheckable(True)
        self.timestampGroup.setObjectName("timestampGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.timestampGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.timestampGroup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.timeFormatCombo = QtWidgets.QComboBox(self.timestampGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeFormatCombo.sizePolicy().hasHeightForWidth())
        self.timeFormatCombo.setSizePolicy(sizePolicy)
        self.timeFormatCombo.setObjectName("timeFormatCombo")
        self.gridLayout.addWidget(self.timeFormatCombo, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.timestampGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.dateFormatCombo = QtWidgets.QComboBox(self.timestampGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateFormatCombo.sizePolicy().hasHeightForWidth())
        self.dateFormatCombo.setSizePolicy(sizePolicy)
        self.dateFormatCombo.setObjectName("dateFormatCombo")
        self.gridLayout.addWidget(self.dateFormatCombo, 0, 3, 1, 1)
        self.showDateCheckBox = QtWidgets.QCheckBox(self.timestampGroup)
        self.showDateCheckBox.setObjectName("showDateCheckBox")
        self.gridLayout.addWidget(self.showDateCheckBox, 1, 0, 1, 4)
        self.verticalLayout_3.addWidget(self.timestampGroup)
        self.coloursGroup = QtWidgets.QGroupBox(IrcPage)
        self.coloursGroup.setObjectName("coloursGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.coloursGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.coloursGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.networkButton = QtWidgets.QPushButton(self.coloursGroup)
        self.networkButton.setMinimumSize(QtCore.QSize(100, 0))
        self.networkButton.setText("")
        self.networkButton.setObjectName("networkButton")
        self.gridLayout_2.addWidget(self.networkButton, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.coloursGroup)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 2, 1, 1)
        self.nickButton = QtWidgets.QPushButton(self.coloursGroup)
        self.nickButton.setMinimumSize(QtCore.QSize(100, 0))
        self.nickButton.setText("")
        self.nickButton.setObjectName("nickButton")
        self.gridLayout_2.addWidget(self.nickButton, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.coloursGroup)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.serverButton = QtWidgets.QPushButton(self.coloursGroup)
        self.serverButton.setMinimumSize(QtCore.QSize(100, 0))
        self.serverButton.setText("")
        self.serverButton.setObjectName("serverButton")
        self.gridLayout_2.addWidget(self.serverButton, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.coloursGroup)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 1, 2, 1, 1)
        self.ownNickButton = QtWidgets.QPushButton(self.coloursGroup)
        self.ownNickButton.setMinimumSize(QtCore.QSize(100, 0))
        self.ownNickButton.setText("")
        self.ownNickButton.setObjectName("ownNickButton")
        self.gridLayout_2.addWidget(self.ownNickButton, 1, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.coloursGroup)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.channelButton = QtWidgets.QPushButton(self.coloursGroup)
        self.channelButton.setMinimumSize(QtCore.QSize(100, 0))
        self.channelButton.setText("")
        self.channelButton.setObjectName("channelButton")
        self.gridLayout_2.addWidget(self.channelButton, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.coloursGroup)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 2, 1, 1)
        self.joinButton = QtWidgets.QPushButton(self.coloursGroup)
        self.joinButton.setMinimumSize(QtCore.QSize(100, 0))
        self.joinButton.setText("")
        self.joinButton.setObjectName("joinButton")
        self.gridLayout_2.addWidget(self.joinButton, 2, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.coloursGroup)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.errorButton = QtWidgets.QPushButton(self.coloursGroup)
        self.errorButton.setMinimumSize(QtCore.QSize(100, 0))
        self.errorButton.setText("")
        self.errorButton.setObjectName("errorButton")
        self.gridLayout_2.addWidget(self.errorButton, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.coloursGroup)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 3, 2, 1, 1)
        self.leaveButton = QtWidgets.QPushButton(self.coloursGroup)
        self.leaveButton.setMinimumSize(QtCore.QSize(100, 0))
        self.leaveButton.setText("")
        self.leaveButton.setObjectName("leaveButton")
        self.gridLayout_2.addWidget(self.leaveButton, 3, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.coloursGroup)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.timestampButton = QtWidgets.QPushButton(self.coloursGroup)
        self.timestampButton.setMinimumSize(QtCore.QSize(100, 0))
        self.timestampButton.setText("")
        self.timestampButton.setObjectName("timestampButton")
        self.gridLayout_2.addWidget(self.timestampButton, 4, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.coloursGroup)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 4, 2, 1, 1)
        self.infoButton = QtWidgets.QPushButton(self.coloursGroup)
        self.infoButton.setMinimumSize(QtCore.QSize(100, 0))
        self.infoButton.setText("")
        self.infoButton.setObjectName("infoButton")
        self.gridLayout_2.addWidget(self.infoButton, 4, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.coloursGroup)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.hyperlinkButton = QtWidgets.QPushButton(self.coloursGroup)
        self.hyperlinkButton.setMinimumSize(QtCore.QSize(100, 0))
        self.hyperlinkButton.setText("")
        self.hyperlinkButton.setObjectName("hyperlinkButton")
        self.gridLayout_2.addWidget(self.hyperlinkButton, 5, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.coloursGroup)
        self.textColoursGroup = QtWidgets.QGroupBox(IrcPage)
        self.textColoursGroup.setCheckable(True)
        self.textColoursGroup.setObjectName("textColoursGroup")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.textColoursGroup)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_15 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_15.setText("0:")
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)
        self.ircColor0Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor0Button.sizePolicy().hasHeightForWidth())
        self.ircColor0Button.setSizePolicy(sizePolicy)
        self.ircColor0Button.setObjectName("ircColor0Button")
        self.gridLayout_4.addWidget(self.ircColor0Button, 0, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_19.setText("4:")
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 0, 2, 1, 1)
        self.ircColor4Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor4Button.sizePolicy().hasHeightForWidth())
        self.ircColor4Button.setSizePolicy(sizePolicy)
        self.ircColor4Button.setObjectName("ircColor4Button")
        self.gridLayout_4.addWidget(self.ircColor4Button, 0, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_23.setText("8:")
        self.label_23.setObjectName("label_23")
        self.gridLayout_4.addWidget(self.label_23, 0, 4, 1, 1)
        self.ircColor8Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor8Button.sizePolicy().hasHeightForWidth())
        self.ircColor8Button.setSizePolicy(sizePolicy)
        self.ircColor8Button.setObjectName("ircColor8Button")
        self.gridLayout_4.addWidget(self.ircColor8Button, 0, 5, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_27.setText("12:")
        self.label_27.setObjectName("label_27")
        self.gridLayout_4.addWidget(self.label_27, 0, 6, 1, 1)
        self.ircColor12Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor12Button.sizePolicy().hasHeightForWidth())
        self.ircColor12Button.setSizePolicy(sizePolicy)
        self.ircColor12Button.setObjectName("ircColor12Button")
        self.gridLayout_4.addWidget(self.ircColor12Button, 0, 7, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_16.setText("1:")
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 1, 0, 1, 1)
        self.ircColor1Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor1Button.sizePolicy().hasHeightForWidth())
        self.ircColor1Button.setSizePolicy(sizePolicy)
        self.ircColor1Button.setObjectName("ircColor1Button")
        self.gridLayout_4.addWidget(self.ircColor1Button, 1, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_20.setText("5:")
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 1, 2, 1, 1)
        self.ircColor5Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor5Button.sizePolicy().hasHeightForWidth())
        self.ircColor5Button.setSizePolicy(sizePolicy)
        self.ircColor5Button.setObjectName("ircColor5Button")
        self.gridLayout_4.addWidget(self.ircColor5Button, 1, 3, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_24.setText("9:")
        self.label_24.setObjectName("label_24")
        self.gridLayout_4.addWidget(self.label_24, 1, 4, 1, 1)
        self.ircColor9Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor9Button.sizePolicy().hasHeightForWidth())
        self.ircColor9Button.setSizePolicy(sizePolicy)
        self.ircColor9Button.setObjectName("ircColor9Button")
        self.gridLayout_4.addWidget(self.ircColor9Button, 1, 5, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_28.setText("13:")
        self.label_28.setObjectName("label_28")
        self.gridLayout_4.addWidget(self.label_28, 1, 6, 1, 1)
        self.ircColor13Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor13Button.sizePolicy().hasHeightForWidth())
        self.ircColor13Button.setSizePolicy(sizePolicy)
        self.ircColor13Button.setObjectName("ircColor13Button")
        self.gridLayout_4.addWidget(self.ircColor13Button, 1, 7, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_17.setText("2:")
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 2, 0, 1, 1)
        self.ircColor2Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor2Button.sizePolicy().hasHeightForWidth())
        self.ircColor2Button.setSizePolicy(sizePolicy)
        self.ircColor2Button.setObjectName("ircColor2Button")
        self.gridLayout_4.addWidget(self.ircColor2Button, 2, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_21.setText("6:")
        self.label_21.setObjectName("label_21")
        self.gridLayout_4.addWidget(self.label_21, 2, 2, 1, 1)
        self.ircColor6Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor6Button.sizePolicy().hasHeightForWidth())
        self.ircColor6Button.setSizePolicy(sizePolicy)
        self.ircColor6Button.setObjectName("ircColor6Button")
        self.gridLayout_4.addWidget(self.ircColor6Button, 2, 3, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_25.setText("10:")
        self.label_25.setObjectName("label_25")
        self.gridLayout_4.addWidget(self.label_25, 2, 4, 1, 1)
        self.ircColor10Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor10Button.sizePolicy().hasHeightForWidth())
        self.ircColor10Button.setSizePolicy(sizePolicy)
        self.ircColor10Button.setObjectName("ircColor10Button")
        self.gridLayout_4.addWidget(self.ircColor10Button, 2, 5, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_29.setText("14:")
        self.label_29.setObjectName("label_29")
        self.gridLayout_4.addWidget(self.label_29, 2, 6, 1, 1)
        self.ircColor14Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor14Button.sizePolicy().hasHeightForWidth())
        self.ircColor14Button.setSizePolicy(sizePolicy)
        self.ircColor14Button.setObjectName("ircColor14Button")
        self.gridLayout_4.addWidget(self.ircColor14Button, 2, 7, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_18.setText("3:")
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 3, 0, 1, 1)
        self.ircColor3Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor3Button.sizePolicy().hasHeightForWidth())
        self.ircColor3Button.setSizePolicy(sizePolicy)
        self.ircColor3Button.setObjectName("ircColor3Button")
        self.gridLayout_4.addWidget(self.ircColor3Button, 3, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_22.setText("7:")
        self.label_22.setObjectName("label_22")
        self.gridLayout_4.addWidget(self.label_22, 3, 2, 1, 1)
        self.ircColor7Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor7Button.sizePolicy().hasHeightForWidth())
        self.ircColor7Button.setSizePolicy(sizePolicy)
        self.ircColor7Button.setObjectName("ircColor7Button")
        self.gridLayout_4.addWidget(self.ircColor7Button, 3, 3, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_26.setText("11:")
        self.label_26.setObjectName("label_26")
        self.gridLayout_4.addWidget(self.label_26, 3, 4, 1, 1)
        self.ircColor11Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor11Button.sizePolicy().hasHeightForWidth())
        self.ircColor11Button.setSizePolicy(sizePolicy)
        self.ircColor11Button.setObjectName("ircColor11Button")
        self.gridLayout_4.addWidget(self.ircColor11Button, 3, 5, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.textColoursGroup)
        self.label_30.setText("15:")
        self.label_30.setObjectName("label_30")
        self.gridLayout_4.addWidget(self.label_30, 3, 6, 1, 1)
        self.ircColor15Button = QtWidgets.QPushButton(self.textColoursGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ircColor15Button.sizePolicy().hasHeightForWidth())
        self.ircColor15Button.setSizePolicy(sizePolicy)
        self.ircColor15Button.setObjectName("ircColor15Button")
        self.gridLayout_4.addWidget(self.ircColor15Button, 3, 7, 1, 1)
        self.verticalLayout_3.addWidget(self.textColoursGroup)
        self.notificationsGroup = QtWidgets.QGroupBox(IrcPage)
        self.notificationsGroup.setCheckable(True)
        self.notificationsGroup.setObjectName("notificationsGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.notificationsGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_14 = QtWidgets.QLabel(self.notificationsGroup)
        self.label_14.setWordWrap(True)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 0, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.notificationsGroup)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 2)
        self.joinLeaveCheckBox = QtWidgets.QCheckBox(self.notificationsGroup)
        self.joinLeaveCheckBox.setObjectName("joinLeaveCheckBox")
        self.gridLayout_3.addWidget(self.joinLeaveCheckBox, 2, 0, 1, 1)
        self.ownNickCheckBox = QtWidgets.QCheckBox(self.notificationsGroup)
        self.ownNickCheckBox.setObjectName("ownNickCheckBox")
        self.gridLayout_3.addWidget(self.ownNickCheckBox, 2, 1, 1, 1)
        self.messageCheckBox = QtWidgets.QCheckBox(self.notificationsGroup)
        self.messageCheckBox.setObjectName("messageCheckBox")
        self.gridLayout_3.addWidget(self.messageCheckBox, 3, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.notificationsGroup)
        self.whoGroup = QtWidgets.QGroupBox(IrcPage)
        self.whoGroup.setCheckable(True)
        self.whoGroup.setChecked(False)
        self.whoGroup.setObjectName("whoGroup")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.whoGroup)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_31 = QtWidgets.QLabel(self.whoGroup)
        self.label_31.setObjectName("label_31")
        self.gridLayout_5.addWidget(self.label_31, 0, 0, 1, 1)
        self.whoUsersSpinBox = QtWidgets.QSpinBox(self.whoGroup)
        self.whoUsersSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.whoUsersSpinBox.setMaximum(999)
        self.whoUsersSpinBox.setObjectName("whoUsersSpinBox")
        self.gridLayout_5.addWidget(self.whoUsersSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(174, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.whoGroup)
        self.label_32.setObjectName("label_32")
        self.gridLayout_5.addWidget(self.label_32, 1, 0, 1, 1)
        self.whoIntervalSpinBox = QtWidgets.QSpinBox(self.whoGroup)
        self.whoIntervalSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.whoIntervalSpinBox.setMinimum(30)
        self.whoIntervalSpinBox.setMaximum(600)
        self.whoIntervalSpinBox.setSingleStep(10)
        self.whoIntervalSpinBox.setObjectName("whoIntervalSpinBox")
        self.gridLayout_5.addWidget(self.whoIntervalSpinBox, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.whoGroup)
        self.markerGroup = QtWidgets.QGroupBox(IrcPage)
        self.markerGroup.setObjectName("markerGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.markerGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.markWhenHiddenCheckBox = QtWidgets.QCheckBox(self.markerGroup)
        self.markWhenHiddenCheckBox.setObjectName("markWhenHiddenCheckBox")
        self.verticalLayout.addWidget(self.markWhenHiddenCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_33 = QtWidgets.QLabel(self.markerGroup)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout.addWidget(self.label_33)
        self.markerForegroundButton = QtWidgets.QPushButton(self.markerGroup)
        self.markerForegroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.markerForegroundButton.setText("")
        self.markerForegroundButton.setObjectName("markerForegroundButton")
        self.horizontalLayout.addWidget(self.markerForegroundButton)
        self.label_34 = QtWidgets.QLabel(self.markerGroup)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout.addWidget(self.label_34)
        self.markerBackgroundButton = QtWidgets.QPushButton(self.markerGroup)
        self.markerBackgroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.markerBackgroundButton.setText("")
        self.markerBackgroundButton.setObjectName("markerBackgroundButton")
        self.horizontalLayout.addWidget(self.markerBackgroundButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.markerGroup)
        self.shutdownGroup = QtWidgets.QGroupBox(IrcPage)
        self.shutdownGroup.setObjectName("shutdownGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.shutdownGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.confirmShutdownCheckBox = QtWidgets.QCheckBox(self.shutdownGroup)
        self.confirmShutdownCheckBox.setObjectName("confirmShutdownCheckBox")
        self.verticalLayout_2.addWidget(self.confirmShutdownCheckBox)
        self.verticalLayout_3.addWidget(self.shutdownGroup)
        spacerItem1 = QtWidgets.QSpacerItem(20, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.retranslateUi(IrcPage)
        QtCore.QMetaObject.connectSlotsByName(IrcPage)
        IrcPage.setTabOrder(self.timestampGroup, self.timeFormatCombo)
        IrcPage.setTabOrder(self.timeFormatCombo, self.dateFormatCombo)
        IrcPage.setTabOrder(self.dateFormatCombo, self.showDateCheckBox)
        IrcPage.setTabOrder(self.showDateCheckBox, self.networkButton)
        IrcPage.setTabOrder(self.networkButton, self.serverButton)
        IrcPage.setTabOrder(self.serverButton, self.channelButton)
        IrcPage.setTabOrder(self.channelButton, self.errorButton)
        IrcPage.setTabOrder(self.errorButton, self.timestampButton)
        IrcPage.setTabOrder(self.timestampButton, self.hyperlinkButton)
        IrcPage.setTabOrder(self.hyperlinkButton, self.nickButton)
        IrcPage.setTabOrder(self.nickButton, self.ownNickButton)
        IrcPage.setTabOrder(self.ownNickButton, self.joinButton)
        IrcPage.setTabOrder(self.joinButton, self.leaveButton)
        IrcPage.setTabOrder(self.leaveButton, self.infoButton)
        IrcPage.setTabOrder(self.infoButton, self.textColoursGroup)
        IrcPage.setTabOrder(self.textColoursGroup, self.ircColor0Button)
        IrcPage.setTabOrder(self.ircColor0Button, self.ircColor1Button)
        IrcPage.setTabOrder(self.ircColor1Button, self.ircColor2Button)
        IrcPage.setTabOrder(self.ircColor2Button, self.ircColor3Button)
        IrcPage.setTabOrder(self.ircColor3Button, self.ircColor4Button)
        IrcPage.setTabOrder(self.ircColor4Button, self.ircColor5Button)
        IrcPage.setTabOrder(self.ircColor5Button, self.ircColor6Button)
        IrcPage.setTabOrder(self.ircColor6Button, self.ircColor7Button)
        IrcPage.setTabOrder(self.ircColor7Button, self.ircColor8Button)
        IrcPage.setTabOrder(self.ircColor8Button, self.ircColor9Button)
        IrcPage.setTabOrder(self.ircColor9Button, self.ircColor10Button)
        IrcPage.setTabOrder(self.ircColor10Button, self.ircColor11Button)
        IrcPage.setTabOrder(self.ircColor11Button, self.ircColor12Button)
        IrcPage.setTabOrder(self.ircColor12Button, self.ircColor13Button)
        IrcPage.setTabOrder(self.ircColor13Button, self.ircColor14Button)
        IrcPage.setTabOrder(self.ircColor14Button, self.ircColor15Button)
        IrcPage.setTabOrder(self.ircColor15Button, self.notificationsGroup)
        IrcPage.setTabOrder(self.notificationsGroup, self.joinLeaveCheckBox)
        IrcPage.setTabOrder(self.joinLeaveCheckBox, self.messageCheckBox)
        IrcPage.setTabOrder(self.messageCheckBox, self.ownNickCheckBox)
        IrcPage.setTabOrder(self.ownNickCheckBox, self.whoGroup)
        IrcPage.setTabOrder(self.whoGroup, self.whoUsersSpinBox)
        IrcPage.setTabOrder(self.whoUsersSpinBox, self.whoIntervalSpinBox)
        IrcPage.setTabOrder(self.whoIntervalSpinBox, self.markWhenHiddenCheckBox)
        IrcPage.setTabOrder(self.markWhenHiddenCheckBox, self.markerForegroundButton)
        IrcPage.setTabOrder(self.markerForegroundButton, self.markerBackgroundButton)
        IrcPage.setTabOrder(self.markerBackgroundButton, self.confirmShutdownCheckBox)

    def retranslateUi(self, IrcPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("IrcPage", "<b>Configure IRC</b>"))
        self.timestampGroup.setToolTip(_translate("IrcPage", "Enable to show timestamps"))
        self.timestampGroup.setTitle(_translate("IrcPage", "Show Timestamps"))
        self.label.setText(_translate("IrcPage", "Time Format:"))
        self.timeFormatCombo.setToolTip(_translate("IrcPage", "Select the time format to use"))
        self.label_2.setText(_translate("IrcPage", "Date Format"))
        self.dateFormatCombo.setToolTip(_translate("IrcPage", "Select the date format to use"))
        self.showDateCheckBox.setToolTip(_translate("IrcPage", "Select to show the date in timestamps"))
        self.showDateCheckBox.setText(_translate("IrcPage", "Show Date"))
        self.coloursGroup.setTitle(_translate("IrcPage", "Colors"))
        self.label_3.setText(_translate("IrcPage", "Network Messages:"))
        self.networkButton.setToolTip(_translate("IrcPage", "Select the color for network messages"))
        self.label_9.setText(_translate("IrcPage", "Nick Names:"))
        self.nickButton.setToolTip(_translate("IrcPage", "Select the color for nick names"))
        self.label_4.setText(_translate("IrcPage", "Server Messages:"))
        self.serverButton.setToolTip(_translate("IrcPage", "Select the color for server messages"))
        self.label_10.setText(_translate("IrcPage", "Own Nick Name:"))
        self.ownNickButton.setToolTip(_translate("IrcPage", "Select the color for own nick name"))
        self.label_5.setText(_translate("IrcPage", "Channel Messages:"))
        self.channelButton.setToolTip(_translate("IrcPage", "Select the color for channel messages"))
        self.label_11.setText(_translate("IrcPage", "Join Channel:"))
        self.joinButton.setToolTip(_translate("IrcPage", "Select the color for join channel messages"))
        self.label_6.setText(_translate("IrcPage", "Error Messages:"))
        self.errorButton.setToolTip(_translate("IrcPage", "Select the color for error messages"))
        self.label_12.setText(_translate("IrcPage", "Leave Channel:"))
        self.leaveButton.setToolTip(_translate("IrcPage", "Select the color for leave channel messages"))
        self.label_7.setText(_translate("IrcPage", "Timestamp:"))
        self.timestampButton.setToolTip(_translate("IrcPage", "Select the color for timestamps"))
        self.label_13.setText(_translate("IrcPage", "Channel Info:"))
        self.infoButton.setToolTip(_translate("IrcPage", "Select the color for channel info messages"))
        self.label_8.setText(_translate("IrcPage", "Hyperlink:"))
        self.hyperlinkButton.setToolTip(_translate("IrcPage", "Select the color for hyperlinks"))
        self.textColoursGroup.setToolTip(_translate("IrcPage", "Enable to allow colored text in IRC messages"))
        self.textColoursGroup.setTitle(_translate("IrcPage", "Allow Colored Text in IRC Messages"))
        self.notificationsGroup.setToolTip(_translate("IrcPage", "Enable to show notifications"))
        self.notificationsGroup.setTitle(_translate("IrcPage", "Show Notifications"))
        self.label_14.setText(_translate("IrcPage", "<b>Note:</b> Notifications will only be shown, if the global usage of notifications is enabled on the notifications configuration page."))
        self.joinLeaveCheckBox.setToolTip(_translate("IrcPage", "Select to show a notification for join and leave events"))
        self.joinLeaveCheckBox.setText(_translate("IrcPage", "Join/Leave Event"))
        self.ownNickCheckBox.setToolTip(_translate("IrcPage", "Select to show a notification for every mentioning of your nick"))
        self.ownNickCheckBox.setText(_translate("IrcPage", "Mentioning of Own Nick"))
        self.messageCheckBox.setToolTip(_translate("IrcPage", "Select to show a notification for every message"))
        self.messageCheckBox.setText(_translate("IrcPage", "Every Message"))
        self.whoGroup.setToolTip(_translate("IrcPage", "Select this to enable the automatic lookup of user information for joined channels"))
        self.whoGroup.setTitle(_translate("IrcPage", "Enable Automatic User Information Lookup (/WHO)"))
        self.label_31.setText(_translate("IrcPage", "Max. Number of Users in Channel:"))
        self.whoUsersSpinBox.setToolTip(_translate("IrcPage", "Enter the maximum numbers of users in a channel allowed for this function"))
        self.label_32.setText(_translate("IrcPage", "Update Interval:"))
        self.whoIntervalSpinBox.setToolTip(_translate("IrcPage", "Enter the user information update interval"))
        self.whoIntervalSpinBox.setSuffix(_translate("IrcPage", " s"))
        self.markerGroup.setTitle(_translate("IrcPage", "Marker"))
        self.markWhenHiddenCheckBox.setToolTip(_translate("IrcPage", "Select to mark the current position, when the chat window is hidden"))
        self.markWhenHiddenCheckBox.setText(_translate("IrcPage", "Mark Current Position When Hidden"))
        self.label_33.setText(_translate("IrcPage", "Marker Foreground:"))
        self.markerForegroundButton.setToolTip(_translate("IrcPage", "Select the foreground color for the marker"))
        self.label_34.setText(_translate("IrcPage", "Marker Background:"))
        self.markerBackgroundButton.setToolTip(_translate("IrcPage", "Select the background color for the marker"))
        self.shutdownGroup.setTitle(_translate("IrcPage", "Shutdown"))
        self.confirmShutdownCheckBox.setToolTip(_translate("IrcPage", "Select to confirm a shutdown operation while still connected to an IRC server"))
        self.confirmShutdownCheckBox.setText(_translate("IrcPage", "Confirm Shutdown When Connected"))
