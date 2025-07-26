"use client"

import { Link } from "lucide-react"

export default function NoMatchFoundCard() {
  const scrollToContribute = () => {
    const contributeSection = document.getElementById("contribute-section")
    if (contributeSection) {
      contributeSection.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <div className="no-match-message">
      <div className="no-match-content">
        <p className="no-match-text">Song not in results? It might not be in our database yet.</p>
        <button onClick={scrollToContribute} className="contribute-link-btn">
          <Link className="icon" />
          Contribute via YouTube link
        </button>
      </div>
    </div>
  )
}
