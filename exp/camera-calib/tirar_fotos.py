import cv2 as cv

cam = cv.VideoCapture(0)
i = 0;
while (True):
    _, frame = cam.read()
    cv.imshow("ext", frame)

    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite("calibration/img" + str(i) + ".png", frame)
        i += 1

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()