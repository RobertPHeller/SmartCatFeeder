##-*- makefile -*-############################################################
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Thu Aug 15 14:29:40 2024
#  Last Modified : <250415.1435>
#
#  Description	
#
#  Notes
#
#  History
#	
#  $Log$
#
##############################################################################
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
##############################################################################


INO = SmartCatFeederFirmware.ino
NAU7802TEST = $(HOME)/Arduino/libraries/Adafruit_NAU7802_Library/examples/nau7802_test/nau7802_test.ino

SOURCES = $(wildcard *.cpp) $(wildcard *.h)

TARGET8M = Build8M/$(INO).merged.bin
TARGET4M = Build4M/$(INO).merged.bin
NAU7802TEST8M = BuildSCALECAL8M/$(notdir NAU7802TEST).merged.bin

all: $(TARGET8M)

8M: $(TARGET8M)

4M: $(TARGET4M)

SCALECAL: $(NAU7802TEST8M)	

$(TARGET8M): $(INO) $(SOURCES) Revision.h partitions8M.csv
	-mkdir Build8M
	-cp partitions8M.csv partitions.csv
	arduino --verbose --verify \
		--board esp32:esp32:adafruit_feather_esp32s3 \
		--pref build.path=Build8M --pref upload.maximum_size=4194304\
		--pref build.flash_size=8MB \
		 $(INO)

$(TARGET4M): $(INO) $(SOURCES) Revision.h partitions4M.csv
	-mkdir Build4M
	-cp partitions4M.csv partitions.csv
	arduino --verbose --verify \
		--board esp32:esp32:adafruit_feather_esp32s3 \
		--pref build.path=Build4M --pref upload.maximum_size=2097152\
		--pref build.flash_size=4MB \
		 $(INO)

$(NAU7802TEST8M): $(NAU7802TEST) partitions8M.csv
	-mkdir BuildSCALECAL8M
	-cp partitions8M.csv partitions.csv
	arduino --verbose --verify \
		--board esp32:esp32:adafruit_feather_esp32s3 \
		--pref build.path=BuildSCALECAL8M \
		--pref upload.maximum_size=4194304\
		--pref build.flash_size=8MB \
		$(NAU7802TEST)
		
upload8M: $(TARGET8M)
	arduino --upload --board esp32:esp32:adafruit_feather_esp32s3 \
	--pref build.path=Build8M --port /dev/ttyUSB0 \
	--pref upload.maximum_size=4194304 --pref build.flash_size=8MB $(INO)

upload4M: $(TARGET4M)
	arduino --upload --board esp32:esp32:adafruit_feather_esp32s3 \
	--pref build.path=Build4M --port /dev/ttyUSB0 \
	--pref upload.maximum_size=2097152 --pref build.flash_size=4MB $(INO)

uploadSCALECAL8M: $(NAU7802TEST8M)
	arduino --upload --board esp32:esp32:adafruit_feather_esp32s3 \
	--pref build.path=BuildSCALECAL8M \
	--port /dev/ttyUSB0 \
	--pref upload.maximum_size=4194304 --pref build.flash_size=8MB \
	$(NAU7802TEST)

Revision.h: FORCE
	python3 ./Revision.py -d -t -H -U

FORCE:
