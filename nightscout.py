#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in13b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in13b.EPD()
    epd.init()
    print("Clear...")
    epd.Clear()
    
    svgfile = open("value.txt", "r")		#File with last mlg/dl value
    infofile = open("timeinfo.txt", "r")	#File with timestamp of last value
    directionfile = open("direction.txt", "r")  #File with direction
    oldfile = open("old.txt", "r")		#File with 1 if old values
    mgdl = svgfile.read(); 			#Fill variable mgdl
    mmol = int(mgdl)/float(18) 			#Convert mgdl to mmol
    mmol = round(mmol, 1)			#Round to 1 decimal digest
    mmolstr = str(mmol)				#Convert to string
    info = infofile.read();			#Fill variable date
    direction = directionfile.read();		#Fill variable direction
    old = oldfile.read();
    old = int(old)

    print "Drawing"
    # Drawing on the Horizontal image
    HBlackimage = Image.new('1', (epd2in13b.EPD_HEIGHT, epd2in13b.EPD_WIDTH), 255)  # 212*104 298*126
    HRedimage = Image.new('1', (epd2in13b.EPD_HEIGHT, epd2in13b.EPD_WIDTH), 255)  # 212*104 298*126

    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)
    font85 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 85)
    font20 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 20)
    if mmol > 3.9:
     drawblack.text((5, 0), mmolstr, font = font85, fill = 0)
     drawred.text((5, 80), info, font = font20, fill = 0)
    else:
     drawred.text((5, 0), mmolstr, font = font85, fill = 0)
     drawred.text((5, 80), info, font = font20, fill = 0)

    if old == 1:
     drawblack.line((5, 50, 120, 50), fill = 0, width = 7)

    print mmol
    print info

    if 'Flat' in direction:
     drawblack.line((147, 45, 207, 45), fill = 0, width = 7)
     drawblack.line((207, 45, 187, 25), fill = 0, width = 7)
     drawblack.line((207, 45, 187, 65), fill = 0, width = 7)
    elif 'FortyFiveUp' in direction:
     drawblack.line((157, 70, 207, 20), fill = 0, width = 9)
     drawblack.line((207, 20, 167, 20), fill = 0, width = 7)
     drawblack.line((207, 20, 207, 60), fill = 0, width = 7)
    elif 'FortyFiveDown' in direction:
     drawblack.line((157, 20, 207, 70), fill = 0, width = 9)
     drawblack.line((207, 70, 167, 70), fill = 0, width = 7)
     drawblack.line((207, 70, 207, 30), fill = 0, width = 7)
    elif 'SingleUp' in direction:
     drawred.line((182, 10, 182, 80), fill = 0, width = 7)
     drawred.line((182, 10, 162, 40), fill = 0, width = 9)
     drawred.line((182, 10, 202, 40), fill = 0, width = 9)
    elif 'SingleDown' in direction:
     drawred.line((182, 80, 182, 10), fill = 0, width = 7)
     drawred.line((182, 80, 162, 50), fill = 0, width = 9)
     drawred.line((182, 80, 202, 50), fill = 0, width = 9)
    elif 'DoubleUp' in direction:
     drawred.line((182, 10, 182, 80), fill = 0, width = 7)
     drawred.line((182, 10, 162, 40), fill = 0, width = 9)
     drawred.line((182, 10, 202, 40), fill = 0, width = 9)
     drawred.line((142, 10, 142, 80), fill = 0, width = 7)
     drawred.line((142, 10, 122, 40), fill = 0, width = 9)
     drawred.line((142, 10, 162, 40), fill = 0, width = 9)
    elif 'DoubleDown' in direction:
     drawred.line((182, 80, 182, 10), fill = 0, width = 7)
     drawred.line((182, 80, 162, 50), fill = 0, width = 9)
     drawred.line((182, 80, 202, 50), fill = 0, width = 9)
     drawred.line((142, 80, 142, 10), fill = 0, width = 7)
     drawred.line((142, 80, 122, 50), fill = 0, width = 9)
     drawred.line((142, 80, 162, 50), fill = 0, width = 9)
    else:
     print 'No direction found'
    epd.display(epd.getbuffer(HBlackimage.rotate(180)), epd.getbuffer(HRedimage.rotate(180)))

    time.sleep(0)
  #  epd.sleep()

except:
    svgobject = open("value.txt", "r")
    infoobject = open("timeinfo.txt", "r")
    directionobject = open("direction.txt", "r")
    oldobject = open("old.txt", "r")
    svg = svgobject.read();
    info = infoobject.read();
    direction = directionobject.read();
    old = oldobject.read();
    svgobject.close()
    infoobject.close()
    directionobject.close()
    oldobject.close()
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
