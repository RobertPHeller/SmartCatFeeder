// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 16:28:18 2024
//  Last Modified : <240829.1048>
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
/// @file Sensors.cpp
/// @author Robert Heller
/// @date Fri Aug 16 16:28:18 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_NAU7802.h>
#include <Adafruit_VL6180X.h>
#include "Display.h"
#include "Sensors.h"

namespace Sensors {

static Adafruit_NAU7802 bowl;
static Adafruit_VL6180X binlowsensor;

void Initialize()
{
    if ( !bowl.begin())
    {
        Display::PrintError("Failed to find NAU7802");
        while (true) delay(100);
    }
    Display::Display.println("Found NAU7802");
    bowl.setLDO(NAU7802_3V0);
    bowl.setGain(NAU7802_GAIN_128);
    bowl.setRate(NAU7802_RATE_10SPS);
    // Take 10 readings to flush out readings
    for (uint8_t i=0; i<10; i++) 
    {
        while (! bowl.available()) delay(1);
        bowl.read();
    }
    while (! bowl.calibrate(NAU7802_CALMOD_INTERNAL)) 
    {
        delay(1000);
    }
    Display::Display.println("Calibrated internal offset");
    while (! bowl.calibrate(NAU7802_CALMOD_OFFSET)) 
    {
        delay(1000);
    }
    Display::Display.println("Calibrated system offset");
    if (! binlowsensor.begin())
    {
        Display::PrintError("Failed to find VL6180X");
        while (true) delay(100);
    }
    Display::Display.println("Found VL6180X");
}

// Range to far wall
#define THRESH  1000

bool FoodBinLow()
{
    uint8_t range = binlowsensor.readRange();
    uint8_t status = binlowsensor.readRangeStatus();
    if (status == VL6180X_ERROR_NONE)
    {
        return range < THRESH;
    }
    else
    {
        return true; // assume empty
    }
}

// Conversion factors...
#define TARE 1000
#define OUNCE 500.0


double BowlAmmount()
{
    while (! bowl.available()) 
    {
        delay(1);
    }
    int32_t val = bowl.read();
    return (val-TARE)/OUNCE;
}

}
