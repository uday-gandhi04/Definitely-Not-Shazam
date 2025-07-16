import React, { useState } from 'react';
import axios from 'axios';

export default function RecordButton() {
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const startRecording = async () => {
    setError('');
    setResult(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', blob, 'recording.webm');

        try {
          const res = await axios.post('http://localhost:5000/api/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          console.log('Response:', res.data);
          if (res.data && res.data.title) {
            setResult(res.data);
          } else {
            setError('No match found.');
          }
        } catch (err) {
          console.error(err);
          setError(err.response?.data?.error || 'An error occurred.');
        } finally {
          setRecording(false);
        }
      };

      recorder.start();
      setRecording(true);

      // Auto-stop after 5 seconds
      setTimeout(() => {
        recorder.stop();
      }, 5000);

    } catch (err) {
      console.error(err);
      setError('Microphone access denied or not available.');
    }
  };

  return (
    <div>
      <h2>🎤 Record Using Mic</h2>
      <button onClick={startRecording} disabled={recording}>
        {recording ? 'Recording…' : 'Start Recording'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Match Found:</h3>
          <p><strong>{result.title}</strong> by {result.artist}</p>
          <a href={result.youtube_url} target="_blank" rel="noopener noreferrer">
            Watch on YouTube
          </a>
        </div>
      )}
    </div>
  );
}
