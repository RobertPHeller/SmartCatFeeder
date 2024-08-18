// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Thu Aug 15 12:59:18 2024
//  Last Modified : <240817.0827>
//
//  Description	
//
//  Notes
//
//  History
//	
/////////////////////////////////////////////////////////////////////////////
//
//    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
//			51 Locke Hill Road
//			Wendell, MA 01379-9728
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program; if not, write to the Free Software
//    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
//
// 
//
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <WiFi.h>
#include <Wire.h>
#include "time.h"
#include "esp_sntp.h"
#include <RTClib.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Adafruit_TSC2007.h>
//#include <Adafruit_NAU7802.h>
#include <Adafruit_MotorShield.h>
#include <Adafruit_VL6180X.h>

#include <FS.h>
#include <SPIFFS.h>

#include "Display.h"
#include "Networking.h"
#include "Clock.h"
#include "Mechanical.h"
#include "Sensors.h"
#include "Preferences.h"
#include "Schedule.h"
#include "FeedWebServer.h"

DEFINE_SINGLETON_INSTANCE(Preferences::Preferences);
static Preferences::Preferences prefs("/Preferences.dat");
DECLARESCHEDULE;

#define FORMAT_SPIFFS_IF_FAILED true
void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);
    Display::Initialize();
    if(!SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED)) {
        Display::PrintError("SPIFFS Mount Failed");
        while (1) delay(100);
    }
    prefs.Read();
    Schedule::Schedule::Read("/Schedule.dat");
    Clock::Initialize();
    Networking::Initialize();
    Mechanical::Initialize();
    Sensors::Initialize();
}
                
void loop() {
    // put your main code here, to run repeatedly:
    FeedWebServer::FeedWebServer::instance()->handleClient();
}    
