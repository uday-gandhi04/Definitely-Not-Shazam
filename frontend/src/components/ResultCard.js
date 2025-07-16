import React from "react";

const ResultCard = ({ song }) => {
  return (
    <div className="result-card">
      <h3>{song.title}</h3>
      <p><strong>Artist:</strong> {song.artist}</p>
      <p><strong>Confidence:</strong> {song.confidence}%</p>
      <a href={song.youtube_url} target="_blank" rel="noopener noreferrer">
        Listen on YouTube
      </a>
    </div>
  );
};

export default ResultCard;
