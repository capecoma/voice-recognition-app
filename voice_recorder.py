import speech_recognition as sr
import whisper
import numpy as np
import threading
import time
from datetime import datetime

class VoiceRecorder:
    def __init__(self, trigger_words=None, recording_duration=20):
        """
        Initialize the voice recorder with optional trigger words and recording duration.
        
        Args:
            trigger_words (list): List of words that will trigger recording
            recording_duration (int): Duration to record in seconds after trigger
        """
        self.recognizer = sr.Recognizer()
        self.whisper_model = whisper.load_model("base")
        self.trigger_words = trigger_words or ["start", "record", "begin"]
        self.recording_duration = recording_duration
        self.is_listening = False
        self.recording = False
        
    def listen_for_trigger(self):
        """Continuously listen for trigger words."""
        self.is_listening = True
        print("Listening for trigger words:", self.trigger_words)
        
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1)
                    # Use whisper for trigger word detection
                    audio_data = np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0
                    result = self.whisper_model.transcribe(audio_data)
                    text = result["text"].lower()
                    
                    if any(word in text for word in self.trigger_words):
                        print("Trigger word detected! Starting recording...")
                        self.start_recording()
                        
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Error during listening: {str(e)}")
                    continue
    
    def start_recording(self):
        """Start recording for the specified duration."""
        self.recording = True
        
        with sr.Microphone() as source:
            print(f"Recording for {self.recording_duration} seconds...")
            try:
                audio = self.recognizer.record(source, duration=self.recording_duration)
                self.recording = False
                
                # Save audio to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe the recording
                print("Transcribing...")
                audio_data = np.frombuffer(audio.get_wav_data(), np.int16).flatten().astype(np.float32) / 32768.0
                result = self.whisper_model.transcribe(audio_data)
                
                # Save transcription
                transcript_filename = f"transcript_{timestamp}.txt"
                with open(transcript_filename, "w") as f:
                    f.write(result["text"])
                
                print(f"Transcription saved to {transcript_filename}")
                print("Transcription:", result["text"])
                
            except Exception as e:
                print(f"Error during recording/transcription: {str(e)}")
                self.recording = False
    
    def start(self):
        """Start the voice recorder."""
        self.listen_thread = threading.Thread(target=self.listen_for_trigger)
        self.listen_thread.start()
    
    def stop(self):
        """Stop the voice recorder."""
        self.is_listening = False
        if hasattr(self, 'listen_thread'):
            self.listen_thread.join()

def main():
    # Example usage
    recorder = VoiceRecorder(
        trigger_words=["start", "record", "begin"],
        recording_duration=20
    )
    
    try:
        recorder.start()
        print("Press Ctrl+C to stop...")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        recorder.stop()

if __name__ == "__main__":
    main()