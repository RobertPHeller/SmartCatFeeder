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
#  Last Modified : <240901.1244>
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
import Part, TechDraw, TechDrawGui
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))
import time
import datetime
from PySide.QtCore import QCoreApplication, QEventLoop, QTimer

def execute(loop, ms):
    timer = QTimer()
    timer.setSingleShot(True)
    
    timer.timeout.connect(loop.quit)
    timer.start(ms)
    loop.exec_()

def sleep(ms):
    if not QCoreApplication.instance():
        app = QCoreApplication([])
        execute(app, ms)
    else:
        loop = QEventLoop()
        execute(loop, ms)


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
    
from abc import ABCMeta, abstractmethod, abstractproperty
    
class HM187_7D(object):
    __metaclass__ = ABCMeta
    def A():
        pass
    @staticmethod
    def B():
        pass
    @staticmethod
    def C():
        pass
    @staticmethod
    def D():
        pass
    @staticmethod
    def E():
        pass
    _backFract = 0.17142857142857143
    _frameFract = 0.4857142857142857
    _frontFract = 0.34285714285714286
    _MHoleDiameter = (3.0/16.0)*25.4
    _TermWidth = .187*25.4
    _TermInsulationWidth = .25*25.4
    _TermLength = .250*25.4
    _TermThick  = (1.0/16.0)*25.4
    _termColor = tuple([.75,.75,.75])
    _insulationColor = tuple([0.0,0.0,0.0])
    _frameLengthOff = (6.0/16.0)*25.4
    _frameBobbinOff = .125*25.4
    _frameColor = tuple([.5,.5,.5])
    _bobbinColor = tuple([165.0/255.0,42.0/255.0,42.0/255.0])
    def _buildtransformer(self):
        YNorm=Base.Vector(0,1,0)
        self.__frameDepth = self._frameFract*self.B()
        self.__backDepth   = self._backFract*self.B()
        bobbinZOff            = self.E()-self.B()
        self.__frontDepth  = bobbinZOff+self._frontFract*self.B()
        
        self.__initMHvector()
        self.frame = Part.makePlane(self.__frameDepth,self.A(),\
                                     self.origin.add(Base.Vector(0,0,\
                                                          self.__frontDepth)),\
                                     YNorm).extrude(Base.Vector(0,1,0))
        frameBodyLength = self.A()-(self._frameLengthOff*2)
        #sys.__stderr__.write("*** HM187_7D._buildtransformer(): self.A() = %f,self._frameLengthOff = %f, frameBodyLength = %f\n"%(self.A(),self._frameLengthOff,frameBodyLength))
        self.frame = self.frame.fuse(\
            Part.makePlane(self.__frameDepth,frameBodyLength,\
                           self.origin.add(Base.Vector(self._frameLengthOff,\
                                                       1,\
                                                       self.__frontDepth)),\
                           YNorm).extrude(Base.Vector(0,\
                                                      self._frameBobbinOff,\
                                                      0)))
        C_Remainder = self.C()-(1+self._frameBobbinOff)
        self.frame = self.frame.fuse(\
            Part.makePlane(self.__frameDepth,self._frameBobbinOff,
                           self.origin.add(Base.Vector(self._frameLengthOff,\
                                                      1+self._frameBobbinOff,\
                                                      self.__frontDepth)),\
                           YNorm).extrude(Base.Vector(0,C_Remainder,0)))
        flangv2 = self._frameLengthOff+frameBodyLength-self._frameBobbinOff
        self.frame = self.frame.fuse(\
            Part.makePlane(self.__frameDepth,self._frameBobbinOff,
                           self.origin.add(Base.Vector(flangv2,\
                                                       1+self._frameBobbinOff,\
                                                       self.__frontDepth)),\
                           YNorm).extrude(Base.Vector(0,C_Remainder,0)))
        frametop = self.C()-self._frameBobbinOff
        self.frame = self.frame.fuse(\
            Part.makePlane(self.__frameDepth,frameBodyLength,\
                           self.origin.add(Base.Vector(self._frameLengthOff,\
                                                       frametop,\
                                                       self.__frontDepth)),\
                           YNorm).extrude(Base.Vector(0,\
                                                      self._frameBobbinOff,\
                                                      0)))
        self.frame = self.frame.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._MHoleDiameter/2.0,\
                                self._mhvector[1],YNorm))).extrude(Base.Vector(0,1,0)))     
        self.frame = self.frame.cut(\
            Part.Face(Part.Wire(Part.makeCircle(self._MHoleDiameter/2.0,\
                                self._mhvector[2],YNorm))).extrude(Base.Vector(0,1,0)))
        bobbinLength = frameBodyLength-(2*self._frameBobbinOff)
        bobbonWidth  = self.B() 
        self.__bobbinHeight = C_Remainder-self._frameBobbinOff
        self.__bobbinXOff   = self._frameLengthOff+self._frameBobbinOff
        self.bobbin = Part.makePlane(bobbonWidth,bobbinLength,\
                                     self.origin.add(Base.Vector(self.__bobbinXOff,\
                                                     1+self._frameBobbinOff,\
                                                     bobbinZOff)),\
                                     YNorm).extrude(Base.Vector(0,\
                                                                self.__bobbinHeight,\
                                                                0))
        self.terms = dict()
        self.__terminal(2)
        self.__terminal(4)
        self.__terminal(6)
        self.__terminal(8)
        self.__terminal(10)
    def __terminal(self,number):
        YNorm=Base.Vector(0,1,0)
        if number < 6:
            YOff = 1+self._frameBobbinOff
        else:
            YOff = self.C()-(1+self._frameBobbinOff+self._TermThick)
        xnum = (number-1)%5
        XOff = ((self.B()/4)*xnum)+(self._TermWidth/2.0)+self.__bobbinXOff
        insulationLength = (self.E()-self.B())-self._TermLength
        term = Part.makePlane(self._TermLength,self._TermWidth,\
                              self.origin.add(Base.Vector(XOff,YOff,0)),\
                              YNorm).extrude(Base.Vector(0,self._TermThick,0))
        insX = XOff - ((self._TermInsulationWidth-self._TermWidth)/2.0)
        insulation = Part.makePlane(insulationLength,\
                                    self._TermInsulationWidth,\
                                    self.origin.add(Base.Vector(insX,YOff,\
                                                           self._TermLength)),\
                                    YNorm).extrude(Base.Vector(0,self._TermThick,0))
        self.terms[number] = (term,insulation)
    def __initMHvector(self):
        xoff0 = (self.A()-self.D())/2.0
        xoff1 = xoff0+self.D()
        zoff  = self.__frontDepth + (self.__frameDepth/2.0) 
        self._mhvector = {
            1 : self.origin.add(Base.Vector(xoff0,0,zoff)),
            2 : self.origin.add(Base.Vector(xoff1,0,zoff))
        }
    def MountingHole(self,i,yBase,height):
        mhv = self._mhvector[i]
        mhz = Base.Vector(mhv.x,yBase,mhv.z)
        return Part.Face(Part.Wire(Part.makeCircle(self._MHoleDiameter/2.0,\
                                                   mhz,\
                                                   Base.Vector(0,1,0))))\
                             .extrude(Base.Vector(0,height,0))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+'_frame')
        obj.Shape = self.frame
        obj.Label=self.name+'_frame'
        obj.ViewObject.ShapeColor=self._frameColor
        obj = doc.addObject("Part::Feature",self.name+'_bobbin')
        obj.Shape = self.bobbin
        obj.Label=self.name+'_bobbin'
        obj.ViewObject.ShapeColor=self._bobbinColor
        for i in self.terms:
            term, insulation = self.terms[i]
            istring = "%d"%(i)
            obj = doc.addObject("Part::Feature",self.name+'_terminalLug'+istring)
            obj.Shape = term
            obj.Label=self.name+'_terminalLug'+istring
            obj.ViewObject.ShapeColor=self._termColor
            obj = doc.addObject("Part::Feature",self.name+'_terminalIns'+istring)
            obj.Shape = insulation
            obj.Label=self.name+'_terminalIns'+istring
            obj.ViewObject.ShapeColor=self._insulationColor
        
