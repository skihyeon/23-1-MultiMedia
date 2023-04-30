import cv2
import numpy as np

width = 320
height = 240

k_lap = np.array([[0,1,0],[1,-4,1],[0,1,0]])
k_lap_e = np.array([[1,1,1],[1,-8,1],[1,1,1]])

img_org = cv2.imread('img.png')
img_res = cv2.resize(img_org, (width,height))
img_col = cv2.cvtColor(img_res, cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(img_col)

Yf_lap = cv2.filter2D(Y, -1, k_lap)
Yf_lap_e = cv2.filter2D(Y, -1, k_lap_e)
img_lap = cv2.cvtColor(cv2.merge((Yf_lap, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
img_lap_e = cv2.cvtColor(cv2.merge((Yf_lap_e, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
cframe = np.hstack((img_res, img_lap, img_lap_e))

cv2.imshow('High-pass filtered results', cframe)

cv2.waitKey()