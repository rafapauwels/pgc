import cv2 as cv

cam = cv.VideoCapture(0)

while (True):
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()