import pyaudio
import pyttsx3
import threading
import queue

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Queue to manage text-to-speech requests
tts_queue = queue.Queue()

# Function to process the text-to-speech queue
def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        tts_engine.say(text)
        tts_engine.runAndWait()
        tts_queue.task_done()

# Start the text-to-speech worker thread
tts_thread = threading.Thread(target=tts_worker)
tts_thread.daemon = True
tts_thread.start()

# Function to capture audio and speak it out
def capture_and_speak():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print("Listening...")

    try:
        while True:
            data = stream.read(1024)
            # Here you can process the audio data if needed
            # For now, we will just speak out a placeholder text
            tts_queue.put("Speaking out audio input")
    except KeyboardInterrupt:
        pass

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Stop the text-to-speech worker thread
    tts_queue.put(None)
    tts_thread.join()

if __name__ == "__main__":
    capture_and_speak()