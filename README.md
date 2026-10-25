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
