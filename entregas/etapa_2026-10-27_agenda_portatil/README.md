# Etapa 27/10 — agendas com solar portátil

Continuação técnica: [interface de carga](../etapa_2026-10-27_interface_carga/README.md),
com PV12/48V separado e perdas explícitas. Os resultados desta pasta são a
comparação anterior sob hipóteses agregadas; foram preservados com seus hashes.

Suplemento técnico condicionado; 35 itens em desenvolvimento, nenhum aprovado.
Método, hipóteses e comandos em [AGENDA_PORTATIL_2026-10-27.md](../../docs/AGENDA_PORTATIL_2026-10-27.md).

- [Grade30min](grade30/resumo_agenda_portatil.json): dois casos I27 e política construtiva I29 de7000km, até202dias completos e8h/dia. Não é menor tempo global.
- [Grade15min](grade15/resumo_agenda_portatil.json): comparação I27, diferença0,04213% com interface hipotética.
- [Figura I27](grade30/agenda_i27.png): velocidade/demanda terminal e SOC separado das baterias.
- [Viagem completa](grade30/i29_viagem_7000km.csv): inclui noites, estados do portátil, energia e condução diária.

Cada resumo registra SHA256 das entradas e dos CSV. O verificador reabre os CSV,
reconstitui cronologia/energia e confere os hashes. A interface HV de2kW/90% é
hipotética. Teto e portátil reutilizam os perfis solares conferidos da entrega26/10.
Este suplemento ainda não foi incorporado ao memorial/visualizador anteriores.
