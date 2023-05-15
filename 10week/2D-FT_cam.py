import cv2
import numpy as np

width = 320
height = 240

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
	ret, img = cap.read()
	if ret:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		F = np.fft.fft2(gray)
		Fshift = np.fft.fftshift(F)
		mag_spc = np.clip((20*np.log(np.abs(Fshift))),0, 255).astype(np.uint8)
		cframe = np.hstack((gray, mag_spc))
		cv2.imshow('2D-FFT', cframe)

		key = cv2.waitKey(33)
		if key == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()