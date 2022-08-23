import cv2 as cv

from calibrador import Calibrador

path = "/home/pauwels/Documents/Sync/UFABC/PGC/pgc"

cam_e = cv.VideoCapture(2)
cam_d = cv.VideoCapture(0)

dist_cam = 11      # Distancia entre o centro das cameras em cm (ajustar)
f_cam = 6          # Distancia focal em mm (ajustar)
campo_cam = 56.6   # Campo de visao em graus (ajustar)

calib = Calibrador(path + '/exp/stereo-match/stereoMap.xml')

while (True):
    _, frame_e = cam_e.read()
    _, frame_d = cam_d.read()

    # Aplicar filtro