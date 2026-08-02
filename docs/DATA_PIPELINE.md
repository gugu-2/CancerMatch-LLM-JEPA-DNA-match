# The Data Pipeline (From FASTA to 3D Molstar)

This document explains the exact lifecycle of a biological sample as it moves through the PathoMatch architecture.

## Step 1: Ingestion
A researcher uploads a `.FASTA` or `.FASTQ` genetic file via the React UI, alongside Patient EHR metadata (Species, Allergies, Renal Function) and a Hardware Tier selection (Base vs Premium).

## Step 2: Biological Engine (Math Layer)
1.  **Filtering:** The backend converts the DNA into k-mers and creates a MinHash sketch. It compares this sketch against known pathogen databases in $O(1)$ time to quickly eliminate 99% of non-matching diseases.
2.  **Alignment:** The remaining sequences are processed through the `sequence_aligner.py`. If in **Premium Mode**, it builds the massive $O(mn)$ Smith-Waterman matrices. If in **Base Mode**, it slices the DNA into chunks. It extracts the exact mutation (e.g., A234G).

## Step 3: Thermodynamics Layer
The mutation is mapped to a 3D protein structure.
1.  **Binding Calculation:** `thermodynamics.py` calculates the Binding Free Energy ($\Delta G_{bind}$) of standard antibiotics against this new mutated structure.
2.  **Resistance Flag:** If the mutation physically blocks the antibiotic, it is mathematically flagged as Resistant.

## Step 4: NLP Translation Layer (LLM)
The backend compiles a raw JSON packet containing the exact mutations and resistance flags.
1.  **RAG Retrieval:** The system queries ChromaDB for the official clinical guidelines for the specific species (or falls back to Human via FIT).
2.  **Prompt Injection:** The mathematical facts and the retrieved guidelines are injected into the LLM prompt, alongside the Patient's EHR constraints (e.g., "Do not prescribe Penicillin due to Allergy").
3.  **Audit:** The generated response is scanned by the `SafetyAuditor` to ensure the LLM didn't invent a fake drug or dosage.

## Step 5: 3D Visualization (UI Render)
The backend sends the final LLM report back to the React frontend, alongside the Protein Data Bank (PDB) ID of the mutated target.
1.  The UI renders the text report.
2.  The UI injects the PDB ID into the `<pdbe-molstar>` Web Component, which reaches out to the European Bioinformatics Institute, downloads the 3D atomic coordinates, and renders the interactive molecule in the dashboard.
