#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      A21059
#
# Created:     19/03/2015
# Copyright:   (c) A21059 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math
import numpy
import copy
from PyQt4 import QtGui,QtCore, uic

class Triplet():
   def __init__(self):
      self.x = 0.0
      self.y = 0.0
      self.z = 0.0

   def InitLight(self,LightElevation,LightAngle):
      self.x =  math.cos(LightElevation) * math.cos(LightAngle)
      self.y = -math.cos(LightElevation) * math.sin(LightAngle)
      self.z =  math.sin(LightElevation)

   def DotTriplet(t1, t2):
       return t1.x * t2.x + t1.y * t2.y + t1.z * t2.z

   def NormTriplet(self):
      return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

   def NormalizeTriplet(self):
      tmp = self.NormTriplet()
      if tmp == 0: return
      tmp = 1.0 / tmp
      self.x *=  tmp
      self.y *=  tmp
      self.z *=  tmp


class SAFEARRAYBOUND():
   def __init__(self):
      self.cElements = 0
      self.lLbound = 0

class SAFEARRAY2D():
   def __init__(self):
      self.cDims = 0
      self.fFeatures = 0
      self.cbElements = 0
      self.cLocks = 0
      self.pvData = 0

      arr = SAFEARRAYBOUND()
      self.Bounds= [arr for x in range(2)]

