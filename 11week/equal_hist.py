import cv2
import numpy as np
from matplotlib import pyplot as plt

img_name = input("Enter image name : ")
img = cv2.imread(img_name + ".png")
img = cv2.resize(img, (640, 480))

YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
Y,Cr,Cb = cv2.split(YCrCb)

equ_Y = cv2.equalizeHist(Y)
merge_img = cv2.merge((equ_Y,Cr,Cb))

res_img = cv2.cvtColor(merge_img, cv2.COLOR_YCrCb2BGR)

cimg = np.hstack((img, res_img))
cv2.imshow('Hist', cimg)

color = ('b', 'g', 'r')

for i, col in enumerate(color):
	histr = cv2.calcHist([img],[i],None,[256],[0,256])
	plt.plot(histr, color = col)
	plt.xlim([0,256])
plt.show()

for i, col in enumerate(color):
	histr = cv2.calcHist([res_img],[i],None,[256],[0,256])
	plt.plot(histr, color = col)
	plt.xlim([0,256])
plt.show()


cv2.waitKey()

