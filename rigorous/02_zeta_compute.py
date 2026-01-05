#!/usr/bin/env python3
"""
Воспроизводимая проверка спектральных/геометрических сумм на L(2,1).
Цель: зафиксировать численную проверку формулы для α⁻¹ и места, где требуется строгая нормировка (например, κ_Cas).

Навигация:
  ← 01_spectral.md | 03_casimir_derivation.md →
  Главная: 00_main.md
"""

from mpmath import mp, nsum, diff, log, pi, sqrt, inf, exp, gamma as mpgamma
import numpy as np

mp.dps = 80  # 80 знаков точности

print("="*70)
print("ВОСПРОИЗВОДИМАЯ ПРОВЕРКА: спектральные/геометрические суммы на L(2,1)")
print("="*70)

# =============================================================================
# §1. ГЕОМЕТРИЧЕСКИЕ ОБЪЁМЫ (точные значения)
# =============================================================================

print("\n§1. ГЕОМЕТРИЧЕСКИЕ ОБЪЁМЫ")
print("-"*40)

Vol_S3 = 2 * pi**2          # Объём S³ радиуса R=1
Vol_RP3 = pi**2             # Объём RP³ = S³/Z₂
Len_S1 = 2 * pi             # Длина S¹
Sys_RP3 = pi                # Систола RP³

Vol_S3_S1 = Vol_S3 * Len_S1  # = 4π³

print(f"Vol(S³)       = 2π²   = {float(Vol_S3):.10f}")
print(f"Vol(RP³)      = π²    = {float(Vol_RP3):.10f}")
print(f"Length(S¹)    = 2π    = {float(Len_S1):.10f}")
print(f"Vol(S³×S¹)    = 4π³   = {float(Vol_S3_S1):.10f}")
print(f"Systole(RP³)  = π     = {float(Sys_RP3):.10f}")

# Геометрическое ядро
S_geo = Vol_S3_S1 + Vol_RP3 + Sys_RP3
print(f"\nS_geo = 4π³ + π² + π = {float(S_geo):.12f}")

# =============================================================================
# §2. ДЗЕТА-ФУНКЦИИ НА L(2,1)
# =============================================================================

print("\n§2. ДЗЕТА-ФУНКЦИИ ЛАПЛАСИАНОВ")
print("-"*40)

def zeta_scalar_L21(s, N_max=None):
    """
    ζ_scalar(s) на L(2,1) для скалярного лапласиана.
    λ_n = n(n+2), d_n = (n+1)² для чётных n.
    """
    s = mp.mpf(s)
    def term(k):
        n = 2*k  # только чётные n
        d_n = (n + 1)**2
        lam_n = n * (n + 2)
        if lam_n == 0:
            return mp.mpf(0)
        return d_n / lam_n**s
    
    if N_max:
        return sum(term(k) for k in range(1, N_max+1))
    return nsum(term, [1, inf])

def zeta_vector_L21(s, N_max=None):
    """
    ζ_vector(s) на L(2,1) для коэкзактных 1-форм.
    λ_n = (n+1)², d_n = 2n(n+2) для чётных n.
    """
    s = mp.mpf(s)
    def term(k):
        n = 2*k  # только чётные n
        d_n = 2 * n * (n + 2)
        lam_n = (n + 1)**2
        if lam_n == 0:
            return mp.mpf(0)
        return d_n / lam_n**s
    
    if N_max:
        return sum(term(k) for k in range(1, N_max+1))
    return nsum(term, [1, inf])

def zeta_dirac_L21(s, N_max=None):
    """
    ζ_Dirac(s) на L(2,1).
    λ_n = (n+3/2)², d_n = 2(n+1)(n+2) для нечётных n.
    """
    s = mp.mpf(s)
    def term(k):
        n = 2*k + 1  # только нечётные n
        d_n = 2 * (n + 1) * (n + 2)
        lam_n = (n + mp.mpf('1.5'))**2
        return d_n / lam_n**s
    
    if N_max:
        return sum(term(k) for k in range(0, N_max))
    return nsum(term, [0, inf])

# Проверка при s=2 (должно сходиться)
print(f"ζ_scalar(2) = {float(zeta_scalar_L21(2)):.10f}")
print(f"ζ_vector(2) = {float(zeta_vector_L21(2)):.10f}")
print(f"ζ_Dirac(2)  = {float(zeta_dirac_L21(2)):.10f}")

