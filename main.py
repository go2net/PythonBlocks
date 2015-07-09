#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:
#
# Author:      Jack.Shi
#
# Created:     02/03/2015
# Copyright:   (c) 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sip
sip.setapi('QVariant', 2)

import sys, os
#import Workspace
from blocks.WorkspaceController import WorkspaceController
from generators.PythonGen import PythonGen

from PyQt4 import QtGui,QtCore, uic

class MainWnd(QtGui.QMainWindow):

  def __init__(self):
    super(MainWnd, self).__init__()

    self.filename = None

    uic.loadUi('main.ui', self)

    QtCore.QObject.connect(self.actionNew, QtCore.SIGNAL('triggered()'), self.onNew)
    QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL('triggered()'), self.onOpen)
    QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.onSave)
    QtCore.QObject.connect(self.actionRun, QtCore.SIGNAL('triggered()'), self.onRun)

    self.actionStop.setEnabled(False)

    #self.btnExit.clicked.connect(self.close)
    self.actionQuit.triggered.connect(self.close)
    #self.frame.layout().setContentsMargins(0, 0, 0, 0)
    # Create a new WorkspaceController
    self.wc = WorkspaceController(self.frame)
    self.resetWorksapce()
    self.InitBlockGenusListWidget()
    self.show()

  def InitBlockGenusListWidget(self):
    from blocks.BlockGenus import BlockGenus
    
    for name in BlockGenus.nameToGenus:
      item = QtGui.QListWidgetItem()
      item.setText(name)
      item.setData(QtCore.Qt.UserRole, BlockGenus.nameToGenus[name])
      self.lwBlockGenus.addItem(item)
    
    self.lwBlockGenus.itemSelectionChanged.connect(self.onBlockGenusItemChanged)

  def onBlockGenusItemChanged(self):
    from BlockGenusTreeModel import BlockGenusTreeModel
    from components.propertyeditor.QVariantDelegate import QVariantDelegate
    items = self.lwBlockGenus.selectedItems()    
    if(len(items) != 1): return
    item = items[0]
    
    genus = item.data(QtCore.Qt.UserRole)
    langDefLocation = os.getcwd() + "\\"+ "support\\block_genuses.xml"
    model = BlockGenusTreeModel(self, genus, langDefLocation)
    self.tvBlockGenusView.init()
    self.tvBlockGenusView.setModel(model)
    self.tvBlockGenusView.setItemDelegate(QVariantDelegate(self.tvBlockGenusView));
    self.tvBlockGenusView.expandAll()
    
  def showBlock(self, genusNode):
    from blocks.Block import Block
    if(genusNode == None): return
    
    block = Block.loadBlockFrom(genusNode)
    print(block)
    pass
  
  def closeEvent(self, event):

    reply = QtGui.QMessageBox.question(self, 'Message',
       "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
       event.accept()
    else:
       event.ignore()


  def onNew(self):
    self.wc.resetWorkspace();

  def onOpen(self):
    if (self.isWorkspaceChanged()):
       quit_msg = "There have no saved change, do you want to save it?"
       reply = QtGui.QMessageBox.question(self, 'Message',
                      quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

       if reply == QtGui.QMessageBox.Yes:
          self.onSave();

    self.loadFile();
    #this.setTitle(makeFrameTitle());

  def onRun(self):
    #try:
      gen = PythonGen(WorkspaceController.workspace)
      code = gen.workspaceToCode()
      print(code)
      exec(code)
    #except:
    #  exc_type, exc_obj, exc_tb = sys.exc_info()
    #  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #  print(exc_type, fname, exc_tb.tb_lineno,exc_obj)
    #pass

  def loadFile(self):
    self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.', ".blks(*.blks)")
    print(self.filename)

    try:
       QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
       self.loadBlockFile(self.filename);
      #context.setWorkspaceChanged(false);
    #except:
    #   print("ERROR!")
    #   pass
    finally:
       QtGui.QApplication.restoreOverrideCursor()


  def isWorkspaceChanged(self):
    return False


  def loadBlockFile(self,filename):
    if (filename != None):
       #saveFilePath = savedFile.getAbsolutePath();
       #saveFileName = savedFile.getName();
       self.wc.resetWorkspace();
       self.wc.loadProjectFromPath(filename);
       #didLoad();

  def onSave(self):
    import codecs
    if(self.filename == None or self.filename == ''):
      self.filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".blks")
    block_file = codecs.open(self.filename, "w",'utf-8')
    block_file.write(self.wc.getSaveString())
    block_file.close()

  def resetWorksapce(self):
    self.wc.resetWorkspace();
    #self.wc.resetLanguage();
    #self.wc.setLangResourceBundle(ResourceBundle.getBundle("com/ardublock/block/ardublock"));
    #self.wc.setStyleList(list);
    #self.wc.setLangDefDtd(this.getClass().getResourceAsStream(LANG_DTD_PATH));
    #self.wc.setLangDefStream(this.getClass().getResourceAsStream(ARDUBLOCK_LANG_PATH));
    self.wc.setLangDefFilePath("support\\lang_def.xml")
    self.wc.loadFreshWorkspace();
    self.wc.initWorkspacePanel()

    #loadDefaultArdublockProgram();

    self.saveFilePath = None;
    self.saveFileName = "untitled";
    self.workspaceEmpty = True;

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  win = MainWnd()
  sys.exit(app.exec_())
