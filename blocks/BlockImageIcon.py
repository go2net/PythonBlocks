from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

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


class  FileDownloader(QObject) :
    def __init__(self, url, parent=None):
        QObject.__init__(self, parent)

        self.manager  = QNetworkAccessManager()
        self._downloadedData = QByteArray ()
        self.connect( self.manager, SIGNAL("finished(QNetworkReply*)"), self.fileDownloaded)
     
        request = QNetworkRequest (url)
        reply = self.manager.get(request)
        loop = QEventLoop()
        self.connect(reply, SIGNAL('finished()'), loop, SLOT('quit()'));
        loop.exec();
        #reply.finished.connect(self.fileDownloaded, reply)
        #self._downloadedData = reply.readAll()
        #print(self._downloadedData)

    def quit(self):
        print('QUIT')    
    
    def fileDownloaded(self, reply) :
        #print('fileDownloaded')
        self._downloadedData = reply.readAll()
        # emit a signal
        #print(self._downloadedData)
        reply.deleteLater();
        self.emit(SIGNAL("downloaded()")) 
     
    def downloadedData(self) :
        return self._downloadedData;


class BlockImageIcon(QLabel):
    
    def __init__(self, fileLocation, img_loc, width, height, isEditable, wrapText):
        QLabel.__init__(self)
        self._url = ''
        self.fileLocation = fileLocation
        self.blockImageIcon = QPixmap()
        self.loadImage(QUrl.fromLocalFile('F://projects/PythonBlocks/resource/79-Home.png'))
        self.blockImageIcon.loadFromData(self.imgCtrl.downloadedData())
        self.img_loc = img_loc
        self._isEditable = isEditable
        self._wrapText = wrapText
        self.setPixmap(self.blockImageIcon)
        #setPreferredSize(new Dimension(blockImageIcon.getIconWidth(), blockImageIcon.getIconHeight()));
   
        #self.setText('HELLO') 

        #store in blockImageMap
        #icon = QPixmap(os.getcwd() +fileLocation)
        if(self.blockImageIcon != None and width > 0 and height > 0): 
            self.blockImageIcon = self.blockImageIcon.scaled(width, height)        
        self.resize(self.blockImageIcon.size()) 
        pass
    
    def loadImage(self, url):
        imageUrl = QUrl(url);
        self.imgCtrl = FileDownloader(imageUrl, self) 
        self.connect(self.imgCtrl , SIGNAL ('downloaded()'), self.downloaded);        
        
    def downloaded(self):
        icon = QPixmap() 
        icon.loadFromData(self.imgCtrl.downloadedData())
     
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
  
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value  
