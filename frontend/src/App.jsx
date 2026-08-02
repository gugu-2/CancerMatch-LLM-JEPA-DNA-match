import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="app-container">
      <aside className="sidebar">
        <h1>PathoMatch</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
          Genomic Intelligence for One Health
        </p>
      </aside>
      <main className="main-content">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
