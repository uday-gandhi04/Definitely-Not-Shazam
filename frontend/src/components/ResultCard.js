"use client"
import { ExternalLink } from "lucide-react"

const ResultCard = ({ song }) => {
  return (
    <div className="card result-card">
      <div className="result-card-header">
        <h3 className="result-card-title">{song.title}</h3>
        <p className="result-card-artist">by {song.artist}</p>
      </div>
      <div className="card-content">
        <div className="confidence-row">
          <span className="confidence-label">Confidence Score</span>
          <span className="confidence-badge">{song.confidence.toFixed(1)}%</span>
        </div>
        {song.youtube_url && (
          <a href={song.youtube_url} target="_blank" rel="noopener noreferrer" className="youtube-link">
            <ExternalLink className="icon" />
            Listen on YouTube
          </a>
        )}
      </div>
    </div>
  )
}

export default ResultCard
