"""Substitui lacunas dos35itens por métodos técnicos e liga evidências reais.

Não é relatório final,aprovação humana ou substituição de teoria já desenvolvida.
"""
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]
BEGIN='<!-- execucao-integrada:inicio -->';END='<!-- execucao-integrada:fim -->'
METHODS={
1:('Balanço funcional E_inicial+E_FV=E_final+E_consumida+E_perdas+E_cortada.','BEV AuroraSolar para2p,arquiteturaB por interfaceDCexternaOEM. Serviços48V independentes;interface física não demonstrada.'),
2:('F_rol=Crr·m·g; cargas estáticas N_f+N_r=m·g.','PneusOEM preservados. Não especificar pressão,medida ou índice de carga sem ficha da varianteSK505.GG1.2;Crr é sensibilidade.'),
3:('ΔE_c=½m(v0²−vf²); F_desac=m·a; calor de atrito=demanda−resistências−regeneração.','Geometria representativa,partição por eixo e limites de aderência separados. Não atribuir frações regenerativas hipotéticas aoOEM.'),
4:('P=T·ω; F_roda=T·i·η_red/r; F_roda≤P·η_red/v.','205kW/410Nm são picos documentados,sem mapaOEM. Envelopes de engenharia não são curvas do fabricante.'),
5:('n_motor=60·i·v/(2πr); P_perdas=(1−η_red)·P_entrada.','Relações8/10/12 e eficiências sensibilizadas;redutorOEM permanece intacto. Relação real/óleo/volume não demonstrados.'),
6:('E_nom=N_módulos·E_módulo; E_disponível=E_nom·min(DoD,1−SOC_reserva).','Pack de tração110brutos/98úteis da mesma variante. Serviços3US5000=14,4kWh nominal,uso móvel/BMS/fixação ainda condicionados.'),
7:('V_carga=V_fonte−I·R; P_DC=V_carga·I; R=ρ(T)·L/A; P_Joule=I²R.','Resolver a raiz estável da carga de potência constante. Ampacidade instalada,terminais,I²t e corrente prospectiva real exigem dados não substituídos pela queda de tensão.'),
8:('P_FV≈P_STC·G_POA/1000·[1+γ(T_c−25°C)]·f_perdas; E=ΣP·Δt.','1540Wp documentados por2×380+2×390 e1600Wp portáteis,somenteparados/ângulos fixos. FamíliaPV e limitesMPPT específicos por cenário;Wp não são kWh.'),
9:('P_AC≤P_contínua(T); S_AC=V·I; P_AC=S_AC·FP; P_bateria≈P_AC/η+P_vazio.','220V60Hz configuráveis noGX. Comparador independente250/60teto+150/60portáteis não aprova MPPTcompartilhado nem saída48V paraHV.'),
10:('Q̇_perdas=P_entrada−P_saída; m·cp·dT/dt=Q̇_gerada−Q̇_retirada.','Separar motor,inversor e redutor. UA,vazão/eficiências não calibrados aoOEM devem ser faixas explícitas,sem dupla contagem de perdas.'),
11:('Q_v=Cd·A_eff·√(2gH·|ΔT|/T); 1/A_eff²=1/A_baixa²+1/A_alta².','Ventilação natural prioritária. Com vento0 eΔT0,modelo produz vazão0. CO2/vapor usam balanços de geração e renovação,sem prometer salubridade.'),
12:('P_calor,red=(1−η_red)P_entrada; fluxo de calor e lubrificação são requisitos distintos.','BEV não usa lubrificação de motor diesel. ÓleoOEM do redutor,grau/volume/intervalo não publicados permanecem desconhecidos;nenhuma substituição proposta.'),
13:('E_dia=ΣP_i·t_i+ΣE_ciclo·frequência; E_bat=E_AC/η_inv+E_DC/η_DC+E_vazio.','Método médio diárioDEC046 para duas pessoas;lavanderia ocasional,picos/simultaneidade em análise separada. Prioridades automáticas não fixam SOC/BMS arbitrários.'),
14:('R_r=m·g·x_CG/L; R_f=m·g−R_r; ΔR=m·a·h_CG/L; índice≈(t/2−|y_CG|)/h_CG.','Suspensão/pneusOEM inalterados. Índice quaseestático não fornece velocidade segura de curva ou homologação;limites por eixo/rigidez/curso desconhecidos.'),
15:('EI·d⁴u/dx⁴=q; ΣF=F_aplicada; Σ(r×F)=M_aplicado; σ_eq=√(σ_tração²+3τ²).','ChassiOEM é referência. FEM de trilhos/tiras e grupos de parafusos são modelos locais;sem inventar material/rigidez/ancoragens da carroceria.'),
16:('Envelope útil=dimensão interna−2·(isolamento+revestimento); colisãoAABB exige sobreposição positiva nos3eixos.','Carenagem/portas/vidros são envelopes estimados. Não confundir sólidos válidosSTEP com estanqueidade,fixação ou geometriasOEM verificadas.'),
17:('m=Σm_i; r_CG=Σ(m_i r_i)/m; todas as cotasCAD em metros.','Dois layouts e alternativas de teto;A tem acesso e circulação de estudo,B mantém falha de acesso documentada. Geometria comercial e folgas precisam revisão real.'),
18:('m_total=m_OEM+Σm_conversão+m_pessoas+m_bagagem+m_água; m_água é conservada entre reservatórios.','Partida100Ltotais:85Ltanque+15Lboiler. Cassete é o tanque negro,sem reservatório duplicado. CG/eixos são estimados,sem pesagem.'),
19:('∇·U=0; ρ(U·∇)U=−∇p+∇·τ_eff; Cd=F_D/(½ρA_refU_ref²).','RANS kOmegaSST com piso móvel e parede,3malhas equipadas. Relatar resíduos,histórico de força,y+ e variação de malha. GCI requer hipóteses não demonstradas;Cd permanece faixa condicional.'),
20:('F_rol=Crr·m·g em pista plana; P_rol=F_rol·v.','Crr0,008/0,012/0,016 é caixa de hipóteses,não ensaio de pneusOEM;variar massa e condição de uso mantendo pneus de fábrica.'),
21:('F_D=½ρ·Cd·A_ref·v_rel².','Vento externo0 implica v_rel=v_veículo. Usar a mesma área de normalização doCFD;limiteCd0,72 é sensibilidade conservadora,não valorOEM.'),
22:('P_roda=(F_D+F_rol)·v; P_bat=P_roda/η_tração+P_aux,OEM.','Auxiliar700W de estudo sensibilizado0/300/700/1500W somente em movimento. Serviços habitáveis vêm do banco48V e não entram na tração.'),
23:('N=ceil[E_dia·(autonomia_h/24)/(E_módulo·min(DoD,1−reserva)))].','Comparar24/48h semSol para ambas reservas. Capacidade nominal não é energia útil;110/98kWh da tração são conceitos distintos.'),
24:('C_ref,moeda=Σq_i·preço_i conhecido; total instalado não existe se faltam linhas/frete/tributos.','BOM separaEUR/USD/BRL,conversão e componentesOEM. Valores de lista não são cotação importada;preços desconhecidos continuamnull.'),
25:('Crédito_solar(t+Δt)=crédito_solar(t)+E_FV→HV−P_tração·Δt; crédito inicial0.','MILP de alocação por janela e partidas em grade,40/80km/h;serviços cíclicos separados. Uma sessão hipotética não demonstra interfaceOEM ou ótimo global.'),
26:('e(v)=P_bat(v)/v emkWh/km; rendimento espacial=1/e(v) emkm/kWh.','Avaliar40/80km/h constantes,plano,25°C/UR50/vento0,consumo habitável separado. Sensibilidade deCd/Crr/η/massa não equivale a previsão rodoviária.'),
27:('E_utilizável=(SOC_inicial−0,30)E_tração; ∫P(v)dt≤E_utilizável.','Principal100→30%,sensibilidade80→30%. No modelo planoP(v)=a·v+b·v³+P_aux é convexo;Jensen justifica velocidade constante no controle sem reposiçãoHV. Limite8h não é transferido doitem29.'),
28:('m·dv/dt=min(F_torque,F_potência,F_aderência)−F_resistiva.','Tração dianteira inclui transferência dinâmica de carga. Variante limitada90km/h não atinge100km/h;0–90 hipotético não é mediçãoOEM.'),
29:('E_inicial+E_FV=E_final+E_tração+E_serviços+E_perdas+E_cortada; SOCs separados.','7000km plano,ambosSOC100%,até8h/dia,sem recarga elétrica externa. DiaSãoCarlos21junho repetido é idealização. Grade não comprova ótimo global ou caminhoDCimplementável.'),
30:('ρc·∂T/∂t=∇·(k∇T)+J²ρ_el(T); ρ_el(T)=ρ20[1+α(T−20°C)].','Campos multidimensionais de cobre/isolamento e sensibilidade. CorrenteDC calculada não é RMSde fase;cabosHV permanecemOEM sem modificação.'),
31:('C_i·dT_i/dt=Σ(T_j−T_i)/R_ij+Q_solar,i; noCFD,empuxo≈ρ0gβ(T−T0).','Cabine fechada,parada,sem pessoas/AC;manhã→meiodia25°Cexternos. CFD3D é complemento de contorno congelado,nãoCHT matinal ou ensaio veicular.'),
32:('Q̇_AC=Q̇_condução+Q̇_solar+Q̇_metabólica+Q̇_infiltração+Q̇_interna.','33°Cexternos/25°Cinternos/1ocupante principal,2complementar,regime permanente. kWtérmico não é kWelétrico;6,2A e220V implicam1364VA,FP/partida e capacidade real ainda pendentes.'),
33:('ΔE_c=400mJ para30→10m/s; a=−4m/s²; ρcp∂T/∂t=∇·k∇T+Q̇_fricção.','Ensaio5s/inicial25°C,disco2Drz,atrito e regeneração limitada em hipóteses. Subtrair arrasto/rolamento.108km/h é condição prescrita de componente,acima do limitador do veículo.'),
34:('I=P_carga/V; Q̇_Joule=I²R_int; C_b·dT_b/dt=Q̇_Joule−UA(T_b−T_c).','20/80kW são ensaios térmicos, não potência solar. ModeloECM/múltiplos nós é parametrizado,com resistência/massa/troca sensibilizadas e sem curvaOEM inventada.'),
35:('Δp_bomba(Q)=Δp_circuito(Q); Q̇_trocado=ṁ·cp·(T_saida−T_entrada).','BombaBosch candidata e radiador2D resolvem circuito conceitual,não seleçãoOEM. Vazões/perdas/temperaturas e potência elétrica são conservadas;rede de glicol não é água potável.')}

