#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Aug 18 11:37:13 2024
#  Last Modified : <250331.1546>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
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
import Mesh

import os
import sys
sys.path.append(os.path.dirname(__file__))

class DFRobotGearMotor(object):
    GearBoxHeight = 46
    GearBoxWidth  = 32
    GearBoxDepth  = 25.2-2.0
    GearBoxSpacers = 2.0
    MotorHeight   = 30.8
    MotorDiameter = 24.4
    MotorCenterXOff = 32-12.2
    MotorCenterYOff = 24.2-13.2
    ShaftDiameter = 6
    ShaftDFlat    = 5.4
    ShaftDFlatLength = 12
    ShaftClearHole = 6.5
    ShaftLength   = 18.5
    ShaftX        = 16
    ShaftZ        = 46-(6+9)
    @classmethod
    def ShaftY(cls):
        return cls.ShaftZ
    ShaftSpacerDia = 12 # Guess 
    MountingHoleX1 = (32-18)/2
    MountingHoleX2 = 32-((32-18)/2)
    MountingHoleZ1 = 7
    @classmethod
    def MountingHoleY1(cls):
        return cls.MountingHoleZ1
    MountingHoleZ2 = 46-6
    @classmethod
    def MountingHoleY2(cls):
        return cls.MountingHoleZ2
    MountingHoleDia = 3.6
    MountingHoleSpacerDia = 8 # Guess
    @classmethod
    def CutShaftZ(cls,origin,part,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        if not isinstance(part,Part.Shape):
            raise RuntimeError("part is not a Shape")
        shaft = Part.Face(Part.Wire(Part.makeCircle(cls.ShaftDiameter/2.0,origin,Base.Vector(0,0,1)))).extrude(Base.Vector(0,0,length))
        d = Part.makePlane(length,cls.ShaftDiameter,\
                           origin.add(Base.Vector(-cls.ShaftDiameter/2.0,\
                                                  cls.ShaftDFlat-(cls.ShaftDiameter/2),\
                                                  0)),\
                           Base.Vector(0,1,0)).extrude(Base.Vector(0,cls.ShaftDiameter-cls.ShaftDFlat,0))
        shaft = shaft.cut(d)
        return part.cut(shaft)
    @classmethod
    def OriginFromShaftHole(cls,shaftOrigin):
        if not isinstance(shaftOrigin,Base.Vector):
            raise RuntimeError("shaftOrigin is not a Vector")
        return shaftOrigin.add(Base.Vector(-cls.ShaftX,\
                                           -(cls.GearBoxDepth+cls.GearBoxSpacers),\
                                           -(cls.ShaftZ+cls.MotorHeight)))
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.motor = Part.Face(Part.Wire(Part.makeCircle(self.MotorDiameter/2.0,\
                                         origin.add(Base.Vector(self.MotorCenterXOff,\
                                                                self.MotorCenterYOff,\
                                                                0)),\
                                         Base.Vector(0,0,1))))\
                            .extrude(Base.Vector(0,0,self.MotorHeight))
        gearboxOrigin = origin.add(Base.Vector(0,0,self.MotorHeight))
        self.gearbox = Part.makePlane(self.GearBoxWidth,self.GearBoxDepth,\
                                      gearboxOrigin)\
                           .extrude(Base.Vector(0,0,self.GearBoxHeight))
        self.MountingHoles = list()
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX1,\
                                                                0,\
                                                                self.MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX2,\
                                                                0,\
                                                                self.MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX1,\
                                                                0,\
                                                                self.MountingHoleZ2)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX2,\
                                                                0,\
                                                                self.MountingHoleZ2)))
        for i in range(0,4):
            hspace = Part.Face(Part.Wire(Part.makeCircle(self.MountingHoleSpacerDia/2.0,\
                                                         self.MountingHoles[i],\
                                                         Base.Vector(0,1,0))))\
                        .extrude(Base.Vector(0,-self.GearBoxSpacers,0))
            self.gearbox = self.gearbox.fuse(hspace)
        self.shaftOrigin = gearboxOrigin.add(Base.Vector(self.ShaftX,0,self.ShaftZ))
        self.shaft = Part.Face(Part.Wire(Part.makeCircle(self.ShaftDiameter/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.ShaftLength))
        d = Part.makePlane(self.ShaftDiameter,self.ShaftDFlatLength,\
                           self.shaftOrigin.add(Base.Vector(-self.ShaftDiameter/2,\
                         -self.ShaftLength,\
                                                self.ShaftDFlat-(self.ShaftDiameter/2))))\
                       .extrude(Base.Vector(0,0,self.ShaftDiameter-self.ShaftDFlat))
        #self.d = d
        self.shaft = self.shaft.cut(d)
        sspace = Part.Face(Part.Wire(Part.makeCircle(self.ShaftSpacerDia/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.GearBoxSpacers))
        self.gearbox = self.gearbox.fuse(sspace)
    def MountingHole(self,i,Y,YDelta):
        xhole = self.MountingHoles[i]
        HoleOrigin = Base.Vector(xhole.x,Y,xhole.z)
        hole = Part.Face(Part.Wire(Part.makeCircle(self.MountingHoleDia/2,HoleOrigin,Base.Vector(0,1,0))))\
                    .extrude(Base.Vector(0,YDelta,0))
        return hole
    def ShaftHole(self,Y,YDelta):
        HoleOrigin = Base.Vector(self.shaftOrigin.x,Y,self.shaftOrigin.z)
        hole = Part.Face(Part.Wire(Part.makeCircle(self.ShaftClearHole/2,HoleOrigin,Base.Vector(0,1,0))))\
                    .extrude(Base.Vector(0,YDelta,0))
        return hole
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_motor')
        obj.Shape = self.motor
        obj.Label=self.name+'_motor'
        obj.ViewObject.ShapeColor=tuple([0.5,0.5,0.5])
        obj = doc.addObject("Part::Feature",self.name+'_gearbox')
        obj.Shape = self.gearbox
        obj.Label=self.name+'_gearbox'
        obj.ViewObject.ShapeColor=tuple([0.5,0.5,0.5])
        obj = doc.addObject("Part::Feature",self.name+'_shaft')
        obj.Shape = self.shaft
        obj.Label=self.name+'_shaft'
        obj.ViewObject.ShapeColor=tuple([0.8,0.8,0.8])
        #obj = doc.addObject("Part::Feature",self.name+'_d')
        #obj.Shape = self.d
        #obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])

class DFRobotGearMotor_UpsideDown(DFRobotGearMotor):
    MountingHoleZ1 = 6
    MountingHoleZ2 = 46-7
    ShaftZ        =  6+9
    MotorCenterYOff = 13.2
    MotorCenterXOff = 12.2
    @classmethod
    def OriginFromShaftHole(cls,shaftOrigin):
        if not isinstance(shaftOrigin,Base.Vector):
            raise RuntimeError("shaftOrigin is not a Vector")
        return shaftOrigin.add(Base.Vector(-cls.ShaftX,\
                                           -(cls.GearBoxDepth+cls.GearBoxSpacers),\
                                           -cls.ShaftZ))
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        gearboxOrigin = origin.add(Base.Vector(0,self.GearBoxSpacers,0))
        self.gearbox = Part.makePlane(self.GearBoxWidth,self.GearBoxDepth,\
                                      gearboxOrigin)\
                           .extrude(Base.Vector(0,0,self.GearBoxHeight))
        self.MountingHoles = list()
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX1,\
                                                                0,\
                                                                self.MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX2,\
                                                                0,\
                                                                self.MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX1,\
                                                                0,\
                                                                self.MountingHoleZ2)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.MountingHoleX2,\
                                                                0,\
                                                                self.MountingHoleZ2)))
        for i in range(0,4):
            hspace = Part.Face(Part.Wire(Part.makeCircle(self.MountingHoleSpacerDia/2.0,\
                                                         self.MountingHoles[i],\
                                                         Base.Vector(0,1,0))))\
                        .extrude(Base.Vector(0,-self.GearBoxSpacers,0))
            self.gearbox = self.gearbox.fuse(hspace)
        self.shaftOrigin = gearboxOrigin.add(Base.Vector(self.ShaftX,0,self.ShaftZ))
        self.shaft = Part.Face(Part.Wire(Part.makeCircle(self.ShaftDiameter/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.ShaftLength))
        d = Part.makePlane(self.ShaftDiameter,self.ShaftDFlatLength,\
                           self.shaftOrigin.add(Base.Vector(-self.ShaftDiameter/2,\
                         -self.ShaftLength,\
                                                self.ShaftDFlat-(self.ShaftDiameter/2))))\
                       .extrude(Base.Vector(0,0,self.ShaftDiameter-self.ShaftDFlat))
        #self.d = d
        self.shaft = self.shaft.cut(d)
        sspace = Part.Face(Part.Wire(Part.makeCircle(self.ShaftSpacerDia/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.GearBoxSpacers))
        self.gearbox = self.gearbox.fuse(sspace)
        self.motor = Part.Face(Part.Wire(Part.makeCircle(self.MotorDiameter/2.0,\
                                         origin.add(Base.Vector(self.MotorCenterXOff,\
                                                                self.MotorCenterYOff,\
                                                                self.GearBoxHeight)),\
                                         Base.Vector(0,0,1))))\
                            .extrude(Base.Vector(0,0,self.MotorHeight))
                

class MotorDrivePlate(object):
    __PlateDiameter = 39
    PlateThick    = .125*25.4
    __HubDiameter   = 10
    HubLength     = 12+3+2
    __HubScrewDia   = 3.6
    __HubScrewHeadDepth = 3
    __HubScrewHeadDia = 5.5
    __HubShaftDepth = 12
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        plate = Part.Face(Part.Wire(Part.makeCircle(self.__PlateDiameter/2.0,\
                                                    origin.add(Base.Vector(0,0,self.HubLength-self.PlateThick))))).extrude(Base.Vector(0,0,self.PlateThick))
        hub = Part.Face(Part.Wire(Part.makeCircle(self.__HubDiameter/2.0,\
                                                    origin)))\
                             .extrude(Base.Vector(0,0,self.HubLength))
        plate = plate.fuse(hub)
        #print(type(plate),file=sys.__stderr__)
        plate = DFRobotGearMotor.CutShaftZ(origin,plate,self.__HubShaftDepth)
        screwhole = Part.Face(Part.Wire(Part.makeCircle(self.__HubScrewDia/2,\
                                                        origin)))\
                             .extrude(Base.Vector(0,0,self.HubLength))
        plate = plate.cut(screwhole)
        screwhead = Part.Face(Part.Wire(Part.makeCircle(self.__HubScrewHeadDia/2,\
                                                        origin.add(Base.Vector(0,0,self.HubLength-self.__HubScrewHeadDepth)))))\
                             .extrude(Base.Vector(0,0,self.__HubScrewHeadDepth))
        self.plate = plate.cut(screwhead)
        #self.screwhead = screwhead
        
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.plate
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        #obj = doc.addObject("Part::Feature",self.name+"_head")
        #obj.Shape = self.screwhead
        #obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
    def MakeSTL(self,filename):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature","temp")
        obj.Shape=self.plate
        objs = list()
        objs.append(obj)
        Mesh.export(objs,filename)
        doc.removeObject(obj.Label)

class MotorDrivePlate_Y(object):
    __PlateDiameter = 39
    PlateThick    = .125*25.4
    __HubDiameter   = 10
    HubLength     = 12+3+2
    __HubScrewDia   = 3.6
    __HubScrewHeadDepth = 3
    __HubScrewHeadDia = 5.5
    __HubShaftDepth = 12
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        plate = Part.Face(Part.Wire(Part.makeCircle(self.__PlateDiameter/2.0,\
                                                    origin.add(Base.Vector(0,-(self.HubLength-self.PlateThick),0)),Base.Vector(0,1,0)))).extrude(Base.Vector(0,-self.PlateThick,0))
        hub = Part.Face(Part.Wire(Part.makeCircle(self.__HubDiameter/2.0,\
                                                    origin,Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,-self.HubLength,0))
        plate = plate.fuse(hub)
        #print(type(plate),file=sys.__stderr__)
        #plate = DFRobotGearMotor.CutShaftY(origin,plate,self.__HubShaftDepth)
        screwhole = Part.Face(Part.Wire(Part.makeCircle(self.__HubScrewDia/2,\
                                                        origin,Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,-self.HubLength,0))
        plate = plate.cut(screwhole)
        screwhead = Part.Face(Part.Wire(Part.makeCircle(self.__HubScrewHeadDia/2,\
                                                        origin.add(Base.Vector(0,-(self.HubLength-self.__HubScrewHeadDepth),0)),Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,-self.__HubScrewHeadDepth,0))
        self.plate = plate.cut(screwhead)
        #self.screwhead = screwhead
        
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.plate
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        #obj = doc.addObject("Part::Feature",self.name+"_head")
        #obj.Shape = self.screwhead
        #obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])

import math

def radians(degrees):
    return (degrees/180)*math.pi

class AugerMountPlate(MotorDrivePlate):
    __MountHoleRadius = (16.5+11.5)/2
    __SmallPeg    = 1
    __LargeHole    = 3.3/2
    __PegLength   = 6
    __StartAngle  = 30
    __DeltaAngle  = 90
    def __init__(self,name,origin):
        super().__init__(name,origin)
        peg1X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle))
        peg1Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle))
        peg2X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg2Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg3X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg3Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg4X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        peg4Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        #smallPegOrig = self.origin.add(Base.Vector(peg1X,peg1Y,self.HubLength))
        #smallPeg = Part.Face(Part.Wire(Part.makeCircle(self.__SmallPeg,smallPegOrig,Base.Vector(0,0,1)))).extrude(Base.Vector(0,0,self.__PegLength))
        #self.plate = self.plate.fuse(smallPeg)
        screwHoleOrig = self.origin.add(Base.Vector(peg2X,peg2Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg3X,peg3Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg4X,peg4Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        
class AgitatorMountPlate(MotorDrivePlate):
    __MountHoleRadius = (16.5+11.5)/2
    __LargeHole    = 3.3/2
    __LargeHoleClear = 4.4/2
    __StartAngle  = 30
    __DeltaAngle  = 90
    @classmethod
    def MountYHoleRing(cls,part,origin,thick):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        if not isinstance(part,Part.Shape):
            raise RuntimeError("part is not a Shape")
        for i in range(0,4):
            dang = cls.__DeltaAngle*i
            hX = cls.__MountHoleRadius * math.cos(radians(cls.__StartAngle+\
                                                            dang))
            hZ = cls.__MountHoleRadius * math.sin(radians(cls.__StartAngle+\
                                                            dang))
            holeOorigin = origin.add(Base.Vector(hX,0,hZ))
            hole = Part.Face(Part.Wire(Part.makeCircle(cls.__LargeHoleClear,\
                                                       holeOorigin,\
                                                       Base.Vector(0,1,0))))\
                            .extrude(Base.Vector(0,thick,0))
            part = part.cut(hole)
        return part
    def __init__(self,name,origin):
        super().__init__(name,origin)
        peg1X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle))
        peg1Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle))
        peg2X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg2Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg3X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg3Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg4X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        peg4Y = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        screwHoleOrig = self.origin.add(Base.Vector(peg1X,peg1Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig,Base.Vector(0,0,1)))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg2X,peg2Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg3X,peg3Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg4X,peg4Y,self.HubLength-self.PlateThick))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig))).extrude(Base.Vector(0,0,self.PlateThick))
        self.plate = self.plate.cut(screwHole)

