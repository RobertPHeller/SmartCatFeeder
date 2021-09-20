#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Sep 19 13:30:40 2021
#  Last Modified : <210920.1224>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2021  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
#*****************************************************************************



import FreeCAD as App
import Part
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

from abc import ABCMeta, abstractmethod, abstractproperty

class Bud_AC(object):
    __metaclass__ = ABCMeta
    @staticmethod
    def A():
        pass
    @staticmethod
    def B():
        pass
    @staticmethod
    def C():
        pass
    @staticmethod
    def TYPE():
        pass
    @staticmethod
    def GUAGE():
        pass
    @staticmethod
    def BRACKETHOLES():
        return False
    def _buildbox(self):
        ox = self.origin.x
        oy = self.origin.y
        oz = self.origin.z
        XNorm=Base.Vector(1,0,0)
        XNorm_=Base.Vector(-1,0,0)
        XThick=Base.Vector(self.GUAGE(),0,0)
        XThick_=Base.Vector(-self.GUAGE(),0,0)
        YNorm=Base.Vector(0,1,0)
        YNorm_=Base.Vector(0,-1,0)
        YThick=Base.Vector(0,self.GUAGE(),0)
        YThick_=Base.Vector(0,-self.GUAGE(),0)
        ZNorm=Base.Vector(0,0,1)
        ZNorm_=Base.Vector(0,0,-1)
        ZThick=Base.Vector(0,0,self.GUAGE())
        ZThick_=Base.Vector(0,0,-self.GUAGE())
        base = Part.makePlane(self.B(),self.A(),self.origin,YNorm).extrude(YThick)
        front = Part.makePlane(self.A(),self.C(),self.origin,ZNorm).extrude(ZThick)
        frontflange = Part.makePlane(.5*25.4,self.A(),\
                                     self.origin.add(Base.Vector(0,\
                                                     self.C()-self.GUAGE(),\
                                                     )),\
                                     YNorm).extrude(YThick_)
        if (self.TYPE() == 'A'):
            center = self.A()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(center,self.C()-self.GUAGE(),(.5-.187)*25.4)),YNorm))).extrude(YThick_)
            frontflange = frontflange.cut(h)
        elif (self.TYPE() == 'B'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(2.969*25.4,self.C(),(.5*25.4)-(0.187*25.4))),YNorm))).extrude(YThick_)
            frontflange = frontflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(self.A()-2.969*25.4,self.C(),(.5*25.4)-(0.187*25.4))),YNorm))).extrude(YThick_)
            frontflange = frontflange.cut(h2)
        elif (self.TYPE() == 'C'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(0.812*25.4,self.C(),.25*25.4)),YNorm))).extrude(YThick_)
            frontflange = frontflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,self.origin.add(Base.Vector(self.A()-0.812*25.4,self.C(),.25*25.4)),YNorm))).extrude(YThick_)
            frontflange = frontflange.cut(h2)
        front = front.fuse(frontflange)
        backorig = self.origin.add(Base.Vector(self.A(),0,self.B()))
        back  = Part.makePlane(self.A(),self.C(),backorig,ZNorm_).extrude(ZThick_)
        backflange = Part.makePlane(.5*25.4,self.A(),\
                                    self.origin.add(Base.Vector(0,\
                                                    self.C()-self.GUAGE(),\
                                                    0+self.B()-(.5*25.4))),\
                                                    YNorm).extrude(YThick_)
        if (self.TYPE() == 'A'):
            center = self.A()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(-center,self.C()-self.GUAGE(),-.187*25.4)),YNorm))).extrude(YThick_)
            backflange = backflange.cut(h)
        elif (self.TYPE() == 'B'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(-2.969*25.4,self.C(),(-.5+0.187)*25.4)),YNorm))).extrude(YThick_)
            backflange = backflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(-(self.A()-2.969*25.4),self.C(),(-.5+0.187)*25.4)),YNorm))).extrude(YThick_)
            backflange = backflange.cut(h2)
        elif (self.TYPE() == 'C'):
            h1 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(-0.812*25.4,self.C(),-.25*25.4)),YNorm))).extrude(YThick_)
            backflange = backflange.cut(h1)
            h2 = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,backorig.add(Base.Vector(-(self.A()-0.812*25.4),self.C(),-.25*25.4)),YNorm))).extrude(YThick_)
            backflange = backflange.cut(h2)
        back = back.fuse(backflange)
        leftorig = self.origin.add(Base.Vector(0,self.C(),self.B()))
        left  = Part.makePlane(self.B(),self.C(),leftorig,XNorm_).extrude(XThick_)
        leftflange = Part.makePlane(self.B(),.5*25.4,\
                                    leftorig.add(Base.Vector(0,\
                                                             0,\
                                                             -self.B())),\
                                    YNorm).extrude(YThick_)
        if (self.TYPE() == 'A'):
            center = self.B()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,leftorig.add(Base.Vector((.5-.187)*25.4,-center,self.C())),YNorm))).extrude(YThick_)
            leftflange = leftflange.cut(h)
        left = left.fuse(leftflange)
        #if (self.BRACKETHOLES()):
        #    bh1 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,leftorig.add(Base.Vector(0,-(25.4-self.GUAGE()),self.C()-25.4)),XNorm))).extrude(XThick)
        #    left = left.cut(bh1)
        #    bh2 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,leftorig.add(Base.Vector(0,-((self.B()+self.GUAGE())-25.4),self.C()-25.4)),XNorm))).extrude(XThick)
        #    left = left.cut(bh2)
        rightorig = self.origin.add(Base.Vector(self.A(),self.C(),0))
        right = Part.makePlane(self.B(),self.C(),rightorig,XNorm).extrude(XThick_)
        rightflange = Part.makePlane(self.B(),.5*25.4,\
                                     rightorig.add(Base.Vector(-.5*25.4,\
                                                               0,0)),\
                                     YNorm).extrude(YThick_)
        if (self.TYPE() == 'A'):
            center = self.B()/2.0
            h = Part.Face(Part.Wire(Part.makeCircle(0.136*25.4*.5,rightorig.add(Base.Vector((-.5+.187)*25.4,-center,self.C())),YNorm))).extrude(YThick_)
            rightflange = rightflange.cut(h)
        right = right.fuse(rightflange)
        #if (self.BRACKETHOLES()):
        #    bh1 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,rightorig.add(Base.Vector(0,-(25.4-self.GUAGE()),self.C()-25.4)),XNorm))).extrude(XThick)
        #    right = right.cut(bh1)
        #    bh2 = Part.Face(Part.Wire(Part.makeCircle(0.219*25.4*.5,rightorig.add(Base.Vector(0,-((self.B()+self.GUAGE())-25.4),self.C()-25.4)),XNorm))).extrude(XThick)
        #    right = right.cut(bh2)
        self.box = base.fuse(front).fuse(back).fuse(left).fuse(right)
    def cutout(self,other):
        self.box = self.box.cut(other)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_ACBox')
        obj.Shape = self.box
        obj.Label=self.name+'_ACBox'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])
        
