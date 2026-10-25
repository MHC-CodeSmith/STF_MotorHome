# Revisão dos 35 itens — 25/10/2026

Revisão técnica desta worktree após a correção do CAD. **Nenhum item foi aprovado como resultado final de engenharia.** Há uma carroceria externa detalhada em uso, métodos numéricos verificados e requisitos parcialmente preparados. Testes sintéticos não foram contados como resultados físicos do motorhome.

Fontes locais: enunciado original 2026, pp. 1–2; divisão P1–P7; apostila SEM0571 v0.4, Cristiano Bigonha Tibiriçá, 2025. O levantamento reenviado é idêntico ao já existente, hash `0c0ad68fa68e1b12f5ad37717da460c7c1c1444017b3b24e36319f293d7bb8fc`; seus candidatos CAD nas pp. 6–8 foram reexaminados. O levantamento é referência de aquisição, não autoridade para corrigir requisitos ou comprovar licenças. As consultas usaram textos locais por trechos, sem reenviar os PDFs completos.

## Condições que a integração deve preservar

- São Carlos, céu limpo em 21/06, ambiente 25 °C, UR 50%, vento atmosférico zero, salvo temperaturas especiais. Coordenadas/altitude obtidas juntas no cadastro oficial INMET A711, conforme registro de execução.
- Motorhome para ao menos duas pessoas. A malha de uma van não demonstra que os equipamentos ou a ocupação estão resolvidos.
- I25: eletricidade solar do dia; I26: km/kWh na bateria; I27: alvo final 30%; I29: 7000 km com somente bateria inicial e solar, até 8 h dirigindo por dia de calendário.
- I30/I33: campos multidimensionais dos componentes reais. I33: 30 → 10 m/s em 5 s, início 25 °C. I34: carregadores 20/80 kW. I32: 33 °C externo, 25 °C interno, passageiro e regime permanente.
- Há maximizador de distância e minimizador de tempo em grade, com testes analíticos. Casos condicionados não garantem viabilidade física da viagem. As oito horas diárias pertencem a I29; I27 usa o dia completo e SOC final exatamente30%.

## Conferência ponto a ponto

“Pendente” indica dado/artefato ainda ausente; “parcial” indica trabalho utilizável com fronteiras explícitas. A coluna de apostila remete às páginas físicas do PDF. Modelos de veículo, solar e elétrica exigem referências adicionais; não se atribuem esses métodos à apostila quando ela não os apresenta.

