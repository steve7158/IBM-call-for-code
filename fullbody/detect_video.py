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

try:
    while (video_capture.isOpened()):
        # image = cv2.imread(imagePath)
        ret, frame=video_capture.read()
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))


    # detect people in the image
        (rects, weights) = hog.detectMultiScale(frame,winStride=(4, 4),padding=(8, 8),scale=1.05)
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

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
            Latitudes_all.append(lat)
            Longitudes_all.append(longi)

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
