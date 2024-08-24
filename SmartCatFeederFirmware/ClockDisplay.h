// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sat Aug 24 13:10:01 2024
//  Last Modified : <240824.1419>
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
/// @file ClockDisplay.h
/// @author Robert Heller
/// @date Sat Aug 24 13:10:01 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __CLOCKDISPLAY_H
#define __CLOCKDISPLAY_H

#include <Adafruit_GFX.h>

namespace ClockDisplay {

#define CLOCK_W 160
#define CLOCK_H10 0
#define CLOCK_H1 32
#define CLOCK_COLON 58
#define CLOCK_M10 64
#define CLOCK_M1  96
#define CLOCK_AMPM 128
#define CLOCK_H  50
#define CLOCK_X   0
#define CLOCK_Y   0
#define CLOCK_COLOR HX8357_CYAN
#define CLOCK_BACKGROUND HX8357_BLACK

class ClockDisplay : public GFXcanvas1 {
public:
    ClockDisplay() : GFXcanvas1(CLOCK_W,CLOCK_H)
    {
    }
    ~ClockDisplay() {}
    void DisplayTime(int hours, int minutes, bool colonflag);
private:
    typedef struct {
        /** The bitmap itself. */
        unsigned char *bits;
        /** The width of the bitmap. */
        int  width;
        /** The height of the bitmap. */
        int  height; 
    } digitBitmapMap;
    static digitBitmapMap digitBitmaps[10];
    void drawdigit(int v,int xoff);
    void drawcolon();
    void drawampm(bool am);
};

}

#endif // __CLOCKDISPLAY_H

