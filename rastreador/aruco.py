import cv2
import numpy as np

ARUCO_MARKER = cv2.aruco.DICT_5X5_250

def encontrar_centro(frame, desenhar):
    # TODO Criar classe para esse helper do aruco e mover essas inicializações
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_MARKER)
    arucoParams = cv2.aruco.DetectorParameters_create()
    # TODO

    # frame_flip = cv2.flip(frame, 0)
    corners, ids, _ = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    centro, frame = desenhar_marcador(corners, ids, frame, desenhar)
    return centro, frame

def desenhar_marcador(corners, ids, frame, desenhar):
    if len(corners) > 0:
        for (corner, id) in zip(corners, ids):
            (topL, topR, botR, botL) = corner.reshape((4, 2))
            topR = (int(topR[0]), int(topR[1]))
            topL = (int(topL[0]), int(topL[1]))
            botR = (int(botR[0]), int(botR[1]))
            botL = (int(botL[0]), int(botL[1]))

            cx = int((topL[0] + botR[0]) / 2.0)
            cy = int((topL[1] + botR[1]) / 2.0)
            if (desenhar):
                cor = (0, 255, 0)
                cv2.line(frame, topL, topR, cor, 2)
                cv2.line(frame, topR, botR, cor, 2)
                cv2.line(frame, botR, botL, cor, 2)
                cv2.line(frame, botL, topL, cor, 2)
                
                cv2.circle(frame, (cx, cy), 4, cor, -1)
            return (cx, cy), frame
    return (0, 0), frame

def gerar_aruco():
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_MARKER)
    id = 1
    tag_size = 1000
    tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")

    cv2.aruco.drawMarker(arucoDict, id, tag_size, tag, 1)
    cv2.imwrite("marker.png", tag)

if __name__ == '__main__':
    gerar_aruco()
