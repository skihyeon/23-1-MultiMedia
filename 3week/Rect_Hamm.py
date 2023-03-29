import numpy as np
import pyaudio
import keyboard
import time
import sys
import scipy.signal as signal
import fplot

RATE = 16000
CHUNK = int(RATE/10)
kernel_size = 15

##define filters
Rect = signal.firwin(kernel_size, 0.125, window='boxcar', fs=RATE)
Hamm = signal.firwin(kernel_size, 0.125, window='hamming', fs=RATE)
##

##plot
fplot.mfreqz(Rect)
fplot.show()
fplot.mfreqz(Hamm)
fplot.show()
##

in_data = np.zeros(CHUNK+kernel_size, dtype=np.int16)
filters = 'X'

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

while(True):
    samples = stream.read(CHUNK)
    in_data[kernel_size:kernel_size+CHUNK] = np.frombuffer(samples, dtype=np.int16)
    if filters == "Rect":
        out = signal.lfilter(Rect, 1, in_data)
    elif filters == "Hamm":
        out = signal.lfilter(Hamm, 1, in_data)
    else:
        out = in_data[kernel_size:kernel_size+CHUNK]

    stream.write(out.astype(np.int16).tobytes())

    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('r'):
        filters = "Rect"
        print("Filter ON, Rectangular Window.")
    if keyboard.is_pressed('h'):
        filters = "Hamm"
        print("Filter ON, Hamming Window.")
    if keyboard.is_pressed('x'):
        filters = 'X'
        print("Filter Off")    
stream.stop_stream()
stream.close()
p.terminate()
