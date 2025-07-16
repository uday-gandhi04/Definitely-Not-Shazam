import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './ResultCard'; // Ensure this matches the actual file casing exactly

export default function RecordButton() {
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const recordFor10Seconds = async () => {
    setRecording(true);
    setError('');
    setResult(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.mp3');

        try {
          const response = await axios.post('http://localhost:5000/api/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });

          const data = response.data;
          if (data.length === 0) {
            setResult("No match found.");
          } else if (data[0].confidence >= 90) {
            setResult(<ResultCard song={data[0]} />);
          } else {
            setResult(data.map((song, index) => (
              <ResultCard key={index} song={song} />
            )));
          }
        } catch (err) {
          setError('Error uploading audio.');
        }
        setRecording(false);
      };

      mediaRecorder.start();

      // Stop after 10 seconds
      setTimeout(() => {
        mediaRecorder.stop();
        stream.getTracks().forEach(track => track.stop());
      }, 10000);

    } catch (err) {
      setError('Microphone access denied or not available.');
      setRecording(false);
    }
  };

  return (
    <div className="record-button">
      <h3>🎤 Record Using Mic</h3>
      <button onClick={recordFor10Seconds} disabled={recording}>
        {recording ? "Recording (10s)..." : "Start 10-Second Recording"}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && <div>{result}</div>}
    </div>
  );
}
