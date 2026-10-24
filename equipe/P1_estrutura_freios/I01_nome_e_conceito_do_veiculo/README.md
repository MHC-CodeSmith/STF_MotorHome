# Item 01 — Nome e conceito do veículo

**Responsável:** P1 — Estrutura, freios, massa e custos  
**Enunciado / tarefa:** Definir nome, referência e requisitos de veículo habitável para pelo menos duas pessoas.  
**Depende de:** Requisitos gerais e decisões de conceito  
**Status:** Em desenvolvimento: conceito BEV Aurora Solar documentado; revisão final pendente.

## Conceito de trabalho

Motorhome elétrico solar para pelo menos duas pessoas, proposto sobre E-Ducato MY25 L3H2 de 4250 kg. Motor elétrico OEM, bateria de tração e integração solar a dimensionar. Arquitetura, diagrama, ficha conferida e pendências em [ARQUITETURA_ELETRICA.md](../../../docs/ARQUITETURA_ELETRICA.md); entradas em [arquitetura_eletrica_proposta.yaml](../../../config/arquitetura_eletrica_proposta.yaml). A malha detalhada atual é referência de carroceria e precisa de adaptação às cotas dessa variante.

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
