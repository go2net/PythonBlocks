#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from ConnectorsInfoWnd import ConnectorsInfoWnd

class TreeItem(object):
  def __init__(self, data, parent=None):
      self.parentItem = parent
      self.itemData = data
      self.childItems = []
     
  def columnCount(self):
      return len(self.itemData)
      
  def childCount(self):
      return len(self.childItems)
      
  def child(self, row):
      return self.childItems[row]
      
  def data(self, column):
      try:
          return self.itemData[column]
      except IndexError:
          return None
          
  def parent(self):
    return self.parentItem
        
  def appendChild(self, item):
      self.childItems.append(item)
 
class BlockGenusTreeModel(QPropertyModel):
  
  def __init__(self, mainWnd, genus, langDefLocation, parent=None):
    super(BlockGenusTreeModel, self).__init__(parent)
    self.properties = {}
    self.mainWnd = mainWnd
    self.langDefLocation = langDefLocation
    self.rootItem = TreeItem(("Property", "Value"))
    self.setupModelData(genus, self.m_rootItem)

    
  '''      
  def columnCount(self, parent):
      if parent.isValid():
          return parent.internalPointer().columnCount()
      else:
          return self.rootItem.columnCount()    
 
  def rowCount(self, parent):
      if parent.column() > 0:
          return 0

      if not parent.isValid():
          parentItem = self.rootItem
      else:
          parentItem = parent.internalPointer()

      return parentItem.childCount()
 

  def index(self, row, column, parent):
    if not self.hasIndex(row, column, parent):
        return QtCore.QModelIndex()

    if not parent.isValid():
        parentItem = self.rootItem
    else:
        parentItem = parent.internalPointer()

    childItem = parentItem.child(row)
    if childItem:
        return self.createIndex(row, column, childItem)
    else:
        return QtCore.QModelIndex()
 
  def headerData(self, section, orientation, role):
      if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
          return self.rootItem.data(section)

      return None 
  '''
  def setupModelData(self, genus, parent):
    parents = [parent]
    self.mainWnd.showBlock(genus)
    
    #columnData = ['A','B']  
    #print(genusNode.attrib)
    #
    self.properties['genusName'] = Property('Genus Name', genus.genusName, parents[-1])    
    self.properties['kind'] = Property('Genus Kind', genus.kind, parents[-1], Property.COMBO_BOX_EDITOR, ['command', 'data', 'function', 'param','procedure','variable'])
    self.properties['initLabel'] = Property('Init Label', genus.initLabel, parents[-1])
    self.properties['labelPrefix'] = Property('Label Prefix', genus.labelPrefix, parents[-1])
    self.properties['labelSuffix'] = Property('Label Suffix', genus.labelSuffix, parents[-1])    
    self.properties['color'] = Property('Color',genus.color , parents[-1], Property.COLOR_EDITOR)
       
    self.properties['connectors'] = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)    

    self.all_connectors = genus.sockets
    
    plug_index = 0
    socket_index = 0
    
    if genus.plug != None:
      Property('Plug #'+str(plug_index), '',  self.properties['connectors'])
    
    for connector in genus.sockets:
      
      connector_kind = connector.kind
      if(connector_kind == 0):
        Property('Socket #'+str(socket_index), '',  self.properties['connectors'])
        socket_index += 1
      else:
        Property('Plug #'+str(plug_index), '',  self.properties['connectors'])
        plug_index += 1
    
    lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
    for key in genus.properties:
      Property(key,genus.properties[key], lang_root)
    
    self.properties['connectors'].onAdvBtnClick = self.onShowConnectorsInfo
    
  def onShowConnectorsInfo(self):

    dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
    dlg.exec_()
    print('onShowConnectorsInfo')

  #def dataChanged ( topLeft, bottomRight ):
  #  print('dataChanged')

  '''  
  def parent(self, index):
    if not index.isValid():
      return QtCore.QModelIndex()

    childItem = index.internalPointer()
    parentItem = childItem.parent()

    if parentItem == self.rootItem:
        return QtCore.QModelIndex()
         
  def data(self, index, role):
      if not index.isValid():
          return None

      if role != QtCore.Qt.DisplayRole:
          return None

      item = index.internalPointer()

      return item.data(index.column())
      
  def flags(self, index):
      if not index.isValid():
          return 0

      return QtCore.Qt.ItemIsTristate |QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable  
  ''' 
