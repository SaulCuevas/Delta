# pcb-tools-extension / Pillow
import math
import os
import sys
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageOps
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext

import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 100


def putstr(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def genImage(CAMFolder, top):
    GERBER_FOLDER = os.path.abspath(os.path.join(CAMFolder, 'GerberFiles'))
    DRILL_FOLDER = os.path.abspath(os.path.join(CAMFolder, 'DrillFiles'))

    putstr('loading ')
    copper = load_layer(os.path.join(GERBER_FOLDER, 'copper_top.gtl'))
    putstr('.')
    mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask_top.gts'))
    putstr('.')
    silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen_top.gto'))
    putstr('.')
    drill = load_layer(os.path.join(DRILL_FOLDER, 'drill_1_16.drd'))
    putstr('.')
    outline = load_layer(os.path.join(GERBER_FOLDER, 'profile.gko'))
    putstr('. end\n')

    putstr('drawing ')
    ctx = GerberCairoContext(scale=20)
    putstr('.')

    metal_settings = RenderSettings(color=(30.0 / 255.0, 119.0 / 255.0, 93 / 255.0))
    bg_settings = RenderSettings(color=(30.0 / 300.0, 110.0 / 300.0, 93 / 300.0))
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)
    putstr('.')

    copper_settings = RenderSettings(color=(0.9 * 1.2, 0.5 * 1.2, 0.1 * 1.2))
    ctx.render_layer(mask, settings=copper_settings)
    putstr('.')

    our_settings = RenderSettings(color=theme.COLORS['white'], alpha=0.80)
    ctx.render_layer(silk, settings=our_settings)
    putstr('.')

    ctx.render_layer(outline)
    putstr('.')
    ctx.render_layer(drill)
    putstr('. end\n')

    putstr('dumping ... ')
    ctx.dump('Vision Artificial/PCB/board-top.png')
    putstr('end \n')

    ctx.clear()
    putstr('loading bottom ')
    copper = load_layer(os.path.join(GERBER_FOLDER, 'copper_bottom.gbl'))
    putstr('.')
    mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask_bottom.gbs'))
    putstr('.')
    silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen_bottom.gbo'))
    putstr('. end\n')

    putstr('drawing bottom ')
    ctx.render_layer(copper, settings=metal_settings, bgsettings=bg_settings)
    putstr('.')
    ctx.render_layer(mask, settings=copper_settings)
    putstr('.')
    ctx.render_layer(silk, settings=our_settings)
    putstr('.')
    ctx.render_layer(outline)
    putstr('.')
    ctx.render_layer(drill)
    putstr('. end\n')

    putstr('dumping bottom ...')
    ctx.dump('Vision Artificial/PCB/board-bottom.png')

    im = Image.open('Vision Artificial/PCB/board-bottom.png')
    im_mirror = ImageOps.mirror(im)
    im_mirror.save('Vision Artificial/PCB/board-bottom.png', quality=100)
    putstr('. end\n')

    if top:
        putstr('loading ')
        copper = load_layer(os.path.join(GERBER_FOLDER, 'copper_top.gtl'))
        putstr('.')
        mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask_top.gts'))
        putstr('.')
        silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen_top.gto'))
        putstr('.')
        drill = load_layer(os.path.join(DRILL_FOLDER, 'drill_1_16.drd'))
        putstr('.')
        outline = load_layer(os.path.join(GERBER_FOLDER, 'profile.gko'))
        putstr('. end\n')
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=False)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=False)
        ctx.render_layer(copper, settings=RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0)),
                         bgsettings=bg_settings)
        putstr('drawing mask ')
        putstr('.')
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        putstr('.')
        ctx.render_layer(silk, settings=RenderSettings(color=(1, 1, 1), mirror=False))
        putstr('.')
        ctx.render_layer(drill, settings=RenderSettings(mirror=False))
        putstr('.')

    else:
        ctx.clear()
        metal_settings = RenderSettings(color=(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0), mirror=True)
        bg_settings = RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0), mirror=True)
        ctx.render_layer(copper, settings=RenderSettings(color=(0.0 / 300.0, 0.0 / 300.0, 0.0 / 300.0)),
                         bgsettings=bg_settings)
        putstr('drawing mask ')
        putstr('.')
        ctx.render_layer(mask, settings=metal_settings, bgsettings=bg_settings)
        putstr('.')
        ctx.render_layer(silk, settings=RenderSettings(color=(1, 1, 1), mirror=True))
        putstr('.')
        ctx.render_layer(drill, settings=RenderSettings(mirror=True))
        putstr('.')
    putstr(' end\n')
    putstr('dumping mask ...')
    ctx.dump('Vision Artificial/PCB/board-mask.png')
    putstr(' end\n')


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
    cv2.imwrite(os.path.join(os.getcwd(), 'Vision Artificial/PCB/mask.jpg'), map_img)
    cv2.imwrite(os.path.join(os.getcwd(), 'Vision Artificial/PCB/output.jpg'), img3)

    rot_deg = math.degrees(math.atan2((int(dst[1][0][0]) - int(dst[0][0][0])), (int(dst[1][0][1]) - int(dst[0][0][1]))))

    return dst, rot_deg


if __name__ == "__main__":
    path = askdirectory(title='Selecciona la carpeta CAM', initialdir='C:/Users/saulc/Documents/EAGLE/projects')
    print(path)
    top_bottom = input('¿Es top layer? (Y/N) ')

    if top_bottom == 'Y' or top_bottom == 'y':
        genImage(path, top=True)
    elif top_bottom == 'N' or top_bottom == 'n':
        genImage(path, top=False)
    else:
        print('...')

    map_path = askopenfilename(title='Selecciona la imagen a comparar', filetypes=[("Imágenes", ".jpg .png")],
                               initialdir='C:/Users/saulc/Downloads/SIFT_PCB')

    # read images
    temp_img_gray = cv2.imread('Vision Artificial/PCB/board-mask.png', 0)
    map_img = cv2.imread(map_path)
    cv2.imwrite('Vision Artificial/PCB/from.jpg', map_img)

    # image segmentation
    # """
    hsv = cv2.cvtColor(map_img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 180])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    """
    gray = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)
    mask = cv2.Canny(gray, 30, 200)
    """

    # equalize histograms
    temp_img_eq = cv2.equalizeHist(temp_img_gray)
    map_img_eq = cv2.equalizeHist(mask)

    # calculate matched coordinates
    coords, grados_rot = get_matched_coordinates(temp_img_eq, map_img_eq)

    print(coords)
    print(grados_rot)
