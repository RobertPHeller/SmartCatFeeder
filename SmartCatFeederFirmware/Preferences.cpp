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
//  Last Modified : <240827.0950>
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

#include "Preferences.h"
#include "Display.h"

namespace Preferences {

Preferences::SettingsButton::SettingsButton(ScreenMode next, Adafruit_GFX *gfx,
                                            int16_t x, int16_t y, uint16_t w, 
                                            uint16_t h, uint16_t outline,
                                            uint16_t fill, uint16_t textcolor, 
                                            const char *label, 
                                            uint8_t textsize)
      : _next(next)
, _gfx(gfx)
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



void Preferences::displayAllSettings_()
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
}

void Preferences::waitformainselection_()
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
            delay(100);
        }
    }
    else
    {
        ssid_button_.press(false); // tell the button it is NOT pressed
        if (ssid_button_.justReleased())
        {
            screen_ = ssid_button_.GetNext();
        }
    }
    if (hostname_button_.contains(p.x, p.y))
    {
        hostname_button_.press(true);  // tell the button it is pressed
        if (hostname_button_.justPressed())
        {
            delay(100);
        }
    }
    else
    {
        hostname_button_.press(false); // tell the button it is NOT pressed
        if (hostname_button_.justReleased())
        {
            screen_ = hostname_button_.GetNext();
        }
    }
    if (clockfmt_button_.contains(p.x, p.y))
    {
        clockfmt_button_.press(true);  // tell the button it is pressed
        if (clockfmt_button_.justPressed())
        {
            delay(100);
        }
    }
    else
    {
        clockfmt_button_.press(false); // tell the button it is NOT pressed
        if (clockfmt_button_.justReleased())
        {
            screen_ = clockfmt_button_.GetNext();
        }
    }
    if (timeZone_button_.contains(p.x, p.y))
    {
        timeZone_button_.press(true);  // tell the button it is pressed
        if (clockfmt_button_.justPressed())
        {
            delay(100);
        }
    }
    else
    {
        timeZone_button_.press(false); // tell the button it is NOT pressed
        if (timeZone_button_.justReleased())
        {
            screen_ = clockfmt_button_.GetNext();
        }
    }
    if (return_.contains(p.x, p.y))
    {
        return_.press(true);  // tell the button it is pressed
        if (return_.justPressed())
        {
            return_.drawButton(true);
            delay(100);
        }
    }
    else
    {
        return_.press(false); // tell the button it is NOT pressed
        if (return_.justReleased())
        {
            return_.drawButton();
            screen_ = exit;
        }
    }
}

void Preferences::displayYesNo_(char const* question)
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11);
    Display::Display.println(question);
    yes_.drawButton();
    no_.drawButton();
}

int Preferences::yesnoanswer_()
{
    int result = -1;
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
            delay(100);
        }
    }
    else
    {
        yes_.press(false); // tell the button it is NOT pressed
        if (yes_.justReleased())
        {
            yes_.drawButton();
            result = 1;
        }
    }
    if (no_.contains(p.x, p.y))
    {
        no_.press(true);  // tell the button it is pressed
        if (no_.justPressed())
        {
            no_.drawButton(true);
            delay(100);
        }
    }
    else
    {
        no_.press(false); // tell the button it is NOT pressed
        if (no_.justReleased())
        {
            no_.drawButton();
            result = 0;
        }
    }
    return result;
}

#include "lock.xbm.h"

void Preferences::displayWiFissids_()
{
    Display::Display.fillScreen(HX8357_BLACK);
    Display::Display.fillRect(10,10,300,42,HX8357_WHITE);
    Display::Display.setTextColor(HX8357_BLUE,HX8357_WHITE);
    Display::Display.setTextSize(5);
    Display::Display.setCursor(11,11); 
    Display::Display.println("Networks:");
    Display::Display.setTextColor(HX8357_GREEN,HX8357_WHITE);
    for (int i=0; i<8; i++)
    {
        if (i+ssid_index_ >= ssid_count_) break;
        int y = 44*i;
        Display::Display.fillRect(10,y-1,300,42,HX8357_WHITE);
        Display::Display.setCursor(11,y);
        Display::Display.print(WiFi.SSID(i+ssid_index_).c_str());
        if (WiFi.encryptionType(i+ssid_index_) != WIFI_AUTH_OPEN)
        {
            Display::Display.drawXBitmap(270,y,lock_bits,lock_width,
                                         lock_height,HX8357_GREEN);
        }
    }
    if (ssid_index_ > 0)
    {
        previous_.drawButton();
    }
    if (ssid_index_+8 < ssid_count_)
    {
        next_.drawButton();
    }
    return_.drawButton();
}

