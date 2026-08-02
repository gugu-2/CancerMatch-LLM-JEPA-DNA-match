import React, { useState } from 'react';
import SampleUpload from './SampleUpload';

const Dashboard = () => {
  const [report, setReport] = useState(null);

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Clinical Analysis</h2>
        <p style={{ color: 'var(--text-muted)' }}>Upload a patient's DNA/protein sample to retrieve targeted antimicrobial guidelines.</p>
      </div>

      <SampleUpload onUploadSuccess={(data) => setReport(data)} />

      {report && (
        <div className="glass-panel report-card">
          <h3>AI Clinical Report ({report.data_received.species})</h3>
          
          <div style={{ marginBottom: '2rem' }}>
            <h4 style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Treatment Recommendation</h4>
            <div className="report-content">
              {report.ai_report.llm_response}
            </div>
          </div>

          <div>
            <h4 style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Sources Retrieved (RAG)</h4>
            <ul className="docs-list">
              {report.ai_report.retrieved_documents.map((doc, i) => (
                <li key={i}>{doc}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
