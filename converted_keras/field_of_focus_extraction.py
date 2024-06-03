from PIL import Image 
import cv2
import numpy as np
import pandas as pd
import csv
import os 
import collections
from detection import *
import csv

x = 0
y = 0

#df = pd.read_csv('/Users/jiya/downloads/sample1.csv')

cam = cv2.VideoCapture("/Users/jiya/downloads/D114-S3-before_gaze(s9).mp4") 

try: 
    if not os.path.exists('data'): 
        os.makedirs('data') 
except OSError: 
    print ('Error: Creating directory of data') 

currentframe = 0

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getFrame(sec, x, y):
    cam.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    print(sec)
    hasFrames,image = cam.read()
    if hasFrames:
        name = './data/frame' + str(sec) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, image) 
        n = Image.open('/Users/jiya/converted_keras/data/frame' + str(sec) + '.jpg')
        width, height = n.size
        x = x*width
        y = y*height
        #im_crop = n.crop((x-46.0, y-46.0, x+46.0, y+46.0))
        im_crop = n.crop((x-300.0, y-300.0, x+300.0, y+300.0))
        zone, zone_confidence = returnZone(im_crop)
        im_crop.save(name)
    return hasFrames, zone, zone_confidence, name

#seconds is 32, x is 23, y is 24
sec = 0
hasFrames, zone, zone_confidence, name = getFrame(sec, 0, 0)
success = hasFrames
prev = 0
with open('/Users/jiya/downloads/D114-S3-before_gaze(s9).csv') as cards:
   csv_reader = csv.DictReader(cards)
   csv_reader1 = csv.reader(cards)
   x_pos = []
   y_pos = []
   seconds_array = []
   image_name = []
   gaze = []
   gaze_confidence = []
   line = csv_reader1.line_num
   first = 0
   firstLine = csv_reader1.line_num
   repeat = True
   add = True
   count = 0
   for row in csv_reader:
        seconds = row['seconds']
        rowX = row['gaze_pos_x']
        rowY = row['gaze_pos_y']
        if is_float(seconds) and repeat:
            first = float(seconds)
            repeat = False
        if is_float(seconds) and is_float(rowX) and is_float(rowY) and success:
            if line == 0:
                prev = float(seconds) 
                line += 1
            if add:
                sec = sec + float(seconds) - first
                add = False
            else:
                sec = sec + float(seconds) - prev 
            #sec = round(sec, 2)
            hasFrames, zone, zone_confidence, name = getFrame(sec, float(rowX), float(rowY))
            success = hasFrames
            gaze.append(zone)
            gaze_confidence.append(zone_confidence)
            x_pos.append(rowX)
            y_pos.append(rowY)
            seconds_array.append(seconds)
            image_name.append(name)
            prev = float(seconds)
        else:
            gaze.append('')
            gaze_confidence.append('')



df = pd.DataFrame(list())
df['gaze_pos_x'] = x_pos
df['gaze_pos_y'] = y_pos
df['seconds'] = seconds_array
df['gaze_zone'] = gaze
df['gaze_zone_confidence'] = gaze_confidence
df.to_csv('new_data.csv')


