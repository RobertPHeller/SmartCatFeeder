// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 08:49:55 2024
//  Last Modified : <240828.0948>
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
/// @file Preferences.h
/// @author Robert Heller
/// @date Fri Aug 16 08:49:55 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __PREFERENCES_H
#define __PREFERENCES_H

#include <string>
#include "Singleton.h"
#include <FS.h>
#include <SPIFFS.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <Adafruit_GFX.h>
#include "Keyboard.h"


namespace Preferences {



class Preferences : public Singleton<Preferences> {
public:
    enum ClockFormat {Twelve, TwentyFour};
    // Constructor: initialize to defaults.
    Preferences(const char * prefsfile)
                : ssid_("")
          , password_("")
          , hostname_("catfeeder")
          , timeZone_("EST5EDT,M3.2.0,M11.1.0")   // TZ_America_New_York
          , prefsfile_(prefsfile)
          , clockFormat_(Twelve)
          , ssid_button_(&Display::Display,10,45,300,42*3,HX8357_WHITE,
                         HX8357_BLACK,HX8357_GREEN,"Network Name:",5)
          , hostname_button_(&Display::Display,10,173,300,42*2,
                             HX8357_WHITE,HX8357_BLACK,HX8357_GREEN,
                             "Host name:",5)
          , clockfmt_button_(&Display::Display,10,259,300,42*2,
                             HX8357_WHITE,HX8357_BLACK,HX8357_GREEN,
                             "Clock Format:",5)
          , timeZone_button_(&Display::Display,10,345,300,42*2,
                             HX8357_WHITE,HX8357_BLACK,HX8357_GREEN,
                             "Time Zone:",5)
    {
        return_.initButtonUL(&Display::Display,10,278,300,42,
                             HX8357_WHITE,HX8357_BLACK,HX8357_BLUE,
                             "Return",5);
        yes_.initButtonUL(&Display::Display,35,236,100,42,
                          HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                          "Yes",5);
        no_.initButtonUL(&Display::Display,195,236,100,42,
                         HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                         "No",5);
        previous_.initButtonUL(&Display::Display,35,236,100,42,
                               HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                               "Previous",5);
        next_.initButtonUL(&Display::Display,195,236,100,42,
                           HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                           "Next",5);
        Twelve_.initButtonUL(&Display::Display,35,52,100,42,
                             HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                             "12",5);
        TwentyFour_.initButtonUL(&Display::Display,195,52,100,42,
                                 HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                                 "24",5);
        Apply_.initButtonUL(&Display::Display,35,96,300,42,
                           HX8357_WHITE,HX8357_BLACK,HX8357_MAGENTA,
                           "Apply",5);
    }
    int Read()
    {
        File file = SPIFFS.open(prefsfile_.c_str());
        if(!file) return 0; // No stored preferences, use initialized defaults.
        do {
            char buffer[256];
            size_t len = file.readBytesUntil('\n',buffer,sizeof(buffer));
            if (len > 0)
            {
                char *p1 = strchr(buffer,':');
                while (p1 <= &buffer[255] && isspace(*p1)) p1++;
                if (p1 != NULL)
                {
                    *p1++ = '\0';
                    if (strncasecmp("ssid",buffer,4) == 0)
                    {
                        ssid_ = p1;
                    } else if (strncasecmp("password",buffer,8) == 0)
                    {
                        password_ = p1;
                    } else if (strncasecmp("hostname",buffer,8) == 0)
                    {
                        hostname_ = p1;
                    } else if (strncasecmp("clockformat",buffer,11) == 0)
                    {
                        if (strncasecmp("twelve",p1,6) == 0)
                        {
                            clockFormat_ = Twelve;
                        }
                        else
                        {
                            clockFormat_ = TwentyFour;
                        }
                    } else if (strncasecmp("timezone",buffer,8) == 0)
                    {
                        timeZone_ = p1;
                    }
                }
            }
        } while (file);
        file.close();
        return 0;
    }
    int Write()
    {
        char buffer[256];
        File file = SPIFFS.open(prefsfile_.c_str(),FILE_WRITE,true);
        if(!file) return -1; // can't write/create prefs!
        snprintf(buffer,sizeof(buffer),"ssid: %s",ssid_.c_str());
        file.println(buffer);
        snprintf(buffer,sizeof(buffer),"password: %s",password_.c_str());
        file.println(buffer);
        snprintf(buffer,sizeof(buffer),"hostname: %s",hostname_.c_str());
        file.println(buffer);
        switch (clockFormat_) {
        case Twelve:
            file.println("clockformat: twelve"); break;
        case TwentyFour:
            file.println("clockformat: twentyfour"); break;
        }
        snprintf(buffer,sizeof(buffer),"timezone: %s",timeZone_.c_str());
        file.println(buffer);
        file.close();
        return 0;
    }
    const char * GetSSID() const {return ssid_.c_str();}
    void SetSSID(const char *ssid) 
    {
        ssid_ = ssid;
    }
    const char * GetPassword() const {return password_.c_str();}
    void SetPassword(const char *password)
    {
        password_ = password;
    }
    const char * GetHostname() const {return hostname_.c_str();}
    void SetHostname(const char *hostname)
    {
        hostname_ = hostname;
    }
    ClockFormat GetClockFormat() const {return clockFormat_;}
    void SetClockFormat(ClockFormat clockFormat)
    {
        clockFormat_ = clockFormat;
    }
    const char * GetTimeZone() const {return timeZone_.c_str();}
    void SetTimeZone(const char *timezone)
    {
        timeZone_ = timezone;
    }
    void Settings();
private:
    std::string ssid_;
    std::string password_;
    std::string hostname_;
    std::string timeZone_;
    std::string prefsfile_;
    ClockFormat clockFormat_;
    Keyboard::Keyboard keyboard;
    void ssidScreen();
    bool displayYesNo_(const char *question);
    void displayWiFissids_(int first, int count);
    void ssidSelected(int i);
    void ssidGetPassword(const char *ssid,char *passwordBuffer,
                         size_t bufferSize);
    static constexpr const uint8_t LISTSIZE = 4;
    bool list_currstate[LISTSIZE], list_laststate[LISTSIZE];
    bool listJustPressed(uint8_t i)
    {
        HASSERT(i < LISTSIZE);
        return (list_currstate[i] && !list_laststate[i]);
    }
    bool listJustReleased(uint8_t i)
    {
        HASSERT(i < LISTSIZE);
        return  (!list_currstate[i] && list_laststate[i]);
    }
    void listPress(uint8_t i, bool p)
    {
        HASSERT(i < LISTSIZE);
        list_laststate[i] = list_currstate[i];
        list_currstate[i] = p;
    }
    bool listIsPressed(uint8_t i) 
    {
        HASSERT(i < LISTSIZE);
        return list_currstate[i];
    }
        
