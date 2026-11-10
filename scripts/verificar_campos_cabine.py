"""Balanço independente por faces: condução/difusão + armazenamento do ar CFD."""
import json
import re

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from desenvolver_cabine_cfd import ROOT, scalar_field


def patch_values(text, name, count):
    block=re.search(r'\b'+name+r'\s*\{(.*?)\n\s*\}',text,re.DOTALL)[1]
    nonuniform=re.search(r'value\s+nonuniform\s+List<scalar>\s+\d+\s*\((.*?)\)\s*;',block,re.DOTALL)
    if nonuniform: return np.fromstring(nonuniform[1],sep=' ')
    uniform=float(re.search(r'value\s+uniform\s+([\deE.+-]+)',block)[1])
    return np.full(count,uniform)


def main():
    root=ROOT/'entregas/desenvolvimento_2026-11-09'
    base=json.loads((root/'cabine_cfd/resumo.json').read_text())
    transient=json.loads((root/'cabine_transiente/resumo.json').read_text())
    walls=base['wall_equivalent_c'];L,W,H=base['geometry_m'];rho_cp=1.1*1006
    checks=[]
    for row in transient['cases']:
        nx,ny,nz=row['mesh'];case=root/'cabine_transiente'/f'mesh_{nx}_{ny}_{nz}_dt{row["max_dt_s"]}'
        mesh=case/'constant/polyMesh'
        owner_text=(mesh/'owner').read_text()
        owner=np.fromstring(re.search(r'\n\d+\s*\((.*?)\)',owner_text,re.DOTALL)[1],sep=' ',dtype=int)
        boundary=(mesh/'boundary').read_text()
        heat=[]
        for time in ['250','300']:
            T=scalar_field(case/time/'T');alphat=(case/time/'alphat').read_text()
            patch_flux={}
            for name in walls:
                patch=re.search(r'\b'+name+r'\s*\{(.*?)\}',boundary,re.DOTALL)[1]
                n=int(re.search(r'nFaces\s+(\d+)',patch)[1]);start=int(re.search(r'startFace\s+(\d+)',patch)[1])
                a=patch_values(alphat,name,n)
                if len(a)!=n: raise ValueError('Patch incompleto')
                axis=0 if name in ['front','rear'] else (1 if name in ['left','right'] else 2)
                dim=[L,W,H][axis]; cells=[nx,ny,nz][axis]
                area=([W*H,L*H,L*W][axis])/n
                q=rho_cp*(1.7e-5/.71+a)*(walls[name]+273.15-T[owner[start:start+n]])/(dim/cells/2)*area
                patch_flux[name]=float(q.sum())
            heat.append({'time_s':float(time),'mean_k':float(T.mean()),'flux_w':patch_flux,'net_w':sum(patch_flux.values())})
        storage=rho_cp*L*W*H*(heat[1]['mean_k']-heat[0]['mean_k'])
        input_energy=50*(heat[0]['net_w']+heat[1]['net_w'])/2
        total_transfer=50*sum((abs(heat[0]['flux_w'][k])+abs(heat[1]['flux_w'][k]))/2 for k in walls)
        checks.append({'mesh':row['mesh'],'dt_max_s':row['max_dt_s'],'heat_faces':heat,
                       'stored_energy_change_j':storage,'integrated_boundary_heat_j':input_energy,
                       'balance_residual_j':input_energy-storage,
                       'relative_to_absolute_boundary_transfer':abs(input_energy-storage)/total_transfer,
                       'quadrature':'trapézio de snapshots250/300s; não integração exata dos passos internos'})
    finest=root/'cabine_transiente/mesh_48_20_20_dt0.1/campo_3d.npz';field=np.load(finest)
    T=field['temperature_c'];U=field['velocity_m_s'];x=field['x_m'];z=field['z_m'];j=T.shape[1]//2
    fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
    image=ax.pcolormesh(x,z,T[:,j,:],shading='nearest',cmap='inferno')
    ax.quiver(x[::3],z[::2],U[::2,j,::3,0],U[::2,j,::3,2],color='cyan',scale=1.8)
    fig.colorbar(image,ax=ax,label='Temperatura [°C]')
    ax.set(xlabel='X [m]',ylabel='Z [m]',title='I31 — CFD3D transiente complementar, t=300s após restart\nCaixa equivalente; não validação física',aspect='equal')
    fig.savefig(root/'cabine_transiente/campo_temperatura_velocidade.png',dpi=160);plt.close(fig)
    mean_delta=abs(transient['cases'][2]['snapshots'][-1]['mean_c']-transient['cases'][1]['snapshots'][-1]['mean_c'])
    time_delta=abs(transient['cases'][3]['snapshots'][-1]['mean_c']-transient['cases'][1]['snapshots'][-1]['mean_c'])
    out={'cases':checks,'finest_mesh_mean_delta_k':mean_delta,'half_step_mean_delta_k':time_delta,
         'acceptable_physical_result':False,'notes':['Balanço utiliza o mesmo fluxo discreto e Cp/rho constantes assumidos.',
             'Independência de máximo/estratificação e funções de parede não demonstradas.',
             'SIMPLE não convergiu; transiente fornece evolução e diagnóstico, não contorno validado.']}
    (root/'cabine_transiente/balanco_convergencia.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'mesh_delta_k':mean_delta,'time_delta_k':time_delta,'balances':checks},ensure_ascii=False))


if __name__=='__main__': main()
