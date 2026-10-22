# Item 34 — Temperatura da bateria em carga

**Responsável:** P7 — Bateria térmica e arrefecimento  
**Enunciado / tarefa:** Modelar temperatura do pack em carregadores 20 e 80 kW; limites de corrente, calor e arrefecimento.  
**Depende de:** I06 (P2), I07 (P2), I09 (P2), I10 (P7), I23 (P2)  
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
