from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from voice_recorder import VoiceRecorder
import speech_recognition as sr
import numpy as np
import asyncio
from typing import List
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
websocket_connections: List[WebSocket] = []

async def status_broadcast(message: str):
    """Broadcast status to all connected clients."""
    for connection in websocket_connections:
        try:
            await connection.send_text(json.dumps({"type": "status", "message": message}))
        except:
            websocket_connections.remove(connection)

async def transcription_broadcast(transcription: str, timestamp: str):
    """Broadcast transcription to all connected clients."""
    for connection in websocket_connections:
        try:
            await connection.send_text(json.dumps({
                "type": "transcription",
                "text": transcription,
                "timestamp": timestamp
            }))
        except:
            websocket_connections.remove(connection)

# Modify VoiceRecorder to use async broadcasts
class AsyncVoiceRecorder(VoiceRecorder):
    async def start_recording(self):
        """Override start_recording to broadcast status and transcription."""
        self.recording = True
        
        with sr.Microphone() as source:
            await status_broadcast(f"Recording for {self.recording_duration} seconds...")
            try:
                audio = self.recognizer.record(source, duration=self.recording_duration)
                self.recording = False
                
                # Save audio to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.wav"
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe the recording
                await status_broadcast("Transcribing...")
                audio_data = np.frombuffer(audio.get_wav_data(), np.int16).flatten().astype(np.float32) / 32768.0
                result = self.whisper_model.transcribe(audio_data)
                
                # Save and broadcast transcription
                transcript_filename = f"transcript_{timestamp}.txt"
                with open(transcript_filename, "w") as f:
                    f.write(result["text"])
                
                await transcription_broadcast(result["text"], timestamp)
                await status_broadcast("Transcription complete")
                
            except Exception as e:
                await status_broadcast(f"Error during recording/transcription: {str(e)}")
                self.recording = False

recorder = AsyncVoiceRecorder()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "start_listening":
                recorder.start()
                await status_broadcast("Started listening for trigger words...")
            
            elif message["type"] == "stop_listening":
                recorder.stop()
                await status_broadcast("Stopped listening")
            
            # For testing: simulate trigger word detection
            elif message["type"] == "simulate_trigger":
                await recorder.start_recording()
    
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        if websocket in websocket_connections:
            websocket_connections.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)