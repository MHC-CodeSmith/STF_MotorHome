# Revisão final por integrante

Cada integrante revisa **a própria parte** antes da entrega (M6: 30/11; entrega oficial: 02/12, 06:00).
O repositório é público: dá para revisar tudo pelo navegador, sem instalar nada.

## Como revisar

1. Abra o relatório: [`relatorio/relatorio.pdf`](../relatorio/relatorio.pdf) (no GitHub, use *Download* se a prévia não carregar).
   Roteiro do vídeo em [`relatorio/roteiro_video.md`](../relatorio/roteiro_video.md).
2. Leia as seções dos seus itens (tabela abaixo; página pelo número impresso no rodapé).
3. Confira com o [checklist de aceitação](guia_revisao.md): enunciado, valores com unidade e fonte, método, hipóteses, figuras e limitações.
4. Para ver código e dados, cada item tem uma pasta em `equipe/` (`codigo/`, `dados/`, `resultados/`); o anexo de códigos está no fim do PDF.
5. Leia as decisões provisórias em que você aparece como responsável (lista abaixo; detalhes em [APROVACOES_FINAIS_PENDENTES.md](APROVACOES_FINAIS_PENDENTES.md)).
6. Registre o parecer abrindo uma *issue* com o modelo **Revisão do integrante**:
   [nova revisão](https://github.com/MHC-CodeSmith/STF_MotorHome/issues/new?template=revisao_integrante.yml).
   Precisa de conta no GitHub. Sem conta, mande o parecer no grupo do WhatsApp no mesmo formato (Pn, itens, aprovado ou correções).

Correção: diga o item, a página e o que muda (valor, fonte ou texto). Quem mantém o repositório aplica, recompila o PDF e responde na issue.

## Itens por integrante

### P1 — Estrutura, freios, massa e custo

| Item | Título | Página | Pasta |
|---|---|---|---|
| I01 | Nome e conceito do veículo | 4 | [`I01_nome_e_conceito_do_veiculo`](../equipe/P1_estrutura_freios/I01_nome_e_conceito_do_veiculo/README.md) |
| I02 | Pneus e rodas | 5 | [`I02_pneus_e_rodas`](../equipe/P1_estrutura_freios/I02_pneus_e_rodas/README.md) |
| I03 | Sistema de freios | 5 | [`I03_sistema_de_freios`](../equipe/P1_estrutura_freios/I03_sistema_de_freios/README.md) |
| I14 | Suspensão e direção | 12 | [`I14_suspensao_e_direcao`](../equipe/P1_estrutura_freios/I14_suspensao_e_direcao/README.md) |
| I15 | Chassi | 12 | [`I15_chassi`](../equipe/P1_estrutura_freios/I15_chassi/README.md) |
| I18 | Massa total com passageiros | 17 | [`I18_massa_total_com_passageiros`](../equipe/P1_estrutura_freios/I18_massa_total_com_passageiros/README.md) |
| I24 | Custo total dos materiais | 20 | [`I24_custo_total_dos_materiais`](../equipe/P1_estrutura_freios/I24_custo_total_dos_materiais/README.md) |
| I33 | Freio: campo térmico multidimensional | 25 | [`I33_freio_campo_termico_multidimensional`](../equipe/P1_estrutura_freios/I33_freio_campo_termico_multidimensional/README.md) |

Decisões provisórias com você entre os responsáveis: A01 (Variante OEM); A04 (Autonomia e módulos de serviços); A10 (Layout e isolamento); A11 (Módulos e ocupação do teto); A14 (Parâmetros físicos e validação); A16 (Orçamento instalado).

### P2 — Bateria, elétrica e cabos

| Item | Título | Página | Pasta |
|---|---|---|---|
| I06 | Bateria | 6 | [`I06_bateria`](../equipe/P2_bateria_eletrica/I06_bateria/README.md) |
| I07 | Fiação elétrica | 7 | [`I07_fiacao_eletrica`](../equipe/P2_bateria_eletrica/I07_fiacao_eletrica/README.md) |
| I09 | Controladores de carga e inversores | 10 | [`I09_controladores_de_carga_e_inversores`](../equipe/P2_bateria_eletrica/I09_controladores_de_carga_e_inversores/README.md) |
| I23 | Capacidade das baterias (kWh) | 20 | [`I23_capacidade_das_baterias_kwh`](../equipe/P2_bateria_eletrica/I23_capacidade_das_baterias_kwh/README.md) |
| I30 | Temperatura de cabos multidimensional | 24 | [`I30_temperatura_de_cabos_multidimensional`](../equipe/P2_bateria_eletrica/I30_temperatura_de_cabos_multidimensional/README.md) |

Decisões provisórias com você entre os responsáveis: A02 (Recarga DC direta ou buffer dedicado); A03 (Alocação FV e MPPT compartilhado); A04 (Autonomia e módulos de serviços); A05 (Inversor de serviços); A06 (Climatização); A07 (Geladeira AC); A08 (Cozinha e lavanderia); A09 (Boiler e rede potável); A11 (Módulos e ocupação do teto); A12 (Barramento DC secundário); A13 (Política e reservas da missão); A15 (Proteções, controle e monitoramento).

### P3 — Carroceria, CAD e CFD

| Item | Título | Página | Pasta |
|---|---|---|---|
| I16 | Carenagem, portas, vidros | 13 | [`I16_carenagem_portas_vidros`](../equipe/P3_carroceria_cad_cfd/I16_carenagem_portas_vidros/README.md) |
| I17 | CAD 3D e vistas cotadas | 13 | [`I17_cad_3d_e_vistas_cotadas`](../equipe/P3_carroceria_cad_cfd/I17_cad_3d_e_vistas_cotadas/README.md) |
| I19 | Coeficiente de arrasto e CFD | 17 | [`I19_coeficiente_de_arrasto_e_cfd`](../equipe/P3_carroceria_cad_cfd/I19_coeficiente_de_arrasto_e_cfd/README.md) |

Decisões provisórias com você entre os responsáveis: A03 (Alocação FV e MPPT compartilhado); A04 (Autonomia e módulos de serviços); A06 (Climatização); A07 (Geladeira AC); A08 (Cozinha e lavanderia); A09 (Boiler e rede potável); A10 (Layout e isolamento); A11 (Módulos e ocupação do teto); A14 (Parâmetros físicos e validação).

### P4 — Motor, transmissão e dinâmica

| Item | Título | Página | Pasta |
|---|---|---|---|
| I04 | Motor elétrico | 6 | [`I04_motor_eletrico`](../equipe/P4_motor_dinamica/I04_motor_eletrico/README.md) |
| I05 | Transmissão | 6 | [`I05_transmissao`](../equipe/P4_motor_dinamica/I05_transmissao/README.md) |
| I20 | Resistência de rolamento | 19 | [`I20_resistencia_de_rolamento`](../equipe/P4_motor_dinamica/I20_resistencia_de_rolamento/README.md) |
| I21 | Forças resistivas versus velocidade | 19 | [`I21_forcas_resistivas_versus_velocidade`](../equipe/P4_motor_dinamica/I21_forcas_resistivas_versus_velocidade/README.md) |
| I22 | Potência resistiva e tração | 20 | [`I22_potencia_resistiva_e_tracao`](../equipe/P4_motor_dinamica/I22_potencia_resistiva_e_tracao/README.md) |
| I28 | Velocidade máxima e 0–100 km/h | 23 | [`I28_velocidade_maxima_e_0100_km_h`](../equipe/P4_motor_dinamica/I28_velocidade_maxima_e_0100_km_h/README.md) |

Decisões provisórias com você entre os responsáveis: A01 (Variante OEM); A13 (Política e reservas da missão); A14 (Parâmetros físicos e validação).

### P5 — Solar, autonomia e otimização

| Item | Título | Página | Pasta |
|---|---|---|---|
| I08 | Painel fotovoltaico | 8 | [`I08_painel_fotovoltaico`](../equipe/P5_solar_autonomia/I08_painel_fotovoltaico/README.md) |
| I25 | Autonomia usando somente solar | 21 | [`I25_autonomia_usando_somente_solar`](../equipe/P5_solar_autonomia/I25_autonomia_usando_somente_solar/README.md) |
| I26 | Consumo (km/kWh) | 22 | [`I26_consumo_km_kwh`](../equipe/P5_solar_autonomia/I26_consumo_km_kwh/README.md) |
| I27 | Autonomia diária com SOC final 30% | 22 | [`I27_autonomia_diaria_com_soc_final_30`](../equipe/P5_solar_autonomia/I27_autonomia_diaria_com_soc_final_30/README.md) |
| I29 | Otimização viagem 7000 km | 23 | [`I29_otimizacao_viagem_7000_km`](../equipe/P5_solar_autonomia/I29_otimizacao_viagem_7000_km/README.md) |

Decisões provisórias com você entre os responsáveis: A02 (Recarga DC direta ou buffer dedicado); A03 (Alocação FV e MPPT compartilhado); A11 (Módulos e ocupação do teto); A13 (Política e reservas da missão).

### P6 — Interior, climatização e cabine

| Item | Título | Página | Pasta |
|---|---|---|---|
| I11 | HVAC e ventilação interna | 10 | [`I11_hvac_e_ventilacao_interna`](../equipe/P6_interior_cabine/I11_hvac_e_ventilacao_interna/README.md) |
| I13 | Materiais e equipamentos internos | 11 | [`I13_materiais_e_equipamentos_internos`](../equipe/P6_interior_cabine/I13_materiais_e_equipamentos_internos/README.md) |
| I31 | Cabine fechada ao meio-dia | 25 | [`I31_cabine_fechada_ao_meio_dia`](../equipe/P6_interior_cabine/I31_cabine_fechada_ao_meio_dia/README.md) |
| I32 | Potência térmica de A/C | 25 | [`I32_potencia_termica_de_a_c`](../equipe/P6_interior_cabine/I32_potencia_termica_de_a_c/README.md) |

Decisões provisórias com você entre os responsáveis: A04 (Autonomia e módulos de serviços); A06 (Climatização); A07 (Geladeira AC); A08 (Cozinha e lavanderia); A09 (Boiler e rede potável); A10 (Layout e isolamento); A12 (Barramento DC secundário); A14 (Parâmetros físicos e validação); A15 (Proteções, controle e monitoramento).

### P7 — Arrefecimento e térmica da bateria

| Item | Título | Página | Pasta |
|---|---|---|---|
| I10 | Resfriamento de componentes elétricos | 10 | [`I10_resfriamento_de_componentes_eletricos`](../equipe/P7_arrefecimento/I10_resfriamento_de_componentes_eletricos/README.md) |
| I12 | Sistema de lubrificação | 11 | [`I12_sistema_de_lubrificacao`](../equipe/P7_arrefecimento/I12_sistema_de_lubrificacao/README.md) |
| I34 | Temperatura da bateria em carga | 26 | [`I34_temperatura_da_bateria_em_carga`](../equipe/P7_arrefecimento/I34_temperatura_da_bateria_em_carga/README.md) |
| I35 | Bomba, radiador e vazão | 26 | [`I35_bomba_radiador_e_vazao`](../equipe/P7_arrefecimento/I35_bomba_radiador_e_vazao/README.md) |

Decisões provisórias com você entre os responsáveis: A14 (Parâmetros físicos e validação); A15 (Proteções, controle e monitoramento).

**Parecer registrado (16/11/2026):** [PARECER_P7_HERICK_ELISEU.md](PARECER_P7_HERICK_ELISEU.md), Herick Eliseu
(issue [#3](https://github.com/MHC-CodeSmith/STF_MotorHome/issues/3), PR [#2](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/2)).
Aprovado com correções: 6 obrigatórias e 5 recomendadas, com página e o que muda; A14 e A15 comentadas.

## Registro dos pareceres

| Integrante | Nome | Data | Parecer | Issue |
|---|---|---|---|---|
| P1 | | | pendente | |
| P2 | Mateus | 20/11/2026 | correções em I07, I23, I30 e I34 ([documento](CORRECOES_TERMICAS_E_BITOLA_2026-11.md)); incorporadas | PR [#5](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/5) |
| P3 | Sabrina Seba | 19/11/2026 | correções em I16, I17 e I19; incorporadas | PR [#4](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/4) |
| P4 | Victor | 23/11/2026 | aprovado com correções em I02, I20 e I28 (raio do item 28, equação de aceleração e justificativa do Cr); contas de I04, I05, I20, I21, I22 e I28 conferidas; incorporadas | PR [#6](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/6) |
| P5 | | | pendente | |
| P6 | Amanda | 19/11/2026 | aprovado sem correções (WhatsApp); o déficit do A/C com 62 m³/h (2,87 kW contra 2,7 kW) já estava descrito no item 32; depois, em 23/11, o grupo resolveu o déficit com a cortina refletiva do para-brisa (2,31 kW) | — |
| P7 | Herick Eliseu | 16/11/2026 | aprovado com correções ([parecer](PARECER_P7_HERICK_ELISEU.md)); as seis obrigatórias aplicadas | [#3](https://github.com/MHC-CodeSmith/STF_MotorHome/issues/3) (PR [#2](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/2)) |

Atualizar esta tabela quando cada issue for fechada. O P7 registrou o parecer por pull request, com o texto completo
em `docs/` e os mesmos campos do modelo de issue. A aprovação não remove as ressalvas técnicas do relatório
(por exemplo, a interface CC solar → tração, B01, continua hipótese).
