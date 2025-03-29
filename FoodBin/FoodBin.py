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
#  Last Modified : <250329.1205>
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
import Part, TechDraw, Mesh
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

import AugerMount
import Pi4
import ChargerPS
import Adafruit
import DFRobotGearMotor

import csv

class WoodBOM(object):
    _woodBOM = dict()
    @classmethod
    def AddPiece(cls,width,height,length):
        key = (width,height,length)
        if key in cls._woodBOM:
            cls._woodBOM[key] += 1
        else:
            cls._woodBOM[key] = 1
    @staticmethod
    def _normPartSizeMM(t):
        return ("%.3fx%.3fx%.3f" % t)
    @staticmethod
    def _inch(mm):
        return mm / 25.4
    @staticmethod
    def _normPartSizeIN(t):
        X, Y, Z = t
        return ("%.4fx%.4fx%.4f" % (WoodBOM._inch(X), WoodBOM._inch(Y), WoodBOM._inch(Z)))
    _units = 'in'
    @classmethod
    def SetUnits(cls,units):
        if units == 'in' or units == 'mm':
            cls._units = units
        else:
            raise RuntimeError("Unsupport units!")
    @classmethod
    def GetUnits(cls):
        return cls._units
    @classmethod
    def _normPartSize(cls,t):
        if cls._units == 'in':
            return WoodBOM._normPartSizeIN(t)
        elif cls._units == 'mm':
            return WoodBOM._normPartSizeMM(t)
        else:
            raise RuntimeError("Unsupport units!")
    @classmethod
    def ListCuts(cls,filename):
        keys = list(cls._woodBOM.keys())
        keys.sort()
        f = open(filename,"w")
        w = csv.writer(f)
        w.writerow([("Size (%s)" % cls._units),"Count"])
        for key in keys:
            w.writerow([cls._normPartSize(key),cls._woodBOM[key]])
        f.close()
    def __init__(self):
        raise RuntimeError("No Instances allowed for WoodBOM!")
        

