# -*- coding: utf-8 -*-
from PyQt4.QtCore import *

class Ship(QObject):
    def __init__(self, layer = None, attribute = None, elmt = None, projectState = None, dbState = None, solution = None):
        QObject.__init__(self)
        self.layer = layer
        self.attribute = attribute
        self.projectState = projectState
        self.dbState = dbState
        self.solution = solution
        self.elmt = elmt
        