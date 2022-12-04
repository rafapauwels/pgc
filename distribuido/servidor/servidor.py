from aruco import encontrar_centro
from distancia import localizar

import cv2
import pickle
import struct
import socket

def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('', 5000))
    server_socket.listen(10)

    conn, _ = server_socket.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
            if not data:
                conn, addr=server_socket.accept()
                continue
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

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

        texto_marcador_1 = 'X_1: {:3.1f}\nY_1: {:3.1f}\nZ_1: {:3.1f}'.format(X_1,Y_1,Z_1)
        texto_marcador_2 = 'X_2: {:3.1f}\nY_2: {:3.1f}\nZ_2: {:3.1f}'.format(X_2,Y_2,Z_2)
        texto_relativo   = 'X_R: {:3.1f}\nY_R: {:3.1f}\nZ_R: {:3.1f}'.format(X_R,Y_R,Z_R)

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