import cv2

class Frames:
    def __init__(self):
        self.cam_e = cv2.VideoCapture(0)
        self.cam_d = cv2.VideoCapture(2)
        self.count = 0

    def capturar_frames(self, live):
        parar = False
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            parar = True

        _, frame_e = self.cam_e.read()
        _, frame_d = self.cam_d.read()

        if key & 0xFF == ord('s'):
            cv2.imwrite("./img_e.png", frame_e)
            cv2.imwrite("./img_d.png", frame_d)

        if live:
            return parar, frame_e, frame_d
        else:
            # usar frames fixos
            e = cv2.imread("./img_e.png")
            d = cv2.imread("./img_d.png")

            return parar, e, d

    def mostrar_frames(self, titulo, frame):
        cv2.imshow(titulo, frame)