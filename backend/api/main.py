import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_engine.llm.rag_pipeline import RAGPipeline

app = FastAPI(title="PathoMatch Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG Pipeline (Mock LLM)
rag = RAGPipeline()

class SamplePayload(BaseModel):
    species: str
    priorAntibiotics: bool
    notes: Optional[str] = None
    fileName: Optional[str] = None
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
    # Trigger the RAG pipeline with species filter and EHR context
    report = rag.generate_report(
        species=payload.species, 
        notes=payload.notes,
        allergies=payload.allergies,
        renal_function=payload.renalFunction
    )
    
    # Determine a mock PDB ID for 3D Visualization based on Species/AMR logic
    # 1bna = standard B-DNA, 7d4f = AMR Ribosome, 4f2c = Canine Parvovirus
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
