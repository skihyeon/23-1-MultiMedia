import numpy as np
import pyaudio
from scipy import signal
from scipy.io import wavfile
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
import playsound
from googletrans import Translator
import os 

dest_dir = 'C:/Konkuk_/23_1_MultiMedia/6week/trans_sounds/'
def listen():
    RATE = 16000
    CHUNK = RATE*5

    p = pyaudio.PyAudio()
    print("Speak now")
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)

    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    wavfile.write(dest_dir+'input.wav', RATE, data.astype(np.int16))

    r = sr.Recognizer()
    wavr = sr.AudioFile(dest_dir+'input.wav')
    with wavr as source:
        audio = r.record(source)
        print("Processing...")
        try:
            input_say = r.recognize_google(audio, language='ko-KR') # speech recognition from korean
            print("You said: " + input_say)
        except:
            input_say = None

    stream.stop_stream()
    stream.close()

    p.terminate()
    return input_say

def translate_and_speak(text, output_cnt):
    translator = Translator()
    translated_text = translator.translate(text, src='ko', dest='en').text 
    print(f"Translated Text: {translated_text}")
    tts = gTTS(text=translated_text, lang='en') 
    while os.path.isfile(dest_dir+'output_%d.wav' % output_cnt) :
        output_cnt += 1
    tts.save(dest_dir+'output_%d.wav' % output_cnt)
    d, fs = sf.read(dest_dir+'output_%d.wav' % output_cnt)
    ds = signal.resample(d, int(len(d)*16/24))
    sf.write(dest_dir+'output_%d.wav' % output_cnt,ds,16000)
    playsound.playsound(dest_dir+'output_%d.wav' % output_cnt)

output_cnt = 0

if __name__ == '__main__':
    while True:
        user_input = listen()
        if user_input:
            if user_input=="종료":
                break
            translate_and_speak(user_input, output_cnt)
