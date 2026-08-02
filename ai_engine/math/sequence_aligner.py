import math

class SequenceAligner:
    def __init__(self, match_score=2, mismatch_penalty=-1, gap_open=-2, gap_extend=-1):
        self.match = match_score
        self.mismatch = mismatch_penalty
        self.gap_open = gap_open
        self.gap_extend = gap_extend

    def jukes_cantor_distance(self, p_divergence):
        """
        Applies the Jukes-Cantor statistical correction for multiple substitutions over evolutionary time.
        d = -3/4 * ln(1 - 4/3 * p)
        """
        if p_divergence >= 0.75:
            return float('inf') # Sequences are completely saturated (random noise)
        
        try:
            d = -0.75 * math.log(1 - (4.0 / 3.0) * p_divergence)
            return d
        except ValueError:
            return float('inf')

    def smith_waterman_gotoh(self, seq1, seq2):
        """
        Smith-Waterman optimal local alignment with Affine Gap Penalties (Gotoh's Algorithm).
        O(mn) Time Complexity using 3 matrices (M, Ix, Iy).
        """
        m, n = len(seq1), len(seq2)
        
        # Initialize Matrices
        # M: Match/Mismatch
        # Ix: Gap in seq2 (Insertion in seq1)
        # Iy: Gap in seq1 (Insertion in seq2)
        M = [[0] * (n + 1) for _ in range(m + 1)]
        Ix = [[0] * (n + 1) for _ in range(m + 1)]
        Iy = [[0] * (n + 1) for _ in range(m + 1)]
        
        max_score = 0
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Score function
                score = self.match if seq1[i-1] == seq2[j-1] else self.mismatch
                
                # Update Ix (Gap in Y)
                Ix[i][j] = max(
                    M[i-1][j] + self.gap_open,
                    Ix[i-1][j] + self.gap_extend
                )
                
                # Update Iy (Gap in X)
                Iy[i][j] = max(
                    M[i][j-1] + self.gap_open,
                    Iy[i][j-1] + self.gap_extend
                )
                
                # Update M (Match/Mismatch)
                M[i][j] = max(
                    0, # Local alignment reset
                    M[i-1][j-1] + score,
                    Ix[i-1][j-1] + score,
                    Iy[i-1][j-1] + score
                )
                
                if M[i][j] > max_score:
                    max_score = M[i][j]
                    
        return max_score

    def chunked_alignment(self, seq1, seq2, window_size=2000, overlap=200):
        """
        Base Tier Fallback (16GB RAM limit).
        Slices the massive sequence into overlapping windows to prevent OOM errors during O(mn) dynamic programming.
        """
        total_score = 0
        
        # Iterate over seq1 in chunks, aligning against the smaller seq2 (usually a read or marker)
        for i in range(0, len(seq1), window_size - overlap):
            chunk = seq1[i:i + window_size]
            
            # Run the standard Smith-Waterman Gotoh algorithm on the small chunk
            chunk_score = self.smith_waterman_gotoh(chunk, seq2)
            
            # Aggregate the highest scoring local alignment from the chunks
            if chunk_score > total_score:
                total_score = chunk_score
                
        return total_score
