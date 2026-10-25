# Item 21 — Forças resistivas versus velocidade

**Responsável:** P4 — Motor, transmissão e dinâmica  
**Enunciado / tarefa:** Produzir força aerodinâmica e de rolamento versus velocidade; cenário plano e sem vento.  
**Depende de:** I18 (P1), I19 (P3), I20 (P4)  
**Status:** Em desenvolvimento — forças de sensibilidade condicionadas, não aprovadas.

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

## Integração energética e otimização

Métodos, equações, hipóteses e resultados rastreáveis em [ENERGIA_E_OTIMIZACAO.md](../../../docs/ENERGIA_E_OTIMIZACAO.md). Resultados são condicionados; não substituem dados reais nem aprovação. A limitação de oito horas diárias é aplicada a I29, não a I27.
