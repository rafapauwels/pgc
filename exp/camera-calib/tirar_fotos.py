import cv2 as cv
import os

op_cam = int(input("Digite 0 para camera esquerda e 2 para direita e 4 para deletar as imagens: "))

path = "/home/pauwels/Documents/pgc/exp/camera-calib/calibration-pics/"

if op_cam == 4:
    for item in os.listdir(path):
        if item.endswith(".png"):
            os.remove(os.path.join(path, item))
else:
    cam = cv.VideoCapture(op_cam)
    i = 0
    while (True):
        _, frame = cam.read()
        cv.imshow("ext", frame)

        key = cv.waitKey(1)
        if  key & 0xFF == ord('q'):
            break

        if key & 0xFF == ord('s'):
            lado = "-esquerda" if op_cam == 0 else "-direita"
            arquivo = path + "img" + str(i) + lado + ".png"
            print(arquivo + " salvo.")
            cv.imwrite(arquivo, frame)
            i += 1

        

    cam.release()
    cv.destroyAllWindows()