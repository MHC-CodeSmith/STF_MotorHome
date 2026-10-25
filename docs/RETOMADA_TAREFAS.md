# Handoff — 23/10/2026

**Entrada mais recente (25/10): [CONTINUIDADE_CAD_ELETRICO.md](CONTINUIDADE_CAD_ELETRICO.md)** — pedido ativo, estado verificado, arquivos e próximos passos. Bateria de tração/motor/elétrica ainda precisam ser incluídos; não confundir com interior/solar já implementados.

**Ler primeiro [ESTADO_ATUAL.md](ESTADO_ATUAL.md)**: resumo curto e atualizado de24/10. O restante abaixo é histórico e contém etapas superadas (semCd,semotimizador,layout0.1). Não repetir aquisições ou usar contagens antigas.


## Atualização prioritária — 24/10/2026

Ler primeiro [AVANCO_2026-10-24.md](AVANCO_2026-10-24.md) e [artefatos portáveis](../entregas/parcial_2026-10-24/README.md). Implementações de geometria/solar/MILP e piloto preservadas em **449e482** (além de c088758). Continuação de layout/atualização CFD ainda no diff:

- `scripts/adaptar_educato.py`, `src/motorhome/adaptacao_geometrica.py`: malha detalhada autoral L3H2 **5,998 m / WB 4,035 m / topo 2,612 m**, rodas preservadas por translação. Cache `aurora-L3H2-01/`; GLB/PNG/manifesto também no repo. Não CAD OEM, largura/espelhos ainda da fonte. Área aberta adaptada **5,004665 m²**.
- `scripts/reparar_superficie_piloto.py`: candidato fechado **10.444 triângulos**, pneus externos preservados; área **4,827840 m²** (−3,53%). Cache `aurora-cfd-superficie-02/`. Ainda não forma validada; não usar reparos antigos que perderam pneus.
- CFD piloto `cfd-aurora-piloto-03/`: **29.527 células**, Mesh OK, skewness max2,362; `simpleFoam -noFunctionObjects` atingiu resíduos em **108 iterações**; log `log.simpleFoam.fields`. Campos lidos via VTK em `cfd-aurora-visual-01/`, também no repo. **Cd final ausente**: `forceCoeffs` em v1912 falha no IOstream SHA1. Atualização local **2412.260127-1** concluída do repositório oficial em `software/openfoam2412-{debs,local}/`; downloads encerrados, hashes OK; novo pós-processamento calculou **Cd piloto0,65303585**, pressão0,64339287/viscoso0,0096429863, ainda não validado. Prefixo novo `software/openfoam2412-local/usr/lib/openfoam/openfoam2412`, wrapper aceita diretamente. BibliotecasScotch do cacheUbuntu copiadas ali. Script wrapper/env: `scripts/executar_openfoam.py`; gerador `scripts/preparar_cfd_piloto.py`. Sem camadas/y+, grade muito grosseira, rodas estacionárias: só piloto.
- Verificação do OpenFOAM distribuído: pitzDaily **12.225 células, 282 iterações**, cache `cfd-verificacao-01/pitzDaily/`; não validação experimental do veículo.
- `config/solar_proposta.yaml`, `src/motorhome/solar.py`, `scripts/calcular_solar.py`: pvlib **0.16.1**, h5py **3.16.0**, Ineichen/POA/Faiman/PVWatts. INMET **A711** oficial: lat **−21,98027777**, lon **−47,88388888**, altitude **859,29 m** (mesmo registro). Fonte `https://apitempo.inmet.gov.br/estacoes/T`, cache `solar-fontes/inmet-estacoes.json`; extrato pequeno no repo.
- JA Solar **JAM54D41-450/LB/1500V**, p.2 da ficha oficial renderizada/inspecionada: **450 W, 22 kg, 1,762×1,134 m, gamma −.003/K**. Dois/três módulos estimam **3,233/4,849 kWh/dia** após hipóteses de perdas10%/eta95%, sem ganho bifacial. Irradiação horizontal **4,5002 kWh/m²/dia**, Tmaxmódulo **53,29°C**. Resultados corretos `solar-calculo-02/`; descartar 01 (teste detectou unidade interna pandas us/ns; corrigido por `total_seconds`). Consumo residencial/integração HV pendentes.
- `src/motorhome/otimizacao_agenda.py`: MILP/SciPy maximiza distância em grade temporal/modos, energia causal/reserva/capacidade/SOC final/8h calendárias; **não otimiza ainda o tempo da viagem I29**, nem substitui curvas reais. SOC fracionário precisa ser definido em relação à janela útil vsSOC OEM. Seis testes analíticos.
- **90 testes passaram**, ruff novo passou antes do último ajuste/documentação. CI instala extras solar/optimization. Status18 parciais/17 não iniciados; nenhum aprovado; YAML global continua intacto. Pilotos originais encerrados; verificar eventual sessão de refino antes de repetir.

