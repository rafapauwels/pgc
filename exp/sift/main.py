import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while (True):
    _, frame = cam.read()
    # cv2.imshow('integrada', frame)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('integrada', gray_frame)

    sift = cv2.SIFT_create()
    kp = sift.detect(gray_frame, None)


    frame = cv2.drawKeypoints(gray_frame, kp, frame, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('integrada', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()