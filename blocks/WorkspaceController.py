#-------------------------------------------------------------------------------
# Name:        WorkspaceController.py
# Purpose:
#
# Author:      Jack.Shi
#
# Created:     02/03/2015
# Copyright:   (c) 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os

from xml.dom.minidom import Document

try:
  from lxml import etree
  from lxml import ElementInclude
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    from xml.etree import ElementInclude
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      from xml.etree import ElementInclude
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree        
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


from PyQt4 import QtGui

from blocks.BlockGenus  import BlockGenus
from blocks.BlockConnectorShape import BlockConnectorShape
from blocks.BlockLinkChecker import BlockLinkChecker
from blocks.Workspace import Workspace

class WorkspaceController():

   workspace = None


   def __init__(self,frame):
      '''
      Constructs a WorkspaceController instance that manages the
      interaction with the codeblocks.Workspace
      '''
      self.LANG_DEF_FILEPATH = ""
      self.langDefRoot = None
      self.workspacePanel = frame

      # flags
      self.isWorkspacePanelInitialized = False

      # The single instance of the Workspace Controller
      WorkspaceController.workspace = Workspace();

      # flag to indicate if a workspace has been loaded/initialized
      self.workspaceLoaded = False

      # flag to indicate if a new lang definition file has been set
      self.langDefDirty = True



   def setLangDefFilePath(self,filePath):
      '''
      Sets the file path for the language definition file, if the
      language definition file is located in
      '''
      self.LANG_DEF_FILEPATH = filePath; # TODO do we really need to save the file path?

      # DocumentBuilderFactory factory=DocumentBuilderFactory.newInstance();
      # DocumentBuilder builder;
      # Document doc;

      try:
         langDefLocation = os.getcwd() + "\\"+ self.LANG_DEF_FILEPATH
         tree = etree.parse(langDefLocation)
         root = tree.getroot()
         ElementInclude.include(root)
         self.langDefRoot = root
         # set the dirty flag for the language definition file
         # to true now that a new file has been set
         self.langDefDirty = True;

      except:
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         print(exc_type, fname, exc_tb.tb_lineno,exc_obj)


   def loadFreshWorkspace(self):
      '''
      Loads a fresh workspace based on the default specifications in the language
      definition file.  The block canvas will have no live blocks.
      '''

      # need to just reset workspace (no need to reset language) unless
      # language was never loaded

      # reset only if workspace actually exists
      if(self.workspaceLoaded):
         self.resetWorkspace()

      if(self.langDefDirty):
         self.loadBlockLanguage(self.langDefRoot)

      self.workspace.loadWorkspaceFrom(None, self.langDefRoot)

      self.workspaceLoaded = True


   def resetWorkspace(self):
      '''
      Resets the entire workspace.  This includes all blocks, pages, drawers, and trashed blocks.
      Also resets the undo/redo stack.  The language (i.e. genuses and shapes) is not reset.
      '''

      # clear all pages and their drawers
      # clear all drawers and their content
      # clear all block and renderable block instances
      self.workspace.reset()
      pass
      # clear action history
      # rum.reset()

      # clear runblock manager data
      # rbm.reset()

   def reset(self):
      '''
      Clears the Workspace of:
       - all the live blocks in the BlockCanvas.
       - all the pages on the BlockCanvas
       - all its BlockDrawers and the RB's that reside within them
       - clears all the BlockDrawer bars of its drawer references and
         their associated buttons
       - clears all RenderableBlock instances (which clears their associated
         Block instances.)
       Note: we want to get rid of all RendereableBlocks and their
       references.

       Want to get the Workspace ready to load another workspace
     '''


      # we can't iterate and remove widgets at the same time so
      # we remove widgets after we've collected all the widgets we want to remove
      # TreeSet.remove() doesn't always work on the TreeSet, so instead,
      # we clear and re-add the widgets we want to keep

      #widgetsToRemove = []
      #widgetsToKeep = []

      '''      for(WorkspaceWidget w : workspaceWidgets){
     if(w instanceof Page){
        widgetsToRemove.add(w);
     }else{
        widgetsToKeep.add(w);
     }
    }
    workspaceWidgets.clear();
    workspaceWidgets.addAll(widgetsToKeep);
    workspaceWidgets.add(factory);

    //We now reset the widgets we removed.
    //Doing this for each one gets costly.
    //Do not do this for Pages because on repaint,
    //the Page tries to access its parent.
    for (WorkspaceWidget w : widgetsToRemove){
       Container parent = w.getJComponent().getParent();
       if(w instanceof Page){
          ((Page)w).reset();
       }
      if(parent != null){
         parent.remove(w.getJComponent());
         parent.validate();
         parent.repaint();
      }
    }

  //We now reset, the blockcanvas, the factory, and the renderableblocks
  blockCanvas.reset();
  addPageAt(Page.getBlankPage(), 0, False); //TODO: System expects PAGE_ADDED event
  factory.reset();
  RenderableBlock.reset();
  revalidate();
  }'''


   def loadBlockLanguage(self, root):
      '''
      Loads all the block genuses, properties, and link rules of
      a language specified in the pre-defined language def file.
      @param root Loads the language specified in the Element root
      '''

      from blocks.SocketRule import SocketRule
      from blocks.CommandRule import CommandRule

      # load connector shapes
      # MUST load shapes before genuses in order to initialize connectors within
      # each block correctly
      BlockConnectorShape.loadBlockConnectorShapes(root)

      # load genuses
      BlockGenus.loadBlockGenera(root)

      # load rules
      BlockLinkChecker.addRule(CommandRule())
      BlockLinkChecker.addRule(SocketRule())

      # set the dirty flag for the language definition file
      # to false now that the lang file has been loaded
      self.langDefDirty = False


   #################################
   # TESTING CODEBLOCKS SEPARATELY #
   #################################

   def createAndShowGUI(wc):
      '''
      Create the GUI and show it.  For thread safety, this method should be
      invoked from the event-dispatching thread.
      '''

      print("Creating GUI...");
      wc.initWorkspacePanel()

      #Create and set up the window.
      #JFrame frame = new JFrame("OpenBlocks Demo");
      #frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      #  int inset = 50;
      #  Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();

      #frame.setBounds(100, 100, 800, 500);

      #create search bar
      #SearchBar searchBar = new SearchBar("Search blocks", "Search for blocks in the drawers and workspace", workspace);
      #for(SearchableContainer con : wc.getAllSearchableContainers())
      #{
      #   searchBar.addSearchableContainer(con);
      #}

      # create save button
      #JButton saveButton = new JButton("Save");
      #saveButton.addActionListener(new ActionListener() {
      # public void actionPerformed(ActionEvent e){
      #    System.out.println(workspace.getSaveString());
      # }
      #});

      #JPanel topPane = new JPanel();
      #searchBar.getComponent().setPreferredSize(new Dimension(130, 23));
      #topPane.add(searchBar.getComponent());
      #topPane.add(saveButton);
      #frame.add(topPane, BorderLayout.PAGE_START);
      #layout  = QtGui.QHBoxLayout()
      #frame.setLayout(layout )
      #layout.addWidget(wc.getWorkspacePanel())

      #frame.setVisible(true);


   def getWorkspacePanel(self):

      '''
      Returns the QFrame of the entire workspace.
      @return the QFrame of the entire workspace.
      '''

      if(not self.isWorkspacePanelInitialized):
         self.initWorkspacePanel();

      #self.workspacePanel.setStyleSheet("background-color: rgb(170, 255, 0);")
      return self.workspacePanel;


   def initWorkspacePanel(self):
      '''
      This method creates and lays out the entire workspace panel with its
      different components.  Workspace and language data not loaded in
      this function.
      Should be call only once at application startup.
      '''

      layout  = QtGui.QHBoxLayout()
      self.workspacePanel.setLayout(layout);
      layout.addWidget(self.workspace);

      self.isWorkspacePanelInitialized = True;



   def getSaveString(self):
         '''
         * Returns the save string for the entire workspace.  This includes the block workspace, any
         * custom factories, canvas view state and position, pages
         * @return the save string for the entire workspace.
      '''
      #try:
         doc = self.getSaveNode();

         #writer = StringWriter();
         #transformerFactory = TransformerFactory.newInstance();
         #transformer = transformerFactory.newTransformer();
         #transformer.setOutputProperty(OutputKeys.INDENT, "yes");
         #transformer.transform(DOMSource(node), StreamResult(writer));
         return doc.toprettyxml(indent='\t');
      #except:
      #   pass


   def getSaveNode(self,validate=True):

         '''
         * Returns a DOM node for the entire workspace. This includes the block
         * workspace, any custom factories, canvas view state and position, pages
         *
         * @param validate If {@code true}, perform a validation of the output
         * against the code blocks schema
         * @return the DOM node for the entire workspace.
         '''
      #try:
         doc = Document()
         documentElement = doc.createElement("CODEBLOCKS");
         # schema reference
         #documentElement.setAttributeNS(XMLConstants.W3C_XML_SCHEMA_INSTANCE_NS_URI, "xsi:schemaLocation", Constants.XML_CODEBLOCKS_NS+" "+Constants.XML_CODEBLOCKS_SCHEMA_URI);

         workspaceNode = WorkspaceController.workspace.getSaveNode(doc);
         if (workspaceNode != None):
            documentElement.appendChild(workspaceNode);


         doc.appendChild(documentElement);

         return doc;
      #except:
      #   pass

   def loadProjectFromPath(self, path):

      # XXX here, we could be strict and only allow valid documents...
      # validate(doc);
      projectRoot = etree.parse(path).getroot()
      # load the canvas (or pages and page blocks if any) blocks from the save file
      # also load drawers, or any custom drawers from file.  if no custom drawers
      # are present in root, then the default set of drawers is loaded from
      # langDefRoot
      WorkspaceController.workspace.loadWorkspaceFrom(projectRoot, self.langDefRoot);
      self.workspaceLoaded = True;


