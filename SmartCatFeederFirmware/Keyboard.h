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
//  Last Modified : <240825.1553>
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


namespace Keyboard {

class Keyboard
{
public:
    Keyboard() : mode_(Off){}
    ~Keyboard() {}
    void start();
    void end();
    bool KeyPressed(char &c);
private:
    typedef enum {Off=0, LowerAlnum, UpperAlnum, Special} KeyMode;
    void SetMode(KeyMode mode) {mode_ = mode;}
    typedef enum {blank=0, shift, return_l, return_r, delete_l, delete_r, 
        special, spacebar_l, spacebar_m, spacebar_r, alnum} IconId;
    typedef struct keyCell {
        int16_t x;
        int16_t y;
        uint8_t ischar:1;
        uint8_t newmode:2;
        uint8_t iconid:6;
        unsigned char c;
    } KeyCell;
    KeyMode mode_;
    void drawkeyboard_();
    const KeyCell *getTouch(uint16_t x, uint16_t y) const;
    static constexpr const KeyCell LowerAlnum_[50] = {
        {120,160,1,LowerAlnum,blank,'1'},
        {144,160,1,LowerAlnum,blank,'2'},
        {168,160,1,LowerAlnum,blank,'3'},
        {192,160,1,LowerAlnum,blank,'4'},
        {216,160,1,LowerAlnum,blank,'5'},
        {240,160,1,LowerAlnum,blank,'6'},
        {264,160,1,LowerAlnum,blank,'7'},
        {288,160,1,LowerAlnum,blank,'8'},
        {312,160,1,LowerAlnum,blank,'9'},
        {336,160,1,LowerAlnum,blank,'0'},
        {120,192,1,LowerAlnum,blank,'q'},
        {144,192,1,LowerAlnum,blank,'w'},
        {168,192,1,LowerAlnum,blank,'e'},
        {192,192,1,LowerAlnum,blank,'r'},
        {216,192,1,LowerAlnum,blank,'t'},
        {240,192,1,LowerAlnum,blank,'y'},
        {264,192,1,LowerAlnum,blank,'u'},
        {288,192,1,LowerAlnum,blank,'i'},
        {312,192,1,LowerAlnum,blank,'o'},
        {336,192,1,LowerAlnum,blank,'p'},
        {120,224,0,UpperAlnum,shift,'\0'},
        {144,224,1,LowerAlnum,blank,'a'},
        {168,224,1,LowerAlnum,blank,'s'},
        {192,224,1,LowerAlnum,blank,'d'},
        {216,224,1,LowerAlnum,blank,'f'},
        {240,224,1,LowerAlnum,blank,'g'},
        {264,224,1,LowerAlnum,blank,'h'},
        {288,224,1,LowerAlnum,blank,'j'},
        {312,224,1,LowerAlnum,blank,'k'},
        {336,224,1,LowerAlnum,blank,'l'},
        {120,256,0,Special,special,'\0'},
        {144,256,1,LowerAlnum,blank,'z'},
        {168,256,1,LowerAlnum,blank,'x'},
        {192,256,1,LowerAlnum,blank,'c'},
        {216,256,1,LowerAlnum,blank,'v'},
        {240,256,1,LowerAlnum,blank,'b'},
        {264,256,1,LowerAlnum,blank,'n'},
        {288,256,1,LowerAlnum,blank,'m'},
        {312,256,1,LowerAlnum,return_l,'\r'},
        {336,256,1,LowerAlnum,return_r,'\r'},
        {120,288,1,LowerAlnum,blank,'.'},
        {144,288,1,LowerAlnum,blank,','},
        {168,288,1,LowerAlnum,spacebar_l,' '},
        {192,288,1,LowerAlnum,spacebar_m,' '},
        {216,288,1,LowerAlnum,spacebar_m,' '},
        {240,288,1,LowerAlnum,spacebar_m,' '},
        {264,288,1,LowerAlnum,spacebar_m,' '},
        {288,288,1,LowerAlnum,spacebar_r,' '},
        {312,288,1,LowerAlnum,delete_l,'\b'},
        {336,288,1,LowerAlnum,delete_r,'\b'}
    };
    static constexpr const KeyCell UpperAlnum_[50] = {
        {120,160,1,LowerAlnum,blank,'1'},
        {144,160,1,LowerAlnum,blank,'2'},
        {168,160,1,LowerAlnum,blank,'3'},
        {192,160,1,LowerAlnum,blank,'4'},
        {216,160,1,LowerAlnum,blank,'5'},
        {240,160,1,LowerAlnum,blank,'6'},
        {264,160,1,LowerAlnum,blank,'7'},
        {288,160,1,LowerAlnum,blank,'8'},
        {312,160,1,LowerAlnum,blank,'9'},
        {336,160,1,LowerAlnum,blank,'0'},
        {120,192,1,LowerAlnum,blank,'Q'},
        {144,192,1,LowerAlnum,blank,'W'},
        {168,192,1,LowerAlnum,blank,'E'},
        {192,192,1,LowerAlnum,blank,'R'},
        {216,192,1,LowerAlnum,blank,'T'},
        {240,192,1,LowerAlnum,blank,'Y'},
        {264,192,1,LowerAlnum,blank,'U'},
        {288,192,1,LowerAlnum,blank,'I'},
        {312,192,1,LowerAlnum,blank,'O'},
        {336,192,1,LowerAlnum,blank,'P'},
        {120,224,0,LowerAlnum,shift,'\0'},
        {144,224,1,LowerAlnum,blank,'A'},
        {168,224,1,LowerAlnum,blank,'S'},
        {192,224,1,LowerAlnum,blank,'D'},
        {216,224,1,LowerAlnum,blank,'F'},
        {240,224,1,LowerAlnum,blank,'G'},
        {264,224,1,LowerAlnum,blank,'H'},
        {288,224,1,LowerAlnum,blank,'J'},
        {312,224,1,LowerAlnum,blank,'K'},
        {336,224,1,LowerAlnum,blank,'L'},
        {120,256,0,Special,special,'\0'},
        {144,256,1,LowerAlnum,blank,'Z'},
        {168,256,1,LowerAlnum,blank,'X'},
        {192,256,1,LowerAlnum,blank,'C'},
        {216,256,1,LowerAlnum,blank,'V'},
        {240,256,1,LowerAlnum,blank,'B'},
        {264,256,1,LowerAlnum,blank,'N'},
        {288,256,1,LowerAlnum,blank,'M'},
        {312,256,1,LowerAlnum,return_l,'\r'},
        {336,256,1,LowerAlnum,return_r,'\r'},
        {120,288,1,LowerAlnum,blank,'.'},
        {144,288,1,LowerAlnum,blank,','},
        {168,288,1,LowerAlnum,spacebar_l,' '},
        {192,288,1,LowerAlnum,spacebar_m,' '},
        {216,288,1,LowerAlnum,spacebar_m,' '},
        {240,288,1,LowerAlnum,spacebar_m,' '},
        {264,288,1,LowerAlnum,spacebar_m,' '},
        {288,288,1,LowerAlnum,spacebar_r,' '},
        {312,288,1,LowerAlnum,delete_l,'\b'},
        {336,288,1,LowerAlnum,delete_r,'\b'}
    };
    static constexpr const KeyCell Special_[50] = {
        {120,160,1,Special,blank,'!'},
        {144,160,1,Special,blank,'@'},
        {168,160,1,Special,blank,'#'},
        {192,160,1,Special,blank,'$'},
        {216,160,1,Special,blank,'%'},
        {240,160,1,Special,blank,'^'},
        {264,160,1,Special,blank,'&'},
        {288,160,1,Special,blank,'*'},
        {312,160,1,Special,blank,'('},
        {336,160,1,Special,blank,')'},
        {120,192,1,Special,blank,'`'},
        {144,192,1,Special,blank,'~'},
        {168,192,1,Special,blank,'-'},
        {192,192,1,Special,blank,'_'},
        {216,192,1,Special,blank,'+'},
        {240,192,1,Special,blank,'='},
        {264,192,1,Special,blank,'{'},
        {288,192,1,Special,blank,'}'},
        {312,192,1,Special,blank,'['},
        {336,192,1,Special,blank,']'},
        {120,224,0,LowerAlnum,shift,'\0'},
        {144,224,1,Special,blank,';'},
        {168,224,1,Special,blank,':'},
        {192,224,1,Special,blank,'"'},
        {216,224,1,Special,blank,'\''},
        {240,224,1,Special,blank,'|'},
        {264,224,1,Special,blank,'\\'},
        {288,224,1,Special,blank,'<'},
        {312,224,1,Special,blank,'>'},
        {336,224,1,Special,blank,'?'},
        {120,256,0,LowerAlnum,alnum,'\0'},
        {144,256,1,Special,blank,'/'},
        {168,256,0,Special,blank,' '},
        {192,256,0,Special,blank,' '},
        {216,256,0,Special,blank,' '},
        {240,256,0,Special,blank,' '},
        {264,256,0,Special,blank,' '},
        {288,256,0,Special,blank,' '},
        {312,256,1,Special,return_l,'\r'},
        {336,256,1,Special,return_r,'\r'},
        {120,288,1,Special,blank,'.'},
        {144,288,1,Special,blank,','},
        {168,288,1,Special,spacebar_l,' '},
        {192,288,1,Special,spacebar_m,' '},
        {216,288,1,Special,spacebar_m,' '},
        {240,288,1,Special,spacebar_m,' '},
        {264,288,1,Special,spacebar_m,' '},
        {288,288,1,Special,spacebar_r,' '},
        {312,288,1,Special,delete_l,'\b'},
        {336,288,1,Special,delete_r,'\b'}
    };
    static constexpr uint8_t Keys_ = 50;
    static constexpr uint8_t KeysRowStride_ = 10;
    static constexpr uint8_t KeyRowHeight_ = 32;
    static constexpr uint8_t KeyColumnWidth_ = 24;
    static constexpr uint16_t KOrigX_ = 120;
    static constexpr uint16_t KOrigY_ = 160;
    static constexpr uint16_t KWidth_ = 350-120;
    static constexpr uint16_t KHeight_ = 320-160;
};

}

#endif // __KEYBOARD_H

