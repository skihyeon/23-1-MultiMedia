import cv2
import numpy as np

width = 320
height = 240

img_org = cv2.imread('img.png')
img_res = cv2.cvtColor(img_org, cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(img_res)
blur = cv2.GaussianBlur(Y, (0,0), 2)
filtered_Y = np.clip(2.0*Y - blur, 0, 255).astype(np.uint8)
cfiltered = cv2.cvtColor(cv2.merge((filtered_Y, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
cframe = np.hstack((cv2.flip(img_org,1), cv2.flip(cfiltered,1)))
cv2.imshow('Original, Unsharp-mask', cframe)

cv2.waitKey()