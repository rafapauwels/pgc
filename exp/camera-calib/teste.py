import cv2 as cv

e = cv.VideoCapture(0)
d = cv.VideoCapture(2)

# e.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
# e.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

while 1:
    _, frame_esquerda = e.read()
    _, frame_direita = d.read()

    cv.imshow('Esquerda', frame_esquerda)
    cv.imshow('Direita', frame_direita)

    key = cv.waitKey(1)
    if  key & 0xFF == ord('q'):
        break