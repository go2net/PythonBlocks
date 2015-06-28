#!/usr/bin/env python

from PyQt4 import QtCore

class TreeItem(object):
  def __init__(self, data, parent=None):
      self.parentItem = parent
      self.itemData = data
      self.childItems = []
      
  def columnCount(self):
      return 2 #len(self.childItems)

  def childCount(self):
      return 2 #len(self.childItems)

  def child(self, row):
      return None #self.childItems[row]

  def data(self, column):
      try:
          return self.itemData[column]
      except IndexError:
          return None

      
class BlockGenusTreeModel(QtCore.QAbstractItemModel):
  def __init__(self, genus, parent=None):
    super(BlockGenusTreeModel, self).__init__(parent)
    
    self.rootItem = TreeItem(("Property", "Value"))
    self.setupModelData(genus, self.rootItem)
        
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
 
  def setupModelData(self, genus, parent):
    pass
