// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Tue Aug 27 09:52:48 2024
//  Last Modified : <240829.1452>
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
/// @file MainScreen.h
/// @author Robert Heller
/// @date Tue Aug 27 09:52:48 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __MAINSCREEN_H
#define __MAINSCREEN_H

#include <Adafruit_GFX.h>

#include "Singleton.h"
#include "Button_xbm.h"

namespace MainScreen {

class MainScreen : public Singleton<MainScreen>
{
public:
    MainScreen() : lastMillis_(0) {}
    ~MainScreen() {}
    void Initialize();
    void Loop();
    String Page();
private:
    typedef enum {gear=0, clock, hand, lastbutton} ButtonIndex;
    Button_xbm::Button_xbm buttons_[3];
    int lastMillis_;
    ButtonIndex check_buttons_();
    void refreshScreen_();
};

}

#endif // __MAINSCREEN_H

