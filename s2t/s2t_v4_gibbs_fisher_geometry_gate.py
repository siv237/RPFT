import json, math

source = json.load(open("s2t_v4_correlation_cell_free_energy_density_gate_results.json", encoding="utf-8"))
rows = []
for c in source["candidates"]:
    r = c["radius_over_sigma"]
    fisher = 4*c["variance_dimensionless_eigenvalue"]/r**4
    hx = r**2*c["hessian"]
    rows.append({"name": c["name"], "radius_over_sigma": r,
                 "density": c["dimensionless_density"],
                 "Fisher_log_radius": fisher,
                 "Jeffreys_log_radius": math.sqrt(fisher),
                 "Fisher_normalized_hessian": hx/fisher})
result = {"gate": "version4_gibbs_fisher_geometry", "date": "2026-08-11",
          "formula": "I_x=4 Var(mu)/r^4", "candidates": rows,
          "verdict": "canonical radial measure derived; relative topology prior open"}
with open("s2t_v4_gibbs_fisher_geometry_gate_results.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2); f.write("\n")
print(json.dumps(result, ensure_ascii=False, indent=2))