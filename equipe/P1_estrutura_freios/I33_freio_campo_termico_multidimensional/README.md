# Item 33 — Freio: campo térmico multidimensional

**Responsável:** P1 — Estrutura, freios, massa e custos
**Enunciado / tarefa:** Frenagem de 30m/s para 10m/s em 5s, 25°C inicial; calcular energia e campo térmico 2D/3D.
**Depende de:** I03 (P1), I18 (P1)
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

## Registro histórico de auditoria — 22/10/2026
O registro abaixo é histórico e foi superado pela reclassificação documentada em 12/11/2026 na seção “Interface contextual com I28”. A antiga aresta I28→I33 foi então removida do DAG de dependências de dados e preservada como relação contextual não bloqueante.

## Interface contextual com I28

I28 informa o limitador operacional nominal de 90 km/h para contextualizar a interpretação do ensaio do componente. Não é entrada necessária ao cálculo prescrito em I33 (30→10 m/s em 5 s, 25 °C): a energia cinética e a distribuição térmica são calculadas com massa de I18 e parâmetros de freio de I03. O início e a análise matemática de I33, portanto, não aguardam o resultado de aceleração/velocidade de I28. A condição de 108 km/h continua identificada como ensaio de componente especificado no trabalho acadêmico, acima do limitador, sem alegação de que o veículo atinja essa velocidade. A relação está registrada como contexto não bloqueante em `metadata/interfaces_contextuais.csv`.

## Revisão desta frente — 23/10/2026

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). O método disponível e seus limites estão em [frente térmica](../../../docs/FRENTE_TERMICA.md) e [verificação de requisitos](../../../docs/VERIFICACAO_CAD_APOSTILA.md). Casos sintéticos não são resultados finais.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
