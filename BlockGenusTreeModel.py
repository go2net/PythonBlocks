#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property
from ConnectorsInfoWnd import ConnectorsInfoWnd
try:
  from lxml import etree
  #from lxml import ElementInclude
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    #from xml.etree import ElementInclude
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      #from xml.etree import ElementInclude
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree        
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


from PyQt4 import QtCore, QtGui

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
    from blocks.BlockGenus import BlockGenus
    parents = [parent]
    tree = etree.parse(self.langDefLocation)
    root = tree.getroot()
    all_genus = root.findall('BlockGenus')
 
    genusNode = None
 
    for node in all_genus:
      if(node.attrib["name"] == genus.getGenusName()):
        genusNode = node
        break
 
    if(node == None): return
    
    genus = BlockGenus.loadGenus(node)
    
    self.mainWnd.showBlock(genus)
    
    #columnData = ['A','B']  
    #print(genusNode.attrib)
    #
    Property('Genus Name', genus.genusName, parents[-1])    
    Property('Genus Kind', genus.kind, parents[-1])
    Property('Init Label', genus.initLabel, parents[-1])
    Property('Label Prefix', genus.labelPrefix, parents[-1])
    Property('Label Suffix', genus.labelSuffix, parents[-1])    
    Property('Color',genus.color , parents[-1], Property.COLOR_EDITOR)
       
    connectors_root = Property('Connectors','', parents[-1],Property.ADVANCED_EDITOR)    

    self.all_connectors = genus.sockets
    
    plug_index = 0
    socket_index = 0
    
    if genus.plug != None:
      connector_root = Property('Plug #'+str(plug_index), '',  connectors_root)
    
    for connector in genus.sockets:
      
      connector_kind = connector.kind
      if(connector_kind == 0):
        connector_root = Property('Socket #'+str(socket_index), '',  connectors_root)
        socket_index += 1
      else:
        connector_root = Property('Plug #'+str(plug_index), '',  connectors_root)
        plug_index += 1
    
    lang_root = Property('Language','', parents[-1],Property.ADVANCED_EDITOR) 
    for key in genus.properties:
      Property(key,genus.properties[key], lang_root)
    
    connectors_root.onAdvBtnClick = self.onShowConnectorsInfo
    
  def onShowConnectorsInfo(self):

    dlg = ConnectorsInfoWnd(self.mainWnd, self.all_connectors)
    dlg.exec_()
    print('onShowConnectorsInfo')

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
