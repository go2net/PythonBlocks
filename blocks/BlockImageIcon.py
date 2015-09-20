from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ImageLocation():
    
    LOCATION = ['CENTER', 'EAST', 'WEST', 'NORTH', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'NORTHEAST', 'NORTHWEST']
    ALIGMENT = [
        Qt.AlignHCenter|Qt.AlignVCenter,  # CENTER
        Qt.AlignRight|Qt.AlignVCenter,      # EAST
        Qt.AlignLeft|Qt.AlignVCenter,       # WEST
        Qt.AlignHCenter|Qt.AlignTop,       # NORTH
        Qt.AlignHCenter|Qt.AlignBottom,  # SOUTH
        Qt.AlignRight|Qt.AlignBottom, # SOUTHEAST
        Qt.AlignLeft|Qt.AlignBottom, # SOUTHWEST
        Qt.AlignRight|Qt.AlignTop,  # NORTHEAST
        Qt.AlignLeft|Qt.AlignTop] # NORTHWEST
    
    def  getImageLocation(s):
        for loc in ImageLocation.LOCATION:
            if (loc == s.upper()):
                return loc 
        else:
            return ''
            
    def getImageAlign(s):
        index = ImageLocation.LOCATION.indexof(s)
        return ImageLocation.ALIGMENT[index]


class BlockImageIcon(QLabel):
    
    def __init__(self, blockImageIcon, img_loc, isEditable, wrapText):
        QLabel.__init__(self)
        self.blockImageIcon = blockImageIcon
        self.img_loc = img_loc
        self._isEditable = isEditable
        self._wrapText = wrapText
        self.setPixmap(blockImageIcon)
        #setPreferredSize(new Dimension(blockImageIcon.getIconWidth(), blockImageIcon.getIconHeight()));
        self.resize(blockImageIcon.size())    
        #self.setText('HELLO') 
        
        pass
        
    @property
    def icon(self):
        return self.blockImageIcon

    @icon.setter
    def icon(self, value):
        self.blockImageIcon = value
        self.setPixmap(value)
        
        
    @property
    def location(self):
        return self.img_loc

    @location.setter
    def location(self, value):
        self.img_loc = value        
        
    @property
    def isEditable(self):
        return self._isEditable

    @isEditable.setter
    def isEditable(self, value):
        self._isEditable = value    
  
    @property
    def wrapText(self):
        return self._wrapText

    @wrapText.setter
    def wrapText(self, value):
        self._wrapText = value    
  
