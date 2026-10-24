# Item 06 — Bateria

**Responsável:** P2 — Bateria, elétrica e fios  
**Enunciado / tarefa:** Escolher células/pack/BMS: tecnologia, tensão, massa, limites, curva e segurança.  
**Depende de:** I04 (P4)  
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
