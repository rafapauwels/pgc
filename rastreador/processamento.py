import cv2
import numpy as np
import json
import platform

def gerar_pointcloud(frame, disparity_cloud, Q):
    points_3d = cv2.reprojectImageTo3D(disparity_cloud, Q, handleMissingValues=False)
    mask_map = disparity_cloud > disparity_cloud.min()

    out_points = points_3d[mask_map]
    out_cores = frame[mask_map]

    colors = out_cores.reshape(-1,3)
    vertices = np.hstack([out_points.reshape(-1,3),colors])

    ply_header = '''ply
        format ascii 1.0
        element vertex %(vert_num)d
        property float x
        property float y
        property float z
        property uchar red
        property uchar green
        property uchar blue
        end_header
        '''
    with open('pointcloud.ply', 'w') as f:
        f.write(ply_header %dict(vert_num=len(vertices)))
        np.savetxt(f, vertices, '%f %f %f %d %d %d')

def disparity_map(frame_esquerda, frame_direita, scaled, for_cloud):
    path = '/home/pauwels/Documents/Sync/UFABC/PGC/pgc/rastreador/parametros/sgbm.params'
    pathWindows = 'C:\\Users\\Rafael\\Desktop\\Sync\\UFABC\\PGC\\pgc\\rastreador\\parametros\\sgbm.params'

    if platform.system() == "Windows":
        path = pathWindows

    f = open(path)
    params = json.load(f)
    f.close()

    P1 = 8*3*params['block_size']*params['block_size']
    P2 = 32*3*params['block_size']*params['block_size']
    stereo = cv2.StereoSGBM_create(
            minDisparity=params['min_disp'],
            numDisparities=params['num_disp'],
            blockSize=params['block_size'],
            P1=P1,
            P2=P2,
            disp12MaxDiff=params['disp12MaxDiff'],
            preFilterCap=params['preFilterCap'],
            uniquenessRatio=params['uniquenessRatio'],
            speckleWindowSize=params['speckleWindowSize'],
            speckleRange=params['speckleRange'],
            mode=params['mode']
        )

    frame_esquerda_gray = cv2.cvtColor(frame_esquerda, cv2.COLOR_BGR2GRAY)
    frame_direita_gray = cv2.cvtColor(frame_direita, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(frame_esquerda_gray, frame_direita_gray)
    
    if for_cloud:
        disparity_cloud = np.float32(np.divide(disparity, 16.0))

    if scaled:
        disparity_scaled = (disparity / 16.).astype(np.uint8)
        return disparity_scaled
    else:
        disparity = cv2.normalize(disparity, disparity, alpha=255, beta=0, norm_type=cv2.NORM_MINMAX)
        disparity = np.uint8(disparity)
        return disparity