def zeta_prime_scalar_L21_twisted_at_zero(N_max=50000):
    total = mp.mpf(0)
    H2 = mp.mpf(0)
    H4 = mp.mpf(0)
    H6 = mp.mpf(0)
    H8 = mp.mpf(0)
    for m in range(1, N_max + 1):
        mm = mp.mpf(m)
        inv2 = 1 / (mm**2)
        H2 += inv2
        H4 += inv2**2
        H6 += inv2**3
        H8 += inv2**4
        total += -4 * mm**2 * log(1 - 1 / (4 * mm**2)) - 1
    tail = (
        (1 / (2 * 4)) * (mp.zeta(2) - H2)
        + (1 / (3 * 4**2)) * (mp.zeta(4) - H4)
        + (1 / (4 * 4**3)) * (mp.zeta(6) - H6)
        + (1 / (5 * 4**4)) * (mp.zeta(8) - H8)
    )
    A_prime = -2 * mp.zeta(3) / (pi**2)
    B_prime = mp.zeta(0)
    return total + tail + A_prime + B_prime

print("\n§2b. Twisted (acyclic) сектор для скаляра на RP³: проверка Nash–O’Connor")
print("-"*40)
zeta_prime_twisted = zeta_prime_scalar_L21_twisted_at_zero(50000)
ln_det_twisted = -zeta_prime_twisted
tau_pred = (3 / (pi**2)) * mp.zeta(3) - 2 * log(2)
ln_det_pred = -tau_pred / 2
print(f"ζ'_scalar_twisted(0) = {float(zeta_prime_twisted):.10f}")
print(f"ln Det_scalar_twisted = {-float(zeta_prime_twisted):.10f}")
print(f"ln Det_pred (Nash–O’Connor) = {float(ln_det_pred):.10f}")
print(f"Δ = {float(ln_det_twisted - ln_det_pred):.3e}")

print("\n§2c. Скалярный det′ на S³ и восстановление untwisted сектора на RP³")
print("-"*40)
ln_det_scalar_S3 = log(pi) + mp.zeta(3) / (2 * pi**2)
ln_det_scalar_RP3_untwisted = ln_det_scalar_S3 - ln_det_twisted
print(f"ln Det'_scalar(S³) (candidate) = {float(ln_det_scalar_S3):.10f}")
print(f"ln Det'_scalar(RP³, untwisted) = {float(ln_det_scalar_RP3_untwisted):.10f}")
candidate = log(pi / 2) + 2 * mp.zeta(3) / (pi**2)
print(f"Closed form candidate: ln(π/2) + 2·ζ(3)/π² = {float(candidate):.10f}")
print(f"Δ = {float(ln_det_scalar_RP3_untwisted - candidate):.3e}")

print("\n§2d. Проверка det′ скаляра на S³ без внешних формул")
print("-"*40)
def ln_det_scalar_S3_from_convergent_sum(N_max=200000):
    total = mp.mpf(0)
    H2 = mp.mpf(0)
    H4 = mp.mpf(0)
    H6 = mp.mpf(0)
    H8 = mp.mpf(0)
    for m in range(2, N_max + 1):
        mm = mp.mpf(m)
        inv2 = 1 / (mm**2)
        H2 += inv2
        H4 += inv2**2
        H6 += inv2**3
        H8 += inv2**4
        total += mm**2 * log(1 - inv2) + 1
    tail = (
        -(1 / 2) * (mp.zeta(2) - 1 - H2)
        -(1 / 3) * (mp.zeta(4) - 1 - H4)
        -(1 / 4) * (mp.zeta(6) - 1 - H6)
        -(1 / 5) * (mp.zeta(8) - 1 - H8)
    )
    return mp.zeta(3) / (2 * pi**2) + total + tail - mp.zeta(0) + 1

ln_det_S3_num = ln_det_scalar_S3_from_convergent_sum(200000)
print(f"ln Det'_scalar(S³) (num) = {float(ln_det_S3_num):.10f}")
print(f"ln Det'_scalar(S³) (candidate) = {float(ln_det_scalar_S3):.10f}")
print(f"Δ = {float(ln_det_S3_num - ln_det_scalar_S3):.3e}")

