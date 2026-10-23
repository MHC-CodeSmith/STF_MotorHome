# Handoff — 23/10/2026

## Missão e decisões

Concluir projeto acadêmico de motorhome elétrico solar (35 itens), conforme enunciado/apostila, aproveitando CAD/código existentes. Usuário autoriza avanço autônomo e rejeitou o bloco grosseiro como CAD principal. **Usar o Ducato detalhado; não voltar ao bloco nem tratar testes sintéticos como resultados físicos.** A pausa antiga foi seguida de instruções para avançar. Nenhum processo longo está ativo.

- **Worktree:** `/home/mhc/motorhome_solar_codex_tarefas`; **branch:** `hub/tarefas-motorhome-com-codex`; **HEAD/base:** `1a4a750`. Alterações desta frente **ainda sem commit/push**; preservar o diff.
- Outra conversa usa `/home/mhc/motorhome_solar_codex`: não editar/copiar seus arquivos não commitados; integrar somente commits revisados.
- D002 em `docs/decisoes.md` e `config/geometria_trabalho.json`: exterior escolhido para trabalho; componentes/variante física não aprovados. Não enviar mensagens a terceiros.
- Ler resumos/trechos locais; nunca reanexar PDFs/CAD/ZIP ou ler extrações grandes inteiras.

## Feito / evidência cara

**Cache desta frente:** `/home/mhc/motorhome_referencias_tarefas` (prefixo das pastas abaixo).

| Artefato | Resultado/local |
|---|---|
| Exterior real | `ducato-exterior-04/`: `ducato_exterior_m.glb`, `.stl`, `ducato_exterior.png`, `ducato_vistas.png`, manifesto/atribuição. **Usar 04; 01–03 são superados.** |
| Fonte/identidade | OpenX Assets **20261015**, razor24 (2019)/Dogan Ulus (2025), **MPL-2.0 AND CC-BY-4.0**. Original GLB **1.007.100 bytes**, em `cad-downloads/openx-20261015/vehicles/fiat_ducato_2014/`. |
| Geometria medida | **32.350 triângulos**, extensão **4,999985 × 2,507636 × 2,245168 m** com espelhos; silhueta frontal YZ **4,258336656 m²**. **Malha aberta; sem Cd/volume de cabine validado.** |
| Extração | Grupo `Grp_Exterior`, excluindo interior; glTF→Z-up: **x'=x, y'=-z, z'=y**, sem reescala/convex hull. Rodas/portas/vidros/espelhos preservados. |
| Delica | `/home/mhc/motorhome_referencias/downloads/_Delica_Assembly.step` e `.FCStd`: **68 sólidos/790 faces**, móveis/interior. Prévia `delica-review/`. Não encaixado no Ducato; licença/adequação pendentes. |
| Métodos | `src/motorhome/{termica_2d,sistemas_termicos,agenda_energia,geometria_malha}.py` e testes correspondentes. Demonstração `verificacao-termica-01/` é **SYNTHETIC**; ordem espacial mínima **2,002**. I33 prescrito: **400 J/kg, 80 W/kg**, não calor integral de disco. |
| Verificações | **75 testes passaram**, ruff/links/hashes OK, zero erros estruturais. **11 itens parciais: 16,17,19,27,29,30–35; 24 não iniciados; nenhum aprovado.** YAML aprovado intacto, revisão `0.0.0-scaffold`, **24 nulls**. |
| Correções | I27 final **30%**, não ≥30%; I26 **km/kWh**; I18 inclui fiação I07/arrefecimento I10. CI e documentação/teorias dos métodos atualizadas. |

## Retomar daqui

1. [REVISAO_35_ITENS.md](REVISAO_35_ITENS.md): requisito/evidência/apostila/ação por item.
2. [CARROCERIA_DE_TRABALHO.md](CARROCERIA_DE_TRABALHO.md): aquisição, créditos, hashes, limites e comandos. Manifesto pequeno no item I17 em `resultados/manifesto_carroceria.json`; licenças em `externos/openx/`.
3. [FRENTE_TERMICA.md](FRENTE_TERMICA.md): equações/hipóteses/testes. `VERIFICACAO_CAD_APOSTILA.md` é histórico com aviso de atualização. `gerar_envelope_cad.py`/`proposta_envelope.json` são só o experimento antigo.
4. `metadata/itens.csv`, `fontes_externas/{catalogo,registro_importacoes}.csv` e `REGISTRO_M0.md` registram donos/fontes/pendências.

**Próximas ações:** conferir variante/dimensões reais (malha ~5 m não é automaticamente L3H2/E-Ducato); reparar furos/interseções para CFD e executar domínio/solver/convergência; adaptar layout para duas pessoas/equipamentos; obter motor/transmissão/bateria/BMS/pneus/PV/BOM/auxiliares reais e integrar os modelos. **Não copiar massa/desempenho do `.xoma` como ficha técnica**, nem misturar o Delica ao Ducato sem verificar encaixe.

I30–I35 ainda exigem componentes/cenários físicos: solver 2D atual é cartesiano homogêneo/fonte fixa; não resolve automaticamente cabo isolado/rho(T), disco real ou química/CC-CV da bateria. Perfil paralelo não substitui radiador cruzado. I27/I29 **validam agendas, não otimizam**; a integração deve impor SOC **0,30**/tolerância, **7.000.000 m**, **28.800 s/dia**, sem recarga externa. Aprovações e interpretações docentes seguem pendentes; desenvolver o que independe delas, sem inventar respostas.

## Fontes, ambiente e comandos

- PDF reenviado é idêntico ao levantamento já no repo; pp. **6–8** indicam E-Ducato L2H1, Ducato L3H2 e MELVING22. Warehouse retornou web **403**/HTML genérico **10.922 bytes**, sem SKP; MELVING é solar car. Por isso se obteve exterior alternativo, não outro bloco.
- Download efetivo: `https://github.com/vevalabs/openx-assets/releases/download/20261015/openx-assets-glb.zip`, **19.887.432 bytes**; SHA fixado no script. `obter_carroceria.py` foi executado com sucesso; cópia em `ducato-fontes-reproduzidas-01/`. Hashes completos no manifesto/documentação, não pesquisar novamente.
- Extrações: `/home/mhc/motorhome_referencias/textos/`; enunciado ~6 kB; apostila deve ser lida por `rg`/recortes. Páginas físicas **9/10** Fourier/Newton, **31/38–39** trocador, **56** bomba, **74** Eq.112. Ressalvas em `revisao_apostila.md` (fluxo cruzado questionado).
- `.venv` própria herda sistema; **NumPy 1.26.4** evita incompatibilidade com SciPy antigo; Gmsh **4.15.2**. `Matplotlib.set_box_aspect` modifica array: passar `.copy()` (corrigido).
- Shell sandbox falhou com `bwrap: loopback: Failed RTM_NEWADDR`; comandos funcionaram com `sandbox_permissions=require_escalated`, sem rejeição automática. Bright Data indisponível; web/HTTP público usados sem login/compra.

Na worktree, repetir apenas quando necessário:

```bash
git status --short
PYTHONPATH=src .venv/bin/python -m pytest tests -q
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py
```

Reprodução: `scripts/obter_carroceria.py --destino NOVO`; `scripts/preparar_carroceria.py --entrada GLB --metadados XOMA --destino NOVO`; `scripts/demonstrar_frente_termica.py --sintetico --destino NOVO`. Usar `.venv/bin/python`; comandos completos nos docs. Sem commit, merge, push, publicação ou entrega acadêmica final.
