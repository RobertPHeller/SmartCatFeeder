#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Aug 15 16:55:29 2024
#  Last Modified : <240815.1732>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
#*****************************************************************************


from optparse import OptionParser
import subprocess
import os
import time
import platform
import getpass
import filecmp

f_null = open(os.devnull, "w")
usage = "usage: %prog [options]\n\n" + \
    "  %prog -i $(APP_PATH) -o revisions.h\n"
    
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output", dest="output", metavar="FILE",
                  default="Revision",
                  help="generated output files (without the file extentions)")
parser.add_option("-d", "--dirty", dest="dirty", action="store_true",
                  default=False,
                  help="add the \"dirty\" suffix: -d")
parser.add_option("-t", "--time", dest="date", action="store_true",
                  default=False,
                  help="add the date/time to the output")
parser.add_option("-H", "--host", dest="hostname", action="store_true",
                  default=False,
                  help="add the hostname to the output")
parser.add_option("-U", "--username", dest="username", action="store_true",
                  default=False,
                  help="add the username and hostname to the output")
                                                                        
(options, args) = parser.parse_args()

inputs = '..'

orig_dir = os.path.abspath('./')

#initialize hxx output to nothing
outputhxx = ''

# add data/time
if options.date :
    now = time.strftime("%a, %d %b %Y %H:%M:%S %Z")
    outputhxx += '\n#define BUILD_TIME "' + now + '"\n'

# add user and host names
if options.username or options.hostname :
    outputhxx += '\n#define BUILT_BY "'
    if options.username :
        username = getpass.getuser() + '@'
        outputhxx += username
    if options.hostname :
        hostname = platform.node()
        outputhxx += hostname
    outputhxx +='"\n'

main_git_hash = None

# go into the root of the repo
os.chdir(orig_dir)

# get the short hash
git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
git_hash = str(git_hash[:7].decode())

# get the dirty flag
dirty = os.system('git diff --quiet')

hashopts = ""

if dirty :
    hashopts += ':-d'
if main_git_hash is None:
    main_git_hash = git_hash + hashopts

outputhxx = outputhxx[:-1]
if main_git_hash is not None:
    outputhxx += '\n#define PROGRAM_NAME "' + os.path.split(os.path.abspath(orig_dir))[1] + '"\n'
    outputhxx += '\n#define REVISION_GIT_HASH "' + main_git_hash + '"\n'

os.chdir(orig_dir)

# generate the *.hxxout file
output_file = open(options.output + 'Try.h', 'w')
output_file.write(outputhxx)
output_file.close()
# because a build may always run the script, we only want to replace the actual
# output files that get built if something has changed

diffhxx = subprocess.call(["diff",
                           "-I", """Sun, """, "-I", """Mon, """,
                           "-I", """Tue, """, "-I", """Wed, """,
                           "-I", """Thu, """, "-I", """Fri, """,
                           "-I", """Sat, """,
                           options.output + 'Try.h',
                           options.output + '.h'],
                          stdout=f_null, stderr=f_null)

# disable this because we are not actually writing a cxx file above.
diffcxx = 0

if diffhxx != 0 :
    os.system('rm -f ' + options.output + '.h')
    os.system('mv ' + options.output + 'Try.h ' + options.output + '.h')



os.system('rm -f ' + options.output + 'Try.h')
f_null.close()

