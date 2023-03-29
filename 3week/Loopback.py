import numpy as np
import pyaudio
import keyboard

RATE = 16000
CHUNK = int(RATE/10)

def process(signal):
	result = signal
	return result

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

while(True):
	samples = stream.read(CHUNK)
	in_data = np.fromstring(samples, dtype=np.int16)
	#print(in_data)
	out = process(in_data)
	y = out.tostring()
	stream.write(y)
	if keyboard.is_pressed('q'):
		break

stream.stop_stream()
stream.close()
p.terminate()