#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      shijq
#
# Created:     09/03/2015
# Copyright:   (c) shijq 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt4 import QtGui,QtCore
from blocks.Bezier import Bezier
import math
debug = False

class BlockShapeUtil():

   def cornerTo( gp, cornerPoint, nextCornerPoint,  radius):
      if (radius < 0.001):
         #if a small radius, just draw a line
         BlockShapeUtil.lineTo(gp,cornerPoint.x(), cornerPoint.y());
      else:
         BlockShapeUtil.makeCornerTo(gp, cornerPoint, nextCornerPoint, radius);


   def printPos(p):
      print("X="+ str(p.currentPosition().x()) + ", Y=" + str(p.currentPosition().y()))

   def dist(x0, y0, x1, y1):
       "Distance between two points"
       return ((x1 - x0)**2 + (y1 - y0)**2) ** 0.5

   def lineToRelative(gp, x, y):
      currentPoint = gp.currentPosition();
      BlockShapeUtil.lineTo(gp, currentPoint.x() + x, currentPoint.y() + y)

   def lineTo(gp, x, y):
      if debug:
         print("Line to point({0},{1})".format(x,y))
      gp.lineTo(x, y);

   def cornerShape(gp, x1, y1, x2, y2, x3, y3):
      BlockShapeUtil.cubicTo(gp, x1, y1, x2, y2, x3, y3)
   def cubicTo(gp, x1, y1, x2, y2, x3, y3):
      if debug:
         currentPoint = gp.currentPosition();
         print("Draw cubic from point({0},{1}) to point({2},{3}) via control point({4},{5} and {6},{7})".format(currentPoint.x(), currentPoint.y(), x3,y3,x1,y1,x2,y2))
      gp.cubicTo( x1, y1, x2, y2, x3, y3);
   def moveTo(gp, x, y):
      currentPoint = gp.currentPosition();
      if debug:
         print("Move from point({0},{1}) to point({2},{3})".format(currentPoint.x(),currentPoint.y(),x,y))
      gp.moveTo(currentPoint.x() + x, currentPoint.y() + y);


   #def appendPath2(gp1, gp2, reversed):
   #   if(not reversed):
   #      gp1.connectPath(gp2)
   #   else:
   #      gp1.connectPath(gp2.toReversed())

   def appendPath(gp1, gp2, reversed):

      leftmost = 0xffffffff

      type_index_list = []
      for index in range(0,gp2.elementCount()):
         element = gp2.elementAt(index)
         if(element.type == QtGui.QPainterPath.CurveToElement or
            element.type == QtGui.QPainterPath.MoveToElement  or
            element.type == QtGui.QPainterPath.LineToElement):
            type_index_list.append(index)
      #print(type_index_list)
      if(reversed):
         deltaX = gp1.currentPosition().x();
         deltaY = gp1.currentPosition().y();

         last_type_index = type_index_list[len(type_index_list) - 1]
         last_type = gp2.elementAt(last_type_index).type

         if(last_type == QtGui.QPainterPath.MoveToElement):
            last_p1 = QtCore.QPointF(gp2.elementAt(last_type_index))
            deltaX -= last_p1.x()
            deltaY -= last_p1.y()
         elif(last_type == QtGui.QPainterPath.LineToElement):
            last_p1 = QtCore.QPointF(gp2.elementAt(last_type_index))
            deltaX -= last_p1.x()
            deltaY -= last_p1.y()
         elif(last_type == QtGui.QPainterPath.CurveToElement):
            last_p3 = QtCore.QPointF(gp2.elementAt(last_type_index+2))
            deltaX -= last_p3.x()
            deltaY -= last_p3.y()
         else:
         	print("Incorrect type")

         j = len(type_index_list)-1
         while(j>0):
            type_index = type_index_list[j]
            element = gp2.elementAt(type_index)

            pre_type_index = type_index_list[j-1]
            pre_element = gp2.elementAt(pre_type_index)

            type = element.type
            prevType = pre_element.type

            prevX = 0.0
            prevY = 0.0

            if(prevType == QtGui.QPainterPath.MoveToElement or prevType == QtGui.QPainterPath.LineToElement):
               pre_p1 = QtCore.QPointF(gp2.elementAt(pre_type_index))
               prevX = pre_p1.x()
               prevY = pre_p1.y()
            elif(prevType == QtGui.QPainterPath.CurveToElement):
               pre_p3 = QtCore.QPointF(gp2.elementAt(pre_type_index+2))
               prevX = pre_p3.x()
               prevY = pre_p3.y()
            else:
               print("Incorrect type")
               continue

            leftmost = min(leftmost, prevX + deltaX);

            if(type == QtGui.QPainterPath.MoveToElement or type == QtGui.QPainterPath.LineToElement):
               gp1.lineTo(prevX + deltaX, prevY + deltaY);
            elif(type == QtGui.QPainterPath.CurveToElement):
               #print(type_index)
               p1 = QtCore.QPointF(gp2.elementAt(type_index))
               p2 = QtCore.QPointF(gp2.elementAt(type_index+1))
               p3 = QtCore.QPointF(gp2.elementAt(type_index+2))
               gp1.cubicTo(p2.x() + deltaX, p2.y() + deltaY, p1.x() + deltaX, p1.y() + deltaY, prevX + deltaX, prevY + deltaY);
            else:
               print("Incorrect type")

            j -= 1
      else: # Not reversed
         #print(type_index_list)
         element = gp2.elementAt(type_index_list[0])
         p0 = QtCore.QPointF(element)
         deltaX = gp1.currentPosition().x() - p0.x()
         deltaY = gp1.currentPosition().y() - p0.y()

         for j in range(1,len(type_index_list)):
            type_index = type_index_list[j]
            #print(type_index)
            element = gp2.elementAt(type_index)
            type = element.type

            if(type == QtGui.QPainterPath.MoveToElement):
               pass
            elif(type == QtGui.QPainterPath.LineToElement):
               p1 = QtCore.QPointF(gp2.elementAt(type_index))
               gp1.lineTo(p1.x() + deltaX, p1.y() + deltaY);
               leftmost = min(leftmost, p1.x() + deltaX);
            elif(type == QtGui.QPainterPath.CurveToElement):
               p1 = QtCore.QPointF(gp2.elementAt(type_index))
               p2 = QtCore.QPointF(gp2.elementAt(type_index+1))
               p3 = QtCore.QPointF(gp2.elementAt(type_index+2))
               gp1.cubicTo(p1.x() + deltaX, p1.y() + deltaY, p2.x() + deltaX, p2.y() + deltaY, p3.x() + deltaX, p3.y() + deltaY);

               leftmost = min(leftmost, p3.x() + deltaX);
            else:
               print("Incorrect type")


   def makeCornerTo(gp, cornerPoint, nextCornerPoint, radius):
      currentPoint = gp.currentPosition();

      # get fractional to the corner where the line first starts to curve
      distance = BlockShapeUtil.dist(currentPoint.x(),currentPoint.y(),cornerPoint.x(),cornerPoint.y());
      fraction = (distance - radius) / distance;

      # calculate these distance from the current point
      xDistance = (cornerPoint.x() - currentPoint.x()) * fraction;
      yDistance = (cornerPoint.y() - currentPoint.y()) * fraction;

      # draw a line to the point where the line first starts to curve
      BlockShapeUtil.lineToRelative(gp, xDistance, yDistance);

      startCurvePoint = gp.currentPosition();


      # get fractional to the corner where the line first starts to curve
      distanceFromCornerToNextCorner = BlockShapeUtil.dist(cornerPoint.x(),cornerPoint.y(),nextCornerPoint.x(),nextCornerPoint.y());
      fractionToNextCorner = radius / distanceFromCornerToNextCorner;

      # calculate these distance from the current point
      xDistanceFromCornerToEndCurve = (nextCornerPoint.x() - cornerPoint.x()) * fractionToNextCorner;
      yDistanceFromCornerToEndCurve = (nextCornerPoint.y() - cornerPoint.y()) * fractionToNextCorner;


      endCurvePoint = QtCore.QPoint(cornerPoint.x() + xDistanceFromCornerToEndCurve,
        cornerPoint.y() + yDistanceFromCornerToEndCurve);


      # finally draw the cornerShape
      BlockShapeUtil.cornerShape(gp,
        #start at:
        startCurvePoint.x(), startCurvePoint.y(),
        #corner at:
        cornerPoint.x(), cornerPoint.y(),
        #end at:
        endCurvePoint.x(), endCurvePoint.y());

      #    		System.out.println("StartCurve at: " + startCurvePoint);
      #    		System.out.println("Corner at: " + cornerPoint);
      #    		System.out.println("EndCurve at: " + endCurvePoint);
      #    		System.out.println("NextCorner at: " + nextCornerPoint);



   class BevelCacheKey():

      def __init__(self, width, height, area):
         self.width = width;
         self.height = height;
         self.area = area;
         self.hashCode = computeHashCode();


      def computeHashCode(self):
         hash = self.width * 1313 + self.height * 71;
         # Area.hashCode() is not implemented, so we have to do it ourselves..
         pi = area.getPathIterator(null);
         arg = double[6];
         while (not pi.isDone()):

            for i in range(0,6): arg[i] = 0;

            val = pi.getWindingRule();
            val += 3 * pi.currentSegment(arg);
            for i in range(0,6):
               val = (val * 5) + floor(arg[i] * 1000);

            hash = hash * 7 + val;
            pi.next();


         return hash;


      def equals(self, o):
         if not (instanceof(o,BevelCacheKey) or o.hashCode() != hashCode):
            return false;
         b = o;
         return width == b.width and height == b.height and area.equals(b.area);


      def hashCode():
         return self.hashCode;


   BEVEL_CACHE_SIZE = 200;
   bevelCache = {}


   def getBevelImage(width, height, s):
      #key = BlockShapeUtil.BevelCacheKey(width, height, s);

      #img = bevelCache.get(key);
      #if (img != None):
      #   # System.out.println("Found cached bevel!");
      #   return img;

      # System.out.println("Not found cached bevel!");
      # generic light vector - "chosen to look good"
      light = ShapeBevel.getLightVector(-1,-2,2);
      bevelSize = 3;
      # create image
      img = img = QtGui.QImage(
            width,
            height,
            QtGui.QImage.Format_ARGB32);
            #(width, height, Transparency.TRANSLUCENT);
      img.fill(255);
      painter = QtGui.QPainter(img);
      painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
      #g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
      #brush = QtGui.QBrush(ShapeBevel.getFrontFaceOverlay(light));
      #painter.setColor(ShapeBevel.getFrontFaceOverlay(light));
      #painter.fillPath(s,brush);
      ShapeBevel.createShapeBevel(painter, s, 0.1, bevelSize, bevelSize, light);
      # Make a copy of the Area to prevent aliasing.
      #key2 = BevelCacheKey(width, height, s);
      #bevelCache.put(key2, img);
      return img;

