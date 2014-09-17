# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'check_structure_dialog_base.ui'
#
# Created: Thu Sep 11 10:50:43 2014
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

class Ui_checkStructureDialogBase(object):
    def setupUi(self, checkStructureDialogBase):
        checkStructureDialogBase.setObjectName(_fromUtf8("checkStructureDialogBase"))
        checkStructureDialogBase.resize(1020, 300)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Droid Sans [monotype]"))
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        checkStructureDialogBase.setFont(font)
        self.gridLayout = QtGui.QGridLayout(checkStructureDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        
        self.tableView = TableView(checkStructureDialogBase)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.buttonBox = QtGui.QDialogButtonBox(checkStructureDialogBase)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.passAllButton = QtGui.QPushButton(checkStructureDialogBase)
        self.passAllButton.setObjectName(_fromUtf8("passAllButton"))
        self.passAllButton.setFixedWidth(120)
        
        self.applyAllButton = QtGui.QPushButton(checkStructureDialogBase)
        self.applyAllButton.setObjectName(_fromUtf8("applyAllButton"))
        self.applyAllButton.setFixedWidth(120)
        
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        spacerItem2 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        spacerItem3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addWidget(self.passAllButton,  0, 2, 1, 1,alignment = QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.applyAllButton, 1, 2, 1, 1,alignment = QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.buttonBox,      3, 2, 1, 1, alignment = QtCore.Qt.AlignRight |QtCore.Qt.AlignBottom)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.gridLayout.addItem(spacerItem2, 0, 3, 1, 1)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.tableView,      0, 1, 4, 3)



        self.retranslateUi(checkStructureDialogBase)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), checkStructureDialogBase.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), checkStructureDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(checkStructureDialogBase)

    def retranslateUi(self, checkStructureDialogBase):
        checkStructureDialogBase.setWindowTitle(_translate("checkStructureDialogBase", "Elements incohérents", None))
        self.passAllButton.setText(_translate("checkStructureDialogBase", "Set all «Pass»", None))
        self.applyAllButton.setText(_translate("checkStructureDialogBase", "Set all «Apply»", None))
        
class TableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)
        self.actionValues = ['Pass', 'Apply']
        self.setItemDelegateForColumn(5,ComboBoxDelegate(self, self.actionValues))
        self.header = self.horizontalHeader()
        self.setSortingEnabled(True)

 
        
class ComboBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, owner, itemslist):
        QtGui.QItemDelegate.__init__(self, owner)
        self.itemslist = itemslist
        self.owner = owner
 
    def paint(self, painter, option, index):        
        # Get Item Data
        self.owner.openPersistentEditor(index)
        value = index.data(QtCore.Qt.DisplayRole)
        # fill style options with item data
        style = QtGui.QApplication.style()
        opt = QtGui.QStyleOptionComboBox()
        opt.currentText = str(self.itemslist[value])
        opt.rect = option.rect
 
        # draw item data as ComboBox
        style.drawComplexControl(QtGui.QStyle.CC_ComboBox, opt, painter)
 
    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        editor.addItems(self.itemslist)
        editor.setCurrentIndex(0)
        editor.installEventFilter(self)            
        return editor
 
    def setEditorData(self, editor, index):
        text = self.itemslist[index.data(QtCore.Qt.DisplayRole)]
        pos = editor.findText(text)
        if pos == -1:  
            pos = 0
        editor.setCurrentIndex(pos)
 
    def setModelData(self,editor,model,index):
        #editor.setCurrentIndex(int(index.model().data(index)))
        value = editor.currentIndex()
        model.setData(index, value)
 
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

