import numpy as np
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
from scipy import signal
import playsound
import os
from scipy.io import wavfile
RATE = 16000
CHUNK = RATE*2

p = pyaudio.PyAudio()
dest_dir = 'C:/Konkuk_/23_1_MultiMedia/6week/sounds/'

def listen():
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)
    print("Speak now")
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    wavfile.write(dest_dir+'input.wav', RATE, data.astype(np.int16))
    r = sr.Recognizer()
    wavr = sr.AudioFile(dest_dir+'input.wav')
    with wavr as source:
        audio = r.record(source)
        try:
            input_say = r.recognize_google(audio)
            print(f"You said: {input_say}")
        except sr.UnknownValueError:
            print("Sorry, response time out")
            return "Sorry"
    stream.stop_stream()
    stream.close()
    return input_say

def speak(text, output_cnt):
    tts = gTTS(text=text, lang='en')
    while os.path.isfile(dest_dir+'output_%d.wav' % output_cnt) :
        output_cnt += 1
    tts.save(dest_dir+'output_%d.wav' % output_cnt)
    d, fs = sf.read(dest_dir+'output_%d.wav' % output_cnt)
    ds = signal.resample(d, int(len(d)*16/24))
    sf.write(dest_dir+'output_%d.wav' % output_cnt, ds, 16000)
    playsound.playsound(dest_dir+'output_%d.wav' % output_cnt)

output_cnt = 0
speak("Hello, what can I help you with?",output_cnt)
while True:
    user_input = listen()
    if user_input.lower() == 'exit':
        break
    speak(f"You said: {user_input}", output_cnt)

p.terminate()
