# Item 16 — Carenagem, portas, vidros

**Responsável:** P3 — Carroceria, CAD e CFD  
**Enunciado / tarefa:** Geometria e materiais da envoltória, portas, aberturas e vidros.  
**Depende de:** I15 (P1)  
**Status:** Em desenvolvimento — artefatos parciais; revisão humana pendente.

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

## Revisão desta frente — 23/10/2026

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). A [carroceria detalhada](../../../docs/CARROCERIA_DE_TRABALHO.md) substitui o bloco como geometria de trabalho. Não há CFD concluído.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
