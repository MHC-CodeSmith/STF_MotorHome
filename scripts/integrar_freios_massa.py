"""I33: repete campos r-z com massa/CG do novo CAD e teto de PBT."""
import itertools
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.freios_axisimetricos import Pista, resolver


def main():
    out=ROOT/'entregas/desenvolvimento_2026-11-09/freios_integrados';out.mkdir(parents=True,exist_ok=True)
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());p={k:v['value'] for k,v in c['parameters'].items()}
    bc=yaml.safe_load((ROOT/'config/freios_proposta.yaml').read_text());b=bc['assumed'];mat=bc['material_reference']
    typ=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/integracao/layouts_massas.json').read_text())['layouts']['A_fixa']['nominal']
    track=Pista(b['inner_ring_radius_m'],bc['reference_component']['diameter_m']/2,
                b['plate_thickness_m'],b['pad_track_inner_radius_m'],b['pad_track_outer_radius_m'],
                mat['density_kg_m3'],mat['cp_j_kgk'],mat['conductivity_w_mk'])
    rows=[];adherence=[]
    for mass,regen in itertools.product([typ['mass_kg'],4250],p['regen_power_study_kw']):
        def components(t,mass=mass,regen=regen):
            v=30-4*t;demand=mass*4*v
            aero=.5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*v**3
            rolling=p['crr_range'][1]*mass*9.80665*v
            recovered=min(regen*1000,max(0,demand-aero-rolling))
            return demand,aero,rolling,recovered,max(0,demand-aero-rolling-recovered)
        for nr,nz,dt in [(24,8,.02),(48,16,.02),(96,32,.02),(96,32,.01)]:
            r=resolver(track,massa_kg=mass,fracao_eixo=b['front_axle_energy_fraction'],fracao_disco=b['disc_heat_fraction'],
                       nr=nr,nz=nz,dt_s=dt,potencia_total_friccao_w=lambda t:components(t)[4])
            points=(np.arange(round(5/dt))+.5)*dt
            es=np.sum([components(t) for t in points],axis=0)*dt
            rows.append({'mass_kg':mass,'regen_cap_hypothetical_kw':regen,'nr':nr,'nz':nz,'dt_s':dt,
                         'kinetic_j':400*mass,'aero_j':float(es[1]),'rolling_j':float(es[2]),'regen_mechanical_j':float(es[3]),
                         'friction_total_j':float(es[4]),'mechanical_residual_j':float(es[0]-sum(es[1:])),
                         'thermal_residual_j':r['residuo_disco_j'],'peak_surface_c':r['pico_superficie_k']-273.15})
            if nr==96 and dt==.01:
                stem=f'{mass:.3f}kg_regen{regen}kw'
                np.savez_compressed(out/f'campo_{stem}.npz',temperature_k=r['temperatura_k'],r_m=r['r_m'],z_m=r['z_m'])
                pd.DataFrame(r['historico']).to_csv(out/f'temperatura_tempo_{stem}.csv',index=False)
                fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
                image=ax.pcolormesh(r['r_m']*1000,r['z_m']*1000,r['temperatura_k'].T-273.15,shading='nearest',cmap='inferno')
                fig.colorbar(image,ax=ax,label='°C');ax.set(xlabel='r [mm]',ylabel='z [mm]',title=f'I33 campo r-z — {stem} (condicionado)')
                fig.savefig(out/f'campo_{stem}.png',dpi=150);plt.close(fig)
        front=mass*(p['wheelbase_m']-typ['cg_x_m'])/p['wheelbase_m']+mass*4*typ['cg_z_m']/(9.80665*p['wheelbase_m'])
        rear=mass-front
        adherence.append({'mass_kg':mass,'regen_hypothesis_kw':regen,'front_dynamic_kg':front,'rear_dynamic_kg':rear,
                          'front_mu_demand_upper_bound':mass*4*.7/(9.80665*front),'rear_mu_demand_upper_bound':mass*4*.3/(9.80665*rear),
                          'note':'Repartição70/30estimada; sem dadosABS/pneus/limites regeneração. Valor inclui força total, conservador frente às resistências.'})
    pd.DataFrame(rows).to_csv(out/'convergencia.csv',index=False)
    pd.DataFrame(adherence).to_csv(out/'transferencia_carga_aderencia.csv',index=False)
    (out/'resumo.json').write_text(json.dumps({'cases':len(rows),'mass_typical_kg':typ['mass_kg'],
        'disc_geometry_oem_verified':False,'material_is_railway_reference':True,'regeneration_accepted_at_pack_proven':False,
        'initial_speed_108kmh_is_prescribed_component_test':True,'oem_limiter_kmh':90,'physical_validation':False},indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'max_thermal_residual_j':max(abs(r['thermal_residual_j']) for r in rows)}))


if __name__=='__main__':main()
