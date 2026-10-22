# Contratos e interfaces de dados

## Forma preferencial para arquivos numéricos
- `.csv`: colunas com nomes e unidades, como `speed_km_h`, `power_wheel_kW`, `soc_fraction`.
- `.json` ou `.yaml`: valores nomeados com metadados, referência, autor, timestamp, `assumption_status` e versão.
- Origem: `measured`, `manufacturer`, `literature`, `calculated`, `simulated`, `assumed` (se provisório).
- Resultados consolidados **não** são digitados manualmente; gerados pelo script em `codigo/` e registrados em `resultados/`.

## Interface entre grupos
- P1: `mass_breakdown.csv`, `bill_of_materials.csv`, pneus e freios.
- P2: `battery_pack.yaml`, `electrical_limits.yaml`, temperaturas dos cabos.
- P3: `vehicle_geometry.yaml`, `drag_cfd.csv`, CAD/STEP/STL e imagens cotadas.
- P4: `motor_curves.csv`, `traction_curve.csv`, `resistive_forces.csv`, simulação de aceleração.
- P5: `pv_power_timeseries.csv`, `energy_balance.csv`, `range_vs_speed.csv`, `trip_schedule.csv`.
- P6: `cabin_surfaces.csv`, `aux_load_profile.csv`, temperatura e carga HVAC.
- P7: `battery_charge_temperature.csv`, `cooling_loop.csv`, curva de bomba e perfis térmicos.

Não preencher arquivos acima com dados não publicados/validados. Seu aparecimento no contrato é requisito de entrega, não alegação de existência.
