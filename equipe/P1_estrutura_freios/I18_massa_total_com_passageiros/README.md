# Item 18 — Massa total com passageiros

**Responsável:** P1 — Estrutura, freios, massa e custos  
**Enunciado / tarefa:** Somar massas documentadas por componente, passageiros, água, bagagem e cargas.  
**Depende de:** I02 (P1), I03 (P1), I04 (P4), I05 (P4), I06 (P2), I07 (P2), I08 (P5), I09 (P2), I10 (P7), I11 (P6), I12 (P7), I13 (P6), I14 (P1), I15 (P1), I16 (P3), I17 (P3)
**Status:** Em desenvolvimento parcial; revisão humana pendente.

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

## Correção de auditoria — 22/10/2026
I07 (fiação) e I10 (arrefecimento) também entregam massa. Proveniência: enunciado, p. 1, itens 7, 10 e 18; I24 já inclui ambos no CSV inicial. A teoria continua template e sua lista histórica de dependências precisa ser atualizada quando for desenvolvida.

## Cobertura e integração interior - 25/10/2026

[CAD, fontes, modelos de sombra, equipamentos e orçamento de massa](../../../docs/EXPANSAO_SOLAR_E_INTERIOR.md). Não promove as propostas a engenharia aprovada.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