class AgitatorMountPlate_Y(MotorDrivePlate_Y):
    __MountHoleRadius = (16.5+11.5)/2
    __LargeHole    = 3.3/2
    __LargeHoleClear = 4.4/2
    __StartAngle  = 30
    __DeltaAngle  = 90
    def __init__(self,name,origin):
        super().__init__(name,origin)
        peg1X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle))
        peg1Z = self.__MountHoleRadius * math.sin(radians(self.__StartAngle))
        peg2X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg2Z = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      self.__DeltaAngle))
        peg3X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg3Z = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*2)))
        peg4X = self.__MountHoleRadius * math.cos(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        peg4Z = self.__MountHoleRadius * math.sin(radians(self.__StartAngle+\
                                                      (self.__DeltaAngle*3)))
        screwHoleOrig = self.origin.add(Base.Vector(peg1X,-(self.HubLength-self.PlateThick),peg1Z))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig,Base.Vector(0,1,0)))).extrude(Base.Vector(0,-self.PlateThick,0))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg2X,-(self.HubLength-self.PlateThick),peg2Z))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig,Base.Vector(0,1,0)))).extrude(Base.Vector(0,-self.PlateThick,0))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg3X,-(self.HubLength-self.PlateThick),peg3Z))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig,Base.Vector(0,1,0)))).extrude(Base.Vector(0,-self.PlateThick,0))
        self.plate = self.plate.cut(screwHole)
        screwHoleOrig = self.origin.add(Base.Vector(peg4X,-(self.HubLength-self.PlateThick),peg4Z))
        screwHole = Part.Face(Part.Wire(Part.makeCircle(self.__LargeHole,screwHoleOrig,Base.Vector(0,1,0)))).extrude(Base.Vector(0,-self.PlateThick,0))
        self.plate = self.plate.cut(screwHole)
        

