"""Sensibilidade geométrica I28: integra dt=dv/a(v), sem alterar raio canônico."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import quad

from motorhome.cenarios import carregar_configuracao, diretorio_entregas

ROOT = Path(__file__).resolve().parents[1]


def main():
    c = carregar_configuracao(ROOT)
    p = {k: v['value'] for k, v in c['parameters'].items()}
    a = c['development']['performance_envelope']
    out = diretorio_entregas(ROOT)/'mecanica_termica'
    geom = json.loads((diretorio_entregas(ROOT)/'integracao/layouts_massas.json').read_text())['layouts']['A_fixa']['nominal']
    mass, x, h = geom['mass_kg'], geom['cg_x_m'], geom['cg_z_m']
    ratio, eta, mu, g, length = 10, .97, .8, 9.80665, p['wheelbase_m']
    rows = []
    for radius in [a['wheel_radius_m'], .361]:
        def acceleration(v, radius=radius):
            resistance = .5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*v*v + p['crr_range'][1]*mass*g
            motor = min(a['peak_torque_nm']*ratio*eta/radius, a['peak_motor_w']*eta/max(v, .001))
            adhesion = (mu*g*(length-x)/length-resistance/mass)/(1+mu*h/length)
            return min((motor-resistance)/mass, adhesion)
        for speed in [90, 100]:
            time_s, error = quad(lambda v: 1/acceleration(v), 0, speed/3.6, epsabs=1e-7, points=[a['peak_motor_w']*radius/(a['peak_torque_nm']*ratio)])
            rows.append({'mass_kg': mass, 'radius_m': radius, 'target_kmh': speed,
                         'time_s': time_s, 'quadrature_error_s': error,
                         'motor_rpm': speed/3.6/radius*ratio*60/(2*np.pi),
                         'limiter_removed_only_in_model': speed > 90})
    frame = pd.DataFrame(rows)
    reference = pd.read_csv(out/'I28_envelope_0_90_sensibilidade.csv')
    reference = reference[(abs(reference.mass_kg-mass)<1e-6)&(reference.gear_ratio_assumed==ratio)&(reference.gear_eta_assumed==eta)&(reference.adhesion_mu_assumed==mu)].iloc[0]
    deltas = [abs(rows[0]['time_s']-reference.time_to_90_s), abs(rows[1]['time_s']-reference.time_to_100_without_limiter_s)]
    if max(deltas) > 1e-4:
        raise ValueError(f'Quadratura independente diverge da integração temporal: {deltas}')
    frame.to_csv(out/'I28_sensibilidade_raio.csv', index=False)
    receipt = {'script': 'scripts/sensibilizar_raio_i28.py', 'date_utc': datetime.now(timezone.utc).isoformat(),
               'configuration_sha256': hashlib.sha256((ROOT/'config/parametros_globais.yaml').read_bytes()).hexdigest(),
               'canonical_radius_unchanged_m': a['wheel_radius_m'], 'gear_ratio_assumed': ratio,
               'gear_efficiency_assumed': eta, 'mu_assumed': mu,
               'maximum_difference_to_time_integration_s': max(deltas), 'physical_validation': False,
               'note': 'Sensibilidade de raio sob o mesmo envelope hipotético; não é curva OEM nem ensaio.'}
    (out/'I28_sensibilidade_raio.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    print(frame.to_string(index=False))


if __name__ == '__main__':
    main()
