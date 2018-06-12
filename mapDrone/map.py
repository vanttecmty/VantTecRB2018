# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math


'''

	READ:

--- LAS IMAGENES DEL DRON SON EN ASPECT RATIO DE 16:9 CON UNA RESOLUCION DE 5472 X 3648 
	Y LOS CALCULOS SE HACEN EN BASE A ESTOS REQUERIMIENTOS.

--- DOCUMENTACION:

	https://stackoverflow.com/questions/17499409/opencv-calculate-angle-between-camera-and-pixel
	https://stackoverflow.com/questions/47896876/camera-intrinsic-matrix-for-dji-phantom-4?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
	https://phantompilots.com/threads/p4p-lens-field-of-view.114160/
	DJI must state that 84º is diagonal FOV 
	3:2 Aspect Ratio: 5472×3648
	4:3 Aspect Ratio: 4864×3648  
	16:9 Aspect Ratio: 5472×3078

--- MATH
	B = (math.tan(H)*H)*2

--- CONSTANTS

	WIDTH  = 5472.0   640.0  = 8.55 ratio
	HEIGTH = 3648.0   480.0  = 7.6
	ANGLE_PER_PIXEL_H = FOV_H/HEIGTH 
	ANGLE_PER_PIXEL_V = FOV_V/WIDTH
	FOV_V = 53.0
	FOV_H = 67.0
	HEIGTH_DRONE = 20.0 meters
'''





WIDTH  = 5472.0
HEIGTH = 3648.0
FOV_V  = 45.7 * 0.0174533
FOV_H  = 73.7 * 0.0174533
ANGLE_PER_PIXEL_H = FOV_H/WIDTH
ANGLE_PER_PIXEL_V = FOV_V/HEIGTH 
HEIGTH_DRONE = 20.0

#Calculo de metros en las coordenadas

def getDistanceFieldOfView(H,FOV_H,FOV_V):
	
	XDIST = int(math.tan(FOV_H/2)*H*2)
	YDIST = int(math.tan(FOV_V/2)*H*2)
	print("FIELD OF VIEW IN METERS HORIZONTAL:" + str(XDIST))
	print("FIELD OF VIEW IN METERS VERTICAL:" + str(YDIST))
	DIST = [XDIST,YDIST]
	return DIST


def map():

	MIN_THRESH = 0.0

	#READ GRAYSCALE
	img_big_size = cv2.imread('DJI_0418.JPG', 0)
	#RESIZE
	img_noblur =  cv2.resize(img_big_size, (640,480 ))
	height, width = img_noblur.shape
	#READ RGB
	img_bgr_big_size = cv2.imread('DJI_0418.JPG', 1)
	img_bgr =   cv2.resize(img_bgr_big_size, (640,480 ))
	img_ori = img_bgr.copy()
	#BLURR GRAYSCALE
	img = cv2.blur(img_noblur, (7,7)) 

	#THRESHOLD HSV
	hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
	img_hsv = cv2.inRange(hsv, (59, 69, 0), (255, 255,255))

	#CANNY AND DILATE
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	canny_edge = cv2.Canny(img, 100, 80)
	dilated = cv2.dilate(canny_edge, kernel)

	#SUM THEM UP
	final =  cv2.add(img_hsv , dilated)

	#Get contours
	image, contours0, hierarchy  = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	#Get moments
	moments  = [cv2.moments(cnt) for cnt in contours0]
	# Nota Bene: I rounded the centroids to integer.

	centroids = []
	for i,m in enumerate(moments):
		if cv2.contourArea(contours0[i]) > MIN_THRESH:
			centroids.append((int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00']))))


	total_meters_xy = getDistanceFieldOfView(HEIGTH_DRONE,FOV_H,FOV_V)
	total_meters_x = total_meters_xy[0]
	total_meters_y = total_meters_xy[1]

	#Draw contours
	output = []
	for c in centroids:
		# I draw a black little empty circle in the centroid position
		cv2.circle(img_bgr,c,5,(255,0,0),-1)

		y_modified = 480 - c[1]
		x = int(  ((c[0] * total_meters_x * 8.55)/WIDTH) )
		y = int(((y_modified * total_meters_y * 7.6)/HEIGTH))
		cv2.putText(img_bgr, "(" + str(x) + "," + str(y) + ")", (c[0],c[1]), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0,0))
		output.append((x,y))
	
	

	cv2.imshow('HSV TH',img_hsv)
	cv2.imshow('CENTERS',img_bgr)
	cv2.imshow('ORIGINAL',img_ori)
	cv2.imshow('DILATED TH', dilated)
	cv2.imshow('FINAL', final)
	cv2.waitKey(0)

	return output


result = map()
for i in result:
		print i

