import cv2
import numpy as np

N = 256
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

while True :
	ret, img = cap.read()
	if ret:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)/256
		r_gray = cv2.resize(gray,(N,N))
		F = np.fft.rfft2(r_gray)
		F_sh = np.fft.fftshift(F)
		iF_sh = np.fft.ifftshift(F_sh)
		i_gray = np.clip(np.abs(np.fft.irfft2(iF_sh)),0,255)
		cframe = np.hstack((r_gray, i_gray))
		cv2.imshow('2D-FFT', cframe)

		key = cv2.waitKey(33)
		if key == ord('q'):
			break

cap.release()
cv2.destroyAllWinodws()