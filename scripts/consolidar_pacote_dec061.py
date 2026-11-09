"""Gera BOM, síntese acadêmica e lista única de aprovações a partir da execução."""
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/etapa_pos_dec061'


def prosa(text):
    """Espaçamento legível das etiquetas técnicas, preservando identificadores."""
    replacements={
        'autorizaçãoDEC061':'autorização DEC-061', 'arquiteturaBcomo':'arquitetura B como',
        'geometriaL3H2':'geometria L3H2', 'pneus/suspensãoOEM':'pneus e suspensão OEM',
        '220V60Hz':'220 V / 60 Hz', '220V/60Hz':'220 V / 60 Hz',
        '1540Wp':'1.540 Wp', '1600Wp':'1.600 Wp', '1350Wp':'1.350 Wp',
        '7000km':'7.000 km', '35itens':'35 itens', '61decisões':'61 decisões',
        '0aprovações':'0 aprovações', '48V':'48 V', '12V':'12 V', '24V':'24 V',
        '4250kg':'4.250 kg', '3500kg':'3.500 kg', '2790kg':'2.790 kg',
        '90km/h':'90 km/h', '40/80km/h':'40 / 80 km/h', '8h/dia':'8 h/dia',
        '100%nosdoisbancos':'100% nos dois bancos',
        'CFD3D':'CFD 3D', '3malhas':'3 malhas', 'modelosparametrizados':'modelos parametrizados',
        'nãodemonstrada':'não demonstrada', 'nãodemonstrado':'não demonstrado',
        'Nãohá':'Não há', 'fichafinal':'ficha final', 'inviávelsob':'inviável sob',
        'sistemastérmicos':'sistemas térmicos', 'semocupantes':'sem ocupantes',
        '3US5000':'3 × US5000', '14.4kWh':'14,4 kWh', '24h':'24 h', '48h':'48 h',
        '1kW':'1 kW', '50990EUR':'50.990 EUR', '119.1kg':'119,1 kg',
        'FreshWell3000':'FreshWell 3000', 'InverterSmart':'Inverter Smart',
        'semIVA':'sem IVA', 'semrecargas':'sem recargas', 'seminterface':'sem interface',
        'bancosindependentes':'bancos independentes', 'com1ocupante':'com 1 ocupante',
        'com2':'com 2', '1ocupante':'1 ocupante', '2ocupantes':'2 ocupantes',
    }
    import re
    protected=[]
    def hold(match):
        protected.append(match.group(0))
        return f'@@LITERAL{len(protected)-1}@@'
    text=re.sub(r'`[^`]*`|https?://[^\s)]+',hold,text)
    for a,b in replacements.items():
        text=text.replace(a,b)
    # URLs and code paths do not contain these punctuation sequences in this text.
    text=re.sub(r',(?=[A-Za-zÀ-ÿ])', ', ', text)
    text=re.sub(r';(?=\S)', '; ', text)
    for i,literal in enumerate(protected):
        text=text.replace(f'@@LITERAL{i}@@',literal)
    return text


