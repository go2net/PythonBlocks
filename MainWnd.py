
import sip
sip.setapi('QVariant', 2)

import sys, os

from blocks.WorkspaceController import WorkspaceController
from generators.PythonGen import PythonGen

from PyQt4 import QtGui,QtCore, uic

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDockWidget

class MainWnd(QtGui.QMainWindow):
    instance = None
    def __init__(self):

        super(MainWnd, self).__init__()
        self.filename = None

        uic.loadUi('main.ui', self)    

        self.connect(self.actionNew, QtCore.SIGNAL('triggered()'), self.onNew)
        self.connect(self.actionOpen, QtCore.SIGNAL('triggered()'), self.onOpen)
        self.connect(self.actionSave, QtCore.SIGNAL('triggered()'), self.onSave)
        self.connect(self.actionSaveAs, QtCore.SIGNAL('triggered()'), self.onSaveAs)
        self.connect(self.actionRun, QtCore.SIGNAL('triggered()'), self.onRun)
        self.actionSaveAll.triggered.connect(self.onSaveAll)

        #self.connect(self.tabWidget,QtCore.SIGNAL("currentChanged(int)"),self.currentChanged)

        self.actionStop.setEnabled(False)

        self.viewGroup = QtGui.QActionGroup(self)
        self.viewGroup.addAction(self.actionTestBench)
        self.viewGroup.addAction(self.actionBlockEditor)
        self.viewGroup.addAction(self.actionDrawersets)
        self.actionBlockEditor.setChecked(True)

        self.connect(self.viewGroup,QtCore.SIGNAL("triggered(QAction*)"),self.onActionTriggered)               

        self.actionQuit.triggered.connect(self.close)
       
        # Create a new WorkspaceController
        self.wc = WorkspaceController(self.pgBlockEditor)
        
        #self.createBlockFactory("support\\lang_def.xml")
        
        self.resetWorksapce()
        self.InitBlockGenusListWidget()
        self.InitBlockDrawerSetsTreeWidget()
        self.setActiveWidget(self.pgBlockEditor)

        self.show()

        layout  = QtGui.QHBoxLayout()
        self.wndPreview.setLayout(layout);
        self.wndApplyGenus.hide()
        self.lwBlockGenus.setMainWnd(self)
        #self.blockPreviewWnd.resizeEvent = self.onResize
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
    def getInstance():
        print(MainWnd.instance)
        if(MainWnd.instance == None): 
            MainWnd.instance = MainWnd()
            print()
        return MainWnd.instance
     
    def __createDockWindow(self, name):
        """
        Private method to create a dock window with common properties.
        
        @param name object name of the new dock window (string)
        @return the generated dock window (QDockWindow)
        """
        dock = QDockWidget()
        dock.setObjectName(name)
        dock.setFeatures(
            QDockWidget.DockWidgetFeatures(QDockWidget.AllDockWidgetFeatures))
        return dock
  
    def __setupDockWindow(self, dock, where, widget, caption):
        """
        Private method to configure the dock window created with
        __createDockWindow().
        
        @param dock the dock window (QDockWindow)
        @param where dock area to be docked to (Qt.DockWidgetArea)
        @param widget widget to be shown in the dock window (QWidget)
        @param caption caption of the dock window (string)
        """
        if caption is None:
            caption = ""
        self.addDockWidget(where, dock)
        dock.setWidget(widget)
        dock.setWindowTitle(caption)
        dock.show()
        
  
    def createBlockFactory(self,  lang_file):
        from FactoryTreeView import  FactoryTreeView
        
        self.wc.resetWorkspace();
        root = self.wc.setLangDefFilePath(lang_file)
        self.wc.loadFreshWorkspace();
        
        self.blocksFactory = self.__createDockWindow("blocksFactory")
        
        self.factoryWidget = QtGui.QWidget()       

        layout  = QtGui.QVBoxLayout()        
        
        self.searchTxtBox = QtGui.QTextEdit()     
        self.searchTxtBox.setMaximumHeight(23)        
        
        self.factoryBlockTree = FactoryTreeView(root)     
     
        layout.addWidget(self.searchTxtBox)     
        layout.addWidget(self.factoryBlockTree) 
        layout.setContentsMargins(0, 0, 0, 0)

        self.factoryWidget.setLayout(layout)

        self.__setupDockWindow(self.blocksFactory, Qt.LeftDockWidgetArea,
                               self.factoryWidget, self.tr("Blocks Factory"))            
  
    def setActiveWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        if widget == self.pgHome:
            self.blockGenusWnd.hide()
            self.blockPropWnd.hide()   
            self.drawerSetsWnd.hide()       
        if widget == self.pgBlockEditor:
            self.blockGenusWnd.hide()
            self.blockPropWnd.show() 
            self.drawerSetsWnd.hide()       
        if widget == self.pgDrawerSets:  
            self.blockGenusWnd.show()
            self.drawerSetsWnd.show()
            self.lwBlockGenus.setDragEnabled(True)
            self.lwBlockGenus.setDragDropMode(QtGui.QAbstractItemView.DragOnly); 
            self.blockPropWnd.hide()

    def onActionTriggered(self, action):
        if action == self.actionTestBench:
            widget = self.pgHome
        if action == self.actionBlockEditor:
            widget = self.pgBlockEditor    
        if action == self.actionDrawersets:  
            widget = self.pgDrawerSets        
        self.setActiveWidget(widget)
            
    def InitBlockGenusListWidget(self):
        from blocks.BlockGenus import BlockGenus
        
        for name in sorted(BlockGenus.nameToGenus):
          item = QtGui.QListWidgetItem()
          item.setText(name)
          item.setData(QtCore.Qt.UserRole, BlockGenus.nameToGenus[name])
          self.lwBlockGenus.addItem(item)

        self.lwBlockGenus.itemSelectionChanged.connect(self.onBlockGenusItemChanged)

    def onBlockGenusItemChanged(self):
        from components.BlockGenusTreeModel import BlockGenusTreeModel
        from components.propertyeditor.QVariantDelegate import QVariantDelegate
        #print('onBlockGenusItemChanged')
        items = self.lwBlockGenus.selectedItems()    
        if(len(items) != 1): return
        item = items[0]

        genus = item.data(QtCore.Qt.UserRole)
        drawerSetsFile = os.getcwd() + "\\"+ "support\\block_drawersets.xml"
        self.genusTreeModel = BlockGenusTreeModel(self.tvBlockGenusView, self, genus, drawerSetsFile)
        self.tvBlockGenusView.init()
        self.tvBlockGenusView.setModel(self.genusTreeModel)
        self.tvBlockGenusView.setItemDelegate(QVariantDelegate(self.tvBlockGenusView));
        self.tvBlockGenusView.expandAll()
        
        #isStarterIndex = model.getIndexForNode(model.properties['connectors'])
        #self.tvBlockGenusView.setIndexWidget(isStarterIndex, QtGui.QCheckBox())
    
    def InitBlockDrawerSetsTreeWidget(self):
        #from components.DrawerSetsTreeView import DrawerSetsTreeView
        #langDefLocation = os.getcwd() + "\\"+ "support\\block_genuses.xml"
        #print('InitBlockDrawerSetsTreeWidget')
        #root = self.wc.setLangDefFilePath("support\\lang_def.xml")
        #self.wc.loadFreshWorkspace();
        self.tvDrawerSets.init("support\\block_drawersets.jason")
        #self.drawerSetsModel = DrawerSetsTreeModel(self.tvDrawerSets, self, langDefLocation)
        #self.tvDrawerSets.setModel(self.drawerSetsModel)
        #self.tvDrawerSets.expandAll()
        
        #factory = self.wc.workspace.factory
        #for canvas in reversed(factory.canvas.findChildren(FactoryCanvas)) :
        #    print(canvas.name)
        return    
        pass
    
    def onBlockClick(self, block):
        from components.BlockPropTreeModel import BlockPropTreeModel
        from components.propertyeditor.QVariantDelegate import QVariantDelegate

        model = BlockPropTreeModel(self, block)
        self.tvBlockPropView.init()
        self.tvBlockPropView.setModel(model)
        self.tvBlockPropView.setItemDelegate(QVariantDelegate(self.tvBlockPropView));
        self.tvBlockPropView.expandAll()
        pass

    def showBlock(self, genus):
        #from blocks.BlockGenus import BlockGenus
        from blocks.Block import Block
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock
    
        if(genus == None): return   
    
        block = Block.createBlockFromID(None, genus.genusName)
            
        child_list = self.wndPreview.findChildren(FactoryRenderableBlock)
        for i in reversed(range(len(child_list))): 
            child_list[i].deleteLater()
    
        factoryRB = FactoryRenderableBlock.from_block(None, block)
            
        factoryRB.setParent(self.wndPreview)
        factoryRB.show()  
            
        factoryRB.move((self.wndPreview.width() - factoryRB.width())/2, (self.wndPreview.height() - factoryRB.height())/2)
    
        pass

    def onResize(self, event):
        from blocks.FactoryRenderableBlock import FactoryRenderableBlock

        print('onResize')
        child_list = self.wndPreview.findChildren(FactoryRenderableBlock)
        if(len(child_list) != 1): return
        factoryRB = child_list[0]

        factoryRB.move((self.wndPreview.width() - factoryRB.width())/2, (self.wndPreview.height() - factoryRB.height())/2)

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
        try:
            gen = PythonGen(WorkspaceController.workspace)
            code = gen.workspaceToCode()
            print(code)
            exec(code)
        except:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
          print(exc_type, fname, exc_tb.tb_lineno,exc_obj)
        #pass

    def loadFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.', "Block file (*.blks);;All files (*.*)" )

        if(filename == ''): return   # User cancel load

        self.filename = filename

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
           #self.wc.resetWorkspace();
           self.wc.loadProjectFromPath(filename);

    def onSave(self):        
        widget = self.stackedWidget.currentWidget()
        if widget == self.pgHome:
            pass     
        if widget == self.pgBlockEditor:
            self.onSaveBlockEditor()   
        if widget == self.pgDrawerSets:  
            self.onSaveDrawerSets()         

    def onSaveBlockEditor(self):        
        import codecs
        filename = self.filename
        if(filename == None or filename == ''):
            filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".blks(*.blks)")
            if(filename == ''): return   # User cancel load 
          
        block_file = codecs.open(filename, "w",'utf-8')
        block_file.write(self.wc.getSaveString())
        block_file.close()

    def onSaveDrawerSets(self):        
        import codecs

        drawerSetsFileName = 'support\\block_drawersets.jason'
          
        file = codecs.open(drawerSetsFileName, "w",'utf-8')        
        file.write(self.tvDrawerSets.getSaveString())
        file.close()
        
        genusFileName = 'support\\block_genuses.jason'
          
        file = codecs.open(genusFileName, "w",'utf-8')        
        file.write(self.lwBlockGenus.getSaveString())
        file.close()        

        
    def onSaveAs(self):
        import codecs
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".blks(*.blks)")

        if(filename == ''): return   # User cancel load 
          
        block_file = codecs.open(filename, "w",'utf-8')
        block_file.write(self.wc.getSaveString())
        block_file.close()

    def onSaveAll(self):
        print('onSaveAll')
        
    def resetWorksapce(self):
        self.wc.resetWorkspace();
        self.wc.setLangDefFilePath("support\\lang_def.xml")
        self.wc.loadFreshWorkspace();
        self.wc.initWorkspacePanel()

        self.saveFilePath = None;
        self.saveFileName = "untitled";
        self.workspaceEmpty = True;
