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
#  Last Modified : <210913.1250>
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


class AugerMount(object):
    _MainHoleDiameter = 44.787449
    _MountingHoleDiameter = 6.033542
    _MHoleX = 32.488306
    _MHoleY1 = -27.963135
    _MHoleY2 =  32.836395
    @classmethod
    def CutHoles(cls,panel,origin,thickness):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        extrude = Base.Vector(0,0,thickness)
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MainHoleDiameter/2,origin)))\
                    .extrude(extrude))
        mh1 = origin.add(Base.Vector(-cls._MHoleX,cls._MHoleY1,0))
        sys.__stderr__.write("*** AugerMount.CutHoles(): mh1 is (%f,%f,%f)\n"%(mh1.x,mh1.y,mh1.z))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,mh1)))\
                    .extrude(extrude))
        mh2 = origin.add(Base.Vector(cls._MHoleX,cls._MHoleY1,0))
        sys.__stderr__.write("*** AugerMount.CutHoles(): mh2 is (%f,%f,%f)\n"%(mh2.x,mh2.y,mh2.z))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,mh2)))\
                    .extrude(extrude))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,\
                                origin.add(Base.Vector(-cls._MHoleX,\
                                                       cls._MHoleY2,0)))))\
                    .extrude(extrude))
        panel = panel.cut(Part.Face(Part.Wire(\
                Part.makeCircle(cls._MountingHoleDiameter/2,\
                                origin.add(Base.Vector(cls._MHoleX,\
                                                       cls._MHoleY2,0)))))\
                    .extrude(extrude))
        return panel
                            
                      
        
        
