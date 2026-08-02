# 🚀 PathoMatch: Master Deployment & Testing Guide (For New Computers)

This is the comprehensive, step-by-step digital runbook for migrating, deploying, and testing the PathoMatch platform on a brand-new computer or laptop.

Because PathoMatch is an **Offline-First AI Platform**, you will need to install the software that actually runs the AI locally. Follow these instructions exactly.

---

## 💻 1. Hardware Requirements
Before you begin, ensure your new computer meets the requirements to run local AI models:
- **Processor:** Modern multi-core CPU (Intel i5/i7 10th Gen+, AMD Ryzen, or Apple Silicon M1/M2/M3).
- **RAM:** Minimum **16GB** (32GB strongly recommended for running the 7B parameter LLMs smoothly).
- **Disk Space:** At least **30GB** of free SSD space (for Docker images, genomic databases, and LLM weights).
- **GPU (Optional but highly recommended):** NVIDIA GPU with CUDA support, or Apple Silicon unified memory.

---

## 🛠️ 2. Prerequisite Software Installation

You must install this foundational software on the new computer.

### A. Install Docker Desktop (Crucial)
PathoMatch is fully containerized. Docker manages the database, backend, and frontend environments.
1. Go to [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Download and install the version for your OS.
3. **Windows Users:** Ensure you enable **WSL2** (Windows Subsystem for Linux) during the Docker installation process.
4. **Verification:** Open Docker Desktop and ensure the engine is "Running" (green icon in the bottom left).

### B. Install Python & Node.js (For Native Testing)
If you want to run the code natively without Docker:
1. **Python 3.10+**: Download from [python.org](https://www.python.org/downloads/). (Check the box to "Add Python to PATH" during installation).
2. **Node.js (v18+)**: Download from [nodejs.org](https://nodejs.org/).

### C. Install Ollama (The AI Runner)
Ollama is the engine that will run our Large Language Model (Mistral) locally on your hardware.
1. Go to [https://ollama.com/download](https://ollama.com/download)
2. Install it for your OS.
3. Open a terminal (Command Prompt or PowerShell) and run:
   ```bash
   ollama pull mistral
   ```
   *Note: This will download the ~4GB Mistral AI model. This may take a while depending on your internet connection.*

---

## 📦 3. Codebase Migration

1. On your current computer, compress the entire `patho_match` directory into a `.zip` file.
2. Transfer the `.zip` file to your new computer via a USB flash drive, external hard drive, or a secure file transfer service.
3. Unzip the folder in a dedicated workspace (e.g., `Documents/patho_match`).

---

## 🧠 4. Build the AI Vector Database (ChromaDB)

PathoMatch uses a local vector database to store the clinical guidelines. This database must be generated on the new machine.

1. Open a terminal and navigate to your `patho_match` folder.
2. Install the backend Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```
3. Run the Vector Database Setup Script:
   ```bash
   python scripts/setup_vector_db.py
   ```
4. **Expected Output:** You should see logs indicating that the `all-MiniLM-L6-v2` embedding model is downloading (~90MB), followed by `Vector store successfully built and persisted!`.

---

## 🚀 5. Launch the Platform (Docker Compose)

Now that the AI models are downloaded and the Vector DB is built, it's time to boot the software!

1. Ensure **Docker Desktop** is open and running in the background.
2. Open a terminal in the root `patho_match` directory.
3. Run the orchestration command:
   ```bash
   docker-compose up --build
   ```
4. Docker will now download the PostgreSQL, Redis, Nginx, and Python images, compile the React frontend, and link them all into an isolated network.
5. **Success:** Once you see logs indicating `Uvicorn running on http://0.0.0.0:8000` and the frontend server starting, the platform is live!

---

## 🩺 6. How to Test the Software (The Walkthrough)

1. Open your web browser (Chrome/Edge/Safari) and go to:
   👉 **`http://localhost:3000`**
2. You will see the premium "Dark Mode Genomics" PathoMatch Dashboard.
3. **The Test:**
   - Under *Sequence File*, select any mock `.fasta` or `.txt` file on your computer.
   - Under *Patient Species*, select **Canine (Canis lupus)**.
   - Add a note: "Suspected septic peritonitis".
   - Click **Analyze Sequence**.
4. **Verification:** 
   - A loading spinner will appear.
   - The UI will slide in a beautifully formatted **AI Clinical Report**.
   - Read the *Sources Retrieved*. You should **ONLY** see guidelines related to dogs (Canine). You should see zero mention of human or bovine guidelines.
   - This proves that the local LangChain AI, the ChromaDB metadata filter, and the React UI are all communicating flawlessly in your offline, secure environment!

---

## ⚠️ 7. Troubleshooting FAQ

- **Error: "Failed to connect to Docker daemon"**
  *Fix:* Docker Desktop is not running. Open the Docker Desktop app from your start menu.
  
- **Error: "ModuleNotFoundError: No module named 'langchain'" when running setup_vector_db.py**
  *Fix:* You forgot to install the python requirements. Run `pip install -r backend/requirements.txt`.

- **The UI is blank or not connecting on port 3000**
  *Fix:* Sometimes port 3000 is occupied by another app. If `docker-compose` fails, you can run the UI natively:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  Then click the Localhost link provided in the terminal (usually `http://localhost:5173`).
