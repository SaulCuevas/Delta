import sys

sys.path.append("../Delta")

from VisionArtificial import SVA_SMD
import cv2
import os
import math

path1 = "C:/Users/saulc/Downloads/CAM/test.png"
# path1 = "C:/Users/saulc/Downloads/IMG_20240110_222245.jpg"
path2 = path1
path3 = path1
path4 = path1

img1, img2, img3, img4, offsets_reales, rot_real = SVA_SMD.getCentroidAngleSMD(path1, path2, path3, path4)

cv2.imshow("im1", SVA_SMD.ResizeWithAspectRatio(img1, height=960))
cv2.imshow("im2", SVA_SMD.ResizeWithAspectRatio(img2, height=960))
cv2.imshow("im3", SVA_SMD.ResizeWithAspectRatio(img3, height=960))
cv2.imshow("im4", SVA_SMD.ResizeWithAspectRatio(img4, height=960))

cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd1.png'), img1)
cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd2.png'), img2)
cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd3.png'), img3)
cv2.imwrite(os.path.join(os.getcwd(), 'temp/output_smd4.png'), img4)

cv2.waitKey(0)
cv2.destroyAllWindows()