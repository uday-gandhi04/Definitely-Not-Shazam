// ContributeForm.js
import React, { useState } from 'react';
import axios from 'axios';

export default function ContributeForm() {
  const [url, setUrl] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse(null);

    try {
      const res = await axios.post('http://localhost:5000/api/contribute', { url });
      setResponse(res.data.message);
    } catch (err) {
      setResponse("Failed to process the link.");
    }
  };

  return (
    <div className="contribute-form">
      <h3>🎧 Contribute a Song or Playlist</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter YouTube song or playlist URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit">Submit</button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}
