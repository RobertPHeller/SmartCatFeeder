// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 16:25:46 2024
//  Last Modified : <240816.2203>
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
/// @file Clock.cpp
/// @author Robert Heller
/// @date Fri Aug 16 16:25:46 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <time.h>
#include <esp_sntp.h>
#include <RTClib.h>
#include <FS.h>
#include <SPIFFS.h>
#include "Display.h"
#include "Preferences.h"
namespace Clock {

static RTC_PCF8523 rtc;

static const char* ntpServer1 = "pool.ntp.org";
static const char* ntpServer2 = "time.nist.gov";

void Initialize()
{
    struct timespec thetime = {0,0};
    if (! rtc.begin()) {
        Display::PrintError("Couldn't find RTC");
        while (1) delay(100);
    }
    
    if (! rtc.initialized() || rtc.lostPower()) {
        rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }
    
    rtc.start();
    uint32_t time = rtc.now().unixtime();
    thetime.tv_sec = time;
    clock_settime (CLOCK_REALTIME, &thetime);
    configTzTime(Preferences::Preferences::instance()->GetTimeZone(), 
                 ntpServer1, ntpServer2);
}

void timeavailable(struct timeval *t)
{
    rtc.adjust(DateTime((uint32_t)(t->tv_sec)));
}

}


