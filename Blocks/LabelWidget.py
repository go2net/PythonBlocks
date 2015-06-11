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
  DROP_DOWN_MENU_WIDTH = 7;
  def __init__(self,initLabelText, prefix, suffix,  fieldColor, tooltipBackground):
      QtGui.QWidget.__init__(self)

      self.prefix = prefix
      self.suffix = suffix            
      self.loading  = True;
      
      if(initLabelText == None): initLabelText = "";
      self.tooltipBackground = tooltipBackground;
      self.labelBeforeEdit = initLabelText;

      self.labelPrefix = ShadowLabel(self)
      self.labelSuffix = ShadowLabel(self)

      self.textField = BlockLabelTextField(self)      
      self.textLabel = ShadowLabel(self)
      self.menu = LabelMenu(self)      

      self.isEditable = False
      self.isVariable = False
      self.hasMenu = False
      self.editingText = False
      self.isPressed = False
      self.menuShowed = False
      self.lastSelectedItem = None
      
      # set up textfield colors
      self.textField.setTextColor(QtCore.Qt.white); #white text
      
      self.textField.connect(self.textField, SIGNAL('textChanged()'), self.textChanged)
      
      p = self.textField.palette();
      p.setColor(QtGui.QPalette.Base, fieldColor); #background matching block color
      self.textField.setPalette(p);
       
      self.loading  = False;
      
  def mousePressEvent(self, event):
    self.isPressed = True
    event.ignore();  
    
  def mouseReleaseEvent(self, event):
    if(not self.isPressed): return
    # Set to editing state upon mouse click if this block label is editable
    # if clicked and if the label is editable,
    #print('mouseReleaseEvent')
    #print(self.isEditable)
    if (self.isEditable):
      # if clicked and if the label is editable,
      # then set it to the editing state when the label is clicked on
      self.setEditingState(True);
      #self.textField.setSelectionStart(0);
      self.textField.selectAll()
        
    event.ignore();   
 
  def setMenu(self, hasSiblings, siblings, isVariable):
    self.isVariable = isVariable
    self.hasMenu = hasSiblings or self.isVariable
    
    if(self.hasMenu):
      self.menu.setMenu(siblings, self.isVariable);
      self.textField.hide()
      self.textLabel.hide() 
      self.menu.show()     
    else:
      self.textField.hide()
      self.textLabel.show()   
      self.menu.hide()
      
    self.updateDimensions()
  
  def textChanged(self):

    if(self.loading): return

    if(self.hasMenu):
      self.menu.setText(self.textField.toPlainText());
      self.menu.adjustSize()
    else:
      self.textLabel.setText(self.textField.toPlainText());
      self.textLabel.adjustSize()
    
    self.updateDimensions();
      
    self.fireTextChanged(self.textField.toPlainText());

  
  def isTextValid(self, text):
    return text != ""

  def getText(self):
      return self.textLabel.text().strip();

  def setText(self,text):
    self.updateLabelText(str(text).strip());

  def setEditable(self,isEditable):
    self.isEditable = isEditable;
    self.textLabel.isEditable = isEditable 


  def setEditingState(self,editing) :
    #print(self.getText())
    if (editing):
      self.editingText = True;
      self.textField.setText(self.textLabel.text().strip());
      self.labelBeforeEdit = self.textLabel.text();
      self.textField.show()
      self.textLabel.hide()    
      self.menu.hide()  
      self.textField.setFocus()

    else:
      #print(self.editingText)
      # update to current textfield.text
      # if text entered was not empty and if it was editing before
      
      if(self.editingText):
        self.editingText = False;
        
        # make sure to remove leading and trailing spaces before testing if text is valid
        # TODO if allow labels to have leading and trailing spaces, will need to modify this if statement
        
        if(self.isTextValid(self.textField.toPlainText().strip())):
          #print(self.textField.toPlainText().strip())
          self.setText(self.textField.toPlainText());
        else:
          self.setText(self.labelBeforeEdit);
          
  def fireTextChanged(self, text):
    #print("abstract fireTextChanged")
    pass
    
  def fireGenusChanged(self, text):
    #print("abstract fireTextChanged")
    pass
  

  def updateLabelText(self,text):
    #elf.loading = True
    # leave some space to click on
     
    #the blockLabel needs to update the data in Block
    #self.fireTextChanged(text);

    if(self.hasMenu):
      self.textField.hide()
      self.textLabel.hide()
      self.menu.show() 
    else:
      self.textField.hide()
      self.textLabel.show()
      self.menu.hide() 
    
    if(self.prefix == ''):
      self.labelPrefix.hide()
    else:
      self.labelPrefix.show()
      
    if(self.suffix == ''):
      self.labelSuffix.hide()
    else:
      self.labelSuffix.show()
      
    if (text == ""):
       text = "     ";

    self.labelPrefix.setText(self.prefix)
    self.labelSuffix.setText(self.suffix) 
    
    self.textLabel.setText(text);
    self.textField.setText(text);
    self.menu.setText(text); 
    
    # resize to new text
    self.updateDimensions();
    
  def updateDimensions(self):
   
    self.labelPrefix.adjustSize()
    self.labelSuffix.adjustSize()      
    self.textLabel.adjustSize()
    self.textField.adjustSize()
    self.menu.adjustSize()
    
    if(self.labelPrefix.text()!=''):
      self.labelPrefix.adjustSize()
      self.labelPrefix.resize(self.labelPrefix.width()+8,
        self.labelPrefix.height());  
    else:
      self.labelPrefix.resize(0, 0)
    
    if(self.labelSuffix.text()!=''):
      self.labelSuffix.adjustSize()
      self.labelSuffix.resize(self.labelSuffix.width()+3,
        self.labelSuffix.height());         
    else:
      self.labelSuffix.resize(0, 0)
      
    if(self.editingText):
      self.textField.resize(self.textLabel.width()+3,
        self.textLabel.height());  
       
      self.textField.move(self.labelPrefix.width(), 0)
      self.labelSuffix.move(self.labelPrefix.width()+self.textLabel.width(), 0)
      updatedDimension = QtCore.QSize(
         self.labelPrefix.width()+self.textLabel.width()+self.labelSuffix.width(),
          self.textLabel.height());        
      
    else:
      
      if(self.hasMenu):
        self.menu.resize(self.menu.width()+LabelWidget.DROP_DOWN_MENU_WIDTH+7,
          self.menu.height());
          
        self.menu.move(self.labelPrefix.width(), 0)
        if(self.labelSuffix.text()!=''):
          self.labelSuffix.move(self.labelPrefix.width()+self.menu.width(), 0)
        
        updatedDimension = QtCore.QSize(
          self.labelPrefix.width()+self.menu.width()+self.labelSuffix.width(),
          self.menu.height()); 
      else:
        self.textLabel.resize(self.textLabel.width()+7,
          self.textLabel.height()); 
          
        self.textLabel.move(self.labelPrefix.width(), 0)
        self.labelSuffix.move(self.labelPrefix.width()+self.textLabel.width(), 0)
        updatedDimension = QtCore.QSize(
          self.labelPrefix.width()+self.textLabel.width()+self.labelSuffix.width(),
          self.textLabel.height());        

    self.resize(updatedDimension);

  def setFont(self,font):

      self.labelPrefix.setFont(font)
      self.labelSuffix.setFont(font)
      self.textField.setCurrentFont(font)
      self.textLabel.setFont(font)
      self.menu.setFont(font)

