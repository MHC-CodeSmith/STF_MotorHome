"""Empacota GLB existente para inspeção offline; não é editor CAD nem solver."""

import argparse
import base64
import hashlib
import json
from pathlib import Path

import yaml


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--glb', type=Path, required=True)
    p.add_argument('--layout', type=Path, required=True)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--licenca-three', type=Path, required=True)
    p.add_argument('--instalacoes', type=Path, required=True)
    p.add_argument('--equipamentos', type=Path, default=Path('config/equipamentos_interior.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    layout = yaml.safe_load(args.layout.read_text())
    data = {'glb_base64': base64.b64encode(args.glb.read_bytes()).decode(), 'layout': layout,
            'layout_alignment_assumed': {'rear_x_m': -3.35, 'floor_z_m': .68}}
    data['equipment'] = yaml.safe_load(args.equipamentos.read_text())
    cad_inputs = []
    for key, filename in [('interior_glb_base64', 'interior_equipado.glb'),
                          ('roof_fixed_glb_base64', 'cobertura_fixa.glb'),
                          ('roof_stowed_glb_base64', 'cobertura_recolhida.glb'),
                          ('roof_open_glb_base64', 'cobertura_aberta.glb')]:
        path = args.instalacoes/filename
        cad_inputs.append(path)
        data[key] = base64.b64encode(path.read_bytes()).decode()
    html = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aurora Solar · inspeção da geometria</title>
<style>*{box-sizing:border-box}body{margin:0;font:15px system-ui;color:#21384a;background:#edf1f4}header{background:#12354b;color:white;padding:18px 24px}h1{font-size:23px;margin:0 0 7px}p{margin:8px 0;line-height:1.5}main{display:grid;grid-template-columns:1fr 300px;max-width:1600px;margin:auto}#scene{height:85vh;min-height:440px;position:relative}canvas{display:block}aside{padding:18px;background:white;max-height:85vh;overflow:auto}#components button{font-size:12px;text-align:left;width:100%}button{font:inherit;margin:3px;padding:8px;background:#e7eff4;border:1px solid #aebfca;border-radius:5px;cursor:pointer}label{display:block;margin:14px 0}.tag{font-size:12px;border:1px solid #94b6c7;display:inline-block;padding:3px 7px;border-radius:4px}footer{padding:10px 24px;font-size:13px}#loading{padding:8px 24px;background:#dce9f0}small{line-height:1.6;display:block}a{color:#17628e}@media(max-width:850px){main{grid-template-columns:1fr}#scene{height:56vh;min-height:320px}}</style>
<header><h1>Aurora Solar · motorhome elétrico</h1><span class="tag">Proposta autoral · geometria em revisão</span><p>Carroceria detalhada derivada do Ducato, adaptada às cotas L3H2. Abra este arquivo diretamente no navegador, sem internet.</p></header>
<main><div id="scene" role="img" aria-label="Vista tridimensional interativa da carroceria proposta"></div><aside>
<strong>Vistas</strong><p><button data-view="iso">Perspectiva</button><button data-view="side">Lateral</button><button data-view="top">Superior</button><button data-view="front">Frontal</button></p>
<label><input type="checkbox" id="inside"> Ver interior equipado / corte do teto</label><label><input type="checkbox" id="hideShell"> Ocultar carroceria</label><label><input type="checkbox" id="hideBed"> Retirar cama para ver instalações inferiores</label><label><input type="checkbox" id="wire"> Triângulos da carroceria</label><label><input type="checkbox" id="panels" checked> Cobertura solar</label><label><input type="checkbox" id="extensionInstalled"> Comparar extensão empilhada (carga em revisão)</label><label><input type="checkbox" id="deploy"> Abrir extensão solar (estacionado)</label><p id="solarState"></p>
<p><strong>Base proposta</strong><br>5,998 m de comprimento<br>4,035 m de entre-eixos<br>2,612 m de altura da carroceria<br>2,745 m fixa / 2,805 m com extensão recolhida</p>
<small>Modelos autorais dimensionados: cama longitudinal, geladeira, lava-seca, indução, pia, sanitário, ducha, HVAC sob cama e mesa. Detalhes não são CAD OEM. Alinhamento X=-3,35 m / piso Z=0,68 m assumido; portas, caixas de roda, acabamentos e fixações ainda precisam de revisão. Extensão solar sem dimensionamento estrutural final.</small>
<p><strong>Localizar equipamentos</strong></p><div id="components"></div><div id="itemInfo" style="font-size:12px;border-top:1px solid #ccd;padding-top:10px"></div><p><a href="interior_equipado.step">CAD STEP do interior</a> · <a href="cobertura_fixa.step">Cobertura fixa</a> · <a href="cobertura_recolhida.step">Extensão recolhida</a> · <a href="cobertura_aberta.step">Cobertura aberta</a></p>
</aside></main><p id="loading">Carregando geometria…</p>
<footer><p>Inspeção visual; este visualizador não é um CAD paramétrico. Ver <a href="README.md">resultados e limitações</a>. Base OEM elétrica proposta; forma adaptada não homologada Fiat.</p>
<p>Geometria: razor24 (2019), Dogan Ulus (2025), OpenX Assets 20261015, MPL-2.0 AND CC-BY-4.0. Transformações autorais: eixos, comprimento e altura; rodas por translação. Créditos/licenças completos em <a href="ATTRIBUTION.txt">ATTRIBUTION.txt</a>, <a href="CC-BY-4.0.txt">CC-BY-4.0</a> e <a href="MPL-2.0.txt">MPL-2.0</a>. Fonte em <a href="https://github.com/vevalabs/openx-assets/tree/1a63f13b5cfee3e01207a84b13b40fc172d92a95/src/vehicles/fiat_ducato_2014">OpenX Assets</a>. Renderização: Three.js 0.180.0, licença MIT preservada.</p></footer>
<script>window.AURORA_DATA=__DATA__;</script><script>__BUNDLE__</script></html>'''
    html = html.replace('__DATA__', json.dumps(data, ensure_ascii=True).replace('</', '<\\/'))
    html = html.replace('__BUNDLE__', args.bundle.read_text().replace('</script', '<\\/script'))
    html += '\n<!-- Three.js license (preserved in standalone file):\n'+args.licenca_three.read_text()+'\n-->\n'
    args.destino.mkdir(parents=True, exist_ok=False)
    (args.destino/'visualizador.html').write_text(html)
    manifest = {'status': 'INSPECAO_VISUAL_NAO_CAD_HOMOLOGADO', 'script': 'scripts/gerar_visualizador.py',
                'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [args.glb, args.layout, args.bundle, args.licenca_three, args.equipamentos, *cad_inputs]},
                'alignment_assumed': data['layout_alignment_assumed'], 'offline': True,
                'output_sha256': hashlib.sha256((args.destino/'visualizador.html').read_bytes()).hexdigest()}
    (args.destino/'manifesto_visualizador.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(json.dumps({'bytes': (args.destino/'visualizador.html').stat().st_size, **manifest}))


if __name__ == '__main__':
    main()