print("\n§2e. Коэкзактные 1-формы: ζ'(0) и ln det (аналитически)")
print("-"*40)
zeta_prime_vector_S3 = -(mp.zeta(3) / (pi**2)) + 2 * log(2 * pi)
ln_det_vector_S3 = -zeta_prime_vector_S3
print(f"ζ'_vector(S³, coexact)(0) = {float(zeta_prime_vector_S3):.10f}")
print(f"ln Det_vector(S³, coexact) = {float(ln_det_vector_S3):.10f}")

zeta_prime_vector_RP3_untwisted = (3 * mp.zeta(3) / (pi**2)) + 2 * log(2)
ln_det_vector_RP3_untwisted = -zeta_prime_vector_RP3_untwisted
print(f"ζ'_vector(RP³, untwisted, coexact)(0) = {float(zeta_prime_vector_RP3_untwisted):.10f}")
print(f"ln Det_vector(RP³, untwisted, coexact) = {float(ln_det_vector_RP3_untwisted):.10f}")

zeta_prime_vector_RP3_twisted = (-4 * mp.zeta(3) / (pi**2)) + 2 * log(pi)
ln_det_vector_RP3_twisted = -zeta_prime_vector_RP3_twisted
print(f"ζ'_vector(RP³, twisted, coexact)(0) = {float(zeta_prime_vector_RP3_twisted):.10f}")
print(f"ln Det_vector(RP³, twisted, coexact) = {float(ln_det_vector_RP3_twisted):.10f}")

print(f"Check S³ = twisted + untwisted: Δ = {float((ln_det_vector_RP3_twisted + ln_det_vector_RP3_untwisted) - ln_det_vector_S3):.3e}")

# =============================================================================
# §3. ПРОИЗВОДНЫЕ В НУЛЕ (регуляризованные)
# =============================================================================

print("\n§3. ζ'(0) — РЕГУЛЯРИЗОВАННЫЕ ДЕТЕРМИНАНТЫ")
print("-"*40)

def zeta_prime_at_zero(zeta_func, name):
    """Вычисление ζ'(0) через численное дифференцирование."""
    try:
        result = diff(zeta_func, 0)
        print(f"ζ'_{name}(0) = {float(result):.10f}")
        return result
    except Exception as e:
        print(f"ζ'_{name}(0): ошибка ({e})")
        return None

# Эти суммы расходятся при s→0, нужна регуляризация
print("ВНИМАНИЕ: Прямые суммы расходятся при s→0.")
print("Требуется heat kernel вычитание (см. §4).")

# =============================================================================
# §4. HEAT KERNEL ВЫЧИТАНИЕ
# =============================================================================

print("\n§4. МЕТОД HEAT KERNEL")
print("-"*40)

def heat_trace_scalar_L21(t, N_max=100):
    """
    Tr(exp(-t·Δ)) для скаляров на L(2,1).
    """
    t = mp.mpf(t)
    total = mp.mpf(0)
    for k in range(1, N_max+1):
        n = 2*k
        d_n = (n + 1)**2
        lam_n = n * (n + 2)
        total += d_n * exp(-t * lam_n)
    return total

# Weyl асимптотика: Tr(e^{-tΔ}) ~ Vol/(4πt)^{3/2} при t→0
print("Weyl асимптотика для L(2,1):")
print(f"  a_0 = Vol(L(2,1))/(4π)^(3/2) = π²/(4π)^(3/2) = {float(Vol_RP3 / (4*pi)**1.5):.10f}")

# Малое t: проверка
t_small = mp.mpf('0.01')
heat_val = heat_trace_scalar_L21(t_small, N_max=500)
weyl_approx = Vol_RP3 / (4 * pi * t_small)**1.5
print(f"\nПри t={float(t_small)}:")
print(f"  Tr(e^{{-tΔ}})  = {float(heat_val):.6f}")
print(f"  Weyl approx   = {float(weyl_approx):.6f}")
print(f"  Ratio         = {float(heat_val/weyl_approx):.6f}")

print("\n§4b. κ_Cas как 1D остаток на S¹ (Abel/heat-kernel)")
print("-"*40)

def kappa_cas_half_from_abel(t):
    t = mp.mpf(t)
    q = exp(-t)
    S = q / (1 - q)**2
    return -(S - 1 / t**2) / 2

_t_kappa = mp.mpf('0.005')
kappa_Cas_num = kappa_cas_half_from_abel(_t_kappa)
kappa_Cas_exact = -mp.zeta(-1) / 2
print(f"t = {_t_kappa}")
print(f"κ_Cas(num)   = {float(kappa_Cas_num):.15f}")
print(f"κ_Cas(exact) = {float(kappa_Cas_exact):.15f}   (= 1/24)")
print(f"Δ = {float(kappa_Cas_num - kappa_Cas_exact):+.3e}")

