import numpy as np
import pyaudio
import keyboard
import time
import sys

RATE = 16000
CHUNK = int(RATE/10)
kernel_size = 37
kernel = np.full(kernel_size, 1/kernel_size)
in_data = np.zeros(CHUNK+kernel_size, dtype=np.int16)
filter_on = False

def convolution(signal, kernel):
	n_sig = signal.size
	n_ker = kernel.size

	rev_kernel = kernel[::-1].copy()
	result = np.zeros(n_sig - n_ker, dtype=np.int16)

	for i in range(n_sig - n_ker):
		if filter_on:
			result[i] = np.dot(signal[i:i+n_ker], rev_kernel)
		else:
			result[i] = signal[i+n_ker]

	signal[0:n_ker] = signal[n_sig-n_ker:n_sig]
	return result

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

while(True):
	samples = stream.read(CHUNK)
	in_data[kernel_size:kernel_size+CHUNK] = np.fromstring(samples, dtype=np.int16)
	#print(in_data)
	out = convolution(in_data, kernel)
	if in_data[0] > 700 :
		print("IN : ")
		print(in_data)
		print("OUT : ")
		print(out)
	y = out.tostring()
	stream.write(y)
	if keyboard.is_pressed('q'):
		break
	if keyboard.is_pressed('f'):
		if filter_on:
			filter_on = False
			print("Filter off.")
		else:
			filter_on = True
			print("Filter on.")

stream.stop_stream()
stream.close()
p.terminate()