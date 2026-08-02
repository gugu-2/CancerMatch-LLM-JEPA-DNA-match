import React, { useState } from 'react';
import SampleUpload from './SampleUpload';

const Dashboard = () => {
  const [report, setReport] = useState(null);

  return (
    <div>
      <SampleUpload onUploadSuccess={(data) => setReport(data)} />

      {report && (
        <div className="ide-mockup-card" style={{ marginTop: '80px', animation: 'slideUp 0.5s ease-out' }}>
          <div className="ide-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span className="timeline-pill pill-done">DONE</span>
              <span style={{ fontSize: '12px', color: 'var(--c-muted)', padding: '2px 0', marginLeft: '8px' }}>
                Target: {report.data_received.species}
              </span>
            </div>
            
            {/* Display Safety Audit Status */}
            {report.ai_report.safety_audit && (
              <div style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span style={{ color: 'var(--c-muted-soft)' }}>LLM Auditor:</span>
                {report.ai_report.safety_audit.status === 'PASS' ? (
                  <span style={{ color: 'var(--c-success)', fontWeight: 'bold' }}>✓ PASS</span>
                ) : (
                  <span style={{ color: 'var(--c-error)', fontWeight: 'bold' }}>⚠ FAIL</span>
                )}
              </div>
            )}
          </div>

          {/* FIT Extrapolation Warning Banner */}
          {report.ai_report.extrapolated_from_human && (
            <div style={{ backgroundColor: 'var(--c-timeline-thinking)', color: 'var(--c-ink)', padding: '8px 16px', fontSize: '13px', fontWeight: '500', borderBottom: '1px solid var(--c-hairline)' }}>
              ⚠ Found In Translation (FIT): No veterinary guidelines found. Extrapolating from human clinical data.
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
            <div style={{ borderRight: '1px solid var(--c-hairline)' }}>
              <div style={{ padding: '24px', borderBottom: '1px solid var(--c-hairline)' }}>
                <h3 className="title-md" style={{ marginBottom: '8px' }}>Retrieved Context</h3>
                <div className="timeline-track" style={{ marginBottom: 0, marginTop: '12px' }}>
                  <span className="timeline-pill pill-grep">GREPPING</span>
                  <span className="timeline-pill pill-read">READING</span>
                </div>
              </div>
              <div className="ide-pane" style={{ margin: 0, border: 'none', borderRadius: 0, height: '100%' }}>
                {report.ai_report.retrieved_documents.length > 0 ? report.ai_report.retrieved_documents.map((doc, i) => (
                  <div key={i} style={{ marginBottom: '16px', color: 'var(--c-muted-soft)' }}>
                    // Source {i + 1}<br/>
                    <span style={{ color: 'var(--c-body)' }}>{doc}</span>
                  </div>
                )) : (
                  <div style={{ color: 'var(--c-muted-soft)' }}>// No context retrieved</div>
                )}
              </div>
            </div>

            <div>
              <div style={{ padding: '24px', borderBottom: '1px solid var(--c-hairline)' }}>
                <h3 className="title-md" style={{ marginBottom: '8px' }}>Treatment Recommendation</h3>
                <div className="timeline-track" style={{ marginBottom: 0, marginTop: '12px' }}>
                  <span className="timeline-pill pill-think">THINKING</span>
                  <span className="timeline-pill pill-edit">EDITING</span>
                </div>
              </div>
              <div className="ide-pane" style={{ margin: 0, border: 'none', borderRadius: 0, minHeight: '300px' }}>
                {report.ai_report.llm_response}
              </div>
            </div>
          </div>
          
          {/* 3D Biomolecular Visualization Panel */}
          {report.data_received.pdb_id && (
            <div style={{ borderTop: '1px solid var(--c-hairline)', padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h3 className="title-md">3D Structural Analysis</h3>
                <span className="timeline-pill" style={{ backgroundColor: 'var(--c-primary)', color: 'white' }}>
                  PDB: {report.data_received.pdb_id.toUpperCase()}
                </span>
              </div>
              <div style={{ height: '400px', width: '100%', position: 'relative', borderRadius: '8px', overflow: 'hidden', border: '1px solid var(--c-hairline)' }}>
                {/* 
                  The pdbe-molstar component requires absolute positioning to fill its container properly.
                  We pass the dynamically retrieved PDB ID to molecule-id.
                */}
                <pdbe-molstar 
                  molecule-id={report.data_received.pdb_id} 
                  hide-controls="true" 
                  bg-color-r="250" bg-color-g="250" bg-color-b="250"
                  style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
                ></pdbe-molstar>
              </div>
              <p style={{ fontSize: '13px', color: 'var(--c-muted)', marginTop: '12px' }}>
                Interactive 3D visualization powered by PDBe Molstar. 
                {report.data_received.hardware_tier_used === 'premium' ? 
                  " Rendering full MM/PBSA simulation." : 
                  " Rendering lightweight rigid-body empirical docking."}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