- Refino com camadas **REJEITADO**: `cfd-aurora-refino-01/02/`,74969células,MeshOK mas divergiu;51,13%extrusão.02 encerrado por writeNow (exit0 não é convergência). Novo diagnóstico sem camadas em `cfd-aurora-refino-semcamadas-01/`; consultar logs/sessão. Nunca usar os Cd divergidos.
- `config/layout_proposto.yaml` / `scripts/gerar_layout_proposto.py`: reservas de ocupação2pessoas e teto2módulos, figura emrepo; encaixe real/ergonomia/equipamentos pendentes. Copiar os resultados para a revisão final dos itens13/17, sem declarar especificação pronta.

## Missão e decisões

Concluir projeto acadêmico de motorhome elétrico solar (35 itens), conforme enunciado/apostila, aproveitando CAD/código existentes. Usuário autoriza avanço autônomo e rejeitou o bloco grosseiro como CAD principal. **Usar o Ducato detalhado; não voltar ao bloco nem tratar testes sintéticos como resultados físicos.** A pausa antiga foi seguida de instruções para avançar. Nenhum processo longo está ativo.

- **Worktree:** `/home/mhc/motorhome_solar_codex_tarefas`; **branch:** `hub/tarefas-motorhome-com-codex`; **HEAD:** `c088758` (recuperação local dos 75 testes/CAD/métodos); base `1a4a750`. Arquitetura elétrica posterior ainda no diff. Nenhum push.
- Outra conversa usa `/home/mhc/motorhome_solar_codex`: não editar/copiar seus arquivos não commitados; integrar somente commits revisados.
- D002 em `docs/decisoes.md` e `config/geometria_trabalho.json`: exterior escolhido para trabalho; componentes/variante física não aprovados. Não enviar mensagens a terceiros.
- **D003 / resposta à cobrança elétrica:** [ARQUITETURA_ELETRICA.md](ARQUITETURA_ELETRICA.md) e `config/arquitetura_eletrica_proposta.yaml`: proposta BEV Aurora Solar sobre E-Ducato MY25 L3H2 4250 kg, código 505.GG1.2. OEM 205 kW/410 Nm, 110/98 kWh, 400 V; dados e cotas conferidos no PDF Fiat eslovaco (20/03/2026), pp.1/4/5 visualmente. Cache `fichas-eletricas/`, SHA no YAML. **Carroceria atual de 5 m NÃO é L3H2 de 5,998 m.** Adaptar antes de CFD final. Integração solar HV/BMS e carga simultânea à tração ainda não verificadas. Sem gerador a combustível; I29 sem recarga externa. Não confundir proposta com parâmetros aprovados.
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
| Verificações | **75 testes passaram**, ruff/links/hashes OK, zero erros estruturais. **16 itens parciais: 01,04,06,15,16,17,19,23,27,29,30–35; 19 não iniciados; nenhum aprovado.** YAML aprovado intacto, revisão `0.0.0-scaffold`, **24 nulls**. |
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
- OpenFOAM **v1912 patch200626** instalado por extração de pacotes apt, sem sudo, em `software/openfoam-local/usr/` no cache. `simpleFoam -help` e `surfaceCheck` executados. Manifesto `software/openfoam-instalacao.json`; exemplos em `usr/share/doc/openfoam-examples/examples/`. Wrapper/env ainda precisa entrar no repo: `WM_PROJECT_DIR=PREFIX/share/openfoam`, `FOAM_ETC=PREFIX/share/openfoam/etc`, `FOAM_LIBBIN=PREFIX/lib`, PATH com `PREFIX/bin`, LD_LIBRARY_PATH com `PREFIX/lib:PREFIX/lib/x86_64-linux-gnu`. Limitar RAM/cores (outros agentes usam host).
- Reparos experimentais **REJEITADOS** em `ducato-reparo-{01,02,03}/`: 01 mantém 85 arestas abertas/242 não manifold; 02 fecha mas perde rodas/espelhos; 03 por grupos fecha mas perde pneus (z mínimo 0,216 m e rodas de apenas 0,268 m) e reduz área frontal de 4,2583 para 3,7653 m². **Não usar para CFD ou como resultado.** `pymeshfix==0.18.1` instalado com `--no-deps`; não exige PyVista para `clean_from_arrays`. Próximo reparo deve preservar pneus/aberturas e medir fidelidade, não só estanqueidade.

Na worktree, repetir apenas quando necessário:

```bash
git status --short
PYTHONPATH=src .venv/bin/python -m pytest tests -q
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py
```

Reprodução: `scripts/obter_carroceria.py --destino NOVO`; `scripts/preparar_carroceria.py --entrada GLB --metadados XOMA --destino NOVO`; `scripts/demonstrar_frente_termica.py --sintetico --destino NOVO`. Usar `.venv/bin/python`; comandos completos nos docs. Commit local `c088758`; sem merge, push, publicação ou entrega acadêmica final.
