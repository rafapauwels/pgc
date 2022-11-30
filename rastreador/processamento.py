import cv2
import numpy as np

def stereo3d(frame_e, frame_d, Q):
    min_disp = -128
    num_disp = 128
    
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=16,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=150,
        speckleRange=32,
    )

    disp = stereo.compute(frame_e, frame_d).astype(np.float32)
    height, width, _ = frame_e.shape

    focal_mm = 6.22
    sensor_width = 5.14
    focal_pixel = focal_mm * width / sensor_width

    # Para visualizar o mapa de disparidades
    # disp = cv2.normalize(disp, disp, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)

    disp = np.uint8(disp)
    return cv2.reprojectImageTo3D(disp, Q)

def colorMap(frame_esquerda, frame_direita):
    # matcher_e = cv2.StereoSGBM_create(
    #     minDisparity=-128,
    #     numDisparities=128,
    #     blockSize=16,
    #     disp12MaxDiff=1,
    #     uniquenessRatio=10,
    #     speckleWindowSize=150,
    #     speckleRange=32,
    # )
    # matcher_d = cv2.ximgproc.createRightMatcher(matcher_e)
    # filtro=cv2.ximgproc.createDisparityWLSFilter(matcher_left=matcher_e)
    # filtro.setLambda(80000)
    # filtro.setSigmaColor(1.2)

    # disparidade_e = matcher_e.compute(frame_e, frame_d)
    # disparidade_d = matcher_d.compute(frame_d, frame_e)

    # disparidade = filtro.filter(disparidade_e, frame_e, None, disparidade_d)
    # return matcher_e.compute(frame_e, frame_d)

    block_size = 10
    min_disp = -128
    max_disp = 0
    # Maximum disparity minus minimum disparity. The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
    # Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 200
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0
    stereo = cv2.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=block_size,
            uniquenessRatio=uniquenessRatio,
            speckleWindowSize=speckleWindowSize,
            speckleRange=speckleRange,
            disp12MaxDiff=disp12MaxDiff,
            P1=8 * 1 * block_size * block_size,
            P2=32 * 1 * block_size * block_size,
        )

    frame_esquerda_gray = cv2.cvtColor(frame_esquerda, cv2.COLOR_BGR2GRAY)
    frame_direita_gray = cv2.cvtColor(frame_direita, cv2.COLOR_BGR2GRAY)

    # frame_esquerda_gray = cv.GaussianBlur(frame_esquerda_gray, (5,5), cv.BORDER_DEFAULT)
    # frame_direita_gray = cv.GaussianBlur(frame_direita_gray, (5,5), cv.BORDER_DEFAULT)

    disparity = stereo.compute(frame_esquerda_gray, frame_direita_gray)

    disparity = cv2.normalize(disparity, disparity, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
    disparity = np.uint8(disparity)
    return disparity