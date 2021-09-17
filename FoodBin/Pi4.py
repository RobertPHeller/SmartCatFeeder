#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Sep 16 16:09:40 2021
#  Last Modified : <210917.0801>
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

class USB(object):
    _Width = 14.754606786829118
    _Height = 16
    _Length = 17.88500654516162
    _Color  = tuple([211.0/255.0,211.0/255.0,211.0/255.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        # orientation: NegY
        Norm=Base.Vector(0,-1,0)
        self.usb = Part.makePlane(self._Width,self._Length,origin,Norm)\
                .extrude(Base.Vector(0,-self._Height,0))
    def cutout(self,xBase,xDepth):
        o = Base.Vector(xBase,self.origin.y,self.origin.z-self._Width)
        return Part.makePlane(self._Width,self._Height,o,Base.Vector(1,0,0))\
                .extrude(Base.Vector(xDepth,0,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.usb
        obj.Label=self.name
        obj.ViewObject.ShapeColor=self._Color
        
            

class Eth(object):
    _Width = 15.498137146309533
    _Height = 13.5
    _Length = 21.62601953479005
    _Color  = tuple([211.0/255.0,211.0/255.0,211.0/255.0])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        # orientation: NegY
        Norm=Base.Vector(0,-1,0)
        self.eth = Part.makePlane(self._Width,self._Length,origin,Norm)\
                .extrude(Base.Vector(0,-self._Height,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.eth
        obj.Label=self.name
        obj.ViewObject.ShapeColor=self._Color
    def cutout(self,xBase,xDepth):
        o = Base.Vector(xBase,self.origin.y,self.origin.z-self._Width)
        return Part.makePlane(self._Width,self._Height,o,Base.Vector(1,0,0))\
                .extrude(Base.Vector(xDepth,0,0))

class Pi4(object):
    _Width = 56
    _Length = 85
    _Thick = 1.2
    _USB1_CenterOffset = 9
    _USB2_CenterOffset = 27
    _Eth_CenterOffset = 45.75
    _USB_Eth_XOff = 3.15617762561676
    _Color = tuple([0.0,1.0,0.0])
    _mhy1 = 3.5
    _mhy2 = 56-3.5
    _mhx2 = 85-3.5
    _mhx1 = (85-3.5)-58
    _mhdia = 2.7
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        # orientation: NegY
        self.initMholes()
        Norm=Base.Vector(0,-1,0)
        self.board = Part.makePlane(self._Width,self._Length,origin,Norm)\
                    .extrude(Base.Vector(0,-self._Thick,0))
        self.board = self.board.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,\
                                                self.mhvector[1],Norm)))\
                    .extrude(Base.Vector(0,-self._Thick,0)))
        self.board = self.board.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,\
                                                self.mhvector[2],Norm)))\
                    .extrude(Base.Vector(0,-self._Thick,0)))
        self.board = self.board.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,\
                                                self.mhvector[3],Norm)))\
                    .extrude(Base.Vector(0,-self._Thick,0)))
        self.board = self.board.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,\
                                                self.mhvector[4],Norm)))\
                    .extrude(Base.Vector(0,-self._Thick,0)))
        self.usb1 = USB(self.name+"_usb1",origin.add(Base.Vector(\
                         -self._USB_Eth_XOff,\
                         -self._Thick,\
                         -(self._USB1_CenterOffset-(USB._Width/2.0)))))
        self.usb2 = USB(self.name+"_usb2",origin.add(Base.Vector(\
                         -self._USB_Eth_XOff,\
                         -self._Thick,\
                         -(self._USB2_CenterOffset-(USB._Width/2.0)))))
        self.eth = Eth(self.name+"_eth",origin.add(Base.Vector(\
                         -self._USB_Eth_XOff,\
                         -self._Thick,\
                         -(self._Eth_CenterOffset-(Eth._Width/2.0)))))
    def initMholes(self):
        self.mhvector = {
            1 : self.origin.add(Base.Vector(self._mhx1,0,-self._mhy1)),
            2 : self.origin.add(Base.Vector(self._mhx2,0,-self._mhy1)),
            3 : self.origin.add(Base.Vector(self._mhx1,0,-self._mhy2)),
            4 : self.origin.add(Base.Vector(self._mhx2,0,-self._mhy2))
        }
    def MountingHole(self,i,yBase,height):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,yBase,mhv.z)
        return Part.Face(Part.Wire(Part.makeCircle(self._mhdia/2.0,mhz,\
                                                   Base.Vector(0,-1,0))))\
                           .extrude(Base.Vector(0,-height,0))
    def Standoff(self,i,yBase,diameter,height):
        mhv = self.mhvector[i]
        mhz = Base.Vector(mhv.x,yBase,mhv.z)
        return Part.Face(Part.Wire(Part.makeCircle(diameter/2.0,mhz,\
                                                   Base.Vector(0,-1,0))))\
                           .extrude(Base.Vector(0,-height,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_board")
        obj.Shape = self.board
        obj.Label=self.name+"_board"
        obj.ViewObject.ShapeColor=self._Color
        self.usb1.show()
        self.usb2.show()
        self.eth.show()
    def usb1Cutout(self,xBase,xDepth):
        return self.usb1.cutout(xBase,xDepth)
    def usb2Cutout(self,xBase,xDepth):
        return self.usb2.cutout(xBase,xDepth)
    def ethCutout(self,xBase,xDepth):
        return self.eth.cutout(xBase,xDepth)
        


if __name__ == '__main__':
    if "Pi4" in App.listDocuments().keys():
        App.closeDocument("Pi4")
    doc = App.newDocument("Pi4")
    doc = App.activeDocument()
    pi4 = Pi4("pi4",Base.Vector(0,0,0))
    pi4.show()
    Gui.activeDocument().activeView().viewFront()
    Gui.SendMsgToActiveView("ViewFit")
