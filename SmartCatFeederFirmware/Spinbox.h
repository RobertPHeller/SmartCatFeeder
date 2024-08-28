// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Wed Aug 28 14:40:22 2024
//  Last Modified : <240828.1642>
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
/// @file Spinbox.h
/// @author Robert Heller
/// @date Wed Aug 28 14:40:22 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __SPINBOX_H
#define __SPINBOX_H

#include <Arduino.h>
#include <stdio.h>
#include <Adafruit_GFX.h>



class Spinbox {
public:
    Spinbox(Adafruit_GFX *gfx, int16_t x, int16_t y,  
            uint16_t outline, uint16_t fill,uint16_t textcolor,
            int16_t minv, int16_t maxv, 
            const char *fmt = "%d");
    void drawBox(int16_t value = 0);
    void processAt(int16_t x, int16_t y);
    int16_t Value() {return _value;}
protected:
    bool incrContains(int16_t x, int16_t y);
    void incrPress(bool p)
    {
        incr_laststate = incr_currstate;
        incr_currstate = p;
    }
    bool incrJustPressed();
    bool incrJustReleased();
    void incr();
    bool decrContains(int16_t x, int16_t y);
    void decrPress(bool p)
    {
        decr_laststate = decr_currstate;
        decr_currstate = p;
    }
    bool decrJustPressed();
    bool decrJustReleased();
    void decr();
private:
    Adafruit_GFX *_gfx; 
    int16_t _x1, _y1; // Coordinates of top-left corner
    int16_t _ww, _hh; // total width, total height
    int16_t _incr_x1, _incr_y1; // Coordinates of top-left corner of incr
    int16_t _incr_w, _incr_h;
    int16_t _decr_x1, _decr_y1; // Coordinates of top-left corner of incr
    int16_t _decr_w, _decr_h;
    uint8_t _textsize_x;
    uint8_t _textsize_y;
    uint16_t _outlinecolor, _fillcolor, _textcolor;
    int16_t _value, _minVal, _maxVal;
    char _format[10];
    bool incr_currstate, incr_laststate;
    bool decr_currstate, decr_laststate;
};
#endif // __SPINBOX_H