print("\n§4c. Прототип KK: Casimir-константа калибровочного сектора на RP³×S¹")
print("-"*40)

def casimir_energy_S1_massive(a, L=2*pi, M_max=50, antiperiodic=False):
    a = mp.mpf(a)
    L = mp.mpf(L)
    if a == 0:
        return -pi / (6 * L)
    total = mp.mpf(0)
    for m in range(1, M_max + 1):
        sgn = -1 if (antiperiodic and (m % 2 == 1)) else 1
        total += sgn * mp.besselk(1, L * a * m) / m
    return -(a / pi) * total

def kappa_cas_gauge_KK_RP3_S1(k_max=25, M_max=50, L=2*pi, include_scalar_lambda0_level=True):
    L = mp.mpf(L)
    E_scalar = mp.mpf(0)
    if include_scalar_lambda0_level:
        E_scalar += casimir_energy_S1_massive(mp.mpf(0), L=L, M_max=M_max)
    for k in range(1, k_max + 1):
        n = 2 * k
        d = (n + 1)**2
        a = sqrt(n * (n + 2))
        E_scalar += d * casimir_energy_S1_massive(a, L=L, M_max=M_max)

    E_vector = mp.mpf(0)
    for k in range(1, k_max + 1):
        n = 2 * k
        d = 2 * n * (n + 2)
        a = n + 1
        E_vector += d * casimir_energy_S1_massive(a, L=L, M_max=M_max)

    return mp.mpf('0.5') * (E_vector - E_scalar)

def kappa_cas_gauge_KK_RP3_S1_components(k_max=25, M_max=50, L=2*pi):
    L = mp.mpf(L)
    E_scalar_lambda0 = casimir_energy_S1_massive(mp.mpf(0), L=L, M_max=M_max)
    E_scalar_massive = mp.mpf(0)
    for k in range(1, k_max + 1):
        n = 2 * k
        d = (n + 1)**2
        a = sqrt(n * (n + 2))
        E_scalar_massive += d * casimir_energy_S1_massive(a, L=L, M_max=M_max)

    E_vector = mp.mpf(0)
    for k in range(1, k_max + 1):
        n = 2 * k
        d = 2 * n * (n + 2)
        a = n + 1
        E_vector += d * casimir_energy_S1_massive(a, L=L, M_max=M_max)

    kappa_from_lambda0_level = -mp.mpf('0.5') * E_scalar_lambda0
    kappa_massive_residual = mp.mpf('0.5') * (E_vector - E_scalar_massive)
    return E_scalar_lambda0, E_scalar_massive, E_vector, kappa_from_lambda0_level, kappa_massive_residual

target = mp.mpf(1) / 24
for k_max in [5, 10, 20, 30]:
    kappa_kk = kappa_cas_gauge_KK_RP3_S1(k_max=k_max, M_max=50, L=2*pi, include_scalar_lambda0_level=True)
    print(f"k_max={k_max:>2}: κ_Cas(gauge, KK) = {float(kappa_kk):.15f}, Δ = {float(kappa_kk - target):+.3e}")

kappa_kk_nozero = kappa_cas_gauge_KK_RP3_S1(k_max=30, M_max=50, L=2*pi, include_scalar_lambda0_level=False)
print(f"Без уровня λ_RP³=0 (убираем весь KK-ряд константы на RP³): κ_Cas(gauge, KK) = {float(kappa_kk_nozero):.15f}")
print(f"Сравнение с Abel κ_Cas(num): κ_KK - κ_Abel = {float((kappa_cas_gauge_KK_RP3_S1(30, 50) - kappa_Cas_num)):+.3e}")

E0, E_scal_mass, E_vec, k0, kmass = kappa_cas_gauge_KK_RP3_S1_components(k_max=30, M_max=50, L=2*pi)
print("Разложение κ_Cas(gauge, KK) = κ(λ_RP³=0 уровень) + κ(остаток массивных уровней):")
print(f"  E_scalar(λ_RP³=0) = {float(E0):+.15f}  -> κ0 = {-float(E0)/2:.15f}")
print(f"  κ_massive_residual = {float(kmass):+.15e}")
print(f"  κ_total = {float(k0 + kmass):.15f}")

