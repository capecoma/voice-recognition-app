# Voice Recognition App (Replit Version)

A Python application that listens for trigger words, records audio, and provides transcription using OpenAI's Whisper model. This version is optimized for running on Replit.

## Features

- Continuous listening for trigger words
- Automatic recording after trigger word detection
- Audio transcription using Whisper
- Real-time updates via WebSocket
- Web interface for control and monitoring

## Running on Replit

1. Create a new Replit
2. Choose "Import from GitHub"
3. Enter the repository URL
4. Select the `replit-version` branch
5. Click "Import from GitHub"

The application will automatically install dependencies and start running.

## Local Development

1. Clone the repository:
```bash
git clone -b replit-version https://github.com/capecoma/voice-recognition-app.git
cd voice-recognition-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. Open the web interface
2. Click the microphone button to start listening
3. Say a trigger word ("start", "record", or "begin") or use the simulation button
4. The app will record for 20 seconds and provide a transcription

## Configuration

You can modify:
- Trigger words
- Recording duration
- Whisper model size

Edit these settings in `voice_recorder.py`.

## License

MIT