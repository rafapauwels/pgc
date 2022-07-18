import cv2 as cv
import os

path = "/home/pauwels/Documents/Sync/UFABC/PGC/pgc/exp/camera-calib/calibration-pics"

cam_0 = cv.VideoCapture(0)
cam_2 = cv.VideoCapture(2)

i = 0
while (True):
    _, frame_0 = cam_0.read()
    _, frame_2 = cam_2.read()
    cv.imshow("direita 0", frame_0)
    cv.imshow("esquerda 2", frame_2)

    key = cv.waitKey(1)
    if  key & 0xFF == ord('q'):
        break

    if key & 0xFF == ord('s'):
        arquivo_0 = path + "/direita/img" + str(i) + ".png"
        arquivo_2 = path + "/esquerda/img" + str(i) + ".png"

        print(arquivo_0 + " salvo.")
        cv.imwrite(arquivo_0, frame_0)
        
        print(arquivo_2 + " salvo.")
        cv.imwrite(arquivo_2, frame_2)
        i += 1

    

cam_0.release()
cam_2.release()
cv.destroyAllWindows()