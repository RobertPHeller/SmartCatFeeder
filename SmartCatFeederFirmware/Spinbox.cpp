// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Wed Aug 28 14:59:30 2024
//  Last Modified : <240828.1651>
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
/// @file Spinbox.cpp
/// @author Robert Heller
/// @date Wed Aug 28 14:59:30 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

static const char rcsid[] = "@(#) : $Id$";


#include <Arduino.h>
#include <stdio.h>
#include <Adafruit_GFX.h>
#include "Spinbox.h"
#include "BackgroundTask.h"

#include "incr.xbm.h"
#include "decr.xbm.h"

#ifndef min
#define min(a, b) (((a) < (b)) ? (a) : (b))
#endif

Spinbox::Spinbox(Adafruit_GFX *gfx, int16_t x, int16_t y, uint16_t outline, 
                 uint16_t fill,uint16_t textcolor, int16_t minv, int16_t maxv, 
                 const char *fmt)
      : _gfx(gfx)
, _x1(x)
, _y1(y)
, _incr_w(incr_width)
, _incr_h(incr_height)
, _decr_w(decr_width)
, _decr_h(decr_height)
, _textsize_x(5)
, _textsize_y(5)
, _outlinecolor(outline)
, _fillcolor(fill)
, _textcolor(textcolor)
, _minVal(minv)
, _maxVal(maxv)
{
    char tempbuffer[20];
    int16_t tempx, tempy;
    uint16_t tempw, temph;
    _hh = _incr_h+_decr_h;
    strncpy(_format,fmt,9);
    _format[9] = '\0';
    snprintf(tempbuffer,sizeof(tempbuffer),_format,_minVal);
    _gfx->setTextSize(_textsize_x,_textsize_y);
    _gfx->getTextBounds(tempbuffer,0,0,&tempx,&tempy,&tempw,&temph);
    tempw += 4;
    temph += 4;
    _ww = tempw+incr_width;
    if (_ww < tempw+decr_width) _ww = tempw+decr_width;
    if (_hh < temph) _hh = temph;
    snprintf(tempbuffer,sizeof(tempbuffer),_format,_maxVal);
    _gfx->getTextBounds(tempbuffer,0,0,&tempx,&tempy,&tempw,&temph);
    tempw += 4;
    temph += 4;
    if (_ww < tempw+incr_width+4) _ww = tempw+incr_width;
    if (_ww < tempw+decr_width) _ww = tempw+decr_width;
    if (_hh < temph) _hh = temph;
    _incr_y1 = _y1;
    _decr_y1 = (_y1+_hh)-decr_height;
    int16_t right = _x1 + _ww;
    _incr_x1 = right-incr_width;
    _decr_x1 = right-decr_width;
    if (_decr_x1 < _incr_x1) _incr_x1 = _decr_x1;
    if (_incr_x1 < _decr_x1) _decr_x1 = _incr_x1;
}

void Spinbox::drawBox(int16_t value)
{
    char buffer[20];
    _value = value;
    snprintf(buffer,sizeof(buffer),_format,_value);
    int w = _ww - max(incr_width,decr_width);
    uint8_t r = min(w, _hh) / 4; // Corner radius
    _gfx->fillRoundRect(_x1, _y1, w, _hh,  r, _fillcolor);
    _gfx->drawRoundRect(_x1, _y1, w, _hh,  r, _outlinecolor);
    _gfx->setCursor(_x1 + (w / 2) - (strlen(buffer) * 3 * _textsize_x),
                    _y1 + (_hh / 2) - (4 * _textsize_y));
    _gfx->setTextColor(_textcolor);
    _gfx->setTextSize(_textsize_x, _textsize_y);
    _gfx->print(buffer);
    _gfx->drawXBitmap(_incr_x1,_incr_y1,incr_bits,incr_width,incr_height,
                      _textcolor);
    _gfx->drawXBitmap(_decr_x1,_decr_y1,decr_bits,decr_width,decr_height,
                      _textcolor);
}

bool Spinbox::incrContains(int16_t x, int16_t y) 
{
    return ((x >= _incr_x1) && (x < (int16_t)(_incr_x1 + _incr_w)) && 
            (y >= _incr_y1) && (y < (int16_t)(_incr_y1 + _incr_h)));
}

bool Spinbox::decrContains(int16_t x, int16_t y) 
{
    return ((x >= _decr_x1) && (x < (int16_t)(_decr_x1 + _decr_w)) && 
            (y >= _decr_y1) && (y < (int16_t)(_decr_y1 + _decr_h)));
}

bool Spinbox::incrJustPressed() 
{ 
    return (incr_currstate && !incr_laststate); 
}

bool Spinbox::decrJustPressed() 
{ 
    return (decr_currstate && !decr_laststate); 
}

bool Spinbox::incrJustReleased() 
{ 
    return (!incr_currstate && incr_laststate); 
} 

bool Spinbox::decrJustReleased() 
{ 
    return (!decr_currstate && decr_laststate); 
} 

void Spinbox::incr()
{
    if (_value < _maxVal) 
    {
        _value++;
        char buffer[20];
        snprintf(buffer,sizeof(buffer),_format,_value);
        int w = _ww - max(incr_width,decr_width);
        _gfx->setCursor(_x1 + (w / 2) - (strlen(buffer) * 3 * _textsize_x),
                        _y1 + (_hh / 2) - (4 * _textsize_y));
        _gfx->setTextColor(_textcolor);
        _gfx->setTextSize(_textsize_x, _textsize_y);
        _gfx->print(buffer);
    }
}

void Spinbox::decr()
{
    if (_value > _minVal) 
    {
        _value--;
        char buffer[20];
        snprintf(buffer,sizeof(buffer),_format,_value);
        int w = _ww - max(incr_width,decr_width);
        _gfx->setCursor(_x1 + (w / 2) - (strlen(buffer) * 3 * _textsize_x),
                        _y1 + (_hh / 2) - (4 * _textsize_y));
        _gfx->setTextColor(_textcolor);
        _gfx->setTextSize(_textsize_x, _textsize_y);
        _gfx->print(buffer);
    }
}

void Spinbox::processAt(int16_t x, int16_t y)
{
    if (incrContains(x,y))
    {
        incrPress(true);
    }
    else
    {
        incrPress(false);
    }
    if (decrContains(x,y))
    {
        decrPress(true);
    }
    else
    {
        decrPress(false);
    }
    if (incrJustReleased())
    {
        incr();
    }
    if (incrJustPressed()) 
    {
        BackgroundTask::RunTasks(100);
    }
    if (decrJustReleased())
    {
        decr();
    }
    if (decrJustPressed()) 
    {
        BackgroundTask::RunTasks(100);
    }
}

