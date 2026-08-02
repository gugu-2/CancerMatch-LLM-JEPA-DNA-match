# PathoMatch Architecture Overview

PathoMatch is designed to solve a critical issue in modern veterinary and human medicine: Antimicrobial Resistance (AMR) across multiple species. It achieves this using an "Offline-First" architecture that guarantees absolute data privacy.

## System Components

### 1. The Frontend (React + Vite)
- **Location:** `/frontend`
- **Tech Stack:** React 18, Vite, Vanilla CSS.
- **Role:** Provides a premium, glassmorphism-styled UI for clinicians to upload FASTA/FASTQ sequence files. It captures crucial metadata, such as the patient's **Species** (Human, Canine, Bovine, etc.).

### 2. The Backend API (FastAPI)
- **Location:** `/backend`
- **Tech Stack:** Python, FastAPI, Pydantic, Uvicorn.
- **Role:** Serves as the central router. It receives the UI payloads, validates the schema (ensuring a species is strictly provided), and passes the context to the AI Engine.

### 3. The AI Engine (LangChain + ChromaDB)
- **Location:** `/ai_engine` & `/scripts/setup_vector_db.py`
- **Tech Stack:** LangChain, ChromaDB, HuggingFace SentenceTransformers, Ollama.
- **Role:** The core intelligence of the platform.
  - **Vector Store:** Clinical guidelines are ingested into a local ChromaDB and strictly tagged with `{"species": "..."}` metadata.
  - **Retrieval Augmented Generation (RAG):** When a sample arrives, LangChain filters the vector store by the exact species. This acts as a mathematical hard-guard against "Cross-Species Hallucination" (e.g., giving a dog a human-only antibiotic dosage).
  - **LLM Synthesis:** The retrieved documents and clinical notes are passed to a local LLM (Mistral via Ollama, currently stubbed with `FakeListLLM` for rapid testing) to generate the final treatment report.

### 4. Container Orchestration (Docker)
- **Location:** `/docker` & `docker-compose.yml`
- **Tech Stack:** Docker, Docker Compose.
- **Role:** Packages the Frontend, Backend, AI Engine, and caching layers (Redis) into isolated containers. This allows enterprise hospitals to deploy the entire stack on their internal intranet without ever sending patient DNA to external APIs like OpenAI.
