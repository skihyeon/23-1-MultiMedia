import numpy as np
import pyaudio
import time

RATE = 16000
CHUNK = int(RATE/10)

p=pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=0)

fp = open('data.raw','wb')

prev=time.time()
cc=0
while(True):
	data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
	print('buffer=%d (%.4f)' % (cc, time.time()-prev))
	prev = time.time()
	data.tofile(fp)
	cc += 1
	if cc == 30:
		break

fp.close()
p.close()