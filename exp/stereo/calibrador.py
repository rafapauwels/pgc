import cv2 as cv

class Calibrador:
    def __init__(self, path):
        cv_file = cv.FileStorage()
        cv_file.open(path, cv.FileStorage_READ)

        self.stereoMapE_x = cv_file.getNode('stereoMapE_x').mat()
        self.stereoMapE_y = cv_file.getNode('stereoMapE_y').mat()
        self.stereoMapD_x = cv_file.getNode('stereoMapD_x').mat()
        self.stereoMapD_y = cv_file.getNode('stereoMapD_y').mat()
    
    def acertar_frames(self, frameE, frameD):
        novoE = cv.remap(frameE, self.stereoMapE_x, self.stereoMapE_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
        novoD = cv.remap(frameD, self.stereoMapD_x, self.stereoMapD_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)

        return novoE, novoD