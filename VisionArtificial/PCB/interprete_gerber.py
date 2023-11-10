import os
from glob import glob
import csv
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

from PIL import Image, ImageOps, ImageDraw, ImageFont
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
import gerber

MIN_MATCH_COUNT = 100

class componentes_class:
    def __init__(self, nombre : str, x : float, y : float, angulo : float, valor : str, paquete : str, numero : str) -> None:
        self.nombre = nombre
        self.x = float(x)
        self.y = float(y)
        self.angulo = float(angulo)
        self.valor = valor
        self.paquete = paquete
        self.numero = numero

class soldadura_class:
    def __init__(self, x, y, cantidad) -> None:
        self.x = x
        self.y = y
        self.cantidad = cantidad

def obtener_pnp(path : str, _top_bottom : bool):
    print("Leyendo archivo de componentes...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    fusion_kicad = False
    if _top_bottom:
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*top-pos.csv'), recursive=True)[0])
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*front.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo") # Convertir en mensaje de error en PyQt
    else:
        try:
            path_pnp = os.path.normpath(glob(os.path.join(path, '**/*bottom-pos.csv'), recursive=True)[0])
            if path_pnp == "": fusion_kicad = True # No es Kicad 
        except:
            try:
                fusion_kicad = True # No es Kicad 
                path_pnp = os.path.normpath(glob(os.path.join(path, '**/*back.csv'), recursive=True)[0])
            except:
                print("No existe tal archivo") # Convertir en mensaje de error en PyQt

    lista_componentes = []

    with open(path_pnp, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        it = 0
        for row in spamreader:
            if fusion_kicad:
                lista_componentes.append(componentes_class(row[0], row[1], row[2], row[3], row[4], row[5], it)) # parse para archivos fusion
            else:
                lista_componentes.append(componentes_class(row[0], row[3], row[4], row[5], row[1], row[2], it)) # parse para archivos kicad
            it += 1

    # lista_componentes.pop(0)
    return lista_componentes

def obtener_soldadura(path : str, _top_bottom : bool):
    print("Leyendo archivo de soldadura...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    if _top_bottom == True:
        path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GTP'), recursive=True)[0])
    else:
        path_solder = os.path.normpath(glob(os.path.join(path, '**/*.GBP'), recursive=True)[0])

    soldadura_lista = []

    copper = gerber.read(path_solder)
    for prim in copper.primitives:
        pos = (prim.bounding_box[0][0] + (prim.bounding_box[0][1] - prim.bounding_box[0][0]) / 2,
            prim.bounding_box[1][0] + (prim.bounding_box[1][1] - prim.bounding_box[1][0]) / 2)
        area_sqr = math.sqrt(math.sqrt(prim.bounding_box[0][1] - prim.bounding_box[0][0]) * (prim.bounding_box[1][1] - prim.bounding_box[1][0]))
        soldadura_lista.append(soldadura_class(round(pos[0], 4), round(pos[1], 4), area_sqr))
    return soldadura_lista

def genImage(CAMFolder : str, top : bool):
    print("Cargando archivos de capa superior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTL'), recursive=True)[0]))
    mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTS'), recursive=True)[0]))
    silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTO'), recursive=True)[0]))
    drill = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.DRL'), recursive=True)[0]))
    try:
        outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GKO'), recursive=True)[0]))
    except:
        outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GM1'), recursive=True)[0]))

    print("Generando imagen de capa superior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    ctx = GerberCairoContext(scale=20)

    metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
    bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
    ctx.render_layer(outline, settings=metal_settings, bgsettings=bg_settings)

    metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
    bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)

    copper_settings = RenderSettings(color=(0.9 * 1.2, 0.5 * 1.2, 0.1 * 1.2))
    ctx.render_layer(mask, settings=copper_settings)

    our_settings = RenderSettings(color=theme.COLORS['white'], alpha=0.80)
    ctx.render_layer(silk, settings=our_settings)

    ctx.render_layer(drill)

    ctx.dump('VisionArtificial/PCB/board-top.png')

    ctx.clear()
    print("Cargando archivos de capa inferior...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBL'), recursive=True)[0]))
    mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBS'), recursive=True)[0]))
    silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GBO'), recursive=True)[0]))

    print("Generando imagen de capa inferior") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    ctx.render_layer(outline, settings=metal_settings, bgsettings=bg_settings)
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)
    ctx.render_layer(mask, settings=copper_settings)
    ctx.render_layer(silk, settings=our_settings)
    ctx.render_layer(drill)

    ctx.dump('VisionArtificial/PCB/board-bottom.png')

    im = Image.open('VisionArtificial/PCB/board-bottom.png')
    im_mirror = ImageOps.mirror(im)
    im_mirror.save('VisionArtificial/PCB/board-bottom.png', quality=100)

    print("Generando máscara para detección de PCB...") # Convertir en cuadro de dialogo en PyQt (round progress bar)
    if top:
        copper = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTL'), recursive=True)[0]))
        mask = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTS'), recursive=True)[0]))
        silk = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GTO'), recursive=True)[0]))
        drill = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.DRL'), recursive=True)[0]))
        try:
            outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GKO'), recursive=True)[0]))
        except:
            outline = load_layer(os.path.normpath(glob(os.path.join(CAMFolder, '**/*.GM1'), recursive=True)[0]))
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=False)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=False)
        ctx.render_layer(outline, settings=RenderSettings(color=(0, 0, 0)), bgsettings=bg_settings)
        ctx.render_layer(silk, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(drill, settings=RenderSettings(mirror=False))

    else:
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=True)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=True)
        ctx.render_layer(outline, settings=RenderSettings(color=(0, 0, 0), mirror=True), bgsettings=bg_settings)
        ctx.render_layer(silk, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        ctx.render_layer(drill, settings=RenderSettings(mirror=True))
    ctx.dump('VisionArtificial/PCB/board-mask.png')

def genImageList(CAMFolder : str, _top_bottom : bool):
    pnp = obtener_pnp(CAMFolder, _top_bottom)
    if(_top_bottom):
        img_path = "VisionArtificial/PCB/board-top.png"
    else:
        img_path = "VisionArtificial/PCB/board-bottom.png"
    img = Image.open(img_path)
    w , h = img.size
    I1 = ImageDraw.Draw(img)
    myFont = ImageFont.truetype('arial.ttf', 40)
    for componente in pnp:
        if(_top_bottom):
            bbox = I1.textbbox((float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), font=myFont, anchor='mm')
            I1.rectangle(bbox, fill='white')
            I1.text((float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), fill = 'red', font=myFont, anchor='mm')
        else:
            bbox = I1.textbbox((w-float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), font=myFont, anchor='mm')
            I1.rectangle(bbox, fill='white')
            I1.text((w-float(componente.x)*20,h-float(componente.y)*20), str(componente.numero), fill = 'red', font=myFont, anchor='mm')
    
    img.save("VisionArtificial/PCB/board-list.png")

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
            map_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

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

    # if --show argument used, then show result image
    plt.imshow(img3, 'gray'), plt.show()

    # result image path
    cv2.imwrite(os.path.join(os.getcwd(), 'VisionArtificial/PCB/mask.jpg'), map_img)
    cv2.imwrite(os.path.join(os.getcwd(), 'VisionArtificial/PCB/output.jpg'), img3)

    rot_deg = math.degrees(math.atan2((int(dst[1][0][0]) - int(dst[0][0][0])), (int(dst[1][0][1]) - int(dst[0][0][1]))))
    orig = dst[1][0] # punto de origen para PCBs
    dim_y, dim_x = map_img.shape # dimension de la imagen

    off_x = orig[0]-dim_x/2 # offset en x desde el centro de la imagen
    off_y = dim_y/2-orig[1] # offset en y desde el centro de la imagen

    return [off_x, off_y], rot_deg
