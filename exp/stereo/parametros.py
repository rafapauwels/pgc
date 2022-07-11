import numpy as np

class Parametros:
    def __init__(self, path):
        # self.ret_esquerda = np.loadtxt(path, '/ret.esquerda')
        # self.ret_direita = np.loadtxt(path, '/ret.direita')
        self.mtx_esquerda = np.loadtxt(path + '/mtx.esquerda')
        self.dist_esquerda = np.loadtxt(path + '/dist.esquerda')
        self.mtx_direita = np.loadtxt(path + '/mtx.direita')
        self.dist_direita = np.loadtxt(path + '/dist.direita')