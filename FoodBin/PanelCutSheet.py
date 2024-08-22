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
#  Last Modified : <240822.1211>
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

import FoodBin

if __name__ == '__main__':
    for docname in App.listDocuments():
        lddoc = App.getDocument(docname)
        if lddoc.Label == 'FoodBin':
            doc = lddoc
            break
    if doc == None:
        App.open("FoodBin.fcstd")
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
                                                
    # Panels:
    #   foodbin_bottom
    #   foodbin_front
    #   foodbin_left
    #   foodbin_right
    #   foodbin_back
    #   foodbin_batteryBack
    #   foodbin_batteryTop
    #   foodbin_top
    #   foodbin_bTopStop
    #   foodbin_agitator_disk1
    #   foodbin_agitator_disk2
    #   foodbin_agitator_disk3
    #   foodbin_agitator_disk4
    #   foodbin_paddle
    #   foodbin_bowlSupportPlate
