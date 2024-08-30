// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 21:31:26 2024
//  Last Modified : <240829.1550>
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
/// @file FeedWebServer.h
/// @author Robert Heller
/// @date Fri Aug 16 21:31:26 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __FEEDWEBSERVER_H
#define __FEEDWEBSERVER_H

#include <WebServer.h>
#include "Singleton.h"
#include "BackgroundTask.h"


namespace FeedWebServer {

class FeedWebServer : public BackgroundTask, public WebServer, public Singleton<FeedWebServer>
{
public:
    FeedWebServer() \
                : WebServer(80)
    , BackgroundTask()
    {
    }
    static void StartServer()
    {
        instance()->_startServer();
    }
    virtual void RunTask()
    {
        handleClient();
    }
private:
    void _startServer()
    {
        on("/", MainScreen);
        on("/style.css", SendStyle);
        on("/javascript.js", SendJavaScript);
        on("/Robot1-110.png", SendRobot1_110);
        on("/icons8-gear-50.png", SendIcons8_gear_50);
        on("/icons8-clock-50.png", SendIcons8_clock_50);
        on("/icons8-hand-50.png", SendIcons8_hand_50);
        on("/settings", Settings);
        on("/schedule", Schedule);
        on("/manual", Manual);
        onNotFound(NotFound);
        begin();
    }
    static void MainScreen() {instance()->_MainScreen();}
    void _MainScreen();
    static void NotFound() {instance()->_notFound();}
    void _notFound();
    static void SendStyle() {instance()->_sendStyle();}
    void _sendStyle();
    static void SendJavaScript() {instance()->_sendJavaScript();}
    void _sendJavaScript();
    static void SendRobot1_110() {instance()->_sendRobot1_110();}
    void _sendRobot1_110();
    static void SendIcons8_gear_50() {instance()->_SendIcons8_gear_50();}
    void _SendIcons8_gear_50();
    static void SendIcons8_clock_50() {instance()->_SendIcons8_clock_50();}
    void _SendIcons8_clock_50();
    static void SendIcons8_hand_50() {instance()->_SendIcons8_hand_50();}
    void _SendIcons8_hand_50();
    static void Settings() {instance()->_Settings();}
    void _Settings();
    static void Schedule() {instance()->_Schedule();}
    void _Schedule();
    static void Manual() {instance()->_Manual();}
    void _Manual();
    String header_(String title);
    String footer_();
};



}

#endif // __FEEDWEBSERVER_H

