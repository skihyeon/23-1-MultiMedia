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
win = "boxcar"
h_hp = signal.firwin(255, cutoff=0.125, window=win, pass_zero='highpass')
h_bp = signal.firwin(255, [0.0625,0.1875], window=win, pass_zero='bandpass')
h_bs = signal.firwin(255, [0.0625, 0.1875], window=win, pass_zero='bandstop')
##

in_data = np.zeros(CHUNK+kernel_size, dtype=np.int16)
filters = 'X'

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

while(True):
    samples = stream.read(CHUNK)
    in_data[kernel_size:kernel_size+CHUNK] = np.frombuffer(samples, dtype=np.int16)
    if filters == "highpass":
        out = signal.lfilter(h_hp, 1, in_data)
    elif filters == "bandpass":
        out = signal.lfilter(h_bp, 1, in_data)
    elif filters == "bandstop":
        out = signal.lfilter(h_bs, 1, in_data)
    else:
        out = in_data[kernel_size:kernel_size+CHUNK]

    stream.write(out.astype(np.int16).tobytes()) # cast back to int16 before writing to stream

    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('h'):
        filters = "highpass"
        print("Filter ON, highpass filter, " +win+" Window.")
    if keyboard.is_pressed('p'):
        filters = "bandpass"
        print("Filter ON, bandpass filter, " +win+" Window.")
    if keyboard.is_pressed('s'):
        filters = "bandstop"
        print("Filter ON, bandstop filter, "+win+" Window.")    
    if keyboard.is_pressed('x'):
        filters = "X"
        print("Filter Off.")

stream.stop_stream()
stream.close()
p.terminate()