| Item / dono | Requisito do professor | Evidência atual | Apostila / fundamento | Ação concreta para fechar |
|---|---|---|---|---|
| 01 / P1 | Nome do carro e conceito elétrico solar | Parcial: proposta BEV Aurora Solar, E-Ducato MY25 L3H2; arquitetura e fonte OEM conferidas | Cap. 1, pp. 5–7, requisitos/projeto | Definir nome, arquitetura, duas pessoas e configuração coerente; registrar decisão |
| 02 / P1 | Pneus/rodas, inclusive pressão, material, dimensões e peso | Parcial: Continental225/75R16C artigo04514690000 documentado; diâmetro0,74422m/massa16,919kg; pressão operacional e roda pendentes | Dados do fabricante, fora do escopo da apostila | Escolher pneu/roda com capacidade de carga, pressão e raio efetivo documentados |
| 03 / P1 | Sistema de freios especificado | Peças visuais não são especificação; dados pendentes | Cap. 2 apoia I33, sem dimensionamento completo do sistema | Obter disco/pinça/pastilha, materiais, massas, dimensões e distribuição de frenagem |
| 04 / P4 | Motor: potência máxima, curvas de torque, potência e eficiência por RPM | Parcial: motor OEM elétrico 205 kW/410 Nm; curvas/mapas ainda ausentes | Curvas reais fora da apostila | Selecionar motor elétrico compatível e obter mapas/limites citados |
| 05 / P4 | Transmissão especificada | Pendente | Referências mecânicas externas | Definir relação, rendimento, limites e compatibilidade roda/motor |
| 06 / P2 | Bateria especificada | Parcial: OEM110/98kWh400V com envelope CAD estimado; serviços2NG51,2V100Ah paralelo+LynxBMSNG; perdas/massa OEM pendentes | Armazenamento térmico não define capacidade elétrica | Definir célula/pack/BMS, tensão, capacidades, massa, curvas e limites |
| 07 / P2 | Fiação elétrica | Parcial: rotasCAD conceituais; manual de serviços70mm²/fusível200A e sensibilidadeI²R/queda; cabo de tração e isolamento pendentes | Cap. 2 para dissipação, não substitui especificação elétrica | Documentar percursos, bitolas, corrente RMS/DC correta, isolamento, perdas e proteção |
| 08 / P5 | Painéis: área, eficiência e tecnologia | Parcial: fixa3JA450+Victron190=1540W; alternativa móvel até2890W; sombra direta e geração5.51/9.19–10.33kWh condicionadas; carga do teto por confirmar | Solar/pvlib fora da apostila | Selecionar módulos; descontar aberturas/equipamentos; definir montagem e perdas |
| 09 / P2 | Controladoras e inversores com eficiências | Parcial: MPPT150/35 principal+opcional e100/20 a12V; MultiPlus-II48/5000,Orion48/12-30,banco10,24kWh eBMS dimensionados noCAD; EVSE/circuitos e curvas pendentes | Conversão elétrica fora da apostila | Compatibilizar tensão/corrente/MPPT/inversor e mapas de eficiência reais |
| 10 / P7 | Resfriamento de componentes elétricos | Balanços disponíveis, arquitetura pendente | Caps. 2–4, condução/convecção/trocadores/bombas | Receber perdas de motor/inversor/bateria e definir circuitos e limites |
| 11 / P6 | A/C, aquecimento e ventilação | Parcial: FreshWell3000 sob cama modelado628x400x286mm/21kg;2700W frio vs2646W carga nominal estimada; curva/dutos e cenários altos pendentes | Cap. 6, pp. 69–72 | Dimensionar ciclo/equipamento após cargas de cabine; fornecer potência elétrica a P5 |
| 12 / P7 | Lubrificação | Pendente; arquitetura não selecionada | Cap. 4 para escoamento, não seleção de lubrificante | Identificar pontos a lubrificar, fluido, circuito, vazão/perdas e fichas |
| 13 / P6 | Materiais/equipamentos internos, incluindo assentos, mobiliário, banheiro, eletrônicos, fogão, geladeira, lavadora/secadora | Parcial:7equipamentos internos/157sólidos; induçãoIE3TP220V60Hz2000W substitui50Hz; garagem/armário técnico,serviços e dutos em conjunto adicional208sólidos; montagem/ergonomia pendentes | Cap. 2 e cap. 6 apoiam materiais/HVAC/geladeira | Escolher equipamentos e materiais reais; conferir portas/rodas/isolamento/ergonomia; BOM/cargas/fontes |
| 14 / P1 | Suspensão/direção | Elementos visuais e chassi solar são referências; especificação pendente | Fora da cobertura específica da apostila | Definir eixos, cargas, geometria e compatibilidade com massa montada |
| 15 / P1 | Chassi e dimensões | Parcial: cotas/limite/massa OEM; malha adaptada às cotas-alvo L3H2, não CAD OEM | Cap. 1, definição de arquitetura; dimensionamento estrutural externo | Vincular chassi real à variante escolhida, cotas, massa e limites de carga |
| 16 / P3 | Carenagem, portas, aberturas e vidros | Parcial: exterior Ducato importado com portas, vidros e espelhos | Cap. 2 para propriedades/trocas; CAD não prescrito pela apostila | Conferir escala/variante e definir materiais, espessuras e aberturas do motorhome |
| 17 / P3 | Geometria 3D e três vistas com cotagem principal | Parcial: exterior detalhado+interior157sólidos+tração/serviços208sólidos STEP/GLB; coberturas; viewer23seletores e vista técnica; tração estimada,não CAD OEM | Enunciado I17; [carroceria](CARROCERIA_DE_TRABALHO.md) | Adaptar interior e instalações; conferir dimensões contra ficha real e completar desenho técnico |
| 18 / P1 | Massa montada com passageiros | Parcial: subtotal3373.36kg com elétrica115.4kg e indução2.3kg;faltam móveis/quadro/suportes/tubos/cabos/ferragens/bagagem; não massa final nem eixos verificados | Conservação/contabilidade; sem BOM na apostila | Somar componentes sem sobreposição, incluindo I07/I10, água, carga e passageiros |
| 19 / P3 | Cd e área frontal com CFD | Parcial: três malhas29527/63668/166212células convergidas, Cd0,653/0,625/0,581; mudança final7,07%; refino com camadas rejeitado | Aerodinâmica externa fora da apostila | Resolver camadas/y+, rodas, geometria e estudo de independência; sem Cd final validado |
| 20 / P4 | Coeficiente de rolamento Cr | Pendente; função usa Cr fornecido | Dados pneu/superfície; não é Cr de trocador | Obter coeficiente com carga/pressão/superfície e fonte apropriadas |
| 21 / P4 | Forças aerodinâmica e rolamento versus velocidade | Parcial:324cenários explícitos Cd/Cr/eta/velocidade; forças tabeladas, não dados aprovados | Dinâmica fora da apostila | Substituir hipóteses por massa/Cd/Cr/rho validados |
| 22 / P4 | Potência resistiva e tração versus velocidade | Parcial: potência nas rodas/terminais nos324cenários; curva disponível real ausente | Dinâmica/motor fora da apostila | Integrar transmissão, motor, mapas de perdas e limites elétricos |
| 23 / P2 | Capacidade das baterias em kWh | Parcial: 110 kWh brutos/98 úteis da ficha; adequação à missão ainda pendente | Armazenamento elétrico não se obtém da Eq. térmica 112 | Dimensionar nominal/útil e janela de SOC a partir de componentes e uso definidos |
| 24 / P1 | Custo dos materiais em R$, incluindo impostos | Pendente; não foram feitas compras | Cap. 1 apoia análise de projeto, não preços atuais | Consolidar BOM, cotações datadas, quantidade, transporte e tributação aplicável com fonte |
| 25 / P5 | Autonomia com solar do dia a 40/80 km/h e gráfico versus velocidade | Parcial: pvlib integrado à sensibilidade; dois módulos10,5–18,7km@40 e6,4–9,8km@80, hipóteses não validadas | Solar/dinâmica fora da apostila | Confirmar perdas/solar-HV/montagem, demanda real e consumo de habitação |
| 26 / P5 | km/kWh da bateria a 40/80 km/h | Parcial:3,25–5,78@40 e1,97–3,03@80 na grade de hipóteses, não faixas medidas | Balanço elétrico e dinâmica externos | Integrar mapas terminal–rodas e auxiliares reais, preservando km/kWh |
| 27 / P5 | Máxima autonomia diária, SOC final 30%, v(t) e potência instantânea | Parcial:335km no cenário condicionado em grade, SOC100→30%exato; agenda e potência terminal exportadas | Conservação; otimização não fornecida pela apostila | Integrar componentes reais, potência mecânica do motor, acelerações e estudo da grade |
| 28 / P4 | Velocidade máxima e 0–100 no plano e sem vento | Pendente | Dinâmica externa | Integrar torque/forças/inércias e limites; informar se 100 km/h é inalcançável |
| 29 / P5 | Menor tempo em 7000 km, bateria inicial+solar, até 8 h/dia | Parcial: minimizador em grade testado; agenda construtiva7000km/1622datas verificada, cenário solar repetido; não ótimo nem previsão da rota | Cap. 1 contextualiza otimização; não resolve a rota | Resolver modelo solar/consumo/integração real e executar otimização da missão física |
| 30 / P2 | Temperatura nos cabos em potência máxima, campo multidimensional | Parcial: solver 2D e Joule testados, sem cabo real | Fourier p. 9, Newton p. 10 | Inserir geometria/material/isolação, corrente real, rho_e(T), contornos e convergência do componente |
| 31 / P6 | Cabine fechada estacionada ao meio-dia, sem A/C e sem passageiros | Parcial: caso condicionado de caixa equivalente,49,079°C ao meio-dia; sol orientado, hipóteseC/UA,48combinações e verificação temporal; não cabine CAD validada | Cap. 2; armazenamento sensível p. 74 Eq. 112 | Extrair superfícies, modelar sol/radiação/convecção e justificar regime/condição inicial |
| 32 / P6 | Potência A/C: 33 °C externo, 25 °C interno, passageiro, permanente | Parcial: caso condicionado33/25°C+UR50%+ventilação, uma/duas pessoas2,516/2,646kW de frio; COP2–3assumido; parâmetros de envelope a revisar | Caps. 2 e 6 | Calcular ganhos e psicrometria com ocupação definida; obter COP/capacidade de equipamento |
| 33 / P1 | Freios: 30→10 m/s em 5 s, início 25 °C e campo multidimensional | Derivação 400 J/kg e 80 W/kg; solver 2D genérico, sem disco real | Cap. 2 e conservação de energia | Distribuir calor com massa/discos/pastilhas/inércias/regeneração; iniciar 298,15 K e refinar malha/tempo |
| 34 / P7 | Temperatura da bateria com cargas 20/80 kW | Parcial: parcela I²R e armazenamento testados, pack sintético | Cap. 2 e Eq. 112 p. 74 | Implementar protocolo real/BMS, dependência SOC/T, calor reversível e arrefecimento |
| 35 / P7 | Bomba, radiador, vazão em potência máxima do motor; perfis e ponto de operação | Parcial: ε-NUT/perfil paralelo e interseções de curvas testados | Eqs. 49–62 pp. 31/38; tabela 4 p. 39; Eq. 93 p. 56 | Obter perdas máximas, fluido, geometria/arranjo do radiador, curvas reais, NPSH e perfis compatíveis |

