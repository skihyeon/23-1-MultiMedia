import numpy as np
import pyaudio
import keyboard

RATE = 16000
CHUNK = int(RATE/10)

output = np.zeros(CHUNK*2, dtype=np.int16)

def Select_channel(signal, ch):
	for i in range(CHUNK):
		if ch=='left':
			output[i*2] = signal[i*2]
			output[i*2+1]=0
		else:
			output[i*2]=0
			output[i*2+1]=signal[i*2]
	return output

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

while(True):
	samples = stream.read(CHUNK)
	in_data = np.fromstring(samples, dtype=np.int16)
	#print(in_data)
	out = Select_channel(in_data, 'right')
	y = out.tostring()
	stream.write(y)
	if keyboard.is_pressed('q'):
		break

stream.stop_stream()
stream.close()
p.terminate()