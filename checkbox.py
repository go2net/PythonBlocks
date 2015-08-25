from PyQt4 import QtCore, QtGui
import sys

class Node(object):   
    def __init__(self, name, parent=None, checked=False):

        self._name = name
        self._children = []
        self._parent = parent
        self._checked = checked

        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def name(self):
        return self._name

    def checked(self):
        return self._checked

    def setChecked(self, state):
        self._checked = state

        for c in self._children:
            c.setChecked(state)

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super().__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()
        if role == QtCore.Qt.CheckStateRole:
            if node.checked():
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            if role == QtCore.Qt.CheckStateRole:
                node = index.internalPointer()
                node.setChecked(not node.checked())
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return "Nodes"

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsUserCheckable

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

def main_simple():
    app = QtGui.QApplication(sys.argv)

    rootNode   = Node("Root")
    n1 = Node("Node1", rootNode)
    n2 = Node("Node2", rootNode)
    n3 = Node("Node3", rootNode)

    n1_1 = Node("Node1 1", n1)
    n1_2 = Node("Node1 2", n1)
    n1_3 = Node("Node1 3", n1)

    n2_1 = Node("Node2 1", n2)
    n2_2 = Node("Node2 2", n2)
    n2_3 = Node("Node2 3", n2)

    n3_1 = Node("Node3 1", n3)
    n3_2 = Node("Node3 2", n3)
    n3_3 = Node("Node3 3", n3)

    model = TreeModel(rootNode)

    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main_simple()