## Correções já executadas

1. A carroceria externa detalhada foi obtida, importada por hierarquia e exportada em GLB/STL, preservando rodas, portas, vidros e espelhos. Não se usou um bloco como substituto.
2. A área frontal é união das projeções da malha, não largura × altura da caixa envolvente. Nenhum valor foi promovido silenciosamente ao YAML aprovado.
3. Foram separados os dados do ativo visual, os componentes reais, as hipóteses e os ensaios sintéticos. O interior Delica não foi apresentado como interior que já cabe no Ducato.
4. Os métodos térmicos passaram a ter [documentação efetiva](FRENTE_TERMICA.md), incluindo as limitações que impedem tratar os ensaios como solução de I30–I35.
5. Há scripts reexecutáveis para adquirir a fonte fixada, preparar a carroceria, gerar vistas/área e verificar métodos. Fontes, hashes, créditos e modificações constam dos registros locais.

## Ordem de execução para o fechamento físico

Verificação integrada mais recente (25/10): **117 testes passaram** (dinâmica, auditoria, fontes simuladas, térmica, agendas, menor tempo e geometria/integração elétrica). Há **27 itens em desenvolvimento parcial e 8 ainda não iniciados** nos metadados; os24campos `null` da configuração são uma contagem distinta. Nenhum item aprovado. `config/parametros_globais.yaml` permanece intacto. O visualizador offline foi aberto em Chromium; testes não aprovam a engenharia final.

