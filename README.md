# Voice Recognition App

A Python application that listens for trigger words, records audio, and provides transcription using OpenAI's Whisper model. Includes both a backend API and a React frontend interface.

## Features

- Continuous listening for trigger words
- Automatic recording after trigger word detection
- Audio transcription using Whisper
- Real-time status updates via WebSocket
- Modern React frontend with live updates
- Saves both audio recordings and transcriptions

## Project Structure

```
├── backend/
│   ├── app.py              # FastAPI backend server
│   ├── voice_recorder.py   # Voice recognition implementation
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   └── components/    # React components
│   └── package.json       # Node.js dependencies
└── README.md
```

## Installation

### Backend

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python app.py
```

### Frontend

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Usage

1. Open the frontend application in your browser (typically http://localhost:3000)
2. Click the microphone button to start listening for trigger words
3. Say one of the trigger words ("start", "record", or "begin") or use the simulation button
4. The app will record for 20 seconds and then provide a transcription

## Customization

You can modify:
- Trigger words
- Recording duration
- Whisper model size

Edit the parameters in `backend/voice_recorder.py` to customize these settings.

## License

MIT
