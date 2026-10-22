# Item 26 — Consumo (km/kWh)

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Distância percorrida por energia elétrica da bateria (km/kWh) a 40 e 80 km/h; explicitar auxiliares.
**Depende de:** I21 (P4), I22 (P4), I23 (P2), I13 (P6)  
**Status:** Não iniciado (estrutura criada automaticamente).

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
Enunciado original, p. 2, item 26: distância por consumo da bateria em km/kWh. A redação anterior “consumo energético por km” descrevia a razão inversa. O título e a unidade foram preservados; a teoria ainda é template e deve receber a mesma correção ao ser desenvolvida.
