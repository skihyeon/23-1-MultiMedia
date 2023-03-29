import sys
import pyaudio as pa
import math
import struct
import time

p = pa.PyAudio()

def callback(in_data, frame_count, time_info, status):
	levels = []
	for _i in range(1024):
		levels.append(struct.unpack('<h', in_data[_i:_i + 2])[0])
	avg_chunk = sum(levels)/len(levels)

	print(avg_chunk, time_info['current_time'])

	return (in_data, pa.paContinue)


stream = p.open(format=pa.paInt16, channels=1, rate=48000, frames_per_buffer=1024, input=True, input_device_index=0, stream_callback=callback)

time.sleep(10)
stream.close()
p.close()