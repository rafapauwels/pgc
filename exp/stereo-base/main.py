from dis import dis
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import PySimpleGUI as sg

from calibrador import Calibrador

path = "/home/pauwels/Documents/Sync/UFABC/PGC/pgc"

def main():
    layout = [
        [sg.Text("Blocksize"), sg.Slider(key="blocksize", range=(-1,30), orientation='h', enable_events=True)],
        [sg.Text("Min disp"), sg.Slider(key="mindisp", range=(-128,128), orientation='h', enable_events=True)],
        [sg.Text("Max disp"), sg.Slider(key="maxdisp", range=(0,128), orientation='h', enable_events=True)],
        [sg.Text("Uniqueness"), sg.Slider(key="uniqueness", range=(5,15), orientation='h', enable_events=True)],
        [sg.Text("Speckle size"), sg.Slider(key="specklesize", range=(50,200), orientation='h', enable_events=True)],
        [sg.Text("Gauss1"), sg.Slider(key="gauss1", range=(5,50), orientation='h', enable_events=True)],
        [sg.Text("Gauss2"), sg.Slider(key="gauss2", range=(0,50), orientation='h', enable_events=True)],
    ]
    
    window = sg.Window("Controles", layout=layout)

    camera_direita = cv.VideoCapture(2)
    camera_esquerda = cv.VideoCapture(0)

    ### CARREGA CALIBRADOR COM MAPA DE PARAMS
    calib = Calibrador(path + '/exp/stereo-base/stereoMap.xml')

    block_size = 10
    min_disp = -128
    max_disp = 0
    # Maximum disparity minus minimum disparity. The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
    # Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 200
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0

    stereo = cv.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size,
        P2=32 * 1 * block_size * block_size,
    )

    while (True):
        _, frame_esquerda = camera_esquerda.read()
        _, frame_direita = camera_direita.read()

        event, values = window.read(timeout=20)

        # if event == 'blocksize':
        #     block_size = int(values['blocksize'])
        #     print("block_size: " + str(block_size))
        # elif event == 'mindisp':
        #     min_disp = int(values['mindisp'])
        #     print("min_disp: " + str(min_disp))
        # elif event == 'maxdisp':
        #     max_disp = int(values['maxdisp'])
        #     print("max_disp: " + str(max_disp))
        # elif event == 'uniqueness':
        #     uniquenessRatio = int(values['uniqueness'])
        #     print("uniquenessRatio: " + str(uniquenessRatio))
        # elif event == 'specklesize':
        #     speckleWindowSize = int(values['specklesize'])
        #     print("speckleWindowSize: " + str(speckleWindowSize))

        stereo = cv.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=block_size,
            uniquenessRatio=uniquenessRatio,
            speckleWindowSize=speckleWindowSize,
            speckleRange=speckleRange,
            disp12MaxDiff=disp12MaxDiff,
            P1=8 * 1 * block_size * block_size,
            P2=32 * 1 * block_size * block_size,
        )
        

        frame_esquerda, frame_direita = calib.acertar_frames(frame_esquerda, frame_direita)

        frame_esquerda_gray = cv.cvtColor(frame_esquerda, cv.COLOR_BGR2GRAY)
        frame_direita_gray = cv.cvtColor(frame_direita, cv.COLOR_BGR2GRAY)

        # frame_esquerda_gray = cv.GaussianBlur(frame_esquerda_gray, (5,5), cv.BORDER_DEFAULT)
        # frame_direita_gray = cv.GaussianBlur(frame_direita_gray, (5,5), cv.BORDER_DEFAULT)

        disparity = stereo.compute(frame_esquerda_gray, frame_direita_gray)

        disparity = cv.normalize(disparity, disparity, alpha=255, beta=0, norm_type=cv.NORM_MINMAX)
        disparity = np.uint8(disparity)

        cv.imshow('Esquerda', frame_esquerda)
        cv.imshow('Direita', frame_direita)

        cv.imshow('Disparity', disparity)
        
        # d = cv.erode(disparity, None, iterations=2)
        # d = cv.dilate(d, None, iterations=2)
        
        # cv.imshow('Disparity2', d)

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