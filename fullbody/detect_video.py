# import the necessary packages
from __future__ import print_function
import pickle
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import csv
import camera_perspective
import sqlite3

connection=sqlite3.connect('camera_cord.db')
c=connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS survial_found(longitude_x INT, latitude_y INT, imagePath TEXT(40));")


video_capture=cv2.VideoCapture('videos/video.mp4')

# csv_file=open('detected_data.csv','w+')
# csv_writer=csv.writer(csv_file)
# csv_writer.writerow(['Latitudes', 'Longitudes'])

# imagePath='images/person_104.bmp'
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
Latitudes_all=[]
Longitudes_all=[]
image_paths=[]
previous_lat=0
previous_longi=0
image_classification=[]
previous_frame_latitude_top=1000
previous_frame_latitude_bottom=1000
previous_frame_longitude_right=1000
previous_frame_longitude_left=1000

i=0
try:
    while (video_capture.isOpened()):
        # image = cv2.imread(imagePath)
        ret, frame=video_capture.read()
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))


    # detect people in the image
        (rects, weights) = hog.detectMultiScale(frame,winStride=(4, 4),padding=(8, 8),scale=1.05)
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        current_frame_latitude_bottom, current_frame_longitude_left, current_frame_latitude_top, current_frame_longitude_right=camera_perspective.frame_coordinate()
        # print(current_frame_latitude_bottom, current_frame_longitude_left, current_frame_latitude_top, current_frame_longitude_right)

        if current_frame_latitude_bottom<previous_frame_latitude_bottom-0.003147354 or current_frame_latitude_top>previous_frame_latitude_top+0.003147354 or current_frame_longitude_left<previous_frame_longitude_left-0.001579 or current_frame_longitude_right>previous_frame_longitude_right+0.001579:
            previous_frame_latitude_top=current_frame_latitude_top
            previous_frame_latitude_bottom=current_frame_latitude_bottom
            previous_frame_longitude_left=current_frame_longitude_left
            previous_frame_longitude_right=current_frame_longitude_right

            temp_filename='survial_images/{}.png'.format(i)
            cv2.imwrite(temp_filename, frame)
    # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                # print('({},{})'.format(xB/2,yB/2))
                center_x = xB/2
                center_y = yB/2
                x_percent=center_x/(frame.shape[1])
                y_percent=center_y/frame.shape[0]
                lat, longi=camera_perspective.make_coordinates(x_percent, y_percent)
                print(type(lat))

                previous_lat=lat
                previous_longi=longi
                Latitudes_all.append(lat)
                Longitudes_all.append(longi)
                print('Rectangle Done')
            image_paths.append(temp_filename)
            i=i+1
            # camera_perspective.change_coordinate()
            print('Frame of interest; Done')

        if ret==True:
            cv2.imshow('frame',frame)

        if cv2.waitKey(25) & 0xFF==ord('q'):
            break
except Exception as e:
    print ('error opening the file: ', e)

print(len(Latitudes_all), len(Longitudes_all))
with open("Latitudes.pickled",'wb') as out_file:
    pickle.dump(Latitudes_all, out_file)

with open("Longitudes.pickled",'wb') as out_file_2:
    pickle.dump(Latitudes_all, out_file_2)

with open('Image_paths.pickled', 'wb') as out_file_3:
    pickle.dump(image_paths, out_file_3) 
