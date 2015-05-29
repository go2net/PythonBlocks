#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     10/03/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import SIGNAL
class LabelWidget(QtGui.QWidget):
  def __init__(self,initLabelText,  fieldColor, tooltipBackground):
      QtGui.QWidget.__init__(self)
      
      self.loading  = True;
      
      if(initLabelText == None): initLabelText = "";
      #self.setFocusTraversalKeysEnabled(False); # MOVE DEFAULT FOCUS TRAVERSAL KEYS SUCH AS TABS
      #self.setLayout(BorderLayout());
      self.tooltipBackground = tooltipBackground;
      self.labelBeforeEdit = initLabelText;

      self.textField = BlockLabelTextField(self)
      

      self.textLabel = ShadowLabel()
      self.hasSiblings = False
      self.isEditable = False
      self.editingText = False
      #self.setFocusPolicy(QtCore.Qt.StrongFocus)
      
      # set up textfield colors
      self.textField.setTextColor(QtCore.Qt.white); #white text
      
      self.textField.connect(self.textField, SIGNAL('textChanged()'), self.textChanged)
      #self.textField.textChanged.connect(self.textChanged)
      
      p = self.textField.palette();
      p.setColor(QtGui.QPalette.Base, fieldColor); #background matching block color
      self.textField.setPalette(p);
      #self.textField.setStyleSheet("border: 1px solid black;")
      #self.textField.setBackground(fieldColor);#background matching block color
      #self.textField.setCaretColor(Color.WHITE);#white caret
      #self.textField.setSelectionColor(Color.BLACK);#black highlight
      #self.textField.setSelectedTextColor(Color.WHITE);#white text when highlighted
      #self.textField.setBorder(textFieldBorder);
      #self.textField.setMargin(textFieldBorder.getBorderInsets(textField));

      #self.textLabel.setAutoFillBackground(True) # This is important!!
      #color  = QtGui.QColor(233, 10, 150)
      #alpha  = 0
      #values = "{r}, {g}, {b}, {a}".format(r = fieldColor.red(),
      #                                     g = fieldColor.green(),
      #                                     b = fieldColor.blue(),
      #                                     a = alpha
      #                                     )
      #self.textLabel.setStyleSheet("QLabel { background-color: rgba("+values+"); }")
      
      self.loading  = False;
      
      self.textField.setParent(self)
      self.textLabel.setParent(self)
      
  def enterEvent(self,event):
    print('enterEvent')
    self.suggestEditable(True);
    
  def leaveEvent(self,event):
    print('leaveEvent')
    self.suggestEditable(False);
    
  def mouseReleaseEvent(self, ev):
    # Set to editing state upon mouse click if this block label is editable
    # if clicked and if the label is editable,
    if (self.isEditable):
      # if clicked and if the label is editable,
      # then set it to the editing state when the label is clicked on
      self.setEditingState(True);
      #self.textField.setSelectionStart(0);
      self.textField.selectAll()
      
  def textChanged(self):
    if(self.loading): return

    self.textLabel.setText(self.textField.toPlainText());
    self.textLabel.adjustSize()
    self.updateDimensions();

    self.fireTextChanged(self.textField.toPlainText());
    
  def suggestEditable(self, suggest):
    '''
     * Toggles the visual suggestion that this label may be editable depending on the specified
     * suggest flag and properties of the block and label.  If suggest is true, the visual suggestion will display.  Otherwise, nothing 
     * is shown.  For now, the visual suggestion is a simple white line boder.
     * Other requirements for indicator to show: 
     * - label type must be NAME
     * - label must be editable
     * - block can not be a factory block
     * @param suggest 
    '''
    if(self.isEditable):
      if(suggest):
        self.setStyleSheet("border:1px solid rgb(255, 255, 255); ")
        #setBorder(BorderFactory.createLineBorder(Color.white));#show white border
      else:
        self.setStyleSheet("border:0px solid rgb(255, 255, 255); ")
        #setBorder(null);#hide white border
  def isTextValid(self, text):
    return text != ""

  def getText(self):
      return self.textLabel.text().strip();

  def setText(self,value):
      self.updateLabelText(str(value).strip());
      '''
      if(isinstance(value, basestring)):
         self.updateLabelText(value.trim());
      elif(isinstance(value, double)):
         updateLabelText(str(value));
      elif(isinstance(value, double)):
         updateLabelText( "True" if value else "False");
      '''
  def setEditable(self,isEditable):
   	self.isEditable = isEditable;

  def setEditingState(self,editing) :
    if (editing):
      self.editingText = True;
      self.textField.setText(self.textLabel.text().strip());
      self.labelBeforeEdit = self.textLabel.text();
      self.textField.show()
      self.textLabel.hide()      
      self.textField.setFocus()
    else:
      print(self.editingText)
      # update to current textfield.text
      # if text entered was not empty and if it was editing before
      if(self.editingText):
        self.editingText = False;
        
        # make sure to remove leading and trailing spaces before testing if text is valid
        # TODO if allow labels to have leading and trailing spaces, will need to modify this if statement
        
        if(self.isTextValid(self.textField.toPlainText().strip())):
          print(self.textField.toPlainText().strip())
          self.setText(self.textField.toPlainText());
        else:
          self.setText(self.labelBeforeEdit);
  def fireTextChanged(self, text):
    print("abstract fireTextChanged")
    pass

  def updateLabelText(self,text):
    # leave some space to click on
    if (text == ""):
       text = "     ";
    #print(text)
    #update the text everywhere
    self.textLabel.setText(text);
    self.textField.setText(text);

    self.textLabel.adjustSize()
    self.textField.adjustSize()

    # resize to new text
    self.updateDimensions();

    #the blockLabel needs to update the data in Block
    self.fireTextChanged(text);
    
    #print(self.editingText)
    #print("x:{0},y:{1},w:{2},h:{3}".format(self.textLabel.x(), 
    #self.textLabel.y(), 
    #self.width(), 
    #self.height()))
         
    # show text label and additional ComboPopup if one exists
    #self.textField.setParent(None)
    #self.textLabel.setParent(self)
    self.textField.hide()
    self.textLabel.show()
    #if (self.hasSiblings):
    #   self.add(self.menu, BorderLayout.EAST);



  def updateDimensions(self):
    
    if(self.editingText):
      self.textField.resize(self.textLabel.width(),
        self.textLabel.height());  
        
      updatedDimension = QtCore.QSize(
        self.textField.width()+5,
        self.textField.height());
    else:
      updatedDimension = QtCore.QSize(
        self.textLabel.width()+5,
        self.textLabel.height());
        
    if(self.hasSiblings):
       updatedDimension.width += LabelWidget.DROP_DOWN_MENU_WIDTH;

    self.textField.resize(updatedDimension);
    self.textLabel.resize(updatedDimension);
    self.resize(updatedDimension);
    #self.fireDimensionsChanged(this.getSize());


  def setFont(self,font):
      self.textField.setCurrentFont(font)
      self.textLabel.setFont(font)

