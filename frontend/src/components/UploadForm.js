import React, { useState } from 'react';
import axios from 'axios';

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const formData = new FormData();
      formData.append('file', file);

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
      setLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: '2rem' }}>
      <h2>🎵 Upload a Song Clip</h2>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => {
          setFile(e.target.files[0]);
          setResult(null);
          setError('');
        }}
      />
      <button onClick={handleUpload} disabled={loading || !file} style={{ marginLeft: '10px' }}>
        {loading ? 'Processing…' : 'Search'}
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
