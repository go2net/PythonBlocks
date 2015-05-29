#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from PyQt4 import QtCore

class Bezier():

   def __init__(self,start_point, c1,c2, end_point):
      steps = 50
      controlPoints = (start_point,c1,c2,end_point)
      
      self.curvePoints = []
      self.bezier_curve_range(steps, controlPoints)


   def getCurvePoints(self):
      return self.curvePoints

   def bezier_curve_range(self,n, points):
       """Range of points in a curve bezier"""
       for i in range(0,n):
           t = i / float(n - 1)
           self.curvePoints.append(self.bezier(t, points))

   def bezier(self,t, points):
       """Calculate coordinate of a point in the bezier curve"""
       n = len(points) - 1
       x = y = 0
       for i, pos in enumerate(points):
           bern = self.bernstein(t, i, n)
           x += pos.x() * bern
           y += pos.y() * bern
       return QtCore.QPointF(x, y)

   def binomial(self,i, n):
       """Binomial coefficient"""
       return math.factorial(n) / float(
           math.factorial(i) * math.factorial(n - i))


   def bernstein(self,t, i, n):
       """Bernstein polynom"""
       return self.binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))
