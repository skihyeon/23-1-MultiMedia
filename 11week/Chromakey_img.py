import cv2
import numpy as np

W=640
H=480

bimg_name = input("Enter background image name : ")
bimg = cv2.imread(bimg_name + ".png")
bimg = cv2.resize(bimg, (W,H))
bb, bg, br = cv2.split(bimg)

timg_name = input("Enter target image name : ")
timg = cv2.imread(timg_name + ".png")
timg = cv2.resize(timg, (W,H))
tb, tg, tr = cv2.split(timg)

for y in range(H):
	for x  in range(W):
		if tg.item(y,x)>120 and tb.item(y,x)>120 and tr.item(y,x)>120:
			tb.itemset(y,x,bb.item(y,x))
			tg.itemset(y,x,bg.item(y,x))
			tr.itemset(y,x,br.item(y,x))

rimg = cv2.merge((tb,tg,tr))
cimg = np.hstack((bimg, rimg))
cv2.imshow('Chroma key', cimg)

key = cv2.waitKey()
