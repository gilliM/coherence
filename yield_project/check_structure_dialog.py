# -*- coding: utf-8 -*-
import GCPs
from PyQt4 import QtCore
from PyQt4 import QtGui
from check_structure_dialog_base import Ui_checkStructureDialogBase
        
class checkStructureDialog(QtGui.QDialog):
    def __init__(self, shipList, parent=None):
        """Constructor."""
        super(checkStructureDialog, self).__init__(parent)
        self.shipList = shipList
        self.ui = Ui_checkStructureDialogBase()
        self.ui.setupUi(self)
        self.model = GCPs.GCPTableModel()
        self.ui.tableView.setModel(self.model)
        header = self.ui.tableView.horizontalHeader()
        self.ui.passAllButton.clicked.connect(self.setPassAll)
        self.ui.applyAllButton.clicked.connect(self.setApplyAll)
        self.initializeTable()
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.header.resizeSection(5,100)
        
        self.ui.tableView.header.sectionClicked.connect(self.model.sortShips)
        stylesheet = "::section{color:rgb(254,254,254);Background-color:rgb(25,25,25);border-radius:6px;font-size:13px}"
        self.ui.tableView.horizontalHeader().setStyleSheet(stylesheet)
        stylesheet = "::section{color:rgb(254,254,254);Background-color:rgb(25,25,25);border-radius:2px;font-size:12px}"
        self.ui.tableView.verticalHeader().setStyleSheet(stylesheet)

    
    def initializeTable(self):
        for ship in self.shipList:
            self.addGCP(ship)
    
    def addGCP(self,ship):
        # add a GCP to the table
        row = self.model.rowCount()
        self.model.insertRows(row)
        self.model.setData(self.model.index(row, 0), ship.layer)
        self.model.setData(self.model.index(row, 1), ship.attribute)
        self.model.setData(self.model.index(row, 2), ship.elmt)
        self.model.setData(self.model.index(row, 3), ship.projectState)
        self.model.setData(self.model.index(row, 4), ship.dbState)
        self.model.setData(self.model.index(row, 6), ship.solution)
        
    def setPassAll(self):
        nRow = self.model.rowCount()
        for row in xrange(nRow):
            index = self.model.index(row, 5)
            self.model.setData(index, 0)
        
    def setApplyAll(self):
        nRow = self.model.rowCount()
        for row in xrange(nRow):
            index = self.model.index(row, 5)
            self.model.setData(index, 1)
        
    