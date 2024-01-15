import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import math
from VisionArtificial import interprete_gerber, SVA_SMD
from Control import Trayectorias

MIN_MATCH_COUNT = 25
pixeles_por_mm = 10.0
altura_pcb = 400
altura_pnp = 380

# herramientas
camara = 0
dispensador = 1
pnp = 2

def get_matched_coordinates(temp_img, map_img):
    """
    Gets template and map image and returns matched coordinates in map image

    Parameters
    ----------
    temp_img: image
        image to be used as template

    map_img: image
        image to be searched in

    Returns
    ---------
    ndarray
        an array that contains matched coordinates

    """

    # initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(temp_img, None)
    kp2, des2 = sift.detectAndCompute(map_img, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # find matches by knn which calculates point distance in 128 dim
    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    print("Matches found - %d/%d" %
              (len(good), MIN_MATCH_COUNT))

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # find homography
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = temp_img.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],
                          [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)  # matched coordinates

        map_img = cv2.polylines(
            map_img, [np.int32(dst)], True, (127, 0, 0), 3, cv2.LINE_AA)

    else:
        print("Not enough matches are found - %d/%d" %
              (len(good), MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)

    # draw template and map image, matches, and keypoints
    img3 = cv2.drawMatches(temp_img, kp1, map_img, kp2,
                           good, None, **draw_params)
    
    # result image path
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/mask.png'), map_img)
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/output.png'), img3)

    # if --show argument used, then show result image
    # plt.imshow(img3, 'gray'), plt.show()

    rot_deg = math.degrees(math.atan2((int(dst[1][0][0]) - int(dst[0][0][0])), (int(dst[1][0][1]) - int(dst[0][0][1]))))
    orig = dst[1][0] # punto de origen para PCBs
    dim_y, dim_x = map_img.shape # dimension de la imagen

    off_x = orig[0]-dim_x/2 # offset en x desde el centro de la imagen
    off_y = dim_y/2-orig[1] # offset en y desde el centro de la imagen

    return [off_x, off_y], rot_deg

def inicioSVA(path : str, map_path : str, _top_bottom : bool, componentes_lista, path1 : str, path2 : str, path3 : str, path4 : str):
    if _top_bottom:
        interprete_gerber.genImage(path, top=True)
    else:
        interprete_gerber.genImage(path, top=False)

    # read images
    temp_img_gray = cv2.imread('temp/board-mask.png', 0)
    map_img = cv2.imread(map_path)
    cv2.imwrite('temp/from.png', map_img)

    # image segmentation
    # """
    hsv = cv2.cvtColor(map_img, cv2.COLOR_BGR2HSV)
    # blur = cv2.GaussianBlur(hsv,(5,5),0)
    # hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    # color_pcb = np.unravel_index(np.argmax(hist, axis=None), hist.shape)[0]
    # cv2.imshow("hist", hist)
    # print("color_pcb = ", str(color_pcb))
    # color_pcb = int(144/2)
    # tresh = 11

    # lower = np.array([0, 0, 0])
    # upper = np.array([color_pcb-tresh, 255, 255])
    # mask1 = cv2.inRange(hsv, lower, upper)
    # lower = np.array([color_pcb+tresh, 0, 0])
    # upper = np.array([180, 255, 255])
    # mask2 = cv2.inRange(hsv, lower, upper)

    # mask = mask1 + mask2
    lower = np.array([0, int(40/100 * 255), int(0/100 * 255)])
    upper = np.array([180, int(100/100 * 255), int(100/100 * 255)])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_not(mask)
    mask = cv2.GaussianBlur(mask, (5,5), 0)

    # equalize histograms
    temp_img_eq = cv2.equalizeHist(temp_img_gray)
    map_img_eq = cv2.equalizeHist(mask)

    # calculate matched coordinates
    offset, grados_rot = get_matched_coordinates(temp_img_eq, map_img_eq)

    # print(offset)
    # print(grados_rot)
    # convertir de pixeles a mm
    offset_x = offset[0]/pixeles_por_mm
    offset_y = offset[1]/pixeles_por_mm

    print(offset_x, offset_y, grados_rot)

    soldadura_lista = interprete_gerber.obtener_soldadura(path, _top_bottom)
    if(not(_top_bottom)): 
        interprete_gerber.mirror_bottom(path, soldadura_lista)
    for x in soldadura_lista:
        nuevo_x = x.x*math.cos(math.radians(grados_rot)) - x.y*math.sin(math.radians(grados_rot))
        nuevo_y = x.x*math.sin(math.radians(grados_rot)) + x.y*math.cos(math.radians(grados_rot))
        x.x = nuevo_x + offset_x
        x.y = nuevo_y + offset_y

    # componentes_lista = interprete_gerber.obtener_pnp(path, _top_bottom)

    # rot_real = np.zeros(len(componentes_lista)) # INSERTAR SVA2
    # offsets_reales = np.ones([len(componentes_lista), 2])*100.0 # INSERTAR SVA2
    # for x in range(offsets_reales.shape[0]):
    #     offsets_reales[x][0] = 100.0 + x*10

    smd_img1, smd_img2, smd_img3, smd_img4, offsets_reales, rot_real = SVA_SMD.getCentroidAngleSMD(path1, path2, path3, path4)
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd1.png'), smd_img1)
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd2.png'), smd_img2)
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd3.png'), smd_img3)
    cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd4.png'), smd_img4)
    
    # print(rot_real)
    # print(offsets_reales)

    if(not(_top_bottom)): 
        interprete_gerber.mirror_bottom(path, componentes_lista)

    for x in range(len(componentes_lista)):
        nuevo_x = componentes_lista[x].x*math.cos(math.radians(grados_rot)) - componentes_lista[x].y*math.sin(math.radians(grados_rot))
        nuevo_y = componentes_lista[x].x*math.sin(math.radians(grados_rot)) + componentes_lista[x].y*math.cos(math.radians(grados_rot))
        componentes_lista[x].x = nuevo_x + offset_x
        componentes_lista[x].y = nuevo_y + offset_y
        componentes_lista[x].angulo += grados_rot + rot_real[x]
        if(componentes_lista[x].angulo) < 0.0: componentes_lista[x].angulo += 360.0
        if(componentes_lista[x].angulo) > 360.0: componentes_lista[x].angulo -= 360.0

    smd_lista = []
    IC_lista = []
    for x in range(len(componentes_lista)):
        if componentes_lista[x].paquete != None and ("res" in componentes_lista[x].paquete or "RES" in componentes_lista[x].paquete or "cap" in componentes_lista[x].paquete or "CAP" in componentes_lista[x].paquete or "led" in componentes_lista[x].paquete or "LED" in componentes_lista[x].paquete):
            smd_lista.append(componentes_lista[x])
        else:
            IC_lista.append(componentes_lista[x])
    
    herr_soldadura = Trayectorias.cambio_herramienta(dispensador)
    puntos_soldadura = Trayectorias.soldaduraclass_to_puntos(soldadura_lista, altura_pcb) 
    herr_pnp = Trayectorias.cambio_herramienta(pnp)
    # puntos_pnp = Trayectorias.componentesclass_to_puntos(componentes_lista, 400, 420)
    puntos_pnp = Trayectorias.componentesclass_to_puntos2(smd_lista, IC_lista, altura_pcb, altura_pnp, offsets_reales)
    herr_cam = Trayectorias.cambio_herramienta(camara)

    puntos = np.append(herr_soldadura, puntos_soldadura, axis=0)
    puntos = np.append(puntos, herr_pnp, axis=0)
    puntos = np.append(puntos, puntos_pnp, axis=0)
    puntos = np.append(puntos, herr_cam, axis=0)
    
    return puntos