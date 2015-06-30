import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

####################################################################
def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

####################################################################
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        # create objects
        list_data = [1,2,3,4]
        lm = MyListModel(list_data, self)
        de = MyDelegate(self)
        lv = QTreeView()

        lv.setItemDelegate(de)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(lv)
        self.setLayout(layout)
        lv.setModel(lm)
####################################################################
class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.red))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        if value:
            print(value)
            text = str(value)
            painter.drawText(option.rect, Qt.AlignLeft, text)

        painter.restore()

####################################################################
class MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return self.listdata[index.row()]
        else:
            return None # QVariant()

####################################################################
if __name__ == "__main__":
    main()
