# Item 26 — Consumo (km/kWh)

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Distância percorrida por energia elétrica da bateria (km/kWh) a 40 e 80 km/h; explicitar auxiliares.
**Depende de:** I21 (P4), I22 (P4), I23 (P2), I13 (P6)  
**Status:** Em desenvolvimento — curvas de sensibilidade condicionadas, não aprovadas.

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

## Integração energética e otimização

Métodos, equações, hipóteses e resultados rastreáveis em [ENERGIA_E_OTIMIZACAO.md](../../../docs/ENERGIA_E_OTIMIZACAO.md). Resultados são condicionados; não substituem dados reais nem aprovação. A limitação de oito horas diárias é aplicada a I29, não a I27.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
