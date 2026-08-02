import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ai_engine.llm.rag_pipeline import RAGPipeline

app = FastAPI(title="PathoMatch Backend")

# Initialize the RAG Pipeline (Mock LLM)
rag = RAGPipeline()

class SamplePayload(BaseModel):
    species: str
    priorAntibiotics: bool
    notes: Optional[str] = None
    fileName: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to PathoMatch Backend API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/upload")
def upload_sample(payload: SamplePayload):
    # Trigger the RAG pipeline with the species filter
    report = rag.generate_report(species=payload.species, notes=payload.notes)
    
    return {
        "status": "success", 
        "message": f"Clinical report generated for {payload.species}",
        "data_received": payload.dict(),
        "ai_report": report
    }