def dirac_casimir_like_KK_RP3_S1(k_max=12, M_max=50, L=2*pi, antiperiodic=False):
    L = mp.mpf(L)
    E_dirac = mp.mpf(0)
    for k in range(0, k_max):
        n = 2 * k + 1
        d = 2 * (n + 1) * (n + 2)
        a = n + mp.mpf('1.5')
        E_dirac += d * casimir_energy_S1_massive(a, L=L, M_max=M_max, antiperiodic=antiperiodic)
    return E_dirac

def kk_logdet_remainder_S1(a, L=2*pi, antiperiodic=False):
    L = mp.mpf(L)
    a = mp.mpf(a)
    if a <= 0:
        return mp.ninf
    x = exp(-a * L)
    if antiperiodic:
        return 2 * log(1 + x)
    return 2 * log(1 - x)

def dirac_logdet_remainder_KK_RP3_S1(k_max=80, L=2*pi, antiperiodic=False):
    L = mp.mpf(L)
    total = mp.mpf(0)
    for k in range(0, k_max):
        n = 2 * k + 1
        d = 2 * (n + 1) * (n + 2)
        a = n + mp.mpf('1.5')
        total += d * kk_logdet_remainder_S1(a, L=L, antiperiodic=antiperiodic)
    return -mp.mpf('0.5') * total

E_dirac_P = dirac_casimir_like_KK_RP3_S1(k_max=12, M_max=50, L=2*pi, antiperiodic=False)
E_dirac_AP = dirac_casimir_like_KK_RP3_S1(k_max=12, M_max=50, L=2*pi, antiperiodic=True)
E_dirac_boson_like = E_dirac_P
E_dirac_fermion_like = -E_dirac_boson_like
print("Dirac (RP³×S¹) в KK-прототипе: из-за спектрального зазора |λ|≥3/2 вклад мал по сравнению с 1/24")
print("  (P)  периодические BC на S¹ (m∈Z)")
print(f"    E_dirac(P) (boson-like) = {float(E_dirac_P):+.15e}")
print(f"    |E_dirac(P)|/(1/24)     = {float(abs(E_dirac_P) / (mp.mpf(1)/24)):.3e}")
print("  (AP) антипериодические BC на S¹ (m∈Z+1/2, proxy через (-1)^m)")
print(f"    E_dirac(AP) (boson-like)= {float(E_dirac_AP):+.15e}")
print(f"    |E_dirac(AP)|/(1/24)    = {float(abs(E_dirac_AP) / (mp.mpf(1)/24)):.3e}")
print(f"  κ_proxy(P) = κ_gauge + E_dirac(P, fermion-like) = {float(kappa_cas_gauge_KK_RP3_S1(30, 50) - E_dirac_P):.15f}")

F_dirac_P = dirac_logdet_remainder_KK_RP3_S1(k_max=80, L=2*pi, antiperiodic=False)
F_dirac_AP = dirac_logdet_remainder_KK_RP3_S1(k_max=80, L=2*pi, antiperiodic=True)
print("Dirac (RP³×S¹) проверка в ζ-det-духе: KK-остаток суммы Σ_m log((2πm/L)^2+a^2) после вычитания локального члена")
print(f"  F_dirac(P)  = {float(F_dirac_P):+.15e}")
print(f"  F_dirac(AP) = {float(F_dirac_AP):+.15e}")
print(f"  |F_dirac(P)|/(1/24)  = {float(abs(F_dirac_P) / (mp.mpf(1)/24)):.3e}")
print(f"  |F_dirac(AP)|/(1/24) = {float(abs(F_dirac_AP) / (mp.mpf(1)/24)):.3e}")

kappa_gauge_KK = kappa_cas_gauge_KK_RP3_S1(k_max=30, M_max=50, L=2*pi, include_scalar_lambda0_level=True)
kappa_qed_P = kappa_gauge_KK + F_dirac_P
kappa_qed_AP = kappa_gauge_KK + F_dirac_AP
print("Полная 1-loop QED-комбинация в KK-прототипе: κ_total = κ_gauge + F_Dirac (не-локальный остаток)")
print(f"  κ_gauge(KK) = {float(kappa_gauge_KK):.15f}")
print(f"  κ_QED(P)    = {float(kappa_qed_P):.15f},  Δ от 1/24 = {float(kappa_qed_P - mp.mpf(1)/24):+.3e}")
print(f"  κ_QED(AP)   = {float(kappa_qed_AP):.15f},  Δ от 1/24 = {float(kappa_qed_AP - mp.mpf(1)/24):+.3e}")