Primeiro conferir a variante/dimensões da carroceria e resolver chassi, layout e equipamentos (I01–I17), em paralelo aos dossiês de motor/transmissão/bateria/painéis. Consolidar massa/BOM e preparar a superfície externa para CFD. Depois integrar Cd/Cr/dinâmica e geração solar para I18–I29. Os métodos térmicos podem avançar em paralelo, mas só recebem o rótulo de resultado do motorhome quando usam componentes e cenários reais. A cada interface alterada, registrar impacto em massa, energia e térmica e refazer os cálculos dependentes.

As escolhas de componentes devem ser propostas concretas e documentadas; a falta de uma aprovação final não impede preparar métodos e comparações. As respostas dos docentes e a revisão humana permanecem registradas como pendências, não como motivo para interromper todo o trabalho independente.

Atualização elétrica: [arquitetura BEV](ARQUITETURA_ELETRICA.md), proposta `eletrica-0.1`, D003/D004. Tabelas OEM pp.1/4/5 conferidas visualmente; a malha2014 foi adaptada para5,998m, sem se tornar CAD OEM. Mapas e integração solar/BMS continuam pendentes.

Estado de24/10: [execução reproduzível](AVANCO_2026-10-24.md), [energia e otimização](ENERGIA_E_OTIMIZACAO.md), [CAD e inspeção](CAD_ONLINE_E_VISUALIZACAO.md), [artefatos](../entregas/parcial_2026-10-24/README.md). Estimativas não fecham a autonomia física sem demanda real e integração solar.

Avanço de 25/10: [cabine/HVAC](CABINE_E_HVAC.md), [pneus e massa](PNEUS_E_MASSA.md). O caso da cabine é condicionado a geometrias/propriedades propostas; não foi promovido a resultado validado.

Ampliação de teto/interior: [cobertura fixa1540W, extensão de estudo2890W e equipamentos dimensionados](EXPANSAO_SOLAR_E_INTERIOR.md). O PDF agora integra estes avanços; as agendas/CFD anteriores são cenários históricos ainda sem esta geometria equipada.
