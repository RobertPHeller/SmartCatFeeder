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
//  Last Modified : <240829.1527>
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
        Schedule::ScheduleManager::instance()->ScheduleManagement();
        break;
    case hand:
        Mechanical::FeedMotors::instance()->ManualFeed();
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

static String currentTime()
{
    char buffer[64];
    struct tm timeinfo;
    int8_t hour;
    
    if (!getLocalTime(&timeinfo))
    {
        return String("<h2>No time available (yet)</h2>");
    }
    switch (Preferences::Preferences::instance()->GetClockFormat()) {
    case Preferences::Preferences::Twelve:
        hour = timeinfo.tm_hour;
        if (hour  > 12) hour -= 12;
        if (hour == 0) hour = 12;
        snprintf(buffer,sizeof(buffer),"<h2>Current time: %2d:%02d%s</h2>",
                 hour,timeinfo.tm_min,(timeinfo.tm_hour<12)?"AM":"PM");
        break;
    case Preferences::Preferences::TwentyFour:
        snprintf(buffer,sizeof(buffer),"<h2>Current time: %2d:%02d</h2>",
                 timeinfo.tm_hour,timeinfo.tm_min);
        break;
    }
    return String(buffer);
}

static String webButtons()
{
    String result("<div id=\"buttonbox\">");
    result+="<a href='/settings'><img src='/icons8-gear-50.png' width='50' height='50' alt='settings' /></a>";
    result+="<a href='/schedule'><img src='/icons8-clock-50.png' width='50' height='50' alt='schedule' /></a>";
    result+="<a href='/manual'><img src='/icons8-hand-50.png' width='50' height='50' alt='manual' /></a>";
    result+="</div>";
    return result;
}

String MainScreen::Page()
{
    char buffer[256];
    String result = currentTime();
    if (Sensors::FoodBinLow())
    {
        result += "<h3 style=\"color:red;\">Food bin is low!</h3>";
    }
    snprintf(buffer,sizeof(buffer),"<h4>Bowl contains %3.1f Oz.</h4>",
             Sensors::BowlAmmount());
    result += buffer;
    struct tm timeinfo;
    if (getLocalTime(&timeinfo))
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
                snprintf(buffer,sizeof(buffer),
                         "<h4>Next feeding at %2d:%02d%s, %2d Oz.</h4>",
                         hour,when.Minute,
                         (when.Hour<12)?"AM":"PM",
                         weight);
                break;
            case Preferences::Preferences::TwentyFour:
                snprintf(buffer,sizeof(buffer),
                         "<h4>Next feeding at %2d:%02d, %2d Oz.</h4>",
                         when.Hour,when.Minute,
                         weight);
                break;
            }
        }
        else
        {
            strncpy(buffer,"<h4>No feeding scheduled.</h4>",sizeof(buffer));
        }
        result += buffer;
    }
    result += webButtons();
    return result;
}

}
