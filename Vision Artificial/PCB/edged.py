import cv2

_from = cv2.imread('Vision Artificial/PCB/from.jpg')
edged = cv2.Canny(_from, 30, 30)
cv2.imwrite('Vision Artificial/PCB/from-edged.png', edged)