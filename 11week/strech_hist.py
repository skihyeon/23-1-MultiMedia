import cv2
import numpy as np

img_name = input("Enter image name : ")
img = cv2.imread(img_name + ".png")
img = cv2.resize(img, (640,480))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
max_y = np.max(gray)
min_y = np.min(gray)
cgray = (255.*(gray-min_y)/(max_y-min_y)).astype(np.uint8)
cimg = np.hstack((gray,cgray))
cv2.imshow('stretching', cimg)
cv2.waitKey()