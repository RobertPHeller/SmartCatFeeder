// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Thu Aug 15 15:12:55 2024
//  Last Modified : <240816.2119>
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
/// @file Display.cc
/// @author Robert Heller
/// @date Thu Aug 15 15:12:55 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Adafruit_TSC2007.h>
#include "Display.h"

#include "Revision.h"

#define STMPE_CS 6
#define TFT_CS   9
#define TFT_DC   10
#define SD_CS    5

#define TFT_RST -1

// For TSC2007
#define TSC_TS_MINX 300
#define TSC_TS_MAXX 3800
#define TSC_TS_MINY 185
#define TSC_TS_MAXY 3700


namespace Display {

// we will assign the calibration values on init
int16_t TSMin_x, TSMax_x, TSMin_y, TSMax_y;
// Use hardware SPI and the above for CS/DC

Adafruit_HX8357 Display = Adafruit_HX8357(TFT_CS, TFT_DC, TFT_RST);
#define TSC_IRQ STMPE_CS
Adafruit_TSC2007 TouchScreen = Adafruit_TSC2007();             // newer rev 2 touch contoller



void Initialize()
{
    Display.begin();
    Display.setRotation(1);
    Display.fillScreen(HX8357_BLACK);
    Display.setTextColor(HX8357_WHITE);
    Display.setTextSize(5);
    Display.println(PROGRAM_NAME);
    Display.setTextSize(3);
    Display.println(BUILD_TIME);
    Display.println(BUILT_BY);
    Display.println(REVISION_GIT_HASH);
    if (! TouchScreen.begin(0x48, &Wire)) {
        PrintError("Couldn't start TSC2007 touchscreen controller");
        while (1) delay(100);
    }
    
    TSMin_x = TSC_TS_MINX; TSMax_x = TSC_TS_MAXX;
    TSMin_y = TSC_TS_MINY; TSMax_y = TSC_TS_MAXY;
    pinMode(TSC_IRQ, INPUT);
}

void PrintError(const char *message)
{
    Display.setTextSize(3);
    Display.setTextColor(HX8357_RED);
    Display.println(message);
}

}
