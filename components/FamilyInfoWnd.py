from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import os

class FamilyInfoWnd(QDialog):
    def __init__(self, treeModel, genus):
        from MainWnd import MainWnd
        super(FamilyInfoWnd, self).__init__(MainWnd.getInstance())
        self.genus = genus
        self.treeModel = treeModel
        dirname, filename = os.path.split(os.path.abspath(__file__))
        loadUi(dirname+'\\family_info.ui', self)   
        
        self.btnAddFamily.clicked.connect(self.onAddFamily)
        self.btnDelFamily.clicked.connect(self.onDelFamily)
        self.btnAddVar.clicked.connect(self.onAddVar)
        self.btnDelVar.clicked.connect(self.onDelVar)       
        
        self.btnOk.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)

    def onAddFamily(self): 
        familyName = self.edtFamily.text()
        item = QListWidgetItem(familyName)
        self.familyList.addItem(item)
        return
        
    def onDelFamily(self):        
        return        
        
    def onAddVar(self):  
        varName = self.edtVar.text()
        item = QListWidgetItem(varName)
        self.variableList.addItem(item)        
        return        
        
    def onDelVar(self):
        return
        
        self.tableView.model().addImage()
        #return self.createIndex(node.row(), 1, node)   
        #self.tableView.itemDelegate().dataChanged.emit(self.tableView)

