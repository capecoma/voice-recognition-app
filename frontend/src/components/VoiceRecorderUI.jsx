import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Volume2, FileText } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

const VoiceRecorderUI = () => {
  const [isListening, setIsListening] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcriptions, setTranscriptions] = useState([]);
  const [status, setStatus] = useState('Idle');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'status') {
        setStatus(data.message);
        if (data.message.includes('Recording')) {
          setIsRecording(true);
        } else if (data.message.includes('complete')) {
          setIsRecording(false);
        }
      } else if (data.type === 'transcription') {
        setTranscriptions(prev => [...prev, {
          time: data.timestamp,
          text: data.text
        }]);
      }
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const toggleListening = () => {
    if (ws) {
      ws.send(JSON.stringify({
        type: isListening ? 'stop_listening' : 'start_listening'
      }));
      setIsListening(!isListening);
    }
  };

  const handleTriggerDetection = () => {
    if (ws) {
      ws.send(JSON.stringify({
        type: 'simulate_trigger'
      }));
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Voice Recognition Control</span>
            <button
              onClick={toggleListening}
              className={`p-4 rounded-full transition-colors ${
                isListening 
                  ? 'bg-green-100 hover:bg-green-200' 
                  : 'bg-red-100 hover:bg-red-200'
              }`}
            >
              {isListening ? <Mic className="text-green-600" /> : <MicOff className="text-red-600" />}
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert className="mb-4">
            <AlertDescription>{status}</AlertDescription>
          </Alert>

          {isListening && (
            <div className="mt-4">
              <button
                onClick={handleTriggerDetection}
                className="w-full p-4 bg-blue-100 hover:bg-blue-200 rounded-lg flex items-center justify-center gap-2"
                disabled={isRecording}
              >
                <Volume2 className="text-blue-600" />
                <span>Simulate Trigger Word Detection</span>
              </button>
            </div>
          )}
          
          {isRecording && (
            <div className="mt-4 p-4 bg-red-100 rounded-lg flex items-center justify-center gap-2">
              <Mic className="text-red-600 animate-pulse" />
              <span>Recording in progress...</span>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="text-gray-600" />
            Transcriptions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {transcriptions.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No transcriptions yet</p>
            ) : (
              transcriptions.map((trans, index) => (
                <div 
                  key={index}
                  className="p-4 bg-gray-50 rounded-lg"
                >
                  <div className="text-sm text-gray-500 mb-1">{trans.time}</div>
                  <div>{trans.text}</div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default VoiceRecorderUI;