#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Sep 19 19:32:50 2021
#  Last Modified : <210920.1316>
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

import BudHB

class ChargerPS(object):
    # Base board
    _Length = 111.76
    _Width  = 71.12
    _Thick  = 1.2
    _Color  = tuple([0.0,1.0,0.0])
    # Mounting Holes
    _MHoleDiameter = 4.5
    _MHoleXOff0 = 5.08
    _MHoleXOff1 = 5.08+60.96
    _MHoleYOff0 = 17.78
    _MHoleYOff1 = 17.78+88.9
    # Battery connector
    _BatteryConnXOff   = 10.414
    _BatteryConnWidth  =  9.906
    #
    _PowerConnXOff     = 38.354
    _PowerConnWidth    = 21.59
    # Both Connectors
    _ConnYOff   = -9.906
    _ConnHeight = 10.01
    _ConnLength = 11.43+3.3
    _ConnColor  = tuple([1.0,1.0,1.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.__initMHoles()
        YNorm=Base.Vector(0,1,0)
        YThick=Base.Vector(0,self._Thick,0)
        self.board = Part.makePlane(self._Length,self._Width,self.origin,\
                                    YNorm).extrude(YThick)
        for i in range(1,5):
            self.board = self.board.cut(Part.Face(\
                            Part.Wire(Part.makeCircle(self._MHoleDiameter/2.0,\
                                                      self.mhvector[i],\
                                                      YNorm))).extrude(YThick))
        self.__battOrigin = self.origin.add(Base.Vector(self._BatteryConnXOff,\
                                                        self._Thick,\
                                                        self._ConnYOff))
        self.batteryConn = Part.makePlane(self._ConnLength,\
                                          self._BatteryConnWidth,\
                                          self.__battOrigin,\
                                          YNorm)\
                                   .extrude(Base.Vector(0,self._ConnHeight,0))
        self.__powerOrigin = self.origin.add(Base.Vector(self._PowerConnXOff,\
                                                        self._Thick,\
                                                        self._ConnYOff))
        self.powerConn = Part.makePlane(self._ConnLength,\
                                          self._PowerConnWidth,\
                                          self.__powerOrigin,\
                                          YNorm)\
                                   .extrude(Base.Vector(0,self._ConnHeight,0))
    def __initMHoles(self):
        self.mhvector = {
            1 : self.origin.add(Base.Vector(self._MHoleXOff0,0,self._MHoleYOff0)),
            2 : self.origin.add(Base.Vector(self._MHoleXOff1,0,self._MHoleYOff0)),
            3 : self.origin.add(Base.Vector(self._MHoleXOff0,0,self._MHoleYOff1)),
            4 : self.origin.add(Base.Vector(self._MHoleXOff1,0,self._MHoleYOff1))
        }
    def ConnectorCutouts(self,box):
        extrude = Base.Vector(0,0,self._ConnLength)
        box.cutout(Part.makePlane(self._BatteryConnWidth,self._ConnHeight,\
                                     self.__battOrigin).extrude(extrude))
        box.cutout(Part.makePlane(self._PowerConnWidth,self._ConnHeight,\
                                     self.__powerOrigin).extrude(extrude))
        return box
    def MountingHole(self,i,yBase,height):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,yBase,mhv.z)
        return Part.Face(Part.Wire(Part.makeCircle(self._MHoleDiameter/2.0,\
                                                   mhz,\
                                                   Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,height,0))
    def Standoff(self,i,yBase,diameter,height):
        mhv = self.mhvector[i] 
        mhz = Base.Vector(mhv.x,yBase,mhv.z)
        return Part.Face(Part.Wire(Part.makeCircle(diameter/2.0,mhz,\
                                                   Base.Vector(0,1,0))))\
                           .extrude(Base.Vector(0,height,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_board')
        obj.Shape = self.board
        obj.Label=self.name+'_board'
        obj.ViewObject.ShapeColor=self._Color
        obj = doc.addObject("Part::Feature",self.name+'_batteryConn')
        obj.Shape = self.batteryConn
        obj.Label=self.name+'_batteryConn'
        obj.ViewObject.ShapeColor=self._ConnColor
        obj = doc.addObject("Part::Feature",self.name+'_powerConn')
        obj.Shape = self.powerConn
        obj.Label=self.name+'_powerConn'
        obj.ViewObject.ShapeColor=self._ConnColor
        
class ChargerPSBox(object):
    _StandoffHeight = 6
    _StandoffDiameter = 8
    _StandoffColor = tuple([1.0,1.0,0.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.box = BudHB.AC_402(self.name+"_box",self.origin)
        self.board = ChargerPS(self.name+"_board",self.origin.add(Base.Vector(\
                (.5*25.4+self.box.GUAGE()),\
                self._StandoffHeight+self.box.GUAGE(),\
                self.box.GUAGE())))
        self.board.ConnectorCutouts(self.box)
        self.standoffs = dict()
        for i in range(1,5):
            self.box.cutout(self.board.MountingHole(i,self.origin.y,\
                                                    self.box.GUAGE()))
            self.standoffs[i] = self.board.Standoff(i,\
                                            self.origin.y+self.box.GUAGE(),\
                                            self._StandoffDiameter,\
                                            self._StandoffHeight)
    def show(self):
        self.box.show()
        self.board.show()
        doc = App.activeDocument()
        for i in range(1,5):
            obj = doc.addObject("Part::Feature",self.name+("_standoff%d"%(i)))
            obj.Shape = self.standoffs[i]
            obj.Label=self.name+("_standoff%d"%(i))
            obj.ViewObject.ShapeColor=self._StandoffColor

if __name__ == '__main__':
    if "ChargerPSBox" in App.listDocuments().keys():
        App.closeDocument("ChargerPSBox")
    doc = App.newDocument("ChargerPSBox")
    doc = App.activeDocument()
    chargerBox = ChargerPSBox("chargerBox",Base.Vector(0,0,0))
    chargerBox.show()
    Gui.activeDocument().activeView().viewRear()
    Gui.SendMsgToActiveView("ViewFit")
