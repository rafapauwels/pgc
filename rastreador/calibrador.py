import cv2

class Calibrador:
    def __init__(self):
        path = '/home/pauwels/Documents/Sync/UFABC/PGC/pgc/rastreador/'
        cv_file = cv2.FileStorage()

        cv_file.open(path + 'stereoMap.xml', cv2.FileStorage_READ)
        self.stereoMapE_x = cv_file.getNode('stereoMapE_x').mat()
        self.stereoMapE_y = cv_file.getNode('stereoMapE_y').mat()
        self.stereoMapD_x = cv_file.getNode('stereoMapD_x').mat()
        self.stereoMapD_y = cv_file.getNode('stereoMapD_y').mat()
        cv_file.release()

        cv_file.open(path + 'Q.mat', cv2.FileStorage_READ)
        self.Q = cv_file.getNode('matrix').mat()
        cv_file.release()

    def retificar(self, frame_e, frame_d):
        fe = cv2.remap(frame_e, self.stereoMapE_x, self.stereoMapE_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        fd = cv2.remap(frame_d, self.stereoMapD_x, self.stereoMapD_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        return fe, fd
    
    def recuperarQ(self):
            return self.Q
