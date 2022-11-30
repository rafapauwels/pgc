import math
import numpy as np

# distancia = offset*focal/disparidade
# x_pixel = f*(X/Z) + c_x
# y_pixel = f*(Y/Z) + c_y
def calcular_distancia(centro_e, frame_e, centro_d, frame_d, Q):
    _, width, _ = frame_e.shape
    focal_mm = 6.22
    sensor_width = 5.14
    distancia_cameras = 9.5

    # F(pixels) = F(mm) * im_width / sensor_width
    focal_pixel = focal_mm * width / sensor_width

    x_e = centro_e[0]
    y_e = centro_e[1]
    x_d = centro_d[0]

    disparidade = x_e - x_d
    X, Y, Z, dist = 0, 0, 0, 0
    if (disparidade != 0):
        dist = abs((distancia_cameras * focal_pixel) / disparidade)
        X = (x_e / focal_pixel) * dist
        Y = (y_e / focal_pixel) * dist

    return X, Y, dist, dist