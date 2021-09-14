EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:74ahc123a
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L 74AHC123A U?
U 1 1 6140A7CA
P 3000 2100
F 0 "U?" H 3000 2200 60  0000 C CNN
F 1 "74AHC123A" H 3000 2100 60  0000 C CNN
F 2 "" H 3000 2100 60  0001 C CNN
F 3 "" H 3000 2100 60  0001 C CNN
	1    3000 2100
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 6140A866
P 2000 2200
F 0 "R?" V 2080 2200 50  0000 C CNN
F 1 "650 1%" V 2000 2200 50  0000 C CNN
F 2 "" V 1930 2200 50  0001 C CNN
F 3 "" H 2000 2200 50  0001 C CNN
	1    2000 2200
	0    1    1    0   
$EndComp
$Comp
L C_Small C?
U 1 1 6140A88C
P 2300 2300
F 0 "C?" H 2310 2370 50  0000 L CNN
F 1 "100 nf 1%" H 2310 2220 50  0000 L CNN
F 2 "" H 2300 2300 50  0001 C CNN
F 3 "" H 2300 2300 50  0001 C CNN
	1    2300 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 2200 2500 2200
Connection ~ 2300 2200
Wire Wire Line
	2300 2400 2500 2400
$Comp
L +3.3V #PWR?
U 1 1 6140A8D3
P 3000 1300
F 0 "#PWR?" H 3000 1150 50  0001 C CNN
F 1 "+3.3V" H 3000 1440 50  0000 C CNN
F 2 "" H 3000 1300 50  0001 C CNN
F 3 "" H 3000 1300 50  0001 C CNN
	1    3000 1300
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR?
U 1 1 6140A8FC
P 1850 1700
F 0 "#PWR?" H 1850 1550 50  0001 C CNN
F 1 "+3.3V" H 1850 1840 50  0000 C CNN
F 2 "" H 1850 1700 50  0001 C CNN
F 3 "" H 1850 1700 50  0001 C CNN
	1    1850 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 1300 3000 1500
Wire Wire Line
	1850 1700 1850 2200
$Comp
L GND #PWR?
U 1 1 6140A946
P 3000 2900
F 0 "#PWR?" H 3000 2650 50  0001 C CNN
F 1 "GND" H 3000 2750 50  0000 C CNN
F 2 "" H 3000 2900 50  0001 C CNN
F 3 "" H 3000 2900 50  0001 C CNN
	1    3000 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 2900 3000 2700
$Comp
L GND #PWR?
U 1 1 6140A982
P 2300 1750
F 0 "#PWR?" H 2300 1500 50  0001 C CNN
F 1 "GND" H 2300 1600 50  0000 C CNN
F 2 "" H 2300 1750 50  0001 C CNN
F 3 "" H 2300 1750 50  0001 C CNN
	1    2300 1750
	0    1    1    0   
$EndComp
Wire Wire Line
	2500 1750 2300 1750
$Comp
L R R?
U 1 1 6140A9BF
P 2250 1950
F 0 "R?" V 2330 1950 50  0000 C CNN
F 1 "10K" V 2250 1950 50  0000 C CNN
F 2 "" V 2180 1950 50  0001 C CNN
F 3 "" H 2250 1950 50  0001 C CNN
	1    2250 1950
	0    1    1    0   
$EndComp
Wire Wire Line
	2500 1950 2400 1950
Wire Wire Line
	2100 1950 1850 1950
Connection ~ 1850 1950
$Comp
L Conn_01x04_Male J?
U 1 1 6140AA3B
P 1250 1900
F 0 "J?" H 1250 2100 50  0000 C CNN
F 1 "Input" H 1250 1600 50  0000 C CNN
F 2 "" H 1250 1900 50  0001 C CNN
F 3 "" H 1250 1900 50  0001 C CNN
	1    1250 1900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 6140AA74
P 1450 2400
F 0 "#PWR?" H 1450 2150 50  0001 C CNN
F 1 "GND" H 1450 2250 50  0000 C CNN
F 2 "" H 1450 2400 50  0001 C CNN
F 3 "" H 1450 2400 50  0001 C CNN
	1    1450 2400
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 6140AAAB
P 1450 1600
F 0 "#PWR?" H 1450 1450 50  0001 C CNN
F 1 "+5V" H 1450 1740 50  0000 C CNN
F 2 "" H 1450 1600 50  0001 C CNN
F 3 "" H 1450 1600 50  0001 C CNN
	1    1450 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1450 1800 1450 1600
Wire Wire Line
	1450 1900 1850 1900
Connection ~ 1850 1900
Wire Wire Line
	1450 2100 1450 2400
Wire Wire Line
	1450 2000 1700 2000
Wire Wire Line
	1700 2000 1700 1850
Wire Wire Line
	1700 1850 2500 1850
