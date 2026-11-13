# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Fontes — item 29

| Fonte | URL/DOI | Página/tabela/seção | Dados extraídos | Data de acesso | Licença/uso |
|---|---|---|---|---|---|
| Enunciado2026 fornecido | `docs/fontes_recebidas/Projeto Sist. Térmicos e Fluídicos 2026.pdf` | p.2,I27/I29 | SOC30%;7000km/8h/dia | Trecho local conferido27/10/2026 | Documento da disciplina; não redistribuir sem autorização |
| Perfis solares/proposta elétrica anteriores | [Dossiê](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md) | Solar/serviços e YAMLs citados | Teto1540W, portátil4x400W, serviços10,24kWh | Fontes26/10; reuso27/10 | Sem nova importação; URLs/hashes preservados |

Hipóteses novas de operação: [etapa27/10](../../../docs/AGENDA_PORTATIL_2026-10-27.md).
Não são dados novos do fabricante.

Nova fonte primária: [manualNRGkick2602-04-1](https://nrgkick.com/wp-content/uploads/Bedienungsanleitung-DE-EN-FR-NL-TR.pdf),
p20 conferida27/10; candidatoEVSE50/60Hz, não evidência de aceitaçãoOBCMY25.
Hashes/registro no [dossiê da interface](../../../docs/INTERFACE_CARGA_2026-10-27.md).

Fontes externas candidatas ficam em `fontes_externas/catalogo.csv`; citar apenas as realmente utilizadas.

28/10:OSRM/OpenStreetMap, Open-Meteo/ERA5 eCopernicusDEM2021GLO90, todos
comURLs eSHA256 registrados no [dossiê](../../../docs/ROTA_REAL_2026-10-28.md)
e emfontes_rota.json da entrega. Atribuir©OpenStreetMap contributors/ODbL;
Open-Meteo/ERA5 eDOI10.5270/ESA-c5d3d65 paraDEM. Fontes brutas no cache externo.

<!-- execucao-integrada:inicio -->
Fontes específicas da execução (não representam aprovação da instalação):

- `oem_sk`: https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf; consulta/revisão: 2026-03-20. Origem: fabricante.
- `maxeon3_2022`: https://sunpower.maxeon.com/int/sites/default/files/2022-05/sp_max3_104c_com_380-400_dc_ds_en_a4_544454.pdf; consulta/revisão: 2026-11-10. Origem: ficha_fabricante_espelho.
  Espelho original conferido: https://solsol.eu/file/view/1080/sunpower-spr-max3-400wp-com_en.pdf;SHA256 `d6c76ef9231cb1621d8401a46fbef617724e6bc6ea873bb3f4658261fef75757`.
- `pylon`: https://en.pylontech.com.cn/products/c23/134.html; consulta/revisão: 2026-11-09. Origem: fabricante.
- `venema`: https://4x4electric.com/charging-technique/; consulta/revisão: 2026-11-09. Origem: relato_primario_outro_veiculo.
- `sungrow`: https://uk.sungrowpower.com/upload/file/20221215/EN%20FS%20IDC30E%20DC%20Charger%20Factsheet.pdf; consulta/revisão: 2026-11-09. Origem: fabricante.
- `hyp`: hipotese_engenharia; consulta/revisão: 2026-11-09. Origem: hipotese_engenharia.

Evidência técnica: `entregas/integrado_maxeon1540/otimizacao_resolucao_temporal/resumo.json`. Condições/hipóteses constam no YAML;valoresOEM não publicados permanecem desconhecidos.
<!-- execucao-integrada:fim -->
