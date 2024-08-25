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
//  Last Modified : <240824.2052>
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
#include "ClockDisplay.h"

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
    Schedule::Schedule::Read();
    Clock::Initialize();
    Networking::Initialize();
    Mechanical::Initialize();
    Sensors::Initialize();
}

ClockDisplay::ClockDisplay clockDisplay;

#include "clock.xbm.h"
#include "gear.xbm.h"
#include "hand.xbm.h"

static enum {MainScreen, SettingsScreen, ScheduleScreen, ManualScreen} currentScreen = MainScreen;

void loop() {
    // put your main code here, to run repeatedly:
    struct tm timeinfo;
    uint16_t x, y, z1, z2;
    FeedWebServer::FeedWebServer::instance()->handleClient();
    Schedule::Schedule::CheckForFeeding();
    Mechanical::CheckFeedCycle();
    switch (currentScreen)
    {
    case MainScreen:
        Display::Display.fillScreen(HX8357_BLACK);
        if (getLocalTime(&timeinfo))
        {
            clockDisplay.DisplayTime(timeinfo.tm_hour,timeinfo.tm_min,(timeinfo.tm_sec&&1));
        }
        else
        {
            delay(1000);
            return;
        }
        if (Sensors::FoodBinLow())
        {
            Display::Display.setTextColor(HX8357_RED,HX8357_BLACK);
            Display::Display.setTextSize(3);
            Display::Display.setCursor(0,50);
            Display::Display.println("Food bin is low!");
        }
        Display::Display.setTextColor(HX8357_WHITE,HX8357_BLACK);
        Display::Display.setTextSize(2);
        Display::Display.setCursor(0,100);
        Display::Display.printf("Bowl contains %3.1f Oz.",Sensors::BowlAmmount());
        Display::Display.setCursor(0,150);
        {
            Clock::TimeOfDay now;
            now.Hour = timeinfo.tm_hour;
            now.Minute = timeinfo.tm_min;
            const Schedule::Schedule *next = Schedule::Schedule::NextSchedule(now);
            if (next != nullptr)
            {
                Clock::TimeOfDay when = next->GetWhen();
                Sensors::Weight weight = next->GetGoalAmmount();
                int8_t hour;
                switch (Preferences::Preferences::instance()->GetClockFormat())
                {
                case Preferences::Preferences::Twelve:
                    hour = when.Hour;
                    if (hour  > 12) hour -= 12;
                    if (hour == 0) hour = 12;
                    Display::Display.printf("Next feeding at %2d:%02d%s, %2d Oz.",
                                            hour,when.Minute,
                                            (when.Hour<12)?"AM":"PM",
                                            weight);
                    break;
                case Preferences::Preferences::TwentyFour:
                    Display::Display.printf("Next feeding at %2d:%02d, %2d Oz.",
                                            when.Hour,when.Minute,
                                            weight);
                    break;
                }
            }
            else
            {
                Display::Display.println("No feeding scheduled.");
            }
        }
        // touch icons
        Display::Display.drawXBitmap(25,400,gear_bits,gear_width,gear_height,HX8357_GREEN);
        Display::Display.drawXBitmap(125,400,clock_bits,clock_width,clock_height,HX8357_BLUE);
        Display::Display.drawXBitmap(230,400,hand_bits,hand_width,hand_height,HX8357_YELLOW);
        if (Display::TouchScreen.read_touch(&x, &y, &z1, &z2))
        {
            if (y >= 400 && y <= 450)
            {
                if (x >= 25 && x <= 75)
                {
                    // gear: settings
                    Preferences::Preferences::instance()->SettingsScreenStart();
                    currentScreen = SettingsScreen;
                }
                else if (x >= 125 && x <= 175)
                {
                    // clock: schedule
                    Schedule::Schedule::ScheduleScreenStart();
                    currentScreen = ScheduleScreen;
                }
                else if (x >= 230 && x <= 280)
                {
                    // hand -- manual feading
                    Mechanical::ManualFeedingStart();
                    currentScreen = ManualScreen;
                }
            }
        }
        break;
    case SettingsScreen:
        if (!Preferences::Preferences::instance()->SettingsScreen()) 
        {
            currentScreen = MainScreen;
        }
        break;
    case ScheduleScreen:
        if (!Schedule::Schedule::ScheduleScreen())
        {
            currentScreen = MainScreen;
        }
        break;
    case ManualScreen:
        if (!Mechanical::ManualFeeding())
        {
            currentScreen = MainScreen;
        }
        break;
    }
    delay(100);
}    
