from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QVariantDelegate(QtGui.QItemDelegate):
    def __inti__(self, parent):
        super(QVariantDelegate, self).__init__(parent)
        self.m_finishedMapper =  QtCore.QSignalMapper(self);
        self.connect(self.m_finishedMapper, QtCore.SIGNAL("mapped(QtGui.QWidget*)"), self, QtCore.SIGNAL("commitData(QtGui.QWidget*)"));
        self.connect(self.m_finishedMapper, QtCore.SIGNAL("mapped(QWidget*)"), self, QtCore.SIGNAL("closeEditor(QWidget*)"));
    
    def createEditor(self, parent, option , index ):
        editor = None
        p = index.internalPointer()
    
        obj_type = p.obj_type
        if(obj_type != None):     
            editor = p.createEditor(self, parent, option);
            if (editor != None):
                if (editor.metaObject().indexOfSignal("editFinished()") != -1):
                    self.connect(editor, QtCore.SIGNAL("editFinished()"), self.m_finishedMapper, QtCore.SLOT("map()"));
                    self.m_finishedMapper.setMapping(editor, editor);

                if (editor.metaObject().indexOfSignal("currentIndexChanged(int)") != -1):
                    self.connect(editor, QtCore.SIGNAL("currentIndexChanged(int)"), self.currentIndexChanged)

        else:
            editor = super(QVariantDelegate, self).createEditor(parent, option, index)

        #self.parseEditorHints(editor, p.editorHints());
        return editor;
  
  
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
        #self.closeEditor.emit(self.sender(), QAbstractItemDelegate.NoHint)
        #self.emit(SIGNAL("commitData(QWidget*)"), self.sender())
        #self.emit(SIGNAL("closeEditor(QWidget*)"), self.sender())
        pass
        
    def setModelData(self, editor, model, index) :
        data = index.model().data(index, Qt.EditRole);  
        obj_type = index.internalPointer().obj_type
        if(obj_type != None):  
            data = index.internalPointer().editorData(editor);
            if (data != None):
                model.setData(index, data , Qt.EditRole); 
        else:
            super(QVariantDelegate, self).setModelData(editor, model, index)

    
    def setEditorData (self, editor, index):
        #self.m_finishedMapper.blockSignals(True);
        data = index.model().data(index, QtCore.Qt.EditRole);   
        
        obj_type = index.internalPointer().obj_type
        if(obj_type != None):              
            index.internalPointer().setEditorData(editor, data)     
        else:
            super(QVariantDelegate, self).setEditorData(editor, index)

    def updateEditorGeometry(self, editor, option,  index ):
        return QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index);

    
    def sizeHint (self, option, index):
        size=QtGui.QItemDelegate.sizeHint(self, option, index);
        #h=size.height();

        size.setHeight(21);
        return size;
   
    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor) 
