import numpy as np
import cv2 as cv
import glob

def calibrarCameras():
    tamanhoChess = (9,7)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((tamanhoChess[0] * tamanhoChess[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:tamanhoChess[0],0:tamanhoChess[1]].T.reshape(-1,2)

    objpoints = []
    imgpointsEsquerda = []
    imgpointsDireita = []

    path = '/home/pauwels/Documents/Sync/UFABC/PGC/pgc/exp/camera-calib'
    imagesEsquerda = sorted(glob.glob(path + '/calibration-pics/esquerda/*.png'))
    imagesDireita = sorted(glob.glob(path + '/calibration-pics/direita/*.png'))

    count = 0
    for esq, direita in zip(imagesEsquerda, imagesDireita):
        imgEsquerda = cv.imread(esq)
        imgDireita = cv.imread(direita)

        grayEsquerda = cv.cvtColor(imgEsquerda, cv.COLOR_BGR2GRAY)
        grayDireita = cv.cvtColor(imgDireita, cv.COLOR_BGR2GRAY)

        retE, cornersE = cv.findChessboardCorners(grayEsquerda, tamanhoChess, None)
        retD, cornersD = cv.findChessboardCorners(grayDireita, tamanhoChess, None)

        if retE and retD == True:
            count += 1
            objpoints.append(objp)

            cornersSubEsquerda = cv.cornerSubPix(grayEsquerda, cornersE, (11,11), (-1,-1), criteria)
            imgpointsEsquerda.append(cornersSubEsquerda)

            cornersSubDireita = cv.cornerSubPix(grayDireita, cornersD, (11,11), (-1,-1), criteria)
            imgpointsDireita.append(cornersSubDireita)

            cv.drawChessboardCorners(imgEsquerda, tamanhoChess, cornersE, retE)
            cv.imshow('img esq', imgEsquerda)
            cv.drawChessboardCorners(imgDireita, tamanhoChess, cornersD, retD)
            cv.imshow('img dir', imgDireita)
            cv.waitKey(1000)

    if count == 0:
        print("O padrao nao foi encontrado em nenhuma imagem")
    else:
        retE, mtxE, distE, rvecsE, tvecsE = cv.calibrateCamera(objpoints, imgpointsEsquerda, grayEsquerda.shape[::-1], None, None)
        retD, mtxD, distD, rvecsD, tvecsD = cv.calibrateCamera(objpoints, imgpointsDireita, grayDireita.shape[::-1], None, None)
        
        novaCameraE = cv.getOptimalNewCameraMatrix(mtxE, distE, (640, 480), 1, (640, 480))
        novaCameraD = cv.getOptimalNewCameraMatrix(mtxD, distD, (640, 480), 1, (640, 480))
        
        ## Calibração stereo
        ## Encontrar relação entre as cameras
        retStereo, novaMtxE, distE, novaMtxD, distD, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsEsquerda, imgpointsDireita, mtxE, distE, mtxD, distD, (640, 480), criteria)

        # Retificação stereo
        rectE, rectD, projMtxE, projMtxD, Q, roiE, roiD = cv.stereoRectify(novaMtxE, distE, novaMtxD, distD, (640, 480), rot, trans, 1, (0, 0))

        stereoMapE = cv.initUndistortRectifyMap(novaMtxE, distE, rectE, projMtxE, (640, 480), cv.CV_16SC2)
        stereoMapD = cv.initUndistortRectifyMap(novaMtxD, distD, rectD, projMtxD, (640, 480), cv.CV_16SC2)

        calibFile = cv.FileStorage(path + '/calibration-data/stereoMap.xml', cv.FILE_STORAGE_WRITE)
        
        calibFile.write('stereoMapE_x', stereoMapE[0])
        calibFile.write('stereoMapE_y', stereoMapE[1])
        calibFile.write('stereoMapD_x', stereoMapD[0])
        calibFile.write('stereoMapD_y', stereoMapD[1])

        calibFile.release()

calibrarCameras()