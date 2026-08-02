# PathoMatch: A Hybrid Mathematical & AI Framework for Genomic Intelligence

![PathoMatch Banner](https://img.shields.io/badge/Status-Beta_Ready-success?style=for-the-badge)
![Math Engine](https://img.shields.io/badge/Engine-Deterministic_Math-red?style=for-the-badge)
![AI Engine](https://img.shields.io/badge/LLM-RAG_Audited-blue?style=for-the-badge)

PathoMatch is a state-of-the-art bioinformatics platform designed to combat Antimicrobial Resistance (AMR) across multiple species. It completely abandons the industry trend of relying purely on probabilistic LLMs for biology. 

Instead, PathoMatch employs a **Hybrid Architecture**: It uses a pure, unconstrained mathematical engine (using $O(mn)$ Smith-Waterman arrays and MM/PBSA thermodynamics) to guarantee 100% deterministic DNA matching, and then feeds those proven facts into an LLM via Retrieval-Augmented Generation (RAG) to translate the math into clinical guidelines.

## The Core Innovations

### 1. The Mathematical Biological Engine
LLMs and JEPAs hallucinate. Math does not. PathoMatch includes a custom-built mathematical engine inside `ai_engine/math/`:
- **MinHash & Jaccard:** $O(1)$ heuristic sequence filtering.
- **Burrows-Wheeler Transform (BWT):** FM-Index backward search for exact read mapping.
- **Smith-Waterman (Gotoh's Algorithm):** $O(mn)$ dynamic programming arrays for perfect local alignment.
- **MM/PBSA Thermodynamics:** Calculates Antimicrobial Resistance (AMR) by predicting the structural Binding Free Energy ($\Delta G_{bind}$) of drugs against mutated targets.

### 2. Multi-Tier Hardware Architecture
To support both broke researchers and massive biotech enterprises, PathoMatch forks its algorithms dynamically:
- **Researcher Mode (Base):** Optimized for 16GB RAM laptops. Uses overlapping windowed sequence alignment (to prevent $O(mn)$ RAM crashes) and rigid-body empirical docking functions.
- **Enterprise Mode (Premium):** Unlocks unconstrained algorithms. Requires massive NVIDIA GPU clusters (A100/H100) for full water-solvent molecular dynamics simulations.

### 3. Interactive 3D Biomolecular Visualization
To build clinical trust, the UI integrates **PDBe Molstar** (the industry-standard European Bioinformatics Institute WebGL viewer). The dashboard renders stunning 3D models of the DNA or mutated proteins dynamically fetched from the Protein Data Bank (PDB).

### 4. Advanced Clinical Safety (NLP)
- **Found In Translation (FIT):** If veterinary guidelines for a specific species (e.g., Feline) are missing, the system automatically falls back to Human clinical data while clearly warning the physician.
- **LLM-as-a-Judge:** A secondary LLM agent continuously audits the primary generative output, verifying that it never hallucinates dosages that contradict the retrieved documents.

## Documentation Overview

1. 🚀 **[Deployment & Testing Guide](docs/DEPLOYMENT_GUIDE.md):** The absolute master guide on how to install requirements and launch the platform on new hardware.
2. 🏛️ **[Architecture Overview](docs/ARCHITECTURE.md):** The technical breakdown of the Math Engine, the Dual-Tier scaling, and the RAG pipeline.
3. 🔌 **[API Reference](docs/API_REFERENCE.md):** Details on the `/api/upload` endpoint and the complex JSON payloads (including hardware_tier).
4. 📈 **[Business Plan](docs/business_plan.md) & [Clinical Review](docs/clinical_launch_review.md):** Go-to-market strategies and CMO certifications.

## Quick Start
```bash
git clone https://github.com/gugu-2/CancerMatch-LLM-JEPA-DNA-match.git
cd patho_match
# Run the FastAPI Backend
cd backend
python -m uvicorn api.main:app --port 8000
# In a new terminal, run the Vite Frontend
cd frontend
npm run dev
```
