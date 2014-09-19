# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_initDb.ui'
#
# Created: Wed Sep 17 14:10:16 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class UiInitDb(object):
    def setupUi(self, initDb):
        initDb.setObjectName(_fromUtf8("initDb"))
        initDb.resize(307, 210)
        self.gridLayout = QtGui.QGridLayout(initDb)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dbName = QtGui.QLabel(initDb)
        self.dbName.setObjectName(_fromUtf8("dbName"))
        self.gridLayout.addWidget(self.dbName, 0, 0, 1, 1)
        self.tHostName = QtGui.QLineEdit(initDb)
        self.tHostName.setObjectName(_fromUtf8("tHostName"))
        self.gridLayout.addWidget(self.tHostName, 1, 1, 1, 1)
        self.port = QtGui.QLabel(initDb)
        self.port.setObjectName(_fromUtf8("port"))
        self.gridLayout.addWidget(self.port, 2, 0, 1, 1)
        self.tPort = QtGui.QLineEdit(initDb)
        self.tPort.setObjectName(_fromUtf8("tPort"))
        self.gridLayout.addWidget(self.tPort, 2, 1, 1, 1)
        self.tUserName = QtGui.QLineEdit(initDb)
        self.tUserName.setObjectName(_fromUtf8("tUserName"))
        self.gridLayout.addWidget(self.tUserName, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(initDb)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
        self.tDbName = QtGui.QLineEdit(initDb)
        self.tDbName.setObjectName(_fromUtf8("tDbName"))
        self.gridLayout.addWidget(self.tDbName, 0, 1, 1, 1)
        self.hostName = QtGui.QLabel(initDb)
        self.hostName.setObjectName(_fromUtf8("hostName"))
        self.gridLayout.addWidget(self.hostName, 1, 0, 1, 1)
        self.userName = QtGui.QLabel(initDb)
        self.userName.setObjectName(_fromUtf8("userName"))
        self.gridLayout.addWidget(self.userName, 3, 0, 1, 1)
        self.tPassword = QtGui.QLineEdit(initDb)
        self.tPassword.setObjectName(_fromUtf8("tPassword"))
        self.gridLayout.addWidget(self.tPassword, 4, 1, 1, 1)
        self.password = QtGui.QLabel(initDb)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridLayout.addWidget(self.password, 4, 0, 1, 1)

        self.retranslateUi(initDb)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), initDb.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), initDb.reject)
        QtCore.QMetaObject.connectSlotsByName(initDb)

    def retranslateUi(self, initDb):
        initDb.setWindowTitle(_translate("initDb", "Database Connecton", None))
        self.dbName.setText(_translate("initDb", "Database Name", None))
        self.port.setText(_translate("initDb", "Port", None))
        self.hostName.setText(_translate("initDb", "hostname", None))
        self.userName.setText(_translate("initDb", "User Name", None))
        self.password.setText(_translate("initDb", "Password", None))

