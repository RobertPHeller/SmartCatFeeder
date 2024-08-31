// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sat Aug 24 09:01:45 2024
//  Last Modified : <240831.1529>
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
/// @file Schedule.cpp
/// @author Robert Heller
/// @date Sat Aug 24 09:01:45 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include <string>
#include <vector>
#include "Clock.h"
#include "Sensors.h"
#include "BackgroundTask.h"
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include "Display.h"
#include <string.h>
#include <ctype.h>
#include <stdio.h>


#include "Preferences.h"
#include "Schedule.h"
#include "Spinbox.h"

namespace Schedule {

const char Schedule::schedfile_[] = "/Schedule.dat";
std::vector<Schedule *> Schedule::Schedule_;

static ScheduleManager schedManager;

void ScheduleManager::ScheduleManagement()
{
    int first = 0;
    displaySchedule_(first);
    while (true)
    {
        TS_Point p = Display::TouchScreen.getPoint();
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
        for (int i=0; i<LISTSIZE; i++)
        {
            if (i+first >= Schedule::NumberOfFeedings()) break;
            int y = 52+(44*i);
            int x = 10;
            int w = 300;
            int h = 42;
            if ((p.x >= x) && (p.x < (int16_t)(x + w)) && (p.y >= y) &&
                p.y < (int16_t)(y + h))
            {
                listPress(i,true);
                if (listJustPressed(i))
                {
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                listPress(i,false);
                if (listJustReleased(i))
                {
                    scheduleSelected_(i+first);
                    first = 0;
                    displaySchedule_(first);
                }
            }
        }
        bool havePrev = first > 0;
        bool haveNext = (first+LISTSIZE) <Schedule::NumberOfFeedings();
        if (havePrev)
        {
            if (previous_.contains(p.x, p.y))
            {
                previous_.press(true);  // tell the button it is pressed
                if (previous_.justPressed())
                {
                    previous_.drawButton(true);
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                previous_.press(false); // tell the button it is NOT pressed
                if (previous_.justReleased())
                {
                    previous_.drawButton();
                    first -= LISTSIZE;
                    if (first < 0) first = 0;
                    displaySchedule_(first);
                }
            }
        }
        if (haveNext)
        {
            if (next_.contains(p.x, p.y))
            {
                next_.press(true);  // tell the button it is pressed
                if (next_.justPressed())
                {
                    next_.drawButton(true);
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                next_.press(false); // tell the button it is NOT pressed
                if (next_.justReleased())
                {
                    next_.drawButton();
                    first += LISTSIZE;
                    displaySchedule_(first);
                }
            }
        }
        if (add_.contains(p.x, p.y))
        {
            add_.press(true);  // tell the button it is pressed
            if (add_.justPressed())
            {
                add_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            add_.press(false); // tell the button it is NOT pressed
            if (add_.justReleased())
            {
                add_.drawButton();
                addSchedule_();
                first = 0;
                displaySchedule_(first);
            }
        }
        if (return_.contains(p.x, p.y))
        {
            return_.press(true);  // tell the button it is pressed
            if (return_.justPressed())
            {
                return_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            return_.press(false); // tell the button it is NOT pressed
            if (return_.justReleased())
            {
                return_.drawButton();
                return;
            }
        }
    }
    
}

void ScheduleManager::displaySchedule_(int first)
{
    int count = Schedule::NumberOfFeedings();
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Feedings:");
    Display::Display.setTextColor(HX8357_GREEN,HX8357_WHITE);
    for (int i=0; i<LISTSIZE; i++)
    {
        if (i+first >= count) break;
        char buffer[16];
        int8_t hour;
        const Schedule* ele = Schedule::Element(i+first);
        Clock::TimeOfDay when = ele->GetWhen();
        Sensors::Weight weight = ele->GetGoalAmmount();
        switch (Preferences::Preferences::instance()->GetClockFormat())
        {
        case Preferences::Preferences::Twelve:
            
            hour = when.Hour;
            if (hour  > 12) hour -= 12;
            if (hour == 0) hour = 12;
            snprintf(buffer,sizeof(buffer),"%2d:%02d%s, %2d Oz.",
                     hour,when.Minute,(when.Hour<12)?"AM":"PM",weight);
            break;
        case Preferences::Preferences::TwentyFour:
            snprintf(buffer,sizeof(buffer),"%2d:%02d, %2d Oz.",when.Hour,
                     when.Minute,weight);
            break;
        }
        int y = (44*i)+52;
        Display::Display.fillRect(10,y-1,300,42,HX8357_WHITE);
        Display::Display.setCursor(11,y);
        Display::Display.print(buffer);
    }
    if (first > 0)
    {
        previous_.drawButton();
    }
    if (first+LISTSIZE < count)
    {
        next_.drawButton();
    }
    add_.drawButton(); 
    return_.drawButton();
}

String ScheduleManager::ScheduleManagementPage(WebServer *server)
{
    char buffer[256];
    if (server->hasArg("delete"))
    {
        size_t index = atoi(server->arg("delete").c_str());
        Schedule::DeleteElement(index);
    }
    if (server->hasArg("add"))
    {
        Clock::TimeOfDay when;
        Sensors::Weight goal = atoi(server->arg("goal").c_str());;
        if (sscanf(server->arg("when").c_str(),"%02d:%02d",&when.Hour,&when.Minute) == 2 &&
            goal > 0 && goal <= 8)
        {
            (void) new Schedule(when,goal);
        }
    }
    String result("<form method='post' action='/schedule' >\n");
    result += "<ul style='list-style-type: none;'>\n";
    for (int i=0; i<Schedule::NumberOfFeedings(); i++)
    {
        int8_t hour;
        const Schedule* ele = Schedule::Element(i);
        Clock::TimeOfDay when = ele->GetWhen();
        Sensors::Weight weight = ele->GetGoalAmmount();
        switch (Preferences::Preferences::instance()->GetClockFormat())
        {
        case Preferences::Preferences::Twelve:
            hour = when.Hour;
            if (hour  > 12) hour -= 12;
            if (hour == 0) hour = 12;
            snprintf(buffer,sizeof(buffer),
                     "<li>%2d:%02d%s, %2d Oz.",
                     hour,when.Minute,(when.Hour<12)?"AM":"PM",weight);
            break;
        case Preferences::Preferences::TwentyFour:
            snprintf(buffer,sizeof(buffer),"<li>%2d:%02d, %2d Oz.",when.Hour,
                     when.Minute,weight);
            break;
        }
        result += buffer;
        snprintf(buffer,sizeof(buffer)," <button type='submit' name='delete' value='%d'>Delete</button></li>\n",i);
        result += buffer;
    }
    result += "<li><label for='time'>Time:</label>";
    result += "<input id='time' type='time' name='when' />";
    result += "<li><label for='ammount'>Goal Ammount:</label>";
    result += "<input id='ammount' type='number' name='goal' value='1' min='1' max='8' />";
    result += "<button type='submit' name='add' value='1'>Add</button></li>";
    result += "</ul></form>";
    return result;        
}

void ScheduleManager::scheduleSelected_(int index)
{
    char buffer[32];
    int8_t hour;
    const Schedule* ele = Schedule::Element(index);
    Clock::TimeOfDay when = ele->GetWhen();
    Sensors::Weight weight = ele->GetGoalAmmount();
    switch (Preferences::Preferences::instance()->GetClockFormat())
    {
    case Preferences::Preferences::Twelve:
        hour = when.Hour;
        if (hour  > 12) hour -= 12;
        if (hour == 0) hour = 12;
        snprintf(buffer,sizeof(buffer),"Feed at %2d:%02d%s",
                 hour,when.Minute,(when.Hour<12)?"AM":"PM");
        break;
    case Preferences::Preferences::TwentyFour:
        snprintf(buffer,sizeof(buffer),"Feed at %2d:%02d",
                 when.Hour,when.Minute);
        break;
    }
    Display::Display.fillScreen(HX8357_BLACK); 
    Display::Display.fillRect(10,10,300,42*2,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println(buffer);
    Display::Display.setCursor(11,Display::Display.getCursorY());
    Display::Display.print(weight);
    Display::Display.println(" ounces");
    delete_.drawButton();
    return_.drawButton();
    while (true)
    {
        TS_Point p = Display::TouchScreen.getPoint();
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
        if (delete_.contains(p.x, p.y))
        {
            delete_.press(true);  // tell the button it is pressed
            if (delete_.justPressed())
            {
                delete_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            delete_.press(false); // tell the button it is NOT pressed
            if (delete_.justReleased())
            {
                delete_.drawButton();
                Schedule::DeleteElement(index);
                return;
            }
        }
        if (return_.contains(p.x, p.y))
        {
            return_.press(true);  // tell the button it is pressed
            if (return_.justPressed())
            {
                return_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            return_.press(false); // tell the button it is NOT pressed
            if (return_.justReleased())
            {
                return_.drawButton();
                return;
            }
        }
    }
    
}

void ScheduleManager::addSchedule_()
{
    switch (Preferences::Preferences::instance()->GetClockFormat())
    {
    case Preferences::Preferences::Twelve:
        addSchedule_12_();
        break;
    case Preferences::Preferences::TwentyFour:
        addSchedule_24_();
        break;
    }
}

#ifndef min
#define min(a, b) (((a) < (b)) ? (a) : (b))
#endif

#include "am.xbm.h"
#include "pm.xbm.h"
#include "incr.xbm.h"
#include "decr.xbm.h"

ScheduleManager::AMPMSelectbox::AMPMSelectbox(Adafruit_GFX *gfx, int16_t x, 
                                              int16_t y, uint16_t outline, 
                                              uint16_t fill, uint16_t color)
      : _gfx(gfx)
, _x1(x)
, _y1(y)
, _am_w(incr_width)
, _am_h(incr_height)
, _pm_w(decr_width)
, _pm_h(decr_height)
, _outlinecolor(outline)
, _fillcolor(fill)
, _color(color)
{
    _ww = am_width+incr_width+4;
    _hh = am_height+4;
    _am_y1 = _y1;
    _pm_y1 = (_y1+_hh)-decr_height;
    int16_t right = _x1 + _ww;
    _am_x1 = right-incr_width;
    _pm_x1 = right-decr_width;
}

void ScheduleManager::AMPMSelectbox::drawBox(ScheduleManager::AMPMSelectbox::AmPmValue value)
{
    _value = value;
    int w = _ww - max(incr_width,decr_width);
    uint8_t r = min(w, _hh) / 4; // Corner radius
    _gfx->fillRoundRect(_x1, _y1, w, _hh,  r, _fillcolor);
    _gfx->drawRoundRect(_x1, _y1, w, _hh,  r, _outlinecolor);
    switch (_value)
    {
    case AM:
        _gfx->drawXBitmap(_x1+2,_y1+2,am_bits,am_width,am_height,_color);
        break;
    case PM:
        _gfx->drawXBitmap(_x1+2,_y1+2,pm_bits,pm_width,pm_height,_color);
        break;
    }
    _gfx->drawXBitmap(_am_x1,_am_y1,incr_bits,incr_width,incr_height,
                      _color);
    _gfx->drawXBitmap(_pm_x1,_pm_y1,decr_bits,decr_width,decr_height,
                      _color);
}

void ScheduleManager::AMPMSelectbox::processAt(int16_t x, int16_t y)
{
    if (amContains(x,y))
    {
        amPress(true);
    }
    else
    {
        amPress(false);
    }
    if (pmContains(x,y))
    {
        pmPress(true);
    }
    else
    {
        pmPress(false);
    }
    if (amJustReleased())
    {
        am();
    }
    if (amJustPressed()) 
    {
        BackgroundTask::RunTasks(100);
    }
    if (pmJustReleased())
    {
        pm();
    }
    if (pmJustPressed()) 
    {
        BackgroundTask::RunTasks(100);
    }
}

bool ScheduleManager::AMPMSelectbox::amContains(int16_t x, int16_t y)
{
    return ((x >= _am_x1) && (x < (int16_t)(_am_x1 + _am_w)) && 
            (y >= _am_y1) && (y < (int16_t)(_am_y1 + _am_h)));
}

bool ScheduleManager::AMPMSelectbox::amJustPressed()
{
    return (am_currstate && !am_laststate); 
}

bool ScheduleManager::AMPMSelectbox::amJustReleased()
{
    return (!am_currstate && am_laststate); 
}

void ScheduleManager::AMPMSelectbox::am()
{
    if (_value != AM)
    {
        _value = AM;
        _gfx->fillRect(_x1+2,_y1+2,am_width,am_height,_fillcolor);
        _gfx->drawXBitmap(_x1+2,_y1+2,am_bits,am_width,am_height,_color);
    }
}

bool ScheduleManager::AMPMSelectbox::pmContains(int16_t x, int16_t y)
{
    return ((x >= _pm_x1) && (x < (int16_t)(_pm_x1 + _pm_w)) && 
            (y >= _pm_y1) && (y < (int16_t)(_pm_y1 + _pm_h)));
}

bool ScheduleManager::AMPMSelectbox::pmJustPressed()
{
    return (pm_currstate && !pm_laststate); 
}

bool ScheduleManager::AMPMSelectbox::pmJustReleased()
{
    return (!pm_currstate && pm_laststate); 
}

void ScheduleManager::AMPMSelectbox::pm()
{
    if (_value != PM)
    {
        _value = PM;
        _gfx->fillRect(_x1+2,_y1+2,pm_width,pm_height,_fillcolor);
        _gfx->drawXBitmap(_x1+2,_y1+2,pm_bits,pm_width,pm_height,_color);
    }
}



void ScheduleManager::addSchedule_24_()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Add Feeding");
    _hours.SetRange(0,23);
    _hours.drawBox(0);
    Display::Display.drawChar(84,52,':',HX8357_BLUE,HX8357_WHITE,5);
    _minutes.drawBox(0);
    _ounces.drawBox(1);
    Display::Display.setCursor(84,52+52);
    Display::Display.setTextColor(HX8357_BLUE);
    Display::Display.setTextSize(5,5);
    Display::Display.print(" ounces");
    add_.drawButton();
    return_.drawButton();
    while (true)
    {
        TS_Point p = Display::TouchScreen.getPoint();
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
        _hours.processAt(p.x,p.y);
        _minutes.processAt(p.x,p.y);
        _ounces.processAt(p.x,p.y);
        if (add_.contains(p.x, p.y))
        {
            add_.press(true);  // tell the button it is pressed
            if (add_.justPressed())
            {
                add_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            add_.press(false); // tell the button it is NOT pressed
            if (add_.justReleased())
            {
                add_.drawButton();
                Clock::TimeOfDay when;
                when.Hour = _hours.Value();
                when.Minute = _minutes.Value();
                Sensors::Weight goalAmmount = _ounces.Value();
                (void) new Schedule(when,goalAmmount);
                return;
            }
        }
        if (return_.contains(p.x, p.y))
        {
            return_.press(true);  // tell the button it is pressed
            if (return_.justPressed())
            {
                return_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            return_.press(false); // tell the button it is NOT pressed
            if (return_.justReleased())
            {
                return_.drawButton();
                return;
            }
        }
    }
}

void ScheduleManager::addSchedule_12_()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Add Feeding");
    _hours.SetRange(1,12);
    _hours.drawBox(1);
    Display::Display.drawChar(84,52,':',HX8357_BLUE,HX8357_WHITE,5);
    _minutes.drawBox(0);
    _ampm.drawBox(AMPMSelectbox::AM);
    _ounces.drawBox(1);
    Display::Display.setCursor(84,52+52);
    Display::Display.setTextColor(HX8357_BLUE);
    Display::Display.setTextSize(5,5);
    Display::Display.print(" ounces");
    add_.drawButton();
    return_.drawButton();
    while (true)
    {
        TS_Point p = Display::TouchScreen.getPoint();
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
        _hours.processAt(p.x,p.y);
        _minutes.processAt(p.x,p.y);
        _ounces.processAt(p.x,p.y);
        _ampm.processAt(p.x,p.y);
        if (add_.contains(p.x, p.y))
        {
            add_.press(true);  // tell the button it is pressed
            if (add_.justPressed())
            {
                add_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            add_.press(false); // tell the button it is NOT pressed
            if (add_.justReleased())
            {
                add_.drawButton();
                Clock::TimeOfDay when;
                int hour = _hours.Value();
                switch (_ampm.Value())
                {
                case AMPMSelectbox::AM:
                    if (hour == 12)
                    {
                        when.Hour = 0;
                    }
                    else
                    {
                        when.Hour = hour;
                    }
                    break;
                case AMPMSelectbox::PM:
                    if (hour == 12)
                    {
                        when.Hour = 12;
                    }
                    else
                    {
                        when.Hour = hour+12;
                    }
                    break;
                }
                when.Minute = _minutes.Value();
                Sensors::Weight goalAmmount = _ounces.Value();
                (void) new Schedule(when,goalAmmount);
                return;
            }
        }
        if (return_.contains(p.x, p.y))
        {
            return_.press(true);  // tell the button it is pressed
            if (return_.justPressed())
            {
                return_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            return_.press(false); // tell the button it is NOT pressed
            if (return_.justReleased())
            {
                return_.drawButton();
                return;
            }
        }
    }
}

}
