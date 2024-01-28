
import cv2
import numpy as np
import glob
import os
import pickle
import math
import random
from datetime import datetime

# 1er PASO -> DEtección de las esquinas del tablero
def find_obj(x = 11, y = 11):
    ################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################
    # chessboardSize = (8,6)  #(columnas, filas)
    chessboardSize = (x, y)  #(columnas, filas)
    # Valor de tablero debe ser 1 abajo
    # Ejemplo: El utilizado para esta prueba es de 9x7
    # FONDO DE TABLERO DEBE SER BLANCO

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    print(criteria)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    # size_of_chessboard_squares_mm = 20
    size_of_chessboard_squares_mm = 10
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    files = os.getcwd() + "/temp/calibrar/*.png"
    # print(files)
    images = glob.glob(files)
    # print(images)

    ##### EXAMPLE ####
    #images = ['/home/deltaassysbot/Documentos/Delta-SVA/Interfaz/example/calib2.png']
    #print(len(images))
    # print(images[0])
    # img = cv2.imread(images[0])
    # cv2.imshow('IMG', img)
    # cv2.waitKey(0)
    ##################

    for num in range(len(images)):
        print(num)
        img = cv2.imread(images[num])
        #cv2.imshow('IMG', img)

        # lwr = np.array([0, 0, 143])
        # upr = np.array([179, 61, 252])
        lwr = np.array([0, 0, 180])
        upr = np.array([179, 61, 252])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        msk = cv2.inRange(hsv, lwr, upr)

        # cv2.imshow('MSK', msk)
        name_msk = 'MSK' + str(num + 1) + '.png'
        cv2.imwrite(name_msk, msk)
        old_msk = os.getcwd() + '/' + name_msk  
        new_msk = os.getcwd() + "/temp/calibrar/msk/" + name_msk
        os.rename(old_msk, new_msk)

        ret, corners = cv2.findChessboardCorners(msk, chessboardSize, None)
        errors = []
        print(f"ret: {ret}")

        # If found, add object points, image points (after refining them)
        if ret == True:

            objpoints.append(objp)
            fix_corners = cv2.cornerSubPix(msk, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboardSize, fix_corners, ret)
            # cv2.imshow('img', img)
            name_corners = 'corners' + str(num + 1) + '.png'
            cv2.imwrite(name_corners, img)
            old_corners = os.getcwd() + '/' + name_corners
            new_corners = os.getcwd() + "/temp/calibrar/corners/" + name_corners
            os.rename(old_corners, new_corners)
            print("SIUUU")
            # cv2.waitKey(0)
        else:
            errors.append(images[num])

    print("END")
    return images, objpoints, imgpoints

def calibration(objpoints, imgpoints):
    ############## CALIBRATION #######################################################
    frameSize = (640,480)
    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
    # print()
    # print(ret)
    # print()
    # print(cameraMatrix)
    # print()
    # print(dist)
    # print()
    # print(rvecs)
    # print()
    # print(tvecs)
    # print()

    # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
    calib_name = os.getcwd() + '/calibration.pkl'
    camMatrix = os.getcwd() + '/cameraMatrix.pkl'
    dist_name = os.getcwd() + '/dist.pkl'
    pickle.dump((cameraMatrix, dist), open(calib_name , "wb" ), protocol = 2)
    pickle.dump(cameraMatrix, open(camMatrix, "wb" ), protocol = 2)
    pickle.dump(dist, open( dist_name, "wb" ), protocol = 2)

    return cameraMatrix, dist, rvecs, tvecs


def undistort(images, cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints):
    ############## UNDISTORTION #####################################################
    for num in range(len(images)):
        img = cv2.imread(images[num])
        h,  w = img.shape[:2]
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

        # Undistort
        dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        name_u1 = 'u1_' + str(num + 1) + '.png'
        ubi = os.getcwd() + "/temp/calibrar/undist1/" + name_u1
        cv2.imwrite(ubi, dst)

        # Undistort with Remapping
        mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        name_u2 = 'u2_' + str(num + 1) + '.png'
        ubi = os.getcwd() + "/temp/calibrar/undist2/" + name_u2
        cv2.imwrite(ubi, dst)

        # Reprojection Error
        mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    print( "total error: {}".format(mean_error/len(objpoints)) )


