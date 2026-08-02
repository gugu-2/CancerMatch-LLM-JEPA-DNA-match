import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="app-container">
      <header className="top-nav">
        <div className="brand">PathoMatch <span className="text-muted" style={{ fontWeight: 400, marginLeft: '8px' }}>Genomics</span></div>
      </header>
      
      <main className="main-content">
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h1 className="display-lg" style={{ marginBottom: '16px' }}>Clinical Analysis</h1>
          <p className="body-md text-muted" style={{ marginBottom: '48px' }}>
            Upload a patient's DNA or protein sequence to securely retrieve targeted antimicrobial guidelines via the local intelligence engine.
          </p>
          <Dashboard />
        </div>
      </main>
    </div>
  );
}

export default App;
