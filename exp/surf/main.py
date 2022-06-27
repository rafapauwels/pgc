import cv2

cam = cv2.VideoCapture(0)
# cam_externa = cv2.VideoCapture(2)

while(True):
    _, frame = cam.read()
    # _, frame_externo = cam_externa.read()

    # Compilar opencv com flag OPENCV_ENABLE_NONFREE ou
    # fazer downgrade para 3.4.2.17
    
    surf = cv2.xfeatures2d.SURF_create(400)
    kp, des = surf.detectAndCompute(frame, None)

    img = cv2.drawKeypoints(frame, kp, None, (255, 0, 0), 4)
    cv2.imshow('integrada', frame)
    # cv2.imshow('externa', frame_externo)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
