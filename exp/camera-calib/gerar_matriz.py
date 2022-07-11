import numpy as np
import cv2 as cv
import glob
import os

def main():
    gerar_matriz("esquerda")
    gerar_matriz("direita")

def gerar_matriz(lado):
    # tamanhoChess = (24,17)
    tamanhoChess = (5,5)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((tamanhoChess[0] * tamanhoChess[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:tamanhoChess[0],0:tamanhoChess[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    path = '/home/pauwels/Documents/pgc/exp/camera-calib'
    images = glob.glob(path + '/calibration-pics/*' + str(lado) +  '.png')

    count = 0
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, tamanhoChess, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            count += 1
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, tamanhoChess, corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(3000)

    if count == 0:
        print("O padrao nao foi encontrado em nenhuma imagem")
    else:
        cv.destroyAllWindows()

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        np.savetxt(path + '/calibration-data/ret.' + str(lado), [ret])
        np.savetxt(path + '/calibration-data/mtx.' + str(lado), mtx)
        np.savetxt(path + '/calibration-data/dist.' + str(lado), dist)
        # np.savetxt(path + '/rvecs.param', rvecs) # Arrumar export de array 3d
        # np.savetxt(path + '/tvecs.param', tvecs)

        ## UNDISTORT

        # frame = cv.imread('teste.png') # trocar para cam
        # h, w = frame.shape[:2]esquerda
        # newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

        # dst = cv.undistort(frame, mtx, dist, None, newcameramtx)

        # x, y, w, h = roi
        # dst = dst[y:y+h, x:x+w]
        # cv.imwrite('resultado.png', dst)

main()