int Preferences::select_ssid_from_list_()
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
    for (int i=0; i<8; i++)
    {
        if (i+ssid_index_ >= ssid_count_) break;
        int y = 44*i;
        int x = 10;
        int w = 300;
        int h = 42;
        if ((p.x >= x) && (p.x < (int16_t)(x + w)) && (p.y >= y) &&
            p.y < (int16_t)(y + h))
        {
            return i;
        }
    }
    bool havePrev = ssid_index_ > 0;
    bool haveNext = (ssid_index_+8) < ssid_count_;
    if (havePrev)
    {
        if (previous_.contains(p.x, p.y))
        {
            previous_.press(true);  // tell the button it is pressed
            if (previous_.justPressed())
            {
                previous_.drawButton(true);
                delay(100);
            }
        }
        else
        {
            previous_.press(false); // tell the button it is NOT pressed
            if (previous_.justReleased())
            {
                previous_.drawButton();
                ssid_index_ -= 8;
                if (ssid_index_ < 0) ssid_index_ = 0;
                screen_ = displaySSIDs;
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
                delay(100);
            }
        }
        else
        {
            next_.press(false); // tell the button it is NOT pressed
            if (next_.justReleased())
            {
                next_.drawButton();
                ssid_index_ += 8;
                screen_ = displaySSIDs;
            }
        }
    }
    if (return_.contains(p.x, p.y))
    {
        return_.press(true);  // tell the button it is pressed
        if (return_.justPressed())
        {
            return_.drawButton(true);
            delay(100);
        }
    }
    else
    {
        return_.press(false); // tell the button it is NOT pressed
        if (return_.justReleased())
        {
            return_.drawButton();
            screen_ = start;
        }
    }
    return -1;
}

void Preferences::set_ssid_(int rel_ssid_index)
{
}


bool Preferences::SettingsScreen()
{
    switch (screen_)
    {
    case start:
        displayAllSettings_();
        screen_ = waitformainselection;
    case waitformainselection:
        waitformainselection_();
        break;
    case ssid:
        if (WiFi.status() == WL_CONNECTED)
        {
            displayYesNo_("Disconnect network?");
            screen_ = disconnectYesNo;
            return true;
        }
        else
        {
            ssid_count_ = WiFi.scanNetworks();
            ssid_index_ = 0;
            screen_ = displaySSIDs;
            return true;
        }
        break;
    case displaySSIDs:
        displayWiFissids_();
        screen_ = selectSSID;
        return true;
    case disconnectYesNo:
        switch (yesnoanswer_())
        {
        case -1:
            break;
        case 0:
            screen_ = start;
            break;
        case 1:
            WiFi.mode(WIFI_STA);
            WiFi.disconnect();
            delay(100);
            screen_ = ssid;
            break;
        }
        break;
    case selectSSID:
        {
            int selected = select_ssid_from_list_();
            if (selected >= 0)
            {
                set_ssid_(ssid_index_+selected);
            }
        }
        break;
    case getpassword:
        break;
    case saveandconnectYesNo:
        switch (yesnoanswer_())
        {
        case -1:
            break;
        case 0:
            screen_ = start;
            break;
        case 1:
            // save prefs and connect...
            break;
        }
        break;
    case hostname:
        break;
    case clockfmt:
        break;
    case timezone:
        break;
    case exit:
        return false;
        break;
    }
    return true;
}

void Preferences::SettingsScreenStart()
{
    screen_ = start;
    Display::Display.fillScreen(HX8357_BLACK);
}



}
 
