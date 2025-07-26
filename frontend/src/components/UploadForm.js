"use client"

import { useState } from "react"
import axios from "axios"
import ResultCard from "./ResultCard"
import NoMatchFoundCard from "./NoMatchFound" // Import the new component
import { Upload, Loader2, AlertCircle } from "lucide-react"

export default function UploadForm() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.")
      return
    }

    setLoading(true)
    setError("")
    setResult(null)

    try {
      const formData = new FormData()
      formData.append("file", file)
      const res = await axios.post("http://localhost:5000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      const data = res.data

      console.log("API Response:", data) // Debug log

      if (!data || data.length === 0) {
        setResult(<NoMatchFoundCard />)
      } else {
        // Show results and add no match message if confidence is low
        const resultCards = data.map((song, index) => <ResultCard key={index} song={song} />)
        const hasLowConfidence = data.every((song) => song.confidence < 90)

        setResult(
          <div>
            {resultCards}
            {hasLowConfidence && <NoMatchFoundCard />}
          </div>,
        )
      }
    } catch (err) {
      console.error("Error during upload:", err)
      setError("An error occurred during upload. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <Upload className="icon" />
          File Upload
        </h2>
        <p className="card-description">Upload an audio file (MP3, WAV, M4A) to identify the song</p>
      </div>
      <div className="card-content">
        <div className="input-group">
          <label htmlFor="audio-file" className="input-label">
            Choose Audio File
          </label>
          <input
            id="audio-file"
            type="file"
            accept="audio/*"
            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
            className="input-field file-input"
          />
        </div>

        <button onClick={handleUpload} disabled={loading || !file} className="btn btn-primary">
          {loading ? (
            <>
              <Loader2 className="icon spinner" />
              Analyzing Audio...
            </>
          ) : (
            <>
              <Upload className="icon" />
              Identify Song
            </>
          )}
        </button>

        {error && (
          <div className="alert alert-error">
            <AlertCircle className="alert-icon" />
            <div className="alert-content">
              <h4 className="alert-title">Upload Error</h4>
              <p className="alert-description">{error}</p>
            </div>
          </div>
        )}

        {result && <div className="w-full">{result}</div>}
      </div>
    </div>
  )
}
