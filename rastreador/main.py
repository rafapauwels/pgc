from calibrador import Calibrador
from frames import Frames
from aruco import encontrar_centro
from distancia import calcular_distancia
from processamento import stereo3d, colorMap

import cv2

def main():
    parar = False
    live = True

    calibrador = Calibrador()
    frames = Frames()

    Q = calibrador.recuperarQ()
    while (not parar):
        # Capturar frames da esquerda e direita
        parar, frame_e, frame_d = frames.capturar_frames(live)

        frame_e, frame_d = calibrador.retificar(frame_e, frame_d)

        # Buscar o centro dos marcadores em cada frame
        centro_e, frame_e = encontrar_centro(frame_e, True)
        centro_d, frame_d = encontrar_centro(frame_d, True)

        # Calcular posição do marcador usando trig
        X, Y, Z, D = calcular_distancia(centro_e, frame_e, centro_d, frame_d, Q)

        texto = 'X: {:3.1f}\nY: {:3.1f}\nZ: {:3.1f}\nD: {:3.1f}\n'.format(X,Y,Z,D)
        linha = 0
        for t in texto.split('\n'):
            linha += 30
            cv2.putText(frame_d, t, (10, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 1, cv2.LINE_AA, False)

        # Usando as funções do opencv para criar o mapa de disparidades e reprojetando para o 3d
        # tresd = stereo3d(frame_d, frame_d, Q)

        # try:
        #     print(tresd[centro_e[0]][centro_e[1]])
        # except Exception as e:
        #     print("deu pau: " + str(e))

        frames.mostrar_frames("ESQ", frame_e)
        frames.mostrar_frames("DIR", frame_d)

        frames.mostrar_frames("Disparidade", colorMap(frame_e, frame_d))

main()