SOURCES={1:['dec','oem_sk'],2:['oem_sk','hyp'],3:['oem_sk','hyp'],4:['oem_sk'],5:['oem_sk','hyp'],
6:['oem_sk','pylon','pylon_us_series2024','pylon_victron'],7:['multi_install','mppt_install','littelfuse_jlln','pylon_us_series2024'],8:['maxeon3_2022','mppt250_60','mppt150_60'],
9:['multi_gx','mppt250_60','mppt150_60','pylon_victron'],10:['oem_sk','hyp'],11:['hyp'],12:['oem_sk','hyp'],
13:['fridge','cooktop','washer','quick_boiler','freshwell_manual_2018'],14:['oem_sk','hyp'],15:['oem_sk','hyp'],
16:['oem_sk','history'],17:['oem_sk','maxeon3_2022'],18:['oem_sk','pylon','maxeon3_2022'],19:['cfd','hyp'],
20:['oem_sk','hyp'],21:['cfd','hyp'],22:['oem_sk','hyp'],23:['oem_sk','pylon','multi_gx'],
24:['oem_sk','victron_price_2026q2','cooktop'],25:['maxeon3_2022','hyp'],26:['cfd','hyp'],27:['oem_sk','hyp'],
28:['oem_sk','hyp'],29:['oem_sk','maxeon3_2022','pylon','venema','sungrow','hyp'],30:['multi_install','hyp'],
31:['openfoam_boussinesq','hyp'],32:['freshwell_manual_2018','webasto'],33:['hyp'],34:['oem_sk','hyp'],35:['hyp']}


