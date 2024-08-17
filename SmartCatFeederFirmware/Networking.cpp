// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 16:24:16 2024
//  Last Modified : <240816.2130>
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
/// @file Networking.cpp
/// @author Robert Heller
/// @date Fri Aug 16 16:24:16 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";


#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <time.h>
#include <esp_sntp.h>
#include <Adafruit_HX8357.h>

#include "Preferences.h"
#include "Clock.h"
#include "Display.h"
#include "Networking.h"

namespace Networking {

void Initialize()
{
    sntp_set_time_sync_notification_cb(Clock::timeavailable);
    sntp_servermode_dhcp(1);
    const char *ssid = Preferences::Preferences::instance()->GetSSID();
    const char *password = Preferences::Preferences::instance()->GetPassword();
    if (strlen(ssid) > 0)
    {
        Display::Display.setTextSize(3);
        Display::Display.setTextColor(HX8357_WHITE);
        Display::Display.printf("Connecting to %s ", ssid);
        WiFi.begin(ssid, password);
        for (int i = 0; i < 120; i++)
        {
            if (WiFi.status() == WL_CONNECTED) break;
            delay(500);
            Display::Display.print(".");
        }
        if (WiFi.status() != WL_CONNECTED) {
            Display::Display.println("");
            Display::PrintError("Not Connected: Network not initialized.");
            return;
        }
        Display::Display.println("");
        Display::Display.print("Connected to ");
        Display::Display.println(ssid);
        Display::Display.print("IP address: ");
        Display::Display.println(WiFi.localIP());
        const char *hostname = Preferences::Preferences::instance()->GetHostname();
        if (!MDNS.begin(hostname))
        {
            Display::PrintError("Error setting up MDNS responder!");
            return;
        }
        Display::Display.println("mDNS responder started");
        
    }
}

}
