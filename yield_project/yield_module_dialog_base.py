# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coherence_module_dialog_base.ui'
#
# Created: Fri Aug 29 08:35:52 2014
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

class Ui_YieldDialogBase(object):
    def setupUi(self, YieldDialogBase):
        YieldDialogBase.setObjectName(_fromUtf8("YieldDialogBase"))
        YieldDialogBase.resize(440, 250)
        self.centralwidget = QtGui.QWidget(YieldDialogBase)
        YieldDialogBase.setCentralWidget(self.centralwidget)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(YieldDialogBase)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 1, 0, 4, 1)
        self.sendRequestButton = QtGui.QCommandLinkButton(YieldDialogBase)
        self.sendRequestButton.setObjectName(_fromUtf8("sendRequestButton"))
        policy = self.textEdit.sizePolicy()
        policy.setVerticalStretch(1)
        policy.setHorizontalStretch(1)
        self.textEdit.setSizePolicy(policy)
        policy = self.sendRequestButton.sizePolicy()
        policy.setHorizontalPolicy(4)
        policy.setVerticalPolicy(4)
        self.sendRequestButton.setSizePolicy(policy)
        self.gridLayout.addWidget(self.sendRequestButton, 4, 0, 1, 1)
        
        self.frame = QtGui.QFrame(YieldDialogBase)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.gridLayout.addWidget(self.frame, 1, 2, 1, 1)
        
        self.reloadLayersButton = QtGui.QCommandLinkButton(YieldDialogBase)
        self.reloadLayersButton.setObjectName(_fromUtf8("reloadLayersButton"))
        policy = self.reloadLayersButton.sizePolicy()
        policy.setVerticalPolicy(4)
        self.reloadLayersButton.setSizePolicy(policy)
        self.verticalLayout.addWidget(self.reloadLayersButton)
        
        self.refreshStructureButton = QtGui.QCommandLinkButton(YieldDialogBase)
        self.refreshStructureButton.setObjectName(_fromUtf8("refreshStructureButton"))
        policy = self.refreshStructureButton.sizePolicy()
        policy.setVerticalPolicy(4)
        self.refreshStructureButton.setSizePolicy(policy)
        self.verticalLayout.addWidget(self.refreshStructureButton)

        self.checkStructureButton = QtGui.QCommandLinkButton(YieldDialogBase)
        self.checkStructureButton.setObjectName(_fromUtf8("checkStructureButton"))
        policy = self.checkStructureButton.sizePolicy()
        policy.setVerticalPolicy(4)
        self.checkStructureButton.setSizePolicy(policy)
        self.verticalLayout.addWidget(self.checkStructureButton)

        self.configureInterfaceButton = QtGui.QCommandLinkButton(YieldDialogBase)
        self.configureInterfaceButton.setObjectName(_fromUtf8("configureInterfaceButton"))
        policy = self.configureInterfaceButton.sizePolicy()
        policy.setVerticalPolicy(4)
        self.configureInterfaceButton.setSizePolicy(policy)
        self.verticalLayout.addWidget(self.configureInterfaceButton)
    
        self.retranslateUi(YieldDialogBase)    
        self.reloadLayersButton.setFocus()
        self.reloadLayersButton.setDefault(True)

    def retranslateUi(self, YieldDialogBase):
        YieldDialogBase.setWindowTitle(_translate("YieldDialogBase", "Get some coherence", None))
        self.sendRequestButton.setText(_translate("YieldDialogBase", "Send Request", None))
        self.reloadLayersButton.setText(_translate("YieldDialogBase", "Reload layers", None))
        self.refreshStructureButton.setText(_translate("YieldDialogBase", "Refresh links", None))
        self.checkStructureButton.setText(_translate("YieldDialogBase", "Check coherence", None))
        self.configureInterfaceButton.setText(_translate("YieldDialogBase", "Configure Interface", None))

