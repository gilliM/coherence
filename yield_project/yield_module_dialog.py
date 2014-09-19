# -*- coding: utf-8 -*-
"""
/***************************************************************************
coherenceDialog
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

# Current rules for validation:
# 1. All "id" fields are not editable.
# 2. Foreigns keys which target table with "value_fr" or "name" fields are combo box.
# 3. Foreigns keys which are not combo box are triggered and therefore not editable.
# 4. All date fields in db need a DateTime widget
# 5. All boolean fields which are not foreign keys are checkbox
# 6. Text fields which have at least one value with more than  40 character need multiline display
# 7. All attributes starting with "geometry" are "Hidden"
#
# to do: Check ranges

# Database requirement:
# The database must have all layers and table in a schema called "distribution".
# All fields which require a checkbox are boolean and aren't foreign key.
# All fields which require a combobox are foreign keys.
# All table of value for combobox have a field called value_fr or name which is used for the combo list.
# All date fields are date type.
# All primary keys are named "id"
#
# It would be easier if triggered fields name start with "tr_*" or "idtr_*".
# It could be good if the name of the value taken in combo box is given in the field name of foreign key.

        
import os
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtXml
from yield_module_dialog_base import Ui_YieldDialogBase
from PyQt4.QtSql import *
from qgis.core import QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry
from ui_buffering import Ui_progressBar
from check_structure_dialog import checkStructureDialog
from ship import Ship
import ast
import time

class yieldMainWindow(QtGui.QMainWindow):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(yieldMainWindow, self).__init__(parent)
        self.db = None
        self.iface = iface
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_YieldDialogBase()
        self.ui.setupUi(self)
        self.tables = []
        
        self.ui.sendRequestButton.clicked.connect(self.request)
        self.ui.textEdit.setText("SELECT table_name FROM information_schema.tables;")
        self.ui.reloadLayersButton.clicked.connect(self.reloadLayers)
        self.ui.refreshStructureButton.clicked.connect(self.refreshStructure)
        self.ui.checkStructureButton.clicked.connect(self.checkStructure)
        self.ui.configureInterfaceButton.clicked.connect(self.configureInterface)
        self.dictLegendRefBySource = {}
        self.dictSourceRefByLegend = {}
        
        self.ui.textEdit.setStyle(QtGui.QStyleFactory.create('Motif'))
        self.center()
    
    def closeEvent(self,e):
        self.db.close()
        self.db.removeDatabase("first2")
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
            
    def configureInterface(self):
        att = 'remark'
        self.tabs = []
        self.groups = []
        self.widgets = []
        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            layer.clearAttributeEditorWidgets()
            layer.setEditorLayout(1)
            self.tabs.append(QgsAttributeEditorContainer("Tab 1", layer))
            fields =  layer.pendingFields()
            for field in fields:
                self.widgets.append(QgsAttributeEditorField(field.name()\
                                    , layer.fieldNameIndex(field.name())\
                                    , layer))
                self.tabs[-1].addChildElement(self.widgets[-1])
            layer.addAttributeEditorWidget(self.tabs[-1])
        
    
    def getNodes(self, node, parent = None):
        if parent == 'source' or parent == 'name' or parent == 'symbology':
            text =  node.firstChild().toText().data()
        else:
            text = []
            n = node.firstChild()
            while (not n.isNull()):
                t = n.nodeName()
                if n.nodeType() == 1:
                    rec = self.getNodes(n, t)
                    if n.toElement().hasAttribute('groupname'):
                        name =  n.toElement().attribute('groupname')
                        group = [t, rec, name]
                        self.barCount += 1
                    else:
                        group = [t, rec]
                    text.append(group)
                n = n.nextSibling()
        return text
    
    def addGroups(self, list, parent = None):
        for group1 in list:
                if group1[0] != 'layer':
                    if len(group1) > 2:
                        index = self.iface.legendInterface().addGroup(group1[2], True, parent)
                    else:
                        index = self.iface.legendInterface().addGroup(group1[0], True, parent)
                    self.addGroups(group1[1], index)
                else:
                    dicInfoLayer = dict((key, value) for (key, value) in group1[1])
                    if 'source' not in dicInfoLayer:
                        QMessageBox.warning(QDialog(),'configuration', "Source not defined for a layer")
                        raise IOError
                    source = dicInfoLayer['source']
                    layer = self.loadTable(source)
                    self.iface.legendInterface().moveLayer(layer, parent)
                    if 'name' in dicInfoLayer:
                        nomTemp = dicInfoLayer['name']
                        nom = ''.join(chr(ord(c)) for c in nomTemp).decode('utf8')
                        layer.setLayerName(nom)
                    if 'symbology' in dicInfoLayer:
                        style = dicInfoLayer['symbology']
                        self.getSymbology(layer, style)
                        
    def reloadLayers(self):
        self.tables = []
        self.vlayer = []
        self.barCount = 0
        self.loadSymbologies()
        # Clear legend
        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            QgsMapLayerRegistry.instance().removeMapLayer(name)
        while self.iface.legendInterface().groupExists(0):
                self.iface.legendInterface().removeGroup(0)        
        
        path = os.path.dirname(os.path.realpath(__file__))
        fName =  path + "/config.xml"
        if not fName:
            return
        file=QFile(fName)
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            QMessageBox.warning(QDialog(),'Application', "Cannot read file %s :\n%s."\
                                %(file.fileName(),file.errorString()))
            return False
        else:
            doc = QtXml.QDomDocument("EnvironmentML");
            if(not doc.setContent(file)):
                file.close()
                QMessageBox.warning(self,"Error","Could not parse xml file.")
            file.close()
            root = doc.documentElement();
            if(root.tagName()!="config"):
                 QMessageBox.warning(self,"Error","Could not parse xml file. Root Element must be <kml/>.")
            else:
                #try:
                t = self.getNodes(root)
                self.initProgressBar()        # create progressbar
                self.addGroups(t)
                #except:
                #    QMessageBox.warning(self,"Configuration failed","Failed to read the configuration file correctly")
                #    return
        self.bar = None
        QtGui.QMessageBox.information(QtGui.QDialog(), "Reloading layers", "Layers are succesfully reloaded")            
        
        
    def loadSymbologies(self):
        text = "SELECT id, stylename, description FROM public.layer_styles";
        query = QSqlQuery(self.db) ;
        test = query.exec_(text);
        self.dicStyle = {}
        while (query.next()):
            i = 0
            self.dicStyle[query.value(1)] = query.value(0)
            
    def getSymbology(self, layer, styleName):
        errorMsg = ''
        print self.dicStyle
        if styleName in self.dicStyle:
            id = self.dicStyle[styleName] 
            styleText = layer.getStyleFromDatabase(str(id),errorMsg)
            layer.applyNamedStyle(styleText,errorMsg)
        else:
            QMessageBox.warning(QDialog(),'Configuration', "Symbology %s not present in database"%styleName)
            raise IOError
             
    def loadTable(self, table):
        QtCore.QCoreApplication.processEvents()
        uri = QgsDataSourceURI()
        # set host name, port, database name, username and password
        uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(), self.db.userName(), self.db.password())
        if table.startswith('od_'):
            uri.setDataSource("distribution", table, 'geometry')
        else:
            uri.setDataSource("distribution", table, None)
        self.vlayer.append(QgsVectorLayer(uri.uri(), table, "postgres"))
        inst = QgsMapLayerRegistry.instance()
        legend = self.iface.legendInterface()
        layer = inst.addMapLayer(self.vlayer[-1])
        legend.setLayerVisible(self.vlayer[-1],False)
        self.iface.mapCanvas().refresh()
        self.bar.progressBar.setValue(self.progress)
        self.progress += self.barInc
        return layer
        

    def refreshProjectInfo(self):
        self.dictLegendRefBySource = {}
        self.dictSourceRefByLegend = {}
        self.changeCount = 0
        for name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            layerSource = layer.source().split(' ')
            for sourceElmt in layerSource:
                if sourceElmt.startswith('table'):
                    tableName = sourceElmt.split('"')[-2]
                    self.dictLegendRefBySource[tableName] = layer.name()
                    self.dictSourceRefByLegend[layer.name()] = tableName
                    
        self.tables = []
        text = "SELECT table_name FROM information_schema.tables WHERE table_schema='distribution';"
        query = QSqlQuery(self.db) ;
        test = query.exec_(text);
        while (query.next()):
            i = 0
            while (query.value(i) is not None): 
                val = str(query.value(i))
                #if val.startswith('od_'):
                self.tables.append(val)
                i = i +1

    def refreshStructure(self):
        self.refreshProjectInfo()
        # dicAttributs:= dic[nom de couche] = liste d'attributs
        # dicCombo := dic[nom de couche, attribut] = liste de valeurs
        # dicType := dic[nom de couche, attribut] = type
        # self.dicStructure := dic[nom de couche, attribut] = [Widget,widgetName, type, valeur(s)]
        while True:
            previous_modif = self.changeCount
            dicAttributs, dicType = self.getDicAttributsAndType()
            dicCombo = self.getDicCombo()
            dicStructure = self.getDicStructure(dicAttributs,dicCombo,dicType)
            shipList = self.getShipList(dicAttributs, dicStructure)
            self.checkStructureDia = checkStructureDialog(shipList)
            shipList = None
            self.checkStructureDia.setApplyAll()
            self.getActions()
            self.checkStructureDia = None
            self.createActionDictionary()
            self.applyActions()
            if previous_modif == self.changeCount:
                break
        QtGui.QMessageBox.information(QtGui.QDialog(), "Change in QGIS project", "Number of modifications applied: %s"%self.changeCount)
    
    def checkStructure(self):
        self.refreshProjectInfo()
        # dicAttributs:= dic[nom de couche] = liste d'attributs
        # dicCombo := dic[nom de couche, attribut] = liste de valeurs
        # dicType := dic[nom de couche, attribut] = type
        # self.dicStructure := dic[nom de couche, attribut] = [Widget,widgetName, type, valeur(s)]
        dicAttributs, dicType = self.getDicAttributsAndType()
        dicCombo = self.getDicCombo()
        dicStructure = self.getDicStructure(dicAttributs,dicCombo,dicType)
        shipList = self.getShipList(dicAttributs, dicStructure)
        self.checkStructureDia = checkStructureDialog(shipList)
        shipList = None
        self.checkStructureDia.show()
        result = self.checkStructureDia.exec_()
        
        if result:
            self.getActions()
            self.checkStructureDia = None
            self.createActionDictionary()
            self.applyActions()
            QtGui.QMessageBox.information(QtGui.QDialog(), "Change in QGIS project", "Number of modifications applied: %s"%self.changeCount)
    
    def createActionDictionary(self):
        self.actionDictionary = {}
        for ship in self.actionShips:
            element = ship.elmt
            elementConfig = ship.dbState
            if (ship.layer,ship.attribute) in self.actionDictionary:
                self.actionDictionary[ship.layer,ship.attribute].append([element,elementConfig])
            else:
                self.actionDictionary[ship.layer,ship.attribute]= [[element,elementConfig]]

    def applyActions(self):
        tables = []
        for key in self.actionDictionary:
            if key[0] not in tables:
                tables.append(key[0])
        for nameLayer, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == 0:
                # The name of the layer is not equal to the name of his data source table
                if layer.name() not in self.dictSourceRefByLegend:
                    continue
                name = self.dictSourceRefByLegend[layer.name()]
                if name in tables:
                    # layer.setEditorLayout(0)
                    fields = layer.pendingFields()
                    id = 0
                    for field in fields:
                        if (name,field.name()) in self.actionDictionary:
                            for sheep in self.actionDictionary[name,field.name()]:
                                self.changeCount +=1
                                element = sheep[0]
                                elementConfig = sheep[1]
                                if element == 'widget':
                                    layer.setEditorWidgetV2(id,elementConfig)
                                elif element == 'isEditable':
                                    booleanValue = ast.literal_eval(elementConfig)
                                    layer.setFieldEditable(id,booleanValue)
                                elif element == 'isMultiline':
                                    config = layer.editorWidgetV2Config(id)
                                    booleanValue = ast.literal_eval(elementConfig)
                                    config[u'IsMultiline'] = booleanValue
                                    config[u'UseHtml'] = False
                                    layer.setEditorWidgetV2Config(id, config)
                                elif element == 'RelationLayer':
                                    config = layer.editorWidgetV2Config(id)
                                    config[u'Layer'] = elementConfig
                                    layer.setEditorWidgetV2Config(id, config)
                                elif element == 'RelationKey':
                                    config = layer.editorWidgetV2Config(id)
                                    config[u'Key'] = elementConfig
                                    layer.setEditorWidgetV2Config(id, config)
                                elif element == 'RelationValue':
                                    config = layer.editorWidgetV2Config(id)
                                    config[u'Value'] = elementConfig
                                    layer.setEditorWidgetV2Config(id, config)
                                if elementConfig == 'DateTime': 
                                    config = layer.editorWidgetV2Config(id)
                                    config[u'display_format'] = u'dd/MM/yy'
                                    config[u'field_format'] = 'yyyy-MM-dd'
                                    config[u'calendar_popup'] = True
                                    layer.setEditorWidgetV2Config(id, config)
                                   # print layer.editorWidgetV2Config(id)
                            # All fields are, by default, editable. Then depending on type, we will change it!
                        id +=1
        return
    
    def getActions(self):
        # As the order of columns can change,
        # we have to re-extract all information from the model
        self.actionShips = []
        nRow = self.checkStructureDia.model.rowCount()
        nCol = self.checkStructureDia.model.columnCount()
        for row in xrange(nRow):
            index = self.checkStructureDia.model.index(row, 5)
            apply = self.checkStructureDia.model.data(index)
            if apply:
                val = ['' for i in range(nCol)]
                for col in xrange(nCol):
                    index = self.checkStructureDia.model.index(row, col)
                    val[col] = self.checkStructureDia.model.data(index)
                newActionShip = Ship(val[0],val[1],val[2],val[3], val[4])
                self.actionShips.append(newActionShip)      
        
    
    def getShipList(self, dicAttributs, dicStructure):
        shipList = []
        for nameLayer, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == 0:
                if layer.name() not in self.dictSourceRefByLegend:
                    continue
                name = self.dictSourceRefByLegend[layer.name()]
                if name in self.tables:
                    #layer.setEditorLayout(0)
                    fields = layer.pendingFields()
                    id = 0
                    for field in fields:
                        if field.name() in dicAttributs[name]:
                            db_widget = dicStructure[name,field.name()][0]
                            values = dicStructure[name,field.name()][3]
                            type = dicStructure[name,field.name()][2]
                            project_widget =layer.editorWidgetV2(id)
                            # All fields are, by default, editable. Then depending on type, we will change it!
                            project_isEditable = layer.fieldEditable(id)
                            db_isEditable = True
                            project_config = layer.editorWidgetV2Config(id)
                            solution = ''
                            if db_widget == 'ValueRelation':
                                for nLayer, vlayer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
                                    try:
                                        if self.dictSourceRefByLegend[vlayer.name()] == values[0]:
                                            clayer = nLayer
                                    except:
                                        continue
                                if ('value_fr' not in dicAttributs[values[0]]) \
                                    and ('name' not in dicAttributs[values[0]])\
                                    and  ('tr_value_fr' not in dicAttributs[values[0]]) :
                                    db_widget = 'TextEdit'
                                    db_isEditable = False
                                elif project_widget == 'ValueRelation':
                                    #Widget is ok, but we will check the configuration here
                                    #first, check the related layer
                                    if 'Layer' not in project_config:
                                        solution = 'Set layer of value relation'
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationLayer',str('None'),\
                                            str(clayer), solution)
                                        shipList.append(newship)
                                    elif project_config[u'Layer'] != clayer:
                                        solution = 'Change layer of value relation'
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationLayer',str(project_config[u'Layer']),\
                                            str(clayer), solution)
                                        shipList.append(newship)
                                    # then check the related key of the layer is ok
                                    if 'Key' not in project_config:
                                        solution = 'Set key of value relation'
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationKey',str('None'),\
                                            str(values[1]), solution)
                                        shipList.append(newship)
                                    elif project_config[u'Key'] != str(values[1]):
                                        solution = 'Change key of value relation'
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationKey',str(project_config[u'Key']),\
                                            str(values[1]), solution)
                                        shipList.append(newship)
                                    # Then check the value of the value is ok
                                    if 'Value' not in project_config:
                                        if 'value_fr' in dicAttributs[values[0]]:
                                            old_value = 'None'; new_value = 'value_fr'
                                            solution = 'Change the value Relation'
                                        elif 'tr_value_fr' in dicAttributs[values[0]]:
                                            old_value = 'None'; new_value = 'tr_value_fr'
                                            solution = 'Change the value Relation'
                                        elif 'name' in dicAttributs[values[0]]:
                                            old_value = 'None'; new_value = 'name'
                                            solution = 'Change the value Relation'
                                        else:
                                            old_value = 'None'; new_value = 'None'
                                            solution = 'No solution, Set manually value of value relation'
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationValue',old_value,\
                                            new_value, solution)
                                        shipList.append(newship)
                                    # Hypothesis: no table have both value_fr and name attribute
                                    elif project_config[u'Value'] != 'value_fr' and project_config[u'Value'] != 'name' and project_config[u'Value'] != 'tr_value_fr' :
                                        solution = 'Change value of value relation'
                                        if 'value_fr' in dicAttributs[values[0]]:
                                             old_value = project_config[u'Value']; new_value = 'value_fr'
                                        elif 'tr_value_fr' in dicAttributs[values[0]]:
                                             old_value = project_config[u'Value']; new_value = 'tr_value_fr'
                                        else:
                                            old_value = 'None'; new_value = 'None'
                                            solution = 'No solution, Set manually value of value relation' 
                                        newship = Ship(str(name),str(field.name()),\
                                            'RelationValue',old_value,\
                                            new_value, solution)
                                        shipList.append(newship)
                                    
                            if project_widget != db_widget:
                                # Check of Valuerelation, DateTime (date), CheckBox (boolean) and TextEdit
                                if project_widget == 'ValueRelation' and db_widget == 'TextEdit' :
                                    solution = 'No solution (Foreign key may be missing in DB)'
                                else:
                                    solution = 'Change current widget with the proposed one'
                                newship = Ship(str(name),str(field.name()),'widget',str(project_widget),db_widget, solution)
                                shipList.append(newship)
                                solution = ''
                            if type == 'longText':
                                #layer.setFieldMultiLine(id,True)
                                solution = 'Set field multiline'
                                if 'IsMultiline' not in project_config:
                                        newship = Ship(str(name),str(field.name()),\
                                       'isMultiline',str(False),\
                                       str(True), solution)
                                        shipList.append(newship)
                                elif project_config['IsMultiline'] != True:
                                    newship = Ship(str(name),str(field.name()),\
                                               'isMultiline',str(project_config['IsMultiline']),\
                                               str(True))
                                    shipList.append(newship)       
                            if field.name() == 'id':
                                db_isEditable = False
                                solution = 'Set field non editable'
                            if field.name().startswith('tr_'):
                                db_isEditable = False
                                solution = 'Set field non editable'
                            if project_isEditable != db_isEditable:
                                if solution == '':
                                    solution = 'Change editability of the field'
                                newship = Ship(str(name),str(field.name()),\
                                               'isEditable',str(project_isEditable),\
                                               str(db_isEditable), solution)
                                shipList.append(newship)
                            id +=1
        return shipList


    def updateStructure(self, dicAttributs, dicStructure):
        for nameLayer, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.type() == 0:
                if layer.name() not in self.dictSourceRefByLegend:
                    continue
                name = self.dictSourceRefByLegend[layer.name()]
                if name in self.tables:
                    layer.setEditorLayout(0)
                    fields = layer.pendingFields()
                    id = 0
                    for field in fields:
                        if field.name() in dicAttributs[name]:
                            widget = dicStructure[name,field.name()][0]
                            values = dicStructure[name,field.name()][3]
                            type = dicStructure[name,field.name()][2]
                            layer.setEditorWidgetV2(id,widget)
                            # All fields are, by default, editable. Then depending on type, we will change it!
                            layer.setFieldEditable(id,True)
                            config = {}
                            # DPFE rule
                            if field.name().startswith('tr_') or type == 'primaryKey':
                                layer.setEditorWidgetV2(id,'TextEdit')
                                layer.setFieldEditable(id,False)
                                
                            if widget == 'ValueRelation':
                                for nameLayer, vlayer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
                                    try:
                                        if self.dictSourceRefByLegend[vlayer.name()] == values[0]:
                                            clayer = nameLayer
                                    except:
                                        continue
                                config = {}
                                config[u'Layer'] = clayer
                                config[u'Key'] = str(values[1])
                                config[u'FilterExpression'] = None
                                config[u'AllowMulti'] = False
                                config[u'AllowNull'] = True
                                config[u'OrderByValue'] = False
                                
                                if 'value_fr' in dicAttributs[values[0]]:
                                    config[u'Value'] = 'value_fr'         
                                elif 'tr_value_fr' in dicAttributs[values[0]]:
                                    config[u'Value'] = 'tr_value_fr'   
                                elif 'name'in dicAttributs[values[0]]:
                                    config[u'Value'] = 'name'
                                else:
                                    # DPFE RULE
                                    config[u'Value'] = str(values[1])
                                    
                                    #QWAT RULE
                                    # All fields which are foreign key but not value or name are triggered
                                    # Triggerd are simply TextEdit widgets, non editables
                                    #layer.setEditorWidgetV2(id,'TextEdit')
                                    #layer.setFieldEditable(id,False)
                                    
                            if type == 'longText':
                                #print dir(layer)
                                #layer.setFieldMultiLine(id,True)
                                config = {}
                                config[u'UseHtml'] = False
                                config[u'IsMultiline'] = True
                            if type == 'date':
                                config[u'display_format'] = u'dd/MM/yy'
                                config[u'field_format'] = 'yyyy-MM-dd'
                                config[u'calendar_popup'] = True
                            layer.setEditorWidgetV2Config(id, config)
                            id +=1
        return
    
    def getDicStructure(self, dAtt,dCom,dTyp):
        dicStructure = {}
        for table, attributes in dAtt.items():
            for att in attributes:
                type = dTyp[table, att]
                if (table, att) in dCom:
                    widget = 'ValueRelation'
                    values = dCom[table, att]
                elif type == 'primaryKey':
                    widget = 'TextEdit'
                    values = None
                elif type == 'boolean':
                    # It is important to have the bool check after the foreignKey check.
                    # Because some bollean fields-type need a combo box (Null, True or False)
                    widget = 'CheckBox'
                    values = False
                elif type == 'date':
                    widget = 'DateTime'
                elif att.startswith('geometry'):
                    widget = 'Hidden'
                else:
                    widget = 'TextEdit'
                    values = None
                widgetName = widget +'_'+att 
                dicStructure[table, att] = [widget,widgetName,type,values]
        return dicStructure
    
    def getDicAttributsAndType(self):
        dicAtt = {}
        dicType = {}
        for table in self.tables:
            textPM = """SELECT pg_attribute.attname