class HM187E16(HM187_7D):
    @staticmethod
    def A():
        return 3.25*25.4
    @staticmethod
    def B():
        return 1.68*25.4
    @staticmethod
    def C():
        return 1.93*25.4
    @staticmethod
    def D():
        return 2.81*25.4
    @staticmethod
    def E():
        return 2.055*25.4
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self._buildtransformer()

class ACPowerInlet(object):
    _OuterWidth     = 33
    _InnerWidth     = 31
    _OuterHeight    = 30
    _InnerHeight    = 27
    _OuterDepth     =  5
    _InnerDepth     = 15.7
    _TerminalDepth  = 10
    _TerminalWidth  = 25
    _TerminalHeight = 20
    _BodyColor      = tuple([0.0,0.0,0.0])
    _TerminalColor  = tuple([.85,.85,.85])
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector")
        self.origin = origin
        self.body = Part.makePlane(self._OuterWidth,\
                                   self._OuterHeight,\
                                   self.origin)\
                                  .extrude(Base.Vector(0,0,-self._OuterDepth))
        self.innerOrigin = self.origin.add(Base.Vector(\
                        (self._OuterWidth-self._InnerWidth)/2.0,\
                        (self._OuterHeight-self._InnerHeight)/2.0,\
                        0))
        self.body = self.body.fuse(\
                Part.makePlane(self._InnerWidth,self._InnerHeight,\
                               self.innerOrigin)\
                            .extrude(Base.Vector(0,0,self._InnerDepth)))
        terminalOrigin = self.origin.add(Base.Vector(\
                            (self._OuterWidth-self._TerminalWidth)/2.0,\
                            (self._OuterHeight-self._TerminalHeight)/2.0,\
                            self._InnerDepth))
        self.terminals = Part.makePlane(self._TerminalWidth,\
                                        self._TerminalHeight,\
                                        terminalOrigin)\
                                    .extrude(Base.Vector(0,\
                                                         0,\
                                                         self._TerminalDepth))
    def Cutout(self,thickness):
        return Part.makePlane(self._InnerWidth,self._InnerHeight,\
                              self.innerOrigin)\
                             .extrude(Base.Vector(0,0,thickness))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_body")
        obj.Shape = self.body
        obj.Label=self.name+"_body"
        obj.ViewObject.ShapeColor=self._BodyColor
        obj = doc.addObject("Part::Feature",self.name+"_terminals")
        obj.Shape = self.terminals
        obj.Label=self.name+"_terminals"
        obj.ViewObject.ShapeColor=self._TerminalColor

