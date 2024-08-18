// -!- c++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Fri Aug 16 21:31:26 2024
//  Last Modified : <240817.1351>
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
/// @file FeedWebServer.h
/// @author Robert Heller
/// @date Fri Aug 16 21:31:26 2024
/// 
///
//////////////////////////////////////////////////////////////////////////////

#ifndef __FEEDWEBSERVER_H
#define __FEEDWEBSERVER_H

#include <WebServer.h>
#include "Singleton.h"

namespace FeedWebServer {

class FeedWebServer : public WebServer, public Singleton<FeedWebServer>
{
public:
    FeedWebServer() \
                : WebServer(80)
    {
    }
    static void StartServer()
    {
        instance()->_startServer();
    }
private:
    void _startServer()
    {
        on("/", Welcome);
        on("/style.css", SendStyle);
        on("/javascript.js", SendJavaScript);
        on("/Robot1-110.png", SendRobot1_110);
        onNotFound(NotFound);
        begin();
    }
    static void Welcome() {instance()->_welcome();}
    void _welcome();
    static void NotFound() {instance()->_notFound();}
    void _notFound();
    static void SendStyle() {instance()->_sendStyle();}
    void _sendStyle();
    static void SendJavaScript() {instance()->_sendJavaScript();}
    void _sendJavaScript();
    static void SendRobot1_110() {instance()->_sendRobot1_110();}
    void _sendRobot1_110();
    String header_(String title);
    String footer_();
};



}

#endif // __FEEDWEBSERVER_H

