import React, { useState } from 'react';

function SampleUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [metadata, setMetadata] = useState({
    species: '',
    priorAntibiotics: false,
    notes: '',
    allergies: '',
    renalFunction: 'Normal',
    hardwareTier: 'base'
  });

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleMetadataChange = (e) => {
    const { name, value, type, checked } = e.target;
    setMetadata(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setLoadingStage('GREPPING');
    
    // Read the file content if a file is selected
    let sequenceData = "";
    if (file) {
      const text = await file.text();
      sequenceData = text;
    }

    const payload = {
      species: metadata.species,
      priorAntibiotics: metadata.priorAntibiotics,
      notes: metadata.notes,
      fileName: file ? file.name : null,
      sequenceData: sequenceData,
      allergies: metadata.allergies,
      renalFunction: metadata.renalFunction,
      hardwareTier: metadata.hardwareTier
    };

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      
      // Simulate network delay for AI processing feel
      setTimeout(() => setLoadingStage('THINKING'), 500);
      
      setTimeout(() => {
        setLoading(false);
        onUploadSuccess(data);
      }, 1200);
      
    } catch (error) {
      console.error('Error submitting payload', error);
      alert("Failed to connect to backend API");
      setLoading(false);
    }
  };

  return (
    <div className="surface-card feature-card">
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '24px', marginBottom: '24px', padding: '16px', backgroundColor: 'var(--c-background)', borderRadius: '6px', border: '1px solid var(--c-hairline)' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input 
                type="radio" 
                name="hardwareTier" 
                value="base" 
                checked={metadata.hardwareTier === 'base'} 
                onChange={handleMetadataChange}
                style={{ accentColor: 'var(--c-primary)' }}
              />
              <span style={{ fontWeight: '500' }}>Researcher Mode (Base)</span>
            </label>
            <p style={{ fontSize: '12px', color: 'var(--c-muted)', margin: '4px 0 0 24px' }}>Optimized for 16GB RAM laptops. Uses chunked alignment and empirical docking.</p>
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
              <input 
                type="radio" 
                name="hardwareTier" 
                value="premium" 
                checked={metadata.hardwareTier === 'premium'} 
                onChange={handleMetadataChange}
                style={{ accentColor: 'var(--c-primary)' }}
              />
              <span style={{ fontWeight: '500' }}>Enterprise Mode (Premium)</span>
            </label>
            <p style={{ fontSize: '12px', color: 'var(--c-muted)', margin: '4px 0 0 24px' }}>Requires massive GPU clusters. Uses unconstrained O(mn) alignment and MM/PBSA.</p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Sequence File (FASTA/FASTQ)</label>
            <input className="text-input" type="file" accept=".fasta,.fastq,.fa,.fq" onChange={handleFileChange} required />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Patient Species</label>
            <select className="text-input" name="species" value={metadata.species} onChange={handleMetadataChange} required>
              <option value="" disabled>Select patient species</option>
              <option value="Human">Human (Homo sapiens)</option>
              <option value="Canine">Canine (Canis lupus)</option>
              <option value="Feline">Feline (Felis catus)</option>
              <option value="Bovine">Bovine (Bos taurus)</option>
              <option value="Equine">Equine (Equus caballus)</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Patient Allergies</label>
            <input 
              className="text-input" 
              type="text" 
              name="allergies" 
              value={metadata.allergies} 
              onChange={handleMetadataChange} 
              placeholder="e.g. Penicillin, Sulfa" 
            />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Renal Function</label>
            <select className="text-input" name="renalFunction" value={metadata.renalFunction} onChange={handleMetadataChange}>
              <option value="Normal">Normal</option>
              <option value="Mild Impairment">Mild Impairment</option>
              <option value="Moderate Impairment">Moderate Impairment</option>
              <option value="Severe Impairment">Severe Impairment (Dialysis)</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Clinical Notes</label>
          <textarea 
            className="text-input"
            name="notes" 
            value={metadata.notes} 
            onChange={handleMetadataChange}
            placeholder="Enter patient symptoms, history, etc..."
          />
        </div>

        <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '32px' }}>
          <input 
            type="checkbox" 
            id="priorAnti"
            name="priorAntibiotics" 
            checked={metadata.priorAntibiotics} 
            onChange={handleMetadataChange} 
            style={{ width: '16px', height: '16px', accentColor: 'var(--c-primary)' }}
          />
          <label htmlFor="priorAnti" style={{ margin: 0 }}>Patient has received prior antibiotics</label>
        </div>

        <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={loading}>
          {loading ? (
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div className="spinner"></div> 
              {loadingStage === 'GREPPING' ? 'Grepping Guidelines...' : 'Thinking...'}
            </span>
          ) : "Analyze Sequence"}
        </button>
      </form>
    </div>
  );
}

export default SampleUpload;
