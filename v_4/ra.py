import os
import playsound
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAD7sFiWRrKvdkzis_xCa81PsaDsdnte3k"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.0-pro-latest")







# def keepConversation():


def askFromGoogle(question):    
    response = model.generate_content(question)
    if response._result and response._result.candidates:
        answer = response._result.candidates[0].content.parts[0].text
        print(answer)
        return answer



def speak(text):
    if not text:
        return
    tts = gTTS(text=text, lang='en')
    filename = 'voice_.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio():
    speak("Is there anything you would like to ask?")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        speak('mmm ...')
        
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
            # speak(text)
            text = askFromGoogle(text )
            speak(text)
        status = "listening"
    elif status == "listening":
        print("Listening...")
        text = get_audio()
        status = "speaking"
    
    loop()



loop()