class Bevel():
   def __init__(self,src_img,back_color=QtCore.Qt.black,height=5,angle=135,elevation=30):
      LightPos = Triplet()
      arrSrcBytes= []
      tSASrc = SAFEARRAY2D()

      w = src_img.width()
      h = src_img.height()

      ptr = src_img.bits()
      ptr.setsize(src_img.byteCount())
      img_arr = numpy.asarray(ptr).reshape(src_img.width(),src_img.height(), 4)

      print(img_arr)
      arrHeight = [[0 for x in range(w)] for x in range(h)]
      arrWork1  = [[0 for x in range(w)] for x in range(h)]
      arrWork2  = [[0 for x in range(w)] for x in range(h)]
      arrHilite = [[0 for x in range(w)] for x in range(h)]
      arrShadow = [[0 for x in range(w)] for x in range(h)]

      # Setup parameters
      BevelHeight    = height
      LightAngle     = Bevel.DegreesToRadians(angle)
      LightElevation = Bevel.DegreesToRadians(elevation)

      LightPos.InitLight(LightElevation,LightAngle)

      #MileStone "1 - Started", True

      # Setup work mask
      for i in range(0, h):
         for j in range(0, w):
            color = QtGui.QColor(src_img.pixel(j,i))
            if(color == back_color):
               arrHeight[i][j]  = 0
               arrWork1 [i][j]  = 0
            else:
               arrHeight[i][j] = 1
               arrWork1 [i][j] = 1

      #print (arrWork1)
      #return image

      # Shrink work mask and build height field

      # MileStone "2 - Building height field"

      for k in range(0, BevelHeight): # Depth
         for i in range(1, h-1):
            for j in range(1, w-1):
               if((arrWork1[i][j] == 0) or
                  (arrWork1[i][j-1] == 0) or
                  (arrWork1[i-1][j] == 0) or
                  (arrWork1[i+1][j] == 0) or
                  (arrWork1[i][j+1] == 0)):
                  arrWork2[i][j] = 0
                  #continue
               else:
                  arrWork2[i][j] = 1
                  arrHeight[i][j] += 1

         # SwapArrayDataPtrs VarPtrArray(arrWork1()), VarPtrArray(arrWork2())
         arrWork1 = copy.deepcopy(arrWork2)

      # At this point, the height field values range from
      # 0 to (BevelHeight+1)
      # Normalize them to (0...255)
      # MileStone "3 - Normalizing height field"

      Bevel.NormalizeArray(arrHeight, 0, BevelHeight + 1)


      # Blur Height field
      # MileStone "4 - Blurring height"

      #print(arrHeight)
      arrHeight = Bevel.BlurArray(arrHeight)
      #print(arrHeight)


      vx = Triplet()
      vy = Triplet()
      vN = Triplet()

      # Dim vx As Triplet, vy As Triplet, vN As Triplet
      # Dim vLight As Triplet
      # Dim IncidentLight As Double

      # MileStone "5 - Calculating light"

      # Calculate incident light
      for i in range(1, h-1):
         for j in range(1, w-1):
            if arrHeight[i][j] == 0 or arrHeight[i][j] == 255:
               # Do nothing
               pass
            else:
               vN.x = (arrHeight[i][j] ) - 0.25 * (2 * arrHeight[i+1][j]  + arrHeight[i+1][j-1]  + arrHeight[i+1][j+1] )
               vN.y = (arrHeight[i][j] ) - 0.25 * (2 * arrHeight[i][j+1]  + arrHeight[i-1][j+1]  + arrHeight[i+1][j+1] )
               vN.z = 1.0

               IncidentLight = Triplet.DotTriplet(vN, LightPos) / vN.NormTriplet()

               if IncidentLight > 0 :
                  arrHilite[i][j]  = round(255 * IncidentLight)
               else:
                  arrShadow[i][j]  = round(-255 * IncidentLight)

      # MileStone "6 - Blurring lights"


      #return image

      for k in range(0, 3):
         arrHilite = Bevel.BlurArray(arrHilite)
         arrShadow = Bevel.BlurArray(arrShadow)


      #return image

      # MileStone "7 - Merging height/light"
      for i in range(0, h):
         for j in range(0, w):
            arrHilite[i][j] = round((arrHilite[i][j]* (255 - arrHeight[i][j]))/255)


      for i in range(0, h):
         for j in range(0, w):
            arrShadow[i][j] = round((arrShadow[i][j]*(255 - arrHeight[i][j]))/255)


      # MileStone "8 - Rendering"
      # Render effect
      #print (arrHeight)
      self.image = src_img
      #self.image = QtGui.QImage(w,h,QtGui.QImage.Format_ARGB32)
      for i in range(0, h):
         for j in range(0, w):
            rgb = src_img.pixel(j,i)
            color = QtGui.QColor(rgb)
            #color = QtGui.QColor(img_arr[i,j,2],img_arr[i,j,1],img_arr[i,j,0])
            if(color == back_color):
               # Do nothing
               #img.setPixel(i, j, image.pixel(i,j))
               pass
            elif arrHeight[i][j] == 0 or arrHeight[i][j] == 255:
               #img.setPixel(i, j, image.pixel(i,j))
               # Do nothing
               pass
            else:
               #img.setPixel(i, j, image.pixel(i,j))

               if arrShadow[i][j] > 0:
                  self.image.setPixel(j,i, Bevel.Darken(arrShadow[i][j], rgb))
                  #new_color = Bevel.Darken(arrShadow[i][j],color )
                  #img_arr[i,j,0] = color.blue()
                  #img_arr[i,j,1] = color.green()
                  #img_arr[i,j,2] = color.red()

               if arrHilite[i][j] > 0:
                  self.image.setPixel(j, i, Bevel.Lighten(arrHilite[i][j], rgb))
                  #new_color = Bevel.Lighten(arrShadow[i][j],color )
                  #img_arr[i,j,0] = color.blue()
                  #img_arr[i,j,1] = color.green()
                  #img_arr[i,j,2] = color.red()

      #print( img_arr)
      #arr = numpy.reshape(img_arr, -1)
      #print( arr)
      #img_arr.re
      #self.image = QtGui.QImage(arr,w,h,src_img.bytesPerLine,QtGui.QImage.Format_ARGB32)

   def getBevelImage(self):
      return self.image

   def DegreesToRadians(deg):
      return math.pi * deg / 180

   def NormalizeArray(arr, Min, Max):
      for i in range(0,len(arr)):
         for j in range(0,len(arr[i])):
            arr[i][j] = ((arr[i][j] - Min) * 255) // (Max - Min)

   def BlurArray(arr):
      x1 =  1
      y1 =  1
      x2 = len(arr) - 1
      y2 = len(arr[0]) - 1

      arrTmp= [[0 for x in range(y2+1)] for x in range(x2+1)]

      for i in range(x1,x2):
         for j in range(y1,y2):
            # Centre - coefficient: 1
            tmp = arr[i][j]
            # Adjacent pixels - coefficient: 3
            tmp = tmp + 4 * arr[i][j-1]
            tmp = tmp + 4 * arr[i-1][j]
            tmp = tmp + 4 * arr[i][j+1]
            tmp = tmp + 4 * arr[i+1][j]
            # Diagonal pixels - coefficient: 2
            tmp = tmp + 3 * arr[i-1][j-1]
            tmp = tmp + 3 * arr[i+1][j-1]
            tmp = tmp + 3 * arr[i-1][j+1]
            tmp = tmp + 3 * arr[i+1][j+1]
            # Set light as the weighted average
            if(tmp != 0):
               tt = 0
            arrTmp[i][j] = tmp // 29

      return arrTmp

   def Lighten(Amount, rgb):
      color =  QtGui.QColor(rgb)
      red = color.red()
      green = color.green()
      blue = color.blue()
      # r = CByte(Amount * 255 + (1# - Amount) * r)
      r = round(color.red()*(255 - Amount)/255) + Amount
      # g = CByte(Amount * 255 + (1# - Amount) * g)
      g = round(color.green()*(255 - Amount)/255) + Amount
      # b = CByte(Amount * 255 + (1# - Amount) * b)
      b = round(color.blue()*(255 - Amount)/255) + Amount

      return QtGui.QColor(r,g,b).rgb()

   def Darken(Amount, rgb):
      color =  QtGui.QColor(rgb)
      r = round(color.red()*(255 - Amount)/255)
      g = round(color.green()*(255 - Amount)/255)
      b = round(color.blue()*(255 - Amount)/255)

      return QtGui.QColor(r,g,b).rgb()


import sys
def main():
   app = QtGui.QApplication(sys.argv)

   color = QtGui.QColor(255,0,0)
   print(color.rgb())
   # Create the window and the graphics view
   win = QtGui.QMainWindow()
   win.resize(200,200)
   canvas = QtGui.QGraphicsScene()
   view = QtGui.QGraphicsView(canvas, win)
   view.resize(200, 200)

   image = QtGui.QImage("D:\\temp.bmp")
   bevel = Bevel(image)

   pixmap = QtGui.QPixmap.fromImage(bevel.getBevelImage())

   # Add the image to the canvas
   canvas.addPixmap(pixmap)

   win.show()
   sys.exit(app.exec_())



   pass

if __name__ == '__main__':
    main()
