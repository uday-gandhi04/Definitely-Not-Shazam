import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './ResultCard'; // Ensure this matches the actual file casing exactly

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

      const data = res.data;

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
      console.error(err);
      setError("An error occurred during upload.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>🎵 Upload a Song Clip</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>{result}</div>
    </div>
  );
}
