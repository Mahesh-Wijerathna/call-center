# voice_call.py

import socket
import sounddevice as sd
import numpy as np
import tkinter as tk
import threading

# Audio Configuration
AUDIO_FORMAT = np.int16
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024

# Network Configuration
TARGET_HOST = "127.0.0.1"  # Use localhost for testing
SEND_PORT = 50009          # Port for sending audio
RECEIVE_PORT = 50008       # Port for receiving audio

# UDP Sockets Setup
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive.bind((TARGET_HOST, RECEIVE_PORT))

# Mute toggle state
is_muted = False

# Tkinter GUI Setup
root = tk.Tk()
root.title("Python WebRTC Voice Call")

status_label = tk.Label(root, text="Audio Status: Transmitting")
status_label.pack(pady=10)

def toggle_mute():
    global is_muted
    is_muted = not is_muted
    if is_muted:
        mute_button.config(text="Unmute")
        status_label.config(text="Audio Status: Muted")
    else:
        mute_button.config(text="Mute")
        status_label.config(text="Audio Status: Transmitting")

mute_button = tk.Button(root, text="Mute", command=toggle_mute)
mute_button.pack(pady=10)

# Audio Callback for Sending
def audio_callback(indata, frames, time, status):
    if status:
        print("Audio input error:", status)
    if not is_muted:
        # Send audio data as bytes
        sock_send.sendto(indata.tobytes(), (TARGET_HOST, SEND_PORT))

# Function to Start Sending Audio
def start_sending():
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype=AUDIO_FORMAT, callback=audio_callback, blocksize=CHUNK_SIZE):
        print("Audio streaming started...")
        root.mainloop()  # Keep the Tkinter GUI running

# Thread for Receiving and Playing Audio
def receive_audio():
    while True:
        try:
            data, _ = sock_receive.recvfrom(CHUNK_SIZE * 2)  # 2 bytes per int16 sample
            audio_data = np.frombuffer(data, dtype=AUDIO_FORMAT)
            print("Receiving audio data")
            sd.play(audio_data, SAMPLE_RATE)
        except Exception as e:
            print("Receiving error:", e)
            break

# Start Receiving Audio in a Separate Thread
receive_thread = threading.Thread(target=receive_audio)
receive_thread.daemon = True  # Allow the thread to close with the program
receive_thread.start()

# Start the Tkinter GUI and Sending Audio
start_sending()
