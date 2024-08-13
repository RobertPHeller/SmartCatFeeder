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
#  Last Modified : <240813.1436>
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
import TouchDisplay

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
    __Width  = 7.75 * 25.4
    __Height = 20  * 25.4
    __ExtraHeight = 5 * 25.4
    __BinBottomOffset = 4 * 25.4
    __BackDepth = 2.75 * 25.4
    __Length = 7.5 * 25.4
    __Thickness = .125 * 25.4
    __FingerWidth = .5 * 25.4
    __BaseThick = (3.0/8.0) * 25.4
    __BowlExtension = 4 * 25.4
    __pi4StandoffHeight = 6
    __pi4ZOffset = 6
    __Color = tuple([210.0/255.0,180.0/255.0,140.0/255.0])
    __BaseColor = tuple([1.0,1.0,0.0])
    __LidColor  = tuple([1.0,1.0,1.0])
    __StandoffColor = tuple([0.0,1.0,1.0])
    __pi4StandoffDiameter = 6
    __BatteryHeight = (3.7+.125)*25.4
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
        self.left = Part.makePlane(self.__Height+self.__ExtraHeight,self.__Length,leftOrigin,XNorm)\
                        .extrude(Base.Vector(self.__Thickness,0,0))
        self.left = self.left.cut(self.bottom).cut(self.front)
        leftCutOrigin = leftOrigin.add(Base.Vector(0,-self.__BackDepth,self.__Height))
        leftcut = Part.makePlane(self.__ExtraHeight,\
                                 self.__Length-self.__BackDepth,\
                                 leftCutOrigin,XNorm)\
                         .extrude(Base.Vector(self.__Thickness,0,0))
        self.left = self.left.cut(leftcut)
        rightOrigin = origin.add(Base.Vector(self.__Width,self.__Length,\
                        self.__Height+self.__ExtraHeight))
        self.right = Part.makePlane(self.__Height+self.__ExtraHeight,self.__Length,rightOrigin,NegXNorm)\
                        .extrude(Base.Vector(-self.__Thickness,0,0))
        self.right = self.right.cut(self.bottom).cut(self.front)
        rightCutOrigin = rightOrigin.add(Base.Vector(0,-self.__BackDepth,0))
        rightcut = Part.makePlane(self.__ExtraHeight,\
                                  self.__Length-self.__BackDepth,\
                                  rightCutOrigin,NegXNorm)\
                         .extrude(Base.Vector(-self.__Thickness,0,0))
        self.right = self.right.cut(rightcut)
        backOrigin = origin.add(Base.Vector(0,\
                                            self.__Length-self.__BackDepth,\
                                            self.__Height+self.__ExtraHeight))
        self.back = Part.makePlane(self.__Height+self.__ExtraHeight,\
                                   self.__Width,backOrigin,\
                                   NegYNorm)\
                    .extrude(Base.Vector(0,-self.__Thickness,0))
        self.back = self.back.cut(self.bottom)
        self.back = self.__cutZYfingers(self.back,startz=0,endz=self.__Height+self.__ExtraHeight,\
                                      yoffset=self.__Length-self.__BackDepth-self.__Thickness)
        self.back = self.__cutZYfingers(self.back,startz=0,endz=self.__Height+self.__ExtraHeight,\
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
        self.b1 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,0,\
                                    self.__BatteryHeight-self.__BaseThick)),\
                                   self.__Length)
        self.b2 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,\
                                    self.__BackDepth-self.__Thickness,\
                                    self.__BatteryHeight-self.__BaseThick)),\
                                   self.__Length)
        
        lidOrigin = origin.add(Base.Vector(0,0,self.__Height))
        self.lid = Part.makePlane(self.__Width,\
                                  self.__Length-self.__BackDepth,\
                                  lidOrigin,ZNorm)\
                          .extrude(Base.Vector(0,0,self.__Thickness))
        topOrigin = lidOrigin.add(Base.Vector(0,self.__Length-self.__BackDepth,\
                                              self.__ExtraHeight))
        self.top = Part.makePlane(self.__Width,\
                                  self.__BackDepth,\
                                  topOrigin,ZNorm)\
                          .extrude(Base.Vector(0,0,self.__Thickness))
        #pi4Origin = origin.add(Base.Vector(self.__Thickness,\
        #                                   self.__Length-\
        #                                   self.__BackDepth-\
        #                                   (self.__pi4StandoffHeight+\
        #                                    self.__Thickness),\
        #                                   self.__BaseThick+\
        #                                   self.__pi4ZOffset+\
        #                                   Pi4.Pi4.__Width))
        #self.pi4 = Pi4.Pi4(self.name+"__pi4",pi4Origin)
        #self.left = self.left.cut(self.pi4.usb1Cutout(0,self.__Thickness))
        #self.left = self.left.cut(self.pi4.usb2Cutout(0,self.__Thickness))
        #self.left = self.left.cut(self.pi4.ethCutout(0,self.__Thickness))
        #self.back = self.back.cut(self.pi4.MountingHole(1,backOrigin.y,self.__Thickness))
        #self.back = self.back.cut(self.pi4.MountingHole(2,backOrigin.y,self.__Thickness))
        #self.back = self.back.cut(self.pi4.MountingHole(3,backOrigin.y,self.__Thickness))
        #self.back = self.back.cut(self.pi4.MountingHole(4,backOrigin.y,self.__Thickness))
        #self.pi4Standoffs = dict()
        #for i in range(1,5):
        #    self.pi4Standoffs[i] = self.pi4.Standoff(i,\
        #                                    (self.__Length-self.__BackDepth)-\
        #                                    self.__Thickness,\
        #                                    self.__pi4StandoffDiameter,\
        #                                    self.__pi4StandoffHeight)
        self.chargerps = ChargerPS.ChargerPSBox(self.name+"__chargerPSox",\
                                                backOrigin.add(\
                                                 Base.Vector(self.__Thickness*2.5,\
                                                             0,\
                                                             -(self.__Height-self.__BinBottomOffset-3*25.4))))
        for i in range(1,5):
            self.back = self.back.cut(\
                self.chargerps.board.MountingHole(i,backOrigin.y,\
                                                  -self.__Thickness))
        for i in range(1,3):
            self.back = self.back.cut(\
                self.chargerps.transformer.MountingHole(i,backOrigin.y,\
                                                        -self.__Thickness))
        screenXOff = (self.__Width-TouchDisplay.RaspberryPiTouchDisplay.OuterWidth())/2.0
        screenZOff = -self.__ExtraHeight+((self.__ExtraHeight-TouchDisplay.RaspberryPiTouchDisplay.OuterHeight())/2.0)
        touchOrigin = backOrigin.add(Base.Vector(screenXOff,-(self.__Thickness+1),screenZOff))
        self.screen = TouchDisplay.RaspberryPiTouchDisplay("screen",\
                                                            touchOrigin)
        self.back = self.back.cut(self.screen.body)
        self.screenbracket = self.screen.MakeMountingBracket(self.__Thickness)
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
        self.screen.show(doc)
        #self.pi4.show()
        #for i in range(1,5):
        #    obj = doc.addObject("Part::Feature",self.name+("_standoff%d"%(i)))
        #    obj.Shape = self.pi4Standoffs[i]
        #    obj.Label=self.name+("_standoff%d"%(i))
        #    obj.ViewObject.ShapeColor=self.__StandoffColor
        self.chargerps.show()
        obj = doc.addObject("Part::Feature",self.name+"_screenBracket")
        obj.Shape = self.screenbracket
        obj.Label=self.name+"_screenBracket"
        obj.ViewObject.ShapeColor=self.__StandoffColor
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
    Gui.activeDocument().activeView().viewRear()
    Gui.SendMsgToActiveView("ViewFit")
        
