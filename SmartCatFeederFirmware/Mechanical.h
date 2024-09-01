// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Thu Aug 15 15:04:21 2024
//  Last Modified : <240831.2033>
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
/// @file Mechanical.h
/// @author Robert Heller
/// @date Thu Aug 15 15:04:21 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __MECHANICAL_H
#define __MECHANICAL_H

#include <Arduino.h>
#include <Adafruit_MotorShield.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <WebServer.h>
#include "Sensors.h"
#include "Singleton.h"
#include "BackgroundTask.h"
#include "Spinbox.h"

namespace Mechanical {

extern void Initialize();

class FeedMotors : public BackgroundTask, public Singleton<FeedMotors>
{
public:
    FeedMotors();
    virtual void RunTask();
    void StartFeeding(Sensors::Weight goalAmmount);
    void ManualFeed();
    String ManualFeedingPage(WebServer *webserver, int &code);
private:
    void start_();
    void stop_();
    Adafruit_DCMotor *feedMotor_;
    Adafruit_DCMotor *agitatorMotor_;
    Sensors::Weight goalAmmount_;
    bool running_;
    Spinbox _ounces;
    Adafruit_GFX_Button return_;
    Adafruit_GFX_Button feed_;
};

}

#endif // __MECHANICAL_H

