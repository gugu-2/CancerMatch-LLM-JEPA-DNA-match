import React, { useState } from 'react';

function SampleUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metadata, setMetadata] = useState({
    species: '',
    priorAntibiotics: false,
    notes: ''
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
    
    const payload = {
      species: metadata.species,
      priorAntibiotics: metadata.priorAntibiotics,
      notes: metadata.notes,
      fileName: file ? file.name : null
    };

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      
      // Simulate network delay for AI processing feel
      setTimeout(() => {
        setLoading(false);
        onUploadSuccess(data);
      }, 800);
      
    } catch (error) {
      console.error('Error submitting payload', error);
      alert("Failed to connect to backend API");
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Sequence File (FASTA/FASTQ)</label>
            <input type="file" accept=".fasta,.fastq,.fa,.fq" onChange={handleFileChange} required />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Patient Species</label>
            <select name="species" value={metadata.species} onChange={handleMetadataChange} required>
              <option value="" disabled>Select patient species</option>
              <option value="Human">Human (Homo sapiens)</option>
              <option value="Canine">Canine (Canis lupus)</option>
              <option value="Feline">Feline (Felis catus)</option>
              <option value="Bovine">Bovine (Bos taurus)</option>
              <option value="Equine">Equine (Equus caballus)</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Clinical Notes</label>
          <textarea 
            name="notes" 
            value={metadata.notes} 
            onChange={handleMetadataChange}
            placeholder="Enter patient symptoms, history, etc..."
          />
        </div>

        <div className="form-group">
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              name="priorAntibiotics" 
              checked={metadata.priorAntibiotics} 
              onChange={handleMetadataChange} 
            />
            Patient has received prior antibiotics
          </label>
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? (
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
              <div className="spinner"></div> Analyzing...
            </span>
          ) : "Analyze Sequence"}
        </button>
      </form>
    </div>
  );
}

export default SampleUpload;
