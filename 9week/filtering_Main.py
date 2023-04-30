import cv2
import numpy as np
from filters import Filters

print("Filters")
print("Lowpass filter_gray : LPFg")
print("Lowpass filter_color : LPFc")
print("Gaussian filter : Gaus")
print("Median filter : Medi")
print("Highpass filter : High")
print("Edge filter : Edge")

filter_input = str(input('Enter Filter Kind: '))

Ft = Filters()

if filter_input == 'LPFg':
	mes, res = Ft.LPF_gray()
	cv2.imshow(mes, res)

elif filter_input == 'LPFc':
	mes, res = Ft.LPF_color()
	cv2.imshow(mes, res)

elif filter_input == 'Gaus':
	mes, res = Ft.Gaussian()
	cv2.imshow(mes, res)

elif filter_input == 'Medi':
	mes, res = Ft.Median()
	cv2.imshow(mes, res)

elif filter_input == 'High':
	mes, res = Ft.HPF()
	cv2.imshow(mes, res)

elif filter_input == 'Edge':
	mes, res = Ft.Edge()
	cv2.imshow(mes, res)
else :
	print("Wrong filter")
	quit()

cv2.waitKey()

