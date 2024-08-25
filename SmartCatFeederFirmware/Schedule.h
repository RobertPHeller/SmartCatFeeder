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
//  Last Modified : <240824.2101>
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

#include <string>
#include <vector>
#include <algorithm>
#include "Clock.h"
#include "Sensors.h"
#include <FS.h>
#include <SPIFFS.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>

namespace Schedule {

class Schedule
{
public:
    Schedule(Clock::TimeOfDay when,Sensors::Weight goalAmmount)
                : when_(when)
          , goalAmmount_(goalAmmount)
    {
        Schedule_.push_back(this);
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
    static bool ScheduleScreen();
    static void ScheduleScreenStart();
    static void CheckForFeeding();
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
private:
    Clock::TimeOfDay when_;
    Sensors::Weight goalAmmount_;
    static std::vector<Schedule *> Schedule_;
    static const char schedfile_[];
};

}

#define DECLARESCHEDULE std::vector<Schedule::Schedule *> Schedule::Schedule::Schedule_

#endif // __SCHEDULE_H

