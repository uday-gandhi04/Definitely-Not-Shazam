"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import ResultCard from "./ResultCard"
import NoMatchFoundCard from "./NoMatchFound"
import { Mic, Square, AlertCircle } from "lucide-react"

export default function RecordButton() {
  const [recording, setRecording] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  const [countdown, setCountdown] = useState(0)

  useEffect(() => {
    let interval = null
    if (recording && countdown > 0) {
      interval = setInterval(() => {
        setCountdown((countdown) => countdown - 1)
      }, 1000)
    } else if (countdown === 0) {
      clearInterval(interval)
    }
    return () => clearInterval(interval)
  }, [recording, countdown])

  const recordFor10Seconds = async () => {
    setRecording(true)
    setError("")
    setResult(null)
    setCountdown(10)

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      const audioChunks = []

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" })
        const formData = new FormData()
        formData.append("file", audioBlob, "recording.wav")

        try {
          const response = await axios.post("http://localhost:5000/api/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          })
          const data = response.data

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
          console.error("Error uploading audio:", err)
          setError("Error uploading audio. Please try again.")
        } finally {
          setRecording(false)
          setCountdown(0)
        }
      }

      mediaRecorder.start()
      setTimeout(() => {
        mediaRecorder.stop()
        stream.getTracks().forEach((track) => track.stop())
      }, 10000)
    } catch (err) {
      console.error("Microphone access error:", err)
      setError("Microphone access denied or not available. Please ensure permissions are granted.")
      setRecording(false)
      setCountdown(0)
    }
  }

  return (
    <div className="card record-card">
      <div className="card-header">
        <h2 className="card-title">
          <Mic className="icon" />
          Voice Recognition
        </h2>
        <p className="card-description">Tap the button and let us listen to identify your song</p>
      </div>

      <div className="record-section">
        <div className="record-button-container">
          <button
            onClick={recordFor10Seconds}
            disabled={recording}
            className={`record-button ${recording ? "recording" : ""}`}
          >
            {recording && (
              <div className="pulse-rings">
                <div className="pulse-ring"></div>
                <div className="pulse-ring"></div>
                <div className="pulse-ring"></div>
              </div>
            )}

            {recording ? <Square className="icon" /> : <Mic className="icon" />}
          </button>

          {recording && (
            <div className="recording-status">
              <div className="recording-timer">{countdown}s</div>
              <div className="recording-text">Listening...</div>
            </div>
          )}

          {!recording && !result && !error && <div className="recording-text">Tap to start recording</div>}
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle className="alert-icon" />
            <div className="alert-content">
              <h4 className="alert-title">Recording Error</h4>
              <p className="alert-description">{error}</p>
            </div>
          </div>
        )}

        {result && <div className="w-full">{result}</div>}
      </div>
    </div>
  )
}
