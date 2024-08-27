// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Tue Aug 27 09:52:58 2024
//  Last Modified : <240827.1236>
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
/// @file MainScreen.cpp
/// @author Robert Heller
/// @date Tue Aug 27 09:52:58 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Adafruit_TSC2007.h>
#include "Display.h"
#include "time.h"
#include "ClockDisplay.h"
#include "Button_xbm.h"
#include "BackgroundTask.h"
#include "MainScreen.h"
#include "Mechanical.h"
#include "Sensors.h"
#include "Preferences.h"
#include "Schedule.h"

namespace MainScreen {

#include "clock.xbm.h"
#include "gear.xbm.h"
#include "hand.xbm.h"

void MainScreen::Initialize()
{
    buttons_[gear].initButtonUL(&Display::Display,25,400,gear_width,gear_height,gear_bits,HX8357_GREEN);
    buttons_[clock].initButtonUL(&Display::Display,125,400,clock_width,clock_height,clock_bits,HX8357_BLUE);
    buttons_[hand].initButtonUL(&Display::Display,230,400,hand_width,hand_height,hand_bits,HX8357_YELLOW);
}
void MainScreen::Loop()
{
    switch (check_buttons_())
    {
    case gear:
        Preferences::Preferences::instance()->Settings();
        break;
    case clock:
        break;
    case hand:
        break;
    default:
        break;
    }
    if ((millis() - lastMillis_) > 1000)
    {
        refreshScreen_();
        lastMillis_ = millis();
    }
    BackgroundTask::RunTasks(100);
}

MainScreen::ButtonIndex MainScreen::check_buttons_()
{
    ButtonIndex btn = lastbutton;
    TS_Point p = Display::TouchScreen.getPoint();;
    if (((p.x == 0) && (p.y == 0)) || (p.z < 10)) 
    {
        // this is our way of tracking touch 'release'!
        p.x = p.y = p.z = -1;
    }
    // Scale from ~0->4000 to  tft.width using the calibration #'s
    if (p.z != -1) 
    {
        int py = map(p.x, Display::TSMax_x, Display::TSMin_x, 0, Display::Display.height());
        int px = map(p.y, Display::TSMin_y, Display::TSMax_y, 0, Display::Display.width());
        p.x = px;
        p.y = py;
    }
    for (uint8_t b = (uint8_t)gear; b < (uint8_t)lastbutton; b++)
    {
        if (buttons_[b].contains(p.x, p.y))
        {
            buttons_[b].press(true);
        }
        else
        {
            buttons_[b].press(false);
        }
    }
    for (uint8_t b = (uint8_t)gear; b < (uint8_t)lastbutton; b++)
    {
        if (buttons_[b].justReleased())
        {
            btn = (ButtonIndex)b;
        }
        if (buttons_[b].justPressed())
        {
            BackgroundTask::RunTasks(100); // UI debouncing
        }
    }
    return btn;
}

ClockDisplay::ClockDisplay clockDisplay;

void MainScreen::refreshScreen_()
{
    struct tm timeinfo;
    
    Display::Display.fillScreen(HX8357_BLACK);
    if (getLocalTime(&timeinfo))
    {
        clockDisplay.DisplayTime(timeinfo.tm_hour,timeinfo.tm_min,(timeinfo.tm_sec&&1));
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
    for (uint8_t b = (uint8_t)gear; b < (uint8_t)lastbutton; b++)
    {
        buttons_[b].drawButton();
    }
}
}
