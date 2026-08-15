import numpy as np

# 1. Fundamental Geometric Constants (from deductive logic)
S_geo = 4*np.pi**3 + np.pi**2 + np.pi
delta_Cas = 1/(24 * S_geo)
delta_BB = 1/(np.pi**4 * S_geo**2)

alpha_inv_theory = S_geo - delta_Cas - delta_BB
alpha_theory = 1/alpha_inv_theory

print(f"Inverse Fine Structure Constant (Theory): {alpha_inv_theory:.12f}")

# 2. Derived Electron Parameters

# 2.1 Elementary Charge (e) in Planck units
# alpha = e^2 / (4*pi)  =>  e = sqrt(4 * pi * alpha)
e_planck = np.sqrt(4 * np.pi * alpha_theory)
print(f"Elementary Charge (Planck units):       {e_planck:.12f}")

# 2.2 Anomalous Magnetic Moment (Schwinger term approximation)
# a_e = alpha / (2*pi)
a_e_theory = alpha_theory / (2 * np.pi)
print(f"Anomalous Magnetic Moment (1-loop):     {a_e_theory:.12f}")

# Comparison with CODATA 2022
alpha_inv_codata = 137.035999177
a_e_codata = 0.00115965218059 # CODATA 2022 value for electron magnetic moment anomaly

print("-" * 40)
print("COMPARISON:")
print(f"alpha^-1 Diff: {alpha_inv_theory - alpha_inv_codata:.2e}")
print(f"a_e Diff:      {a_e_theory - a_e_codata:.2e}")

# Theoretical prediction vs Experiment for a_e
# Note: The simple Schwinger term alpha/2pi is only the first order.
# Real physics includes alpha^2, alpha^3... terms.
# Checking if our geometric alpha gives the correct FIRST ORDER contribution.
