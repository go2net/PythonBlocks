#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     16/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui,QtCore, uic

class GraphicsManager():

   # get GraphicConfiguration for default screen - this should only be done once at startup **/
   #GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
   #private static GraphicsDevice gs = ge.getDefaultScreenDevice();
   #public static GraphicsConfiguration gc = gs.getDefaultConfiguration();

   MAX_RECYCLED_IMAGES = 50
   numRecycledImages = 0;
   recycledImages = []
   '''
   * Functionally equivalent to
   *   gc.createCompatibleImage(width, height, Transparency.TRANSLUCENT)
   * but allows reusing released images.
   '''
   def getGCCompatibleImage(width, height,back_color):
      size = QtCore.QSize(width, height)
      imgList = None
      if(size in GraphicsManager.recycledImages):
         imgList = GraphicsManager.recycledImages[size]

      if (imgList == None or len(imgList) ==0):
         img = QtGui.QImage(
            width,
            height,
            QtGui.QImage.Format_ARGB32);
         img.fill(0);
         return img;

      GraphicsManager.numRecycledImages-=1;
      img = imgList.pop();

      # Clear the image
      img.fill(0);
      return img;


   '''
   * Add an image to the recycled images list (or if img = null, does nothing).
   * Note: the passed variable should be immediately set to null to avoid aliasing bugs.
   '''
   def recycleGCCompatibleImage(img):
      return;
      if (img == None):
         return;
      # Make sure we don't waste too much memory
      if (GraphicsManager.numRecycledImages >= GraphicsManager.MAX_RECYCLED_IMAGES):
         GraphicsManager.recycledImages= []

      size = QtCore.QSize(img.width(), img.height())

      imgList = GraphicsManager.recycledImages[size];
      if (imgList == None):
         imgList = []
         GraphicsManager.recycledImages[size] = imgList;

      imgList.append(img);



if __name__ == '__main__':
    main()
