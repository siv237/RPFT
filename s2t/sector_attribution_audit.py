import json
import math

with open('enriched_sector_map_results.json', encoding='utf-8') as f:
    data = json.load(f)

mu_trend = data['mu_trend']
beta_trend = data['beta_trend']

# Finite-difference style sensitivities
mu_slopes = []
for left, right in zip(mu_trend, mu_trend[1:]):
    dmu = right['mu_heavy'] - left['mu_heavy']
    da2 = right['mean_a2_fit'] - left['mean_a2_fit']
    da2n = right['mean_a2_over_4pi_fit'] - left['mean_a2_over_4pi_fit']
    mu_slopes.append({
        'mu_interval': [left['mu_heavy'], right['mu_heavy']],
        'da2_dmu': da2 / dmu,
        'd_a2_over_4pi_dmu': da2n / dmu,
    })

beta_slopes = []
for left, right in zip(beta_trend, beta_trend[1:]):
    dbeta = right['beta'] - left['beta']
    da2 = right['mean_a2_fit'] - left['mean_a2_fit']
    dtheta_plus = right['theta_plus_over_pi'] - left['theta_plus_over_pi']
    dtheta_minus = right['theta_minus_over_pi'] - left['theta_minus_over_pi']
    beta_slopes.append({
        'beta_interval': [left['beta'], right['beta']],
        'da2_dbeta': da2 / dbeta,
        'dtheta_plus_over_pi_dbeta': dtheta_plus / dbeta,
        'dtheta_minus_over_pi_dbeta': dtheta_minus / dbeta,
    })

mean_abs_mu_sensitivity = sum(abs(row['da2_dmu']) for row in mu_slopes) / len(mu_slopes)
mean_abs_beta_sensitivity = sum(abs(row['da2_dbeta']) for row in beta_slopes) / len(beta_slopes)
separation_ratio = mean_abs_mu_sensitivity / max(mean_abs_beta_sensitivity, 1e-15)

results = {
    'source': 'enriched_sector_map_results.json',
    'mu_slopes': mu_slopes,
    'beta_slopes': beta_slopes,
    'summary': {
        'mean_abs_da2_dmu': mean_abs_mu_sensitivity,
        'mean_abs_da2_dbeta': mean_abs_beta_sensitivity,
        'sector_separation_ratio': separation_ratio,
        'interpretation': {
            'holonomy_sector': 'beta strongly controls phase branches theta_+, theta_- while barely moving mean a2',
            'mass_sector': 'mu strongly controls mean a2 and a2/(4pi), hence the subleading internal spectral load',
            'volume_sector': 'a0 remains approximately invariant across the map and stays geometric-leading',
        },
    },
    'proposed_dictionary': [
        {
            'operator_component': 'a0 leading term',
            'role': 'global geometric vacuum backbone',
            'toe_reading': 'background spectral-correlation volume sector',
            'ugsm_reading': 'vacuum geometric normalization sector',
        },
        {
            'operator_component': 'a2 local/subleading term',
            'role': 'local curvature plus internal spectral load',
            'toe_reading': 'local geometric-response block',
            'ugsm_reading': 'effective EFT curvature/mass-sensitive sector',
        },
        {
            'operator_component': 'theta_+, theta_- branches',
            'role': 'global holonomy/Wilson sector',
            'toe_reading': 'modular/phase-like global branch',
            'ugsm_reading': 'pi-sector and compact-cycle phase sector',
        },
        {
            'operator_component': 'mu-heavy channel',
            'role': 'internal channel loading',
            'toe_reading': 'hidden/internal spectral substructure',
            'ugsm_reading': 'effective internal multiplet deformation of observables',
        },
    ],
}

with open('sector_attribution_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))