print("Сходимость F_dirac по k_max (должно быстро стабилизироваться из-за exp(-L a))")
for K in [20, 40, 80, 120]:
    Fp = dirac_logdet_remainder_KK_RP3_S1(k_max=K, L=2*pi, antiperiodic=False)
    Fap = dirac_logdet_remainder_KK_RP3_S1(k_max=K, L=2*pi, antiperiodic=True)
    print(f"  k_max={K:>3}: F_dirac(P)={float(Fp):+.15e}, F_dirac(AP)={float(Fap):+.15e}")

S_geo_tmp = 4*pi**3 + pi**2 + pi
sigma_codata = mp.mpf('0.000000085')
d_alpha_P = -F_dirac_P / S_geo_tmp
d_alpha_AP = -F_dirac_AP / S_geo_tmp
print("Оценка влияния Dirac-остатка на α⁻¹, если добавлять его в κ (только чувствительность):")
print(f"  Δα⁻¹(P)  ≈ {float(d_alpha_P):+.3e}  (~{float(d_alpha_P/sigma_codata):+.3f}σ)")
print(f"  Δα⁻¹(AP) ≈ {float(d_alpha_AP):+.3e}  (~{float(d_alpha_AP/sigma_codata):+.3f}σ)")

# =============================================================================
# §5. КАНОНИЧЕСКАЯ ФОРМУЛА
# =============================================================================

print("\n§5. ИТОГОВАЯ ФОРМУЛА")
print("-"*40)

# Геометрическое ядро
S_geo = 4*pi**3 + pi**2 + pi

# Поправки
kappa_Cas = kappa_Cas_num
delta_Cas = kappa_Cas / S_geo
delta_BlackBody = 1 / (pi**4 * S_geo**2)

# Результат
alpha_inv = S_geo - delta_Cas - delta_BlackBody

print(f"S_geo           = {float(S_geo):.12f}")
print(f"κ_Cas           = {float(kappa_Cas):.15f}")
print(f"δ_Cas           = {float(delta_Cas):.15f}")
print(f"δ_BlackBody     = {float(delta_BlackBody):.15f}")
print(f"\nα⁻¹ (theory)    = {float(alpha_inv):.12f}")
print(f"α⁻¹ (CODATA)    = 137.035999177")

diff_val = float(alpha_inv) - 137.035999177
uncertainty = 0.000000085
sigma = diff_val / uncertainty

print(f"\nΔ               = {diff_val:.2e}")
print(f"Отклонение      = {sigma:.4f}σ")

# =============================================================================
# §6. РАЗБОР ЧЛЕНОВ
# =============================================================================

print("\n§6. ПРОИСХОЖДЕНИЕ КАЖДОГО ЧЛЕНА")
print("-"*40)

print(f"""
┌─────────────────────────────────────────────────────────────────┐
│  ЧЛЕН          │  ЗНАЧЕНИЕ        │  ПРОИСХОЖДЕНИЕ              │
├─────────────────────────────────────────────────────────────────┤
│  4π³           │  {float(4*pi**3):.10f}  │  Vol(S³×S¹), фермионы       │
│  π²            │  {float(pi**2):.10f}   │  Vol(RP³), бозоны           │
│  π             │  {float(pi):.10f}    │  Sys(RP³), топология        │
├─────────────────────────────────────────────────────────────────┤
│  S_geo         │  {float(S_geo):.10f}  │  СУММА                      │
├─────────────────────────────────────────────────────────────────┤
│  -κ_Cas/S      │  {float(-delta_Cas):.12f}│  Casimir-поправка       │
│  -1/(π⁴·S²)    │  {float(-delta_BlackBody):.12f}│  Stefan-Boltzmann       │
├─────────────────────────────────────────────────────────────────┤
│  α⁻¹           │  {float(alpha_inv):.10f}  │  ИТОГО                      │
│  CODATA        │  137.035999177   │  Эксперимент                │
│  Δ/σ           │  {sigma:+.4f}σ          │  В пределах погрешности     │
└─────────────────────────────────────────────────────────────────┘
""")

print("="*70)
print("СТАТУС: численное совпадение воспроизводимо; строгая нормировка κ_Cas и других констант вынесена в отдельные файлы")
print("="*70)
