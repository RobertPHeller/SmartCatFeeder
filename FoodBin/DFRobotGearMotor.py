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
#  Last Modified : <240818.2217>
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

import os
import sys
sys.path.append(os.path.dirname(__file__))

class DFRobotGearMotor(object):
    __GearBoxHeight = 46
    @classmethod
    def GearBoxHeight(cls):
        return cls.__GearBoxHeight
    __GearBoxWidth  = 32
    @classmethod
    def GearBoxWidth(cls):
        return cls.__GearBoxWidth
    __GearBoxDepth  = 25.2-2.0
    __GearBoxSpacers = 2.0
    __MotorHeight   = 30.8
    __MotorDiameter = 24.4
    __MotorCenterXOff = 32-12.2
    __MotorCenterYOff = 24.2-13.2
    __ShaftDiameter = 6
    __ShaftDFlat    = 5.4
    __ShaftDFlatLength = 12
    __ShaftClearHole = 6.5
    __ShaftLength   = 18.5
    __ShaftX        = 16
    @classmethod
    def ShaftX(cls):
        return cls.__ShaftX
    __ShaftZ        = 46-(6+9)
    @classmethod
    def ShaftY(cls):
        return cls.__ShaftZ
    __ShaftSpacerDia = 12 # Guess 
    @classmethod
    def ShaftSpacerDia(cls):
        return cls.__ShaftSpacerDia
    __MountingHoleX1 = (32-18)/2
    @classmethod
    def MountingHoleX1(cls):
        return cls.__MountingHoleX1
    __MountingHoleX2 = 32-((32-18)/2)
    @classmethod
    def MountingHoleX2(cls):
        return cls.__MountingHoleX2
    __MountingHoleZ1 = 7
    @classmethod
    def MountingHoleY1(cls):
        return cls.__MountingHoleZ1
    __MountingHoleZ2 = 46-6
    @classmethod
    def MountingHoleY2(cls):
        return cls.__MountingHoleZ2
    __MountingHoleDia = 3.6
    @classmethod
    def MountingHoleDia(cls):
        return cls.__MountingHoleDia
    __MountingHoleSpacerDia = 8 # Guess
    @classmethod
    def CutShaftZ(cls,origin,part,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        if not isinstance(part,Part.Shape):
            raise RuntimeError("part is not a Shape")
        shaft = Part.Face(Part.Wire(Part.makeCircle(cls.__ShaftDiameter/2.0,origin,Base.Vector(0,0,1)))).extrude(Base.Vector(0,0,length))
        d = Part.makePlane(length,cls.__ShaftDiameter,\
                           origin.add(Base.Vector(-cls.__ShaftDiameter/2.0,\
                                                  cls.__ShaftDFlat-(cls.__ShaftDiameter/2),\
                                                  0)),\
                           Base.Vector(0,1,0)).extrude(Base.Vector(0,cls.__ShaftDiameter-cls.__ShaftDFlat,0))
        shaft = shaft.cut(d)
        return part.cut(shaft)
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.motor = Part.Face(Part.Wire(Part.makeCircle(self.__MotorDiameter/2.0,\
                                         origin.add(Base.Vector(self.__MotorCenterXOff,\
                                                                self.__MotorCenterYOff,\
                                                                0)),\
                                         Base.Vector(0,0,1))))\
                            .extrude(Base.Vector(0,0,self.__MotorHeight))
        gearboxOrigin = origin.add(Base.Vector(0,0,self.__MotorHeight))
        self.gearbox = Part.makePlane(self.__GearBoxWidth,self.__GearBoxDepth,\
                                      gearboxOrigin)\
                           .extrude(Base.Vector(0,0,self.__GearBoxHeight))
        self.MountingHoles = list()
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.__MountingHoleX1,\
                                                                0,\
                                                                self.__MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.__MountingHoleX2,\
                                                                0,\
                                                                self.__MountingHoleZ1)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.__MountingHoleX1,\
                                                                0,\
                                                                self.__MountingHoleZ2)))
        self.MountingHoles.append(gearboxOrigin.add(Base.Vector(self.__MountingHoleX2,\
                                                                0,\
                                                                self.__MountingHoleZ2)))
        for i in range(0,4):
            hspace = Part.Face(Part.Wire(Part.makeCircle(self.__MountingHoleSpacerDia/2.0,\
                                                         self.MountingHoles[i],\
                                                         Base.Vector(0,1,0))))\
                        .extrude(Base.Vector(0,-self.__GearBoxSpacers,0))
            self.gearbox = self.gearbox.fuse(hspace)
        self.shaftOrigin = gearboxOrigin.add(Base.Vector(self.__ShaftX,0,self.__ShaftZ))
        self.shaft = Part.Face(Part.Wire(Part.makeCircle(self.__ShaftDiameter/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.__ShaftLength))
        d = Part.makePlane(self.__ShaftDiameter,self.__ShaftDFlatLength,\
                           self.shaftOrigin.add(Base.Vector(-self.__ShaftDiameter/2,\
                         -self.__ShaftLength,\
                                                self.__ShaftDFlat-(self.__ShaftDiameter/2))))\
                       .extrude(Base.Vector(0,0,self.__ShaftDiameter-self.__ShaftDFlat))
        #self.d = d
        self.shaft = self.shaft.cut(d)
        sspace = Part.Face(Part.Wire(Part.makeCircle(self.__ShaftSpacerDia/2.0,\
                                                         self.shaftOrigin,\
                                                         Base.Vector(0,1,0))))\
                         .extrude(Base.Vector(0,-self.__GearBoxSpacers))
        self.gearbox = self.gearbox.fuse(sspace)
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
        smallPegOrig = self.origin.add(Base.Vector(peg1X,peg1Y,self.HubLength))
        smallPeg = Part.Face(Part.Wire(Part.makeCircle(self.__SmallPeg,smallPegOrig,Base.Vector(0,0,1)))).extrude(Base.Vector(0,0,self.__PegLength))
        self.plate = self.plate.fuse(smallPeg)
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
    __LargeHole    = 2.5
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
        

class GearMotorMount(object):
    __PipeDiameter = 48
    __PipeHeight   = 14.5
    __PipeInner    = 41
    __FlangeHeight = 8
    __FlangeDiameter = 57.78
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
        mountFaceOrigin = origin.add(Base.Vector(-DFRobotGearMotor.ShaftX(),\
                                                 -(DFRobotGearMotor.GearBoxHeight()-DFRobotGearMotor.ShaftY()),0))
        mountFace = Part.makePlane(DFRobotGearMotor.GearBoxWidth(),\
                                   DFRobotGearMotor.GearBoxHeight(),\
                                   mountFaceOrigin)\
                           .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.fuse(mountFace)
        pipeInner = Part.Face(Part.Wire(Part.makeCircle(self.__PipeInner/2.0,\
                                                origin.add(Base.Vector(0,0,\
                                                self.__FlangeHeight)))))\
                                       .extrude(Base.Vector(0,0,self.__PipeHeight))
        part = part.cut(pipeInner)
        shaftSpacer = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.ShaftSpacerDia()/2,\
                                                          origin)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(shaftSpacer)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX1(),\
                                              DFRobotGearMotor.MountingHoleY1(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia()/2)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX1(),\
                                              DFRobotGearMotor.MountingHoleY2(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia()/2)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX2(),\
                                              DFRobotGearMotor.MountingHoleY1(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia()/2)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        mhO = mountFaceOrigin.add(Base.Vector(DFRobotGearMotor.MountingHoleX2(),\
                                              DFRobotGearMotor.MountingHoleY2(),\
                                              0))
        mh = Part.Face(Part.Wire(Part.makeCircle(DFRobotGearMotor.MountingHoleDia()/2)))\
                                        .extrude(Base.Vector(0,0,self.__FlangeHeight))
        part = part.cut(mh)
        self.part = part
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
        obj.Shape=self.plate
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
    Gui.activeDocument().activeView().viewTop()
    Gui.SendMsgToActiveView("ViewFit")
