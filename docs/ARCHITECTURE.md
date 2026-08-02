# PathoMatch Architecture Overview

PathoMatch is built on a **Hybrid Architecture** that strictly separates probabilistic Natural Language Processing from deterministic biological math.

## 1. The Frontend (UI & 3D Visualization)
- **Framework:** React + Vite. Designed with an editorial, minimalist "Cursor" aesthetic (cream canvas, near-black ink, 1px hairlines).
- **3D Viewer:** Integrates the `<pdbe-molstar>` Web Component to render WebGL macromolecular structures (PDB/mmCIF) in real-time, allowing users to spin and zoom into structural clashes causing Antimicrobial Resistance.
- **Interaction:** Collects massive DNA FASTA payloads, user hardware configurations (`hardwareTier`), and Patient EHR constraints (Allergies, Renal Function) and proxies them to the backend API.

## 2. The Deterministic Biological Engine (Backend Math)
Instead of relying on AI to "guess" genetics, PathoMatch uses custom Python mathematical calculators located in `backend/ai_engine/math/`.
- **`bio_algorithms.py`**: Executes MinHash/Jaccard approximation and Burrows-Wheeler Transform FM-Indexing.
- **`sequence_aligner.py`**: Executes $O(mn)$ Smith-Waterman local alignment using Gotoh's affine gap penalty matrices, corrected by Jukes-Cantor evolutionary distances.
- **`thermodynamics.py`**: Calculates $\Delta G_{bind}$ using MM/PBSA equations or lightweight empirical rigid-body scoring (depending on the hardware tier).

## 3. Multi-Tier Hardware Scaling
Because the Math engine pushes hardware to its absolute limits, PathoMatch forks its execution based on the API `hardwareTier` parameter:
- **Base (Researcher Mode):** Restricts execution to a 16GB RAM / 8GB VRAM footprint by using overlapping sliding windows for Smith-Waterman and empirical docking.
- **Premium (Enterprise Mode):** Bypasses all constraints, demanding massive cloud RAM and NVIDIA GPU clusters to run unchunked $O(mn)$ matrices and full Molecular Dynamics.

## 4. The Clinical NLP Engine (RAG & Safety)
Located in `backend/ai_engine/llm/rag_pipeline.py`. Once the math engine proves the biological facts, the NLP engine translates them into medical advice.
- **Strict RAG:** Queries a ChromaDB vector store strictly filtered by the incoming `species` metadata.
- **Found In Translation (FIT):** If veterinary species data is absent, the retriever automatically climbs the taxonomic hierarchy to pull Human clinical data, flagging the UI to warn the clinician.
- **Safety Auditor:** A secondary `SafetyAuditor` class intercepts the generated LLM report and acts as a "Judge", blocking the response if it detects hallucinatory dosages or contraindications against the Patient's EHR.
