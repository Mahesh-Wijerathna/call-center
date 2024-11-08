import threading
import tkinter as tk
import time

# Flags to control thread behavior
listening = False
watching = False

# Function to listen to the mic in a separate thread
def listen_mic():
    while True:
        if listening:
            print("Listening to the mic...")
            # Implement actual mic listening logic here
        time.sleep(1)  # Adjust according to listening needs

# Function to watch an image on the screen in a separate thread
def watch_image():
    while True:
        if watching:
            print("Watching the screen/image...")
            # Implement actual image watching logic here
        time.sleep(1)  # Adjust for watching frequency

# Start or stop the mic listening thread
def toggle_listen():
    global listening
    listening = not listening
    listen_button.config(text="Stop Listening" if listening else "Start Listening")

# Start or stop the image watching thread
def toggle_watch():
    global watching
    watching = not watching
    watch_button.config(text="Stop Watching" if watching else "Start Watching")

# Tkinter UI setup
root = tk.Tk()
root.title("Thread Controller")

listen_button = tk.Button(root, text="Start Listening", command=toggle_listen)
listen_button.pack(pady=10)

watch_button = tk.Button(root, text="Start Watching", command=toggle_watch)
watch_button.pack(pady=10)

# Thread setup
mic_thread = threading.Thread(target=listen_mic, daemon=True)
watch_thread = threading.Thread(target=watch_image, daemon=True)

mic_thread.start()
watch_thread.start()

root.mainloop()
