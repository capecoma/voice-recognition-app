# Voice Recognition App

A Python application that listens for trigger words, records audio, and provides transcription using OpenAI's Whisper model.

## Features

- Continuous listening for trigger words
- Automatic recording after trigger word detection
- Audio transcription using Whisper
- Saves both audio recordings and transcriptions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/capecoma/voice-recognition-app.git
cd voice-recognition-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python voice_recorder.py
```

The app will:
1. Listen continuously for trigger words ("start", "record", or "begin")
2. Start recording for 20 seconds when a trigger word is detected
3. Transcribe the recording using Whisper
4. Save both the audio file and transcription

## Customization

You can modify:
- Trigger words
- Recording duration
- Whisper model size

Edit the parameters in `voice_recorder.py` to customize these settings.

## License

MIT