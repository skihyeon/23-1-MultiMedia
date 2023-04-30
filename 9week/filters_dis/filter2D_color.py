import cv2
import numpy as np

ksize = int(input('Enter kernel size:'))
kernel = np.ones((ksize, ksize), np.float32)/(ksize*ksize)
ngain = float(input('Enter noise gain:'))

width = 600
height = 400

img_org = cv2.imread('img.png')
img = cv2.cvtColor(img_org, cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(img)
noisy = np.clip(Y + np.random.random((height,width))*ngain, 0, 255).astype(np.uint8)
filtered = cv2.filter2D(noisy, -1, kernel)
cnoisy = cv2.cvtColor(cv2.merge((noisy,Cr,Cb)), cv2.COLOR_YCrCb2BGR)
cfiltered = cv2.cvtColor(cv2.merge((filtered,Cr,Cb)), cv2.COLOR_YCrCb2BGR)
cframe = np.hstack((img_org, cnoisy, cfiltered))

cv2.imshow('Original, Noisy, Filtered', cframe)
cv2.waitKey()