def append_block(path,text):
    prior=path.read_text() if path.exists() else ''
    if BEGIN in prior:prior=prior[:prior.index(BEGIN)]+prior[prior.index(END)+len(END):]
    path.write_text(prior.rstrip()+'\n\n'+BEGIN+'\n'+text.rstrip()+'\n'+END+'\n')


def main():
    review=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/revisao_35_itens.json').read_text())
    records={x['item']:x for x in review['items']};c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());index=[]
    snapshot=ROOT/'entregas/integrado_maxeon1540/parametros_resolvidos.json';resolved=json.loads(snapshot.read_text())
    decisions=json.loads((ROOT/'entregas/etapa_pos_dec061/matriz_decisoes_61.json').read_text())

    with (ROOT/'metadata/itens.csv').open() as f:items=list(csv.DictReader(f))
    for item in items:
        n=int(item['numero']);folder=ROOT/item['pasta'];record=records[n];equation,method=METHODS[n]
        append_block(folder/'README.md','Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.')
        theory=folder/'teoria.md';old=theory.read_text()
        if 'A preencher com equações corretas e citações. Não inventar dados.' in old:
            old=old.replace('A preencher com equações corretas e citações. Não inventar dados.',equation)
            old=old.replace('Descrever método, condição de contorno e critérios de convergência (se aplicável).',method)
            old=old.replace('Identificar aproximações e sensibilidade das entradas.',record['remaining_limit'])
            theory.write_text(old)
        append_block(theory,f'Método técnico integrado: {equation}\n\n{method}\n\nEscopo: {record["remaining_limit"]}\n\nFonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.')
        evidence=ROOT/record['evidence'];hashval=hashlib.sha256(evidence.read_bytes()).hexdigest()
        result={'item':n,'owner':record['owner'],'requirement':record['requirement'],'model_equations':equation,'method_and_conditions':method,
            'status':record['status'],'executed':record['executed_or_reviewed'],'remaining_limit':record['remaining_limit'],
            'evidence':record['evidence'],'evidence_sha256':hashval,'human_approval':False,'physical_validation':False}
        relevant={x['decision'] for x in decisions if n in x['items']}
        parameter_values={key:value for key,value in resolved['parameters'].items() if relevant.intersection(value.get('decisions',[]))}
        (folder/'dados/parametros_execucao_integrada.json').write_text(json.dumps({
            'item':n,'canonical_source':'config/parametros_globais.yaml','canonical_revision':c['revision'],
            'derived_snapshot':str(snapshot.relative_to(ROOT)),'snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            'values':parameter_values,'editable_source':False,'physical_validation':False,
            'note':'Cópia derivada de entradas efetivamente resolvidas;editar apenas fonte canônica e reexecutar. Parâmetros de geometria/loads adicionais no snapshot,sem nova fonte de verdade.'},indent=2,ensure_ascii=False)+'\n')
        (folder/'resultados/execucao_integrada.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
        append_block(folder/'resultados/README.md',f'Execução integrada: `{record["evidence"]}`.\n\n{record["executed_or_reviewed"]}\n\nLimite: {record["remaining_limit"]}\n\nÍndice local: `execucao_integrada.json`;SHA256da evidência: `{hashval}`. Não aprovado fisicamente.')
        append_block(folder/'codigo/README.md','Reprodução integrada pelo repositório:\n\n```bash\nPYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar\nPYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente .venv/bin/python scripts/verificar_cenario_integrado.py\n```\n\nCFD e campos específicos preservam comandos em `docs/EXECUCAO_TECNICA02.md`;a cadeia integrada não substitui esses ensaios. Ver arquivos reais de evidência no índice local.')
        source_lines=[]
        for key in SOURCES[n]:
            src=c['sources'][key];url=src.get('url') or src.get('path')
            source_lines.append(f'- `{key}`: {url or src.get("kind","hipótese registrada")}; consulta/revisão: {src.get("accessed",src.get("date",src.get("version","ver YAML")))}. Origem: {src.get("kind","ver YAML")}.')
            if src.get('mirror'):source_lines.append(f'  Espelho original conferido: {src["mirror"]};SHA256 `{src.get("sha256")}`.')
        append_block(folder/'fontes.md','Fontes específicas da execução (não representam aprovação da instalação):\n\n'+'\n'.join(source_lines)+f'\n\nEvidência técnica: `{record["evidence"]}`. Condições/hipóteses constam no YAML;valoresOEM não publicados permanecem desconhecidos.')
        append_block(folder/'validacao.md',f'Revisão computacional registrada no índice `resultados/execucao_integrada.json`.\n\nLimitação remanescente: {record["remaining_limit"]}\n\nRevisão humana final: **PENDENTE**. Não houve instalação/ensaio físico,homologação ou aceite inferido por este gerador.')
        index.append({'item':n,'owner':record['owner'],'path':str((folder/'resultados/execucao_integrada.json').relative_to(ROOT)),'evidence_sha256':hashval})
    (ROOT/'entregas/indice_execucao_35.json').write_text(json.dumps({'items':sorted(index,key=lambda x:x['item']),'human_approvals':0,'physical_validation':False},indent=2,ensure_ascii=False)+'\n');print('35métodos/índices técnicos ligados a evidências reais;0aprovações.')


if __name__=='__main__':main()
