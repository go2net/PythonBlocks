from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from blocks.BlockGenus import BlockGenus
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
        
        self.btnOk.clicked.connect(self.onOk)
        self.btnCancel.clicked.connect(self.reject)

        self.edtFamily.textChanged.connect(self.onFamilyNameChanged)
        self.familyList.itemSelectionChanged .connect(self.onFamilyListSelectionChanged)
        self.familyList.setSelectionMode(QAbstractItemView.SingleSelection)

        self.edtVar.textChanged.connect(self.onVarNameChanged)
        self.varList.itemSelectionChanged .connect(self.onVarListSelectionChanged)
        self.varList.setSelectionMode(QAbstractItemView.SingleSelection)
        
        for familyName in BlockGenus.families:
            item = QListWidgetItem(familyName)
            self.familyList.addItem(item) 

        self.families = {}

    def onOk(self):
        items = self.allFamilyNames()
        for familyName in items:
             self.families[familyName] = []
             
        return self.accept()

    def allFamilyNames(self):
        items = []
        for i in range(self.familyList.count()):
            items.append(self.familyList.item(i).text())
        return items
        
    def allVarNames(self,  familyName):
        return self.families[familyName]        

    def onFamilyNameChanged(self):
        familyName = self.edtFamily.text().strip()
        items = self.allFamilyNames()
        self.btnAddFamily.setEnabled(familyName != '' and self.edtFamily.text() not in items)
        
    def onVarNameChanged(self):
        listItems=self.familyList.selectedItems()
        if not listItems: 
            self.btnDelFamily.setEnabled(False)
            return
            
        item = listItems[0]
        familyName = item.text()
        
        varName = self.edtVar.text().strip()
        items = self.allVarNames(familyName)
        self.btnAddVar.setEnabled(varName != '' and self.edtVar.text() not in items) 

    def onFamilyListSelectionChanged(self): 
        listItems=self.familyList.selectedItems()
        if not listItems: 
            self.btnDelFamily.setEnabled(False)
            return
            
        item = listItems[0]
        familyName = item.text()
        
        self.varList.clear()
        for varName in self.families[familyName]:
            self.varList.addItem(varName)         
        
        self.edtFamily.setText(familyName)
        self.btnDelFamily.setEnabled(True)
        
        self.onVarNameChanged()

    def onVarListSelectionChanged(self): 
        listItems=self.varList.selectedItems()
        if not listItems: 
            self.btnDelVar.setEnabled(False)
            return
            
        item = listItems[0]
        varName = item.text() 
        
        self.edtVar.setText(varName)
        self.btnDelVar.setEnabled(True)

    def onAddFamily(self):
        familyName = self.edtFamily.text().strip()
        item = QListWidgetItem(familyName)
        self.familyList.addItem(item)
        self.onFamilyNameChanged()
        self.edtFamily.setText('')
        
        self.families[familyName] = []
        
        return
        
    def onDelFamily(self):
        listItems=self.familyList.selectedItems()
        if not listItems: 
            return
            
        for item in listItems:
            familyName = item.text()
            self.familyList.takeItem(self.familyList.row(item))          
            if familyName in self.families: 
                del self.families[familyName]
        
        self.onFamilyNameChanged()
        
    def onAddVar(self):
        listItems=self.familyList.selectedItems()
        print(listItems)
        if not listItems or len(listItems) != 1: 
            return
        
        item = listItems[0]
        familyName = item.text()   
        
        varName = self.edtVar.text().strip()
        self.families[familyName].append(varName)
        
        item = QListWidgetItem(varName)
        self.varList.addItem(item)
        self.onVarNameChanged()
        self.edtVar.setText('') 
        
        return
        
    def onDelVar(self):
        listItems=self.familyList.selectedItems()
        if not listItems or len(listItems) != 1: 
            return
            
        item = listItems[0]
        familyName = item.text()   
        
        listItems = self.varList.selectedItems()
        if not listItems: 
            return  
        
        for item in listItems:            
            self.varList.takeItem(self.varList.row(item)) 
            self.families[familyName].remove(item.text())       
        
        self.onVarNameChanged()

