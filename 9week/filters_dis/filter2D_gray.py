import cv2
import numpy as np

ksize = int(input('Enter kernel size:'))
kernel = np.ones((ksize, ksize), np.float32)/(ksize*ksize)
ngain = float(input('Enter noise gain:'))

width = 600
height = 400

img = cv2.imread('img.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
noisy = np.clip(img+np.random.random((height, width))*ngain, 0, 255).astype(np.uint8)
filtered_img = cv2.filter2D(noisy, -1, kernel)
cframe = np.hstack((img, noisy, filtered_img))
cv2.imshow('Original, Noisy, Filtered', cframe)

key = cv2.waitKey()

