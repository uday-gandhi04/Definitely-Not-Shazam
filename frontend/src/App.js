import React from 'react';
import UploadForm from './components/UploadForm';
import RecordButton from './components/RecordButton';
import ContributeForm from './components/ContributeForm';

function App() {
  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <h1>🔍 NotShazam</h1>
      <p>Identify any song from a clip or mic recording</p>
      <UploadForm />
      <hr style={{ margin: '2rem 0' }} />
      <RecordButton />
      <hr style={{ margin: '2rem 0' }} />
      <ContributeForm />
    </div>
  );
}

export default App;
