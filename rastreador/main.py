from calibrador import Calibrador
from frames import Frames
from aruco import encontrar_centro
from distancia import localizar
from processamento import gerar_pointcloud, disparity_map

import cv2
import numpy as np

def main():
    parar = False
    live = True
    mapa_disparidade = True
    pointcloud = False
    distancias = True

    calibrador = Calibrador()
    frames = Frames()

    Q = calibrador.recuperarQ()
    K1 = calibrador.recuperarK1()
    while (not parar):
        # Capturar frames da esquerda e direita
        parar, frame_e, frame_d = frames.capturar_frames(live)

        frame_e, frame_d = calibrador.retificar(frame_e, frame_d)

        # Buscar o centro dos marcadores em cada frame
        centros_e, frame_e = encontrar_centro(frame_e, True)
        centros_d, frame_d = encontrar_centro(frame_d, True)

        # Calcula mapa de disparidades para geração da nuvem de pontos
        if mapa_disparidade:
            disp_map = disparity_map(frame_e, frame_d, scaled=True, for_cloud=pointcloud)
            if pointcloud:
                gerar_pointcloud(frame_d, disp_map, Q)
                parar = True

            frames.mostrar_frames("Disparidade", disp_map)

        # Calcula a posição 3D do ponto através de
        # Q | x    | = | X |
        #   | y    |   | Y |
        #   | disp |   | Z |
        #   | 1    |   | W |
        if distancias:
            disparidade_marcador_1 = centros_e[1][0] - centros_d[1][0]
            disparidade_marcador_2 = centros_e[2][0] - centros_d[2][0]
            X_1, Y_1, Z_1 = localizar(centros_e[1], disparidade_marcador_1, Q)
            X_2, Y_2, Z_2 = localizar(centros_e[2], disparidade_marcador_2, Q)
            X_R, Y_R, Z_R = abs(X_1-X_2), (Y_1-Y_2), (Z_1-Z_2)

            texto_marcador_1 = 'X_1: {:3.1f}\nY_1: {:3.1f}\nZ_1: {:3.1f}'.format(X_1,Y_1,Z_1)
            texto_marcador_2 = 'X_2: {:3.1f}\nY_2: {:3.1f}\nZ_2: {:3.1f}'.format(X_2,Y_2,Z_2)
            texto_relativo   = 'X_R: {:3.1f}\nY_R: {:3.1f}\nZ_R: {:3.1f}'.format(X_R,Y_R,Z_R)

            frame_e = imprimir_texto(frame_e,  10, texto_marcador_1)
            frame_e = imprimir_texto(frame_e, 140, texto_marcador_2)
            frame_e = imprimir_texto(frame_e, 410, texto_relativo)

        frames.mostrar_frames("DIR", frame_d)
        frames.mostrar_frames("ESQ", frame_e)

def imprimir_texto(frame, column, texto):
    linha = 0
    for t in texto.split('\n'):
        linha += 30
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 3, cv2.LINE_AA, False)
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, cv2.LINE_AA, False)

    return frame

main()


