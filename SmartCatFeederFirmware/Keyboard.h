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
//  Last Modified : <240824.2126>
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
    typedef enum {LowerAlnum, UpperAlnum, Special1Num, Special2Num} KeyMode;
    Keyboard() : mode_(LowerAlnum){}
    ~Keyboard() {}
    void SetMode(KeyMode mode);
    bool KeyPressed(char &c);
private:
    KeyMode mode_;
};

}

#endif // __KEYBOARD_H

