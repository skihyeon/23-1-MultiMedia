import cv2
import numpy as np

def Build_H_LPF(N, f_radius):
	HN = N/2
	H = np.zeros((N,N), dtype=np.float32)

	for y in range(N):
		for x in range(N):
			fy = (y-HN)/HN
			fx = (x-HN)/HN
			radius = np.sqrt(fy*fy+fx*fx)
			if radius <= f_radius:
				H[y][x] = 1
	return H

def Build_H_HPF(N, f_radius):
	HN = N/2
	H = np.ones((N,N), dtype=np.float32)

	for y in range(N):
		for x in range(N):
			fy = (y-HN)/HN
			fx = (x-HN)/HN
			radius = np.sqrt(fy*fy+fx*fx)
			if radius <= f_radius:
				H[y][x] = 0
	return H

def Filter2D_FT(Fin,H):
	mag = np.abs(Fin)
	phs = np.angle(Fin)
	fmag = H*mag
	return fmag*np.exp(1j*phs)

def F2D_FT(gray,N):
	gray = cv2.resize(gray, (N,N))
	F = np.fft.fft2(gray)
	Fshift = np.fft.fftshift(F)
	mag_spc = np.clip((20*np.log(np.abs(Fshift))),0,255).astype(np.uint8)
	cframe = np.hstack((gray, mag_spc))
	mes = '2D-FT'
	return mes, cframe

def F2D_FT_loopback(gray, N):
	gray = gray/255
	r_gray = cv2.resize(gray, (N,N))
	F = np.fft.rfft2(r_gray)
	F_sh = np.fft.fftshift(F)
	iF_sh = np.fft.ifftshift(F_sh)
	i_gray = np.clip(np.abs(np.fft.irfft2(iF_sh)),0 ,255)
	cframe = np.hstack((r_gray, i_gray))
	mes = '2D-FT_loopback'
	return mes, cframe

def F2D_FT_filter_LPF(gray, N):
	fcut = float(input("Enter cut-off radius[0~1]: "))
	H = Build_H_LPF(N, fcut)
	img_H = (H*255).astype(np.uint8)
	gray = gray/255
	r_gray = cv2.resize(gray,(N,N))
	F = np.fft.fft2(r_gray)
	F_sh = np.fft.fftshift(F)
	FF = Filter2D_FT(F_sh, H)
	iF_sh = np.fft.ifftshift(FF)
	i_gray = np.clip(np.abs(np.fft.ifft2(iF_sh)),0,255)
	cframe = np.hstack((img_H, r_gray, i_gray))
	mes = '2D-FT_filter'
	return mes, cframe

def F2D_FT_filter_HPF(gray, N):
	fcut = float(input("Enter cut-off radius[0~1]: "))
	H = Build_H_HPF(N, fcut)
	img_H = (H*255).astype(np.uint8)
	gray = gray/255
	r_gray = cv2.resize(gray,(N,N))
	F = np.fft.fft2(r_gray)
	F_sh = np.fft.fftshift(F)
	FF = Filter2D_FT(F_sh, H)
	iF_sh = np.fft.ifftshift(FF)
	i_gray = np.clip(np.abs(np.fft.ifft2(iF_sh)),0,255)
	cframe = np.hstack((img_H, r_gray, i_gray))
	mes = '2D-FT_filter'
	return mes, cframe

N = 256
menu = 0

img = cv2.imread("new_image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#https://darkpgmr.tistory.com/171

print("Choose Menu!\n1.2D-FT\n2.2D-FT_loopback\n3.2D-FT_filter_LPF\n4.2D-FT_filter_HPF")
menu = int(input("input menu:"))

if menu == 1:
    mes, show_img = F2D_FT(gray, N)
elif menu == 2:
    mes, show_img = F2D_FT_loopback(gray, N)
elif menu == 3:
    mes, show_img = F2D_FT_filter_LPF(gray, N)
elif menu == 4:
	mes, show_img = F2D_FT_filter_HPF(gray, N)

cv2.imshow(mes, show_img)
key = cv2.waitKey()


cv2.destroyAllWindows()