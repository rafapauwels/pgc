import cv2 as cv

cam_e = cv.VideoCapture(0)
cam_d = cv.VideoCapture(2)

while (True):
    _, frame_e = cam_e.read()
    _, frame_d = cam_d.read()