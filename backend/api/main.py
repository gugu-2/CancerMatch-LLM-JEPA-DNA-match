import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_engine.llm.rag_pipeline import RAGPipeline
from ai_engine.math.sequence_aligner import SequenceAligner
from ai_engine.math.thermodynamics import ThermodynamicsCalculator

app = FastAPI(title="PathoMatch Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG Pipeline (Ollama local inference)
rag = RAGPipeline()

class SamplePayload(BaseModel):
    species: str
    priorAntibiotics: bool
    notes: Optional[str] = None
    fileName: Optional[str] = None
    sequenceData: Optional[str] = None
    allergies: Optional[str] = None
    renalFunction: Optional[str] = "Normal"
    hardwareTier: Optional[str] = "base"

@app.get("/")
def read_root():
    return {"message": "Welcome to PathoMatch Backend API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/upload")
def upload_sample(payload: SamplePayload):
    math_results_str = ""
    
    # Trigger Math Engine if sequence data is provided
    if payload.sequenceData and len(payload.sequenceData.strip()) > 5:
        aligner = SequenceAligner()
        therm = ThermodynamicsCalculator()
        # Clean sequence (remove fasta header if present)
        seq = "".join([line for line in payload.sequenceData.split('\n') if not line.startswith('>')]).strip()
        target_marker = "ACGTACGT" # Mock pathogen marker
        
        if payload.hardwareTier == "base":
            # Protect 16GB RAM with chunked alignment & empirical scoring
            sw_score = aligner.chunked_alignment(seq, target_marker, window_size=2000)
            amr_pred = therm.lightweight_empirical_scoring(steric_clashes=2, h_bond_loss=1)
        else:
            # Premium Tier WGS simulation
            sw_score = aligner.smith_waterman_gotoh(seq[:1000], target_marker)
            amr_pred = therm.predict_amr(-10.0, -5.0)
            
        is_resistant = amr_pred.get('resistance_predicted', False)
        math_results_str = f" [Math Engine Detects Pathogen Match Score: {sw_score}. AMR Mutation Detected: {is_resistant}]"

    combined_notes = (payload.notes or "") + math_results_str

    # Trigger the RAG pipeline with species filter and EHR context + Math results
    report = rag.generate_report(
        species=payload.species, 
        notes=combined_notes,
        allergies=payload.allergies,
        renal_function=payload.renalFunction
    )
    
    # Determine a mock PDB ID for 3D Visualization based on Species/AMR logic
    mock_pdb_id = "1bna"
    if "canine" in payload.species.lower():
        mock_pdb_id = "4f2c"
    elif payload.priorAntibiotics:
        mock_pdb_id = "7d4f"

    return {
        "status": "success",
        "message": "Sample analyzed successfully.",
        "data_received": {
            "species": payload.species,
            "hardware_tier_used": payload.hardwareTier,
            "pdb_id": mock_pdb_id
        },
        "ai_report": report
    }
