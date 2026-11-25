# Item 07 — Fiação elétrica

<!-- revisao-final:inicio -->
> **Estado em 16/11/2026:** o resultado final está no [relatório](../../../relatorio/relatorio.pdf), seção 7 (p. 7). Para revisar e registrar o parecer, siga o [guia de revisão por integrante](../../../docs/REVISAO_INTEGRANTES.md). O texto abaixo é o histórico do desenvolvimento; onde ele disser "em desenvolvimento", vale o relatório.
<!-- revisao-final:fim -->

**Responsável:** P2 — Bateria, elétrica e fios  
**Enunciado / tarefa:** Seções, material, isolação, correntes, perdas e critérios de proteção.  
**Depende de:** I04 (P4), I06 (P2), I09 (P2)  
**Status:** Parcial — rotas CAD conceituais e estimativa dos cabos do inversor de serviços; tração e circuito completo pendentes.

Ver [integração elétrica](../../../docs/CAD_TRACAO_E_SERVICOS.md) e
[resultados condicionados](../../../entregas/parcial_2026-10-24/resumo_integracao_eletrica.json).

## Entrega mínima
- `teoria.md`: fenômeno físico, equações, hipóteses e faixa de validade.
- `fontes.md`: referências completas, URL, página/tabela, fabricante e data de acesso.
- `dados/`: entradas com unidades e proveniência; dados desconhecidos continuam como pendentes.
- `codigo/`: notebooks ou scripts com comando exato para executar.
- `resultados/`: tabelas, figuras e logs gerados pelo código. Não inserir resultados fictícios.
- `validacao.md`: testes, revisão humana, limitações, e links para PRs.
- `externos/`: registro dos arquivos de terceiros incorporados legalmente.

## Interface
Entradas oficiais em `config/parametros_globais.yaml`; cada atualização relevante requer registro em `docs/decisoes.md` e deve avisar itens dependentes.

## Aceite
O item só vira **aprovado** quando tiver resultados reproduzíveis, referências e uma revisão por outro integrante.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1560_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
