import cv2
import numpy as np
import random

class Filters :
	def __init__(self, img = cv2.imread('img2.png')):
		self.width = 320
		self.height = 240
		self.img_org = img
		self.img_res = cv2.resize(self.img_org, (self.width, self.height))

	def LPF_gray(self):
		ksize = int(input('Enter kernel size: '))
		kernel = np.ones((ksize,ksize), np.float32)/(ksize*ksize)
		ngain = float(input('Enter noise gain: '))

		img = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2GRAY)
		noisy = np.clip(img+np.random.random((self.height,self.width))*ngain, 0, 255).astype(np.uint8)
		filtered_img = cv2.filter2D(noisy, -1, kernel)
		cframe = np.hstack((img, noisy, filtered_img))
		message = 'Original, Noisy, Filtered'
		return message, cframe

	def LPF_color(self):
		ksize = int(input('Enter kernel size: '))
		kernel = np.ones((ksize,ksize), np.float32)/(ksize*ksize)
		ngain = float(input('Enter noise gain: '))

		img = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2YCrCb)
		Y, Cr, Cb = cv2.split(img)
		noisy = np.clip(Y + np.random.random((self.height,self.width))*ngain, 0, 255).astype(np.uint8)
		filtered = cv2.filter2D(noisy, -1, kernel)
		cnoisy = cv2.cvtColor(cv2.merge((noisy,Cr,Cb)), cv2.COLOR_YCrCb2BGR)
		cfiltered = cv2.cvtColor(cv2.merge((filtered,Cr,Cb)), cv2.COLOR_YCrCb2BGR)
		cframe = np.hstack((self.img_res, cnoisy, cfiltered))

		message = 'Original, Noisy, Filtered'
		return message, cframe

	def Gaussian(self):
		img_col = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2YCrCb)
		Y, Cr, Cb = cv2.split(img_col)
		blur = cv2.GaussianBlur(Y, (0,0), 2)
		filtered_Y = np.clip(2.0*Y - blur, 0, 255).astype(np.uint8)
		
		cfiltered = cv2.cvtColor(cv2.merge((filtered_Y, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
		cframe = np.hstack((cv2.flip(self.img_res,1), cv2.flip(cfiltered,1)))
		
		message = 'Original, Unsharp-mask'
		return message, cframe

	def Median(self):
		ksize = int(input('Enter kernel size: '))

		blurr = int(input('Gaussain blur : 1 \nsalt and pepper noise : 2 \n ==> '))
		img_col = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2YCrCb)
		Y, Cr, Cb = cv2.split(img_col)
		if blurr == 2:
			rat_noise = float(input('Enter frequency of salt and pepper noise(0 ~ 1): '))
			
			## salt and pepper noise ##
			num_noise = int(self.width*self.height*rat_noise)
			for i in range(num_noise):
				y = random.randint(0, self.height-1)
				x = random.randint(0, self.width-1)
				Y[y][x] = 255
			###########################

		elif blurr == 1:
			Y = cv2.GaussianBlur(Y, (0,0), 2)

		filtered = cv2.medianBlur(Y, ksize)
		cnoisy = cv2.cvtColor(cv2.merge((Y,Cr,Cb)), cv2.COLOR_YCrCb2BGR)
		cfiltered = cv2.cvtColor(cv2.merge((filtered, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
		cframe = np.hstack((self.img_res, cnoisy, cfiltered))

		message = 'Original, Noisy, Median-Filtered'
		return message, cframe

	def HPF(self):
		k_lap = np.array([[0,1,0],[1,-4,1],[0,1,0]])
		k_lap_e = np.array([[1,1,1],[1,-12,1],[1,1,1]])

		img_col = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2YCrCb)
		Y, Cr, Cb = cv2.split(img_col)
		Yf_lap = cv2.filter2D(Y, -1, k_lap)
		Yf_lap_e = cv2.filter2D(Y, -1, k_lap_e)
		img_lap = cv2.cvtColor(cv2.merge((Yf_lap, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
		img_lap_e = cv2.cvtColor(cv2.merge((Yf_lap_e, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
		cframe = np.hstack((self.img_res, img_lap, img_lap_e))
		message = 'HPF results'

		return message, cframe

	def Edge(self):
		gray = cv2.cvtColor(self.img_res, cv2.COLOR_BGR2GRAY)
		sobel = cv2.Sobel(gray, cv2.CV_8U, 2, 0 ,3)
		th1 = int(input('Enter two treshold 1 : '))
		th2 = int(input('Enter two treshold 2 : '))
		canny = cv2.Canny(gray, th1, th2)
		cframe = np.hstack((gray, sobel, canny))
		
		message = 'Gray, Sobel, Canny'
		cv2.imwrite('Canny.png', canny)
		return message, cframe