from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
import sys

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
    
    def __init__(self, url, img_loc, _icon, width, height, isEditable, wrapText):
        QLabel.__init__(self)
        self._url = url
        if(_icon == None):
            self._imgIcon = QPixmap()
            if(self._url != ''):
                self.imgCtrl = FileDownloader(QUrl(url))
                self._imgIcon.loadFromData(self.imgCtrl.downloadedData())
                
            #self._imgIcon = self._imgIcon.scaled(self.width(), self.height())   
        else:
            self._imgIcon = _icon
        
        self.img_loc = img_loc
        self._isEditable = isEditable
        self._wrapText = wrapText
        
        #setPreferredSize(new Dimension(_imgIcon.getIconWidth(), _imgIcon.getIconHeight()));
   
        #store in blockImageMap
        #icon = QPixmap(os.getcwd() +fileLocation)
        if(self._imgIcon != None and not self._imgIcon.isNull() and width > 0 and height > 0): 
            #print('scaled in __init__')
            #self._imgIcon = self._imgIcon.scaled(width, height)        
            self.setPixmap(self._imgIcon)

        self.resize(QSize(width, height)) 
    
    def resizeEvent(self, event):
        try:
            if(event.oldSize() != event.size() and self._imgIcon != None and event.size() != self._imgIcon.size()):
                if(self._url != ''):
                    self.imgCtrl = FileDownloader(QUrl(self._url ))
                    icon = QPixmap()
                    icon.loadFromData(self.imgCtrl.downloadedData())
                    self._imgIcon =icon.scaled(event.size().width(), event.size().height()) 
                    self.setPixmap(self._imgIcon)
                    
            #self.resize(event.size()) 
            QLabel.resizeEvent(self, event)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,exc_obj)
        
    def getImageInfo(self):
        import base64
        ImageInfo = {}
        ImageInfo['location'] = self.location
        ImageInfo['isEditable'] = self.isEditable
        ImageInfo['wrapText'] = self.wrapText
        ImageInfo['url'] = self.url
        ImageInfo['width'] = self.width()
        ImageInfo['height'] = self.height()
        
        # Save QPixmap to QByteArray via QBuffer.
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        self.icon.save(buffer, 'PNG')
        icon_data = byte_array.data()
        b64_data = base64.b64encode(icon_data)
        icon_b64_str = b64_data.decode("utf-8") 
        ImageInfo['icon'] = icon_b64_str
        return ImageInfo
    
    def loadImage(self, url):
        imageUrl = QUrl(url);
        self.imgCtrl = FileDownloader(imageUrl, self) 
        self.connect(self.imgCtrl , SIGNAL ('downloaded()'), self.downloaded);        
        
    def downloaded(self):
        icon = QPixmap() 
        icon.loadFromData(self.imgCtrl.downloadedData())
        icon = icon.scaled(self.width(), self.height())        
     
    @property
    def icon(self):
        return self._imgIcon

    @icon.setter
    def icon(self, _icon):
        if(_icon != None and not _icon.isNull() and self.width() > 0 and self.height() > 0): 
            self._imgIcon = _icon.scaled(self.width(), self.height())
            self.setPixmap(self._imgIcon)        
        else:
            print(self.width())
    
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
