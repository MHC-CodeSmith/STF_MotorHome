# Revisão dos35itens após avanço na rota —28/10/2026

Rota rodoviária costeira:7511.3km. FontesOSRM/OSM, relevoCopernicus eERA5. Dados/modelos rastreados no suplemento.

## Novos resultados de viagem

| Cenário | Progresso(km) | Dia7000km | DiaChuí | Estado |
|---|---:|---:|---:|---|
| clear_60 | 7511.28 | 296.93 | 330.93 | arrived |
| clear_80 | 7511.28 | 387.92 | 428.92 | arrived |
| clear_90 | 7511.28 | 390.92 | 430.92 | arrived |
| era5_60 | 4112.66 | — | — | service_reserve_violation_predicted |
| era5_80 | 3462.12 | — | — | service_reserve_violation_predicted |
| era5_90 | 3459.51 | — | — | service_reserve_violation_predicted |
| clear_80_sem_interface | 242.43 | — | — | traction_stranded_without_interface |

Os dias são tempo decorrido desde21/06/2025. Uma política que interrompe por reserva indica a primeira falha daquela gestão; não estabelece inviabilidade de toda arquitetura.

## Evidências e falta concreta por item

| Item | Requisito | O que já existe | O que ainda falta |
|---|---|---|---|
| 01/P1 | Nome do carro e conceito elétrico solar | Parcial: proposta BEV Aurora Solar, E-Ducato MY25 L3H2; arquitetura e fonte OEM conferidas | Definir nome, arquitetura, duas pessoas e configuração coerente; registrar decisão |
| 02/P1 | Pneus/rodas, inclusive pressão, material, dimensões e peso | Parcial: Continental225/75R16C artigo04514690000 documentado; diâmetro0,74422m/massa16,919kg; pressão operacional e roda pendentes | Escolher pneu/roda com capacidade de carga, pressão e raio efetivo documentados |
| 03/P1 | Sistema de freios especificado | Referência Brembo300×32 ventilado pesquisada; compatibilidadeMY25 pendente; [I33 condicionado](FREIOS_2D.md) | Confirmar peça exata/pinça/pastilha, propriedades, cotas, massas e distribuição |
| 04/P4 | Motor: potência máxima, curvas de torque, potência e eficiência por RPM | Parcial: motor OEM elétrico 205 kW/410 Nm; curvas/mapas ainda ausentes | Selecionar motor elétrico compatível e obter mapas/limites citados |
| 05/P4 | Transmissão especificada | Redutor fixo OEM retido, arquitetura confirmada porFiatDE; relação/rendimento/RPM pendentes | Obter relação total e limites/perdas, preservando varianteSK |
| 06/P2 | Bateria especificada | Parcial: OEM110/98kWh400V com envelope CAD estimado; serviços2NG51,2V100Ah paralelo+LynxBMSNG; perdas/massa OEM pendentes | Definir célula/pack/BMS, tensão, capacidades, massa, curvas e limites |
| 07/P2 | Fiação elétrica | Parcial: rotasCAD conceituais; manual de serviços70mm²/fusível200A e sensibilidadeI²R/queda; cabo de tração e isolamento pendentes | Documentar percursos, bitolas, corrente RMS/DC correta, isolamento, perdas e proteção |
| 08/P5 | Painéis: área, eficiência e tecnologia | Teto1540W e portátil1600W documentados/modelados; solar12/48V separado; geração agora calculada ao longo da rota/data. | Confirmar montagem/fixações, sombras, curvaIV, clippingMPPT e perdas; refinar dados meteorológicos da rota |
| 09/P2 | Controladoras e inversores com eficiências | Parcial: MPPT150/35 principal+opcional e100/20 a12V; MultiPlus-II48/5000,Orion48/12-30,banco10,24kWh eBMS dimensionados noCAD; EVSE/circuitos e curvas pendentes | Compatibilizar tensão/corrente/MPPT/inversor e mapas de eficiência reais |
| 10/P7 | Resfriamento de componentes elétricos | Dois circuitos propostos; bateriaECM e ponto hidráulico Bosch+campos em [integração](FECHAMENTO_TERMICO_E_MISSAO.md) | Confirmar perdas/UA/limites reais, ventilação e integrar fisicamente |
| 11/P6 | A/C, aquecimento e ventilação | Parcial: FreshWell3000 sob cama modelado628x400x286mm/21kg;2700W frio vs2646W carga nominal estimada; curva/dutos e cenários altos pendentes | Dimensionar ciclo/equipamento após cargas de cabine; fornecer potência elétrica a P5 |
| 12/P7 | Lubrificação | Escopo de lubrificaçãoBEV identificado; reterOEM, sem óleo de motor diesel. Grau/volume do redutor pendentes | Identificar pontos a lubrificar, fluido, circuito, vazão/perdas e fichas |
| 13/P6 | Materiais/equipamentos internos, incluindo assentos, mobiliário, banheiro, eletrônicos, fogão, geladeira, lavadora/secadora | Parcial:7equipamentos internos/157sólidos; induçãoIE3TP220V60Hz2000W substitui50Hz; garagem/armário técnico,serviços e dutos em conjunto adicional208sólidos; montagem/ergonomia pendentes | Escolher equipamentos e materiais reais; conferir portas/rodas/isolamento/ergonomia; BOM/cargas/fontes |
| 14/P1 | Suspensão/direção | ArquiteturaOEM elétrica pesquisada: pseudo-MacPherson/feixes reforçados/EPS; referênciaUK, sem placaSK | Definir eixos, cargas, geometria e compatibilidade com massa montada |
| 15/P1 | Chassi e dimensões | Parcial: cotas/limite/massa OEM; malha adaptada às cotas-alvo L3H2, não CAD OEM | Vincular chassi real à variante escolhida, cotas, massa e limites de carga |
| 16/P3 | Carenagem, portas, aberturas e vidros | Parcial: exterior Ducato importado com portas, vidros e espelhos | Conferir escala/variante e definir materiais, espessuras e aberturas do motorhome |
| 17/P3 | Geometria 3D e três vistas com cotagem principal | Parcial: exterior detalhado+interior157sólidos+tração/serviços208sólidos STEP/GLB; coberturas; viewer23seletores e vista técnica; tração estimada,não CAD OEM | Adaptar interior e instalações; conferir dimensões contra ficha real e completar desenho técnico |
| 18/P1 | Massa montada com passageiros | Subtotal conhecido com portátil3458,605kg; taraOEM inclui tração. Ainda não massa completa/eixos. | Somar componentes sem sobreposição, incluindo I07/I10, água, carga e passageiros; conferir eixos/CG |
| 19/P3 | Cd e área frontal com CFD | Parcial: três malhas29527/63668/166212células convergidas, Cd0,653/0,625/0,581; mudança final7,07%; refino com camadas rejeitado | Resolver camadas/y+, rodas, geometria e estudo de independência; sem Cd final validado |
| 20/P4 | Coeficiente de rolamento Cr | ComparaçãoCamper0451473 classeC2/C:Cr0,0068–0,0080 de rótulo, não adoção nem medição no A/S | Obter coeficiente com carga/pressão/superfície e fonte apropriadas |
| 21/P4 | Forças aerodinâmica e rolamento versus velocidade | Parcial:324cenários explícitos Cd/Cr/eta/velocidade; forças tabeladas, não dados aprovados Novo estudo integra consumo por trecho com velocidade aproximada e relevoDEM. | Substituir hipóteses por massa/Cd/Cr/rho validados |
| 22/P4 | Potência resistiva e tração versus velocidade | Parcial: potência nas rodas/terminais nos324cenários; curva disponível real ausente Novo estudo integra consumo por trecho com velocidade aproximada e relevoDEM. | Integrar transmissão, motor, mapas de perdas e limites elétricos |
| 23/P2 | Capacidade das baterias em kWh | Parcial: 110 kWh brutos/98 úteis da ficha; adequação à missão ainda pendente | Dimensionar nominal/útil e janela de SOC a partir de componentes e uso definidos |
| 24/P1 | Custo dos materiais em R$, incluindo impostos | BOM27linhas/20linhas nãoOEM sem oferta registrada; referênciaIE3TPR$439, sem preço final/taxas confirmados | Consolidar BOM, cotações datadas, quantidade, transporte e tributação aplicável com fonte |
| 25/P5 | Autonomia com solar do dia a 40/80 km/h e gráfico versus velocidade | Teto atual1540W:17,89–31,80km@40/10,85–16,68km@80 antes da habitação; grade condicionada20–90km/h | Fechar interfaceHV/perdas e demanda; portátil como alternativa parada |
| 26/P5 | km/kWh da bateria a 40/80 km/h | Parcial:3,25–5,78@40 e1,97–3,03@80 na grade de hipóteses, não faixas medidas Novo estudo integra consumo por trecho com velocidade aproximada e relevoDEM. | Integrar mapas terminal–rodas e auxiliares reais, preservando km/kWh |
| 27/P5 | Máxima autonomia diária, SOC final 30%, v(t) e potência instantânea | Atual27/10:326,403km semHV/344,768km comHVhipotética; solar12/48V separado, correntes0/6/8/10A e SOC100→30%exato | Verificar aceitaçãoOBC/perfis/componentes e grade nova; potência nas rodas exportada, eixo do motor ainda null |
| 28/P4 | Velocidade máxima e 0–100 no plano e sem vento | Limitador90km/h de série na variante4250kg, fichaSKp3;0–100 inalcançável com limitador ativo | Confirmar curvas para atingir90; não inventar aceleração sem mapas |
| 29/P5 | Menor tempo em 7000 km, bateria inicial+solar, até 8 h/dia | Rota costeiraOSRM de7511.3km,21pontos,DEM5km,ERA5 em14nós; comparação60/80/90km/h e marco7000km; replay de velocidades/energia. | Fechar interfaceOEM, mapas/Cd/Cr e cargas reais; melhorar despacho para dias nublados, validar paradas e obter mínimo global de tempo. Resultados condicionados. |
| 30/P2 | Temperatura nos cabos em potência máxima, campo multidimensional | Parcial: cabo120/150mm² com ficha; campo r-theta feixe/isolamento/R(T), três malhas, correntes/h/k condicionados | Confirmar corrente RMS real, k/R(T) do produto, contatos/agrupamento/contornos e revisar alternativa paralela |
| 31/P6 | Cabine fechada estacionada ao meio-dia, sem A/C e sem passageiros | Parcial: caso condicionado de caixa equivalente,49,079°C ao meio-dia; sol orientado, hipóteseC/UA,48combinações e verificação temporal; não cabine CAD validada | Extrair superfícies, modelar sol/radiação/convecção e justificar regime/condição inicial |
| 32/P6 | Potência A/C: 33 °C externo, 25 °C interno, passageiro, permanente | Parcial: caso condicionado33/25°C+UR50%+ventilação, uma/duas pessoas2,516/2,646kW de frio; COP2–3assumido; parâmetros de envelope a revisar | Calcular ganhos e psicrometria com ocupação definida; obter COP/capacidade de equipamento |
| 33/P1 | Freios: 30→10 m/s em 5 s, início 25 °C e campo multidimensional | Campo r–z condicionado, energia/partição, série analítica e refinamentos; [evidências](FREIOS_2D.md) | Confirmar peçaMY25/cotas/material, distribuição e inércias, contato móvel/regeneração e revisão humana |
| 34/P7 | Temperatura da bateria com cargas 20/80 kW | ECM SOC/T com dois nós térmicos20/80kW, eventos de parada,18sensibilidades+2adiabáticos e balanços; parâmetros não OEM | Calibrar OCV/R(SOC,T)/entropia/capacidades/UA e BMS real |
| 35/P7 | Bomba, radiador, vazão em potência máxima do motor; perfis e ponto de operação | Curva publicadaBosch039202453G cruza circuito assumido em31,85L/min;96W elétricos; perfis na vazão calculada | Obter perdas reais/UA/fluido/ventilador/NPSH e limites; circuito ainda condicionado |

## Limites e fechamento da entrega

- Os35itens possuem trabalho iniciado; nenhum tem aprovação humana final registrada.
- Testes e replay verificam implementação, conservação e rastreabilidade; não medem o veículo físico.
- Estado de carga é a fração de energia restante: I27 parte100% e termina30% da janela útil98kWh nesta hipótese.
- I29 parte100%, reserva10% na tração e20% nos serviços; não impõe30% ao fim da viagem.
- Rota aproximada por vias reaisOSM; limites por classe/perfilOSRM não substituem placas.
- 21jun2025 é a partida histórica escolhida; calendário/local mudam a geração em cada parada.
- DadosERA5 são reanálise horária em14nós espaciais; céu limpo é outro cenário. Falha de política não prova inviabilidade global.
- Sem recargas externas; transferência48V→OBCOEM continua hipótese e requer comprovação.
- Faltam integração dos suplementos ao memorial final, revisão cruzada, seminário e vídeo com os integrantes.

Ver[estudo da rota](../../docs/ROTA_REAL_2026-10-28.md) e[matriz técnica](../../docs/REVISAO_35_ITENS.md).
