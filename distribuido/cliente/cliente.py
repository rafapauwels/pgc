from calibrador import Calibrador

import cv2
import socket
import struct
import pickle
import requests

def main():
    calibrador = Calibrador()

    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(('', 5000))

    cam_e = cv2.VideoCapture(0)
    cam_d = cv2.VideoCapture(2)

    while True:
        _, frame_e = cam_e.read()
        _, frame_d = cam_d.read()

        frame_e, frame_d = calibrador.retificar(frame_e, frame_d)
        
        _, codificado_e = cv2.imencode('.jpg', frame_e)
        _, codificado_d = cv2.imencode('.jpg', frame_d)

        pacote = { 'esq': codificado_e, 'dir': codificado_d, 'Q': calibrador.Q }
        data = pickle.dumps(pacote, 0)
        res = requests.post('http://127.0.0.1:5000/track', data = data).json()

        texto_marcador_1 = 'X_1: {:3.1f}\nY_1: {:3.1f}\nZ_1: {:3.1f}'.format(res['esquerda']['X'],res['esquerda']['Y'],res['esquerda']['Z'])
        texto_marcador_2 = 'X_2: {:3.1f}\nY_2: {:3.1f}\nZ_2: {:3.1f}'.format(res['direita']['X'],res['direita']['Y'],res['direita']['Z'])
        texto_relativo   = 'X_R: {:3.1f}\nY_R: {:3.1f}\nZ_R: {:3.1f}'.format(res['relativo']['X'],res['relativo']['Y'],res['relativo']['Z'])

        frame_e = imprimir_texto(frame_e,  10, texto_marcador_1)
        frame_e = imprimir_texto(frame_e, 140, texto_marcador_2)
        frame_e = imprimir_texto(frame_e, 410, texto_relativo)

        cv2.imshow('s', frame_e)
        cv2.waitKey(1)

def imprimir_texto(frame, column, texto):
    linha = 0
    for t in texto.split('\n'):
        linha += 30
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 3, cv2.LINE_AA, False)
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, cv2.LINE_AA, False)

    return frame


main()