    void hostnameScreen();
    void clockFormatScreen();
    void timeZoneScreen();
    class SettingsButton {
    public:
        SettingsButton(Adafruit_GFX *gfx, int16_t x, 
                       int16_t y, uint16_t w, uint16_t h, uint16_t outline, 
                       uint16_t fill, uint16_t textcolor, const char *label, 
                       uint8_t textsize);
        void drawButton(const char * value,const char *message = NULL, 
                        bool inverted = false);
        bool contains(int16_t x, int16_t y);
        /**********************************************************************/
        /*!
         *     @brief    Sets button state, should be done by some touch function
         *     @param    p  True for pressed, false for not.
         *   */
        /**********************************************************************/
        void press(bool p) {
            laststate = currstate;
            currstate = p;
        }
        
        bool justPressed();
        bool justReleased();
        /**********************************************************************/
        /*!
         *     @brief    Query whether the button is currently pressed
         *     @returns  True if pressed
         *   */
        /**********************************************************************/
        bool isPressed(void) { return currstate; };
    private:
        Adafruit_GFX *_gfx;
        int16_t _x1, _y1; // Coordinates of top-left corner
        uint16_t _w, _h;
        uint8_t _textsize_x;
        uint8_t _textsize_y;
        uint16_t _outlinecolor, _fillcolor, _textcolor;
        char _label[30];
        bool currstate, laststate;
    };
    
    SettingsButton ssid_button_;
    SettingsButton hostname_button_;
    SettingsButton clockfmt_button_;
    SettingsButton timeZone_button_;
    Adafruit_GFX_Button return_;
    Adafruit_GFX_Button yes_;
    Adafruit_GFX_Button no_;
    Adafruit_GFX_Button previous_;
    Adafruit_GFX_Button next_;
    Adafruit_GFX_Button Twelve_;
    Adafruit_GFX_Button TwentyFour_;
    Adafruit_GFX_Button Apply_;
    
    static constexpr uint8_t NAMEZIZE = 10;
    static constexpr uint8_t TZSIZE = 32;
    
    typedef struct tzEntry {
        char name[NAMEZIZE];
        char value[TZSIZE];
    } TzEntry;
    static constexpr const TzEntry TimeZoneList_[LISTSIZE] = {
        {"Eastern", "EST5EDT,M3.2.0,M11.1.0"},
        {"Central", "CST6CDT,M3.2.0,M11.1.0"},
        {"Mountain", "MST7MDT,M3.2.0,M11.1.0"},
        {"Pacific", "PST8PDT,M3.2.0,M11.1.0"}
    };
};

}

#endif // __PREFERENCES_H

