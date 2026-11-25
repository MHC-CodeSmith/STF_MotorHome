# Item 23 — Capacidade das baterias (kWh)

<!-- revisao-final:inicio -->
> **Estado em 16/11/2026:** o resultado final está no [relatório](../../../relatorio/relatorio.pdf), seção 23 (p. 20). Para revisar e registrar o parecer, siga o [guia de revisão por integrante](../../../docs/REVISAO_INTEGRANTES.md). O texto abaixo é o histórico do desenvolvimento; onde ele disser "em desenvolvimento", vale o relatório.
<!-- revisao-final:fim -->

**Responsável:** P2 — Bateria, elétrica e fios  
**Enunciado / tarefa:** Dimensionar energia útil/nominal, SOC, limites e margens.  
**Depende de:** I06 (P2), I08 (P5), I13 (P6), I22 (P4)  
**Status:** Em desenvolvimento: proposta elétrica e dados OEM publicados; especificação final pendente.

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

## Base elétrica de trabalho

Proposta e fonte OEM conferida em [ARQUITETURA_ELETRICA.md](../../../docs/ARQUITETURA_ELETRICA.md). Dados parciais em [arquitetura_eletrica_proposta.yaml](../../../config/arquitetura_eletrica_proposta.yaml); lacunas permanecem explícitas. Não é aprovação da configuração física final.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1560_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
