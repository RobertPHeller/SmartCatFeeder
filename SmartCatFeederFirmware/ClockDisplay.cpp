// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sat Aug 24 13:33:27 2024
//  Last Modified : <240824.1420>
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
/// @file ClockDisplay.cpp
/// @author Robert Heller
/// @date Sat Aug 24 13:33:27 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Adafruit_GFX.h>
#include "Preferences.h"
#include "Display.h"
#include "ClockDisplay.h"

namespace ClockDisplay {

#include "_0.xbm.h"
#include "_1.xbm.h"
#include "_2.xbm.h"
#include "_3.xbm.h"
#include "_4.xbm.h"
#include "_5.xbm.h"
#include "_6.xbm.h"
#include "_7.xbm.h"
#include "_8.xbm.h"
#include "_9.xbm.h"
#include "am.xbm.h"
#include "colon.xbm.h"
#include "pm.xbm.h"

ClockDisplay::digitBitmapMap ClockDisplay::digitBitmaps[] = {
    {_0_bits, _0_width, _0_height},
    {_1_bits, _1_width, _1_height},
    {_2_bits, _2_width, _2_height},
    {_3_bits, _3_width, _3_height},
    {_4_bits, _4_width, _4_height},
    {_5_bits, _5_width, _5_height},
    {_6_bits, _6_width, _6_height},
    {_7_bits, _7_width, _7_height},
    {_8_bits, _8_width, _8_height},
    {_9_bits, _9_width, _9_height}
};

void ClockDisplay::drawdigit(int v,int xoff)
{
    drawXBitmap(xoff,0,digitBitmaps[v].bits,digitBitmaps[v].width,digitBitmaps[v].height,1);
}

void ClockDisplay::drawcolon()
{
     drawXBitmap(CLOCK_COLON,0,colon_bits,colon_width,colon_height,1);
}

void ClockDisplay::drawampm(bool am)
{
    if (am)
    {
        drawXBitmap(CLOCK_AMPM,0,am_bits,am_width,am_height,1);
    }
    else
    {
        drawXBitmap(CLOCK_AMPM,0,pm_bits,pm_width,pm_height,1);
    }
}


void ClockDisplay::DisplayTime(int hours, int minutes, bool colonflag)
{
    int hHigh, hLow;
    bool am;
    int mHigh = minutes / 10;
    int mLow  = minutes % 10;
    bool display_ampm = false;
    
    switch (Preferences::Preferences::instance()->GetClockFormat()) 
    {
    case Preferences::Preferences::Twelve:
        {
            int hour = hours;
            if (hour  > 12) hour -= 12;
            if (hour == 0) hour = 12;
            am = hours<12;
            hHigh = hour / 10;
            hLow =  hour % 10;
            display_ampm = true;
            break;
        }
    case Preferences::Preferences::TwentyFour:
        hHigh = hours / 10;
        hLow  = hours % 10;
        break;
    }
    fillScreen(0);
    if (hHigh != 0)
    {
        drawdigit(hHigh,CLOCK_H10);
    }
    drawdigit(hLow,CLOCK_H1);
    if (colonflag) drawcolon();
    drawdigit(mHigh,CLOCK_M10);
    drawdigit(mLow,CLOCK_M1);
    if (display_ampm) drawampm(am);
    Display::Display.drawBitmap(CLOCK_X,CLOCK_Y,getBuffer(),CLOCK_W,CLOCK_H,
                                CLOCK_COLOR,CLOCK_BACKGROUND);
}

}
