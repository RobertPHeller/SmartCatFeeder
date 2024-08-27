// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Tue Aug 27 09:57:16 2024
//  Last Modified : <240827.1020>
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
/// @file BackgroundTask.h
/// @author Robert Heller
/// @date Tue Aug 27 09:57:16 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __BACKGROUNDTASK_H
#define __BACKGROUNDTASK_H

#include <vector>

class BackgroundTask
{
public:
    
    BackgroundTask()
    {
        addTask(this);
    }
    ~BackgroundTask()
    {
        removeTask(this);
    }
    virtual void RunTask() = 0;
    static void RunTasks(int sleepMillis);
private:
    typedef std::vector<BackgroundTask *> TaskVector;
    static TaskVector taskVector_;
    static void addTask(BackgroundTask *task);
    static void removeTask(BackgroundTask *task);
};

#endif // __BACKGROUNDTASK_H

