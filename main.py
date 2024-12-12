from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from voice_recorder import VoiceRecorder
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve static files
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Initialize voice recorder
recorder = VoiceRecorder()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('start_listening')
def handle_start_listening():
    recorder.start()
    emit('status', {'message': 'Started listening for trigger words...'})

@socketio.on('stop_listening')
def handle_stop_listening():
    recorder.stop()
    emit('status', {'message': 'Stopped listening'})

@socketio.on('simulate_trigger')
def handle_simulate_trigger():
    recorder.start_recording()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    socketio.run(app, host='0.0.0.0', port=port)