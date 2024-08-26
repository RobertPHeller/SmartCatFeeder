// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Mon Aug 26 14:10:02 2024
//  Last Modified : <240826.1421>
//
//  Description	
//
//  Notes
//
//  History
//	
/////////////////////////////////////////////////////////////////////////////
/// @copyright
///    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
///			51 Locke Hill Road
///			Wendell, MA 01379-9728
///
///    This program is free software; you can redistribute it and/or modify
///    it under the terms of the GNU General Public License as published by
///    the Free Software Foundation; either version 2 of the License, or
///    (at your option) any later version.
///
///    This program is distributed in the hope that it will be useful,
///    but WITHOUT ANY WARRANTY; without even the implied warranty of
///    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
///    GNU General Public License for more details.
///
///    You should have received a copy of the GNU General Public License
///    along with this program; if not, write to the Free Software
///    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
/// @file Button_xbm.cpp
/// @author Robert Heller
/// @date Mon Aug 26 14:10:02 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";


#include <Adafruit_GFX.h>
#include "Button_xbm.h"

namespace Button_xbm {

Button_xbm::Button_xbm()
{
    _gfx = 0;
}

void Button_xbm::initButtonUL(Adafruit_GFX *gfx, int16_t x1, int16_t y1, 
                              uint16_t w, uint16_t h, const uint8_t bitmap[], 
                              uint16_t color)
{
    _x1 = x1;
    _y1 = y1;
    _w = w;
    _h = h;
    _color = color;
    _gfx = gfx; 
    _bitmap = bitmap;
}

void Button_xbm::drawButton()
{
    _gfx->drawXBitmap(_x1,_y1,_bitmap, _w, _h, _color);
}

bool Button_xbm::contains(int16_t x, int16_t y)
{
    return ((x >= _x1) && (x < (int16_t)(_x1 + _w)) && (y >= _y1) &&
            (y < (int16_t)(_y1 + _h)));
}

bool Button_xbm::justPressed()
{
    return (currstate && !laststate);
}

bool Button_xbm::justReleased()
{
    return (!currstate && laststate);
}




}
