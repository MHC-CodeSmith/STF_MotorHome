# Suplemento27/10 — interface de carga

Modelo condicionado de I09/I27/I29 com solar12/48V separado, carga0/6/8/10A,
perdas por ramo e perfil horário residencial. **Aceitação OEM não comprovada.**

- [Método, fontes e limites](../../docs/INTERFACE_CARGA_2026-10-27.md).
- [Com interface hipotética](com_interface_hipotetica/resumo_interface_carga.json): I27,344,767978km; viagem construtiva7000km/276dias completos, não mínimo global.
- [Sem interface](sem_interface/resumo_interface_carga.json): controle I27,326,402651km.
- [Gráfico](com_interface_hipotetica/interface_i27.png): velocidade, corrente discreta e SOC por bateria.
- [Viagem completa](com_interface_hipotetica/viagem_7000km.csv): inclui espera, montagem, correntes e energia.

JSON registra SHA256 das entradas/CSV. Reabrir com
`scripts/verificar_interface_carga.py CAMINHO_DA_SUBPASTA`.
O manual primário do candidato fica no cache externo, sem redistribuição.
PDF e visualizador anteriores preservados; suplemento ainda não incorporado ao memorial.
