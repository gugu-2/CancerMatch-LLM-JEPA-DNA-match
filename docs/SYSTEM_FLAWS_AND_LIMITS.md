# System Flaws and Architectural Limits

PathoMatch is designed for maximum theoretical accuracy. However, pushing algorithms to their limits introduces severe bottlenecks. This document serves as a brutally honest technical review of the software's flaws, weaknesses, and strengths.

## 1. Hardware Bottlenecks (The $O(mn)$ Problem)
*   **The Flaw:** The Smith-Waterman sequence alignment algorithm operates in $O(mn)$ time complexity. This means it creates a 2D matrix comparing every single DNA base of the query against every base of the target.
*   **The Consequence:** If a user uploads a massive 500GB Whole Genome Sequencing (WGS) file in **Enterprise Mode**, the matrix will instantly consume terabytes of RAM. If the server does not have 512GB+ of memory, the system will crash (Out Of Memory).
*   **The Mitigation:** We introduced **Researcher Mode**, which forcefully slices the DNA into tiny 2,000-base windows. While this saves RAM, it slightly degrades the ability to detect massive structural variations (like huge chromosomal inversions).

## 2. The Molecular Dynamics Physics Trap
*   **The Flaw:** Calculating true Antimicrobial Resistance (AMR) requires simulating water molecules surrounding the mutated protein using MM/PBSA thermodynamics.
*   **The Consequence:** This requires massive GPU clusters (NVIDIA A100s). In the Base tier, we bypass this by using rigid-body empirical docking (similar to AutoDock Vina). 
*   **The Mitigation Flaw:** Rigid-body docking assumes proteins are stiff like rocks. In reality, proteins flex and bend. By skipping the flexibility calculations to save VRAM, the Base Tier will occasionally miss resistance mutations that rely on "induced fit" conformational changes.

## 3. Evolutionary Blindspots (The Jukes-Cantor Limit)
*   **The Flaw:** The mathematical engine relies on statistical transition matrices (Jukes-Cantor) to correct for cross-species evolutionary time.
*   **The Consequence:** This math is calibrated for *natural* evolution. If a user uploads a **synthetically engineered pathogen** or a rapidly mutating synthetic virus, the evolutionary assumptions break down completely. The software will likely misclassify the divergence.

## 4. RAG Extrapolation Risks (Found In Translation)
*   **The Flaw:** When veterinary clinical guidelines are missing, the system's "FIT" protocol automatically extrapolates treatments from Human guidelines.
*   **The Consequence:** While the AI is instructed to adjust for species differences (e.g., Canine renal function), human and animal metabolisms are fundamentally different. Extrapolating a human chemotherapy dose to a dog carries an inherent, unquantifiable risk of toxicity that the mathematical engine cannot catch.

---

## The Strengths (Why this system still wins)
Despite these severe hardware and evolutionary constraints, PathoMatch remains vastly superior to generic black-box AI platforms for one reason: **Transparency.**

When the system predicts resistance, it doesn't just give a probability score. It provides the exact $\Delta \Delta G$ thermodynamic equation and renders a 3D structural model via Molstar so the clinician can literally *see* the physical clash preventing the drug from working. It fails loudly when out of memory rather than hallucinating quietly.