NoConn ~ 3500 2400
$Comp
L R R?
U 1 1 6140AB96
P 3800 1750
F 0 "R?" V 3880 1750 50  0000 C CNN
F 1 "1K" V 3800 1750 50  0000 C CNN
F 2 "" V 3730 1750 50  0001 C CNN
F 3 "" H 3800 1750 50  0001 C CNN
	1    3800 1750
	0    1    1    0   
$EndComp
Wire Wire Line
	4100 1750 3950 1750
Wire Wire Line
	3650 1750 3500 1750
$Comp
L R R?
U 1 1 6140AC25
P 4400 1250
F 0 "R?" V 4480 1250 50  0000 C CNN
F 1 "1K" V 4400 1250 50  0000 C CNN
F 2 "" V 4330 1250 50  0001 C CNN
F 3 "" H 4400 1250 50  0001 C CNN
	1    4400 1250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 1400 4400 1550
$Comp
L +5V #PWR?
U 1 1 6140AC92
P 4400 800
F 0 "#PWR?" H 4400 650 50  0001 C CNN
F 1 "+5V" H 4400 940 50  0000 C CNN
F 2 "" H 4400 800 50  0001 C CNN
F 3 "" H 4400 800 50  0001 C CNN
	1    4400 800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 800  4400 1100
$Comp
L GND #PWR?
U 1 1 6140ACD4
P 4400 2200
F 0 "#PWR?" H 4400 1950 50  0001 C CNN
F 1 "GND" H 4400 2050 50  0000 C CNN
F 2 "" H 4400 2200 50  0001 C CNN
F 3 "" H 4400 2200 50  0001 C CNN
	1    4400 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 1950 4400 2200
$Comp
L R R?
U 1 1 6140AE97
P 5000 850
F 0 "R?" V 5080 850 50  0000 C CNN
F 1 "1K" V 5000 850 50  0000 C CNN
F 2 "" V 4930 850 50  0001 C CNN
F 3 "" H 5000 850 50  0001 C CNN
	1    5000 850 
	0    1    1    0   
$EndComp
$Comp
L C_Small C?
U 1 1 6140AF27
P 5750 1050
F 0 "C?" H 5760 1120 50  0000 L CNN
F 1 ".1 uf" H 5760 970 50  0000 L CNN
F 2 "" H 5750 1050 50  0001 C CNN
F 3 "" H 5750 1050 50  0001 C CNN
	1    5750 1050
	1    0    0    -1  
$EndComp
$Comp
L Laserdiode_1C2A LD?
U 1 1 6140AFC0
P 5300 1550
F 0 "LD?" H 5250 1725 50  0000 C CNN
F 1 "SPL PL90" H 5250 1450 50  0000 C CNN
F 2 "" H 5200 1525 50  0001 C CNN
F 3 "" H 5330 1350 50  0001 C CNN
	1    5300 1550
	0    -1   -1   0   
$EndComp
$Comp
L Q_NMOS_GDS Q?
U 1 1 6140B306
P 5200 2300
F 0 "Q?" H 5400 2350 50  0000 L CNN
F 1 "TK31N60X" H 5400 2250 50  0000 L CNN
F 2 "" H 5400 2400 50  0001 C CNN
F 3 "" H 5200 2300 50  0001 C CNN
	1    5200 2300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 6140B65C
P 5300 2700
F 0 "#PWR?" H 5300 2450 50  0001 C CNN
F 1 "GND" H 5300 2550 50  0000 C CNN
F 2 "" H 5300 2700 50  0001 C CNN
F 3 "" H 5300 2700 50  0001 C CNN
	1    5300 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 2700 5300 2500
Wire Wire Line
	5000 2300 5000 1500
Wire Wire Line
	5000 1500 4400 1500
Connection ~ 4400 1500
Wire Wire Line
	5300 2100 5300 1850
Wire Wire Line
	5300 850  5300 1350
Wire Wire Line
	4850 850  4400 850 
Connection ~ 4400 850 
Wire Wire Line
	5150 850  5750 850 
Wire Wire Line
	5750 850  5750 950 
Connection ~ 5300 850 
$Comp
L GND #PWR?
U 1 1 6140B82A
P 5750 1350
F 0 "#PWR?" H 5750 1100 50  0001 C CNN
F 1 "GND" H 5750 1200 50  0000 C CNN
F 2 "" H 5750 1350 50  0001 C CNN
F 3 "" H 5750 1350 50  0001 C CNN
	1    5750 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 1150 5750 1350
$Comp
L PN2222A Q?
U 1 1 6140AB3F
P 4300 1750
F 0 "Q?" H 4500 1825 50  0000 L CNN
F 1 "PN2222A" H 4500 1750 50  0000 L CNN
F 2 "TO_SOT_Packages_THT:TO-92_Molded_Narrow" H 4500 1675 50  0001 L CIN
F 3 "" H 4300 1750 50  0001 L CNN
	1    4300 1750
	1    0    0    -1  
$EndComp
$EndSCHEMATC
