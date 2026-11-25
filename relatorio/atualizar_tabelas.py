"""Gera valores e tabelas do memorial a partir das saídas do cenário ativo.

Não executa simulações nem altera suas saídas. Evita manter números de massa e
consumo digitados no texto depois de uma mudança no projeto.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'entregas/integrado_maxeon1560'
R = ROOT/'relatorio'


def csvs(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def fmt(v, n=1):
    return f'{float(v):.{n}f}'.replace('.', ',')


def escape(s):
    return s.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')


def table(path, caption, label, headings, rows, spec):
    text = '\\begin{table}[H]\\centering\\small\n'
    text += '\\caption{'+caption+'}\\label{'+label+'}\n'
    text += '\\begin{tabularx}{\\linewidth}{'+spec+'}\n\\toprule\n'
    text += ' & '.join(headings)+' \\\\\n\\midrule\n'
    text += ''.join(' & '.join(row)+' \\\\\n' for row in rows)
    text += '\\bottomrule\n\\end{tabularx}\n\\end{table}\n'
    path.write_text(text)


def main():
    from sys import path
    path.insert(0, str(ROOT/'src'))
    from motorhome.reconciliacao import consumo_plano
    config = json.loads((E/'parametros_resolvidos.json').read_text())
    p = {k:v['value'] for k,v in config['parameters'].items()}
    nominal = json.loads((E/'integracao/layouts_massas.json').read_text())['layouts']['A_fixa']['nominal']
    mass = nominal['mass_kg']
    plates = json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas/resumo.json').read_text())['selected_plates_gross_mass_kg']
    values = {'MassaNom':(mass,1), 'MargemNom':(4250-mass,1), 'CgX':(nominal['cg_x_m'],3),
              'CgY':(nominal['cg_y_m'],3), 'CgZ':(nominal['cg_z_m'],3),
              'EixoDianteiro':(nominal['front_kg'],0), 'EixoTraseiro':(nominal['rear_kg'],0),
              'RolamentoNom':(p['crr_range'][1]*mass*9.80665,0),
              'MassaComChapas':(mass+plates,1), 'MargemComChapas':(4250-mass-plates,1)}
    for speed, word in [(40,'Quarenta'),(80,'Oitenta')]:
        c = consumo_plano(speed,mass,p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=p['traction_aux_assumed_w']/1000)
        values['Consumo'+word]=(c['kwh_km'],3)
        values['DistanciaEnergia'+word]=(c['km_kwh'],2)
        values['PotenciaBateria'+word]=(c['bateria_kw'],2)
    daily=csvs(E/'energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv')
    opt=next(x for x in daily if x['horizon_kind']=='optimal_upto24h' and float(x['soc_initial'])==1)
    opt80=next(x for x in daily if x['horizon_kind']=='optimal_upto24h' and float(x['soc_initial'])==.8)
    values['AlcanceOitentaSoc']=(opt80['distance_km'],1)
    eight=next(x for x in daily if x['horizon_kind']=='fixed' and float(x['driving_horizon_h'])==8 and float(x['soc_initial'])==1)
    eta_red=min(config['development']['performance_envelope']['gear_efficiency'], key=lambda x:abs(x-.97))
    for row, suffix in [(opt,'Dia'),(eight,'Oito')]:
        for key,name,n in [('distance_km','Alcance',1),('constant_speed_kmh','Velocidade',1),('driving_horizon_h','Horas',1),('battery_power_kw','PotenciaBat',2),('wheels_power_kw','PotenciaRoda',2)]:
            values[name+suffix]=(row[key],n)
        values['PotenciaMotor'+suffix]=(float(row['wheels_power_kw'])/eta_red,2)
    acceleration=csvs(E/'mecanica_termica/I28_envelope_0_90_sensibilidade.csv')
    acc=next(x for x in acceleration if abs(float(x['mass_kg'])-mass)<.001 and float(x['gear_ratio_assumed'])==10 and float(x['gear_eta_assumed'])==.97 and float(x['adhesion_mu_assumed'])==.8)
    values['AcelNoventa']=(acc['time_to_90_s'],1)
    values['AcelCem']=(acc['time_to_100_without_limiter_s'],1)
    radius=csvs(E/'mecanica_termica/I28_sensibilidade_raio.csv')
    for row in radius:
        if float(row['radius_m'])==.361:
            values['AcelRaio'+('Noventa' if float(row['target_kmh'])==90 else 'Cem')]=(row['time_s'],2)
    for key,word in [('time_to_90_s','Noventa'),('time_to_100_without_limiter_s','Cem')]:
        values['AcelMin'+word]=(min(float(x[key]) for x in acceleration),1)
        values['AcelMax'+word]=(max(float(x[key]) for x in acceleration),1)
    brakes=csvs(E/'freios_integrados/convergencia.csv')
    for regen,name in [(0,'FreioPico'),(40,'FreioRegenQuarenta'),(80,'FreioRegenOitenta')]:
        row=next(x for x in brakes if abs(float(x['mass_kg'])-mass)<.001 and float(x['regen_cap_hypothetical_kw'])==regen and int(x['nr'])==96 and float(x['dt_s'])==.01)
        values[name]=(row['peak_surface_c'],2)
    bed=json.loads((E/'cama_estrutura/resumo.json').read_text())
    values['MassaExtraCama']=(bed['acrescimo_massa_kg'],1)
    values['MassaCamaInventario']=(bed['massas_kg']['estrado']+bed['massas_kg']['quadro_aco']+bed['massas_kg']['postes_aco']+12,1)
    values['UtilCama']=(bed['utilizacao_maxima'],3)
    sensitivity=csvs(E/'integracao/massa_cg_eixos_sensibilidade.csv')
    for key,word in [('front_kg','Frente'),('rear_kg','Tras'),('pbt_margin_kg','Margem')]:
        for rows,label in [(sensitivity,'Ambos'),([x for x in sensitivity if x['layout']=='A_fixa'],'A')]:
            values[word+'Min'+label]=(min(float(x[key]) for x in rows),0)
            values[word+'Max'+label]=(max(float(x[key]) for x in rows),0)
    dispatch=csvs(E/'despacho_i25/melhores_por_velocidade.csv')
    def solar_row(services, minimum, speed):
        return next(x for x in dispatch if int(x['step_min'])==5 and x['services_cyclic']==str(services)
                    and abs(float(x['hypothetical_dc_min_input_kw'])-minimum)<1e-8 and float(x['speed_kmh'])==speed)
    for services, word in [(False,'Sem'),(True,'Com')]:
        for speed,name in [(40,'Quarenta'),(80,'Oitenta')]:
            values['AutSolar'+word+name]=(solar_row(services,.38,speed)['distance_km'],1)
    candidates=[x for x in dispatch if int(x['step_min'])==15 and x['services_cyclic']=='False'
                and abs(float(x['hypothetical_dc_min_input_kw'])-.38)<1e-8]
    best=max(candidates,key=lambda x:float(x['distance_km']))
    values['AutSolarMax']=(best['distance_km'],1)
    values['AutSolarVel']=(best['speed_kmh'],0)
    rows=[]
    for services,minimum,label in [(False,0,'Sem habitação'),(False,.38,'Sem habitação'),(True,.38,'Com habitação'),(False,3,'Sem habitação')]:
        a,b=solar_row(services,minimum,40),solar_row(services,minimum,80)
        generation=float(a['pv_generated_kwh']); domestic=float(a['service_day_kwh']); hv=float(a['solar_hv_received_kwh'])
        rows.append([label,fmt(minimum,2),fmt(generation,2),fmt(domestic,2),fmt(generation-domestic-hv,2),fmt(hv,2),fmt(a['distance_km']),fmt(b['distance_km'])])
    table(R/'tabela_i25.tex','Item 25 — energia do dia e distância; passo de 5 min e mínimo na saída CC.','tab:i25',
          ['Caso','Mínimo','Geração','Serviços','Perdas/corte','Tração','40 km/h','80 km/h'],rows,'Xrrrrrrr')
    deck=json.loads((ROOT/'entregas/aero_equipado1540/comparacao_deck/resumo.json').read_text())
    deck_rows=[]
    for mode,label in [('com_deck','Com deck'),('sem_deck','Sem deck')]:
        r40=deck['por_velocidade_kmh']['40'][mode];r80=deck['por_velocidade_kmh']['80'][mode]
        deck_rows.append([label,fmt(deck['cd_cfd'][mode],4),fmt(deck['cda_m2'][mode],3),fmt(r40['potencia_bateria_kw'],2),fmt(r80['potencia_bateria_kw'],2),fmt(r40['kwh_km'],3),fmt(r80['kwh_km'],3)])
    table(R/'tabela_deck.tex','Itens19/20/26 — comparação aerodinâmica com a mesma massa; potências no lado da bateria.','tab:deck',
          ['Caso','$C_d$','$C_dA$ [m²]','$P_{40}$ [kW]','$P_{80}$ [kW]','$e_{40}$ [kWh/km]','$e_{80}$ [kWh/km]'],deck_rows,'Xrrrrrr')
    for speed,name in [('40','Quarenta'),('80','Oitenta')]:
        row=deck['por_velocidade_kmh'][speed]
        values['SemDeckCons'+name]=(row['sem_deck']['kwh_km'],3)
        values['SemDeckBat'+name]=(row['sem_deck']['potencia_bateria_kw'],2)
        values['DeckPercentual'+name]=(row['diferenca_percentual'],1)
        values['DeckKmEmpate'+name]=(deck['km_dia_para_empatar'][speed],0)
    (R/'valores_integrados.tex').write_text('% Gerado por relatorio/atualizar_tabelas.py; cenário maxeon1560_independente.\n'+''.join('\\newcommand{\\'+name+'}{'+fmt(v,n)+'}\n' for name,(v,n) in values.items()))
    inventory=[x for x in csvs(E/'integracao/inventario_massas.csv') if x['layout']=='A_fixa']
    # Partição disjunta: cada id é contado uma única vez.
    groups={}
    for row in inventory:
        key=row['id']
        if key=='base_oem':group='Veículo-base (inclui bateria de tração)'
        elif key.startswith(('MAXEON','portatil')) or key=='fixacoes_solares':group='Teto FV, portáteis com bolsas e fixações solares'
        elif key.startswith('US5000') or key=='inversor':group='Banco de serviços e inversor'
        elif key in ['quadro_cama','postes_cama','estrado','cama_colchao']:group='Cama: estrado, quadro, postes e colchão do inventário'
        elif key.startswith('agua'):group='Água limpa/cinza/cassete e boiler (100 L no total)'
        elif key.startswith('ocupante') or key in ['bagagens','consumiveis_alimentos']:group='Ocupantes, bagagem e alimentos'
        elif key in ['geladeira_AC','cassete','cooktop_armazenado','boiler','bomba','lava_seca','hvac']:group='Equipamentos domésticos, sanitário e climatização'
        elif key in ['tanque_limpa','tanque_cinza','suportes_eletricos','hidraulica_acessorios','cabos_protecoes_controle','boiler_dutos_e_grelhas','janelas_protecao_solar','cuba_torneira']:group='Tanques, cabos, hidráulica, suportes e proteções solares'
        else:group='Mobiliário, piso, isolamento e revestimentos'
        groups[group]=groups.get(group,0)+float(row['mass_kg'])
    assert abs(sum(groups.values())-mass)<1e-7
    rows=[[escape(k),fmt(v)] for k,v in groups.items()]
    rows.append([r'\textbf{Total}',r'\textbf{'+fmt(mass)+'}'])
    table(R/'tabela_massa.tex','Item 18 — massa montada com a cama redimensionada; somas do inventário.','tab:massa',['Parcela','Massa [kg]'],rows,'Xr')
    cost=csvs(E/'i24_custo_brl/custo_por_linha.csv'); rows=[]
    for x in cost:
        if x['caso']!='nominal':continue
        low=next(r for r in cost if r['id']==x['id'] and r['caso']=='baixo')
        high=next(r for r in cost if r['id']==x['id'] and r['caso']=='alto')
        rows.append([escape(x['descricao']),x['qtd'],fmt(float(x['total_brl'])/1000,2),fmt(float(low['total_brl'])/1000,2)+'--'+fmt(float(high['total_brl'])/1000,2)])
    rows.append([r'\textbf{Total}', '',fmt(sum(float(x['total_brl']) for x in cost if x['caso']=='nominal')/1000,2),fmt(sum(float(x['total_brl']) for x in cost if x['caso']=='baixo')/1000,2)+'--'+fmt(sum(float(x['total_brl']) for x in cost if x['caso']=='alto')/1000,2)])
    table(R/'tabela_custos.tex','Item 24 — orçamento por componente/rubrica; valores já incluem a hipótese tributária. Estimativas são identificadas na descrição.','tab:custos',['Componente ou rubrica','Qtd.','Nominal [mil R\\$]','Faixa [mil R\\$]'],rows,'Xrrr')
    rows=[]
    for key,v in bed['casos'].items():
        util=max(v.get('utilizacao',0),v.get('utilizacao_flambagem',0),v.get('utilizacao_compressao',0))
        rows.append([escape(key).replace(r'\_', ' '),fmt(util,3),fmt(v['flecha_mm'],2) if 'flecha_mm' in v else '--',fmt(v['limite_flecha_mm'],2) if 'limite_flecha_mm' in v else '--'])
    table(R/'tabela_cama.tex','Item 17 — verificação da cama por elementos idealizados; utilização 1 é o limite.','tab:cama',['Caso','Utilização','Flecha [mm]','Limite [mm]'],rows,'Xrrr')
    print(json.dumps({'mass_kg':mass,'macros':len(values),'cost_rows':len(rows)}))


if __name__=='__main__':
    main()
