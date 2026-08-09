# Family Wilson Majorana Core Selector Gate

> Status: algebraic selector pass; common parent action open

## Construction

A generation-blind B-L vortex produces three real Majorana core modes. The
existing oriented family Wilson branch supplies

```text
K_n = Log R_n(theta_*) = theta_* [n]_cross.
```

For every geometrically selected Wilson axis, `K_n` is a real antisymmetric
`3 x 3` matrix of rank two. The boundary coupling

```text
S_core,fam = (i/2) integral chi^T K_n chi
```

gaps two Majorana modes and leaves `ker K_n = R n`, hence exactly one real
core mode. Orientation reversal changes `K_n` to `-K_n` but preserves the
rank-one projector `n n^T`.

## Result

This supplies a non-arbitrary generation selector from an operator already
present in II.B and avoids inserting a rank-one Yukawa matrix by hand:

```text
3 core modes -> 1 core mode.
```

If the ambient-to-core restriction map is constructed, the mechanism can
restore the candidate complement rank `24-1=23`.

## Remaining Gate

The current action does not yet derive the restriction of the same family
Wilson connection to the B-L core. A common boundary superconnection must
produce both the vortex BdG operator and the `K_n` coupling. The numerical
weight `23+pi^-1` also remains open.

## Evidence

- `s2t_family_wilson_majorana_core_selector_audit.py`
- `s2t_family_wilson_majorana_core_selector_results.json`
- `family_wilson_majorana_core_selector_gate.tex`
- [[bl-defect-action-global-consistency-gate]]
- [[continuous-wilson-gap-action-gate]]