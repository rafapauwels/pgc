import cv2 as cv

class Frames:
    def __init__(self):
        self.cam_e = cv.VideoCapture(0)
        self.cam_d = cv.VideoCapture(2)

    def capturar_frames(self):
        parar = False
        if cv.waitKey(1) & 0xFF == ord('q'):
            parar = True

        _, frame_e = self.cam_e.read()
        _, frame_d = self.cam_d.read()

        return parar, frame_e, frame_d

    def mostrar_frames(self, titulo, frame):
        cv.imshow(titulo, frame)