class ChargerPSBox(object):
    _StandoffHeight = 6
    _StandoffDiameter = 8
    _StandoffColor = tuple([1.0,1.0,0.0])
    _inletXOff = 4.5*25.4
    _inletYOff = 1+(ACPowerInlet._OuterHeight/2.0)
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
        self.transformer = HM187E16(self.name+"_transformer",\
                        origin.add(Base.Vector(\
                                   .5*25.4+self.box.GUAGE()+self.board._Width,\
                                   self.box.GUAGE(),\
                                   (self.box.B()*.55)-HM187E16.E()/2.0)))
        for i in range(1,3):
            self.box.cutout(self.transformer.MountingHole(i,self.origin.y,\
                                                          self.box.GUAGE()))
        self.inlet = ACPowerInlet(self.name+"_acinlet",\
                                  self.origin.add(Base.Vector(self._inletXOff,\
                                                              self._inletYOff,\
                                                              0)))
        self.box.cutout(self.inlet.Cutout(self.box.GUAGE()))
    def show(self):
        self.box.show()
        self.board.show()
        self.transformer.show()
        self.inlet.show()
        doc = App.activeDocument()
        for i in range(1,5):
            obj = doc.addObject("Part::Feature",self.name+("_standoff%d"%(i)))
            obj.Shape = self.standoffs[i]
            obj.Label=self.name+("_standoff%d"%(i))
            obj.ViewObject.ShapeColor=self._StandoffColor





