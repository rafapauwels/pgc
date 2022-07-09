import cv2 as cv
import numpy as np

from parametros import Parametros

def main():
    camera_esquerda = cv.VideoCapture(0)
    camera_direita = cv.VideoCapture(0)

    ### CARREGA PARAMETROS DO PATH
    p = Parametros('/home/pauwels/Documents/pgc/exp/camera-calib/calibration-data')

    ### CRIA CAMERAS CALIBRADAS
    camera_esquerda_nova, camera_direita_nova = calibrar(p, camera_esquerda, camera_direita)

    stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)

    while (True):
        ret_esquerda, frame_esquerda = camera_esquerda.read()
        ret_direita, frame_direita = camera_direita.read()

        ### REMOVE DISTORCAO USANDO CAMERAS CALIBRADAS E PARAMETROS DAS CAMERAS
        frame_esquerda = cv.undistort(frame_esquerda, p.mtx_esquerda, p.dist_esquerda, None, camera_esquerda_nova)
        frame_direita = cv.undistort(frame_direita, p.mtx_direita, p.dist_direita, None, camera_direita_nova)

        disparity = stereo.compute(frame_esquerda, frame_direita)

        cv.imshow('Esquerda', frame_esquerda)
        cv.imshow('Direita', frame_direita)
        cv.imshow('Disparity', disparity)

    
def calibrar(p, camera_esquerda, camera_direita):
    w_esquerda = int(camera_esquerda.get(3))
    h_esquerda = int(camera_esquerda.get(4))
    w_direita = int(camera_direita.get(3))
    h_direita = int(camera_direita.get(4))

    camera_esquerda_nova = cv.getOptimalNewCameraMatrix(p.mtx_esquerda, p.dist_esquerda, (w_esquerda, h_esquerda), 1, (w_esquerda, h_esquerda))
    camera_direita_nova = cv.getOptimalNewCameraMatrix(p.mtx_direita, p.dist_direita, (w_direita, h_direita), 1, (w_direita, h_direita))

    return camera_esquerda_nova, camera_direita_nova

main()