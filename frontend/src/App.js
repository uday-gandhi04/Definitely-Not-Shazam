import ContributeForm from "./components/ContributeForm"
import RecordButton from "./components/RecordButton"
import UploadForm from "./components/UploadForm"
import "./styles.css"

export default function HomePage() {
  return (
    <div className="app-container">
      <div className="main-content-area">
        <div className="header-section">
          <h1 className="main-title">
            <span className="icon">🎵</span>NotShazam
          </h1>
          <p className="subtitle">Discover any song instantly with our advanced audio recognition technology</p>
        </div>

        <RecordButton />

        <hr className="section-separator" />

        <div className="cards-grid">
          <UploadForm />
          <div id="contribute-section">
            <ContributeForm />
          </div>
        </div>

        
      </div>
    </div>
  )
}
