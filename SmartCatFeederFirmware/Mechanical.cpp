// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 16:27:29 2024
//  Last Modified : <240929.1250>
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
/// @file Mechanical.cpp
/// @author Robert Heller
/// @date Fri Aug 16 16:27:29 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include <Adafruit_MotorShield.h>
#include <Adafruit_GFX.h>
#include <Adafruit_HX8357.h>
#include <Adafruit_TSC2007.h>
#include "Display.h"
#include "Sensors.h"
#include "Singleton.h"
#include "Mechanical.h"
#include "Spinbox.h"

namespace Mechanical {

static Adafruit_MotorShield motorshield;
static FeedMotors motors;

void Initialize()
{
    if (!motorshield.begin())
    {
        Display::PrintError("Could not find Motor Shield. Check wiring.");
        while (1) delay(100);
    }
}

FeedMotors::FeedMotors()
      : BackgroundTask()
, feedMotor_(motorshield.getMotor(1))
, agitatorMotor_(motorshield.getMotor(3))
, running_(false)
,  _ounces(&Display::Display,10,52+52,HX8357_WHITE,HX8357_BLACK,
           HX8357_BLUE,1,8,"%d")
{
    return_.initButtonUL(&Display::Display,10,278,300,42,
                         HX8357_WHITE,HX8357_BLACK,HX8357_BLUE,
                         "Return",5);
    feed_.initButtonUL(&Display::Display,210,236,100,42,
                       HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                       "Feed",5);
}

void FeedMotors::RunTask()
{
    if (! running_) return;
    if (Sensors::BowlAmmount() >= goalAmmount_)
    {
        stop_();
    }
}

void FeedMotors::start_()
{
    if (running_) return;
    feedMotor_->setSpeed(255);
    feedMotor_->run(FORWARD);
    feedMotor_->run(RELEASE);
    agitatorMotor_->setSpeed(255);
    agitatorMotor_->run(FORWARD);
    agitatorMotor_->run(RELEASE);
    running_ = true;
}

void FeedMotors::stop_()
{
    if (! running_) return;
    feedMotor_->setSpeed(0);
    feedMotor_->run(RELEASE);
    agitatorMotor_->setSpeed(0);
    agitatorMotor_->run(RELEASE);
    running_ = false;
}

void FeedMotors::StartFeeding(Sensors::Weight goalAmmount)
{
    if (running_) return;
    goalAmmount_ = goalAmmount;
    if (Sensors::BowlAmmount() < goalAmmount_)
    {
        start_();
    }
}

void FeedMotors::ManualFeed()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5); 
    Display::Display.setCursor(11,11);
    Display::Display.println("Feed Ammount");
    _ounces.drawBox(1);
    Display::Display.setCursor(84,52+52);
    Display::Display.setTextColor(HX8357_BLUE);
    Display::Display.setTextSize(5,5);
    Display::Display.print(" ounces");
    feed_.drawButton();
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
        _ounces.processAt(p.x,p.y);
        if (feed_.contains(p.x, p.y))
        {
            feed_.press(true);  // tell the button it is pressed
            if (feed_.justPressed())
            {
                feed_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            feed_.press(false); // tell the button it is NOT pressed
            if (feed_.justReleased())
            {
                feed_.drawButton();
                StartFeeding(_ounces.Value());
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

String FeedMotors::ManualFeedingPage(WebServer *server,int &code)
{
    if (server->hasArg("feed"))
    {
        Sensors::Weight goal = atoi(server->arg("goal").c_str());
        if (goal > 0 && goal <= 8)
        {
            StartFeeding(goal);
            server->sendHeader("Location:", "/");
            code = 301;
            return "<p>The document has moved <a href='/'>here</a></p>";
        }
    }
    code = 200;
    String result("<form method='post' action='/manual' >\n");
    result += "<ul style='list-style-type: none;'>\n";
    result += "<input id='ammount' type='number' name='goal' value='1' min='1' max='8' />";
    result += "<button type='submit' name='feed' value='1'>Feed</button></li>";
    result += "</ul></form>";
    result += "<a href='/'>Back to Home</a>";
    return result;
}

}