def generate_undistort(image, type = 0):
    # Read in the saved objpoints and imgpoints
    calib_name = os.getcwd() + '/calibration.pkl'
    cameraMatrix, dist = pickle.load(open(calib_name, "rb" ))
    #dist_pickle = pickle.load( open( "wide_dist_pickle.p", "rb" ) )

    # Read in an image
    img = cv2.imread(image)
    ho,  wo = img.shape[:2]
    #print(f"{h} {w}")
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (wo,ho), 1, (wo,ho))

    # Undistort
    if type == 0:
        undistorted = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    else:
        # Undistort with Remapping
        mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (wo,ho), 5)
        undistorted = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    #print(roi)
    undistorted = undistorted[y:y+h, x:x+w]
    undistorted = cv2.resize(undistorted,(wo,ho))
    fecha = datetime.now()
    fecha = fecha.strftime("%Y%m%d_%H%M%S")
    name = 'undistorted' + fecha + '.png'
    ubi = os.getcwd() + "/temp/" + name
    cv2.imwrite(ubi, undistorted)
    return ubi


def pixel_mm(undistort, x, y, mm): 
    points = [] # 2d points in image plane.
    img = cv2.imread(undistort)

    # lwr = np.array([0, 0, 143])
    # upr = np.array([179, 61, 252])
    lwr = np.array([0, 0, 180])
    upr = np.array([179, 61, 252])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    msk = cv2.inRange(hsv, lwr, upr)
    # cv2.imshow('MSK', msk)

    chessboardSize = (x,y)  #(columnas, filas)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, corners = cv2.findChessboardCorners(msk, chessboardSize, None)
    if ret == True:
        points.append(corners)

    print()
    print(np.array(points).shape)
    print()

    d = []

    for j in range(chessboardSize[0]):
        for i in range(chessboardSize[1] - 1):
            # tv = f"V: {j + i * 8} {j + (i + 1) * 8}"
            # print(tv)
            xiv = points[0][j + i * 8][0][0] - points[0][j + (i + 1) * 8][0][0]
            yiv = points[0][j + i * 8][0][1] - points[0][j + (i + 1) * 8][0][1]
            x2v = math.pow(xiv, 2)
            y2v = math.pow(yiv, 2)
            dv = math.sqrt(x2v + y2v)
            #print(dv)
            d.append(dv)

    for j in range(chessboardSize[1]):
        for i in range(chessboardSize[0] - 1):
            # th = f"H: {i + (j * 8)} {(i + 1) + (j * 8)}"
            # print(th)
            xih = points[0][i + (j * 8)][0][0] - points[0][(i + 1) + (j * 8)][0][0]
            yih = points[0][i + (j * 8)][0][1] - points[0][(i + 1) + (j * 8)][0][1]
            x2h = math.pow(xih, 2)
            y2h = math.pow(yih, 2)
            dh = math.sqrt(x2h + y2h)
            #print(dh)
            d.append(dh)

    # print(d)
    print(f"SIZE: {len(d)}")
    print(f"MAX: {max(d)}")
    print(f"MIN: {min(d)}")
    prom = sum(d)/len(d)
    print(f"PROM: {prom}")

    pix = prom/mm
    print(f"PIX per mm: {pix}")

    return pix


def contornos(example):
    img = cv2.imread(example)
    cv2.imwrite('/home/deltaassysbot/Documentos/ORIGINAL.png', img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('/home/deltaassysbot/Documentos/GRAY.png', gray)

    blur = cv2.GaussianBlur(gray, (3,3), 0)
    cv2.imwrite('/home/deltaassysbot/Documentos/BLUR.png', blur)

    lw = 30
    ratio = 3
    kernel = 3
    canny = cv2.Canny(blur, lw, lw * ratio, kernel)
    cv2.imwrite('/home/deltaassysbot/Documentos/CANNY.png', canny)

    (contornos, _) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #(contornos, _) = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    con = cv2.drawContours(img, contornos, -1, (0, 255, 0), 2)
    cv2.imwrite('/home/deltaassysbot/Documentos/CONTORNOS.png', con)

    contours_poly = [None]*len(contornos)
    boundRect = [None]*len(contornos)
    for i, c in enumerate(contornos):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
 
    drawing = np.zeros((canny.shape[0], canny.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contornos)):
        color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
        cv2.drawContours(drawing, contours_poly, i, color)
        cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
    
    
    cv2.imwrite('/home/deltaassysbot/Documentos/RECT.png', drawing)


# images, objpoints, imgpoints = find_obj(11, 11)
# print(str(len(objpoints)) + ", " + str(len(imgpoints)))
# cameraMatrix, dist, rvecs, tvecs = calibration(objpoints, imgpoints)
# undistort(images, cameraMatrix, dist, rvecs, tvecs, objpoints, imgpoints)

#pix = pixel_mm("/home/deltaassysbot/Documentos/Delta-SVA/temp/calibrar/undist2/u2_3.png", 21)
#example = "/home/deltaassysbot/Documentos/Delta-SVA/temp/example.png"
#example = "/home/deltaassysbot/Documentos/Delta-SVA/temp/hex.png"
#contornos(example)
