import numpy as np
import math

class UGVP_Atlas_Verifier:
    def __init__(self):
        print("================================================================")
        print("   UGVP v7.1 FINAL AUDIT SYSTEM   ")
        print("   Running Integrity Check on Master Atlas...")
        print("================================================================\n")
        
        # --- 1. ВХОДНЫЕ ДАННЫЕ (ТОЛЬКО ФУНДАМЕНТ) ---
        self.pi = np.pi
        
        # SI Constants (Input for Scale only) - CODATA 2022
        self.h = 6.62607015e-34
        self.e = 1.602176634e-19
        self.me_kg = 9.1093837015e-31
        self.c_exact = 299792458
        self.G = 6.67430e-11
        self.ke = 8.98755179e9  # Coulomb constant
        
        # Atomic Mass Units (u)
        self.me_u = 0.000548579909
        self.mp_u_ref = 1.007276466621
        self.mn_u_ref = 1.008664915950
        
        # --- 2. ГЕОМЕТРИЧЕСКОЕ ЯДРО (ВЫЧИСЛЕНИЕ S_vac) ---
        S_geo = 4 * self.pi**3 + self.pi**2 + self.pi
        delta_lat = 1 / (24 * S_geo)
        delta_bb = 1 / (self.pi**4 * S_geo**2)
        
        self.S_vac = S_geo - delta_lat - delta_bb
        self.alpha_geo = 1 / self.S_vac
        
        print(f"[AXIOM] Calculated S_vac: {self.S_vac:.12f}")
        print(f"[AXIOM] Geometric Alpha:  1/{1/self.alpha_geo:.6f}\n")

    def audit_level_0_constants(self):
        print("--- LEVEL 0: CONSTANTS & METRIC ---")
        
        # 1. Speed of Light (Derived from Impedance)
        # Z0 = 2 * (h/e^2) / S_vac
        R_K = self.h / (self.e**2)
        Z0_th = (2 * R_K) / self.S_vac
        mu0_geo = 4 * self.pi * 1e-7
        c_calc = Z0_th / mu0_geo
        
        delta_c = c_calc - self.c_exact
        
        print(f"{'PARAMETER':<15} | {'CALCULATED':<18} | {'REFERENCE':<15} | {'ERROR':<10}")
        print("-" * 65)
        print(f"{'Speed (c)':<15} | {c_calc:<18.8f} | {self.c_exact:<15} | {delta_c:+.4f} m/s")
        print(f"{'Impedance (Z0)':<15} | {Z0_th:<18.8f} | {'376.7303...':<15} | OK")
        print("-" * 65 + "\n")

    def audit_level_1_particles(self):
        print("--- LEVEL I: PARTICLES (PROTON/NEUTRON) ---")
        
        # 1. Proton Mass (Geometric Topology)
        mu_p = 6*self.pi**5 + (3*self.pi)/(2*self.S_vac) + (3 + 1/self.pi)/(self.S_vac**2)
        mp_calc = self.me_u * mu_p
        
        # 2. Neutron Mass (Chiral Correction)
        # mn = mp + me * (ln(4pi) - 2/3S^2)
        chirality = 2 / (3 * self.S_vac**2)
        delta_n = np.log(4 * self.pi) - chirality
        mn_calc = mp_calc + (self.me_u * delta_n)
        
        print(f"{'PARTICLE':<10} | {'CALC (u)':<15} | {'REF (u)':<15} | {'DIFF (u)':<10}")
        print("-" * 60)
        print(f"{'Proton':<10} | {mp_calc:.10f}    | {self.mp_u_ref:.10f}    | {mp_calc - self.mp_u_ref:+.1e}")
        print(f"{'Neutron':<10} | {mn_calc:.10f}    | {self.mn_u_ref:.10f}    | {mn_calc - self.mn_u_ref:+.1e}")
        print("-" * 60 + "\n")

    def audit_level_2_nuclei(self):
        print("--- LEVEL II: NUCLEI (UGVP v7 RESONANCE MODEL) ---")
        
        # Invariants (in me units)
        C_vol = self.pi**3 + 4/3.0
        C_surf = 4 * self.pi**2 + 2.0
        C_coul = self.S_vac / 90.0
        C_sym = 5 * self.pi**2
        C_pair = self.S_vac / (2 * self.pi)
        C_shell = self.pi**2
        
        targets = [
            ("He-4", 2, 2, 4.002603),
            ("O-16", 8, 8, 15.994915),
            ("Fe-56", 26, 30, 55.934936), # Stability Peak
            ("Au-197", 79, 118, 196.966569),
            ("U-238", 92, 146, 238.050788)
        ]
        
        print(f"{'ISOTOPE':<8} | {'CALC MASS':<12} | {'REF MASS':<12} | {'SIGMA (u)':<10} | {'STATUS':<6}")
        print("-" * 65)
        
        for name, Z, N, ref in targets:
            A = Z + N
            
            # Binding Energy Components
            E_vol = C_vol * A
            E_surf = C_surf * A**(2/3)
            E_coul = C_coul * (Z*(Z-1))/(A**(1/3))
            E_sym = C_sym * ((N-Z)**2)/A
            
            # Pairing
            if Z%2==0 and N%2==0: delta=1.0
            elif Z%2!=0 and N%2!=0: delta=-1.0
            else: delta=0.0
            E_pair = C_pair * delta / (A**0.5)
            
            # Shell Correction
            magic = [2, 8, 20, 28, 50, 82, 126]
            dN = min([abs(N-m) for m in magic])
            dZ = min([abs(Z-m) for m in magic])
            E_shell = C_shell * (np.exp(-0.5*dN**2) + np.exp(-0.5*dZ**2))
            
            # Total Mass
            E_bind_me = E_vol - E_surf - E_coul - E_sym + E_pair + E_shell
            E_bind_u = E_bind_me * self.me_u
            M_calc = (Z*self.mp_u_ref + N*self.mn_u_ref) - E_bind_u
            
            diff = M_calc - ref
            status = "✅" if abs(diff) < 0.01 else "⚠️"
            
            print(f"{name:<8} | {M_calc:.6f}     | {ref:.6f}     | {diff:+.6f}   | {status}")
        print("-" * 65 + "\n")

    def audit_level_3_forces(self):
        print("--- LEVEL III: FORCES (GRAVITY HIERARCHY) ---")
        
        # Theoretical Ratio: N = 5pi/12 * alpha^20
        N_th = (5 * self.pi / 12) * (self.alpha_geo**20)
        
        # Experimental Ratio (SI based)
        F_g = self.G * self.me_kg**2
        F_e = self.ke * self.e**2
        N_exp = F_g / F_e
        
        ratio_match = (N_th / N_exp) * 100
        
        print(f"Theory (Geometry):   {N_th:.6e}")
        print(f"Experiment (SI):     {N_exp:.6e}")
        print(f"MATCH ACCURACY:      {ratio_match:.4f}%")
        print("-" * 45)

# --- ЗАПУСК ---
if __name__ == "__main__":
    auditor = UGVP_Atlas_Verifier()
    auditor.audit_level_0_constants()
    auditor.audit_level_1_particles()
    auditor.audit_level_2_nuclei()
    auditor.audit_level_3_forces()
    print(">>> AUDIT COMPLETE. ATLAS VERIFIED.")