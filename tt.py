from PyQt4 import QtGui, QtCore

class Food(object):
    def __init__(self, name, shortDescription, note, parent = None):
        self.data = (name, shortDescription, note);
        self.parentIndex = parent

class FavoritesTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.foods = []  
        self.loadData() 

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self.foods[index.row()].data[index.column()]
        return None

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.foods)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 3

    def index(self, row, column, parent = QtCore.QModelIndex()):  
        return self.createIndex(row, column, parent)

    def loadData(self):   
        allFoods=("Apples", "Pears", "Grapes", "Cookies", "Stinkberries")
        allDescs = ("Red", "Green", "Purple", "Yummy", "Huh?")
        allNotes = ("Bought recently", "Kind of delicious", "Weird wine grapes",
                    "So good...eat with milk", "Don't put in your nose")
        for name, shortDescription, note in zip(allFoods, allDescs, allNotes):
            food = Food(name, shortDescription, note)                                      
            self.foods.append(food) 

def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    model = FavoritesTableModel() 

    #Table view
    view1 = QtGui.QTableView()
    view1.setModel(model)
    view1.show()

    #Tree view
    view2 = QtGui.QTreeView()
    view2.setModel(model)
    view2.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
