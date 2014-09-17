# -*- coding: utf-8 -*-
"""
/***************************************************************************
Yield project
                                 A QGIS plugin
 prototype for connection database
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QColor, QApplication, QMessageBox, QDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from yield_module_dialog import yieldMainWindow
import os.path
from qgis.core import *
from qgis.gui import *
import random
from PyQt4.QtSql import *

import site

class yieldMain:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'yield_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.mw = yieldMainWindow(self.iface)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Where is the yield?')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'yield')
        self.toolbar.setObjectName(u'yield')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('yieldProject', message)


    def add_action(self, icon_path, text, callback, enabled_flag=True,
        add_to_menu=True, add_to_toolbar=True, status_tip=None,
        whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/yield_project/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'prototype for jam'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Jam Resampler'),
                action)
        self.iface.removeToolBarIcon(action)
    
    def take_a_shape(self):
        table = ("rectangle", "diamond", "pentagon", "triangle","equilateral_triangle",\
                  "regular_star", "arrow", "circle", "cross")
        index = int(round(random.random()*(len(table)-1)))
        shape = table[index]
        return shape

    def run(self):
        #sudo apt-get install libqt4-sql-psql
        
        db = QSqlDatabase.addDatabase("QPSQL","first2");
        """db.setHostName("sige-demo");
        db.setDatabaseName("sige");
        db.setUserName("sige");
        db.setPassword("sige");"""
        db.setHostName("localhost");
        db.setDatabaseName("yield_db");
        db.setUserName("postgres");
        db.setPassword("postgres");
        db.setPort(5432)
        ok = db.open();
        if ok:
            QMessageBox.information(QDialog(), "Database status", "Database is connected")        
            self.mw.db = db
            #print db.lastError().databaseText()
            #print db.lastError().driverText()
    
            self.mw.show()
            
            ## Run the dialog event loop
            
        else:
            QMessageBox.critical(QDialog(), "Database status", "Connection failed")   