class BlockLabelTextField(QtGui.QTextEdit):
  def __init__(self, labelWidget):    
      QtGui.QTextEdit.__init__(self, labelWidget)
      self.labelWidget = labelWidget
      #self.setFocusPolicy(QtCore.Qt.StrongFocus)
      #self.setContentsMargins(0, 0, 0, 0)
      #self.setStyleSheet("padding:0;")
      self.document().setDocumentMargin(0)
      self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      self.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
      #self.setFrameShape(QtGui.QFrame.Panel)
      
  def focusInEvent(self, event):
    pass
    #print("focusInEvent")
    #self.labelWidget.setEditingState(False)
    
  def focusOutEvent(self, event):
    #print("focusOutEvent")
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

  def __init__(self, parent, isEditable=False):
      QtGui.QLabel.__init__(self, parent)
      self.offsetSize = 1;
      self.setMargin(0)
      self.setIndent(0)
      self.isEditable = isEditable
      #self.setStyleSheet("padding:0;")
      #self.document().setDocumentMargin(0)
      #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
      #self.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
      #self.setFrameShape(QtGui.QFrame.NoFrame)
      #self.setStyleSheet("border:1px solid rgb(255, 255, 255); ")
  #def enterEvent(self,event):
  #  self.labelWidget.suggestEditable(True);
    
  def enterEvent(self,event):
    print('enterEvent')
    self.suggestEditable(True);
    
  def leaveEvent(self,event):
    print('leaveEvent')
    self.suggestEditable(False);   
  
    
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
    #print(self.isEditable)
    if(self.isEditable):
      if(suggest):
        self.setStyleSheet("border:1px solid rgb(255, 255, 255); ")
        #setBorder(BorderFactory.createLineBorder(Color.white));#show white border
      else:
        self.setStyleSheet("border:0px solid rgb(255, 255, 255); ")
        #setBorder(null);#hide white border
  
  def getPreferredSize(self):
      str = self.text()
      # gather font metrics in QTextEdit
      textEditFont = self.font();
      fm = QtGui.QFontMetrics(textEditFont);

      pixelsWide = fm.boundingRect(str).width()+1;
      pixelsHigh = fm.boundingRect(str).height()+1;

      return QtCore.QSize(pixelsWide,pixelsHigh)    
    
  def paintEvent(self,event):
      #print('ShadowLabel paintEvent')
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
      
      
class LabelMenu(ShadowLabel):

  shadowPositionArray = [[0,-1],[1,-1], [-1,0], [2,0],	[-1,1], [1,1],  [0,2], 	[1,0],  [0,1]];
  shadowColorArray =	[0.5,	0.5,	0.5, 	0.5, 	0.5, 	0.5,	0.5,	0,		0];

  def __init__(self, parent=None):
      ShadowLabel.__init__(self, parent)
      self.labelWidget = parent
      self.setStyleSheet("border-radius: 3px; border:1px solid rgb(255, 255, 255,150); background-color : rgb(200, 200, 200,150);")
      self.lastSelectedItem = None
      self.isVariable = False
  
  def mouseReleaseEvent(self, event):
    self.popupmenu.popup(event.globalPos())       
    event.ignore();  
    

  def doStuff(self, sender, item):
    if(sender != self.lastSelectedItem):
      if(self.lastSelectedItem != None):
        self.lastSelectedItem.setChecked(False)      
      self.lastSelectedItem = sender
  
    sender.setChecked(True)
    self.labelWidget.fireGenusChanged(item[1])
    pass    
    
  def renameVariable(self, sender, item):
    print(self.text())
    pass
      
  def newVariable(self, sender):
    pass      
    
  def setMenu(self, siblings, isVariable):
    self.isVariable = isVariable
    self.popupmenu = QtGui.QMenu();
      
    for sibling in siblings:
      entry = self.popupmenu.addAction(sibling[1])
      entry.setCheckable (True)
      if(sibling[1] == self.text()):
        entry.setChecked(True)
        self.lastSelectedItem = entry
      self.connect(entry,QtCore.SIGNAL('triggered()'), lambda sender=entry, item=sibling: self.doStuff(sender, item))    
    
    if(isVariable):
      if(len(siblings) > 0):
         self.popupmenu.addSeparator()
      entry = self.popupmenu.addAction('Rename variable')  
      self.connect(entry,QtCore.SIGNAL('triggered()'),  lambda sender=entry, item=self.lastSelectedItem: self.renameVariable(sender, item)) 
      
      entry = self.popupmenu.addAction('New variable')  
      self.connect(entry,QtCore.SIGNAL('triggered()'),  lambda sender=entry: self.newVariable(sender)) 
    
  def getPreferredSize(self):
      return ShadowLabel.getPreferredSize(self)
      str = self.text()
      # gather font metrics in QTextEdit
      textEditFont = self.font();
      fm = QtGui.QFontMetrics(textEditFont);

      pixelsWide = fm.boundingRect(str).width()+1;
      pixelsHigh = fm.boundingRect(str).height()+1;

      return QtCore.QSize(pixelsWide,pixelsHigh)    
    
  def paintEvent(self,event):
    ShadowLabel.paintEvent(self,event)
    #return
    painter = QtGui.QPainter();
    painter.begin(self)
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    
    triangle = QtGui.QPainterPath()  
    triangle_left = self.width()-LabelWidget.DROP_DOWN_MENU_WIDTH-3
    triangle.moveTo(triangle_left,self.height()/3);
    triangle.lineTo(self.width()-3, self.height()/3);
    triangle.lineTo(triangle_left +LabelWidget.DROP_DOWN_MENU_WIDTH/2, self.height()/3+LabelWidget.DROP_DOWN_MENU_WIDTH-3);
    triangle.lineTo(triangle_left, self.height()/3);
    triangle.closeSubpath()

    brush = QtGui.QBrush(QtGui.QColor(255,255,255,255));
    #painter.setColor(QtGui.QColor(255,255,255,100));
    painter.fillPath(triangle,brush)
    painter.setPen(QtGui.QColor(0, 0, 0, 255));
    #painter.setColor(QtGui.QColor.BLACK);
    #painter.drawPath(triangle);
    painter.end()
