#!/usr/bin/env python

from components.propertyeditor.QPropertyModel import  QPropertyModel
from components.propertyeditor.Property import Property

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


from PyQt4 import QtCore

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
  def __init__(self, genus, langDefLocation, parent=None):
    super(BlockGenusTreeModel, self).__init__(parent)
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
    tree = etree.parse(self.langDefLocation)
    root = tree.getroot()
    all_genus = root.findall('BlockGenus')
 
    genusNode = None
 
    for node in all_genus:
      if(node.attrib["name"] == genus.getGenusName()):
        genusNode = node
        break
 
    if(genusNode == None): return
    
    #columnData = ['A','B']  
    #print(genusNode.attrib)
    #
    Property('Genus Name', genusNode.attrib["name"], parents[-1])
    
    if('kind' in genusNode.attrib):
      Property('Genus Kind', genusNode.attrib["kind"], parents[-1])
    else:
      Property('Genus Kind', '', parents[-1])
      
    if('initlabel' in genusNode.attrib):
      
      Property('Init Label', genusNode.attrib["initlabel"], parents[-1])
    else:
      Property('Init Label', '', parents[-1]) 
    
    if('label-prefix' in genusNode.attrib):  
      Property('label-prefix', genusNode.attrib["label-prefix"], parents[-1])
    else:
      Property('label-prefix', '', parents[-1])
      
    if('label-suffix' in genusNode.attrib):    
      Property('label-suffix', genusNode.attrib["label-suffix"], parents[-1])
    else:
      Property('label-suffix', '', parents[-1])
    
    
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
