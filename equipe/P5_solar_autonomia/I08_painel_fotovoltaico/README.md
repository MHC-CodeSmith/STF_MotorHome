# Item 08 — Painel fotovoltaico

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Área, eficiência, tecnologia, potência, massa, montagem e configuração.  
**Depende de:** I17 (P3)  
**Status:** Em desenvolvimento: módulo candidato e geração condicionada calculados; montagem e conversão pendentes.

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

## Execução de 24/10/2026

[Estimativa solar, fontes e hipóteses](../../../docs/AVANCO_2026-10-24.md), configuração `config/solar_proposta.yaml` e script `scripts/calcular_solar.py`. Dois/três módulos são cenários a verificar na montagem. Não são ainda energia útil comprovada na bateria de tração.

## Cobertura e integração interior - 25/10/2026

[CAD, fontes, modelos de sombra, equipamentos e orçamento de massa](../../../docs/EXPANSAO_SOLAR_E_INTERIOR.md). Não promove as propostas a engenharia aprovada.
