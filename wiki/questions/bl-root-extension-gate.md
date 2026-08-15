# B-L Root Extension Gate

> Status: working
> Research status: representation and continuous-anomaly gates pass; dynamics remain open
> Type: question
> Updated: 2026-08-06

## Question

Can the missing sterile order-four root connection and the charge-two Majorana pairing field arise from one minimal, anomaly-free extension?

## Results

- In left-handed Weyl convention, one `N_c` with B-L charge `+1` per generation cancels the gravitational, cubic, nonabelian mixed, and both abelian mixed anomalies.
- A B-L generator holonomy of `pi/2` acts on `N_c` by `+i` and squares to the required meridian sign `-1`.
- A scalar with B-L charge `-2` makes `Phi_BL N_c N_c` gauge invariant and converts the meridian flux into unit pairing winding.
- The mixed trace `sum Y(B-L)=8/3` per generation is nonzero, so kinetic mixing is a genuine new running coupling.
- The extension also adds a gauge coupling, breaking scale, scalar potential, Higgs portal, and Majorana Yukawa matrix.

## Verdict

This is the first tested coherent extension that closes the root representation and continuous local anomaly gates. It is not a closure of the frozen S2T action because its finite-algebra origin, symmetry-breaking saddle, kinetic-mixing boundary value, and mass scale remain underived.

## Evidence

- `s2t/audits/s2t_bl_root_extension_gate_audit.py`
- `s2t/results/s2t_bl_root_extension_gate_results.json`
- `s2t/gates/bl_root_extension_gate.tex`