import time
from random import randint
from distances import get_rois_data
from darknet import execute, execute_test
import numpy as np
import cv2
from glob import glob
import os
import sys


TIME_DIVIDER = 10.0
MAX_TIME = 60

def generate_data():
    '''Funcion para generar coordenadas aleatorias de objetos'''
    result = []
    for i in range(10):
        identifier = randint(0,1)
        x1 = randint(1, 50)
        y1 = randint(50, 100)
        x2 = randint(50, 100)
        y2 = randint(1, 50)
        result.append([identifier, x1, y1, x2, y2])
    return result

def parse_data(data):
    results = []
    for val in data:
        if val[0] == 'b':
            results.append([1, val[2][0], val[2][2], val[2][1], val[2][3]])
        else:
            results.append([0, val[2][0], val[2][2], val[2][1], val[2][3]])
    return results

<<<<<<< HEAD
def call(data_calib,images):
    '''Realiza llamadas a codigo de red neuronal en C y pasa datos a codigo path.py'''
=======
def obtain_data():
>>>>>>> 6256ad92366ff80fc57d559a4c12a11590a058ec
    print('-------DATOS DARKNET------')
    data = execute() #Llama darknet
    # print(data)
    if len(data):
        data = parse_data(data)
        # print(data)
        distances = get_rois_data(data) # Obtiene datos de objetos
        # print(distances)
    else:
        print('---------Nothing detected------------')

def main():
    '''AQUI SE ARMA LA CARNE'''
    while True:
<<<<<<< HEAD
        data = execute(data_calib,images.pop(0))
        print(data)
        if len(data):
            data = parse_data(data)
            print(data)
            distances = get_rois_data(data) 
            print(distances)
=======
        print("Escribe reto")
        reto = raw_input()
        if reto == "navgps":
            # No usa vision
            continue
        elif reto == "autonav":
            obtain_data()
        elif reto == "speed":
            obtain_data()
        elif reto == "autodock":
            # No usa vision
            continue
>>>>>>> 6256ad92366ff80fc57d559a4c12a11590a058ec
        else:
            obtain_data()

<<<<<<< HEAD

def calibration():
    
    #Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #Checkboard size
    cbrow = 8
    cbcol = 6

    #Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((cbrow*cbcol,3), np.float32)
    objp[:,:2] = np.mgrid[0:cbcol,0:cbrow].T.reshape(-1,2)

    #Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob('sample_images/*.jpg')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (cbcol,cbrow),None)

        #If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            #Draw and display the corners
            img = cv2.drawChessboardCorners(img, (cbcol,cbrow), corners2,ret)
        

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    #Get new optimal camera matrix
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))



    data_calib = []
    data_calib.append(mtx)
    data_calib.append(dist)
    data_calib.append(None)
    data_calib.append(newcameramtx)

    return data_calib

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


data_calib = calibration()
print(data_calib)
images = load_images_from_folder('/home/vantec/Documents/VantTecRB2018/communications/communicator/darknet/Competencia')
call(data_calib,images)

=======
main()
>>>>>>> 6256ad92366ff80fc57d559a4c12a11590a058ec
