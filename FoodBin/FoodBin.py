#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Sep 12 20:13:56 2021
#  Last Modified : <210912.2356>
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
import Part, Drawing
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

class FoodBin(object):
    _Width  = 7.5 * 25.4
    _Height = 20  * 25.4
    _BinBottomOffset = 4 * 25.4
    _BackDepth = 2 * 25.4
    _Length = 7.5 * 25.4
    _Thickness = .125 * 25.4
    _FingerWidth = .5 * 25.4
    _Color = tuple([210.0/255.0,180.0/255.0,140.0/255.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        XNorm=Base.Vector(1,0,0)
        NegXNorm=Base.Vector(-1,0,0)
        YNorm=Base.Vector(0,1,0)
        NegYNorm=Base.Vector(0,-1,0)
        ZNorm=Base.Vector(0,0,1)
        bottomOrigin = origin.add(Base.Vector(0,0,\
                                              self._BinBottomOffset))
        self.bottom = Part.makePlane(self._Width,\
                                     self._Length-self._BackDepth,\
                                     bottomOrigin,ZNorm)\
                                .extrude(Base.Vector(0,0,self._Thickness))
        self.bottom = self.cutXZfingers(self.bottom,\
                                        yoffset=0,\
                                        zoffset=self._BinBottomOffset,\
                                        endx=self._Width)
        self.bottom = self.cutXZfingers(self.bottom,\
                                        zoffset=self._BinBottomOffset,\
                                        yoffset=self._Length-self._Thickness-self._BackDepth,\
                                        endx=self._Width,\
                                        )
        self.bottom = self.cutYZfingers(self.bottom,\
                                        zoffset=self._BinBottomOffset,\
                                        starty=0,\
                                        endy=self._Length-self._BackDepth)
        self.bottom = self.cutYZfingers(self.bottom,\
                                        zoffset=self._BinBottomOffset,\
                                        starty=0,\
                                        endy=self._Length-self._BackDepth,\
                                        xoffset=self._Width-self._Thickness)
        frontOrigin = origin.add(Base.Vector(0,0,self._BinBottomOffset))
        self.front = Part.makePlane(self._Height-self._BinBottomOffset,\
                                    self._Width,frontOrigin,YNorm)\
                              .extrude(Base.Vector(0,self._Thickness,0))
        self.front = self.front.cut(self.bottom)
        self.front = self.cutZYfingers(self.front,\
                                        startz=self._BinBottomOffset,\
                                        endz=self._Height) 
        self.front = self.cutZYfingers(self.front,\
                                        startz=self._BinBottomOffset,\
                                        endz=self._Height,\
                                        xoffset=self._Width-self._Thickness)
        leftOrigin = origin.add(Base.Vector(0,self._Length,0))
        self.left = Part.makePlane(self._Height,self._Length,leftOrigin,XNorm)\
                        .extrude(Base.Vector(self._Thickness,0,0))
        self.left = self.left.cut(self.bottom).cut(self.front)
        rightOrigin = origin.add(Base.Vector(self._Width,self._Length,self._Height))
        self.right = Part.makePlane(self._Height,self._Length,rightOrigin,NegXNorm)\
                        .extrude(Base.Vector(-self._Thickness,0,0))
        self.right = self.right.cut(self.bottom).cut(self.front)
        backOrigin = origin.add(Base.Vector(0,\
                                            self._Length-self._BackDepth,\
                                            self._Height))
        self.back = Part.makePlane(self._Height,self._Width,backOrigin,NegYNorm)\
                    .extrude(Base.Vector(0,-self._Thickness,0))
        self.back = self.back.cut(self.bottom)
        self.back = self.cutZYfingers(self.back,startz=0,endz=self._Height,\
                                      yoffset=self._Length-self._BackDepth-self._Thickness)
        self.back = self.cutZYfingers(self.back,startz=0,endz=self._Height,\
                                      yoffset=self._Length-self._BackDepth-self._Thickness,\
                                      xoffset=self._Width-self._Thickness)
        self.left = self.left.cut(self.back)
        self.right = self.right.cut(self.back)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_bottom")
        obj.Shape = self.bottom
        obj.Label=self.name+"_bottom"
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_front")
        obj.Shape = self.front
        obj.Label=self.name+"_front"
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_left")
        obj.Shape = self.left
        obj.Label=self.name+"_left"
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_right")
        obj.Shape = self.right
        obj.Label=self.name+"_right"
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+"_back")
        obj.Shape = self.back
        obj.Label=self.name+"_back"
        obj.ViewObject.ShapeColor=self._Color
    def cutXZfingers(self,panel,*,startx=0,endx=0,zoffset=0,yoffset=0):
        x = startx
        ZNorm=Base.Vector(0,0,1)
        while x <= endx:
            panel = panel.cut(Part.makePlane(self._FingerWidth,\
                                             self._Thickness,\
                                             self.origin.add(Base.Vector(x,yoffset,zoffset)),\
                                             ZNorm).extrude(Base.Vector(0,0,self._Thickness)))
            x += self._FingerWidth*2
        return panel
    def cutYZfingers(self,panel,*,starty=0,endy=0,zoffset=0,xoffset=0):
        y = starty
        ZNorm=Base.Vector(0,0,1) 
        while y <= endy:
            panel = panel.cut(Part.makePlane(self._Thickness,\
                                             self._FingerWidth,\
                                             self.origin.add(Base.Vector(xoffset,y,zoffset)),\
                                             ZNorm).extrude(Base.Vector(0,0,self._Thickness)))
            y += self._FingerWidth*2
        return panel
    def cutZYfingers(self,panel,*,startz=0,endz=0,yoffset=0,xoffset=0):
        z = startz
        YNorm=Base.Vector(0,1,0)
        while z <= endz:
            panel = panel.cut(Part.makePlane(self._FingerWidth,\
                                             self._Thickness,\
                                             self.origin.add(Base.Vector(xoffset,yoffset,z)),\
                                             YNorm).extrude(Base.Vector(0,self._Thickness,0)))
            z += self._FingerWidth*2
        return panel
if __name__ == '__main__':
    if "FoodBin" in App.listDocuments().keys():
        App.closeDocument("FoodBin")
    doc = App.newDocument("FoodBin")
    doc = App.activeDocument()
    foodbin = FoodBin("foodbin",Base.Vector(0,0,0))
    foodbin.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewIsometric()
        
