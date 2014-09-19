# -*- coding: utf-8 -*-
"""
/***************************************************************************
yield project
                                 A QGIS plugin
 prototype fore database connection and coherence between plugin and database
                             -------------------
        begin                : 2014-08-27
        git sha              : $Format:%H$
        copyright            : (C) 2014 by gillian
        email                : gillian.milani@romandie.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

        
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_initDb import UiInitDb

class iniDbDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(iniDbDialog, self).__init__(parent)
        self.ui = UiInitDb()
        self.ui.setupUi(self)
        