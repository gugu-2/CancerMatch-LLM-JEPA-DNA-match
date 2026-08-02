class ThermodynamicsCalculator:
    def __init__(self, temperature_k=298.15):
        self.T = temperature_k # Room temperature (~25C)

    def calculate_binding_free_energy(self, E_vdw, E_elec, G_polar, SASA, gamma=0.00542, b=0.92, delta_S=0):
        """
        Calculates the MM/PBSA Binding Free Energy (Delta G_bind).
        Delta G_bind = Delta E_MM + Delta G_solv - T*Delta S
        Where:
        Delta E_MM = Delta E_vdw + Delta E_elec
        Delta G_solv = Delta G_polar + Delta G_nonpolar
        Delta G_nonpolar = gamma * SASA + b
        """
        # Gas-phase molecular mechanics energy
        E_MM = E_vdw + E_elec
        
        # Solvation free energy
        G_nonpolar = (gamma * SASA) + b
        G_solv = G_polar + G_nonpolar
        
        # Entropy (usually calculated via Normal Mode Analysis, set to 0 for simplified mock)
        T_delta_S = self.T * delta_S
        
        # Total Binding Free Energy (kcal/mol)
        G_bind = E_MM + G_solv - T_delta_S
        return G_bind

    def predict_amr(self, G_bind_wt, G_bind_mutant, resistance_threshold=2.0):
        """
        Predicts Antimicrobial Resistance (AMR) based on the difference in binding affinity.
        Delta Delta G_bind = G_bind(Mutant) - G_bind(WT)
        If the value is highly positive, the mutation destabilized the drug binding -> Resistant.
        """
        delta_delta_G = G_bind_mutant - G_bind_wt
        
        is_resistant = delta_delta_G > resistance_threshold
        
        return {
            "delta_delta_G_kcal_mol": round(delta_delta_G, 3),
            "resistance_predicted": is_resistant,
            "mechanistic_insight": "Drug binding severely destabilized." if is_resistant else "Drug binding maintained."
        }

    def lightweight_empirical_scoring(self, steric_clashes, h_bond_loss, rigid_threshold=1.5):
        """
        Base Tier Fallback (8GB VRAM limit).
        Skips expensive water solvent and entropy MD simulations.
        Uses a highly simplified, rigid-body empirical scoring function estimating Delta Delta G 
        purely based on physical geometry clashes and lost hydrogen bonds.
        """
        # Empirical penalty calculation (mocked weights similar to AutoDock Vina)
        clash_penalty = steric_clashes * 0.8  # Strong penalty for physical overlapping atoms
        hbond_penalty = h_bond_loss * 0.5     # Penalty for losing critical binding bonds
        
        estimated_delta_delta_g = clash_penalty + hbond_penalty
        
        is_resistant = estimated_delta_delta_g > rigid_threshold
        
        return {
            "delta_delta_G_kcal_mol": round(estimated_delta_delta_g, 3),
            "resistance_predicted": is_resistant,
            "mechanistic_insight": "Empirical model predicts structural clash/bond loss." if is_resistant else "Empirical model predicts drug fits."
        }
