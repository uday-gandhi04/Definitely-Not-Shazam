"use client"

import { useState } from "react"
import axios from "axios"
import { Link, Loader2, CheckCircle, AlertCircle } from "lucide-react"

export default function ContributeForm() {
  const [url, setUrl] = useState("")
  const [responseMessage, setResponseMessage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [isSuccess, setIsSuccess] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setResponseMessage(null)
    setLoading(true)
    setIsSuccess(null)

    try {
      const res = await axios.post("http://localhost:5000/api/contribute", { url })
      setResponseMessage(res.data.message)
      setIsSuccess(true)
      setUrl("")
    } catch (err) {
      console.error("Failed to process link:", err)
      setResponseMessage("Failed to process the link. Please check the URL and try again.")
      setIsSuccess(false)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">
          <Link className="icon" />
          Contribute Content
        </h2>
        <p className="card-description">Help expand our music database by submitting YouTube songs or playlists</p>
      </div>
      <div className="card-content">
        <form onSubmit={handleSubmit} className="form">
          <div className="input-group">
            <label htmlFor="youtube-url" className="input-label">
              YouTube URL
            </label>
            <input
              id="youtube-url"
              type="url"
              placeholder="https://youtube.com/watch?v=..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
              className="input-field"
            />
          </div>

          <button type="submit" disabled={loading || !url} className="btn btn-primary">
            {loading ? (
              <>
                <Loader2 className="icon spinner" />
                Processing...
              </>
            ) : (
              <>
                <Link className="icon" />
                Submit Contribution
              </>
            )}
          </button>
        </form>

        {responseMessage && (
          <div className={`alert ${isSuccess ? "alert-success" : "alert-error"}`}>
            {isSuccess ? <CheckCircle className="alert-icon" /> : <AlertCircle className="alert-icon" />}
            <div className="alert-content">
              <h4 className="alert-title">{isSuccess ? "Success!" : "Error"}</h4>
              <p className="alert-description">{responseMessage}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
