# Item 30 — Temperatura de cabos multidimensional

**Responsável:** P2 — Bateria, elétrica e fios  
**Enunciado / tarefa:** Potência máxima do motor; perdas Joule com resistividade dependente da temperatura; simulação 2D/3D.  
**Depende de:** I04 (P4), I07 (P2)  
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

## Avanço de 26/10/2026 — cabos r–theta

Método/casos, hipóteses, fontes e convergência em [cabos e radiador](../../../docs/CABOS_E_RADIADOR_2D.md). Resultados reproduzíveis em [resumo](resultados/resumo_cabos.json); o requisito continua parcial e sem aprovação humana.
