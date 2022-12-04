from flask import Flask, request, jsonify
from aruco import encontrar_centro
from distancia import localizar

import cv2
import pickle
import struct
import socket

app = Flask(__name__)

@app.route('/track', methods = ['POST'])
def track():
    frame_data = request.data
    frame_data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    frame_e = cv2.imdecode(frame_data['esq'], cv2.IMREAD_COLOR)
    frame_d = cv2.imdecode(frame_data['dir'], cv2.IMREAD_COLOR)

    # Buscar o centro dos marcadores em cada frame
    centros_e, frame_e = encontrar_centro(frame_e, True)
    centros_d, frame_d = encontrar_centro(frame_d, True)

    disparidade_marcador_1 = centros_e[1][0] - centros_d[1][0]
    disparidade_marcador_2 = centros_e[2][0] - centros_d[2][0]
    X_1, Y_1, Z_1 = localizar(centros_e[1], disparidade_marcador_1, frame_data['Q'])
    X_2, Y_2, Z_2 = localizar(centros_e[2], disparidade_marcador_2, frame_data['Q'])
    X_R, Y_R, Z_R = abs(X_1-X_2), (Y_1-Y_2), (Z_1-Z_2)

    return jsonify({'esquerda':{'X': X_1, 'Y': Y_1, 'Z': Z_1}, 'direita':{'X': X_2, 'Y': Y_2, 'Z': Z_2}, 'relativo':{'X': X_R, 'Y': Y_R, 'Z': Z_R}})

def imprimir_texto(frame, column, texto):
    linha = 0
    for t in texto.split('\n'):
        linha += 30
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 3, cv2.LINE_AA, False)
        cv2.putText(frame, t, (column, linha), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 1, cv2.LINE_AA, False)

    return frame

app.run()