# Registro efetivo da execução pós-DEC061

Worktree: `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`. A outra worktree foi preservada. Base histórica: `2ef84f67c3aa820633b0565e92c0a23ea810302b`.

## O que foi executado

|Comando / operação|Resultado registrado|
|---|---|
|`PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py`|61 decisões, 35 itens, 972 casos de consumo, 36 comparações DC/buffer, 56 missões; campos 2D de cabos/freios, rede térmica e trecho potável; `output/execucao_pos_dec061.log`.|
|`.venv/bin/python scripts/consolidar_pacote_dec061.py`|BOM de 26 linhas e 16 escolhas finais pendentes; subtotal conhecido de 3.550 kg, custo instalado desconhecido.|
|`.venv/bin/python scripts/verificar_pos_dec061.py`|PASSOU; 15 hashes de entrada, 138 saídas numéricas e 9 arquivos complementares; `output/qa_pos_dec061.json`.|
|`PYTHONPATH=src .venv/bin/python -m pytest -q`|197 passaram; `output/testes_pos_dec061.txt`. Inclui conservação, unidades, bloqueio por falta de interface e modelos multidimensionais.|
|`ruff check src scripts tests`|PASSOU; `output/ruff_pos_dec061.txt`.|
|`.venv/bin/python scripts/verificar_estrutura.py`|Estrutura dos 35 itens e sete responsáveis OK; não é aprovação física.|
|`.venv/bin/python scripts/auditar_projeto.py --json`|Zero erros estruturais; lacunas explícitas mantidas em `output/auditoria_pos_dec061.json`. Campos null incluem metadados e preços desconhecidos, não apenas parâmetros físicos.|
|`.venv/bin/python scripts/verificar_entrega_integrada.py --destino output/verificacao_historica_pos_dec061.json`|Retorno 1: os 124 hashes de artefatos antigos conferem, mas há uma divergência de proveniência do antigo `resumo_freios.json`, porque seu código-fonte mudou. O resultado histórico não foi sobrescrito.|
|Execução dos quatro runners antigos sem `--historico`, com argumentos obrigatórios preenchidos por caminhos de teste|4/4 bloquearam antes de ler dados ou produzir resultados; `output/guardas_historicas_pos_dec061.json`.|
|Integridade e links|Registro original com SHA-256 conferido; 16 identificadores únicos na lista de aprovações; nenhum link local quebrado nos cinco documentos principais; `git diff --check` sem erros.|

Os scripts foram corrigidos durante a execução quando a verificação apontou uma referência YAML inválida e uma variável local que ocultava o módulo de expressão regular. A versão entregue foi reexecutada após essas correções. A interrupção por limite de uso ocorreu na revisão final dos documentos; a retomada completou essa etapa e a conferência do pacote.

## Arquivos alterados ou acrescentados

- Governança: `AGENTS.md`, `README.md`, `docs/HUB_CONTEXT.md`, `docs/RETOMADA_COMPACTA.md`, `docs/decisoes.md`.
- Fonte ativa e classificação: `config/parametros_globais.yaml`, `config/servicos_proposta.yaml`, `config/registro_cenarios.yaml`, `metadata/conciliacao_dec061.yaml`.
- Registro original: `docs/decisoes_motorhome_2026-10-28.md`, incorporado byte a byte, sem edição de decisões.
- Integração: `docs/INTEGRACAO_POS_DEC061.md`, `docs/MATRIZ_DECISOES_61.md`, `docs/REVISAO_35_ITENS.md`, `docs/BLOQUEIOS_POS_DEC061.md`, `docs/PLANO_EXECUCAO_POS_DEC061.md`, `docs/ARQUITETURA_POS_DEC061.md`, `docs/APROVACOES_FINAIS_PENDENTES.md` e este registro.
- Métodos e reprodução: `src/motorhome/reconciliacao.py`, extensão compatível de `src/motorhome/freios_axisimetricos.py`, `scripts/conciliar_dec061.py`, `scripts/consolidar_pacote_dec061.py`, `scripts/verificar_pos_dec061.py`, `tests/test_reconciliacao.py`.
- Proteção contra uso do método antigo: `scripts/calcular_interface_carga.py`, `scripts/calcular_agenda_portatil.py`, `scripts/construir_viagem_condicionada.py`, `scripts/simular_rota_real.py`.
- Mensagem da auditoria: `scripts/auditar_projeto.py`; referências: `fontes_externas/catalogo.csv`.
- Resultados e logs: `entregas/etapa_pos_dec061/` e arquivos `output/*pos_dec061*` indicados acima.

## Limites da entrega

Nenhum novo CFD aerodinâmico ou CFD 3D da cabine foi executado; aproveitaram-se as três malhas existentes e reexecutou-se a rede térmica com limites explícitos. Não houve ensaio físico, contato com fabricante, compra, alteração HV, modificação de suspensão/pneus, envio de e-mail ou aprovação humana final. Paradas de água e redução automática de cargas ainda não têm implementação validada no replay. A comparação de horários permanece parcial e não demonstra ótimo global.

O principal próximo trabalho é P2/P4 obterem evidência da interface DC e da variante/eixos; P1/P3 completarem massas/CAD/CFD/fixações; P6 fechar cargas e aparelhos compatíveis; P7 confirmar parâmetros térmicos OEM. O plano detalha dependências. A única lista de deliberações finais permanece `docs/APROVACOES_FINAIS_PENDENTES.md`.
