#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Aug 20 15:19:24 2024
#  Last Modified : <241103.0839>
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
import Part, TechDraw, TechDrawGui
from FreeCAD import Base

import os
import sys
sys.path.append(os.path.dirname(__file__))
import time
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


import FoodBin

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
    doc.addObject('TechDraw::DrawSVGTemplate','SmallCutPanelTemplate')
    doc.SmallCutPanelTemplate.Template = "smallcutpanel.svg"
    doc.addObject('TechDraw::DrawPage','SmallCutPanelPage_1')
    doc.SmallCutPanelPage_1.Template = doc.SmallCutPanelTemplate
    doc.SmallCutPanelPage_1.ViewObject.show()
    doc.addObject('TechDraw::DrawPage','SmallCutPanelPage_2')
    doc.SmallCutPanelPage_2.Template = doc.SmallCutPanelTemplate
    doc.SmallCutPanelPage_2.ViewObject.show()
    doc.addObject('TechDraw::DrawPage','SmallCutPanelPage_3')
    doc.SmallCutPanelPage_3.Template = doc.SmallCutPanelTemplate
    doc.SmallCutPanelPage_3.ViewObject.show()
                                                
    # Panels (1/8" hardwood laser cut plywood):
    #   foodbin_bottom -- sheet 2
    #   foodbin_front -- sheet 2
    #   foodbin_left -- sheet 1
    #   foodbin_right -- sheet 1
    #   foodbin_back -- sheet 2
    #   foodbin_batteryBack -- sheet 3
    #   foodbin_batteryTop -- sheet 2
    #   foodbin_top -- sheet 2
    #   foodbin_bTopStop -- sheet 3
    #   foodbin_agitator_disk1 -- sheet 1
    #   foodbin_agitator_disk2 -- sheet 1
    #   foodbin_agitator_disk3 -- sheet 1
    #   foodbin_agitator_disk4 -- sheet 1
    #   foodbin_paddle -- sheet 3
    #   foodbin_bowlSupportPlate -- sheet 3
    #   foodbin_screenFlapSupport -- sheet 3
    #   foodbin_screenFlapLockPlate -- sheet 3
    
    sideWidth = FoodBin.FoodBin.Length()
    sideHeight = FoodBin.FoodBin.Height()
    side_centerX = sideHeight/2.0
    side_centerY = sideWidth/2.0
    
    leftSide = doc.foodbin_left
    left_side = doc.addObject('TechDraw::DrawViewPart','Left_Side')
    doc.SmallCutPanelPage_1.addView(left_side)
    left_side.Source = leftSide
    left_side.X = 6.35+side_centerX
    left_side.Y = 6.35+side_centerY
    left_side.Rotation = 90.0
    left_side.Direction = (-1.0,0.0,0.0)
    rightSide = doc.foodbin_right
    right_side = doc.addObject('TechDraw::DrawViewPart','Right_side')
    doc.SmallCutPanelPage_1.addView(right_side)
    right_side.Source = rightSide
    right_side.X = 6.35+side_centerX
    right_side.Y = 6.35+sideWidth+6.35+side_centerY
    right_side.Rotation = 90.0
    right_side.Direction = (1.0,0.0,0.0)
    agitatorDisk1 = doc.foodbin_agitator_disk1
    agitator_disk1 = doc.addObject('TechDraw::DrawViewPart','Agitator_Disk1')
    doc.SmallCutPanelPage_1.addView(agitator_disk1)
    agitator_disk1.Source = agitatorDisk1
    agitator_disk1.X = 6.35+sideHeight+6.35+1.5*25.4
    agitator_disk1.Y = 6.35+sideWidth+side_centerY+50.8
    agitator_disk1.Rotation = 90.0
    agitator_disk1.Direction = (0.0,1.0,0)
    agitatorDisk2 = doc.foodbin_agitator_disk2
    agitator_disk2 = doc.addObject('TechDraw::DrawViewPart','Agitator_Disk2')
    doc.SmallCutPanelPage_1.addView(agitator_disk2)
    agitator_disk2.Source = agitatorDisk2
    agitator_disk2.X = 6.35+sideHeight+6.35+1.5*25.4
    agitator_disk2.Y = 6.35+sideWidth+side_centerY-25.4
    agitator_disk2.Rotation = 90.0
    agitator_disk2.Direction = (0.0,1.0,0)
    agitatorDisk3 = doc.foodbin_agitator_disk3
    agitator_disk3 = doc.addObject('TechDraw::DrawViewPart','Agitator_Disk3')
    doc.SmallCutPanelPage_1.addView(agitator_disk3)
    agitator_disk3.Source = agitatorDisk3
    agitator_disk3.X = 6.35+sideHeight+6.35+1.5*25.4
    agitator_disk3.Y = 6.35+sideWidth+side_centerY-2*50.8
    agitator_disk3.Rotation = 90.0
    agitator_disk3.Direction = (0.0,1.0,0)
    agitatorDisk4 = doc.foodbin_agitator_disk4
    agitator_disk4 = doc.addObject('TechDraw::DrawViewPart','Agitator_Disk4')
    doc.SmallCutPanelPage_1.addView(agitator_disk4)
    agitator_disk4.Source = agitatorDisk4
    agitator_disk4.X = 6.35+sideHeight+6.35+1.5*25.4
    agitator_disk4.Y = 6.35+sideWidth+.75*side_centerY-3*50.8-25.4
    agitator_disk4.Rotation = 90.0
    agitator_disk4.Direction = (0.0,1.0,0)

    front = doc.foodbin_front
    front_ = doc.addObject('TechDraw::DrawViewPart','Front')
    doc.SmallCutPanelPage_2.addView(front_)
    front_.Source = front
    front_.X = 6.35+side_centerX-75
    front_.Y = 6.35+side_centerY
    front_.Rotation = 90.0
    front_.Direction = (0.0,-1.0,0.0)
    back  = doc.foodbin_back
    back_ = doc.addObject('TechDraw::DrawViewPart','Back')
    doc.SmallCutPanelPage_2.addView(back_)
    back_.Source = back
    back_.X = 6.35+side_centerX
    back_.Y = 6.35+side_centerY+6.35+sideWidth
    back_.Rotation = 90.0
    back_.Direction = (0.0,1.0,0.0)
    bottom = doc.foodbin_bottom
    bottom_ = doc.addObject('TechDraw::DrawViewPart','Bottom')
    doc.SmallCutPanelPage_2.addView(bottom_)
    bottom_.Source = bottom
    bottom_.X = 6.35+side_centerX-180+(sideHeight-(6 * 25.4))
    bottom_.Y = 6.35+side_centerY
    bottom_.Rotation = 90.0
    bottom_.Direction = (0.0,.0,1.0)
    top = doc.foodbin_top
    top_ = doc.addObject('TechDraw::DrawViewPart','Top')
    doc.SmallCutPanelPage_2.addView(top_)
    top_.Source = top
    top_.X = 6.35+side_centerX-200+sideHeight
    top_.Y = 6.35+side_centerY+6.35+sideWidth
    top_.Rotation = 90.0
    top_.Direction = (0.0,.0,1.0)
    batteryTop = doc.foodbin_batteryTop
    batteryTop_ = doc.addObject('TechDraw::DrawViewPart','Battery_Top')
    doc.SmallCutPanelPage_2.addView(batteryTop_)
    batteryTop_.Source = batteryTop
    batteryTop_.X = 6.35+side_centerX-230+sideHeight
    batteryTop_.Y = 6.35+side_centerY
    batteryTop_.Rotation = 90.0
    batteryTop_.Direction = (0.0,.0,1.0)
    
    bowlSupportPlate = doc.foodbin_bowlSupportPlate
    bowlSupportPlate_ = doc.addObject('TechDraw::DrawViewPart','Bowl_Support_Plate')
    doc.SmallCutPanelPage_3.addView(bowlSupportPlate_)
    bowlSupportPlate_.Source = bowlSupportPlate
    bowlSupportPlate_.X = 6.35+(3.75 * 25.4)
    bowlSupportPlate_.Y = 6.35+side_centerY
    bowlSupportPlate_.Rotation = 90.0
    bowlSupportPlate_.Direction = (0.0,0.0,1.0)
    batteryBack = doc.foodbin_batteryBack
    batteryBack_ = doc.addObject('TechDraw::DrawViewPart','Battery_Back')
    doc.SmallCutPanelPage_3.addView(batteryBack_)
    batteryBack_.Source = batteryBack
    batteryBack_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35
    batteryBack_.Y = 6.35+side_centerY
    batteryBack_.Rotation = 90.0
    batteryBack_.Direction = (0.0,1.0,0.0)
    bTopStop = doc.foodbin_bTopStop
    bTopStop_ = doc.addObject('TechDraw::DrawViewPart','Battery_Top_Stop')
    doc.SmallCutPanelPage_3.addView(bTopStop_)
    bTopStop_.Source = bTopStop
    bTopStop_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35+(2.5*25.4)
    bTopStop_.Y = 6.35+side_centerY
    bTopStop_.Rotation = 90.0
    bTopStop_.Direction = (0.0,1.0,0.0)
    paddle = doc.foodbin_paddle
    paddle_ = doc.addObject('TechDraw::DrawViewPart','Paddle')
    doc.SmallCutPanelPage_3.addView(paddle_)
    paddle_.Source = paddle
    paddle_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35+(5*25.4)
    paddle_.Y = 6.35+side_centerY
    paddle_.Rotation = 90.0
    paddle_.Direction = (0.0,0.0,-1.0)
    screenFlapSupport = doc.foodbin_screenFlapSupport
    screenFlapSupport_ = doc.addObject('TechDraw::DrawViewPart','Screen_Flap_Support')
    doc.SmallCutPanelPage_3.addView(screenFlapSupport_)
    screenFlapSupport_.Source = screenFlapSupport
    screenFlapSupport_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35+(5*25.4)+70.8+6.35
    screenFlapSupport_.Y = 6.35+side_centerY
    screenFlapSupport_.Rotation = 90.0
    screenFlapSupport_.Direction = (1.0,0.0,0.0)
    screenFlapLockPlate = doc.foodbin_screenFlapLockPlate
    screenFlapLockPlate_ = doc.addObject('TechDraw::DrawViewPart','Screen_Flap_Lock_Plate')
    doc.SmallCutPanelPage_3.addView(screenFlapLockPlate_)
    screenFlapLockPlate_.Source = screenFlapLockPlate
    screenFlapLockPlate_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35+(5*25.4)+70.8+6.35+(3*25.4)
    screenFlapLockPlate_.Y = 6.35+side_centerY
    screenFlapLockPlate_.Rotation = 90.0
    screenFlapLockPlate_.Direction = (1.0,0.0,0.0)
    screenFlap  = doc.foodbin_screenFlap
    screenFlap_ = doc.addObject('TechDraw::DrawViewPart','Screen_Flap')
    doc.SmallCutPanelPage_3.addView(screenFlap_)
    screenFlap_.Source = screenFlap
    screenFlap_.X = 6.35+(3.75 * 25.4)+(5.25*25.4)+6.35+(5*25.4)+70.8+6.35+(3*25.4)
    screenFlap_.Y = 6.35+side_centerY+(4*25.4)
    screenFlap_.Rotation = 90.0 
    screenFlap_.Direction = (1.0,0.0,0.0)
    
    doc.recompute()

    sleep(500)

    TechDrawGui.exportPageAsSvg(doc.SmallCutPanelPage_1,"SmartCatFeeder_Page1.svg")
    TechDrawGui.exportPageAsSvg(doc.SmallCutPanelPage_2,"SmartCatFeeder_Page2.svg")
    TechDrawGui.exportPageAsSvg(doc.SmallCutPanelPage_3,"SmartCatFeeder_Page3.svg")

