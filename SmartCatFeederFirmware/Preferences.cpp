// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sat Aug 24 20:25:43 2024
//  Last Modified : <240830.1324>
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
/// @file Preferences.cpp
/// @author Robert Heller
/// @date Sat Aug 24 20:25:43 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";


#include <string>
#include <FS.h>
#include <SPIFFS.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <WiFi.h>
#include <ESPmDNS.h>

#include "BackgroundTask.h"
#include "Preferences.h"
#include "Display.h"
#include "FeedWebServer.h"

namespace Preferences {

Preferences::SettingsButton::SettingsButton(Adafruit_GFX *gfx,
                                            int16_t x, int16_t y, uint16_t w, 
                                            uint16_t h, uint16_t outline,
                                            uint16_t fill, uint16_t textcolor, 
                                            const char *label, 
                                            uint8_t textsize)
      : _gfx(gfx)
, _x1(x)
, _y1(y)
, _w(w)
, _h(h)
, _textsize_x(textsize)
, _textsize_y(textsize)
, _outlinecolor(outline)
, _fillcolor(fill)
, _textcolor(textcolor)
{
    strncpy(_label,label,29);
    _label[29] = '\0';
    
}

void Preferences::SettingsButton::drawButton(const char * value,
                                             const char *message,
                                             bool inverted)
{
    uint16_t fill, outline, text;
    
    if (!inverted) {
        fill = _fillcolor;
        outline = _outlinecolor;
        text = _textcolor;
    } else {
        fill = _textcolor;
        outline = _outlinecolor;
        text = _fillcolor;
    }
    
    uint8_t r = min(_w, _h) / 4; // Corner radius
    _gfx->fillRoundRect(_x1, _y1, _w, _h, r, fill);
    _gfx->drawRoundRect(_x1, _y1, _w, _h, r, outline);
    
    _gfx->setCursor(_x1 + 2, _y1 + 2);
    _gfx->setTextColor(text);
    _gfx->setTextSize(_textsize_x, _textsize_y);
    _gfx->println(_label);
    _gfx->setCursor(_x1 + 2, _gfx->getCursorY());
    _gfx->println(value);
    if (message)
    {
        _gfx->setCursor(_x1 + 2, _gfx->getCursorY());
        _gfx->print(message);
    }
}

bool Preferences::SettingsButton::contains(int16_t x, int16_t y)
{
    return ((x >= _x1) && (x < (int16_t)(_x1 + _w)) && (y >= _y1) &&
            (y < (int16_t)(_y1 + _h)));
}

bool Preferences::SettingsButton::justPressed()
{
    return (currstate && !laststate);
}

bool Preferences::SettingsButton::justReleased()
{
    return (!currstate && laststate);
}

void Preferences::Settings()
{
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println("Settings:");
    ssid_button_.drawButton(ssid_.c_str(),(WiFi.status() == WL_CONNECTED)?"Connected":"Not Connected");
    hostname_button_.drawButton(hostname_.c_str());
    switch (clockFormat_)
    {
    case Twelve:
        clockfmt_button_.drawButton("Twelve Hour");
        break;
    case TwentyFour:
        clockfmt_button_.drawButton("Twenty Four Hour");
        break;
    }
    timeZone_button_.drawButton(timeZone_.c_str());
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
        if (ssid_button_.contains(p.x, p.y))
        {
            ssid_button_.press(true);  // tell the button it is pressed
            if (ssid_button_.justPressed()) 
            {
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            ssid_button_.press(false); // tell the button it is NOT pressed
            if (ssid_button_.justReleased())
            {
                ssidScreen();
            }
        }
        if (hostname_button_.contains(p.x, p.y))
        {
            hostname_button_.press(true);  // tell the button it is pressed
            if (hostname_button_.justPressed())
            {
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            hostname_button_.press(false); // tell the button it is NOT pressed
            if (hostname_button_.justReleased())
            {
                hostnameScreen();
        }
        }
        if (clockfmt_button_.contains(p.x, p.y))
        {
            clockfmt_button_.press(true);  // tell the button it is pressed
            if (clockfmt_button_.justPressed())
            {
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            clockfmt_button_.press(false); // tell the button it is NOT pressed
            if (clockfmt_button_.justReleased())
            {
                clockFormatScreen();
            }
        }
        if (timeZone_button_.contains(p.x, p.y))
        {
        timeZone_button_.press(true);  // tell the button it is pressed
            if (clockfmt_button_.justPressed())
            {
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            timeZone_button_.press(false); // tell the button it is NOT pressed
            if (timeZone_button_.justReleased())
            {
                timeZoneScreen();
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
                break;
            }
        }
        
    }
}    

static bool AllowedMode(String mode)
{
    if (mode == "ssid") return true;
    if (mode == "hostname") return true;
    if (mode == "clockfmt") return true;
    if (mode == "timezone") return true;
    return false;
}

String Preferences::SettingsPage(WebServer *webserver)
{
    char buffer[256];
    String result("<form method='post' action='/settings' >\n");
    String mode = webserver->arg("setting");
    result += "<ul style='list-style-type: none;'>\n";
    if (mode == "ssid")
    {
        if ( webserver->hasArg("update") )
        {
            SetSSID(webserver->arg("newssid").c_str());
            SetPassword(webserver->arg("newpassword").c_str());
            Write();
        }
        result += "<li><label for='ssid'>Network name:</label>\n";
        result += "<input type='text' id='ssid' name='newssid' size='25' /></li>\n";
        result += "<li><label for='password'>Password (leave blank for none):</label>\n";
        result += "<input type='password' id='password' name='newpassword' size='25' /></li>\n";
        
    }
    else if (mode == "hostname")
    {
        if ( webserver->hasArg("update") )
        {
            SetHostname(webserver->arg("newhostname").c_str());
            Write();
        }
        result += "<input type='hidden' name='setting' value='hostname' />\n";
        result += "<li><label for='hostname'>Hostname:</label>\n";
        result += "<input type='text' id='hostname' name='newhostname' size='25' /></li>\n";\
    }
    else if (mode == "clockfmt")
    {
        if ( webserver->hasArg("update") )
        {
            SetClockFormat((ClockFormat)atoi(webserver->arg("clockformat").c_str()));
            Write();
        }
        result += "<input type='hidden' name='setting' value='clockfmt' />\n";
        result += "<li><label for='clockfmt'>Clock format:</label>\n";
        result += "<select name='clockformat' id='clockfmt.>\n";
        snprintf(buffer,sizeof(buffer),
                 "<option value='%d' %s>12 Hour</option>\n",
                 (int)Twelve,(GetClockFormat() == Twelve)?"selected":"");
        result += buffer;
        snprintf(buffer,sizeof(buffer),
                 "<option value='%d' %s>24 Hour</option>\n",
                 (int)TwentyFour,(GetClockFormat() == TwentyFour)?"selected":"");
        result += buffer;
        result += "</select></li>\n";
    }
    else if (mode == "timezone")
    {
        if ( webserver->hasArg("update") )
        {
            SetTimeZone(webserver->arg("timezone").c_str());
            Write();
        }
        result += "<input type='hidden' name='setting' value='timezone' />\n";
        result += "<li><label for='tz'>Time Zone:</label>\n";
        result += "<select name='timezone' id='tz'>\n";
        for (size_t i = 0; i < LISTSIZE; i++)
        {
            snprintf(buffer,sizeof(buffer),
                     "<option value='%s' %s>%s</option>\n",
                     TimeZoneList_[i].value,
                     (strcmp(TimeZoneList_[i].value,GetTimeZone()) == 0)?"selected":"",
                     TimeZoneList_[i].name);
            result += buffer;
        }
        result += "</select></li>\n";
    }
    else
    {
    
        result += "<li><button type='submit' name='setting' value='ssid'>";
        result += ssid_.c_str();
        result += "</button></li>\n";
        result += "<li><button type='submit' name='setting' value='hostname'>";
        result += hostname_.c_str();
        result += "</button></li>\n";
        result += "<li><button type='submit' name='setting' value='clockfmt'>";
        switch (clockFormat_)
        {
        case Twelve:
            result += "12 Hour";
            break;
        case TwentyFour:
            result += "24 Hour";
            break;
        }
        result += "</button></li>\n";
        result += "<li><button type='submit' name='setting' value='timezone'>";
        result += timeZone_.c_str();
        result += "</button></li>\n";
    }
    result += "</ul>\n";
    if (AllowedMode(mode))
    {
        result += "<input type='hidden' name='setting' value='" + mode + 
              "' />\n";
        result += "<button type='submit' name='update' value='true'>Update</button>\n";
    }
    result += "</form>\n";
    result += "<a href='/'>Back to Home</a>&nbsp; <a href='/settings'>Back to Settings</a>";
    return result;
}

void Preferences::ssidScreen()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        if (displayYesNo_("Disconnect network?"))
        {
            WiFi.mode(WIFI_STA);
            WiFi.disconnect();
            BackgroundTask::RunTasks(100);
        }
        else
        {
            return;
        }
    }
    int netCount = WiFi.scanNetworks();
    int first = 0;
    displayWiFissids_(first,netCount);
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
        for (int i=0; i<LISTSIZE; i++)
        {
            if (i+first >= netCount) break;
            int y = 52+(44*i);
            int x = 10;
            int w = 300;
            int h = 42;
            if ((p.x >= x) && (p.x < (int16_t)(x + w)) && (p.y >= y) &&
                p.y < (int16_t)(y + h))
            {
                listPress(i,true);
                if (listJustPressed(i))
                {
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                listPress(i,false);
                if (listJustReleased(i))
                {
                    ssidSelected(i+first);
                    return;
                }
            }
        }
        bool havePrev = first > 0;
        bool haveNext = (first+LISTSIZE) <netCount;
        if (havePrev)
        {
            if (previous_.contains(p.x, p.y))
            {
                previous_.press(true);  // tell the button it is pressed
                if (previous_.justPressed())
                {
                    previous_.drawButton(true);
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                previous_.press(false); // tell the button it is NOT pressed
                if (previous_.justReleased())
                {
                    previous_.drawButton();
                    first -= LISTSIZE;
                    if (first < 0) first = 0;
                    displayWiFissids_(first,netCount);
                }
            }
        }
        if (haveNext)
        {
            if (next_.contains(p.x, p.y))
            {
                next_.press(true);  // tell the button it is pressed
                if (next_.justPressed())
                {
                    next_.drawButton(true);
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                next_.press(false); // tell the button it is NOT pressed
                if (next_.justReleased())
                {
                    next_.drawButton();
                    first += LISTSIZE;
                    displayWiFissids_(first,netCount);
                }
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

bool Preferences::displayYesNo_(char const* question)
{
    Display::Display.fillRect(0,160,480,160,HX8357_BLACK);
    Display::Display.fillRect(10,161,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println(question);
    yes_.drawButton();
    no_.drawButton();
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
        if (yes_.contains(p.x, p.y))
        {
            yes_.press(true);  // tell the button it is pressed
        if (yes_.justPressed())
        {
            yes_.drawButton(true);
            BackgroundTask::RunTasks(100);
        }
        }
        else
        {
            yes_.press(false); // tell the button it is NOT pressed
            if (yes_.justReleased())
            {
                yes_.drawButton();
                return(true);
            }
        }
        if (no_.contains(p.x, p.y))
        {
            no_.press(true);  // tell the button it is pressed
            if (no_.justPressed())
            {
                no_.drawButton(true);
                BackgroundTask::RunTasks(100);
            }
        }
        else
        {
            no_.press(false); // tell the button it is NOT pressed
            if (no_.justReleased())
            {
                no_.drawButton();
                return(false);
            }
        }
    }
}


#include "lock.xbm.h"

void Preferences::displayWiFissids_(int first, int count)
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Networks:");
    Display::Display.setTextColor(HX8357_GREEN,HX8357_WHITE);
    for (int i=0; i<LISTSIZE; i++)
    {
        if (i+first >= count) break;
        int y = (44*i)+52;
        Display::Display.fillRect(10,y-1,300,42,HX8357_WHITE);
        Display::Display.setCursor(11,y);
        Display::Display.print(WiFi.SSID(i+first).c_str());
        if (WiFi.encryptionType(i+first) != WIFI_AUTH_OPEN)
        {
            Display::Display.drawXBitmap(270,y,lock_bits,lock_width,
                                         lock_height,HX8357_GREEN);
        }
    }
    if (first > 0)
    {
        previous_.drawButton();
    }
    if (first+LISTSIZE < count)
    {
        next_.drawButton();
    }
    return_.drawButton();
}

void Preferences::ssidSelected(int selected)
{
    char ssid_buffer[64];
    char password_buffer[64];
    strncpy(ssid_buffer,WiFi.SSID(selected).c_str(),63);
    ssid_buffer[63] = '\0';
    password_buffer[0] = '\0'; // assume no password
    if (WiFi.encryptionType(selected) != WIFI_AUTH_OPEN)
    {
        ssidGetPassword(ssid_buffer,password_buffer,64);
    }
    if (displayYesNo_("Save and connect?"))
    {
        SetSSID(ssid_buffer);
        SetPassword(password_buffer);
        Write();
        WiFi.begin(GetSSID(),GetPassword());
        for (int i = 0; i < 120; i++)
        {
            if (WiFi.status() == WL_CONNECTED) break;
            delay(500);
            Display::Display.print(".");
        }
        Display::Display.println("");
        if (WiFi.status() != WL_CONNECTED) {
            Display::PrintError("Not Connected: Network not initialized.");
            return;
        }
        Display::Display.print("Connected to ");
        Display::Display.println(GetSSID());
        Display::Display.print("IP address: ");
        Display::Display.println(WiFi.localIP());
        if (!MDNS.begin(GetHostname()))
        {
            Display::PrintError("Error setting up MDNS responder!");
            return;
        }
        Display::Display.println("mDNS responder started");
        FeedWebServer::FeedWebServer::StartServer();
        // Add service to MDNS-SD
        MDNS.addService("http", "tcp", 80);
    }        
}

void Preferences::ssidGetPassword(const char *ssid,char *passwordBuffer,
                                  size_t bufferSize)
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42*2,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println(ssid);
    Display::Display.setCursor(11,Display::Display.getCursorY());
    keyboard.start();
    char c, *p = passwordBuffer;
    *passwordBuffer = '\0';
    while ((c=keyboard.KeyPressed()) != '\r')
    {
        if (bufferSize<2) break;
        if (c == '\b')
        {
            if (p > passwordBuffer)
            {
                *--p = '\0';
                bufferSize++;
                Display::Display.setCursor(Display::Display.getCursorX()-5*6,
                                           Display::Display.getCursorY());
                Display::Display.drawChar(Display::Display.getCursorX(),
                                          Display::Display.getCursorY(),
                                          ' ',
                                          HX8357_BLUE,HX8357_WHITE,5,5);
            }
        }
        else
        {
            *p++ = c;
            bufferSize--;
            Display::Display.print(c);
        }
    }
    *p = '\0';
    keyboard.end();
}

void Preferences::hostnameScreen()
{
    char hostname_buffer[64];
    char c, *p = hostname_buffer;
    size_t bufferSize=sizeof(hostname_buffer);
    
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println("Hostname:");
    keyboard.start();
    *p = '\0';
    while ((c=keyboard.KeyPressed()) != '\r')
    {
        if (bufferSize<2) break;
        if (c == '\b')
        {
            if (p > hostname_buffer)
            {
                *--p = '\0';
                bufferSize++;
                Display::Display.setCursor(Display::Display.getCursorX()-5*6,
                                           Display::Display.getCursorY());
                Display::Display.drawChar(Display::Display.getCursorX(),
                                          Display::Display.getCursorY(),
                                          ' ',
                                          HX8357_BLUE,HX8357_WHITE,5,5);
            }
        }
        else
        {
            *p++ = c;
            bufferSize--;
            Display::Display.print(c);
        }
    }
    *p = '\0';
    keyboard.end();
    
}

void Preferences::clockFormatScreen()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE); 
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println("Clock Format");
    Twelve_.drawButton(clockFormat_==Twelve);
    TwentyFour_.drawButton(clockFormat_==TwentyFour);
    Apply_.drawButton();
    return_.drawButton();
    ClockFormat newClockFormat = clockFormat_;
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
        if (Twelve_.contains(p.x,p.y))
        {
            newClockFormat = Twelve;
            Twelve_.drawButton(true);
            TwentyFour_.drawButton(false);
        }
        if (TwentyFour_.contains(p.x,p.y))
        {
            newClockFormat = TwentyFour;
            Twelve_.drawButton(false);
            TwentyFour_.drawButton(true);
        }
        if (Apply_.contains(p.x, p.y))
        {
            Apply_.press(true);  // tell the button it is pressed
            if (Apply_.justPressed())
            {
                BackgroundTask::RunTasks(100); 
            }
        }
        else
        {
            Apply_.press(false); // tell the button it is NOT pressed
            if (Apply_.justReleased())
            {
                if (clockFormat_ != newClockFormat)
                {
                    clockFormat_ = newClockFormat;
                    Write();
                    return;
                }
            }
        }
        if (return_.contains(p.x, p.y))
        {
            return_.press(true);  // tell the button it is pressed
            if (return_.justPressed())
            {
                BackgroundTask::RunTasks(100); 
            }
        }
        else
        {
            return_.press(false); // tell the button it is NOT pressed
            if (return_.justReleased())
            {
                return;
            }
        }
    }
}

void Preferences::timeZoneScreen()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Time Zones:");
    Display::Display.setTextColor(HX8357_GREEN,HX8357_WHITE);
    for (int i=0; i<LISTSIZE; i++)
    {
        int y = (44*i)+52;
        Display::Display.fillRect(10,y-1,300,42,HX8357_WHITE); 
        Display::Display.setCursor(11,y);
        Display::Display.print(TimeZoneList_[i].name);
    }
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
        for (int i=0; i<LISTSIZE; i++)
        {
            int y = 52+(44*i);
            int x = 10;
            int w = 300;
            int h = 42;
            if ((p.x >= x) && (p.x < (int16_t)(x + w)) && (p.y >= y) &&
                p.y < (int16_t)(y + h))
            {
                listPress(i,true);
                if (listJustPressed(i))
                {
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                listPress(i,false);
                if (listJustReleased(i))
                {
                    if (timeZone_ == TimeZoneList_[i].value) return;
                    timeZone_ = TimeZoneList_[i].value;
                    Write();
                    return;
                }
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

const Preferences::TzEntry Preferences::TimeZoneList_[Preferences::LISTSIZE];


}
 