class GearMotorMount(object):
    __PipeDiameter = 48
    __PipeHeight   = 14.5
    __PipeInner    = 41
    __FlangeHeight = 8
    @classmethod
    def FlangeHeight(cls):
        return cls.__FlangeHeight
    @classmethod
    def TotalHeight(cls):
        return cls.__PipeHeight+cls.__FlangeHeight
    __FlangeDiameter = 57.78
    __ScrewHeadDepth = 3
    __ScrewHeadDia = 5.5
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        flange = Part.Face(Part.Wire(Part.makeCircle(self.__FlangeDiameter/2.0,\
                                                     origin)))\
                                      .extrude(Base.Vector(0,0,self.__FlangeHeight))
        pipe = Part.Face(Part.Wire(Part.makeCircle(self.__PipeDiameter/2.0,\
                                                   origin.add(Base.Vector(0,0,self.__FlangeHeight)))))\
                                      .extrude(Base.Vector(0,0,self.__PipeHeight))
        part = flange.fuse(pipe)
        mountFaceOrigin = origin.add(Base.Vector(-DFRobotGearMotor.ShaftX,\
                                                 -(DFRobotGearMotor.GearBoxHeight-DFRobotGearMotor.ShaftY()),0))
        mountFace = Part.makePlane(DFRobotGearMotor.GearBoxWidth,\
                                   DFRobotGearMotor.GearBoxHeight,\
                                   mountFaceOrigin)\
                           .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.fuse(mountFace)
        pipeInner = Part.Face(Part.Wire(Part.makeCircle(self.__PipeInner/2.0,\
                                                origin.add(Base.Vector(0,0,\
                                                self.__FlangeHeight)))))\
                                       .extrude(Base.Vector(0,0,self.__PipeHeight))
        part = part.cut(pipeInner)
        shaftSpacer = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.ShaftSpacerDia/2,\
                                                          origin)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(shaftSpacer)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX1,\
                                              DFRobotGearMotor.GearBoxHeight-DFRobotGearMotor.MountingHoleY1(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mhO.add(Base.Vector(0,0,self.__FlangeHeight-self.__ScrewHeadDepth))
        head = Part.Face(Part.Wire(Part.makeCircle(self.__ScrewHeadDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight+self.__PipeHeight))
        part = part.cut(head)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX1,\
                                              DFRobotGearMotor.GearBoxHeight-DFRobotGearMotor.MountingHoleY2(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mhO.add(Base.Vector(0,0,self.__FlangeHeight-self.__ScrewHeadDepth))
        head = Part.Face(Part.Wire(Part.makeCircle(self.__ScrewHeadDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight+self.__PipeHeight))
        part = part.cut(head)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX2,\
                                              DFRobotGearMotor.GearBoxHeight-DFRobotGearMotor.MountingHoleY1(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mhO.add(Base.Vector(0,0,self.__FlangeHeight-self.__ScrewHeadDepth))
        head = Part.Face(Part.Wire(Part.makeCircle(self.__ScrewHeadDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight+self.__PipeHeight))
        part = part.cut(head)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX2,\
                                              DFRobotGearMotor.GearBoxHeight-DFRobotGearMotor.MountingHoleY2(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mhO.add(Base.Vector(0,0,self.__FlangeHeight-self.__ScrewHeadDepth))
        head = Part.Face(Part.Wire(Part.makeCircle(self.__ScrewHeadDia/2,mhO)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight+self.__PipeHeight))
        part = part.cut(head)
        self.part = part
    def rotate(self,base,dir,angle):
        self.part.rotate(base,dir,angle)
    def translate(self,neworigin):
        self.part.translate(neworigin)
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.part
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.5,0.5,0.5])
    def MakeSTL(self,filename):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature","temp")
        obj.Shape=self.part
        objs = list()
        objs.append(obj)
        Mesh.export(objs,filename)
        doc.removeObject(obj.Label)
    
if __name__ == '__main__':
    if "Motor" in App.listDocuments().keys():
        App.closeDocument("Motor")
    doc = App.newDocument("Motor")
    mount = GearMotorMount("mount",Base.Vector(0,0,0))
    mount.show(doc)
    mount.MakeSTL("GearMotorMount.stl")
    agitatorMount = AgitatorMountPlate("agitatorMount",Base.Vector(200,0,0))
    agitatorMount.show(doc)
    agitatorMount.MakeSTL("AgitatorMountPlate.stl")
    augerMount = AugerMountPlate("augerMount",Base.Vector(400,0,0))
    augerMount.show(doc)
    augerMount.MakeSTL("AugerMountPlate.stl")    
    Gui.activeDocument().activeView().viewTop()
    Gui.SendMsgToActiveView("ViewFit")
