import pyaudio
import threading
import time
from google.cloud import speech
import os

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./nnnn.json"
speech_client = speech.SpeechClient()

class AudioStream:
    def __init__(self, rate=44100, chunk=512):
        self.rate = rate
        self.chunk = chunk
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.buffer = []
        self.is_listening = True

    def start_stream(self):
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def read_audio(self):
        """Continuously read audio and store in buffer."""
        while self.is_listening:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.buffer.append(data)

    def stop_stream(self):
        self.is_listening = False
        time.sleep(0.5)  # Small delay to ensure buffer clears
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def get_audio_buffer(self):
        """Retrieve audio data from buffer and clear it."""
        audio_data = b''.join(self.buffer)
        self.buffer.clear()
        return audio_data

def transcribe_audio(audio_stream):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=audio_stream.rate,
        language_code="en-US"
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    def request_generator():
        while audio_stream.is_listening:
            audio_data = audio_stream.get_audio_buffer()
            if audio_data:
                yield speech.StreamingRecognizeRequest(audio_content=audio_data)

    try:
        # Perform streaming recognition
        responses = speech_client.streaming_recognize(config=streaming_config, requests=request_generator())
        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    print("Final transcript:", transcript)
                else:
                    print("Interim transcript:", transcript)
    except Exception as e:
        print(f"Streaming error: {e}")

def main():
    # Initialize audio streaming
    audio_stream = AudioStream()
    audio_stream.start_stream()
    
    # Start a thread to read audio continuously
    audio_thread = threading.Thread(target=audio_stream.read_audio)
    audio_thread.start()
    
    try:
        # Start transcribing audio
        transcribe_audio(audio_stream)
    except KeyboardInterrupt:
        print("\nStopping transcription...")
    finally:
        # Stop audio stream and threading
        audio_stream.stop_stream()
        audio_thread.join()

if __name__ == "__main__":
    main()
