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
      editor = p.createEditor(parent, option);
      if (editor != None):
        if (editor.metaObject().indexOfSignal("editFinished()") != -1):
          self.connect(editor, QtCore.SIGNAL("editFinished()"), self.m_finishedMapper, QtCore.SLOT("map()"));
          self.m_finishedMapper.setMapping(editor, editor);

    else:
      editor = QtGui.QItemDelegate.createEditor(self, parent, option, index);

    #self.parseEditorHints(editor, p.editorHints());
    return editor;

  def parseEditorHints(self, editor, editorHints):
    return
    if (editor and not editorHints.isEmpty()):
      editor.blockSignals(True);
      # Parse for property values
      #QRegExp rx("(.*)(=\\s*)(.*)(;{1})");
      #rx.setMinimal(true);
      #int pos = 0;
      #while ((pos = rx.indexIn(editorHints, pos)) != -1) 

        # qDebug("Setting %s to %s", qPrintable(rx.cap(1)), qPrintable(rx.cap(3)));
        #editor->setProperty(qPrintable(rx.cap(1).trimmed()), rx.cap(3).trimmed());				
        #pos += rx.matchedLength();

      #editor->blockSignals(false);
  
    
  def setModelData(self, editor, model, index) :
    data = index.model().data(index, Qt.EditRole);	
    obj_type = index.internalPointer().obj_type
    if(obj_type != None):  
        data = index.internalPointer().editorData(editor);
        if (data != None):
          model.setData(index, data , Qt.EditRole); 
    else:
      QItemDelegate.setModelData(self, editor, model, index);

    
  def setEditorData (self, editor, index):

    #self.m_finishedMapper.blockSignals(True);
    data = index.model().data(index, QtCore.Qt.EditRole);	
    
    obj_type = index.internalPointer().obj_type
    if(obj_type != None): 
         
      index.internalPointer().setEditorData(editor, data)
 
    else:
      QtGui.QItemDelegate.setEditorData(self, editor, index);

    #self.m_finishedMapper.blockSignals(False);

  def updateEditorGeometry(self, editor, option,  index ):
    return QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index);

    
  def sizeHint (self, option, index):
    size=QtGui.QItemDelegate.sizeHint(self, option, index);
    #h=size.height();

    size.setHeight(21);
    return size;
   

  def paint(self,  painter,  option, index ):
    if (index.column() == 1):
      painter.save();
      painter.setPen(QtGui.QColor(240, 240, 240) );
      painter.drawRect(option.rect);
      painter.restore();

    QtGui.QItemDelegate.paint(self, painter, option, index);
