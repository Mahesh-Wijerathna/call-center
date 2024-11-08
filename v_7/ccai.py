import sounddevice as sd
import numpy as np
import pyautogui
import pyscreeze
import tkinter as tk
import cv2
import speech_recognition as sr
import google.generativeai as genai
from pydub import AudioSegment
from gtts import gTTS
import os

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

# Find the index of the device with the given name
mic_list = sr.Microphone.list_microphone_names()
device_index = None
def find_device_index():
    global device_index
    for i, name in enumerate(mic_list):
        if name == 'CABLE Output (VB-Audio Virtual ':
            device_index = i
            # print("Microphone: " + name)
            break

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

# Parameters
DURATION = 0.5  # Duration to listen (seconds)
SAMPLE_RATE = 44100  # Sampling rate in Hz
VOLUME_THRESHOLD = 0.01  # Volume threshold for triggering

class VolumeDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Volume Spike Detector")

        # Start and stop buttons
        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Label to show detection status
        self.status_label = tk.Label(root, text="Press Start to begin listening.", font=("Arial", 14))
        self.status_label.pack(pady=20)

        # Flag to control listening loop
        self.listening = False

    def listen_for_volume_increase(self):
        # Record audio for a short duration
        recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()  # Wait for recording to finish

        # Calculate the volume level
        volume_level = np.mean(np.abs(recording))

        # Check if the volume exceeds the threshold
        return volume_level > VOLUME_THRESHOLD

    def start_listening(self):
        self.listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Listening for volume increase...")
        self.listen_loop()

    def listen_loop(self):
        if self.listening:
            if self.listen_for_volume_increase():
                self.status_label.config(text="Call Detected!")
                self.listening = False
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.answer_call()

            else:
                self.status_label.config(text="Listening for volume increase...")
            # Schedule the next check without using threads
            self.root.after(500, self.listen_loop)

    def stop_listening(self):
        self.listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped listening.")

    def keep_call(self):
        find_device_index()
        loop()

    def answer_call(self):
        try:            
            answer_button = pyautogui.locateCenterOnScreen('answer.png',confidence=0.8)
            if answer_button is not None:
                # print(answer_button)
                pyautogui.moveTo(answer_button)
                pyautogui.click()
                self.status_label.config(text="Call Answered ......")
                self.keep_call()

            else: 
                print("Answer button not found.")
                self.status_label.config(text="Answer button not found.")
        except pyscreeze.ImageNotFoundException as e:
            print(f"Error: {e}")
            self.status_label.config(text="Error: Could not locate the image.")

    

# Run the app
root = tk.Tk()
app = VolumeDetectorApp(root)
root.mainloop()
