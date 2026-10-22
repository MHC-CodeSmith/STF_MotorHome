# Motorhome elétrico solar — organização para grupo de 7 e Codex

**Projeto acadêmico de Sistemas Térmicos e Fluídicos (2026).** Este é um *esqueleto de trabalho*, não um projeto de engenharia concluído nem um pacote de simulações validadas.

## Início rápido
Auditoria operacional de 22/10/2026: [diagnóstico e evidências](docs/AUDITORIA_INICIAL.md), [dez trabalhos e interfaces](docs/PLANO_10_TRABALHOS.md), [mapa da apostila](docs/mapa_teorico.md) e [software deste host](docs/software_disponivel.md). Status de 21/10 e notas de aquisição anteriores são históricos; consulte o catálogo e o manifesto atualizados.

1. Leia `AGENTS.md` e `docs/HUB_CONTEXT.md`.
2. Leia os PDFs originais em `docs/fontes_recebidas/` (enunciado, planejamento P1–P7 e levantamento de repositórios).
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
