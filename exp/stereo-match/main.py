import math
import cv2 as cv
import numpy as np
import imutils
import matplotlib.pyplot as plt

from calibrador import Calibrador

def main():
    path = "/home/pauwels/Documents/Sync/UFABC/PGC/pgc"

    # Gráfico 3D
    # plt.ion()
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.set_xlim3d(0, 800)
    # ax.set_ylim3d(0, 100)
    # ax.set_zlim3d(0, 800)

    cam_e = cv.VideoCapture(0)
    cam_d = cv.VideoCapture(2)

    dist_cam = 10      # Distancia entre o centro das cameras em cm (ajustar)
    f_cam = 6.858          # Distancia focal em mm (ajustar)
    campo_cam = 78   # Campo de visao em graus (ajustar)

    # calib = Calibrador(path + '/exp/stereo-match/stereoMap.xml')

    disable = False

    while (True):
        _, frame_ori_e = cam_e.read()
        _, frame_ori_d = cam_d.read()

        # Diminuir ruído
        frame_blur_e = cv.GaussianBlur(frame_ori_e, (5,5), 0)
        frame_blur_d = cv.GaussianBlur(frame_ori_d, (5,5), 0)

        # Localizar centro do objeto nas duas imagens
        obj_e = findCircle(frame_blur_e)
        obj_d = findCircle(frame_blur_d)

        # cv.imshow('DIREITA', frame_blur_d)

        m = hsv_filter(frame_blur_e)
        cv.imshow("mask", m)
        cv.imshow("bitwise esq", cv.bitwise_and(frame_blur_e, frame_blur_e, mask=m))
        cv.imshow("filtro dir", hsv_filter(frame_ori_d))

        key = cv.waitKey(1)
        if  key & 0xFF == ord('q'):
            break

        # Triangular
        # F(mm) = F(pixels) * SensorWidth(mm) / ImageWidth (pixel).
        # F(mm) * Width / SensorWidth = F(pixels)
        if (disable or obj_e == None or obj_d == None):
            continue

        heigh, width, depth = frame_ori_e.shape
        # f_pixel = (width * 0.5) / np.tan(campo_cam * 0.5 * np.pi/180)
        f_pixel = f_cam * width / 6
        print(heigh, width, depth)
        x_e = obj_e[0]
        x_d = obj_d[0]

        disparidade = x_e - x_d
        dist = abs((dist_cam * f_pixel) / disparidade)

        # draw3D(pos_x, dist, pos_y, fig, ax)

        print(dist)
        cv.putText(frame_blur_e, str(round(dist, 3)), (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA)
        cv.imshow('ESQUERDA', frame_blur_e)

def findArUco(frame):
    return 0,0

def draw3D(x, y, z, fig, ax):
    ax.scatter(x, y, -z)
    plt.draw()
    plt.pause(0.1)
    # ax.cla()

def findQr(frame, detector):
    _, points, _ = detector.detectAndDecode(frame)
    return points

# Encontra maior circulo verde dentro do frame
def findCircle(frame):
    # Filtra cor verde
    mascara = hsv_filter(frame)

    contornos = cv.findContours(mascara.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contornos = imutils.grab_contours(contornos)
    centro = None

    if len(contornos) > 0:
        c = max(contornos, key=cv.contourArea)
        ((x, y), r) = cv.minEnclosingCircle(c)
        M = cv.moments(c)

        try: # Investigar Exception has occurred: ZeroDivisionError
            centro = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        except:
            centro = None

        if r > 10:
            cv.circle(frame, (int(x), int(y)), int(r), (255, 0, 255), 5)

    return centro

# https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/
def hsv_filter(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Boundaries encontradas com hsvcheck.py    
    green_lower = np.array([66, 117, 125])
    green_upper = np.array([90, 255, 200])

    green_mask = cv.inRange(hsv, green_lower, green_upper)

    # Operacoes morpho para reduzir ruidos
    green_mask = cv.erode(green_mask, None, iterations=2)
    green_mask = cv.dilate(green_mask, None, iterations=2)

    return green_mask

    # lower boundary RED color range values; Hue (0 - 10)
    # lower1 = np.array([0, 100, 20])
    # upper1 = np.array([10, 255, 255])
    
    # upper boundary RED color range values; Hue (160 - 180)
    # lower2 = np.array([160,50,50])
    # upper2 = np.array([179,255,255])

main()