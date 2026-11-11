"""Rotas de reserva no layoutA e orientação vertical do inversor candidato."""
import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from gerar_cad_eletrico import linha
from gerar_cad_instalacoes import Modelo

from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.desenvolvimento import caixa_intersecao
from motorhome.protecoes import circuito_dc


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()}
    g=c['development']['installation_routes'];parts=c['development']['layout_equipment']['A_fixa'];model=Modelo()
    out=diretorio_entregas(ROOT)/'rotas_instalacoes';out.mkdir(parents=True,exist_ok=True)
    for part in parts:model.box(part['id'],'equipamento',part['position_m'],part['dimensions_m'],[130,155,180,150])
    inv=next(x for x in parts if x['id']=='inversor');clearance=g['inverter_clearance_m']
    lo=np.array(inv['position_m'])-clearance;size=np.array(inv['dimensions_m'])+2*clearance
    # Back of wall-mounting unit has no claim of 100mm cooling clearance;
    # this envelope is a conservative access reservation around all sides.
    service={'id':'reserva_inversor','position_m':lo.tolist(),'dimensions_m':size.tolist()}
    collisions=[x['id'] for x in parts if x['id']!='inversor' and caixa_intersecao(service,x)>0]
    model.box('reserva_inversor','acesso',lo,size,[255,175,30,65])
    routes=[{'id':'cabo_positivo','points_m':g['service_cable_points_m'],'radius_m':g['cable_radius_m']},
        {'id':'cabo_retorno','points_m':(np.array(g['service_cable_points_m'])+g['cable_return_offset_m']).tolist(),'radius_m':g['cable_radius_m']}]
    routes += [{**x,'radius_m':g['pipe_radius_m']} for x in g['potable_routes']]
    checks=[]
    for route in routes:
        linepts=np.array(route['points_m']);length=float(np.linalg.norm(np.diff(linepts,axis=0),axis=1).sum())
        route['length_m']=length
        linha(model,route['id'],'eletrico' if route['id'].startswith('cabo') else 'hidraulica',linepts,route['radius_m'],[205,50,40,255] if route['id'].startswith('cabo') else [35,110,220,255])
        for a,b in itertools.pairwise(linepts):
            lower=np.minimum(a,b)-route['radius_m'];extent=np.abs(a-b)+2*route['radius_m']
            box={'position_m':lower.tolist(),'dimensions_m':extent.tolist()}
            for part in parts:
                volume=caixa_intersecao(box,part)
                if volume>1e-9:checks.append({'route':route['id'],'part':part['id'],'overlap_aabb_m3':volume,'requires_terminal_or_passage_confirmation':True})
    model.export(out,'layoutA_rotas_reserva',{'rear_x_m':0,'cargo_width_m':0,'floor_z_m':0})
    loop=sum(x['length_m'] for x in routes[:2])*(1+g['slack_fraction'])
    electrical=[{'temperature_c':temp,**circuito_dc(4000,p['cable_min_voltage_v'],p['eta_inverter'],loop,70,temp)} for temp in [20,90]]
    result={'inverter_dimensions_xyz_m':inv['dimensions_m'],'inverter_position_m':inv['position_m'],
        'vertical_height_565mm':inv['dimensions_m'][2]==.565,'service_envelope_collisions':collisions,
        'routes':routes,'estimated_cable_loop_with_slack_m':loop,'route_equipment_aabb_contacts':checks,
        'electrical_for_estimated_route':electrical,'oem_passages_validated':False,
        'note':'Envelopes e AABB de rotas não são verificação de chaparia/terminais reais;contatos em pontos de conexão explicitamente listados. CabosHV não alterados;sem central própria/energia entre bancos.'}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
