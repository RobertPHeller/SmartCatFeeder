// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Sun Aug 25 08:41:52 2024
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
/// @file Keyboard.cpp
/// @author Robert Heller
/// @date Sun Aug 25 08:41:52 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";


#include <Adafruit_GFX.h>
#include "Display.h"
#include "Keyboard.h"
#include "BackgroundTask.h"

namespace Keyboard {

void Keyboard::start()
{
    if (mode_ != Off) return;
    SetMode(LowerAlnum);
    drawkeyboard_();
}
void Keyboard::end()
{
    Display::Display.fillRect(KOrigX_,KOrigY_,KWidth_,KHeight_,HX8357_BLACK);
    SetMode(Off);
}


const Keyboard::KeyCell *Keyboard::getTouch(uint16_t x, uint16_t y)
{
    const KeyCell *keys;
    switch (mode_)
    {
    case LowerAlnum:
        keys = LowerAlnum_;
        break;
    case UpperAlnum:
        keys = UpperAlnum_;
        break;
    case Special:
        keys = Special_;
        break;
    case Off:
        return nullptr;
    }
    for (int i=0; i<Keys_; i+=KeysRowStride_)
    {
        int16_t ky = KOrigY_+(keys[i].row*KeyRowHeight_);
        for (int j=0; j<KeysRowStride_; j++)
        {
            int16_t kx = KOrigX_+(keys[i+j].col*KeyColumnWidth_);
            if ((x >= kx) && (x < (kx+KeyColumnWidth_)) &&
                (y >= ky) && (y < (ky+KeyRowHeight_)))
            {
                keyPress(i+j,true);
                if (keyJustPressed(i+j))
                {
                    BackgroundTask::RunTasks(100);
                }
            }
            else
            {
                keyPress(i+j,false);
                if (keyJustReleased(i+j))
                {
                    return &keys[i+j];
                }
            }
        }
        return nullptr;
    }
    return nullptr;
}

char Keyboard::KeyPressed()
{
    if (mode_ == Off) return '\0';
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
        
        if (p.z != -1)
        {
            const KeyCell *cell = getTouch(p.x,p.y);
            if (cell != nullptr)
            {
                if ((KeyMode)(cell->newmode) != mode_)
                {
                    mode_ = (KeyMode)(cell->newmode);
                    drawkeyboard_();
                }
                if (cell->ischar == 1)
                {
                    return cell->c;
                }
            }
        }
    }
}


#include "shift.xbm.h"
#include "return_l.xbm.h"
#include "return_r.xbm.h"
#include "delete_l.xbm.h"
#include "delete_r.xbm.h"
#include "spacebar_l.xbm.h"
#include "spacebar_m.xbm.h"
#include "spacebar_r.xbm.h"
#include "special.xbm.h"
#include "alnum.xbm.h"

void Keyboard::drawkeyboard_()
{
    if (mode_ == Off) return;
    Display::Display.fillRect(KOrigX_,KOrigY_,KWidth_,KHeight_,HX8357_WHITE);
    const KeyCell *keys;
    switch (mode_)
    {
    case LowerAlnum:
        keys = LowerAlnum_;
        break;
    case UpperAlnum:
        keys = UpperAlnum_;
        break;
    case Special:
        keys = Special_;
        break;
    default:
        break;
    }
    for (int i=0;i<Keys_;i++)
    {
        int16_t x = KOrigX_+(keys[i].col*KeyColumnWidth_);
        int16_t y = KOrigY_+(keys[i].row*KeyRowHeight_);
        IconId icon = (IconId) keys[i].iconid;
        unsigned char c = keys[i].c;
        Display::Display.fillRect(x,y,KeyColumnWidth_,KeyRowHeight_,HX8357_BLACK);
        switch (icon)
        {
        case blank:
            Display::Display.drawChar(x,y,c,HX8357_WHITE,HX8357_BLACK,4);
            break;
        case shift:
            Display::Display.drawXBitmap(x,y,shift_bits,shift_width,shift_height,HX8357_WHITE);
            break;
        case return_l:
            Display::Display.drawXBitmap(x,y,return_l_bits,return_l_width,return_l_height,HX8357_WHITE);
            break;
        case return_r:
            Display::Display.drawXBitmap(x,y,return_r_bits,return_r_width,return_r_height,HX8357_WHITE);
            break;
        case delete_l:
            Display::Display.drawXBitmap(x,y,delete_l_bits,delete_l_width,delete_l_height,HX8357_WHITE);
            break;
        case delete_r:
            Display::Display.drawXBitmap(x,y,delete_r_bits,delete_r_width,delete_r_height,HX8357_WHITE);
            break;
        case special:
            Display::Display.drawXBitmap(x,y,special_bits,special_width,special_height,HX8357_WHITE);
            break;
        case spacebar_l:
            Display::Display.drawXBitmap(x,y,spacebar_l_bits,spacebar_l_width,spacebar_l_height,HX8357_WHITE);
            break;
        case spacebar_m:
            Display::Display.drawXBitmap(x,y,spacebar_m_bits,spacebar_m_width,spacebar_m_height,HX8357_WHITE);
            break;
        case spacebar_r:
            Display::Display.drawXBitmap(x,y,spacebar_r_bits,spacebar_r_width,spacebar_r_height,HX8357_WHITE);
            break;
        case alnum:
            Display::Display.drawXBitmap(x,y,alnum_bits,alnum_width,alnum_height,HX8357_WHITE);
            break;
        }
    }
}

const Keyboard::KeyCell Keyboard::LowerAlnum_[Keyboard::Keys_];
const Keyboard::KeyCell Keyboard::UpperAlnum_[Keyboard::Keys_];
const Keyboard::KeyCell Keyboard::Special_[Keyboard::Keys_];

}