if __name__ == '__main__':
    doc = None
    for docname in App.listDocuments():
        lddoc = App.getDocument(docname)
        if lddoc.Label == 'FoodBin':
            doc = lddoc
            break
    if doc == None:
        App.open("FoodBin.FCStd")
        doc = App.getDocument('FoodBin')
    App.ActiveDocument=doc
    # Clean out old garbage, if any
    for g in doc.findObjects('TechDraw::DrawSVGTemplate'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawPage'):
        doc.removeObject(g.Name)
    for g in doc.findObjects('TechDraw::DrawViewPart'):
        doc.removeObject(g.Name)
    # insert a Page object and assign a template
    template = doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
    template.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
    edt = template.EditableTexts
    edt['CompanyName'] = "Deepwoods Software"
    edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA' 
    edt['DrawingTitle1']= 'Smart Cat Feeder'
    edt['DrawingTitle2']= 'Charger and Power Supply'
    edt['DrawnBy'] = "Robert Heller"
    edt['CheckedBy'] = ""
    edt['Approved1'] = ""
    edt['Approved2'] = ""
    edt['Code'] = ""
    edt['Weight'] = ''
    edt['DrawingNumber'] = datetime.datetime.now().ctime()
    edt['Revision'] = "A"
    template.EditableTexts = edt
    page1 = doc.addObject('TechDraw::DrawPage','ChargerPSBoxPage1')
    page1.Template = doc.USLetterTemplate
    edt = page1.Template.EditableTexts
    edt['DrawingTitle3']= "Box Bottom Drill"
    edt['Scale'] = '1'
    edt['Sheet'] = "Sheet 1 of 2"
    page1.Template.EditableTexts = edt
    page1.ViewObject.show()
    boxbottom = doc.addObject('TechDraw::DrawViewPart','BoxBottomView')
    page1.addView(boxbottom)
    boxbottom.Source = doc.foodbin_chargerPSox_box_ACBox
    boxbottom.X = 130
    boxbottom.Y = 130
    boxbottom.Scale = 1
    boxbottom.Direction=(0.0,-1.0,0.0)
    boxbottom.Caption = "Bottom"
    #
    doc.recompute()
    sleep(500)
    TechDrawGui.exportPageAsPdf(page1,"BoxBottomDrill.pdf")
    #
    page2 = doc.addObject('TechDraw::DrawPage','ChargerPSBoxPage2')
    page2.Template = doc.USLetterTemplate
    edt = page2.Template.EditableTexts
    edt['DrawingTitle3']= "Box side Drill"
    edt['Scale'] = '1'
    edt['Sheet'] = "Sheet 2 of 2"
    page2.Template.EditableTexts = edt
    page2.ViewObject.show()
    boxside = doc.addObject('TechDraw::DrawViewPart','BoxSideView')
    page2.addView(boxside)
    boxside.Source = doc.foodbin_chargerPSox_box_ACBox
    boxside.X = 140
    boxside.Y = 140
    boxside.Scale = 1
    boxside.Rotation=180
    boxside.Direction=(0.0,0.0,-1.0)
    boxside.Caption = "Side"
    #
    doc.recompute()
    sleep(500)
    TechDrawGui.exportPageAsPdf(page2,"BoxSideDrill.pdf")
    
