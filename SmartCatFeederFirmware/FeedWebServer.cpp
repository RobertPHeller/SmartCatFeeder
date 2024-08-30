// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 21:32:10 2024
//  Last Modified : <240829.2042>
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
/// @file FeedWebServer.cpp
/// @author Robert Heller
/// @date Fri Aug 16 21:32:10 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";

#include <time.h>
#include <esp_sntp.h>
#include <WebServer.h>
#include <libb64/cdecode.h>
#include "Singleton.h"
#include "Preferences.h"
#include "FeedWebServer.h"
#include "Revision.h"
#include "MainScreen.h"


namespace FeedWebServer {

static FeedWebServer server;
DEFINE_SINGLETON_INSTANCE(FeedWebServer);


void FeedWebServer::_MainScreen()
{
    send(200, "text/html", 
         header_("Smart Cat Feeder") + 
         "<h1>Smart Cat Feeder</h1>" +
         MainScreen::MainScreen::instance()->Page() +
         footer_());
    
}

void FeedWebServer::_notFound()
{
    send(404, "text/html", 
         header_("File Not Found") + 
         "<h1>File Not Found</h1>" +
         footer_());
    
}

void FeedWebServer::_Settings()
{
    send(200, "text/html",
         header_("Settings Management") +
         "<h1>Settings Management</h1>" +
         Preferences::Preferences::instance()->SettingsPage(this) +
         footer_());
}

void FeedWebServer::_Schedule()
{
    send(200, "text/html",
         header_("Schedule Management") +
         "<h1>Schedule Management</h1>" +
         // Schedule::ScheduleManagement::instance()->ScheduleManagementPage(this) +
         footer_());
}

void FeedWebServer::_Manual()
{
    send(200, "text/html",
         header_("Manual Feeding") +
         "<h1>Manual Feeding</h1>" +
         // Mechanical::FeedMotors::instance()->ManualFeedingPage(this<) +
         footer_());
}



void FeedWebServer::_sendStyle()
{
    send(200, "text/css", R"stylesheet(
body { 
background-color: #cccccc;
font-family: Arial, Helvetica, Sans-Serif;
Color: #000088;
}
)stylesheet");
         
}

void FeedWebServer::_sendJavaScript()
{
    send(200, "text/javascript" , R"javascript(
function dummy()
{
}
)javascript");
}

String FeedWebServer::header_(String title)
{
    return String(R"html(
<html>
  <head>
     <title>)html" + title + R"html(</title>
     <meta http-equiv="content-language" content="en" />
     <meta name="generator" content=")html" PROGRAM_NAME ":" REVISION_GIT_HASH R"html(" />
     <link rel="stylesheet" href="/style.css" type="text/css" />
     <script type="text/javascript" src="/javascript.js" />
  </head>
  <body>)html");
}
String FeedWebServer::footer_()
{
    return String(R"html(
   <footer id="colophon" class="site-footer" role="contentinfo">
     <p><img src="/Robot1-110.png" width="63" height="110" alt="Country Robot" style="float:left;" />&copy; 2024 Robert Heller D/B/A Deepwoods Software (The Country Robot)</p>
   </footer>
  </body>
</html>)html");
}

#include "Robot1-110.h"
void FeedWebServer::_sendRobot1_110()
{
    uint8_t buffer[base64_decode_expected_len(sizeof(ROBOT1_110))];
    int status = base64_decode_chars(ROBOT1_110,sizeof(ROBOT1_110),(char *)buffer);
    send(200,"image/png",String((const char *)buffer));
}
#include "icons8-gear-50.png.h"
void FeedWebServer::_SendIcons8_gear_50()
{
    uint8_t buffer[base64_decode_expected_len(sizeof(ICONS8GEAR50))];
    int status = base64_decode_chars(ICONS8GEAR50,sizeof(ICONS8GEAR50),(char *)buffer);
    send(200,"image/png",String((const char *)buffer));
}
#include "icons8-clock-50.png.h"
void FeedWebServer::_SendIcons8_clock_50()
{
    uint8_t buffer[base64_decode_expected_len(sizeof(ICONS8CLOCK50))];
    int status = base64_decode_chars(ICONS8CLOCK50,sizeof(ICONS8CLOCK50),(char *)buffer);
    send(200,"image/png",String((const char *)buffer));
}
#include "icons8-hand-50.png.h"
void FeedWebServer::_SendIcons8_hand_50()
{
    uint8_t buffer[base64_decode_expected_len(sizeof(ICONS8HAND50))];
    int status = base64_decode_chars(ICONS8HAND50,sizeof(ICONS8HAND50),(char *)buffer);
    send(200,"image/png",String((const char *)buffer));
}
    

}
