"""ConciliaDEC001–061 com evidências atuais,sem alterar o registro ou a matriz histórica."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]
SCENARIO = 'maxeon1560_independente'
CURRENT = 'entregas/integrado_maxeon1560'
# A revisão antiga fornece somente a associação item/responsável, não o estado atual.
LIMITS = {
    'P1': 'Massa/CG estimados, não pesagem; limites por eixo, soldas, bases e ancoragens OEM não validados. Freios e regeneração são modelos; custo é estimativa, não cotação instalada.',
    'P2': 'Bancos independentes e HV OEM preservados; CCS2, alocação FV, BMS/atuadores, ampacidade e I²t não demonstrados. 185 mm² não atende pico contínuo no cofre; limiares SOC de hardware permanecem null.',
    'P3': 'CAD de trabalho não é CAD OEM. Comparação com/sem painéis+deck executada, mas sem independência de malha nem validação experimental; curvatura, cargas e apoios reais pendentes.',
    'P4': 'Curva, rotação máxima, perdas e potência contínua OEM não demonstradas; Cr=0,012 e eficiência/aderência são hipóteses. 0–100 não é desempenho operacional da variante limitada a 90 km/h.',
    'P5': '1560 Wp fixos +1600 Wp portáteis só parado. I29: 7000 km, até 8 h/dia, sem recarga externa; 214,755556 dias é chegada condicional na busca finita, não ótimo global. I27 termina em SOC30% sem reposição solar. Piso CC 0,38 kW é hipótese, não mínimo de equipamento validado.',
    'P6': 'Layout A/cama fixa e FreshWell com proteção solar estacionada são provisórios; IAC, capacidade a 33/25 °C, revisão/placa, partida, proteção e instalação não validados. Perfil horário é hipótese; missão principal usa média diária.',
    'P7': '486 casos da bateria são ECM de dois nós, não pack OEM calibrado; 20/80 kW não são potência FV. UA/vazão/chiller são requisitos condicionais, não peças instaladas ou ensaio físico.',
}
# Estudos independentes de Wp preservam a origem antiga, com complemento atual explícito.
ITEM_EVIDENCE = {
    19: 'entregas/aero_equipado1540/comparacao_deck/resumo.json',
    24: f'{CURRENT}/i24_custo_brl/resumo.json',
    29: f'{CURRENT}/i29_fechamento/resumo.json',
    30: f'{CURRENT}/i30_corrente_maxima/resumo.json',
    32: f'{CURRENT}/i32_protecao_solar/resumo.json',
    34: f'{CURRENT}/mecanica_termica/I34_sensibilidades.csv',
    35: 'relatorio/dados_termicos/resumo.json',
}


def current_evidence(item):
    path = ITEM_EVIDENCE.get(item['item'], item['evidence'].replace(
        'entregas/integrado_maxeon1540', CURRENT))
    if not (ROOT / path).is_file():
        raise FileNotFoundError(path)
    return path


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    if SCENARIO not in c['development']['integrated_scenarios']:
        raise ValueError('Cenário da matriz ausente da fonte canônica')
    if hashlib.sha256((ROOT/c['decision_record']).read_bytes()).hexdigest() != c['sources']['dec']['sha256']:
        raise ValueError('Registro original de decisões foi alterado')
    old=json.loads((ROOT/'entregas/etapa_pos_dec061/matriz_decisoes_61.json').read_text())
    review=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/revisao_35_itens.json').read_text());items={r['item']:r for r in review['items']}
    special={
        1:('nao_demonstrado','RecargaB escolhida;CCS2/máxima não comprovam mínimos/handshake/autorização. Via serviços48V descartada.',['entregas/integrado_maxeon1560/buffer_comercial/resumo.json']),
        3:('integrado_condicional','1560WpMaxeon+1600Wpportátil integrados;curvatura/apoios e alocação elétrica não demonstrados.',['entregas/integrado_maxeon1560/solar/resumo.json']),
        5:('comparacao_executada','24h2/3módulos;48h4/5módulos para reservas20/30%. CAD e suporte completo comparados,sem capacidade final aprovada.',['entregas/integrado_maxeon1560/bancos_24_48_cad/resumo.json']),
        20:('restricao_preservada','Nenhuma transferência de energia armazenada entre serviços/tração;buffers apenas dedicados emcomparação.',['entregas/integrado_maxeon1560/buffer_comercial/resumo.json']),
        23:('convergencia_fisica_nao_demonstrada','Cd com/sem painéis+deck:0,62153633/0,55548590; convergência oscilatória, sem GCI/independência de malha nem validação experimental.',['entregas/aero_equipado1540/comparacao_deck/resumo.json']),
        35:('fonte_unica_implementada','YAMLúnico com cenário nomeado;resolvedJSON é saída derivada,hashes por executor e manifesto verificado.',['entregas/integrado_maxeon1560/parametros_resolvidos.json']),
        42:('comparacao_energetica_executada','Comparações de recarga direta/buffer dedicado preservadas; buffer não instalado, capacidades/massas são hipóteses e a interface não foi validada.',['entregas/integrado_maxeon1560/buffer_comercial/resumo.json']),
        46:('media_diaria_integrada','MédiaDEC046 usada;energia,picos e partidas distintos. Fontes não medem hábitos;incertezas não escondidas.',['entregas/integrado_maxeon1560/prioridades_servicos/resumo.json']),
        47:('controle_numerico_condicionado','72autonomias com prioridades e orçamento previsto,sem escolher patamaresSOCBMS;atuadores não instalados.',['entregas/integrado_maxeon1560/prioridades_servicos/resumo.json']),
        54:('comparacao_sem_topologia_aprovada','72mismatch compartilhados;controleindependente250/60+150/60 executado como comparação,sem alterar escolha de estudo prioritário.',['entregas/desenvolvimento_2026-11-09/teto_maxeon/resumo.json']),
        61:('autonomia_aplicada_sem_aceite_final','Autonomia técnica provisória preservada; pareceres acadêmicos incorporados não constituem aceite final de engenharia ou validação física.',['docs/RETOMADA_CURTA.md', 'docs/DECISOES_VIGENTES_P1_P7.md'])}
    rows=[]
    for prior in old:
        number=int(prior['decision'].split('-')[1]);decision=prior['decision']
        keys=[k for k,v in c['parameters'].items() if decision in v.get('decisions',[])]
        evidence=sorted({current_evidence(items[i]) for i in prior['items']})
        status='modelos_executados_validacao_condicionada';pending='; '.join(LIMITS[owner] for owner in sorted({items[i]['owner'] for i in prior['items']}))
        if number in special:
            status,decision_note,extra=special[number];pending=decision_note+' '+pending;evidence+=extra
        # Append core record plus exact original section hash for immutability.
        for name in evidence:
            if not (ROOT/name).is_file():raise FileNotFoundError(name)
        rows.append({'decision':decision,'title':prior['title'],'items':prior['items'],'lead':prior['lead'],
            'owners':sorted({items[i]['owner'] for i in prior['items']}),'parameter_keys':keys,
            'shared_structures':['development.integrated_scenarios','loads','sources'],'status':status,'pending':pending,
            'original_section_sha256':prior['section_sha256'],
            'evidence':[{'path':x,'sha256':hashlib.sha256((ROOT/x).read_bytes()).hexdigest()} for x in sorted(set(evidence))],
            'human_approval':False, 'human_approval_scope':'aceite final de engenharia, não deliberação histórica ou parecer acadêmico'})
    dest=ROOT/'entregas/matriz_decisoes_integrada_61.json';dest.write_text(json.dumps({'canonical_revision':c['revision'],'scenario':SCENARIO,'review_date':'2026-11-26','configuration_sha256':hashlib.sha256((ROOT/'config/parametros_globais.yaml').read_bytes()).hexdigest(),'decision_record_sha256':hashlib.sha256((ROOT/c['decision_record']).read_bytes()).hexdigest(),'decisions':rows,'human_approvals':0,'human_approval_scope':'aceite final de engenharia; deliberações históricas preservadas'},indent=2,ensure_ascii=False)+'\n')
    lines=['# MatrizDEC001–061 integrada','',
        'Reconciliada em 26/11/2026 por `scripts/atualizar_matriz_decisoes_integrada.py`, cenário `maxeon1560_independente`. **Leia as [decisões principais por área](DECISOES_VIGENTES_P1_P7.md)**. O [registro original](decisoes_motorhome_2026-10-28.md) e os hashes de suas 61 seções permanecem intactos. Títulos e vínculos originais são históricos; estado, evidências e pendências abaixo refletem a revisão vigente. Métodos/deliberações aprovados e pareceres acadêmicos não equivalem a aceite final de engenharia. Fonte única: YAML canônico; JSON resolvido é saída derivada. Estudos de CFD/cabine/ancoragens independentes de Wp mantêm sua origem explícita; 1540 no caminho do CFD não significa cenário energético ativo.','',
        '|Decisão|Parâmetros compartilhados|Itens / responsável|Estado / evidência|Pendência de validação|','|---|---|---|---|---|']
    for r in rows:
        short=', '.join(r['parameter_keys']) or 'loads/development/sources;verJSONintegrado'
        links=';'.join(f'[{Path(x["path"]).name}](../{x["path"]})' for x in r['evidence'])
        lines.append(f'|{r["decision"]} — {r["title"]}|{short}|{r["items"]}/{r["lead"]} interfaces{r["owners"]}|{r["status"]};{links}|{r["pending"]}|')
    (ROOT/'docs/MATRIZ_DECISOES_61.md').write_text('\n'.join(lines)+'\n');print('61decisões ligadas a parâmetros/evidências atuais;registro original preservado.')


if __name__=='__main__':main()
