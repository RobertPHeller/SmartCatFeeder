// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 09:13:32 2024
//  Last Modified : <240831.1124>
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
/// @file Schedule.h
/// @author Robert Heller
/// @date Fri Aug 16 09:13:32 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __SCHEDULE_H
#define __SCHEDULE_H

#include <Arduino.h>
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include "Clock.h"
#include "Sensors.h"
#include "Mechanical.h"
#include "Singleton.h"
#include "BackgroundTask.h"
#include <Adafruit_GFX.h>
#include <WebServer.h>
#include <Adafruit_HX8357.h>
#include "Display.h"
#include "Spinbox.h"

#include <FS.h>
#include <SPIFFS.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>

namespace Schedule {

class Schedule
{
private:
    static bool EarlierSched(const Schedule *x, const Schedule *y)
    {
        if (x->when_.Hour < y->when_.Hour)
        {
            return true;
        }
        else if (x->when_.Hour == y->when_.Hour)
        {
            return x->when_.Minute < y->when_.Minute;
        }
        else
        {
            return false;
        }
    }
public:
    Schedule(Clock::TimeOfDay when,Sensors::Weight goalAmmount)
                : when_(when)
          , goalAmmount_(goalAmmount)
    {
        Schedule_.push_back(this);
        std::sort(Schedule_.begin(),Schedule_.end(),EarlierSched);
    }
    ~Schedule()
    {
        auto it = std::find(Schedule_.begin(),Schedule_.end(),this);
        if (it != Schedule_.end())
        {
            Schedule_.erase(it);
        }
    }
    bool TimeEQ(const Clock::TimeOfDay time) const {
        return (time.Hour == when_.Hour && time.Minute == when_.Minute);
    }
    bool TimeGT(const Clock::TimeOfDay time) const {
        if (when_.Hour > time.Hour)
        {
            return true;
        }
        else if (time.Hour == when_.Hour && when_.Minute > time.Minute)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    Clock::TimeOfDay GetWhen() const  {return when_;}
    Sensors::Weight GetGoalAmmount() const  {return goalAmmount_;}
    static size_t Size() {return Schedule_.size();}
    static const Schedule* Element(unsigned i)
    {
        if (i < Schedule_.size())
        {
            return Schedule_[i];
        }
        else
        {
            return nullptr;
        }
    }
    static int Read()
    {
        File file = SPIFFS.open(schedfile_);
        if(!file) return 0; // no schedfile
        for (auto it = Schedule_.begin(); it != Schedule_.end(); it++)
        {
            Schedule_.erase(it);
        }
        do {
            char buffer[256];
            Clock::TimeOfDay when;
            Sensors::Weight goalAmmount;
            size_t len = file.readBytesUntil('\n',buffer,sizeof(buffer));
            if (len > 0)
            {
                int count = sscanf(buffer,"%d %d %d",&when.Hour,&when.Minute,&goalAmmount);
                if (count == 3)
                {
                    (void) new Schedule(when,goalAmmount);
                }
            }
        } while(file);
        file.close();
        return 0;
    }
    static int Write()
    {
        char buffer[256];
        File file = SPIFFS.open(schedfile_,FILE_WRITE,true);
        if(!file) return -1; // can't write/create schedfile!
        for (auto it = Schedule_.begin(); it != Schedule_.end(); it++)
        {
            Schedule *s = *it;
            snprintf(buffer,sizeof(buffer),"%d %d %d",s->when_.Hour,s->when_.Minute,s->goalAmmount_);
            file.println(buffer);
        }
        file.close();
        return 0;
    }
    static bool IsTime(Clock::TimeOfDay now,Sensors::Weight& goalAmmount)
    {
        auto is_time = [now](Schedule *s){return s->TimeEQ(now);};
        auto it = find_if(Schedule_.begin(),Schedule_.end(),is_time);
        if (it != Schedule_.end())
        {
            goalAmmount = (*it)->goalAmmount_;
            return true;
        }
        else
        {
            return false;
        }
    }
    static const Schedule * NextSchedule(const Clock::TimeOfDay& now)
    {
        auto next_time = [now](Schedule *s){return s->TimeGT(now);};
        auto it = find_if(Schedule_.begin(),Schedule_.end(),next_time);
        if (it != Schedule_.end())
        {
            return *it;
        }
        else
        {
            it = Schedule_.begin();
            if (it != Schedule_.end())
            {
                return *it;
            }
            else
            {
                return nullptr;
            }
        }
    }
    static size_t NumberOfFeedings() {return Schedule_.size();}
    static const Schedule * ScheduleElement(size_t index)
    {
        if (index < Schedule_.size())
        {
            return Schedule_[index];
        }
        else
        {
            return nullptr;
        }
    }
    static void DeleteElement(size_t index)
    {
        if (index < Schedule_.size())
        {
            delete Schedule_[index];
        }
    }
private:
    Clock::TimeOfDay when_;
    Sensors::Weight goalAmmount_;
    static std::vector<Schedule *> Schedule_;
    static const char schedfile_[];
};

class ScheduleManager : public BackgroundTask, public Singleton<ScheduleManager>
{
public:
    ScheduleManager() 
                : BackgroundTask()
          , _hours(&Display::Display,10,52,HX8357_WHITE,HX8357_BLACK,
                   HX8357_BLUE,1,12,"%2d")
          , _minutes(&Display::Display,114,52,HX8357_WHITE,HX8357_BLACK,
                     HX8357_BLUE,0,59,"%02d")
          , _ampm(&Display::Display,188,52,HX8357_WHITE,HX8357_BLACK,
                  HX8357_BLUE)
          , _ounces(&Display::Display,10,52+52,HX8357_WHITE,HX8357_BLACK,
                    HX8357_BLUE,1,8,"%d")
    {
        return_.initButtonUL(&Display::Display,10,278,300,42,
                             HX8357_WHITE,HX8357_BLACK,HX8357_BLUE,
                             "Return",5);
        yes_.initButtonUL(&Display::Display,35,236,100,42,
                          HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                          "Yes",5);
        no_.initButtonUL(&Display::Display,195,236,100,42,
                         HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                         "No",5);
        previous_.initButtonUL(&Display::Display,10,236,100,42,
                               HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                               "Previous",5);
        next_.initButtonUL(&Display::Display,110,236,100,42,
                           HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                           "Next",5);
        add_.initButtonUL(&Display::Display,210,236,100,42,
                          HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                          "+",5);
        delete_.initButtonUL(&Display::Display,10,236,300,42,
                             HX8357_WHITE,HX8357_BLACK,HX8357_RED,
                             "Delete",5);
        
    }
    virtual void RunTask()
    {
        struct tm timeinfo;
        if (getLocalTime(&timeinfo))
        {
            Clock::TimeOfDay now;
            now.Hour = timeinfo.tm_hour;
            now.Minute = timeinfo.tm_min;
            Sensors::Weight goalAmmount;
            if (Schedule::IsTime(now,goalAmmount))
            {
                Mechanical::FeedMotors::instance()->StartFeeding(goalAmmount);
            }
        }
    }
    void ScheduleManagement();
    String ScheduleManagementPage(WebServer *webserver);
private:
    class AMPMSelectbox {
    public:
        typedef enum {AM, PM} AmPmValue;
        AMPMSelectbox(Adafruit_GFX *gfx, int16_t x, int16_t y,
                      uint16_t outline, uint16_t fill,uint16_t color);
        void drawBox(AmPmValue = AM);
        void processAt(int16_t x, int16_t y);
        AmPmValue Value() {return _value;}
    protected:
        bool amContains(int16_t x, int16_t y);
        void amPress(bool p)
        {
            am_laststate = am_currstate;
            am_currstate = p;
        }
        bool amJustPressed();
        bool amJustReleased();
        void am();
        bool pmContains(int16_t x, int16_t y);
        void pmPress(bool p)
        {
            pm_laststate = pm_currstate;
            pm_currstate = p;
        }
        bool pmJustPressed();
        bool pmJustReleased();
        void pm();
    private:
        Adafruit_GFX *_gfx;
        int16_t _x1, _y1; // Coordinates of top-left corner
        int16_t _ww, _hh; // total width, total height
        int16_t _am_x1, _am_y1; // Coordinates of top-left corner of am
        int16_t _am_w, _am_h;
        int16_t _pm_x1, _pm_y1; // Coordinates of top-left corner of pm
        int16_t _pm_w, _pm_h;
        uint16_t _outlinecolor, _fillcolor, _color;
        AmPmValue _value;
        bool am_currstate, am_laststate;
        bool pm_currstate, pm_laststate;
    };
    void displaySchedule_(int first);
    void scheduleSelected_(int index);
    void addSchedule_();
    void addSchedule_12_();
    void addSchedule_24_();
    static constexpr const uint8_t LISTSIZE = 4;
    bool list_currstate[LISTSIZE], list_laststate[LISTSIZE];
    bool listJustPressed(uint8_t i)
    {
        HASSERT(i < LISTSIZE);
        return (list_currstate[i] && !list_laststate[i]);
    }
    bool listJustReleased(uint8_t i)
    {
        HASSERT(i < LISTSIZE);
        return  (!list_currstate[i] && list_laststate[i]);
    }
    void listPress(uint8_t i, bool p)
    {
        HASSERT(i < LISTSIZE);
        list_laststate[i] = list_currstate[i];
        list_currstate[i] = p;
    }
    bool listIsPressed(uint8_t i) 
    {
        HASSERT(i < LISTSIZE);
        return list_currstate[i];
    }
    Adafruit_GFX_Button return_;
    Adafruit_GFX_Button yes_;
    Adafruit_GFX_Button no_;
    Adafruit_GFX_Button previous_;
    Adafruit_GFX_Button next_;
    Adafruit_GFX_Button add_;
    Adafruit_GFX_Button delete_;
    Spinbox _hours, _minutes, _ounces;
    AMPMSelectbox _ampm;
};

}


#endif // __SCHEDULE_H

