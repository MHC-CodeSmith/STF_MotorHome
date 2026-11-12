# STF Motorhome Solar — status verificável

[![CI — estrutura, modelos e evidências](https://github.com/MHC-CodeSmith/STF_MotorHome/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/MHC-CodeSmith/STF_MotorHome/actions/workflows/ci.yml)

**Estado do estudo em 12/11/2026:** desenvolvimento computacional dos 35 itens, preservando as 61 decisões. Os resultados são cálculos, simulações ou sensibilidades sob as hipóteses indicadas em cada evidência. O projeto **não está validado fisicamente**: há zero aprovações humanas finais, e a missão solar não foi demonstrada. Arquitetura B (interface DC externa para tração) continua hipótese sem comprovação de compatibilidade ou autorização OEM.

## Revisão rápida

- [Retomada compacta e QA mais recente](docs/RETOMADA_COMPACTA.md)
- [Revisão técnica dos 35 itens, métodos e resultados](docs/REVISAO_GERAL_PROJETO.md)
- [Estados resumidos por item](docs/REVISAO_TECNICA_EXECUCAO02.md)
- [Bloqueios por dependência externa ou humana](docs/BLOQUEIOS_POS_DEC061.md)
- [Decisões DEC-001 a DEC-061](docs/MATRIZ_DECISOES_61.md)
- [Fontes e dados OEM do E-Ducato](docs/DADOS_OEM_EDUCATO_FONTES.md)
- [Escolhas provisórias e aprovações finais pendentes](docs/APROVACOES_FINAIS_PENDENTES.md)

## Reproduzir as verificações

Em Ubuntu/Debian, instale a biblioteca de execução do Gmsh; depois use Python3.11 ou mais recente e as dependências de desenvolvimento/modelagem:

```bash
sudo apt-get update && sudo apt-get install -y libglu1-mesa
python -m pip install -e '.[dev,thermal,cad,solar,optimization]'
python scripts/verificar_estrutura.py
python scripts/auditar_projeto.py
ruff check src scripts tests
PYTHONPATH=src python -m pytest tests -q
MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src python scripts/verificar_cenario_integrado.py
PYTHONPATH=src python scripts/verificar_desenvolvimento.py
```

Os dois últimos verificadores são somente leitura sem `--registrar`: conferem resultados e hashes publicados. O GitHub Actions executa esses comandos em `push` e `pull_request`, com Ruff fixado em0.17.5, e anexa os relatórios QA, manifests, resumos I29 e JUnit à execução. Um CI verde confirma estrutura, software, consistência numérica e integridade dos arquivos sob as hipóteses registradas; **não certifica instalação, segurança, conformidade OEM, convergência física ou viabilidade da missão**.

## Resultados condicionais recentes

- I29 compara buscas finitas distintas e preserva as saídas em `entregas/integrado_maxeon1540/otimizacao_*`; não declara ótimo global.
- O diagnóstico do limiar DC tem código reproduzível em `scripts/analisar_aliasing_limiar_dc.py`, teste próprio e saídas CSV/JSON/PNG em `entregas/integrado_maxeon1540/otimizacao_resolucao_temporal/aliasing_limiar_dc/`. O limiar de 1 kW é hipotético, não especificação de carregador.
- CFD, balanços de massa/eixos, circuitos, HVAC e arrefecimento têm limites, entradas assumidas e evidências listadas na revisão técnica e nos bloqueios. Valores ausentes permanecem lacunas ou sensibilidades explícitas; não são preenchidos como especificações OEM.

---

## Histórico e documentação legada

Os textos abaixo preservam instruções e estados antigos. Para o estado vigente, use os documentos de revisão rápida acima; datas/status antigos são históricos.

# Execução atual — conciliação DEC-001 a DEC-061

[Integração e resultados atuais](docs/INTEGRACAO_POS_DEC061.md) · [35itens](docs/REVISAO_35_ITENS.md) · [61decisões rastreadas](docs/MATRIZ_DECISOES_61.md) · [aprovações finais pendentes](docs/APROVACOES_FINAIS_PENDENTES.md).

**ArquiteturaB escolhida; recargaDC OEM não demonstrada;35trabalhos iniciados e0aprovações finais.** Fonte única: `config/parametros_globais.yaml`. Execute `PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py` e depois `scripts/consolidar_pacote_dec061.py` e `scripts/verificar_pos_dec061.py`. O CAD/PDF anteriores continuam disponíveis como histórico. Os status e potências de extensão descritos abaixo não são o baseline atual.

## Histórico anterior à conciliação

Avanço de26/10: [cabos isolados e radiador cruzado](docs/CABOS_E_RADIADOR_2D.md), com campos2D, fontes, alternativas, três malhas e **132testes passados**. [Memorial de revisão](output/pdf/memorial_revisao_aurora.pdf):20páginas, parcial. I30/I35 ainda dependem de entradas físicas/revisão.

# Motorhome elétrico solar — organização para grupo de 7 e Codex

**Atualização mais recente:** [interior equipado e cobertura solar ampliada](docs/EXPANSAO_SOLAR_E_INTERIOR.md), [visualizador offline](entregas/parcial_2026-10-24/visualizador.html), [memorial parcial16p](output/pdf/memorial_revisao_aurora.pdf). Cobertura fixa1540W; extensão de estudo2890W.112testes,26itens parciais/9nãoiniciados/0aprovados.

**Projeto acadêmico de Sistemas Térmicos e Fluídicos (2026).** Este é um *esqueleto de trabalho*, não um projeto de engenharia concluído nem um pacote de simulações validadas.

## Início rápido
Estado atual: [retomada curta](docs/ESTADO_ATUAL.md), [visualizador 3D offline](entregas/parcial_2026-10-24/visualizador.html), [energia e otimização condicionadas](docs/ENERGIA_E_OTIMIZACAO.md) e [CADs online pesquisados](docs/CAD_ONLINE_E_VISUALIZACAO.md).

Execução de 24/10: [artefatos visuais e CAD adaptado](entregas/parcial_2026-10-24/README.md), [estimativa solar e CFD piloto](docs/AVANCO_2026-10-24.md). Tração elétrica, proposta L3H2; resultados ainda condicionados às hipóteses e à revisão física descrita nos documentos.

Estado desta frente em 23/10: [carroceria Ducato detalhada e arquivos](docs/CARROCERIA_DE_TRABALHO.md), [revisão ponto a ponto dos 35 itens](docs/REVISAO_35_ITENS.md) e [métodos térmicos implementados](docs/FRENTE_TERMICA.md). O envelope autoral anterior fica apenas como teste de exportação.

Auditoria operacional de 22/10/2026: [diagnóstico e evidências](docs/AUDITORIA_INICIAL.md), [dez trabalhos e interfaces](docs/PLANO_10_TRABALHOS.md), [mapa da apostila](docs/mapa_teorico.md) e [software deste host](docs/software_disponivel.md). Status de 21/10 e notas de aquisição anteriores são históricos; consulte o catálogo e o manifesto atualizados.

1. Leia `AGENTS.md` e `docs/HUB_CONTEXT.md`.
2. Consulte os resumos e trechos locais indicados em `docs/RETOMADA_TAREFAS.md`; extraia somente a seção necessária dos PDFs, sem carregar anexos grandes no contexto.
3. Siga `docs/PROMPT_INICIAL_CODEX.md` e `docs/marcos_e_revisoes.md`.
4. Cada integrante trabalha em `equipe/PX_.../Ixx_.../` com código, teoria, fontes, dados e resultados locais.
5. Parâmetros do veículo **só** são publicados em `config/parametros_globais.yaml`. Mudanças compartilhadas exigem revisão de impacto.
6. Prepare `.venv` com `uv venv .venv` e `uv pip install --python .venv/bin/python -e '.[dev]'`. Rode `.venv/bin/python scripts/verificar_estrutura.py`, `.venv/bin/python scripts/auditar_projeto.py` e os testes direcionados documentados na auditoria. Exit 0 da auditoria valida estrutura; parâmetros pendentes e aprovação física são tratados separadamente.

## Organização
- `equipe/`: 7 pessoas, 35 itens, cada item com `README.md`, `teoria.md`, `fontes.md`, `validacao.md`, `codigo/`, `dados/`, `resultados/`, `externos/`.
- `config/`: parâmetros e condições globais para todos os agentes; campos ainda desconhecidos ficam `null`.
- `src/motorhome/`: funções compartilhadas. Nunca copiar funções entre itens se é possível importar a função comum.
- `docs/`: contextos dos agentes, dependências, reuniões, critérios de aceitação e padrão de integração.
- `fontes_externas/`: catálogo, histórico de verificação de links e instruções para importar CAD/código com licença.
- `relatorio/`: organização do texto final e `bibliografia.bib`.

**Atenção:** o enunciado original solicita grupos de 10; confirmar autorização para 7 com docentes. O material de terceiros só pode ser redistribuído/adaptado conforme licença/autorização, com atribuição, e os cálculos do projeto devem ser refeitos nas condições prescritas.

## Revisão de 25/10/2026

[Memorial PDF parcial](output/pdf/memorial_revisao_aurora.pdf), 13 páginas, aproximadamente1MB. [Cabine/HVAC](docs/CABINE_E_HVAC.md) tem caso numérico condicionado; [pneu/massa](docs/PNEUS_E_MASSA.md) tem especificação primária e limites. **105 testes passaram;24 itens parciais/11 não iniciados/0 aprovados.** O projeto completo ainda depende dos componentes, integração elétrica e simulações físicas descritos na matriz.
