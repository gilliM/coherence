#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

LAYER, ATT, ELMT, PROJ, DBVALUE, APP, SOL = range(7)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


class GCP(object):
    def __init__(self, v_layer='', v_att='', v_elmt = '', v_proj='', v_dbvalue='', v_app=0, v_solution = ''):
        self.v_layer = v_layer
        self.v_att = v_att
        self.v_elmt = v_elmt
        self.v_proj = v_proj
        self.v_dbvalue = v_dbvalue
        self.v_app = v_app
        self.v_solution = v_solution

class GCPTableModel(QAbstractTableModel):
    def __init__(self, filename=""):
        super(GCPTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.GCPs = []
        self.v_layers = set()
        self.v_atts = set()
        self.v_elmts = set()
        self.v_projs = set()
        self.v_dbvalues = set()
        self.v_apps = set()
        self.v_solutions = set()
        self.reverseState = False
        self.optionSort = {LAYER : self.sortByLayer,
                ATT : self.sortByAtt,
                PROJ : self.sortByProj,
                ELMT: self.sortByElmt,
                DBVALUE : self.sortByDBState,
                APP : self.sortByApp,
                SOL: self.sortBySol}
            
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index))


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.GCPs)):
            return 
        GCP = self.GCPs[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == LAYER:
                return  GCP.v_layer
            elif column == ATT:
                return  GCP.v_att
            elif column == ELMT:
                return  GCP.v_elmt
            elif column == PROJ:
                return  GCP.v_proj
            elif column == DBVALUE:
                return  GCP.v_dbvalue
            elif column == APP:
                return  GCP.v_app
            elif column == SOL:
                return  GCP.v_solution
        elif role == Qt.TextAlignmentRole:
            return  int(Qt.AlignLeft|Qt.AlignVCenter)
        elif role == Qt.BackgroundColorRole:
            if bool(index.row() % 2):
                return  QColor(181, 238, 181)
            else:
                return  QColor(255, 255, 255)
        return


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return  int(Qt.AlignLeft|Qt.AlignVCenter)
            return  int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return  
        if orientation == Qt.Horizontal:
            if section == LAYER:
                return  "Layer"
            elif section == ATT:
                return  "Attribute"
            elif section == ELMT:
                return  "Element"
            elif section == PROJ:
                return  "Project state"
            elif section == DBVALUE:
                return  "Database state"
            elif section == APP:
                return  "Action"
            elif section == SOL:
                return  "Solution proposed"
        return  int(section + 1)


    def rowCount(self, index=QModelIndex()):
        return len(self.GCPs)


    def columnCount(self, index=QModelIndex()):
        return 7

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.GCPs):
            GCP = self.GCPs[index.row()]
            column = index.column()
            if type(value) == unicode:
                try:
                    value = float(value)
                except:
                    value = 0
            if column == LAYER:
                GCP.v_layer = value
            elif column == ATT:
                GCP.v_att = value
            elif column == ELMT:
                GCP.v_elmt = value
            elif column == PROJ:
                GCP.v_proj = value
            elif column == DBVALUE:
                GCP.v_dbvalue = value
            elif column == APP:
                GCP.v_app = value
            elif column == SOL:
                GCP.v_solution = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False


    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,position + rows - 1)
        for row in range(rows):
            self.GCPs.insert(position + row,GCP())
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position,
                             position + rows - 1)
        self.GCPs = self.GCPs[:position] + \
                     self.GCPs[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True

    def checkValid(self,rowIndex):
        # A ne pas utiliser, pas transformer depuis autre projet
        #!!!!!!!!!!!
        valid = 1
        for i in range(0,7):
            index = self.index(rowIndex, i)
            dat = self.data(index)
            if not isinstance(dat, (int, long, float)):
                valid = 0
        return valid
        #!!!!!!!!!!!

    def sortShips(self, column):
        self.optionSort[column]()
        
    def sortByLayer(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_layer), reverse = self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)
            
    def sortByAtt(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_att), reverse =self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)
    
    def sortByElmt(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_elmt), reverse =self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)
            
    def sortByProj(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_proj), reverse =self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)

    def sortByDBState(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_dbvalue),reverse = self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)

    def sortByApp(self):
        self.GCPs = sorted(self.GCPs, key=lambda x: (x.v_app),reverse = self.reverseState)
        self.reset()
        self.reverseState = (self.reverseState == False)
    
    def sortBySol(self):
        # No sorting by solution column
        return