FROM pg_index, pg_class, pg_attribute 
WHERE 
  pg_class.oid = 'distribution.%s'::regclass AND
  indrelid = pg_class.oid AND
  pg_attribute.attrelid = pg_class.oid AND 
  pg_attribute.attnum = any(pg_index.indkey)
  AND indisprimary;""" %table
            queryPM = QSqlQuery(self.db) ;
            textPM = queryPM.exec_(textPM);
            while (queryPM.next()):
                primaryKey = queryPM.value(0)
                print primaryKey
            text = "SELECT column_name, data_type\
    FROM information_schema.columns \
    WHERE table_name = '%s' \
    ORDER BY ordinal_position;" %table
            query = QSqlQuery(self.db) ;
            test = query.exec_(text);
            attributesList = []
            while (query.next()):
                attributesList.append(query.value(0))
                if query.value(0) == primaryKey:
                    dicType[table,query.value(0)] = 'primaryKey'
                    # for text fields, check if there are multilines
                elif query.value(1) == u'text' or query.value(1) == u'character varying':
                    textLen = """
                    SELECT max (length) 
                    FROM (SELECT character_length(%s) 
                        AS length FROM distribution.%s 
                        GROUP BY id) AS subquery;""" %(query.value(0),table)
                    queryLen = QSqlQuery(self.db);
                    testLen = queryLen.exec_(textLen);
                    while (queryLen.next()):
                        if queryLen.value(0) > 40:
                            dicType[table,query.value(0)] = 'longText'
                        else:
                            dicType[table,query.value(0)] = query.value(1)
                else: 
                    dicType[table,query.value(0)] = query.value(1)                            
            dicAtt[table] = attributesList
            print attributesList
        return dicAtt, dicType
    
    def getDicCombo(self):
        dicCombo = {}
        for table in self.tables:
            text2 = """SELECT
    tc.constraint_name, tc.table_name, kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
    FROM 
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='%s';""" %table
            query2 = QSqlQuery(self.db) ;
            test = query2.exec_(text2);
            while (query2.next()):
                dicCombo[str(query2.value(1)),str(query2.value(2))] = [query2.value(3),query2.value(4)]
        return dicCombo
    
    def request(self):
        text = self.ui.textEdit.toPlainText()
        query = QSqlQuery(self.db) ;
        test_pass = query.exec_(text);
        print text
        if test_pass:
            while (query.next()):
                i = 0
                text =  []
                while query.value(i) is not None: 
                    
                    #if val.startswith('od_'):
                    text.append(query.value(i))
                    i = i +1
                if text != []:
                    print text
        else:
            QtGui.QMessageBox.critical(QtGui.QDialog(), "Query", "Invalid Query")
        
        # Get columns on which a trigger is defined (The trigger is released when event on this column happened)
        # These columns are therefore not the targets of triggers !
        """SELECT * FROM information_schema.triggered_update_columns WHERE event_object_table = 'od_pipe';"""

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def initProgressBar(self):
        
        self.bar = progress_bar();self.bar.center();self.bar.show()
        self.bar.progressBar = self.bar.ui_progbar.progressBar
        self.bar.progressBar.setValue(0)
        self.progress = 0; 
        self.barInc = 1.0/self.barCount*100.0
        self.barInc = 1.0/self.barCount*100.0


class progress_bar(QtGui.QWidget):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui_progbar = Ui_progressBar()
        self.ui_progbar.setupUi(self)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



                
                