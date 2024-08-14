#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Aug 13 18:16:55 2024
#  Last Modified : <240814.1603>
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

class AdafruitTFTFeatherWing(object):
    __BoardOutlineYZInches = [(0,0),(.2,0),(.2,.2),(3.36-.2,.2),(3.36-.2,0),\
                              (3.36,0),(3.36,2.6),(3.36-.2,2.6),\
                              (3.36-.2,2.6-.2),(.2,2.6-.2),(.2,2.6),(0,2.6),\
                              (0,0)]
    __BoardWidthInches = 3.36
    __BoardThick = 1.6
    __BoardMountingHolesYZInches = [(.1,.1),(3.26,.1),(3.26,2.5),(.1,2.5)]
    __BoardMountingHolesRad = .06*25.4
    __LongHeaderYZ = (39.7,40.386)
    __LongHeaderWH = (40.64,8.128)
    __ShortHeaderYZ = (39.7,17.526)
    __ShortHeaderWH = (30.48,8.128)
    __HeaderHeight = 7.37
    __ScreenOriginYZInches = (0,.2)
    __ScreenSizeWHInches   = (3.36,2.2)
    __ScreenThick = 3.3
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        boardPoints = list()
        for Yin,Zin in self.__BoardOutlineYZInches:
            boardPoints.append(origin.add(Base.Vector(0,Yin*25.4,Zin*25.4)))
        self.board = Part.Face(Part.makePolygon(boardPoints))\
                        .extrude(Base.Vector(self.__BoardThick,0,0))
        self.MountingHoles = list()
        for Yin,Zin in self.__BoardMountingHolesYZInches:
            self.MountingHoles.append(origin.add(Base.Vector(0,Yin*25.4,Zin*25.4)))
        #self.holes = list()
        for i in range(0,4):
            h = self.MakeMountingHole(i,origin.x,self.__BoardThick)
            #self.holes.append(h)
            self.board = self.board.cut(h)
        screenWin,screenHin = self.__ScreenSizeWHInches
        screenYin,screenZin = self.__ScreenOriginYZInches
        self.screen = Part.makePlane(screenHin*25.4,screenWin*25.4,\
                                     origin.add(Base.Vector(0,screenWin*25.4+screenYin*25.4,screenZin*25.4)),\
                                     Base.Vector(1,0,0)).extrude(Base.Vector(-self.__ScreenThick,0,0))
        Y,Z = self.__LongHeaderYZ
        W,H = self.__LongHeaderWH
        self.longHeader =  Part.makePlane(H,W,\
                                          origin.add(Base.Vector(self.__BoardThick,Y+W,Z)),\
                                          Base.Vector(1,0,0))\
                               .extrude(Base.Vector(self.__HeaderHeight))
        Y,Z = self.__ShortHeaderYZ
        W,H = self.__ShortHeaderWH
        self.shortHeader =  Part.makePlane(H,W,\
                                          origin.add(Base.Vector(self.__BoardThick,Y+W,Z)),\
                                          Base.Vector(1,0,0))\
                               .extrude(Base.Vector(self.__HeaderHeight))
    def MakeMountingHole(self,index,X,Xdelta):
        holeOrig = Base.Vector(X,self.MountingHoles[index].y,self.MountingHoles[index].z)
        hole = Part.Face(Part.Wire(Part.makeCircle(self.__BoardMountingHolesRad,\
                                                   holeOrig,\
                                                   Base.Vector(1,0,0))))\
                    .extrude(Base.Vector(Xdelta,0,0))
        return hole
    def ScreenCutout(self,DeltaX):
        screenWin,screenHin = self.__ScreenSizeWHInches
        screenYin,screenZin = self.__ScreenOriginYZInches
        screenCutout = Part.makePlane(screenHin*25.4,screenWin*25.4,\
                                     self.origin.add(Base.Vector(0,screenWin*25.4+screenYin*25.4,screenZin*25.4)),\
                                     Base.Vector(1,0,0)).extrude(Base.Vector(DeltaX,0,0))
        return screenCutout
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_board')
        obj.Shape = self.board
        obj.Label=self.name+'_board'
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        #for h in self.holes:
        #    obj = doc.addObject("Part::Feature",self.name+'_hole')
        #    obj.Shape = h
        #    obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+'_screen')
        obj.Shape = self.screen
        obj.Label=self.name+'_screen'
        obj.ViewObject.ShapeColor=tuple([0.8,0.8,0.8])
        obj = doc.addObject("Part::Feature",self.name+'_longHeader')
        obj.Shape = self.longHeader
        obj.Label=self.name+'_longHeader'
        obj.ViewObject.ShapeColor=tuple([0.2,0.2,0.2])
        obj = doc.addObject("Part::Feature",self.name+'_shortHeader')
        obj.Shape = self.shortHeader
        obj.Label=self.name+'_shortHeader'
        obj.ViewObject.ShapeColor=tuple([0.2,0.2,0.2])
        


if __name__ == '__main__':
    if "Display" in App.listDocuments().keys():
        App.closeDocument("Display")
    doc = App.newDocument("Display")
    display = AdafruitTFTFeatherWing("Display",Base.Vector(0,0,0))
    display.show(doc)
    Gui.activeDocument().activeView().viewRight()
    Gui.SendMsgToActiveView("ViewFit")
    
