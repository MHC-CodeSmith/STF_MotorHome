# Item 24 — Custo total dos materiais

<!-- revisao-final:inicio -->
> **Estado em 16/11/2026:** o resultado final está no [relatório](../../../relatorio/relatorio.pdf), seção 24 (p. 20). Para revisar e registrar o parecer, siga o [guia de revisão por integrante](../../../docs/REVISAO_INTEGRANTES.md). O texto abaixo é o histórico do desenvolvimento; onde ele disser "em desenvolvimento", vale o relatório.
<!-- revisao-final:fim -->

**Responsável:** P1 — Estrutura, freios, massa e custos  
**Enunciado / tarefa:** BOM em BRL, quantidades, taxas, impostos de importação e data das cotações.  
**Depende de:** I02 (P1), I03 (P1), I04 (P4), I05 (P4), I06 (P2), I07 (P2), I08 (P5), I09 (P2), I10 (P7), I11 (P6), I12 (P7), I13 (P6), I14 (P1), I15 (P1), I16 (P3), I18 (P1)  
**Status:** Em desenvolvimento — evidências parciais; revisão humana pendente.

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
