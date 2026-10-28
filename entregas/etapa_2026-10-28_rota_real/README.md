# Etapa28/10 — rota rodoviária e revisão dos35itens

- [Revisão visual dos35itens](revisao_35_itens.html): mapa, comparação e pendências por item.
- [Revisão em texto](REVISAO_35_ITENS.md).
- [Método, hipóteses e resultados](../../docs/ROTA_REAL_2026-10-28.md).
- [Resumo dos sete cenários](resumo_rota_real.json).
- [QA do replay](qa_rota.json): fontes solares, velocidades, energia, reservas e8h/dia.
- [Mapa e progresso](rota_e_progresso.png).

CorredorOSRM/OSM de7511,282km por21pontos. Marco7000km mantido dentro da
geometria real. Céu limpo sazonal eERA5horário, relevo5km, tetos de cruzeiro
60/80/90km/h reduzidos pelo trecho e limitador do veículo. Partida21/06/2025,
para reconstituição histórica; limites por trecho são aproximações.

No cenário de céu limpo, chegada aoChuí em330,93/428,92/430,92dias.
Com a política e as cargas atuais, os casosERA5 interrompem por reserva dos
serviços após4112,66/3462,12/3459,51km. Interface de cargaOEM continua
hipotética. A viagem ainda não tem certificado de menor tempo global.

Arquivos`*_agenda.csv.gz` e`*_conducao.csv.gz` são os CSV completos comprimidos
sem perda. O resumo registra hashes dos CSV descomprimidos; o manifesto de
compactação também registra os arquivos distribuídos. Python/pandas abre
`.csv.gz` diretamente. As séries`*_dias.csv` são resumos para leitura rápida.

Reabrir e verificar:

```bash
.venv/bin/python scripts/verificar_rota_real.py entregas/etapa_2026-10-28_rota_real --fontes /home/mhc/motorhome_referencias_tarefas/rota-litoral-fontes-02
```

FonteOSRM/ERA5bruta no cache externo, URLs eSHA256 em`fontes_rota.json`.
Atribuição:©OpenStreetMap contributors/ODbL;OSRM;Open-Meteo/ERA5;
CopernicusDEM2021GLO90,DOI10.5270/ESA-c5d3d65. O traçado não verifica placas,
restrições locais ou disponibilidade de estacionamento para os painéis.

178testes passaram. Revisão física/humana e os fechamentos da matriz continuam
pendentes. MemorialPDF e visualizador26/10 ainda precisam receber estes suplementos.
