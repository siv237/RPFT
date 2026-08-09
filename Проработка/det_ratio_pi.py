import mpmath as mp
import numpy as np

mp.mp.dps = 100

import mpmath as mp

mp.mp.dps = 15 # Грубая точность для быстрого поиска

class SpectrumCache:
    def __init__(self, n_max):
        self.n_max = n_max
        # Спектры на S3 (R=1)
        self.s_lams = [mp.mpf(n*(n+2)) for n in range(n_max)]
        self.s_mults = [mp.mpf((n+1)**2) for n in range(n_max)]
        
        self.v_lams = [mp.mpf((n+1)**2) for n in range(1, n_max)]
        self.v_mults = [mp.mpf(2*n*(n+2)) for n in range(1, n_max)]

        self.d_lams = [mp.mpf((n+1.5)**2) for n in range(n_max)]
        self.d_mults = [mp.mpf(2*(n+1)*(n+2)) for n in range(n_max)]
        
        self.s_signs = [mp.mpf((-1)**n) for n in range(n_max)]
        self.v_signs = [mp.mpf((-1)**n) for n in range(1, n_max)]
        self.d_signs_A = [mp.mpf((-1)**n) for n in range(n_max)]
        self.d_signs_B = [mp.mpf((-1)**(n+1)) for n in range(n_max)]

cache = SpectrumCache(1000) # Уменьшено с 5000 до 1000

def total_twisted_trace(t, mode='MG'):
    s_coeffs = [s * m for s, m in zip(cache.s_signs, cache.s_mults)]
    tr_s = mp.fdot(s_coeffs, [mp.exp(-t * l) for l in cache.s_lams])
    
    v_coeffs = [s * m for s, m in zip(cache.v_signs, cache.v_mults)]
    tr_v = mp.fdot(v_coeffs, [mp.exp(-t * l) for l in cache.v_lams])
    
    mg_part = 0.5 * tr_v - 0.5 * tr_s
    
    if mode == 'MG': return mg_part
    if mode == 'Scalar_only': return -tr_s # Разность ln det для скаляров
    
    d_signs = cache.d_signs_A if 'DiracA' in mode else cache.d_signs_B
    d_coeffs = [s * m for s, m in zip(d_signs, cache.d_mults)]
    tr_d = mp.fdot(d_coeffs, [mp.exp(-t * l) for l in cache.d_lams])
    
    if 'only' in mode: return -tr_d
    return mg_part - tr_d

def calc_delta_gamma_top(mode='MG'):
    # Снижаем t_min для лучшего захвата высоких мод даже в грубом режиме
    integral = mp.quad(lambda t: total_twisted_trace(t, mode)/t, [1e-6, 20.0], maxdegree=3)
    return integral

print("--- FAST SEARCH: Delta Gamma_top ---")
modes = ['MG', 'Scalar_only', 'DiracA_only', 'DiracB_only', 'Dirac_Mixed']
for m in modes:
    if m == 'Dirac_Mixed':
        res = calc_delta_gamma_top('DiracB_only') - calc_delta_gamma_top('DiracA_only')
    else:
        res = calc_delta_gamma_top(m)
    diff = res - mp.pi
    print(f"{m:12s}: {mp.nstr(res, 8)} (diff to pi: {mp.nstr(diff, 4)})")

print("\n--- Additional Combinations ---")
res_s = calc_delta_gamma_top('Scalar_only')
res_mg = calc_delta_gamma_top('MG')
res_dm = calc_delta_gamma_top('DiracB_only') - calc_delta_gamma_top('DiracA_only')

print(f"(Scalar + Dirac_Mixed)/2: {mp.nstr((res_s + res_dm)/2, 8)} (diff: {mp.nstr((res_s + res_dm)/2 - mp.pi, 4)})")
print(f"(Dirac_Mixed - MG)/4:    {mp.nstr((res_dm - res_mg)/4, 8)} (diff: {mp.nstr((res_dm - res_mg)/4 - mp.pi, 4)})")
print(f"(MG + DiracB_only):      {mp.nstr(res_mg + calc_delta_gamma_top('DiracB_only'), 8)} (diff: {mp.nstr(res_mg + calc_delta_gamma_top('DiracB_only') - mp.pi, 4)})")

print(f"\nTarget pi: {mp.nstr(mp.pi, 8)}")
