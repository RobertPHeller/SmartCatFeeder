// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sat Aug 24 21:11:51 2024
//  Last Modified : <240827.1517>
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
/// @file Keyboard.h
/// @author Robert Heller
/// @date Sat Aug 24 21:11:51 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __KEYBOARD_H
#define __KEYBOARD_H

#include <Adafruit_GFX.h>
#include "Display.h"

#include <stdio.h>

#define HASSERT(x) if (!(x)) \
{ \
    char buffer[256];\
    snprintf(buffer,sizeof(buffer),"Assertion failed in file " __FILE__ " line %d: assert(%s)", __LINE__, #x); \
    Serial.println(buffer);\
    while(1) delay(100);\
}


namespace Keyboard {

class Keyboard
{
public:
    Keyboard() : mode_(Off){}
    ~Keyboard() {}
    void start();
    void end();
    char KeyPressed();
private:
    static constexpr uint8_t Keys_ = 50;
    static constexpr uint8_t KeysRowStride_ = 10;
    static constexpr uint8_t KeyRowHeight_ = 32;
    static constexpr uint8_t KeyColumnWidth_ = 24;
    static constexpr uint16_t KOrigX_ = 120;
    static constexpr uint16_t KOrigY_ = 160;
    static constexpr uint16_t KWidth_ = KeysRowStride_*KeyColumnWidth_;
    static constexpr uint16_t KHeight_ = KeyRowHeight_*(Keys_/KeysRowStride_);
    typedef enum {Off=0, LowerAlnum, UpperAlnum, Special} KeyMode;
    void SetMode(KeyMode mode) {mode_ = mode;}
    typedef enum {blank=0, shift, return_l, return_r, delete_l, delete_r, 
        special, spacebar_l, spacebar_m, spacebar_r, alnum} IconId;
    typedef struct keyCell {
        int16_t col;
        int16_t row;
        uint8_t ischar:1;
        uint8_t newmode:2;
        uint8_t iconid:6;
        unsigned char c;
    } KeyCell;
    KeyMode mode_;
    void drawkeyboard_();
    const KeyCell *getTouch(uint16_t x, uint16_t y);
    uint8_t key_currstate[Keys_], key_laststate[Keys_];
    bool keyJustPressed(uint8_t i)
    {
        HASSERT(i < Keys_);
        return (key_currstate[i] && !key_laststate[i]);
    }
    bool keyJustReleased(uint8_t i)
    {
        HASSERT(i < Keys_);
        return  (!key_currstate[i] && key_laststate[i]);
    }
    void keyPress(uint8_t i, bool p)
    {
        HASSERT(i < Keys_);
        key_laststate[i] = key_currstate[i];
        key_currstate[i] = p;
    }
    bool keyIsPressed(uint8_t i)
    {
        HASSERT(i < Keys_); 
        return key_currstate[i];
    }
    static constexpr const KeyCell LowerAlnum_[Keys_] = {
        {0,0,1,LowerAlnum,blank,'1'},
        {1,0,1,LowerAlnum,blank,'2'},
        {2,0,1,LowerAlnum,blank,'3'},
        {3,0,1,LowerAlnum,blank,'4'},
        {4,0,1,LowerAlnum,blank,'5'},
        {5,0,1,LowerAlnum,blank,'6'},
        {6,0,1,LowerAlnum,blank,'7'},
        {7,0,1,LowerAlnum,blank,'8'},
        {8,0,1,LowerAlnum,blank,'9'},
        {9,0,1,LowerAlnum,blank,'0'},
        {0,1,1,LowerAlnum,blank,'q'},
        {1,1,1,LowerAlnum,blank,'w'},
        {2,1,1,LowerAlnum,blank,'e'},
        {3,1,1,LowerAlnum,blank,'r'},
        {4,1,1,LowerAlnum,blank,'t'},
        {5,1,1,LowerAlnum,blank,'y'},
        {6,1,1,LowerAlnum,blank,'u'},
        {7,1,1,LowerAlnum,blank,'i'},
        {8,1,1,LowerAlnum,blank,'o'},
        {9,1,1,LowerAlnum,blank,'p'},
        {0,2,0,UpperAlnum,shift,'\0'},
        {1,2,1,LowerAlnum,blank,'a'},
        {2,2,1,LowerAlnum,blank,'s'},
        {3,2,1,LowerAlnum,blank,'d'},
        {4,2,1,LowerAlnum,blank,'f'},
        {5,2,1,LowerAlnum,blank,'g'},
        {6,2,1,LowerAlnum,blank,'h'},
        {7,2,1,LowerAlnum,blank,'j'},
        {8,2,1,LowerAlnum,blank,'k'},
        {9,2,1,LowerAlnum,blank,'l'},
        {0,3,0,Special,special,'\0'},
        {1,3,1,LowerAlnum,blank,'z'},
        {2,3,1,LowerAlnum,blank,'x'},
        {3,3,1,LowerAlnum,blank,'c'},
        {4,3,1,LowerAlnum,blank,'v'},
        {5,3,1,LowerAlnum,blank,'b'},
        {6,3,1,LowerAlnum,blank,'n'},
        {7,3,1,LowerAlnum,blank,'m'},
        {8,3,1,LowerAlnum,return_l,'\r'},
        {9,3,1,LowerAlnum,return_r,'\r'},
        {0,4,1,LowerAlnum,blank,'.'},
        {1,4,1,LowerAlnum,blank,','},
        {2,4,1,LowerAlnum,spacebar_l,' '},
        {3,4,1,LowerAlnum,spacebar_m,' '},
        {4,4,1,LowerAlnum,spacebar_m,' '},
        {5,4,1,LowerAlnum,spacebar_m,' '},
        {6,4,1,LowerAlnum,spacebar_m,' '},
        {7,4,1,LowerAlnum,spacebar_r,' '},
        {8,4,1,LowerAlnum,delete_l,'\b'},
        {9,4,1,LowerAlnum,delete_r,'\b'}
    };
    static constexpr const KeyCell UpperAlnum_[Keys_] = {
        {0,0,1,LowerAlnum,blank,'1'},
        {1,0,1,LowerAlnum,blank,'2'},
        {2,0,1,LowerAlnum,blank,'3'},
        {3,0,1,LowerAlnum,blank,'4'},
        {4,0,1,LowerAlnum,blank,'5'},
        {5,0,1,LowerAlnum,blank,'6'},
        {6,0,1,LowerAlnum,blank,'7'},
        {7,0,1,LowerAlnum,blank,'8'},
        {8,0,1,LowerAlnum,blank,'9'},
        {9,0,1,LowerAlnum,blank,'0'},
        {0,1,1,LowerAlnum,blank,'Q'},
        {1,1,1,LowerAlnum,blank,'W'},
        {2,1,1,LowerAlnum,blank,'E'},
        {3,1,1,LowerAlnum,blank,'R'},
        {4,1,1,LowerAlnum,blank,'T'},
        {5,1,1,LowerAlnum,blank,'Y'},
        {6,1,1,LowerAlnum,blank,'U'},
        {7,1,1,LowerAlnum,blank,'I'},
        {8,1,1,LowerAlnum,blank,'O'},
        {9,1,1,LowerAlnum,blank,'P'},
        {0,2,0,LowerAlnum,shift,'\0'},
        {1,2,1,LowerAlnum,blank,'A'},
        {2,2,1,LowerAlnum,blank,'S'},
        {3,2,1,LowerAlnum,blank,'D'},
        {4,2,1,LowerAlnum,blank,'F'},
        {5,2,1,LowerAlnum,blank,'G'},
        {6,2,1,LowerAlnum,blank,'H'},
        {7,2,1,LowerAlnum,blank,'J'},
        {8,2,1,LowerAlnum,blank,'K'},
        {9,2,1,LowerAlnum,blank,'L'},
        {0,3,0,Special,special,'\0'},
        {1,3,1,LowerAlnum,blank,'Z'},
        {2,3,1,LowerAlnum,blank,'X'},
        {3,3,1,LowerAlnum,blank,'C'},
        {4,3,1,LowerAlnum,blank,'V'},
        {5,3,1,LowerAlnum,blank,'B'},
        {6,3,1,LowerAlnum,blank,'N'},
        {7,3,1,LowerAlnum,blank,'M'},
        {8,3,1,LowerAlnum,return_l,'\r'},
        {9,3,1,LowerAlnum,return_r,'\r'},
        {0,4,1,LowerAlnum,blank,'.'},
        {1,4,1,LowerAlnum,blank,','},
        {2,4,1,LowerAlnum,spacebar_l,' '},
        {3,4,1,LowerAlnum,spacebar_m,' '},
        {4,4,1,LowerAlnum,spacebar_m,' '},
        {5,4,1,LowerAlnum,spacebar_m,' '},
        {6,4,1,LowerAlnum,spacebar_m,' '},
        {7,4,1,LowerAlnum,spacebar_r,' '},
        {8,4,1,LowerAlnum,delete_l,'\b'},
        {9,4,1,LowerAlnum,delete_r,'\b'}
    };
    static constexpr const KeyCell Special_[Keys_] = {
        {0,0,1,Special,blank,'!'},
        {1,0,1,Special,blank,'@'},
        {2,0,1,Special,blank,'#'},
        {3,0,1,Special,blank,'$'},
        {4,0,1,Special,blank,'%'},
        {5,0,1,Special,blank,'^'},
        {6,0,1,Special,blank,'&'},
        {7,0,1,Special,blank,'*'},
        {8,0,1,Special,blank,'('},
        {9,0,1,Special,blank,')'},
        {0,1,1,Special,blank,'`'},
        {1,1,1,Special,blank,'~'},
        {2,1,1,Special,blank,'-'},
        {3,1,1,Special,blank,'_'},
        {4,1,1,Special,blank,'+'},
        {5,1,1,Special,blank,'='},
        {6,1,1,Special,blank,'{'},
        {7,1,1,Special,blank,'}'},
        {8,1,1,Special,blank,'['},
        {9,1,1,Special,blank,']'},
        {0,2,0,UpperAlnum,shift,'\0'},
        {1,2,1,Special,blank,';'},
        {2,2,1,Special,blank,':'},
        {3,2,1,Special,blank,'"'},
        {4,2,1,Special,blank,'\''},
        {5,2,1,Special,blank,'|'},
        {6,2,1,Special,blank,'\\'},
        {7,2,1,Special,blank,'<'},
        {8,2,1,Special,blank,'>'},
        {9,2,1,Special,blank,'?'},
        {0,3,0,LowerAlnum,alnum,'\0'},
        {1,3,1,Special,blank,'/'},
        {2,3,0,Special,blank,' '},
        {3,3,0,Special,blank,' '},
        {4,3,0,Special,blank,' '},
        {5,3,0,Special,blank,' '},
        {6,3,0,Special,blank,' '},
        {7,3,0,Special,blank,' '},
        {8,3,1,Special,return_l,'\r'},
        {9,3,1,Special,return_r,'\r'},
        {0,4,1,Special,blank,'.'},
        {1,4,1,Special,blank,','},
        {2,4,1,Special,spacebar_l,' '},
        {3,4,1,Special,spacebar_m,' '},
        {4,4,1,Special,spacebar_m,' '},
        {5,4,1,Special,spacebar_m,' '},
        {6,4,1,Special,spacebar_m,' '},
        {7,4,1,Special,spacebar_r,' '},
        {8,4,1,Special,delete_l,'\b'},
        {9,4,1,Special,delete_r,'\b'}
    };
};

}

#endif // __KEYBOARD_H

