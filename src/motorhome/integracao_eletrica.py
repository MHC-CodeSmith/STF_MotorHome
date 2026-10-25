"""Triagem de envelopes e orçamento incremental, sem duplicar o trem de força OEM."""

import numpy as np


def analisar(eletrica, interior):
    caixas = list(eletrica['items'])
    offset = np.array([interior['alignment_assumed']['rear_x_m'],
                       -interior['alignment_assumed']['cargo_width_m']/2,
                       interior['alignment_assumed']['floor_z_m']])
    caixas += [{**i, 'position_xyz_m': (np.array(i['position_xyz_m'])+offset).tolist()}
               for i in interior['items']]
    overlaps = []
    for k, a in enumerate(caixas):
        lo = np.array(a['position_xyz_m'])
        hi = lo+np.array(a['dimensions_xyz_m'])
        for b in caixas[k+1:]:
            low = np.array(b['position_xyz_m'])
            high = low+np.array(b['dimensions_xyz_m'])
            delta = np.minimum(hi, high)-np.maximum(lo, low)
            if (delta > 1e-9).all():
                overlaps.append({'ids': [a['id'], b['id']], 'overlap_volume_m3': float(delta.prod())})
    service_items = [i for i in eletrica['items'] if not i['mass_in_oem_curb'] and not i.get('optional_extension')]
    bank = eletrica['service_bank']
    return {'equipment_pair_overlaps': overlaps,
            'scope': 'AABB de equipamentos, sem estrutura OEM, acabamentos, portas, terminais ou rotas de tubos/cabos',
            'known_added_service_mass_kg': sum(i['mass_kg'] or 0 for i in service_items),
            'unknown_added_mass_ids': [i['id'] for i in service_items if i['mass_kg'] is None],
            'oem_traction_mass_already_in_curb': True,
            'main_bank_energy_kwh': bank['quantity']*51.2*100/1000,
            'bank_continuous_current_a': bank['max_continuous_discharge_a'],
            'bank_recommended_min_200ah_met': bank['capacity_ah'] >= 200,
            'pack_floor_gap_assumed_m': .68-(.23+.32),
            'pack_ground_clearance_assumed_m': .23,
            'full_vehicle_interference_free_verified': False}
