# Item 29 — Otimização viagem 7000 km

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Otimizar velocidade/horário para Belém–Chuí: só bateria inicial e solar, <=8h dirigindo por dia.  
**Depende de:** I25 (P5), I26 (P5), I27 (P5), I23 (P2)  
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

## Avanço28/10 — rodovias e calendário reais

[Rota costeiraOSRM7511km e marco7000km](../../../docs/ROTA_REAL_2026-10-28.md),
velocidades aproximadas por trecho/relevoDEM, solar por local/data eERA5horário.
Sete casos com CSV reabertos: céu limpo60km/h chegaChuí330,93dias; casos
históricos interrompem por reserva dos serviços. [Entrega/QA](../../../entregas/etapa_2026-10-28_rota_real/README.md).
178testes passaram; falta gestão com previsão/reserva, interface física e mínimo global.
