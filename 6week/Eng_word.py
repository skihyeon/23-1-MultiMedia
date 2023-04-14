import numpy as np
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
from scipy import signal
import playsound
import os
from scipy.io import wavfile
import time
import random
from googletrans import Translator


word_list = {
    'apple': '사과',
    'banana': '바나나',
    'cherry': '체리',
    'orange': '오렌지',
    'watermelon': '수박',
    'grape': '포도',
    'pineapple': '파인애플',
    'strawberry': '딸기',
    'melon': '멜론',
    'peach': '복숭아'
}

RATE = 16000
CHUNK = int(RATE*0.1)

p = pyaudio.PyAudio()
dest_dir = 'C:/Konkuk_/23_1_MultiMedia/6week/Eng_words/'

def listen():
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, 
        input=True, output=True, frames_per_buffer=CHUNK, input_device_index=0)
    print("Say word in 3sec!")
    data = []
    start_time = time.time()
    while True:
        chunk = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        data.append(chunk)
        elapsed_time = time.time() - start_time
        secs = int(elapsed_time)
        msecs = int((elapsed_time - int(elapsed_time)) * 10)
        timer = f"\rTime... {secs:02d}.{msecs:01d} sec"
        print(timer, end="")
        if elapsed_time > 3:
            break
    data = np.concatenate(data)
    wavfile.write(dest_dir+'input.wav', RATE, data.astype(np.int16))
    r = sr.Recognizer()
    wavr = sr.AudioFile(dest_dir+'input.wav')
    with wavr as source:
        audio = r.record(source)
        try:
            input_say = r.recognize_google(audio, language='ko-KR')
        except sr.UnknownValueError:
            return " "
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

user_score = 0
computer_score = 0

translator = Translator()

print("Hi, Word Memorization Game Start!")
speak("Hi, Word Memorization Game Start!",output_cnt)

iters=5

for i in range(iters):
    word, trans = random.choice(list(word_list.items()))
    print("---------Start %d/%d game---------" % (i+1,iters))
    print(f"*the word : {word}")
    speak(word, output_cnt)
    user_input = listen()
    if user_input.lower() == "Sorry":
        speak("Response time out", output_cnt)
        print(f"You loose! You : {user_score} vs. Com : {computer_score} points")
        computer_socre += 1
        break
    #translated = translator.translate(word, src='en', dest='ko').text
    print(f"\nYou said : {user_input}")
    if user_input == trans:
        user_score += 1
        print(f"You win! \nYou : {user_score} vs. Com : {computer_score} points")
        speak("You win!", output_cnt)
    elif user_input != trans:
        computer_score += 1
        print(f"You loose! \nYou : {user_score} vs. Com : {computer_score} points")
        speak("I win!", output_cnt)
    print("------------End %d/%d game---------" % (i+1,iters))
    time.sleep(1)
if user_score > computer_score:
    print("Congratulations! You won the game.")
    speak("Congratulations! You won the game.", output_cnt)
elif user_score < computer_score:
    print("Better luck next time. The computer won the game.")
    speak("Better luck next time. The computer won the game.", output_cnt)
else:
    print("It's a tie!")


p.terminate()
