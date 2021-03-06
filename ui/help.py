# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_help_dialog(object):
    def setupUi(self, help_dialog):
        help_dialog.setObjectName("help_dialog")
        help_dialog.setWindowModality(QtCore.Qt.NonModal)
        help_dialog.resize(400, 300)
        help_dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/passkey.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        help_dialog.setWindowIcon(icon)
        help_dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(help_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.help_field = QtWidgets.QTextBrowser(help_dialog)
        self.help_field.setObjectName("help_field")
        self.verticalLayout.addWidget(self.help_field)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_button = QtWidgets.QPushButton(help_dialog)
        self.close_button.setMaximumSize(QtCore.QSize(75, 16777215))
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(help_dialog)
        QtCore.QMetaObject.connectSlotsByName(help_dialog)

    def retranslateUi(self, help_dialog):
        _translate = QtCore.QCoreApplication.translate
        help_dialog.setWindowTitle(_translate("help_dialog", "Help"))
        self.help_field.setPlaceholderText(_translate("help_dialog", "Blah-blah-blah~"))
        self.close_button.setText(_translate("help_dialog", "Close"))
