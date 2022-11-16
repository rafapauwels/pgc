from calibrador import Calibrador
from frames import Frames
from aruco import encontrar_centro
from distancia import calcular_distancia_trig, calcular_distancia_antigo

import cv2

def main():
    parar = False

    calibrador = Calibrador()
    frames = Frames()

    while (not parar):
        # Capturar frames da esquerda e direita
        parar, frame_e, frame_d = frames.capturar_frames()

        frame_e, frame_d = calibrador.retificar(frame_e, frame_d)

        # Buscar o centro dos marcadores em cada frame
        centro_e, frame_e = encontrar_centro(frame_e, True)
        centro_d, frame_d = encontrar_centro(frame_d, True)

        # Calcular posição do marcador
        _, _, _, DT = calcular_distancia_trig(centro_e, frame_e, centro_d, frame_d)
        X, Y, Z, D = calcular_distancia_antigo(centro_e, frame_e, centro_d, frame_d)

        texto = 'X: {:3.1f}\nY: {:3.1f}\nZ: {:3.1f}\nD: {:3.1f}\nDT: {:3.1f}'.format(X,Y,Z,D,DT)
        linha = 0
        for t in texto.split('\n'):
            linha += 30
            cv2.putText(frame_d, t, (10, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 1, cv2.LINE_AA, False)

        frames.mostrar_frames("ESQ", frame_e)
        frames.mostrar_frames("DIR", frame_d)

main()