def main():
    master=ROOT/'config/parametros_globais.yaml'
    cfg=yaml.safe_load(master.read_text())
    p={k:v['value'] for k,v in cfg['parameters'].items()}
    manifest=json.loads((OUT/'manifesto.json').read_text())
    if manifest['inputs_sha256']['config/parametros_globais.yaml']!=hashlib.sha256(master.read_bytes()).hexdigest():
        raise ValueError('Reexecute conciliar_dec061.py antes de consolidar')
    sources=cfg['sources']
    # These masses represent a provisional package, not a completed or legal assembly.
    components=cfg['bom_components']
    rows=[]
    for component in components:
        ident=component['id']
        model=p[component['model_parameter']] if 'model_parameter' in component else component['model']
        q=p[component['quantity_parameter']] if 'quantity_parameter' in component else component['quantity']
        mass=p[component['mass_parameter']] if 'mass_parameter' in component else component['unit_mass_kg']
        owner,source,scope,status=(component[k] for k in ['owner','source','scope','status'])
        url=sources[source].get('url','')
        if source=='history':url='config/'+('solar_proposta.yaml' if ident=='pv_teto' else 'layout_proposto.yaml' if ident=='pv_cabine' else 'solar_portatil_proposta.yaml' if ident=='pv_portatil' else 'equipamentos_interior.yaml' if ident=='cassete' else 'servicos_proposta.yaml')
        rows.append({'id':ident,'model':model,'quantity':q,'unit_mass_kg':mass,
            'known_line_mass_kg':q*mass if q is not None and mass is not None else None,
            'unit_reference_price':p[component['price_parameter']] if 'price_parameter' in component else component['unit_reference_price'],
            'currency':component['price_currency'],'source':url,
            'reference_date':component.get('price_date',component['reference_date']),
            'price_status':'referencia_semIVA_SK' if ident=='veiculo' else 'referencia_historica_tensao_preco_nao_confirmada' if ident=='cooktop' else 'sem_cotacao',
            'installed_price_brl':None,'tax_shipping_verified':False,'owner':owner,'scope':scope,'status':status,
            'dimensions_source':'config/parametros_globais.yaml ou fonte indicada; interfaces/folgasCAD pendentes'})
    with (OUT/'bom_rastreavel.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    known_added=sum(x['known_line_mass_kg'] or 0 for x in rows if x['scope']=='conversao')
    water_payload=sum(p['occupants_kg'])+p['baggage_kg']+p['water_clean_l']
    known_subtotal=p['oem_tare_kg']+known_added+water_payload
    mass_summary={'scenario':'pacote_provisorio_com_masses_parciais_nao_massa_montada',
        'known_added_conversion_kg':known_added,'occupants_baggage_water_kg':water_payload,
        'known_subtotal_kg':known_subtotal,'headroom_to_4250_before_missing_kg':p['oem_pbt_kg']-known_subtotal,
        'excess_over_3500_even_before_missing_kg':max(0,known_subtotal-3500),
        'actual_typical_mass_kg':None,'axle_loads_kg':None,'installed_total_brl':None,
        'missing_mass_ids':[x['id'] for x in rows if x['scope']=='conversao' and x['known_line_mass_kg'] is None],
        'excluded_oem_double_count':['motor','packHV','redutor','inversorHV','cabosHV','freios','arrefecimentoOEM'],
        'buffer_included':False,'water_in_boiler_is_part_of_100L':True}
    (OUT/'bom_massas_custos_resumo.json').write_text(json.dumps(mass_summary,ensure_ascii=False,indent=2)+'\n')
    # Each approval appears exactly once below. Prior approved principles are not reopened.
    choices=[
    ('A01','Variante OEM','SK505.GG1.2/4250kg × SK505.BG1.2/3500kg × BR a documentar','Manter SK505.GG1.2 como candidata integrada; não congelar homologação','Ficha única e maior capacidade de carga;3500kg já excede subtotal conhecido','oem_sk','P1/P4','Tara2790kg;limite90km/h;preço50990EUR semIVA. Eixos/importação e configuração final pendentes','B03; A02/A04/A10/A11','provisorio'),
    ('A02','Recarga DC direta ou buffer dedicado','DC direto × buffer exclusivo × controle sem recarga','Manter controle sem interface como referência; não instalar buffer. Comparação matemática preservada','Não existe equipamento/conjuntoOEM demonstrado para a potênciaFV; buffer não resolve protocolo','venema','P2/P5','Mínimos reais,custo,massa,isolamento e autorização nulos; mínimo1kW nos replays é hipótese','B01; libera missão física somente após evidência','nao_demonstrado_bloqueante'),
    ('A03','Alocação FV e MPPT compartilhado','Fixosserviços/portáteistração × inverso × comutaçãoflexível;1MPPT×múltiplosrastreadores','FV para serviços no controle; flexível apenas como estudo, sem hardware vencedor','A geração não pode ser duplicada; JA e EcoFlow têmcurvas/tensões distintas; cab190Wnão é string48V','history','P2/P5/P3','Topologia,comutação,Vocfrio/Vmpquente,mismatch e perdas precisamdemonstração; sem ponte entre bancos','B01/B05; A02/A11','nao_demonstrado'),
    ('A04','Autonomia e módulos de serviços','24h ×48h;reservas20%×30%;candidatoantigo10.24kWh×US5000modular','3US5000/14.4kWh como banco provisório24h;base48h comparar4/5módulos','3módulos cobrem consumo-base em ambas reservas; massa119.1kg; 48h amplia massa/volume','pylon','P2/P6/P1/P3','Uso veicular,vibração,fixação,BMS e compatibilidade ainda não demonstrados. Caso alto de consumo requer mais capacidade','B06; A05/A06/A07/A08/A09','provisorio_condicionado'),
    ('A05','Inversor de serviços','MultiPlusII48/5000/70-50 × InverterSmart48/5000','MultiPlusII ajustado220V60Hz provisoriamente','Preserva candidato existente;ambos4000W25°C/3700W40°C e ajustáveis210–245V50/60Hz. Smartdispensa carregadorAC','multi','P2','Vazio18Wvs20W;massas30vs28kg;eficiênciasmáximasnão são curvas. EntradaACnão usada na missão;partidas/proteções pendentes','B06; A04/A06/A07/A08/A09','provisorio_condicionado'),
    ('A06','Climatização','FreshWell3000/2.7kWsob banco × CoolTopTrail35/3.5kWde teto × outra compatível','Não congelar modelo. FreshWell segue referência dimensional;Webasto50Hz/teto rejeitado para baseline','Comparação comercial maior foi feita, mas nenhuma compatibilidade220V60Hz sob banco demonstrada','freshwell','P6/P2/P3','Carga térmica1/2p e margens calculadas por rede equivalente;faltamcurvas33°C,dutos,picos e alimentação220V','B07/B08; A04/A05/A10/A11','nao_demonstrado'),
    ('A07','Geladeira AC','MideaMRC10B2 × sucessorMDRD142FGD303 × antigoNRXDCdescartado como principal','MRC10B2/93L220V60Hz provisório','Manual/página documentam alimentação,massa20.8kg e14.1kWh/mês; não misturar18kg do sucessor','fridge','P6/P2/P3','0.47kWh/dreferência antes perdas;testar calor/instalação×1–2;partida,retenção,ventilação e disponibilidade pendentes','B06; A04/A05/A10','provisorio'),
    ('A08','Cozinha e lavanderia','IE3TP1zona × outros1zona;LG11/7kg × compacta documentada','IE3TP220V60Hz2kW e LGCV9011WC4A como candidatos;lavanderia1vez/semana','Cooktopmanual rastreável;LGjá noCAD; secagem não foi omitida do balanço','cooktop','P6/P2/P3','Cooktop2.3kg;LG73kg,68.8L/ciclo e secagem1–4kWh hipotética. Uso da lavanderia quase enche tanque cinza sozinho','B06/B10; A04/A05/A10','provisorio_condicionado'),
    ('A09','Boiler e rede potável','QuickB31505S × ElgenaKB6;Shurflo12V×24V;trecho10×13mm','Quick15L500W como candidato condicionado;Shurflo4008-101-E65/12V provisória;comparar tubulações','CurvaShurflo tem aplicaçãoRV;Quick220Vpressurizado documentado. ElgenaKB6max0.8bar incompatível com rede pressurizada','potable_pump','P6/P2/P3','Boiler7kgvazio +água dentro100L;manter sem ligaçãoarrefecimentoOEM. Quick60Hz/veicular e rotas/proteções/expansão/alívio pendentes','B10; A04/A05/A10/A12','provisorio_condicionado'),
    ('A10','Layout e isolamento','Cama fixa existente × conversível;isolamento32mm × espessuras alternativas','Conservar cama fixa e AFArmaflex32mm provisórios até comparação cotada','AproveitaCAD preexistente; não afirma que cama conversível foi comparada emCAD','history','P3/P6/P1','Folgas,ergonomia,compartimentos,áreas,vidros,fogo/umidade,manutenção e segundoestudo faltam','B08/B09; A04/A06/A07/A08/A09','provisorio_com_comparacao_incompleta'),
    ('A11','Módulos e ocupação do teto','3JA450+190Wcabine × novo arranjo comercial1540Wp comprovável','Manter meta1540Wp; arranjoexistente apenas referência. Crédito48Vde1350Wp é cenário limitado','190Wdebaixa tensão ainda sem caminho48V; não reduzir silenciosamente a meta','history','P3/P2/P5/P1','Falta duasocupações/ancoragens/sombras;BOMconta massa190Wmasreplaynão promete aproveitamento48V','B05/B09; A03/A06/A10','condicionado_nao_validado'),
    ('A12','Barramento DC secundário','12V ×24V com conversor desde48V','12V provisório por bomba/comandos;24V permanece comparação','Mesma carga/cabo em24V reduz perdasJoule para1/4;conversor e catálogo podem alterar vencedor','potable_pump','P2/P6','CurvaShurflo12V não pode ser transplantada para24V;vazio/eficiência de conversor e corrente total pendentes','B06; A09','provisorio_condicionado'),
    ('A13','Política e reservas da missão','08–16 × horário alternativo00–08 × otimização futura;10/20×20/30','Conservar ambos conjuntos e horários como comparação; nenhum ótimo global escolhido','Novos replays coerentes permitem avaliar tendências;horárioalternativo não é políticaotimizadademonstrada','hyp','P5/P2/P4','Dias,soc e conclusão mudam com consumo,interface e clima;somente hipóteses de dia-tipo idealizado','B01/B04; A02/A03/A04/A11','em_comparacao'),
    ('A14','Parâmetros físicos e validação','FaixaCd × Cdconvergido;massatípica ×PBT;modelostérmicosrepresentativos ×dadosOEM','Manter faixas e bloqueios; não aprovarCd,CG,curvasougeometriaOEM ausentes','3malhas não independentes;campostérmicos reais não validam seusparâmetros;100km/hnãoatingívelna4250','cfd','P1/P3/P4/P6/P7','ExigeCAD/massa,eixos,FEA,CFD3Dcabine,curvasmotor,propriedadescabos/freios/bateria e revisão cruzada','B03/B08/B09/B11; libera resultados finais poritem','nao_demonstrado_em_partes'),
    ('A15','Proteções, controle e monitoramento','Indicadores comerciais e atuadores documentados × integração a definir','Manter monitoramento básico comercial e shedding automático como requisitos, sem central própria','DEC047/056 já aprovadas; implementação e patamares ainda dependemBMS e hardware','multi','P2/P6/P7','Circuitos,DR/PE,curto,fusíveis,contatores,falhas e plano de ensaios ainda precisam memorial; nenhum ensaio físico realizado','B06; A04/A05/A12','nao_demonstrado'),
    ('A16','Orçamento instalado','AquisiçãoSK/importação × aquisiçãoBRdocumentada;conversão+montagem+engenharia+encargos','BOM aberta com preços desconhecidosnull; não aprovar total numérico','Somente referências parciais,sem câmbio/frete/tributos e várias massas/componentes faltantes','oem_sk','P1','Motor,packHV,freios e arrefecimentoOEM não são somados novamente. Alternativas não se somam entre si','B12; depende deA01–A15','nao_demonstrado')]
    doc='# Aprovações finais pendentes — lista única pós-DEC061\n\n**Nenhuma aprovação final está sendo solicitada agora para suprir falta de evidência.** Esta é a lista consolidada para revisão ao fechar os estudos. A autorizaçãoDEC061 permite as recomendações provisórias abaixo; não as transforma em aprovadas.\n\nJá aprovados anteriormente e preservados: arquiteturaBcomo direção, bancos independentes,geometriaL3H2,pneus/suspensãoOEM,metas1540+1600Wp,portáteis só parados com ângulo fixo por parada,220V60Hz,média diária de serviços,gerenciamento automático,ventilação natural prioritária,A/Csob banco prioritário,monitoramento básico,água100/70/cassete~20L,7000kmplano,ambosSOC100% e≤8h/dia sem carga externa. **Não reabrir essas decisões para forçar viabilidade.**\n\n'
    for ident,title,options,recommend,why,source,owner,impact,deps,status in choices:
        url=sources[source].get('url')
        reference=f'[{source}]({url})' if url else f'`config/parametros_globais.yaml:sources.{source}`'
        doc+=f'## {ident} — {title}\n\n- **Estado / responsável:** {status}; {owner}.\n- **Opções:** {options}.\n- **Recomendação provisória:** {recommend}.\n- **Justificativa e fonte:** {why}. {reference}.\n- **Impactos e incertezas:** {impact}.\n- **Dependências:** {deps}.\n- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.\n\n'
    (ROOT/'docs/APROVACOES_FINAIS_PENDENTES.md').write_text(prosa(doc).rstrip()+'\n')
    missions=json.loads((OUT/'missoes_7000km.json').read_text())
    successes=[m for m in missions if m['status']=='chegada_condicional']
    controls=[m for m in missions if m['mode']=='sem_interface']
    cabin=json.loads((OUT/'cabine_31_32_reexecutada.json').read_text())
    tr=json.loads((OUT/'itens25_26_27.json').read_text())['i26']
    report=f'''# Integração pós-DEC061 — execução de 09/11/2026

**A interface solar/DC não está demonstrada. A missão física não foi comprovada. Os 35 itens têm trabalhos iniciados e nenhum tem aprovação humana final.** As recomendações comerciais são provisórias.

## Arquivos e histórico

O registro original foi localizado em Downloads e incorporado, sem alteração de bytes, em `docs/decisoes_motorhome_2026-10-28.md`. Seu SHA-256 é `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`. A revisão de 28/10 e a saída anterior estão em `entregas/etapa_2026-10-28_rota_real/`. O CAD, visualizador, PDF parcial, três malhas CFD e resultados térmicos anteriores permanecem preservados.

A fonte ativa é `config/parametros_globais.yaml`, revisão `1.0.0-pos-DEC061`, com unidade, origem, data, responsável, confiança e estado por parâmetro. O estado anterior pode ser recuperado no commit `2ef84f67c3aa820633b0565e92c0a23ea810302b`. A migração e seus impactos estão em `docs/decisoes.md`.

`config/registro_cenarios.yaml` separa o que é histórico dos modelos constitutivos reutilizados. Quatro executores antigos exigem `--historico`: interface de carga AC, agenda portátil, construção de viagem e rota real. Isso permite reproduzir métodos anteriores, sem promovê-los à arquitetura B. O caminho via energia armazenada nos serviços foi retirado da proposta elétrica vigente.

Entregas principais:

- [Matriz das 61 decisões](MATRIZ_DECISOES_61.md), com parâmetros, evidências, itens, responsáveis e pendências.
- [Estado dos 35 itens](REVISAO_35_ITENS.md), com inventário de arquivos por item no JSON desta etapa.
- [Bloqueios técnicos](BLOQUEIOS_POS_DEC061.md), [plano P1–P7](PLANO_EXECUCAO_POS_DEC061.md) e [diagramas funcionais](ARQUITETURA_POS_DEC061.md).
- [Lista única de aprovações finais](APROVACOES_FINAIS_PENDENTES.md), com 16 escolhas, opções, recomendações, fontes, impactos e dependências.
- [BOM rastreável](../entregas/etapa_pos_dec061/bom_rastreavel.csv), com 26 linhas. Preço desconhecido fica vazio; não se soma EUR a BRL nem se inventa total instalado.

## Resultados numéricos para o memorial

O consumo-base dos serviços é **7,229 kWh/dia na bateria**, incluindo geladeira AC, indução, climatização intermitente, boiler, lavagem e secagem ocasionais, cargas DC e perdas. As horas de uso e várias energias continuam hipóteses explícitas. A secagem não tem dado comercial confirmado; foi sensibilizada em 1–4 kWh por ciclo, com frequência de um ciclo semanal.

O arquivo `servicos_24_48h.csv` compara consumo mínimo, base e máximo, reservas de 20% e 30%, e autonomias sem Sol de 24 h e 48 h. No caso-base, 24 h exigem dois módulos US5000 com reserva de 20%, ou três com 30%; 48 h exigem quatro ou cinco. A recomendação de trabalho é **três módulos, 14,4 kWh e 119,1 kg**, permitindo comparar as duas reservas com o mesmo banco. Uso veicular, fixação, BMS, compatibilidade e picos ainda não estão demonstrados. Esse banco não atende automaticamente ao caso de consumo alto.

A BOM provisória contém **{known_added:.1f} kg de conversão conhecida**. Com 2.790 kg OEM e 320 kg de ocupantes, bagagem e água, o subtotal é **{known_subtotal:.1f} kg**, ainda sem móveis, isolamento, suportes, MPPT, cabos, proteções e outras massas. Restam {4250-known_subtotal:.1f} kg até o PBT de 4.250 kg antes desses faltantes. O mesmo pacote excede 3.500 kg em {max(0,known_subtotal-3500):.1f} kg. Não se trata de massa típica completa nem de aprovação por eixo. A água do boiler e do sanitário integra o balanço dos 100 L; motor, pack HV e demais componentes OEM não são somados novamente.

O consumo de tração abaixo usa percurso plano, sem serviços, Cd de 0,62488, Crr de 0,012, densidade de 1,1 kg/m³ e eficiência de 0,90, todos como parâmetros provisórios:

|Massa de estudo|Velocidade|Energia na bateria|Distância por energia|
|---|---|---|---|
'''
    for row in tr:
        report+=f"|{row['mass_kg']} kg|{row['speed_kmh']} km/h|{row['kwh_km']:.3f} kWh/km|{row['km_kwh']:.2f} km/kWh|\n"
    report+=f'''
Foram calculados **972 pontos** variando Cd, área, massa, Crr, densidade e eficiência. A massa de 3.500 kg é apenas um ponto de sensibilidade; 4.250 kg é o teto de PBT candidato. Não se apresentou nenhum deles como massa operacional típica validada. As três malhas CFD anteriores não demonstram independência: a variação final de Cd é 7,07%, sem camadas e y+ verificados. A faixa observada não é intervalo de confiança ou erro físico quantificado.

Foram executados **56 replays** de 7.000 km, com percurso plano, velocidades constantes de 40/80 km/h, dia-tipo de São Carlos em 21/06 repetido, SOC inicial de 100% nos dois bancos, até oito horas de direção por dia e nenhuma recarga elétrica externa. Os {len(controls)} controles sem interface interrompem por reserva de tração. Há {len(successes)} chegadas condicionais, com mínimo de carregamento de **1 kW hipotético**, nunca atribuído ao OEM. O erro máximo de fechamento energético fica abaixo de 10⁻⁶ kWh. As séries completas e os diários estão em `entregas/etapa_pos_dec061/`.

A comparação de horários cobre 08–16 e 00–08. A segunda janela é uma alternativa, não uma política otimizada demonstrada. Os dias calculados não são previsão meteorológica nem tempo mínimo global. Os painéis portáteis só geram nos períodos estacionados planejados, descontando montagem/desmontagem, com orientação e inclinação fixas em cada parada. Os 190 W de baixa tensão do arranjo histórico não são creditados ao banco de 48 V sem conversão comprovada: o replay usa a string principal de 1.350 Wp e mantém a meta de 1.540 Wp em aberto, sem reduzi-la como decisão.

Há **36 comparações** de DC direta versus buffer dedicado, com mínimos hipotéticos de 0,5/1/2/3/5/10 kW e buffers de 0/2/5 kWh inicialmente vazios. Esses estados não recebem energia da bateria de serviços. O despacho tem resolução de 15 minutos, que não representa tempo mínimo de sessão OEM. O resultado demonstra conservação sob hipóteses, sem inventar carregador compatível ou instalar banco extra.

I25 permanece sem autonomia solar fisicamente demonstrada. No controle, o crédito de FV à tração é zero. I26 separa o consumo de tração dos serviços. I27 mantém 100%→30% como principal e 80%→30% como sensibilidade no cálculo sem reposição solar, sem alegar otimização global. A reserva final de 30% não foi imposta ao item 29.

I30 reutiliza o solver de volumes finitos r–theta para cabos de serviços de 70/95 mm², corrente de 102,17 A e três malhas; os campos espaciais e resíduos estão salvos. Geometria, propriedades e contornos são estimados, sem certificação de bitola ou proteção. O enunciado pede cabos do motor; a DEC-026 prioriza os serviços de 48 V. A referência HV anterior foi preservada e essa diferença de escopo continua explícita.

I33 reutiliza o solver r–z com a potência por atrito após descontar arrasto, rolamento e regeneração mecanicamente limitada a 0/40/80 kW. Há comparação de massa, malha e passo temporal. As curvas de regeneração, aceitação no pack, geometria, materiais e repartição OEM continuam pendentes. O ensaio de 30 m/s (108 km/h) foi preservado como requisito acadêmico do componente, acima do limitador de 90 km/h da candidata; não se alega que essa velocidade seja atingível pelo veículo limitado.

I31 foi reexecutado com cabine fechada, sem ocupantes ou A/C: a rede térmica equivalente estima **{cabin['i31_noon_c']:.2f} °C ao meio-dia**. O CFD 3D de convecção natural ainda não foi executado. I32 estima **{cabin['i32'][0]['cooling_required_w']/1000:.3f} kW térmicos com um ocupante** e **{cabin['i32'][1]['cooling_required_w']/1000:.3f} kW com dois**, a 33 °C externos e 25 °C internos. A vazão exterior de 30 m³/h é hipótese do dimensionamento, sem prova de ventilação natural com vento nulo, e não foi aplicada ao ensaio fechado de I31. Falta equipamento sob banco compatível com 220 V/60 Hz e com a capacidade requerida sob incerteza.

A triagem potável é nova e distinta de `hidraulica_proposta.yaml`, que modela água/glicol do arrefecimento. Ela compara um trecho crítico hipotético de 10/13 mm com a curva documentada da bomba Shurflo de 12 V. Os pontos calculados são próximos de 5,47/5,57 L/min; materiais, rotas, pressão admissível, conexões e proteções ainda exigem validação. Com consumo hipotético de 60 L/dia, os 100 L durariam 1,67 dias sem lavanderia. Um ciclo de 68,8 L quase enche sozinho o tanque cinza de 70 L. As paradas sanitárias ainda não estão completamente integradas ao replay energético.

Também foram calculadas comparações de cabos em 12/24 V e sensibilidade do indicador lateral com alturas e deslocamentos hipotéticos do CG. Esses cálculos não demonstram segurança dinâmica, eixo admissível, curso de suspensão ou homologação. Os ensaios térmicos de bateria de 20/80 kW permanecem modelos parametrizados anteriores, sem nova validação OEM e sem representar potências solares disponíveis.

## Parecer da interface DC

A [ficha Fiat SK](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf) documenta CCS2 e potência DC máxima, mas não o mínimo de sessão solar nem a autorização para um equipamento proposto. O [relato primário 4x4electric/Venema](https://4x4electric.com/charging-technique/) e seu teste de 2022 dizem respeito a outro conjunto. Seus 30 kW máximos e 10 kWp de painéis não são mínimos do E-Ducato.

O [Sungrow IDC30E](https://uk.sungrowpower.com/upload/file/20221215/EN%20FS%20IDC30E%20DC%20Charger%20Factsheet.pdf) informa ajuste até 1 kW na FAQ, mas sua alimentação é AC trifásica de 400 V/50 Hz. Isso não comprova a arquitetura direta FV/DC escolhida. Não se propõe alimentá-lo pela bateria de serviços. A [página brasileira do Ducato](https://ducato.fiat.com.br/) apresenta versões diesel; não se transplantaram seus preços ou especificações para o E-Ducato.

**DC direta: não demonstrada. Buffer dedicado: não demonstrado e não instalado. Caminho via armazenamento dos serviços: inviável sob DEC-020.** Falta documentação de tensão, corrente e potência mínimas, comunicação, isolamento, proteções, resposta à intermitência e autorização/compatibilidade do conjunto exato. Se o mínimo real exceder a potência disponível, o cenário direto será inviável nessa condição, sem inferir impossibilidade universal da arquitetura B.

## Reprodução e verificações

Execute os comandos do [plano P1–P7](PLANO_EXECUCAO_POS_DEC061.md). Os scripts numéricos, consolidação e verificação têm manifestos próprios. Resultados de testes e auditorias estão em `output/`.

A suíte passou em **197 testes**, o Ruff passou e a estrutura dos 35 itens foi conferida. A verificação atual checa as 61 decisões, 15 hashes de entrada e 138 saídas numéricas, além do pacote documental. A verificação histórica conferiu os 124 hashes da entrega antiga, mas apontou uma divergência de proveniência em `resumo_freios.json` porque o código dos freios mudou. O artefato e o hash antigos foram preservados; não se ocultou a desatualização.

Ainda faltam a interface DC autorizada, massa e limites por eixo completos, mapas OEM, segundo layout cotado, duas ocupações finais de teto, ancoragens/FEA críticas, CFD convergido, CFD 3D da cabine, projeto elétrico e automação finais, logística sanitária completa e orçamento instalado. Essas pendências estão atribuídas por responsável e não foram convertidas em aprovações.
'''
    (ROOT/'docs/INTEGRACAO_POS_DEC061.md').write_text(report)
    # Supplemental manifest never changes the numerical manifest or previous results.
    generated=['bom_rastreavel.csv','bom_massas_custos_resumo.json']
    supplement={'generator':'scripts/consolidar_pacote_dec061.py',
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'canonical_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),
        'inputs_numerical_manifest_sha256':hashlib.sha256((OUT/'manifesto.json').read_bytes()).hexdigest(),
        'files_sha256':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in generated},
        'documents_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in [
            'docs/INTEGRACAO_POS_DEC061.md','docs/APROVACOES_FINAIS_PENDENTES.md',
            'docs/BLOQUEIOS_POS_DEC061.md','docs/PLANO_EXECUCAO_POS_DEC061.md',
            'docs/ARQUITETURA_POS_DEC061.md','docs/MATRIZ_DECISOES_61.md','docs/REVISAO_35_ITENS.md']}}
    (OUT/'manifesto_pacote.json').write_text(json.dumps(supplement,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'approvals':len(choices),'bom_lines':len(rows),'known_subtotal_kg':known_subtotal,
                      'conditional_arrivals':len(successes),'installed_total_brl':None},indent=2))


if __name__=='__main__':
    main()
