#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Aug 12 09:45:28 2024
#  Last Modified : <240812.1459>
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
import Part
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))

from abc import ABCMeta, abstractmethod, abstractproperty

class RaspberryPiTouchDisplay(object):
    __OuterWidth = 192.96
    @classmethod
    def OuterWidth(cls):
        return cls.__OuterWidth
    __OuterHeight = 110.76
    @classmethod
    def OuterHeight(cls):
        return cls.__OuterHeight
    __BezelThick = 1
    __InnerWidth = 166.2
    __InnerHeight = 100.6
    __TopOffset = 6.63
    __RightOffset = 11.89
    __BaseThick = 5.96
    __ScrewMountRelief = 2.5
    __ScrewMountWidth = 6
    __ScrewMountHeight = 12
    __BaseScrewRightOff = 12.54+20.0
    __BaseScrewTopOff   = 21.58
    __BaseScrewWSpace   = 126.2
    __BaseScrewHSpace   = 65.65
    __BaseScrewHoleRad  = 3.5/2.0
    __PiScrewRightOff   = 12.54+48.45
    __PiScrewTopOff     = 6.63+20.8
    __PiScrewWSpace     = 58.0
    __PiScrewHSpace     = 49.0
    __PiScrewHoleRad    = 3.0/2.0
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.bezel = Part.makePlane(self.__OuterHeight,self.__OuterWidth,\
                                    origin,Base.Vector(0,1,0))\
                    .extrude(Base.Vector(0,self.__BezelThick,0))
        bottomOff = self.__OuterHeight-(self.__InnerHeight+self.__TopOffset)
        leftOff = self.__OuterWidth-(self.__InnerWidth+self.__RightOffset)
        bodyOrigin=origin.add(Base.Vector(leftOff,0,bottomOff))
        self.body = Part.makePlane(self.__InnerHeight,self.__InnerWidth,\
                                    bodyOrigin,Base.Vector(0,1,0))\
                     .extrude(Base.Vector(0,self.__BaseThick,0))
        self.BaseMountingHoles = list()
        baseMount_ll = Base.Vector(self.__OuterWidth-self.__BaseScrewRightOff,\
                                   self.__BaseThick,\
                                   self.__OuterHeight-self.__BaseScrewTopOff)
        self.BaseMountingHoles.append(baseMount_ll)
        baseMount_lr = baseMount_ll.add(Base.Vector(-self.__BaseScrewWSpace,0,0))
        self.BaseMountingHoles.append(baseMount_lr)
        baseMount_ur = baseMount_lr.add(Base.Vector(0,0,-self.__BaseScrewHSpace))
        self.BaseMountingHoles.append(baseMount_ur)
        baseMount_ul = baseMount_ll.add(Base.Vector(0,0,-self.__BaseScrewHSpace))
        self.BaseMountingHoles.append(baseMount_ul)
        self.__ScrewMountAt(origin.add(baseMount_ll),self.__ScrewMountHeight,\
                            self.__ScrewMountWidth)
        self.__ScrewMountAt(origin.add(baseMount_lr),self.__ScrewMountHeight,\
                            self.__ScrewMountWidth)
        self.__ScrewMountAt(origin.add(baseMount_ul),self.__ScrewMountHeight,\
                            self.__ScrewMountWidth)
        self.__ScrewMountAt(origin.add(baseMount_ur),self.__ScrewMountHeight,\
                            self.__ScrewMountWidth)
        self.PiMountingHoles = list()
        piMount_ll = Base.Vector(self.__OuterWidth-self.__PiScrewRightOff,\
                                 self.__BaseThick,\
                                 self.__OuterHeight-self.__PiScrewTopOff)
        self.PiMountingHoles.append(piMount_ll)
        piMount_lr = piMount_ll.add(Base.Vector(-self.__PiScrewWSpace,0,0))
        self.PiMountingHoles.append(piMount_lr)
        piMount_ur = piMount_lr.add(Base.Vector(0,0,-self.__PiScrewHSpace))
        self.PiMountingHoles.append(piMount_ur)
        piMount_ul = piMount_ll.add(Base.Vector(0,0,-self.__PiScrewHSpace))
        self.PiMountingHoles.append(piMount_ul)
        self.__ScrewMountAt(origin.add(piMount_ll),self.__ScrewMountWidth,\
                            self.__ScrewMountHeight)
        self.__ScrewMountAt(origin.add(piMount_lr),self.__ScrewMountWidth,\
                            self.__ScrewMountHeight)
        self.__ScrewMountAt(origin.add(piMount_ul),self.__ScrewMountWidth,\
                            self.__ScrewMountHeight)
        self.__ScrewMountAt(origin.add(piMount_ur),self.__ScrewMountWidth,\
                            self.__ScrewMountHeight)
    def __ScrewMountAt(self,at,w,h):
        relief = Part.makePlane(h,w,at.add(Base.Vector(-w/2,0,-h/2)),\
                                Base.Vector(0,1,0))\
                     .extrude(Base.Vector(0,self.__ScrewMountRelief,0))
        self.body = self.body.fuse(relief)
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_bezel')
        obj.Shape = self.bezel
        obj.Label=self.name+'_bezel'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_body')
        obj.Shape = self.body
        obj.Label=self.name+'_body'
        obj.ViewObject.ShapeColor=tuple([0.8,0.8,0.8])


if __name__ == '__main__':
    if "Display" in App.listDocuments().keys():
        App.closeDocument("Display")
    doc = App.newDocument("Display")
    display = RaspberryPiTouchDisplay("Display",Base.Vector(0,0,0))
    display.show(doc)
    Gui.activeDocument().activeView().viewRear()
    Gui.SendMsgToActiveView("ViewFit")
