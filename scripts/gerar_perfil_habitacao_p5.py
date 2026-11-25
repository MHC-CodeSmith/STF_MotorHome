"""I06/I13: entrega à P5 um perfil horário estimado, conservando o orçamento diário.

Horários são hipóteses, não dados de fabricante. Lavagem/secagem são médias semanais,
não picos elétricos instantâneos de um ciclo. O modelo principal ainda usa a média
contínua; este arquivo torna a rotina alternativa explícita e auditável.
"""
import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]


def gerar_perfil(config):
    p = {k: v['value'] for k, v in config['parameters'].items()}
    usos = {'geladeira': list(range(24)), 'inducao': [8, 12, 19],
            'ar_condicionado': [13, 14, 15], 'boiler': [18, 19],
            'lavagem': [10], 'secagem': [11, 12],
            'iluminacao_eletronicos_bombas': [6, 7, 8, 18, 19, 20, 21, 22]}
    rows, fontes = [], []
    for load in config['loads']:
        key = load['id']
        # A nomenclatura canônica pode incluir frigobar/climatizacao.
        horas = usos.get(key, list(range(24)))
        eta = p['eta_inverter'] if load['side'] == 'AC' else p['eta_lv']
        energy = load['energy_ac_or_dc_kwh_day']['base']
        fontes.append({'id': key, 'fonte': load['source'], 'hipotese_horario': horas,
                       'energia_aparelho_kwh_dia': energy, 'rendimento': eta,
                       'nota': load.get('uncertainty_note', '')})
        for h in range(24):
            app = energy / len(horas) if h in horas else 0.0
            rows.append({'hora_inicio': h, 'hora_fim': h+1, 'id': key, 'alimentacao': load['side'],
                         'potencia_media_aparelho_kw': app,
                         'perdas_conversao_kw': app / eta - app,
                         'potencia_retirada_banco_kw': app / eta})
    for h in range(24):
        rows.append({'hora_inicio': h, 'hora_fim': h+1, 'id': 'inversor_vazio', 'alimentacao': 'DC',
                     'potencia_media_aparelho_kw': 0.0, 'perdas_conversao_kw': p['inverter_idle_w']/1000,
                     'potencia_retirada_banco_kw': p['inverter_idle_w']/1000})
    return rows, fontes


def main():
    cfg = ROOT / 'config/parametros_globais.yaml'
    config = yaml.safe_load(cfg.read_text())
    rows, fontes = gerar_perfil(config)
    out = ROOT / 'entregas/integrado_maxeon1560/perfil_habitacao'
    out.mkdir(exist_ok=True)
    with (out/'por_aparelho.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    total = np.array([sum(r['potencia_retirada_banco_kw'] for r in rows if r['hora_inicio']==h)
                      for h in range(24)])
    with (out/'perfil_24h.csv').open('w') as f:
        writer = csv.writer(f, lineterminator='\n'); writer.writerow(['hora_inicio','potencia_banco_kw'])
        writer.writerows(enumerate(total))
    result = {'script': 'scripts/gerar_perfil_habitacao_p5.py', 'cenario': 'maxeon1560_independente',
              'data': '2026-11-25', 'config_sha256': hashlib.sha256(cfg.read_bytes()).hexdigest(),
              'energia_banco_kwh_dia': float(total.sum()), 'potencia_media_kw': float(total.mean()),
              'pico_medio_1h_kw': float(total.max()), 'fontes_e_hipoteses': fontes,
              'limites': ['Perfil horário estimado, não medido.',
                         'Não substitui corrente de pico ou verificação de simultaneidade do inversor.',
                         'Resultados principais I25/I29 usam carga média; este perfil é o handoff para estudo da rotina.']}
    (out/'resumo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.step(range(25), np.r_[total,total[-1]], where='post', label='rotina horária estimada')
    ax.axhline(total.mean(), color='#e8590c', ls='--', label='média usada em I25/I29')
    ax.set(xlabel='hora local', ylabel='potência retirada do banco [kW]', xlim=(0,24), xticks=range(0,25,3))
    ax.legend();ax.grid(alpha=.25);fig.tight_layout()
    fig.savefig(ROOT/'relatorio/figuras/i13_perfil_habitacao.png', dpi=180);plt.close(fig)
    print(json.dumps({k: result[k] for k in ['energia_banco_kwh_dia','potencia_media_kw','pico_medio_1h_kw']}))


if __name__ == '__main__':
    main()
