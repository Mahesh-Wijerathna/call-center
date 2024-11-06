import sounddevice as sd
import numpy as np

import os
import playsound
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAD7sFiWRrKvdkzis_xCa81PsaDsdnte3k"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.0-pro-latest")





def speak(text):
    if not text:
        return
    tts = gTTS(text=text, lang='en')
    filename = 'voice_.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def get_audio():
    speak("Listening")
    r = sr.Recognizer()
    
    # Define the callback function to capture audio
    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_data = np.frombuffer(indata, dtype=np.int16)
        audio = sr.AudioData(audio_data.tobytes(), 44100, 2)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # Start recording system audio
    with sd.InputStream(callback=callback, channels=2, samplerate=44100):
        sd.sleep(5000)  # Record for 5 seconds


get_audio()