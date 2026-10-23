"""Gera campos 2D, convergência e balanços SYNTHETIC; nenhum resultado do veículo."""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from motorhome.sistemas_termicos import (
    carga_ac,
    carga_ohmica,
    frenagem_especifica,
    perfil_paralelo,
    ponto_bomba,
    transiente_concentrado,
)
from motorhome.termica_2d import Contorno, Malha, Material, resolver


def escrever_csv(path, linhas):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sintetico', action='store_true', required=True)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    entradas = {
        'rotulo': 'SYNTHETIC - VERIFICACAO DE METODO, NAO MOTORHOME',
        'revision': 'synthetic-thermal-1',
        'modo_analitico': {'lx_m': 1., 'ly_m': .7, 'espessura_m': .1,
                           'k_w_mk': 1., 'rho_kg_m3': 1., 'cp_j_kgk': 1.,
                           'base_k': 300., 'amplitude_k': 10., 'tempo_s': .02,
                           'malhas': [8, 16, 32], 'seguranca': .1},
        'aquecimento_2d': {'lx_m': .1, 'ly_m': .07, 'espessura_m': .01,
                           'nx': 32, 'ny': 24, 'k_w_mk': 2., 'rho_kg_m3': 1000.,
                           'cp_j_kgk': 500., 'inicial_k': 300., 'ambiente_k': 295.,
                           'h_w_m2k': 20., 'fonte_fundo_w_m3': 2e5,
                           'fonte_pico_w_m3': 8e5, 'tempo_s': 10.},
        'concentrado': {'capacidade_j_k': 1000., 'ua_w_k': 10., 'inicial_k': 350.,
                       'ambiente_k': 300., 'geracao_w': 0.},
        'trocador_paralelo': {'ua_w_k': 100., 'capacidade_quente_w_k': 100.,
                             'capacidade_fria_w_k': 200., 'quente_entrada_k': 380.,
                             'fria_entrada_k': 300.},
        'bomba': {'vazoes_m3_s': [0., .001, .002, .003],
                  'bomba_pa': [40000., 35000., 20000., 0.],
                  'sistema_pa': [0., 5000., 20000., 45000.]},
        'ac': {'ua_w_k': 100., 'exterior_k': 306.15, 'interior_k': 298.15,
               'solar_transmitido_w': 200., 'equipamentos_w': 50., 'ocupantes': 2,
               'sensivel_por_pessoa_w': 70., 'latente_por_pessoa_w': 40.,
               'ventilacao_sensivel_w': 10., 'ventilacao_latente_w': 20., 'cop': 3.},
        'bateria_ohmica': {'tensao_terminal_v': 400., 'resistencia_pack_ohm': .04,
                          'potencias_terminais_w': [20000., 80000.]},
    }
    fixture_bytes = json.dumps(entradas, ensure_ascii=False, indent=2).encode()
    (out/'entradas_SYNTHETIC.json').write_bytes(fixture_bytes)
    bcs = {l: Contorno('isolado') for l in ['esquerda', 'direita', 'inferior', 'superior']}
    p = entradas['modo_analitico']
    conv = []
    for n in p['malhas']:
        m = Malha(p['lx_m'], p['ly_m'], p['espessura_m'], n, n)
        x, y = m.centros()
        modo = np.cos(np.pi*x/p['lx_m'])*np.cos(np.pi*y/p['ly_m'])
        ti = p['base_k']+p['amplitude_k']*modo
        mat = Material(p['k_w_mk'], p['rho_kg_m3'], p['cp_j_kgk'])
        r = resolver(m, mat, ti, 0., bcs, p['tempo_s'], seguranca=p['seguranca'])
        alfa = mat.k_w_mk/(mat.rho_kg_m3*mat.cp_j_kgk)
        te = p['base_k']+p['amplitude_k']*modo*np.exp(
            -alfa*np.pi**2*(1/m.lx_m**2+1/m.ly_m**2)*p['tempo_s'])
        conv.append({'n': n, 'h_m': max(m.dx, m.dy), 'dt_s': r['passo_s'],
                     'passos': r['passos'], 'erro_rms_k': float(np.sqrt(np.mean((r['temperatura_k']-te)**2))),
                     'residuo_energia_j': r['historico'][-1]['residuo_j']})
    escrever_csv(out/'convergencia_espacial_SYNTHETIC.csv', conv)
    ordens = [float(np.log(conv[i]['erro_rms_k']/conv[i+1]['erro_rms_k'])/np.log(2))
              for i in range(len(conv)-1)]
    assert min(ordens) > 1.8, ordens
    p = entradas['aquecimento_2d']
    m = Malha(p['lx_m'], p['ly_m'], p['espessura_m'], p['nx'], p['ny'])
    x, y = m.centros()
    fonte = p['fonte_fundo_w_m3']+p['fonte_pico_w_m3']*np.exp(
        -50*((x/m.lx_m-.4)**2+(y/m.ly_m-.6)**2))
    bc = {l: Contorno('conveccao', p['ambiente_k'], p['h_w_m2k']) for l in bcs}
    r = resolver(m, Material(p['k_w_mk'], p['rho_kg_m3'], p['cp_j_kgk']),
                 p['inicial_k'], fonte, bc, p['tempo_s'])
    escrever_csv(out/'historico_2d_SYNTHETIC.csv', r['historico'])
    escrever_csv(out/'campo_2d_SYNTHETIC.csv', [
        {'x_m': float(x[j, i]), 'y_m': float(y[j, i]),
         'temperatura_k': float(r['temperatura_k'][j, i]),
         'geracao_w_m3': float(fonte[j, i])}
        for j in range(m.ny) for i in range(m.nx)])
    pg, perfil = perfil_paralelo(**entradas['trocador_paralelo'], fracoes_area=np.linspace(0, 1, 51))
    escrever_csv(out/'trocador_paralelo_SYNTHETIC.csv', perfil)
    bomba = ponto_bomba(**entradas['bomba'])
    tempos = np.linspace(0, 300, 61)
    transiente = [transiente_concentrado(**entradas['concentrado'], duracao_s=float(t))
                  for t in tempos]
    escrever_csv(out/'concentrado_SYNTHETIC.csv', [
        {'tempo_s': float(t), **v} for t, v in zip(tempos, transiente)])
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout='constrained')
    a = axes[0, 0]
    im = a.pcolormesh(x, y, r['temperatura_k'], shading='nearest', cmap='inferno')
    fig.colorbar(im, ax=a, label='Temperatura [K]')
    a.set(title='Difusão 2D com fonte não uniforme', xlabel='x [m]', ylabel='y [m]', aspect='equal')
    a = axes[0, 1]
    a.loglog([c['h_m'] for c in conv], [c['erro_rms_k'] for c in conv], 'o-')
    a.set(title=f'Verificação analítica: ordem mínima {min(ordens):.2f}',
          xlabel='Tamanho de célula h [m]', ylabel='Erro RMS [K]')
    a.grid(True, which='both', alpha=.3)
    a = axes[1, 0]
    a.plot([v['fracao_area'] for v in perfil], [v['quente_k'] for v in perfil], label='Quente')
    a.plot([v['fracao_area'] for v in perfil], [v['fria_k'] for v in perfil], label='Frio')
    a.set(title='Trocador paralelo; não radiador automotivo', xlabel='Área acumulada / total', ylabel='Temperatura [K]')
    a.legend()
    a = axes[1, 1]
    b = entradas['bomba']
    a.plot(np.array(b['vazoes_m3_s'])*1000, np.array(b['bomba_pa'])/1000, label='Bomba')
    a.plot(np.array(b['vazoes_m3_s'])*1000, np.array(b['sistema_pa'])/1000, label='Sistema')
    a.scatter([v['vazao_m3_s']*1000 for v in bomba], [v['pressao_pa']/1000 for v in bomba], color='black', zorder=3)
    a.set(title='Interseção de curvas sintéticas', xlabel='Vazão [L/s]', ylabel='Pressão diferencial [kPa]')
    a.legend()
    fig.suptitle('SYNTHETIC — verificação de métodos; não são resultados do motorhome', fontsize=12)
    fig.savefig(out/'verificacao_SYNTHETIC.png', dpi=160)
    plt.close(fig)
    resumo = {'rotulo': entradas['rotulo'], 'revision': entradas['revision'],
              'data_utc': datetime.now(timezone.utc).isoformat(),
              'entradas_sha256': hashlib.sha256(fixture_bytes).hexdigest(),
              'config_projeto_sha256': hashlib.sha256((ROOT/'config/parametros_globais.yaml').read_bytes()).hexdigest(),
              'script': str(Path(__file__).relative_to(ROOT)),
              'fontes': ['docs/mapa_teorico.md', 'docs/FRENTE_TERMICA.md'],
              'bibliotecas': {'numpy': np.__version__, 'matplotlib': matplotlib.__version__},
              'ordens_espaciais': ordens, 'estado_final_2d': r['historico'][-1],
              'trocador': pg, 'ponto_bomba': bomba, 'ac_sintetico': carga_ac(**entradas['ac']),
              'bateria_parcela_ohmica_sintetica': [carga_ohmica(p, entradas['bateria_ohmica']['tensao_terminal_v'],
                 entradas['bateria_ohmica']['resistencia_pack_ohm'])
                 for p in entradas['bateria_ohmica']['potencias_terminais_w']],
              'aprovacao_engenharia': False}
    assert abs(r['historico'][-1]['residuo_j']) < 1e-6
    (out/'resumo_SYNTHETIC.json').write_text(json.dumps(resumo, indent=2, ensure_ascii=False))
    # Derivação do requisito fica SEPARADA das entradas e resultados sintéticos.
    import yaml
    config = yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    c = config['special_cases']
    prescrito = frenagem_especifica(c['braking_initial_speed_m_per_s'],
                                   c['braking_final_speed_m_per_s'], c['braking_duration_s'])
    (out/'frenagem_prescrita_por_kg.json').write_text(json.dumps({
        'tipo': 'derivacao_do_enunciado_sem_massa_do_veiculo',
        'fonte': 'enunciado 2026 p.2 I33 e config/parametros_globais.yaml',
        'config_sha256': resumo['config_projeto_sha256'], 'data_utc': resumo['data_utc'],
        'script': resumo['script'], 'resultados': prescrito,
        'limite': 'energia translacional removida; não é calor atribuído aos discos'}, indent=2))
    print(f'Verificação SYNTHETIC gerada em {out}; ordem mínima {min(ordens):.3f}; sem aprovação de engenharia.')


if __name__ == '__main__':
    main()
