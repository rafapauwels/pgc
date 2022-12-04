from numpy.linalg import inv

import math
import numpy as np

def localizar(ponto, disp, Q):
    if disp == 0: return 0, 0, 0

    X, Y, Z, W = np.matmul(Q, np.array([ponto[0], ponto[1], disp, 1]))
    return np.multiply(np.array([X/W, Y/W, Z/W]), 2)