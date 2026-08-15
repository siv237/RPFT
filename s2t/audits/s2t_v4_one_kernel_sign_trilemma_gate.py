import json
import math
import numpy as np
from scipy.special import logsumexp

pi = math.pi
a = (3 / (8 * pi**2)) ** 0.25
b = (1 / (16 * pi**2)) ** 0.25
t = (a / 1.35139219568654) ** 2
ell = np.arange(401, dtype=float)

scalar_s4 = logsumexp(np.log((ell+1)*(ell+2)*(2*ell+3)/6)-t*ell*(ell+3)/a**2)
scalar_s22 = 2*logsumexp(np.log(2*ell+1)-t*ell*(ell+1)/b**2)
dirac_s4 = logsumexp(np.log(8*(ell+1)*(ell+2)*(ell+3)/6)-t*(ell+2)**2/a**2)
dirac_s22 = 2*logsumexp(np.log(4*(ell+1))-t*(ell+1)**2/b**2)

def row(x, y):
    z4, z22 = math.exp(x), math.exp(y)
    f4, f22 = -x/t, -y/t
    return {"trace_S4": z4, "trace_S2xS2": z22,
            "bare_winner": "S4" if z4 < z22 else "S2xS2",
            "Gibbs_S4": f4, "Gibbs_S2xS2": f22,
            "Gibbs_winner": "S4" if f4 < f22 else "S2xS2"}

result = {
    "gate": "version4_one_kernel_sign_trilemma", "date": "2026-08-11",
    "time": t, "scale_identity": "Lambda*sigma=1",
    "scalar": row(scalar_s4, scalar_s22), "Dirac": row(dirac_s4, dirac_s22),
    "verdict": "one trace and minus-log trace have opposite carrier minima",
}
with open("s2t_v4_one_kernel_sign_trilemma_gate_results.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2); f.write("\n")
print(json.dumps(result, ensure_ascii=False, indent=2))