class BlockLabelTextField(QtGui.QTextEdit):
  def __init__(self, labelWidget):    
      QtGui.QTextEdit.__init__(self)
      self.labelWidget = labelWidget
      #self.setFocusPolicy(QtCore.Qt.StrongFocus)
      #self.setContentsMargins(0, 0, 0, 0)
      #self.setStyleSheet("padding:0;")
      self.document().setDocumentMargin(0)
      self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
      #self.setFrameShape(QtGui.QFrame.Panel)
      
  def focusInEvent(self, event):
    print("focusInEvent")
    #self.labelWidget.setEditingState(False)
    
  def focusOutEvent(self, event):
    print("focusOutEvent")
    self.labelWidget.setEditingState(False)
  
  # split all text into list of strings by separator '\n' (new line symbol)
  def getPreferredSize(self):
    str = self.toPlainText ()
    # gather font metrics in QTextEdit
    textEditFont = self.currentFont();
    fm = QtGui.QFontMetrics(textEditFont);

    pixelsWide = fm.boundingRect(str).width();
    pixelsHigh = fm.boundingRect(str).height();

    return QtCore.QSize(pixelsWide+6,pixelsHigh)

class ShadowLabel(QtGui.QLabel):

  shadowPositionArray = [[0,-1],[1,-1], [-1,0], [2,0],	[-1,1], [1,1],  [0,2], 	[1,0],  [0,1]];
  shadowColorArray =	[0.5,	0.5,	0.5, 	0.5, 	0.5, 	0.5,	0.5,	0,		0];

  def __init__(self):
      QtGui.QLabel.__init__(self)
      self.offsetSize = 1;
      self.setMargin(0)
      self.setIndent(0)
      #self.setStyleSheet("padding:0;")
      #self.document().setDocumentMargin(0)
      #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      #self.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
      #self.setFrameShape(QtGui.QFrame.NoFrame)
      #self.setStyleSheet("border:1px solid rgb(255, 255, 255); ")
  #def enterEvent(self,event):
  #  self.labelWidget.suggestEditable(True);
    
  #def leaveEvent(self,event):
  #  self.labelWidget.suggestEditable(False);
    
  def getPreferredSize(self):
      str = self.text()
      # gather font metrics in QTextEdit
      textEditFont = self.font();
      fm = QtGui.QFontMetrics(textEditFont);

      pixelsWide = fm.boundingRect(str).width()+1;
      pixelsHigh = fm.boundingRect(str).height()+1;

      return QtCore.QSize(pixelsWide,pixelsHigh)    
    
  def paintEvent(self,event):
      #QtGui.QLabel.paintEvent(self,event)
      #return
      painter = QtGui.QPainter();
      painter.begin(self)
      #painter.fillPath (self.blockArea);
      #painter.drawPath(self.blockArea);


      # g2.addRenderingHints(new RenderingHints(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON));

      # DO NOT DRAW SUPER's to prevent drawing of label's string.
      # Implecations: background not automatically drawn
      # super.paint(g);

      # draw shadows
      for i in range(0,len(self.shadowPositionArray)):
         dx = self.shadowPositionArray[i][0];
         dy = self.shadowPositionArray[i][1];
         painter.setPen(QtGui.QColor(0,0,0, self.shadowColorArray[i]*255));
         painter.drawText((int)((4+dx)*self.offsetSize), self.height()+(int)((dy-4)*self.offsetSize),self.text(), );


      # draw main Text
      painter.setPen(QtCore.Qt.white);
      painter.drawText((int)((4)*self.offsetSize), self.height()+(int)((-4)*self.offsetSize),self.text());
      #painter.drawText(0, 0,self.text());

      painter.end()
