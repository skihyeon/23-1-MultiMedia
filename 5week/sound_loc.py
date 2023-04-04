import numpy as np
import pyaudio
import sys
import keyboard

RATE = 48000
CHUNK = int(RATE/10)
HEAD = 10
DIS = 1
Vs = 339

max_delay = int(RATE*2*HEAD*.01/Vs)
aheadL = np.zeros(max_delay, dtype=np.int16)
aheadR = np.zeros(max_delay, dtype=np.int16)
out = np.zeros(CHUNK*2, dtype=np.int16)

##ITD
def Get_delay(dir_angle):
    distance = 2*HEAD*0.01*np.abs(np.sin(dir_angle))
    delay = int(distance*RATE/Vs)

    return distance, delay

##IID
def Sound_rendering(signal, dir):
    distance, delay = Get_delay(dir)

    if dir>=0:
        for i in range(CHUNK):
            if i < delay :
                out[i*2] = aheadL[max_delay - delay + i]
            else:
                out[i*2] = signal[(i-delay)*2]
            out[i*2] = int(out[i*2]*(DIS/(DIS+distance)))
            out[i*2+1] = signal[i*2]
    else:
        for i in range(CHUNK):
            if i < delay:
                out[i*2+1] = aheadR[max_delay - delay +i]
            else:
                out[i*2+1] = signal[(i-delay)*2]
            out[i*2+1] = int(out[i*2+1]*(DIS/(DIS+distance)))
            out[i*2] = signal[i*2]
    for i in range(max_delay):
        aheadL[i] = signal[((CHUNK-max_delay+i)*2)]
        aheadR[i] = signal[((CHUNK-max_delay+i)*2)]

    return out

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

rendering= True
target_dir = np.pi*float(sys.argv[1])/180
dir = target_dir

while(True):
    samples = stream.read(CHUNK)
    in_data = np.fromstring(samples, dtype=np.int16)
    out = Sound_rendering(in_data, dir)
    y = out.tostring()
    stream.write(y)
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('s'):
        if rendering:
            rendering = False
            dir = 0
            print("Sound_rendering off")
        else:
            rendering = True
            dir = target_dir
            print("Sound_rendering on")

stream.stop_stream()
stream.close()

p.terminate() 