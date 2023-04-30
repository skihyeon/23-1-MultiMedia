import cv2
import random
import numpy as np

ksize = int(input('Enter kernel size: '))
rat_noise = float(input('Enter frequency of noise(0 ~ 1): '))

width = 320
height = 240

img_org = cv2.imread('img.png')
img_res = cv2.resize(img_org, (width, height))
img_col = cv2.cvtColor(img_res, cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(img_col)

## salt noise ##
num_noise = int(width*height*rat_noise)

for i in range(num_noise):
	y = random.randint(0, height-1)
	x = random.randint(0, width-1)
	Y[y][x] = 255

#################

## Median filtering ##
filtered = cv2.medianBlur(Y, ksize)
cnoisy = cv2.cvtColor(cv2.merge((Y, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
cfiltered = cv2.cvtColor(cv2.merge((filtered, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
cframe = np.hstack((img_res, cnoisy, cfiltered))

######################

cv2.imshow('Original, Noisy, Medain-filtered', cframe)

cv2.waitKey()