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
//  Last Modified : <240817.1634>
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
#include "Robot1-110.h"

namespace FeedWebServer {

static FeedWebServer server;
DEFINE_SINGLETON_INSTANCE(FeedWebServer);

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
        snprintf(buffer,sizeof(buffer),"<h2>Current time: %02:%02d</h2>",
                 timeinfo.tm_hour,timeinfo.tm_min);
        break;
    }
    return String(buffer);
}

void FeedWebServer::_welcome()
{
    send(200, "text/html", 
         header_("Smart Cat Feeder") + 
         "<h1>Smart Cat Feeder</h1>" +
         currentTime() +
         footer_());
    
}

void FeedWebServer::_notFound()
{
    send(404, "text/html", 
         header_("File Not Found") + 
         "<h1>File Not Found</h1>" +
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

void FeedWebServer::_sendRobot1_110()
{
    uint8_t buffer[base64_decode_expected_len(sizeof(ROBOT1_110))];
    int status = base64_decode_chars(ROBOT1_110,sizeof(ROBOT1_110),(char *)buffer);
    send(200,"image/png",String((const char *)buffer));
}

    

}