class ShapeBevel():
  def getLightVector( x, y,z):
    # normalized light vector
    light = [x,y,z];
    lightLen = math.sqrt(light[0]*light[0]+light[1]*light[1]+light[2]*light[2]);
    light[0] /= lightLen; light[1] /= lightLen; light[2] /= lightLen;
    return light;

  def getFrontFaceOverlay(light):
    frontNorm = [0,0,1];
    frontGrayAlpha = [0,0]; # receives gray,alpha
    ShapeBevel.getLightingOverlay(frontNorm,light,frontGrayAlpha);
    return QtGui.QColor(frontGrayAlpha[0],frontGrayAlpha[0],frontGrayAlpha[0],frontGrayAlpha[1]);


  def getLightingOverlay( norm, light, grayAlpha):
    '''
    * takes a normalized surface normal and normalized light vector and returns
    * a (gray,alpha) color value to be applied to the block
    '''     
    # dot product with light produces diffuse shading
    lum = norm[0]*light[0] + norm[1]*light[1] + norm[2]*light[2];
    # amount of white to apply (float const is an arbitrary strength)
    shine = (2*norm[2]*lum - light[2]);
    if (shine < 0): shine = 0;
    shine = shine*shine*shine*shine*0.9;
    if (lum < 0): lum = 0;
    # amount of black to apply (float const is an arbitrary strength)
    shad = (1.0-lum);
    shad = shad*shad;
    shad *= 0.8;
    # combine the effects of overlaying shad black and shine white
    grayAlpha[1] = shad+shine-shad*shine;
    if (shine > 0): grayAlpha[0] = shine/grayAlpha[1];
    else: grayAlpha[0] = 0;

  def createShapeBevel(g2,theShape,flatness,numBands, bevelSize,light):
    # draw bands from inside of shape to outside (important)
    numBands = 3

    for  i in range(numBands-1,-1,-1):
       # get the path around the block area, flattening any curves
       # 0.2 is flattening tolerance, big == faster, small == smoother
       bi = BevelIterator(theShape,flatness);

       # cos and sin of angle between surface normal and screen plane
       theCos = 1.0-(i+0.5)/numBands; # center of band
       theSin = math.sqrt(1-theCos*theCos);

       _from = 0; # draw strips from outer edge,
       to = 1.0/numBands*(i+1)*bevelSize; # to this distance
       # the overlap makes sure there is no tiny space between the bands

       pen = QtGui.QPen()
       #g2.setStroke(BasicStroke(to-_from));
       pen.setWidth(to-_from)
       p = QtCore.QPoint(0,0)
       norm = [0,0,0]
       grayAlpha = [0,0]; # receives gray and alpha

       while (not bi.isDone()):
          #count++;
          bi.nextSegment();

          norm[0] = bi.perpVec.x()*theCos;
          norm[1] = bi.perpVec.y()*theCos;
          norm[2] = theSin;
          ShapeBevel.getLightingOverlay(norm,light,grayAlpha);
          #print(grayAlpha)
          brush = QtGui.QBrush(QtGui.QColor(grayAlpha[0]*255,grayAlpha[0]*255,grayAlpha[0]*255,grayAlpha[1]*255));
          #pen.setColor(QtGui.QColor(grayAlpha[0]*255,grayAlpha[0]*255,grayAlpha[0]*255,grayAlpha[1]*255))
          #g2.setComposite(AlphaComposite.Src);

          gp =  QtGui.QPainterPath();
          p = bi.insetPoint2(_from); gp.moveTo(p);
          p = bi.insetPoint3(_from); gp.lineTo(p);
          p = bi.insetPoint3(to); gp.lineTo(p);
          p = bi.insetPoint2(to); gp.lineTo(p);
          gp.closeSubpath ();
          g2.fillPath(gp,brush);

