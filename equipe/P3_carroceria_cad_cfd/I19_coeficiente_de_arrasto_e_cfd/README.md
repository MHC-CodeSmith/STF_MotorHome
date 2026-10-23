# Item 19 — Coeficiente de arrasto e CFD

**Responsável:** P3 — Carroceria, CAD e CFD  
**Enunciado / tarefa:** Simular CFD; obter Cd, área frontal; documentar malha, domínio, solver, contornos e convergência.  
**Depende de:** I17 (P3)  
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
