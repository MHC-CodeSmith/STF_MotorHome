"""Alternativa real400W dobrável: geração, MPPT, massa e triagem de armazenamento."""

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from motorhome.solar import integrar_kwh, simular_dia


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    paths = [Path('config/solar_portatil_proposta.yaml'), Path('config/solar_proposta.yaml'),
             Path('config/equipamentos_interior.yaml'), Path('config/instalacoes_eletricas_proposta.yaml'),
             Path('entregas/parcial_2026-10-24/resumo_expansao_solar.json'),
             Path('entregas/parcial_2026-10-24/resumo_integracao_eletrica.json')]
    c, base, interior, electrical = [yaml.safe_load(f.read_text()) for f in paths[:4]]
    expansion, integration = [json.loads(f.read_text()) for f in paths[4:]]
    m, a, ctrl = c['module'], c['assumed'], c['controller']
    solar = copy.deepcopy(base)
    solar['module'].update(p_stc_w=m['p_stc_w'], gamma_pdc_per_k=m['gamma_pdc_per_k'])
    solar['array'].update(module_counts=[m['quantity']], tilt_deg=a['ground_tilt_deg'], azimuth_deg=a['azimuth_deg'])
    data = simular_dia(solar)
    column = f'terminal_assumed_{m["quantity"]}_modules_w'
    energy = integrar_kwh(data[column])
    # Reserva vertical: comprimento X e altura Z da bolsa são assumidos, não cotas OEM.
    cases, clashes = [], []
    for index in range(m['quantity']):
        pos = list(a['first_case_position_interior_xyz_m'])
        pos[1] += index*a['case_envelope_xyz_m'][1]
        cases.append({'id': f'bolsa_pv_{index+1}', 'position_xyz_m': pos, 'dimensions_xyz_m': a['case_envelope_xyz_m']})
    equipment = [dict(item) for item in interior['items']]
    for item in electrical['items']:
        pos = list(item['position_xyz_m'])
        pos = [pos[0]+3.35, pos[1]+.935, pos[2]-.68]
        equipment.append(item | {'position_xyz_m': pos})
    for case in cases:
        for item in equipment:
            delta = [min(x+s, y+t)-max(x, y) for x, s, y, t in zip(case['position_xyz_m'], case['dimensions_xyz_m'], item['position_xyz_m'], item['dimensions_xyz_m'], strict=True)]
            if all(d > 1e-8 for d in delta):
                clashes.append([case['id'], item['id']])
    cold_v = ctrl['series']*m['voc_v']*(1+(abs(m['beta_voc_per_k'])+m['beta_voc_uncertainty_per_k'])*(25-a['cold_design_c']))
    hot_vmp = ctrl['series']*m['vmp_v']*(1+m['beta_voc_per_k']*(a['operating_cell_hot_c']-25))
    # betaVoc usado como aproximação de betaVmp: marcar triagem, não garantia de MPPT.
    input_isc = ctrl['parallel']*m['isc_a']
    if cold_v >= ctrl['max_cold_voc_v'] or input_isc >= ctrl['max_pv_short_circuit_a'] or clashes:
        raise ValueError({'cold_v': cold_v, 'isc_a': input_isc, 'clashes': clashes})
    total = energy+expansion['energy_kwh']['mixed_stowed_w']
    house = expansion['household_total_excluding_dryer_kwh_day']
    result = {'status': c['status'], 'portable_generation_kwh_day': energy,
              'fixed_plus_portable_generation_kwh_day': total,
              'surplus_after_house_at_assumed90pct_efficiency_kwh_day': total-house/.9,
              'additional_known_mass_kg': m['quantity']*m['mass_with_case_kg']+a['additional_controller_mass_kg'],
              'known_subtotal_with_portable_kg': integration['new_known_mass_subtotal_kg']+m['quantity']*m['mass_with_case_kg']+a['additional_controller_mass_kg'],
              'cold_voc_design_v': cold_v, 'input_isc_stc_a': input_isc,
              'hot_vmp_approx_v': hot_vmp, 'output_current_at44_8v_ideal_a': m['quantity']*m['p_stc_w']/44.8,
              'output_note': '35A pode limitar perto de44,8V; potência máxima nominal não é garantia de saída sem clipping.',
              'case_envelopes_interior': cases, 'equipment_clashes_aabb': clashes,
              'limits': c['limits']+['Vmp quente aproximado com betaVoc; margem de partida requer curvaIV real.',
                                     'Faiman/perdas10%/conversão95% mantidos como hipóteses; sem sombra, só parado, nenhuma agenda otimizada.',
                                     'AABB verifica equipamentos, não todo estrado/rotas/abertura da porta; reserva de bolsa ainda não medida.'],
              'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in [*paths, Path(__file__), Path('src/motorhome/solar.py')]}}
    args.destino.mkdir(parents=True, exist_ok=False)
    data.to_csv(args.destino/'solar_portatil.csv')
    (args.destino/'resumo_solar_portatil.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['inputs_sha256','limits','case_envelopes_interior']}, indent=2))


if __name__ == '__main__':
    main()