class BevelIterator():

  def __init__(self,area, flatness):
    # the point that comes before the current segment's start-point */
    self.pt1 = QtCore.QPointF(0,0);
    # the start-point of the current segment */
    self.pt2 = QtCore.QPointF(0,0);
    # the end-point of the current segment */
    self.pt3 = QtCore.QPointF(0,0);
    # the point that comes after the current segment's end-point */
    self.pt4 = QtCore.QPointF(0,0);
    # a vector pointing inwards from <code>pt2</code>, bisecting the angle at that point,
    # scaled to have a length appropriate for a bevel of thickness 1.0 (in other words, lying
    # on the line that is parallel to the current segment and a distance of 1.0 inwards). */
    self.inset2 = QtCore.QPointF(0,0);
    # a vector pointing inwards from <code>pt3</code>, bisecting the angle at that point,
    # scaled to have a length appropriate for a bevel of thickness 1.0 (in other words, lying
    # on the line that is parallel to the current segment and a distance of 1.0 inwards). */
    self.inset3 = QtCore.QPointF(0,0);
    # a unit vector perpendicular to the current segment, pointing outwards */
    self.perpVec = QtCore.QPointF(0,0);

    self.point_index = 0
    self.array = [0,0,0,0,0,0];
    self.area = area;
    self.flatness = flatness;

    self.points = self.doGetPoints(area,flatness);
    #print (self.points)
    self._iter = iter(self.points)

    self.progress = -2;
    self.pathIterAdvance();
    self.doGetPoint()
    self.pt1 = self.currentPoint
    self.pathIterAdvance();
    self.pt2 = self.currentPoint
    self.pathIterAdvance();
    self.pt3 = self.currentPoint
    self.pathIterAdvance();
    self.pt4 = self.currentPoint

    self.inset2 = self.getInsetVector(self.pt1,self.pt2,self.pt3)
    self.inset3 = self.getInsetVector(self.pt2,self.pt3,self.pt4)
    self.perpVec = self.getPerpVec(self.pt2,self.pt3);

  def printPath(path):
    for i in range(0, path.elementCount()):
      cur = path.elementAt(i);

      if(cur.type == QtGui.QPainterPath.MoveToElement):
        print("M %d %d"%(cur.x,cur.y))
      elif(cur.type == QtGui.QPainterPath.LineToElement):
        print("L %d %d"%(cur.x,cur.y))
      elif(cur.type == QtGui.QPainterPath.CurveToElement):
        c1 = path.elementAt(i + 1);
        c2 = path.elementAt(i + 2);

        assert(c1.type == QtGui.QPainterPath.CurveToDataElement);
        assert(c2.type == QtGui.QPainterPath.CurveToDataElement);


        print("C (%d %d) (%d %d) (%d %d)"%(cur.x,cur.y,c1.x,c1.y,c2.x,c2.y));

        i += 2;
      elif(cur.type == QtGui.QPainterPath.CurveToDataElement):
          pass

  def doGetPoints(self,area,flatness):

    points = []

    #BevelIterator.printPath(area)

    index = 0

    p = QtCore.QPointF(0,0)
    while(index < area.elementCount()):
      cur = area.elementAt(index);
      p1 = QtCore.QPointF(cur)
      if(cur.type == QtGui.QPainterPath.CurveToElement):

        p2 = QtCore.QPointF(area.elementAt(index+1))
        p3 = QtCore.QPointF(area.elementAt(index+2))

        assert(area.elementAt(index+1).type == QtGui.QPainterPath.CurveToDataElement)
        assert(area.elementAt(index+2).type == QtGui.QPainterPath.CurveToDataElement)

        bezier = Bezier(p,p1,p2,p3)
        curve_points = bezier.getCurvePoints()

        points += curve_points
        index += 2
      else:
        points.append(p1)
        p = p1
        index += 1
    return points

  def doGetPoint(self):
    self.currentPoint = self.current_value
    return self.currentPoint;

  def pathIterAdvance(self):
    if (self.progress < -1):
       self.current_value = next(self._iter)
       self.currentPoint = self.current_value
       self.progress+=1;
       return

    try:
       self.current_value = next(self._iter)
       if (self.progress >= 0):
          self.progress+=1; # this isn't the first time around, counting now
    except StopIteration:
       self._iter = iter(self.points)
       self.current_value = next(self._iter)
       self.progress += 1

    p = self.currentPoint;
    self.doGetPoint();
    if ((p.x()-self.currentPoint.x())*(p.x()-self.currentPoint.x())+(p.y()-self.currentPoint.y())*(p.y()-self.currentPoint.y())
       < 0.001):
       self.pathIterAdvance();

  def isDone(self):
    return self.progress >= 2;

  def nextSegment(self):
    if (not self.isDone()):
       self.pathIterAdvance();
       self.pt1 = self.pt2
       self.pt2 = self.pt3
       self.pt3 = self.pt4
       self.pt4 = self.currentPoint
       self.inset2 = self.inset3
       self.inset3 = self.getInsetVector(self.pt2,self.pt3,self.pt4);
       self.perpVec = self.getPerpVec(self.pt2,self.pt3);


  def getInsetVector(self, pt1, pt2, pt3):
    '''
    * a vector parallel to the angle bisector of angle 123,
    * pointing into the block area
    * that assumes a bevel size of 1
    '''
     
    v1 = QtCore.QPointF(pt1.x()-pt2.x(),pt1.y()-pt2.y())
    v2 = QtCore.QPointF(pt3.x()-pt2.x(),pt3.y()-pt2.y())

    # normalize them
    len = math.sqrt(v1.x()*v1.x()+v1.y()*v1.y());
    v1.setX(v1.x()/len)
    v1.setY(v1.y()/len)

    len = math.sqrt(v2.x()*v2.x()+v2.y()*v2.y());
    v2.setX(v2.x()/len)
    v2.setY(v2.y()/len)

    out = QtCore.QPointF(v1.x()+v2.x(),v1.y()+v2.y()); # add vectors
    if (out.x() == 0 and out.y() == 0):
       out.setX(-v1.y());
       out.setY(v1.x());

    else:
       # fix length
       if((-v1.y()*v2.x()+v1.x()*v2.y()) != 0):
          scale = 1.0/(-v1.y()*v2.x()+v1.x()*v2.y());
       else:
          scale = 1.0
       out.setX(out.x() *scale)
       out.setY(out.y() *scale)
    return out

  # returns unit vector perpendicular to the line joining the points */
  def getPerpVec(self,pt1, pt2):
    # perpendicular vector
    vec = QtCore.QPointF(-(pt2.y()-pt1.y()),(pt2.x()-pt1.x()));
    # normalize
    len = math.sqrt(vec.x()*vec.x()+vec.y()*vec.y());
    vec.setX(vec.x()/len)
    vec.setY(vec.y()/len)
    return vec

  def insetPoint2(self,scalar):
      p = QtCore.QPointF()
      p.setX(self.pt2.x()+self.inset2.x()*scalar);
      p.setY(self.pt2.y()+self.inset2.y()*scalar);
      return p;

  def insetPoint3(self,scalar):
      p = QtCore.QPointF()
      p.setX(self.pt3.x()+self.inset3.x()*scalar);
      p.setY(self.pt3.y()+self.inset3.y()*scalar);
      return p;
