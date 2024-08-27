// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Tue Aug 27 10:04:30 2024
//  Last Modified : <240827.1022>
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
/// @file BackgroundTask.cpp
/// @author Robert Heller
/// @date Tue Aug 27 10:04:30 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include <vector>
#include <algorithm>
#include "BackgroundTask.h"

void BackgroundTask::RunTasks(int sleepMillis)
{
    for (auto it=taskVector_.begin(); it != taskVector_.end(); it++)
    {
        (*it)->RunTask();
    }
    delay(sleepMillis);
}

BackgroundTask::TaskVector BackgroundTask::taskVector_;

void BackgroundTask::addTask(BackgroundTask *task)
{
    taskVector_.push_back(task);
}

void BackgroundTask::removeTask(BackgroundTask *task)
{
    auto it = std::find(taskVector_.begin(),taskVector_.end(),task);
    if (it != taskVector_.end())
    {
        taskVector_.erase(it);
    }
}

