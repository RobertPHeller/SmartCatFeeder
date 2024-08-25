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
//  Last Modified : <240824.2029>
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
    {
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
    bool SettingsScreen();
    void SettingsScreenStart();
private:
    enum {start, ssid, hostname, clockfmt, timezone} screen_;
    std::string ssid_;
    std::string password_;
    std::string hostname_;
    std::string timeZone_;
    std::string prefsfile_;
    ClockFormat clockFormat_;
    
};

}

#endif // __PREFERENCES_H

