import pyaudio
import wave
import sys

BUFFER_SIZE = 1024

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

file_sw = wf.getsampwidth()

stream = p.open(format=p.get_format_from_width(file_sw), channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

data = wf.readframes(BUFFER_SIZE)

while len(data)>0:
	stream.write(data)
	data = wf.readframes(BUFFER_SIZE)

stream.stop_stream()
stream.close()

p.terminate()