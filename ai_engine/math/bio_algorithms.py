import hashlib

class MinHashFilter:
    def __init__(self, num_hashes=100, k=21):
        self.num_hashes = num_hashes
        self.k = k

    def get_kmers(self, sequence):
        """Extracts all k-mers of length k from a sequence."""
        return set([sequence[i:i+self.k] for i in range(len(sequence) - self.k + 1)])

    def _hash(self, kmer, seed):
        """Simple hash function with a seed."""
        return int(hashlib.md5((kmer + str(seed)).encode('utf-8')).hexdigest(), 16)

    def compute_sketch(self, sequence):
        """Computes the MinHash sketch for a sequence."""
        kmers = self.get_kmers(sequence)
        sketch = []
        for i in range(self.num_hashes):
            min_hash = float('inf')
            for kmer in kmers:
                h = self._hash(kmer, i)
                if h < min_hash:
                    min_hash = h
            sketch.append(min_hash)
        return sketch

    def jaccard_similarity(self, sketch1, sketch2):
        """Estimates Jaccard similarity based on MinHash sketch collisions."""
        matches = sum(1 for h1, h2 in zip(sketch1, sketch2) if h1 == h2)
        return matches / self.num_hashes


class FMIndex:
    def __init__(self, sequence):
        self.sequence = sequence + '$'
        self.bwt = self._build_bwt()
        self.c_array = self._build_c_array()
        self.occ_table = self._build_occ_table()

    def _build_bwt(self):
        """Constructs the Burrows-Wheeler Transform."""
        rotations = sorted([self.sequence[i:] + self.sequence[:i] for i in range(len(self.sequence))])
        return "".join([rot[-1] for rot in rotations])

    def _build_c_array(self):
        """C[c] array: Count of characters lexicographically smaller than c."""
        c_array = {}
        counts = {c: self.sequence.count(c) for c in set(self.sequence)}
        total = 0
        for c in sorted(counts.keys()):
            c_array[c] = total
            total += counts[c]
        return c_array

    def _build_occ_table(self):
        """Occ(c, i) table: Count of character c in BWT prefix up to index i."""
        occ_table = {c: [0] * len(self.bwt) for c in set(self.bwt)}
        for i, char in enumerate(self.bwt):
            for c in occ_table:
                occ_table[c][i] = occ_table[c][i-1] if i > 0 else 0
            occ_table[char][i] += 1
        return occ_table

    def lf_mapping_search(self, pattern):
        """Backward search algorithm for exact string matching."""
        low = 0
        high = len(self.bwt) - 1
        
        for i in range(len(pattern) - 1, -1, -1):
            c = pattern[i]
            if c not in self.c_array:
                return 0 # Character doesn't exist in genome
            
            low = self.c_array[c] + (self.occ_table[c][low - 1] if low > 0 else 0)
            high = self.c_array[c] + self.occ_table[c][high] - 1
            
            if low > high:
                return 0 # No match found
                
        return high - low + 1 # Number of exact matches
