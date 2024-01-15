import cv2
import numpy as np
import math

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

path = "C:/Users/saulc/Downloads/IMG_20240110_222245.jpg"
img = cv2.imread(path)

[h, w, _] = img.shape

mask = np.zeros((h,w,1), np.uint8)
cv2.circle(mask, [w,0], w, 255, -1)

points = np.array([[0, 0], [w, 0], [0, int(h*math.sin(math.radians(34)))]])
mask_r1 = np.zeros((h,w,1), np.uint8)
cv2.fillPoly(mask_r1, pts=[points], color=(255, 255, 255))
mask_r1 = cv2.bitwise_and(mask_r1, mask)

points = np.array([[0, int(h*math.sin(math.radians(35)))], [w, 0], [int(h*math.cos(math.radians(66))), h]])
mask_r2 = np.zeros((h,w,1), np.uint8)
cv2.fillPoly(mask_r2, pts=[points], color=(255, 255, 255))
mask_r2 = cv2.bitwise_and(mask_r2, mask)

points = np.array([[int(h*math.cos(math.radians(67))), h], [w, 0], [w, h]])
mask_r3 = np.zeros((h,w,1), np.uint8)
cv2.fillPoly(mask_r3, pts=[points], color=(255, 255, 255))
mask_r3 = cv2.bitwise_and(mask_r3, mask)

img_r1 = cv2.bitwise_and(img, img, mask=mask_r1)
img_r2 = cv2.bitwise_and(img, img, mask=mask_r2)
img_r3 = cv2.bitwise_and(img, img, mask=mask_r3)

cv2.imshow("r1", ResizeWithAspectRatio(img_r1, height=960))
cv2.imshow("r2", ResizeWithAspectRatio(img_r2, height=960))
cv2.imshow("r3", ResizeWithAspectRatio(img_r3, height=960))
cv2.waitKey(0)

for x in range(3):
    print(x)