import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('__file__'), '..')))
from ai_engine.math.bio_algorithms import MinHashFilter, FMIndex
from ai_engine.math.sequence_aligner import SequenceAligner
from ai_engine.math.thermodynamics import ThermodynamicsCalculator
def main():
    print('--- Testing bio_algorithms ---')
    mh = MinHashFilter(num_hashes=100, k=3)
    s1 = mh.compute_sketch('ACGTACGT')
    s2 = mh.compute_sketch('ACGTTCGT')
    print(f'Jaccard Similarity: {mh.jaccard_similarity(s1, s2)}')
    fm = FMIndex('ACGTACGT')
    print(f'FMIndex Matches: {fm.lf_mapping_search('ACGT')}')
    print('\n--- Testing sequence_aligner ---')
    aligner = SequenceAligner(match_score=2, mismatch_penalty=-1, gap_open=-2, gap_extend=-1)
    print(f'SW Gotoh Score: {aligner.smith_waterman_gotoh('ACGTACGT', 'ACGTTCGT')}')
    print(f'Jukes-Cantor Distance (p=0.2): {aligner.jukes_cantor_distance(0.2)}')
    print('\n--- Testing thermodynamics ---')
    therm = ThermodynamicsCalculator()
    bind_energy = therm.calculate_binding_free_energy(E_vdw=-10, E_elec=-5, G_polar=12, SASA=150)
    print(f'Binding Free Energy: {bind_energy}')
    print(f'AMR Prediction: {therm.predict_amr(-8.0, -5.0)}')
if __name__ == '__main__':
    main()
