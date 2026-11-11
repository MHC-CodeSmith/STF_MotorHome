"""ConciliaDEC001–061 com evidências atuais,sem alterar o registro ou a matriz histórica."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    old=json.loads((ROOT/'entregas/etapa_pos_dec061/matriz_decisoes_61.json').read_text())
    review=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/revisao_35_itens.json').read_text());items={r['item']:r for r in review['items']}
    special={
        1:('nao_demonstrado','RecargaB escolhida;CCS2/máxima não comprovam mínimos/handshake/autorização. Via serviços48V descartada.',['entregas/integrado_maxeon1540/buffer_comercial/resumo.json']),
        3:('integrado_condicional','1540WpMaxeon+1600Wpportátil integrados;curvatura/apoios e alocação elétrica não demonstrados.',['entregas/integrado_maxeon1540/solar/resumo.json']),
        5:('comparacao_executada','24h2/3módulos;48h4/5módulos para reservas20/30%. CAD e suporte completo comparados,sem capacidade final aprovada.',['entregas/integrado_maxeon1540/bancos_24_48_cad/resumo.json']),
        20:('restricao_preservada','Nenhuma transferência de energia armazenada entre serviços/tração;buffers apenas dedicados emcomparação.',['entregas/integrado_maxeon1540/buffer_comercial/resumo.json']),
        23:('convergencia_fisica_nao_demonstrada','TrêsCFDequipados convergem resíduos,masCdvaria5.23% na última dupla. SemGCI/Cddefinitivo;faixa até0.72 propagada.',['entregas/aero_equipado1540/incerteza_observada.json']),
        35:('fonte_unica_implementada','YAMLúnico com cenário nomeado;resolvedJSON é saída derivada,hashes por executor e manifesto verificado.',['entregas/integrado_maxeon1540/parametros_resolvidos.json']),
        42:('comparacao_energetica_executada','36DCdiários/120missões+32buffercomercial dedicado;capacidade/massa explicitadas,sem instalar buffer ou validar interface.',['entregas/integrado_maxeon1540/buffer_comercial/resumo.json']),
        46:('media_diaria_integrada','MédiaDEC046 usada;energia,picos e partidas distintos. Fontes não medem hábitos;incertezas não escondidas.',['entregas/integrado_maxeon1540/prioridades_servicos/resumo.json']),
        47:('controle_numerico_condicionado','72autonomias com prioridades e orçamento previsto,sem escolher patamaresSOCBMS;atuadores não instalados.',['entregas/integrado_maxeon1540/prioridades_servicos/resumo.json']),
        54:('comparacao_sem_topologia_aprovada','72mismatch compartilhados;controleindependente250/60+150/60 executado como comparação,sem alterar escolha de estudo prioritário.',['entregas/desenvolvimento_2026-11-09/teto_maxeon/resumo.json']),
        61:('autonomia_aplicada_sem_aceite_final','Cenários/componentes provisórios implementados e16escolhas finais consolidadas;0aprovaçõeshumanas.',['docs/APROVACOES_FINAIS_PENDENTES.md'])}
    rows=[]
    for prior in old:
        number=int(prior['decision'].split('-')[1]);decision=prior['decision']
        keys=[k for k,v in c['parameters'].items() if decision in v.get('decisions',[])]
        evidence=sorted({items[i]['evidence'] for i in prior['items']})
        status='modelos_executados_validacao_condicionada';pending='; '.join(dict.fromkeys(items[i]['remaining_limit'] for i in prior['items']))
        if number in special:
            status,pending,extra=special[number];evidence+=extra
        # Append core record plus exact original section hash for immutability.
        for name in evidence:
            if not (ROOT/name).is_file():raise FileNotFoundError(name)
        rows.append({'decision':decision,'title':prior['title'],'items':prior['items'],'lead':prior['lead'],
            'owners':sorted({items[i]['owner'] for i in prior['items']}),'parameter_keys':keys,
            'shared_structures':['development.integrated_scenarios','loads','sources'],'status':status,'pending':pending,
            'original_section_sha256':prior['section_sha256'],
            'evidence':[{'path':x,'sha256':hashlib.sha256((ROOT/x).read_bytes()).hexdigest()} for x in sorted(set(evidence))],
            'human_approval':False})
    dest=ROOT/'entregas/matriz_decisoes_integrada_61.json';dest.write_text(json.dumps({'canonical_revision':c['revision'],'decisions':rows,'human_approvals':0},indent=2,ensure_ascii=False)+'\n')
    lines=['# MatrizDEC001–061 integrada','',
        'Atualizada por `scripts/atualizar_matriz_decisoes_integrada.py`. Registro original e matriz histórica preservados. Métodos aprovados não aprovam resultados. Fonteúnica:YAMLcanônico;JSONresolvido é saída derivada.','',
        '|Decisão|Parâmetros compartilhados|Itens / responsável|Estado / evidência|Pendência de validação|','|---|---|---|---|---|']
    for r in rows:
        short=', '.join(r['parameter_keys']) or 'loads/development/sources;verJSONintegrado'
        links=';'.join(f'[{Path(x["path"]).name}](../{x["path"]})' for x in r['evidence'][:3])
        lines.append(f'|{r["decision"]} — {r["title"]}|{short}|{r["items"]}/{r["lead"]} interfaces{r["owners"]}|{r["status"]};{links}|{r["pending"]}|')
    (ROOT/'docs/MATRIZ_DECISOES_61.md').write_text('\n'.join(lines)+'\n');print('61decisões ligadas a parâmetros/evidências atuais;registro original preservado.')


if __name__=='__main__':main()
