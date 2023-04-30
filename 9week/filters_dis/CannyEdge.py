import cv2
import numpy as np

width = 320
height = 240

img_org = cv2.imread('img.png')
img_res = cv2.resize(img_org, (width, height))
gray = cv2.cvtColor(img_res, cv2.COLOR_BGR2GRAY)
sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0 ,3)
canny = cv2.Canny(gray, 50, 150)
cframe = np.hstack((gray, sobel, canny))

cv2.imshow('Gray, Sobel, Canny', cframe)

cv2.waitKey()