class Bud_BPA(object):
    __metaclass__ = ABCMeta
    @staticmethod
    def AA():
        pass
    @staticmethod
    def BB():
        pass
    @staticmethod
    def TYPE():
        pass
    def _buildbottom(self,C):
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,.040*25.4,0)
        borig = self.origin.add(Base.Vector((.812-.750)*25.4,C,(.250-.187)*25.4))
        bottom = Part.makePlane(self.AA(),self.BB(),borig,YNorm).extrude(YThick)
        #if self.TYPE() == 'A':
        #    centerA = self.AA()/2.0
        #    centerB = self.BB()/2.0
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(centerB,0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(0.219*25.4,centerA,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(centerB,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-0.219*25.4,centerA,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #elif self.TYPE() == 'B':
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(2.875*25.4,0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-2.875*25.4,0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(2.875*25.4,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-2.875*25.4,self.AA()-0.219*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #elif self.TYPE() == 'C':
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(.750*25.4,0.187*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-.750*25.4,0.187*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(.750*25.4,self.AA()-0.187*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        #    h = Part.Face(Part.Wire(Part.makeCircle(0.187*25.4*.5,borig.add(Base.Vector(self.BB()-.750*25.4,self.AA()-0.187*25.4,0)),ZNorm))).extrude(ZThick)
        #    bottom = bottom.cut(h)
        self.bottom = bottom
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_BPABottom')
        obj.Shape = self.bottom
        obj.Label=self.name+'_BPABottom'
        obj.ViewObject.ShapeColor=tuple([.75,.75,.75])



class AC_402(Bud_AC):
    @staticmethod
    def A():
        return(7.000*25.4)
    @staticmethod
    def B():
        return(5.000*25.4)
    @staticmethod
    def C():
        return(2.000*25.4)
    @staticmethod
    def TYPE():
        return 'A'
    @staticmethod
    def GUAGE():
        return(.040*25.4)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self._buildbox()

class BPA_1589(Bud_BPA):
    @staticmethod
    def AA():
        return 4.812*25.4
    @staticmethod
    def BB():
        return 6.812*25.4
    @staticmethod
    def TYPE():
        return 'A'
    @staticmethod
    def _C():
        return(2.0*25.4)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self._buildbottom(self._C())
        


if __name__ == '__main__':
    if "Box" in App.listDocuments().keys():
        App.closeDocument("Box")
    doc = App.newDocument("Box")
    doc = App.activeDocument()
    Box = AC_402("ac_402",Base.Vector(0,0,0))
    Box.show()
    Bottom = BPA_1589("bpa_1589",Base.Vector(0,0,0))
    Bottom.show()
    Gui.activeDocument().activeView().viewRear()
    Gui.SendMsgToActiveView("ViewFit")
