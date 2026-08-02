# JEPA (Joint-Embedding Predictive Architecture) R&D Lab

This folder contains the raw PyTorch blueprints for `BioJEPA`, a self-supervised biological foundation model based on Yann LeCun's (Meta) architecture.

## Why is this not in the main application pipeline?
Training a JEPA model on the global genomic database (NCBI/GenBank) requires immense computational resources (hundreds of GPUs running for months, costing upwards of $1M+). 

Because the live PathoMatch application requires 100% deterministic accuracy for clinical use *today*, the active pipeline uses a **Hybrid Mathematical Architecture** (Smith-Waterman, MinHash, MM/PBSA).

## What is this folder for?
This codebase exists as an R&D asset for the future. When funding allows for the compute required to train a biological foundational model, this `bio_jepa_architecture.py` script serves as the structural scaffold. 

Unlike an LLM which tries to guess the exact next DNA letter (leading to hallucinations), this JEPA model is designed to predict the *latent semantic meaning* of mutated regions, making it theoretically superior for capturing evolutionary biology without syntax errors.
