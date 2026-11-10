# Item 27 — Autonomia diária com SOC final 30%

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Determinar autonomia máxima diária, perfil v(t), Pmotor(t) e SOC final alvo de 30%, com tolerância numérica do solver a declarar e justificar.
**Depende de:** I23 (P2), I25 (P5), I26 (P5)  
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

## Proveniência da correção — 22/10/2026
Enunciado original, p. 2, item 27: carga final de 30% da carga máxima. O antigo `>=30%` ampliava o cenário; foi corrigido para alvo de 30%, sem definir tolerância nem SOC inicial. O YAML preserva o nome histórico `minimum_soc_fraction_daily`; esta auditoria não o altera nem aprova outra interpretação.

## Revisão desta frente — 23/10/2026

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). O método disponível e seus limites estão em [frente térmica](../../../docs/FRENTE_TERMICA.md) e [verificação de requisitos](../../../docs/VERIFICACAO_CAD_APOSTILA.md). Casos sintéticos não são resultados finais.

## Execução de 24/10/2026

Progresso e limites atualizados em [geometria, CFD, solar e otimização](../../../docs/AVANCO_2026-10-24.md). Artefatos de revisão em [entrega parcial](../../../entregas/parcial_2026-10-24/README.md); não há aprovação final de engenharia.

## Integração energética e otimização

Métodos, equações, hipóteses e resultados rastreáveis em [ENERGIA_E_OTIMIZACAO.md](../../../docs/ENERGIA_E_OTIMIZACAO.md). Resultados são condicionados; não substituem dados reais nem aprovação. A limitação de oito horas diárias é aplicada a I29, não a I27.

## Atualização27/10 — portátil e bancos separados

[Modelo, hipóteses e resultados atuais](../../../docs/AGENDA_PORTATIL_2026-10-27.md).
[CSV/figuras/JSON](../../../entregas/etapa_2026-10-27_agenda_portatil/README.md).
Reprodução: `scripts/calcular_agenda_portatil.py`; verificação dos CSV:
`scripts/verificar_agenda_portatil.py`. Configuração própria, global preservado.
I27: SOC final30% exato, sem limite8h; potência de eixo ainda desconhecida.
I29:7000km/até8h diárias, política construtiva, não ótimo de tempo.
Transferência HV é hipótese, sem integração OEM comprovada.

Continuação: [interfaceAC discreta e PV12/48V separado](../../../docs/INTERFACE_CARGA_2026-10-27.md).
O cenário atual usa344,768kmI27 e construção276diasI29; as agendas anteriores
são comparações preservadas. AceitaçãoOEM e revisão humana continuam pendentes.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
