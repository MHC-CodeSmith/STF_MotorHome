# Item 31 — Cabine fechada ao meio-dia

**Responsável:** P6 — Interior, conforto e cabine  
**Enunciado / tarefa:** Estacionada, sem A/C nem passageiros, meio-dia, insolação e balanço térmico. Justificar estado transiente/estacionário.  
**Depende de:** I11 (P6), I13 (P6), I16 (P3), I17 (P3), I08 (P5)  
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

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). O método disponível e seus limites estão em [frente térmica](../../../docs/FRENTE_TERMICA.md) e [verificação de requisitos](../../../docs/VERIFICACAO_CAD_APOSTILA.md). Casos sintéticos não são resultados finais.
