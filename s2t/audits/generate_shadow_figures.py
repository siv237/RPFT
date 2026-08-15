import json
import math
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'figure.dpi': 160,
    'font.size': 10,
})

# 1) scalar window stability
with open('spectral_unity_deep_results.json', encoding='utf-8') as f:
    deep = json.load(f)
windows = ['narrow', 'baseline', 'wide']
a0_errs = [deep['window_stability'][w]['a0_rel_err'] for w in windows]
a2_errs = [deep['window_stability'][w]['a2_rel_err'] for w in windows]
fig, ax = plt.subplots(figsize=(6.2, 3.6))
x = np.arange(len(windows))
width = 0.34
ax.bar(x - width/2, a0_errs, width, label='a0 relative error')
ax.bar(x + width/2, a2_errs, width, label='a2 relative error')
ax.set_yscale('log')
ax.set_xticks(x)
ax.set_xticklabels(windows)
ax.set_ylabel('Relative error')
ax.set_title('Scalar-cycle window stability')
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig('fig_scalar_window_stability.png', bbox_inches='tight')
plt.close(fig)

# 2) gauge holonomy phases and gap
with open('gauge_holonomy_results.json', encoding='utf-8') as f:
    gh = json.load(f)
rows = gh['beta_sweep']
betas = [r['beta'] for r in rows]
tp = [r['theta_plus_over_pi'] for r in rows]
tm = [r['theta_minus_over_pi'] for r in rows]
gaps = [r['effective_circle_gap'] for r in rows]
fig, ax1 = plt.subplots(figsize=(6.4, 3.8))
ax1.plot(betas, tp, marker='o', label=r'$\theta_+/\pi$')
ax1.plot(betas, tm, marker='s', label=r'$\theta_-/\pi$')
ax1.set_xlabel(r'$\beta$')
ax1.set_ylabel('Phase / pi')
ax2 = ax1.twinx()
ax2.plot(betas, gaps, color='black', linestyle='--', marker='d', label='effective gap')
ax2.set_ylabel('Effective gap')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc='center right')
ax1.set_title('Gauge-holonomy phase branches and gap')
fig.tight_layout()
fig.savefig('fig_gauge_holonomy_phases.png', bbox_inches='tight')
plt.close(fig)

# 3) enriched sector heatmap over mu and beta for a2/(4pi)
with open('enriched_sector_map_results.json', encoding='utf-8') as f:
    esm = json.load(f)
mu_vals = esm['mu_heavy_values']
beta_vals = esm['betas']
grid = np.zeros((len(mu_vals), len(beta_vals)))
for i, mu in enumerate(mu_vals):
    for j, beta in enumerate(beta_vals):
        row = next(r for r in esm['rows'] if r['mu_heavy'] == mu and r['beta'] == beta)
        grid[i, j] = row['a2_over_4pi_fit']
fig, ax = plt.subplots(figsize=(6.4, 3.8))
im = ax.imshow(grid, aspect='auto', origin='lower', cmap='viridis')
ax.set_xticks(np.arange(len(beta_vals)))
ax.set_xticklabels([str(b) for b in beta_vals])
ax.set_yticks(np.arange(len(mu_vals)))
ax.set_yticklabels([str(m) for m in mu_vals])
ax.set_xlabel(r'$\beta$')
ax.set_ylabel(r'$\mu_{heavy}$')
ax.set_title(r'Heatmap of $a_2/(4\pi)$ in the enriched operator')
fig.colorbar(im, ax=ax, label=r'$a_2/(4\pi)$')
fig.tight_layout()
fig.savefig('fig_enriched_heatmap.png', bbox_inches='tight')
plt.close(fig)

# 4) attribution sensitivities
with open('sector_attribution_results.json', encoding='utf-8') as f:
    sat = json.load(f)
summary = sat['summary']
labels = ['|da2/dmu|', '|da2/dbeta|']
values = [summary['mean_abs_da2_dmu'], summary['mean_abs_da2_dbeta']]
fig, ax = plt.subplots(figsize=(5.8, 3.6))
ax.bar(labels, values, color=['#4c78a8', '#f58518'])
ax.set_yscale('log')
ax.set_ylabel('Mean absolute sensitivity')
ax.set_title('Sector-attribution sensitivity split')
for i, v in enumerate(values):
    ax.text(i, v * 1.15, f'{v:.2e}', ha='center', va='bottom', fontsize=9)
fig.tight_layout()
fig.savefig('fig_sector_attribution.png', bbox_inches='tight')
plt.close(fig)