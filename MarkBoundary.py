# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:44:14 2022

@author: Ishwar
"""

import cv2
from rembg import remove
import imutils


input_path = "Test2.jpg"
flag= None
image = None

while flag!='q':
	#Read image as per the key_press
    if flag==None:
        image = cv2.imread(input_path)
    elif flag=='clear':
        image = cv2.imread(input_path)
    else:
        image = cv2.imread('recent_saved.jpg')

	# Select Region of Interest
    print("Select your Region of Interest and press 'Enter'.")
    r = cv2.selectROI("Select the area", image)
    print('r is of type : ',type(r))

	# Crop image
    clip_start_x = int(r[1])
    clip_start_y = int(r[0])
    cropped_image = image[clip_start_x:int(r[1]+r[3]),
						clip_start_y:int(r[0]+r[2])]

    bg_removed_img = remove(cropped_image) #rembg function

	#Start edge detection
    img_gray = cv2.cvtColor(bg_removed_img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
	# threshold the image, then perform a series of erosions +
	# dilations to remove any small regions of noise
    # Image sharpening
    thresh = cv2.threshold(img_gray, 0, 50, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
	# find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    for con in c:
        con[0][0] += clip_start_y #start_x
        con[0][1] += clip_start_x #start_y

    cv2.drawContours(image=image, contours=c, contourIdx=-1, color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.imwrite("recent_saved.jpg", image)
    print('Contour in selected area is drawn.')
    cv2.destroyAllWindows()
    
    cv2.imshow('Window for keywait',image)

    print("Press: 'Enter'->Continue, 'c'->Clear, 'q'->Quit application.")
    key_press = cv2.waitKey(0)
    if(key_press==113):
        flag='q'
    elif(key_press==99):
        flag='clear'
    elif(key_press==13):
        flag='contin'
    cv2.destroyAllWindows()
print('Changed image available in directory of program file..')
    