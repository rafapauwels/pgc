import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from parametros import Parametros

path = "/home/pauwels/Documents/Sync/UFABC/PGC/pgc"

def main():
    camera_esquerda = cv.VideoCapture(0)
    camera_direita = cv.VideoCapture(2)

    ### CARREGA PARAMETROS DO PATH
    p = Parametros(path + '/exp/camera-calib/calibration-data')

    ### CRIA CAMERAS CALIBRADAS
    camera_esquerda_nova, camera_direita_nova = calibrar(p, camera_esquerda, camera_direita)

    stereo = cv.StereoBM_create(numDisparities=0, blockSize=15)

    while (True):
        ret_esquerda, frame_esquerda = camera_esquerda.read()
        ret_direita, frame_direita = camera_direita.read()

        ### REMOVE DISTORCAO USANDO CAMERAS CALIBRADAS E PARAMETROS DAS CAMERAS
        # frame_esquerda = cv.undistort(frame_esquerda, p.mtx_esquerda, p.dist_esquerda, None, camera_esquerda_nova)
        # frame_direita = cv.undistort(frame_direita, p.mtx_direita, p.dist_direita, None, camera_direita_nova)

        frame_esquerda_gray = cv.cvtColor(frame_esquerda, cv.COLOR_BGR2GRAY)
        frame_direita_gray = cv.cvtColor(frame_direita, cv.COLOR_BGR2GRAY)

        disparity = stereo.compute(frame_esquerda_gray, frame_direita_gray)

        cv.imshow('Esquerda', frame_esquerda_gray)
        cv.imshow('Direita', frame_direita_gray)
        cv.imshow('Disparity', disparity)
        
        key = cv.waitKey(1)
        if  key & 0xFF == ord('q'):
            break
    
    camera_esquerda.release()
    cv.destroyAllWindows()

    
def calibrar(p, camera_esquerda, camera_direita):
    w_esquerda = int(camera_esquerda.get(3))
    h_esquerda = int(camera_esquerda.get(4))
    w_direita = int(camera_direita.get(3))
    h_direita = int(camera_direita.get(4))

    camera_esquerda_nova = cv.getOptimalNewCameraMatrix(p.mtx_esquerda, p.dist_esquerda, (w_esquerda, h_esquerda), 1, (w_esquerda, h_esquerda))
    camera_direita_nova = cv.getOptimalNewCameraMatrix(p.mtx_direita, p.dist_direita, (w_direita, h_direita), 1, (w_direita, h_direita))

    return camera_esquerda_nova, camera_direita_nova

main()