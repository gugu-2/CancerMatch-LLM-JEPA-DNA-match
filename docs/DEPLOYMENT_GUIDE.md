# Deployment & Testing Guide (Local Hardware Setup)

This guide outlines how to deploy PathoMatch completely locally on consumer-grade hardware (Target: RTX 5050 8GB VRAM, 16GB RAM, 500GB SSD) for zero-cost AI execution.

## 1. Prerequisites

### Install Python & Node.js
- Ensure Python 3.10+ is installed.
- Ensure Node.js (v18+) is installed.

### Install Ollama (Crucial for $0 LLM)
Ollama is required to run the AI engine locally without cloud costs.
1. Download Ollama from `https://ollama.com/download`
2. Open a terminal and pull the Llama-3 model:
   ```bash
   ollama pull llama3
   ```
*(This 8B model uses ~4.5GB VRAM, easily fitting inside your RTX 5050).*

## 2. Backend Setup

1. **Navigate to the Backend Directory:**
   ```bash
   cd patho_match/backend
   ```
2. **Install Python Dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic
   pip install langchain-chroma langchain-huggingface langchain-community
   ```
   *(Note: Ensure you have `sentence-transformers` installed for the embeddings).*
3. **Populate the Vector Database:**
   Before running the API, you must generate the clinical guidelines database.
   ```bash
   cd ../scripts
   python setup_vector_db.py
   ```
4. **Start the FastAPI Server:**
   ```bash
   cd ../backend
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

## 3. Frontend Setup

1. **Navigate to the Frontend Directory:**
   ```bash
   cd patho_match/frontend
   ```
2. **Install Node Packages:**
   ```bash
   npm install
   ```
3. **Run the Vite Development Server:**
   ```bash
   npm run dev
   ```
   *The UI will be accessible at `http://localhost:5173`.*

## 4. End-to-End Testing
1. Open the UI in your browser.
2. Select **"Researcher Mode (Base)"** to protect your 16GB RAM.
3. Upload a sample `.fasta` file.
4. Select a species (e.g., Canine).
5. Click **Analyze Sequence**.
6. **Watch the Backend Console:** You will see the Math Engine process the chunks, followed by Ollama generating the clinical report locally.
7. The 3D Molstar viewer will render the molecule based on the results.
