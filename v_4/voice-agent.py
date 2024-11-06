import os
import playsound
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

import sounddevice as sd
import numpy as np
from pydub import AudioSegment

GOOGLE_API_KEY = "AIzaSyAD7sFiWRrKvdkzis_xCa81PsaDsdnte3k"
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]
model = genai.GenerativeModel("gemini-1.0-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat()

system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
to this message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
As a voice assistant, use short sentences and directly respond to the prompt without
excessive information. You generate only words of value, prioritizing logic and facts
over speculating in your responses to the following prompts.''' 

system_message = system_message.replace("\n", " ")
convo.send_message(system_message)




# def keepConversation():


def askFromGoogle(question):    
    convo.send_message(question)
    if convo.last.text :
        print(convo.last.text)
        return convo.last.text
        


def load_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    audio = audio.set_channels(1)  # Convert to mono if needed
    sample_rate = audio.frame_rate
    audio_data = np.array(audio.get_array_of_samples()) / 32768.0  # Normalize
    return audio_data, sample_rate

def speak(text):
    if not text:
        return
    tts = gTTS(text=text, lang='en')
    filename = 'voice_.mp3'
    tts.save(filename)
    audio_data, sample_rate = load_audio(filename)
    sd.play(audio_data, samplerate=sample_rate, device='CABLE Input (VB-Audio Virtual C')
    sd.wait()
    os.remove(filename)


# Find the index of the device with the given name
mic_list = sr.Microphone.list_microphone_names()
device_index = None
def find_device_index():
    global device_index
    for i, name in enumerate(mic_list):
        if name == 'CABLE Output (VB-Audio Virtual ':
            device_index = i
            print("Microphone: " + name)
            break


def get_audio():
    global device_index, mic_list    
    r = sr.Recognizer()    
    # print("Microphone :" + str(mic_list[device_index]))
    with sr.Microphone(device_index) as source:
        audio = r.listen(source)
        
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    
    return said


status = "speaking"
text = "hey there "

def loop():
    global status
    global text
    if status == "speaking":
        if text:
            text = askFromGoogle(text )
            speak(text)
        status = "listening"
    elif status == "listening":
        print("Listening...")
        text = get_audio()
        status = "speaking"
    
    loop()

find_device_index()
loop()


