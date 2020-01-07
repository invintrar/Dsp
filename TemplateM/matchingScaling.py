#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 05:13:53 2020

@author: Gustavo
"""

# import the necessary packages
import numpy as np
import cv2
 

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized










path='/Users/Gustavo/AnacondaProjects/pythonCode/0_Database/Varios/placas/'


 # load the image image, convert it to grayscale, and detect edges
template = cv2.imread('template.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
cv2.imshow("Template", template)

image = cv2.imread('yo3.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None
visualize=False

# loop over the scales of the image
for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
	resized = image_resize(image,width = int(gray.shape[1] * scale))
	r = gray.shape[1] / float(resized.shape[1])
 
		# if the resized image is smaller than the template, then break
		# from the loop
	if resized.shape[0] < tH or resized.shape[1] < tW:
		break
        
        # detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
	edged = cv2.Canny(resized, 50, 200)
	result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
 
		# check to see if the iteration should be visualized
	if (visualize==False):
			# draw a bounding box around the detected region
		clone = np.dstack([edged, edged, edged])
		cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
			(maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
		cv2.imshow("Visualize", clone)
		cv2.waitKey(0)
 
		# if we have found a new maximum correlation value, then update
		# the bookkeeping variable
	if found is None or maxVal > found[0]:
		found = (maxVal, maxLoc, r)
 
	# unpack the bookkeeping variable and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
 
	# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)