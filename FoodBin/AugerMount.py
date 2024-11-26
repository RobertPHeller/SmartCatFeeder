#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Sep 13 11:52:17 2021
#  Last Modified : <241126.1621>
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
import Part, Mesh
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))


class AugerMount(object):
    _MainHoleDiameter = 44.787449
    _MountingHoleDiameter = 6.033542
    _MHoleX1 = -31.011
    _MHoleX2 =  30.29
    _MHoleY1 = -30.31
    _MHoleY2 =  34.54
    @classmethod
    def CutHoles(cls,panel,origin,thickness):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        extrude = Base.Vector(0,0,thickness)
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MainHoleDiameter/2,origin)))\
                    .extrude(extrude))
        mh1 = origin.add(Base.Vector(cls._MHoleX1,cls._MHoleY1,0))
        #sys.__stderr__.write("*** AugerMount.CutHoles(): mh1 is (%f,%f,%f)\n"%(mh1.x,mh1.y,mh1.z))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,mh1)))\
                    .extrude(extrude))
        mh2 = origin.add(Base.Vector(cls._MHoleX2,cls._MHoleY1,0))
        #sys.__stderr__.write("*** AugerMount.CutHoles(): mh2 is (%f,%f,%f)\n"%(mh2.x,mh2.y,mh2.z))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,mh2)))\
                    .extrude(extrude))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,\
                                origin.add(Base.Vector(cls._MHoleX1,\
                                                       cls._MHoleY2,0)))))\
                    .extrude(extrude))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,\
                                origin.add(Base.Vector(cls._MHoleX2,\
                                                       cls._MHoleY2,0)))))\
                    .extrude(extrude))
        return panel
    def __init__(self,name,origin):                            
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        mount = Mesh.read(os.path.join(os.path.dirname(__file__),\
                                       "../Auger_Drive_Screw_Conveyor/AugerMount.stl"))
        mount.translate(-302,2,-8)
        mount.rotate(0,3.14159,0)
        mount.translate(self.origin.x,self.origin.y,self.origin.z)
        self.mount = mount
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Mesh::Feature",self.name)
        obj.Mesh = self.mount
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])

class bottom(object):
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.bottom = Part.makePlane(100,100,origin.add(Base.Vector(-50,-50,0)))\
                .extrude(Base.Vector(0,0,10))
        self.bottom = AugerMount.CutHoles(self.bottom,origin,10)
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape = self.bottom
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([.5,.5,0.0])



if __name__ == '__main__':
    if "AugerMount" in App.listDocuments().keys():
        App.closeDocument("AugerMount")
    doc = App.newDocument("AugerMount")
    doc = App.activeDocument()
    AugerMount = AugerMount("AugerMount",Base.Vector(0,0,0))
    AugerMount.show()
    bottom = bottom("bottom",Base.Vector(0,0,0))
    bottom.show() 
    Gui.activeDocument().activeView().viewBottom()
    Gui.SendMsgToActiveView("ViewFit")
    