class HalfByHalf(object):
    __Width = .5 * 25.4
    @classmethod
    def ZBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(0,0,1))\
                  .extrude(Base.Vector(0,0,length))
        bb = beam.BoundBox
        WoodBOM.AddPiece(bb.XLength,bb.YLength,bb.ZLength)
        return beam
    @classmethod
    def XBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(1,0,0))\
                  .extrude(Base.Vector(length,0,0))
        bb = beam.BoundBox
        WoodBOM.AddPiece(bb.YLength,bb.ZLength,bb.XLength)
        return beam
    @classmethod
    def YBeam(cls,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        beam = Part.makePlane(cls.__Width,cls.__Width,origin,\
                              Base.Vector(0,1,0))\
                  .extrude(Base.Vector(0,length,0))
        bb = beam.BoundBox
        WoodBOM.AddPiece(bb.ZLength,bb.XLength,bb.YLength)
        return beam

            
import math

def radians(degrees):
    return (degrees/180)*math.pi

class Agitator(object):
    __AgitatorDiskDiameter = 50.8 # 2"
    __DiskThickness = .125 * 25.4
    __CenterDowelDiameter = 12.5 # 1/2"
    __OuterDowelDiameter = 6.25  # 1/4"
    __OuterDowelRadius   = .75*25.4
    __OuterDowelStartAngle = 0
    __OuterDowelDeltaAngle = 90
    __AgitatorLength = 4.125 * 25.4
    __AgitatorDiskSpacing = (4 / 3)*25.4
    __CenterDowelLength = 5 * 25.4
    __FrontDowelHoleDiameter = 13.5
    __Color = tuple([210.0/255.0,180.0/255.0,140.0/255.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        self.center = Part.Face(Part.Wire(Part.makeCircle(self.__CenterDowelDiameter/2,\
                                                          origin,
                                                          Base.Vector(0,1,0))))\
                            .extrude(Base.Vector(0,-self.__CenterDowelLength,0))
        self.outerDowels = list()
        for i in range(0,4):
            dang = self.__OuterDowelDeltaAngle*i
            hX = self.__OuterDowelRadius * \
                        math.cos(radians(self.__OuterDowelStartAngle+dang))
            hZ = self.__OuterDowelRadius * \
                        math.sin(radians(self.__OuterDowelStartAngle+dang))
            dowelOrigin = origin.add(Base.Vector(hX,0,hZ))
            self.outerDowels.append(\
                Part.Face(Part.Wire(Part.makeCircle(self.__OuterDowelDiameter/2,\
                                                    dowelOrigin,\
                                                    Base.Vector(0,1,0))))\
                            .extrude(Base.Vector(0,-self.__AgitatorLength,0)))
        self.disks = list()
        for i in range(0,4):
            diskOrigin = origin.add(Base.Vector(0,-(i*self.__AgitatorDiskSpacing),0))
            disk = Part.Face(Part.Wire(Part.makeCircle(self.__AgitatorDiskDiameter/2,\
                                                       diskOrigin,\
                                                       Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,-self.__DiskThickness,0))
            if i == 0:
                disk = DFRobotGearMotor.AgitatorMountPlate.MountYHoleRing(disk,diskOrigin,self.__DiskThickness)
            disk = disk.cut(self.center)
            for j in range(0,4):
                disk = disk.cut(self.outerDowels[j])
            self.disks.append(disk)
    def FrontHole(self,Y,DeltaY):
        hOrigin = Base.Vector(self.origin.x,Y,self.origin.z)
        return Part.Face(Part.Wire(Part.makeCircle(self.__FrontDowelHoleDiameter/2,\
                                                          hOrigin,
                                                          Base.Vector(0,1,0))))\
                            .extrude(Base.Vector(0,DeltaY,0))
        
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_center")
        obj.Shape = self.center
        obj.Label=self.name+"_center"
        obj.ViewObject.ShapeColor=self.__Color
        for i in range(0,4):
            name="_outerDowel%d"%(i+1)
            obj = doc.addObject("Part::Feature",self.name+name)
            obj.Shape = self.outerDowels[i]
            obj.Label=self.name+name
            obj.ViewObject.ShapeColor=self.__Color
        for i in range(0,4):
            name="_disk%d"%(i+1)
            obj = doc.addObject("Part::Feature",self.name+name)
            obj.Shape = self.disks[i]
            obj.Label=self.name+name
            obj.ViewObject.ShapeColor=self.__Color

class Bowl(object):
    __OuterDiameter = 5*25.4
    __BowlLargeDiameter = 4.65*25.4
    __BowlBottomDiameter = 4.0*25.4
    __RimSize       = .25*25.4
    __Height        = 1.25*25.4
    __Thickness     = 1.5
    __Color = tuple([0.8,0.8,0.8])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        outerrad = self.__OuterDiameter/2
        rim = Part.Face(Part.Wire(Part.makeCircle(outerrad,origin.add(Base.Vector(0,0,self.__Height-self.__Thickness))))).extrude(Base.Vector(0,0,self.__Thickness))
        rim = rim.cut(Part.Face(Part.Wire(Part.makeCircle(outerrad-self.__RimSize,origin.add(Base.Vector(0,0,self.__Height-self.__Thickness))))).extrude(Base.Vector(0,0,self.__Thickness)))
        body = Part.makeCone(self.__BowlBottomDiameter/2,\
                             self.__BowlLargeDiameter/2,\
                             self.__Height-self.__Thickness,origin,Base.Vector(0,0,1))  
        inside = Part.makeCone((self.__BowlBottomDiameter/2)-self.__Thickness,\
                               (self.__BowlLargeDiameter/2)-self.__Thickness,\
                               self.__Height-2*self.__Thickness,\
                               origin.add(Base.Vector(0,0,self.__Thickness)),\
                               Base.Vector(0,0,1))
        body = body.cut(inside)
        self.bowl = rim.fuse(body)
    def CutHole(self,part):
        b = Part.Face(Part.Wire(Part.makeCircle((self.__BowlLargeDiameter/2)+self.__Thickness,self.origin))).extrude(Base.Vector(0,0,self.__Height))
        return part.cut(b)
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.bowl
        obj.Label=self.name
        obj.ViewObject.ShapeColor=self.__Color

class FoodBin(object):
    __Width  = 7.5 * 25.4
    @classmethod
    def Width(cls):
        return cls.__Width
    __Height = 20  * 25.4
    @classmethod
    def Height(cls):
        return cls.__Height
    __BinBottomOffset = 7 * 25.4
    __BackDepth = 2.75 * 25.4
    __Length = 8.5 * 25.4
    @classmethod
    def Length(cls):
        return cls.__Length
    __Thickness = .125 * 25.4
    __FingerWidth = .5 * 25.4
    __BaseThick = (3.0/8.0) * 25.4
    __BowlExtension = 7 * 25.4
    __Adafruit35inTFTZOff = 30
    __Adafruit35inTFTYOff = 30+25.4
    __AdafruitPCF8523ZOff = 6*25.4
    __AdafruitPCF8523XOff = 25.4
    __AdafruitNAU7802YOff = 2+(2*25.4)
    __AdafruitNAU7802ZOff = 30
    __Adafruitvl6180xXOff = 25.4
    __Adafruitvl6180xZOff = 8*25.4
    __flapWidth = 3.36*25.4
    __flapHeight = 2.7*25.4
    __Color = tuple([210.0/255.0,180.0/255.0,140.0/255.0])
    __BaseColor = tuple([1.0,1.0,0.0])
    __LidColor  = tuple([1.0,1.0,1.0])
    __StandoffColor = tuple([0.0,1.0,1.0])
    __BatteryHeight = (4+.125)*25.4
    __ChargerAboveBinBottom = 7*25.4
    __wireHoleRadius = .5*25.4
    __bowlZoff = ((3.0/8.0) * 25.4)+12.7+(.125 * 25.4)
    __bowlXoff = (7.5/2)*25.4
    __bowlYoff = -3.5*25.4
    __strainXoff = ((7.5/2)-2.5)*25.4
    __bowlPaddleDiameter = 2*25.4
    __paddleWidth = 25
    __bowlBoxHeight = 12.7+(.125 * 25.4)+(1*25.4)
    __bowlBoxSupportThick = (3/4)*25.4
    __bowlSupportPlateScrewHoleDiameter = (3/16)*25.4
    __powerCordNotchSize = (3/8)*25.4
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
        self.augerMount = AugerMount.AugerMount("argerMount",augerMountOrigin)
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
        bb = self.base.BoundBox
        WoodBOM.AddPiece(bb.ZLength,bb.XLength,bb.YLength)
        batteryBaseOrigin = origin.add(Base.Vector(self.__Thickness,\
                                                   self.__Length-\
                                                   self.__BackDepth,0))
        self.batteryBase = Part.makePlane(self.__Width-(2*self.__Thickness),\
                                          self.__BackDepth,\
                                          batteryBaseOrigin,ZNorm)\
                        .extrude(Base.Vector(0,0,self.__BaseThick))
        bb = self.batteryBase.BoundBox
        WoodBOM.AddPiece(bb.ZLength,bb.XLength,bb.YLength)
        self.batteryBack = Part.makePlane(self.__BatteryHeight,\
                                          self.__Width,\
                                          batteryBaseOrigin.add(Base.Vector(\
                                            -self.__Thickness,self.__BackDepth,\
                                            self.__BaseThick+\
                                            self.__BatteryHeight)),\
                                          NegYNorm)\
                                   .extrude(Base.Vector(0,-self.__Thickness,0))
        self.left = self.left.cut(self.batteryBack)
        self.right = self.right.cut(self.batteryBack)
        self.batteryTop = Part.makePlane(self.__Width-25.4-(2*self.__Thickness),\
                                         self.__BackDepth,\
                                         batteryBaseOrigin.add(\
                                            Base.Vector(25.4,0,\
                                        (self.__BatteryHeight-self.__Thickness)+\
                                        self.__BaseThick)))\
                        .extrude(Base.Vector(0,0,self.__Thickness))
        self.batteryTop = self.__cutXZfingers(self.batteryTop,\
                                                startx=25.4,\
                                                zoffset=(self.__BatteryHeight+self.__BaseThick)-self.__Thickness,\
                                                yoffset=self.__Length-self.__Thickness,\
                                                endx=self.__Width,\
                                              )
        self.batteryBack = self.batteryBack.cut(self.batteryTop)
        #self.b1 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,\
        #                            self.__Thickness+12.5,\
        #                            self.__BatteryHeight-self.__BaseThick)),\
        #                           self.__Width-(2*self.__Thickness))
        #self.b2 = HalfByHalf.XBeam(batteryBaseOrigin.add(Base.Vector(0,\
        #                            self.__BackDepth-self.__Thickness,\
        #                            self.__BatteryHeight-self.__BaseThick)),\
        #                           self.__Width-(2*self.__Thickness))
        self.bTopStop =  Part.makePlane(12.5,self.__Width-(self.__Thickness*2),\
                                batteryBaseOrigin.add(Base.Vector(\
                                        0,self.__Thickness,(self.__BaseThick+self.__BatteryHeight)-self.__Thickness)),NegYNorm)\
                                        .extrude(Base.Vector(0,-self.__Thickness,0))
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
        self.adafruitNAU7802 = Adafruit.AdafruitNAU7802(self.name+"_adafruitNAU7802",\
                                                        origin.add(Base.Vector(self.__Thickness,\
                                                                      self.__AdafruitNAU7802YOff,\
                                                                      self.__AdafruitNAU7802ZOff)))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(0,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(1,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(2,0,self.__Thickness))
        self.left = self.left.cut(self.adafruitNAU7802.MakeMountingHole(3,0,self.__Thickness))
        self.chargerps = ChargerPS.ChargerPSBox(self.name+"_chargerPSox",\
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
        agitatorMotorOrigin = \
            DFRobotGearMotor.DFRobotGearMotor_UpsideDown.OriginFromShaftHole(\
                        bottomOrigin.add(Base.Vector(self.__Width/2,\
                                                     self.__Length-\
                                                     self.__BackDepth+\
                                                     24.4,1.5*25.4)))
        self.agitatorMotor = DFRobotGearMotor.DFRobotGearMotor_UpsideDown(\
                            self.name+"_agitatorMotor",\
                            agitatorMotorOrigin)
        self.back = self.back.cut(self.agitatorMotor.ShaftHole(backOrigin.y,-self.__Thickness))
        for i in range(0,4):
            self.back = self.back.cut(self.agitatorMotor.MountingHole(i,backOrigin.y,-self.__Thickness))
        yoff = DFRobotGearMotor.DFRobotGearMotor.ShaftLength-\
                DFRobotGearMotor.DFRobotGearMotor.ShaftDFlatLength
        mplateOrigin = self.agitatorMotor.shaftOrigin.add(Base.Vector(0,-yoff,0))
        self.agitatorMount = DFRobotGearMotor.AgitatorMountPlate_Y(\
                            self.name+"_agitatorMount",\
                            mplateOrigin)
        agitatorOrigin = mplateOrigin.add(Base.Vector(0,\
                -DFRobotGearMotor.MotorDrivePlate_Y.HubLength,\
                0))
        self.agitator = Agitator(self.name+"_agitator",agitatorOrigin)
        self.front = self.front.cut(self.agitator.FrontHole(frontOrigin.y,self.__Thickness))
        self.vl6180x = Adafruit.Adafruitvl6180x(self.name+"_vl6180x",
                                                origin.add(Base.Vector(\
                                                    self.__Adafruitvl6180xXOff,\
                                                    (self.__Length-self.__BackDepth)-(self.__Thickness+1.6),\
                                                    self.__Adafruitvl6180xZOff)))
        for i in range(0,4):
            self.back = self.back.cut(self.vl6180x.MakeMountingHole(i,backOrigin.y,-self.__Thickness))
        QWICCableHoleOrigin = origin.add(Base.Vector(\
                                        self.__Adafruitvl6180xXOff-12.5,\
                                        self.__Length-self.__BackDepth,\
                                        self.__Adafruitvl6180xZOff+7.5))
        hole = Part.Face(Part.Wire(Part.makeCircle(3.125,QWICCableHoleOrigin,YNorm))).extrude(Base.Vector(0,self.__Thickness,0))
        self.back = self.back.cut(hole)
        self.adafruitPCF8523 = Adafruit.AdafruitPCF8523(self.name+"_adafruitPCF8523",\
                                               origin.add(Base.Vector(self.__Thickness+self.__AdafruitPCF8523XOff,\
                                                                      ((self.__Length-self.__BackDepth)+Adafruit.AdafruitPCF8523.RaisedBoardHeight()),\
                                                                      self.__AdafruitPCF8523ZOff)))
        self.back = self.back.cut(self.adafruitPCF8523.MakeMountingHole(0,backOrigin.y,self.__Thickness))
        self.back = self.back.cut(self.adafruitPCF8523.MakeMountingHole(1,backOrigin.y,self.__Thickness))
        self.back = self.back.cut(self.adafruitPCF8523.MakeMountingHole(2,backOrigin.y,self.__Thickness))
        self.back = self.back.cut(self.adafruitPCF8523.MakeMountingHole(3,backOrigin.y,self.__Thickness))
        self.bowl = Bowl(self.name+"_bowl",\
                         origin.add(Base.Vector(self.__bowlXoff,\
                                                self.__bowlYoff,\
                                                self.__bowlZoff)))
        strainO1 = origin.add(Base.Vector(self.__strainXoff,
                                          self.__bowlYoff,\
                                          self.__BaseThick))
        strainOrigin = Adafruit.StrainGuageVerticalFlipped.OriginStrain(\
                        strainO1.x,strainO1.y,strainO1.z)
        self.strainGuage = Adafruit.StrainGuageVerticalFlipped(\
                    self.name+"_strainGuage",\
                    strainOrigin)
        plength = (self.__bowlXoff-strainOrigin.x)+25.4
        pwidth  = 50.8 #self.__paddleWidth
        paddle = Part.makePlane(plength,pwidth,\
                            strainOrigin.add(Base.Vector(0,-(25.4-12.5),12.7)))\
                    .extrude(Base.Vector(0,0,self.__Thickness))
        pnotch = Part.makePlane(12.7,25.4-12.5,\
                                strainOrigin.add(Base.Vector(0,25.4,\
                                                 12.7)))\
                             .extrude(Base.Vector(0,0,self.__Thickness))
        paddle = paddle.cut(pnotch)
        paddle = paddle.cut(self.strainGuage.StrainMountHole(\
                        0,strainOrigin.z+12.7,\
                        self.__Thickness))
        paddle = paddle.cut(self.strainGuage.StrainMountHole(\
                        1,strainOrigin.z+12.7,\
                        self.__Thickness))
        self.paddle = paddle
        self.leftBowlBoxSupport = Part.makePlane(\
                self.__bowlBoxSupportThick,\
                self.__BowlExtension-12.5,\
                origin.add(Base.Vector(self.__Thickness,\
                                       -self.__BowlExtension,\
                                       self.__BaseThick)))\
            .extrude(Base.Vector(0,0,self.__bowlBoxHeight-self.__Thickness))
        bb = self.leftBowlBoxSupport.BoundBox
        WoodBOM.AddPiece(bb.XLength,bb.ZLength,bb.YLength)
        self.rightBowlBoxSupport = Part.makePlane(\
                self.__bowlBoxSupportThick,\
                self.__BowlExtension+self.__Length-self.__BackDepth-self.__Thickness,\
                origin.add(Base.Vector(self.__Width-(self.__Thickness+self.__bowlBoxSupportThick),\
                                       -self.__BowlExtension,\
                                       self.__BaseThick)))\
            .extrude(Base.Vector(0,0,self.__bowlBoxHeight-self.__Thickness))
        bb = self.rightBowlBoxSupport.BoundBox
        WoodBOM.AddPiece(bb.XLength,bb.ZLength,bb.YLength)
        self.frontBowlBoxSupport = Part.makePlane(\
                    self.__Width-(2*((self.__Thickness+self.__bowlBoxSupportThick))),\
                    self.__bowlBoxSupportThick,\
                    origin.add(Base.Vector(self.__Thickness+self.__bowlBoxSupportThick,\
                    -self.__BowlExtension,\
                    self.__BaseThick)))\
            .extrude(Base.Vector(0,0,self.__bowlBoxHeight-self.__Thickness))
        bb = self.frontBowlBoxSupport.BoundBox
        WoodBOM.AddPiece(bb.YLength,bb.ZLength,bb.XLength)
        bowlSupportPlate = Part.makePlane(\
                    self.__Width-(2*self.__Thickness),\
                    self.__BowlExtension-12.5,\
                    origin.add(Base.Vector(self.__Thickness,\
                                           -self.__BowlExtension,\
                                           self.__BaseThick+(self.__bowlBoxHeight-self.__Thickness))))\
             .extrude(Base.Vector(0,0,self.__Thickness))
        self.bowlSupportPlate = self.bowl.CutHole(bowlSupportPlate)
        self.__bowlSupportPlateScrewHoles()
        a=self.__Length-(self.__powerCordNotchSize/2)
        notch = Part.Face(Part.Wire(Part.makeCircle(\
                    self.__powerCordNotchSize/2,\
                    origin.add(Base.Vector(0,a,self.__BatteryHeight+50.8)),\
                    Base.Vector(1,0,0))))\
                    .extrude(Base.Vector(self.__Width,0,0))
        notch = notch.fuse(Part.makePlane(\
                self.__powerCordNotchSize,\
                self.__powerCordNotchSize/2,\
                origin.add(Base.Vector(0,self.__Length,\
                    self.__BatteryHeight+50.8-(self.__powerCordNotchSize/2))),
                    Base.Vector(1,0,0))\
                 .extrude(Base.Vector(self.__Length,0,0)))
        self.right = self.right.cut(notch)
        self.left  = self.left.cut(notch)
        self.screenFlapSupport = Part.makePlane(\
                    self.__flapHeight,\
                    self.__flapWidth,\
                    origin.add(Base.Vector(\
                            0,\
                            self.__Adafruit35inTFTYOff+self.__flapWidth,\
                            self.__Adafruit35inTFTZOff+(2.4*25.4))),\
              Base.Vector(1,0,0)).extrude(Base.Vector(-self.__Thickness,0,0))
        self.screenFlapLockPlate = Part.makePlane(\
                    12.5,self.__flapWidth,\
                    origin.add(Base.Vector(\
                            -self.__Thickness,\
                            self.__Adafruit35inTFTYOff+self.__flapWidth,\
                            self.__Adafruit35inTFTZOff+(2.4*25.4)+self.__flapHeight-12.5)),\
               Base.Vector(1,0,0)).extrude(Base.Vector(-self.__Thickness,0,0))
        self.screenFlap = Part.makePlane(\
                        self.__flapHeight-12.5,self.__flapWidth,\
                        origin.add(Base.Vector(\
                            0,\
                            self.__Adafruit35inTFTYOff+self.__flapWidth,\
                            self.__Adafruit35inTFTZOff+(2.4*25.4)-(self.__flapHeight-12.5))),\
                Base.Vector(1,0,0)).extrude(Base.Vector(-self.__Thickness,0,0))
        self.b1 = HalfByHalf.XBeam(\
                origin.add(Base.Vector(\
                        self.__Thickness,\
                        self.__Length,\
                        self.__Height-12.5)),
                        self.__Width-(2*self.__Thickness))
        self.b2 = HalfByHalf.XBeam(\
                origin.add(Base.Vector(\
                        self.__Thickness,\
                        self.__Length,\
                        self.__BatteryHeight+12.5-self.__Thickness)),
                        self.__Width-(2*self.__Thickness))
        self.b3 = HalfByHalf.ZBeam(\
                origin.add(Base.Vector(self.__Thickness,self.__Length-12.5,a)),
                self.__Height-a-12.5)
        self.b4 = HalfByHalf.ZBeam(\
                origin.add(Base.Vector(self.__Width-self.__Thickness-12.5,\
                                       self.__Length-12.5,a)),
                self.__Height-a-12.5)
    def __bowlSupportPlateScrewHoles(self):
        holes = list()
        holes.append(self.origin.add(Base.Vector(\
                self.__Thickness+(self.__bowlBoxSupportThick/2),
                (-self.__BowlExtension)+25.4,\
                self.__BaseThick)))
        holes.append(self.origin.add(Base.Vector(\
                self.__Thickness+(self.__bowlBoxSupportThick/2),
                -(1.5*25.4),\
                self.__BaseThick)))
        holes.append(self.origin.add(Base.Vector(\
                self.__Width-(self.__Thickness+(self.__bowlBoxSupportThick/2)),\
                (-self.__BowlExtension)+25.4,\
                self.__BaseThick)))
        holes.append(self.origin.add(Base.Vector(\
                self.__Width-(self.__Thickness+(self.__bowlBoxSupportThick/2)),\
                -(1.5*25.4),\
                self.__BaseThick)))
        for h in holes:
            hole = Part.Face(Part.Wire(Part.makeCircle(\
                        self.__bowlSupportPlateScrewHoleDiameter/2,
                        h))).extrude(Base.Vector(0,0,self.__bowlBoxHeight))
            self.leftBowlBoxSupport = self.leftBowlBoxSupport.cut(hole)
            self.rightBowlBoxSupport = self.rightBowlBoxSupport.cut(hole)
            self.bowlSupportPlate = self.bowlSupportPlate.cut(hole)
    def show(self,doc=None):
        if doc==None:
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
        #obj.ViewObject.Transparency=50
        obj = doc.addObject("Part::Feature",self.name+"_right")
        obj.Shape = self.right
        obj.Label=self.name+"_right"
        obj.ViewObject.ShapeColor=self.__Color
        #obj.ViewObject.Transparency=50
        obj = doc.addObject("Part::Feature",self.name+"_back")
        obj.Shape = self.back
        obj.Label=self.name+"_back"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_base")
        obj.Shape = self.base
        obj.Label=self.name+"_base"
        obj.ViewObject.ShapeColor=self.__BaseColor
        #obj = doc.addObject("Part::Feature",self.name+"_b1")
        #obj.Shape = self.b1
        #obj.Label=self.name+"_b1"
        #obj.ViewObject.ShapeColor=self.__BaseColor
        #obj = doc.addObject("Part::Feature",self.name+"_b2")
        #obj.Shape = self.b2
        #obj.Label=self.name+"_b2"
        #obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_bTopStop")
        obj.Shape = self.bTopStop
        obj.Label=self.name+"_bTopStop"
        obj.ViewObject.ShapeColor=self.__Color
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
        self.agitatorMotor.show()
        self.agitatorMount.show()
        self.agitator.show()
        self.vl6180x.show()
        self.bowl.show()
        self.strainGuage.show()
        obj = doc.addObject("Part::Feature",self.name+"_paddle")
        obj.Shape = self.paddle
        obj.Label=self.name+"_paddle"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_leftBowlBoxSupport")
        obj.Shape = self.leftBowlBoxSupport
        obj.Label=self.name+"_leftBowlBoxSupport"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_rightBowlBoxSupport")
        obj.Shape = self.rightBowlBoxSupport
        obj.Label=self.name+"_rightBowlBoxSupport"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_frontBowlBoxSupport")
        obj.Shape = self.frontBowlBoxSupport
        obj.Label=self.name+"_frontBowlBoxSupport"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_bowlSupportPlate")
        obj.Shape = self.bowlSupportPlate
        obj.Label=self.name+"_bowlSupportPlate"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_b1")
        obj.Shape = self.b1
        obj.Label=self.name+"_b1"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_b2")
        obj.Shape = self.b2
        obj.Label=self.name+"_b2"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_b3")
        obj.Shape = self.b3
        obj.Label=self.name+"_b3"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_b4")
        obj.Shape = self.b4
        obj.Label=self.name+"_b4"
        obj.ViewObject.ShapeColor=self.__BaseColor
        obj = doc.addObject("Part::Feature",self.name+"_screenFlapSupport")
        obj.Shape = self.screenFlapSupport
        obj.Label=self.name+"_screenFlapSupport"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_screenFlapLockPlate")
        obj.Shape = self.screenFlapLockPlate
        obj.Label=self.name+"_screenFlapLockPlate"
        obj.ViewObject.ShapeColor=self.__Color
        obj = doc.addObject("Part::Feature",self.name+"_screenFlap")
        obj.Shape = self.screenFlap
        obj.Label=self.name+"_screenFlap"
        obj.ViewObject.ShapeColor=self.__Color
        self.augerMount.show(doc)
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
    Gui.activeDocument().activeView().viewLeft()
    Gui.SendMsgToActiveView("ViewFit")
    WoodBOM.ListCuts("Wood.bom")        
