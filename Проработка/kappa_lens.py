import mpmath as mp

mp.mp.dps = 80

# Multiplicities (Ikeda 1979) for even/odd projection
# Scalars (Delta_0): lambda_n = n(n+2), mult_S3 = (n+1)^2
# Vectors coexact (Delta_1): lambda_n = (n+1)^2, mult_S3 = 2 n (n+2)
# Dirac: eigenvalues ±(n+3/2), mult_S3 = 2 (n+1)(n+2)
# On L(2,1): even n survive for bosons; odd n survive for spinor.

def mult_scalar_L(n):
    return 0.5 * (1 + (-1) ** n) * (n + 1) ** 2

def mult_scalar_even_S3(n):
    return 0.5 * (n + 1) ** 2

def mult_vector_L(n):
    return 0.5 * (1 + (-1) ** n) * 2 * n * (n + 2)

def mult_vector_even_S3(n):
    return 0.5 * 2 * n * (n + 2)

def mult_dirac_L(n):
    # note: odd n suppressed, so factor (1+(-1)^{n+1})
    return 0.5 * (1 + (-1) ** (n + 1)) * 2 * (n + 1) * (n + 2)

def mult_dirac_even_S3(n):
    # reference even sector
    return 0.5 * 2 * (n + 1) * (n + 2)

def lam_scalar(n):
    return n * (n + 2)

def lam_vector(n):
    return (n + 1) ** 2

def lam_dirac(n):
    return (n + 1.5) ** 2  # use square of eigenvalue for determinant

def kappa_stabilized(mult_L, lam_fn, N_max=5000):
    total_dz0 = mp.mpf("0")
    results = []
    
    for n in range(1, N_max + 1):
        mL = mult_L(n)
        # dS3 - кратность на накрытии S3 (гладкая часть)
        if "scalar" in mult_L.__name__: 
            dS3 = (n + 1)**2
            # Для L(2,1) mL = 0.5 * (1 + (-1)^n) * (n+1)^2
            # diff_m = mL - 0.5*dS3 = 0.5 * (-1)^n * (n+1)^2
        elif "vector" in mult_L.__name__: 
            dS3 = 2 * n * (n + 2)
        else: # Dirac
            dS3 = 2 * (n + 1) * (n + 2)
            
        diff_m = mL - 0.5 * dS3
        # log(lam_fn(n)) ~ 2 log(n) + O(1/n)
        # Сумма (-1)^n * n^2 * log(n) расходится.
        # Однако физически нас интересует регуляризованный остаток.
        # Используем экспоненциальное сглаживание (heat kernel регуляризация)
        # или анализ средних.
        
        term_dz0 = -diff_m * mp.log(lam_fn(n))
        total_dz0 += term_dz0
        
        # Вычисляем скользящее среднее для подавления осцилляций (-1)^n
        if n > 100 and n % 2 == 0:
            # Для (-1)^n среднее по двум соседним шагам убирает n^2 log n
            # но нужно быть аккуратнее с ростом n.
            current_kappa = total_dz0 / ref_circle
            results.append(current_kappa)
            
    # Анализ сходимости средних
    if len(results) > 10:
        # Пытаемся найти предел последовательности средних
        # (в простейшем случае - среднее последних значений)
        last_avg = sum(results[-10:]) / 10
        return last_avg, results
    return total_dz0 / ref_circle, results

# Нормировка на 1/24 (целевое значение)
ref_circle = mp.mpf("1.0") 

for label, mL, lam in [
    ("scalar", mult_scalar_L, lam_scalar),
    ("vector", mult_vector_L, lam_vector),
    ("dirac", mult_dirac_L, lam_dirac),
]:
    print(f"\n--- Calculating stabilized kappa for {label} ---")
    avg_k, res = kappa_stabilized(mL, lam, N_max=4000)
    print(f"Averaged result: {mp.nstr(avg_k, 10)}")
    print(f"Trend (last 5): {[mp.nstr(x, 6) for x in res[-5:]]}")
