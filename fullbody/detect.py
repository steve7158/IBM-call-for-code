# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import csv
import camera_perspective

csv_file=open('detected_data.csv','w+')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Latitudes', 'Longitudes'])

imagePath='images/person_104.bmp'
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

image = cv2.imread(imagePath)
image = imutils.resize(image, width=min(400, image.shape[1]))
orig = image.copy()

# detect people in the image
(rects, weights) = hog.detectMultiScale(image,winStride=(4, 4),padding=(8, 8),scale=1.05)

rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

# draw the final bounding boxes
for (xA, yA, xB, yB) in pick:
    cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
    print('({},{})'.format(xB/2,yB/2))
    center_x = xB/2
    center_y = yB/2
    x_percent=center_x/(image.shape[1])
    y_percent=center_y/image.shape[0]
    lat, longi=camera_perspective.make_coordinates(x_percent, y_percent)
    csv_writer.writerow([lat, longi])
