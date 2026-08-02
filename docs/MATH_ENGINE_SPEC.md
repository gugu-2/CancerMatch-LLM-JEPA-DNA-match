# Mathematical Engine Specification (PathoMatch)

This document outlines the core algorithms used by PathoMatch to achieve 100% deterministic biological matching, bypassing the probabilistic nature of Large Language Models (LLMs).

## 1. Sequence Filtering (MinHash & Jaccard Similarity)
To prevent $O(mn)$ algorithms from crashing the system on massive whole-genome files, PathoMatch uses a $O(1)$ heuristic filter.

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

We apply the **MinHash** algorithm to approximate Jaccard similarity without storing all k-mers in RAM:
$$P(\min(h(A)) = \min(h(B))) = J(A, B)$$
*(Reference: Ondov et al., "Mash")*

## 2. FM-Index & Burrows-Wheeler Transform (BWT)
For exact read mapping, the system searches backward from the end of the query string using the LF-mapping equations:
$$low = C[c] + Occ(c, low - 1) + 1$$
$$high = C[c] + Occ(c, high)$$
Where $C[c]$ is the count of characters lexicographically smaller than base $c$.

## 3. Local Alignment (Smith-Waterman with Gotoh's Matrices)
The core matching engine uses dynamic programming to track exact insertion/deletion mutations via three recurrence matrices ($M$, $I_x$, $I_y$):

$$M(i, j) = \max \begin{cases} 0 \\ M(i-1, j-1) + s(x_i, y_j) \\ I_x(i-1, j-1) + s(x_i, y_j) \\ I_y(i-1, j-1) + s(x_i, y_j) \end{cases}$$

## 4. Cross-Species Correction (Jukes-Cantor)
When a veterinary pathogen is compared against a human database, raw divergence ($p$) is statistically corrected for evolutionary time:
$$d = -\frac{3}{4} \ln(1 - \frac{4}{3}p)$$

## 5. Antimicrobial Resistance Thermodynamics (MM/PBSA)
To prove that a mutation causes resistance, we calculate the change in Binding Free Energy ($\Delta \Delta G_{bind}$):
$$ \Delta G_{bind} = \Delta E_{MM} + \Delta G_{solv} - T\Delta S $$
If $\Delta \Delta G_{bind} > 2 \text{ kcal/mol}$, the drug is physically repelled by the mutated protein, and the system flags the pathogen as resistant.
