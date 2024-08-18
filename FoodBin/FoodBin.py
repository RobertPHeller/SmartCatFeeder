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
#  Last Modified : <240818.0937>
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
import Part, TechDraw
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

import AugerMount
import Pi4
import ChargerPS
import Adafruit

class HalfByHalf(object):
    __Width = .5 * 25.4
    @classmethod
    def ZBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(0,0,1))\
                  .extrude(Base.Vector(0,0,length))
        return beam
    @classmethod
    def XBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(1,0,0))\
                  .extrude(Base.Vector(length,0,0))
        return beam
    @classmethod
    def YBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(0,1,0))\
                  .extrude(Base.Vector(0,length,0))
        return beam

class FoodBin(object):
    __Width  = 7.5 * 25.4
    __Height = 20  * 25.4
    __BinBottomOffset = 4 * 25.4
    __BackDepth = 2.75 * 25.4
    __Length = 7.5 * 25.4
    __Thickness = .125 * 25.4
    __FingerWidth = .5 * 25.4
    __BaseThick = (3.0/8.0) * 25.4
    __BowlExtension = 4 * 25.4
    __Adafruit35inTFTZOff = 30
    __Adafruit35inTFTYOff = 30
    __AdafruitPCF8523ZOff = 30+(1.3*25.4)
    __AdafruitPCF8523YOff = 2+25.4
    __AdafruitPCF8523XOff = Adafruit.AdafruitPCF8523.RaisedBoardHeight()
    __AdafruitNAU7802YOff = 2+25.4
    __AdafruitNAU7802ZOff = 30
    __Color = tuple([210.0/255.0,180.0/255.0,140.0/255.0])
    __BaseColor = tuple([1.0,1.0,0.0])
    __LidColor  = tuple([1.0,1.0,1.0])
    __StandoffColor = tuple([0.0,1.0,1.0])
    __BatteryHeight = (3.7+.125)*25.4
    __ChargerAboveBinBottom = 5*25.4
    __wireHoleRadius = .5*25.4
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
                                              self.__BinBottomOffset))
        self.bottom = Part.makePlane(self.__Width,\
                                     self.__Length-self.__BackDepth,\
                                     bottomOrigin,ZNorm)\
                                .extrude(Base.Vector(0,0,self.__Thickness))
        self.bottom = self.__cutXZfingers(self.bottom,\
                                        yoffset=0,\
                                        zoffset=self.__BinBottomOffset,\
                                        endx=self.__Width)
        self.bottom = self.__cutXZfingers(self.bottom,\
                                        zoffset=self.__BinBottomOffset,\
                                        yoffset=self.__Length-self.__Thickness-self.__BackDepth,\
                                        endx=self.__Width,\
                                        )
        self.bottom = self.__cutYZfingers(self.bottom,\
                                        zoffset=self.__BinBottomOffset,\
                                        starty=0,\
                                        endy=self.__Length-self.__BackDepth)
        self.bottom = self.__cutYZfingers(self.bottom,\
                                        zoffset=self.__BinBottomOffset,\
                                        starty=0,\
                                        endy=self.__Length-self.__BackDepth,\
                                        xoffset=self.__Width-self.__Thickness)
        augerMountOrigin = bottomOrigin.add(Base.Vector(self.__Width/2,\
                                                        (3.5/2)*25.4,0))
        self.bottom = AugerMount.AugerMount.CutHoles(self.bottom,\
                                                     augerMountOrigin,\
                                                     self.__Thickness)
        frontOrigin = origin.add(Base.Vector(0,0,self.__BinBottomOffset))
        self.front = Part.makePlane(self.__Height-self.__BinBottomOffset,\
                                    self.__Width,frontOrigin,YNorm)\
                              .extrude(Base.Vector(0,self.__Thickness,0))
        self.front = self.front.cut(self.bottom)
        self.front = self.__cutZYfingers(self.front,\
                                        startz=self.__BinBottomOffset,\
                                        endz=self.__Height) 
        self.front = self.__cutZYfingers(self.front,\
                                        startz=self.__BinBottomOffset,\
                                        endz=self.__Height,\
                                        xoffset=self.__Width-self.__Thickness)
        leftOrigin = origin.add(Base.Vector(0,self.__Length,0))
        self.left = Part.makePlane(self.__Height,self.__Length,leftOrigin,XNorm)\
                        .extrude(Base.Vector(self.__Thickness,0,0))
        self.left = self.left.cut(self.bottom).cut(self.front)
        rightOrigin = origin.add(Base.Vector(self.__Width,self.__Length,\
                        self.__Height))
        self.right = Part.makePlane(self.__Height,self.__Length,rightOrigin,NegXNorm)\
                        .extrude(Base.Vector(-self.__Thickness,0,0))
        self.right = self.right.cut(self.bottom).cut(self.front)
        backOrigin = origin.add(Base.Vector(0,\
                                            self.__Length-self.__BackDepth,\
                                            self.__Height))
        self.back = Part.makePlane(self.__Height,\
                                   self.__Width,backOrigin,\
                                   NegYNorm)\
                    .extrude(Base.Vector(0,-self.__Thickness,0))
        self.back = self.back.cut(self.bottom)
        self.back = self.__cutZYfingers(self.back,startz=0,endz=self.__Height,\
                                      yoffset=self.__Length-self.__BackDepth-self.__Thickness)
        self.back = self.__cutZYfingers(self.back,startz=0,endz=self.__Height,\
                                      yoffset=self.__Length-self.__BackDepth-self.__Thickness,\
                                      xoffset=self.__Width-self.__Thickness)
        self.left = self.left.cut(self.back)
        self.right = self.right.cut(self.back)
        baseOrigin = origin.add(Base.Vector(self.__Thickness,-self.__BowlExtension,0))
        self.base = Part.makePlane(self.__Width-(2*self.__Thickness),\
                                   self.__Length-self.__BackDepth-\
                                        self.__Thickness+self.__BowlExtension,\
                                   baseOrigin,ZNorm)\
                        .extrude(Base.Vector(0,0,self.__BaseThick))
        batteryBaseOrigin = origin.add(Base.Vector(self.__Thickness,\
                                                   self.__Length-\
                                                   self.__BackDepth,0))
        self.batteryBase = Part.makePlane(self.__Width-(2*self.__Thickness),\
                                          self.__BackDepth,\
                                          batteryBaseOrigin,ZNorm)\
                        .extrude(Base.Vector(0,0,self.__BaseThick))
        self.batteryBack = Part.makePlane(self.__BatteryHeight,\
                                          self.__Width,\
                                          batteryBaseOrigin.add(Base.Vector(\
                                            -self.__Thickness,self.__BackDepth,\
                                            self.__BaseThick+\
                                            self.__BatteryHeight)),\
                                          NegYNorm)\
                                   .extrude(Base.Vector(0,-self.__Thickness,0))
        self.batteryBack = self.__cutZYfingers(self.batteryBack,\
                                startz=self.__BaseThick,\
                                endz=self.__BatteryHeight,\
                                yoffset=self.__Length-self.__Thickness)
        self.batteryBack = self.__cutZYfingers(self.batteryBack,\
                                startz=self.__BaseThick,\
                                endz=self.__BatteryHeight,\
                                yoffset=self.__Length-self.__Thickness,\
                                xoffset=self.__Width-self.__Thickness)
        self.left = self.left.cut(self.batteryBack)
        self.right = self.right.cut(self.batteryBack)
        self.batteryTop = Part.makePlane(self.__Width-25.4-(2*self.__Thickness),\
                                         self.__BackDepth,\
                                         batteryBaseOrigin.add(\
                                            Base.Vector(25.4,0,\
                                        (self.__BatteryHeight-self.__Thickness)+\
                                        self.__BaseThick)))\
                        .extrude(Base.Vector(0,0,self.__Thickness))
        self.batteryBack = self.batteryBack.cut(self.batteryTop)
        self.b1 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,\
                                    self.__Thickness+12.5,\
                                    self.__BatteryHeight-self.__BaseThick)),\
                                   self.__Width-(2*self.__Thickness))
        self.b2 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,\
                                    self.__BackDepth-self.__Thickness,\
                                    self.__BatteryHeight-self.__BaseThick)),\
                                   self.__Width-(2*self.__Thickness))
        
        lidOrigin = origin.add(Base.Vector(0,0,self.__Height))
        self.lid = Part.makePlane(self.__Width,\
                                  self.__Length-self.__BackDepth,\
                                  lidOrigin,ZNorm)\
                          .extrude(Base.Vector(0,0,self.__Thickness))
        topOrigin = lidOrigin.add(Base.Vector(0,self.__Length-self.__BackDepth,0))
        self.top = Part.makePlane(self.__Width,\
                                  self.__BackDepth,\
                                  topOrigin,ZNorm)\
                          .extrude(Base.Vector(0,0,self.__Thickness))
        self.adafruitTFT = Adafruit.AdafruitTFTFeatherWing(self.name+"_adafruitTFT",\
                                                            origin.add(Base.Vector(self.__Thickness,\
                                                                       self.__Adafruit35inTFTYOff,\
                                                                       self.__Adafruit35inTFTZOff)))
        self.left = self.left.cut(self.adafruitTFT.ScreenCutout(-self.__Thickness))
        self.left = self.left.cut(self.adafruitTFT.MakeMountingHole(0,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitTFT.MakeMountingHole(1,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitTFT.MakeMountingHole(2,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitTFT.MakeMountingHole(3,0,self.__Thickness))
        self.adafruitPCF8523 = Adafruit.AdafruitPCF8523(self.name+"_adafruitPCF8523",\
                                               origin.add(Base.Vector(self.__Thickness+self.__AdafruitPCF8523XOff,\
                                                                      self.__AdafruitPCF8523YOff,\
                                                                      self.__AdafruitPCF8523ZOff)))
        self.left = self.left.cut(self.adafruitPCF8523.MakeMountingHole(0,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitPCF8523.MakeMountingHole(1,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitPCF8523.MakeMountingHole(2,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitPCF8523.MakeMountingHole(3,0,self.__Thickness))
        self.adafruitNAU7802 = Adafruit.AdafruitNAU7802(self.name+"_adafruitNAU7802",\
                                                        origin.add(Base.Vector(self.__Thickness,\
                                                                      self.__AdafruitNAU7802YOff,\
                                                                      self.__AdafruitNAU7802ZOff)))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(0,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(1,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(2,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(3,0,self.__Thickness))
        self.chargerps = ChargerPS.ChargerPSBox(self.name+"__chargerPSox",\
                                                backOrigin.add(\
                                                 Base.Vector(self.__Thickness*2.5,\
                                                             0,\
                                                             -(self.__Height-self.__BinBottomOffset-self.__ChargerAboveBinBottom))))
        for i in range(1,5):
            self.back = self.back.cut(\
                self.chargerps.board.MountingHole(i,backOrigin.y,\
                                                  -self.__Thickness))
        for i in range(1,3):
            self.back = self.back.cut(\
                self.chargerps.transformer.MountingHole(i,backOrigin.y,\
                                                        -self.__Thickness))
        wireHoleOrigin = batteryBaseOrigin.add(Base.Vector(self.__wireHoleRadius,\
                                                           -self.__Thickness,\
                                                           self.__BatteryHeight-self.__BaseThick-(2*self.__wireHoleRadius)))
        wireHole = Part.Face(Part.Wire(Part.makeCircle(self.__wireHoleRadius,\
                                                       wireHoleOrigin,\
                                                       Base.Vector(0,1,0))))\
                          .extrude(Base.Vector(0,self.__Thickness,0))
        self.back = self.back.cut(wireHole)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_bottom")
        obj.Shape = self.bottom
        obj.Label=self.name+"_bottom"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_front")
        obj.Shape = self.front
        obj.Label=self.name+"_front"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_left")
        obj.Shape = self.left
        obj.Label=self.name+"_left"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_right")
        obj.Shape = self.right
        obj.Label=self.name+"_right"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_back")
        obj.Shape = self.back
        obj.Label=self.name+"_back"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_base")
        obj.Shape = self.base
        obj.Label=self.name+"_base"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_b1")
        obj.Shape = self.b1
        obj.Label=self.name+"_b1"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_b2")
        obj.Shape = self.b2
        obj.Label=self.name+"_b2"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_batterybase")
        obj.Shape = self.batteryBase
        obj.Label=self.name+"_batterybase"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_batteryBack")
        obj.Shape = self.batteryBack
        obj.Label=self.name+"_batteryBack"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_batteryTop")
        obj.Shape = self.batteryTop
        obj.Label=self.name+"_batteryTop"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_lid")
        obj.Shape = self.lid
        obj.Label=self.name+"_lid"
        obj.ViewObject.ShapeColor=self.__LidColor
        obj.ViewObject.Transparency=90
        obj = doc.addObject("Part::Feature",self.name+"_top")
        obj.Shape = self.top
        obj.Label=self.name+"_top"
        obj.ViewObject.ShapeColor=self.__Color
        self.adafruitTFT.show()
        self.adafruitPCF8523.show()
        self.adafruitNAU7802.show()
        self.chargerps.show()
    def __cutXZfingers(self,panel,*,startx=0,endx=0,zoffset=0,yoffset=0):
        x = startx
        ZNorm=Base.Vector(0,0,1)
        while x <= endx:
            panel = panel.cut(Part.makePlane(self.__FingerWidth,\
                                             self.__Thickness,\
                                             self.origin.add(Base.Vector(x,yoffset,zoffset)),\
                                             ZNorm).extrude(Base.Vector(0,0,self.__Thickness)))
            x += self.__FingerWidth*2
        return panel
    def __cutYZfingers(self,panel,*,starty=0,endy=0,zoffset=0,xoffset=0):
        y = starty
        ZNorm=Base.Vector(0,0,1) 
        while y <= endy:
            panel = panel.cut(Part.makePlane(self.__Thickness,\
                                             self.__FingerWidth,\
                                             self.origin.add(Base.Vector(xoffset,y,zoffset)),\
                                             ZNorm).extrude(Base.Vector(0,0,self.__Thickness)))
            y += self.__FingerWidth*2
        return panel
    def __cutZYfingers(self,panel,*,startz=0,endz=0,yoffset=0,xoffset=0):
        z = startz
        YNorm=Base.Vector(0,1,0)
        while z <= endz:
            panel = panel.cut(Part.makePlane(self.__FingerWidth,\
                                             self.__Thickness,\
                                             self.origin.add(Base.Vector(xoffset,yoffset,z)),\
                                             YNorm).extrude(Base.Vector(0,self.__Thickness,0)))
            z += self.__FingerWidth*2
        return panel

if __name__ == '__main__':
    if "FoodBin" in App.listDocuments().keys():
        App.closeDocument("FoodBin")
    doc = App.newDocument("FoodBin")
    doc = App.activeDocument()
    foodbin = FoodBin("foodbin",Base.Vector(0,0,0))
    foodbin.show()
    Gui.activeDocument().activeView().viewFront()
    Gui.SendMsgToActiveView("ViewFit")
        
