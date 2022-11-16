import math

# distancia = offset*focal/disparidade
def calcular_distancia(centro_e, frame_e, centro_d, frame_d):
    _, width, _ = frame_e.shape
    focal_mm = 6.22
    sensor_width = 5.14
    distancia_cameras = 9.5

    # F(pixels) = F(mm) * im_width / sensor_width
    focal_pixel = focal_mm * width / sensor_width

    x_e = centro_e[0]
    x_d = centro_d[0]

    disparidade = x_e - x_d
    dist = 0
    if (disparidade != 0):
        dist = abs((distancia_cameras * focal_pixel) / disparidade)
    return 0, 0, 0, dist