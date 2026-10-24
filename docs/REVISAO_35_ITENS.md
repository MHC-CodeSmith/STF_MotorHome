# Revisão dos 35 itens — 23/10/2026

Revisão técnica desta worktree após a correção do CAD. **Nenhum item foi aprovado como resultado final de engenharia.** Há uma carroceria externa detalhada em uso, métodos numéricos verificados e requisitos parcialmente preparados. Testes sintéticos não foram contados como resultados físicos do motorhome.

Fontes locais: enunciado original 2026, pp. 1–2; divisão P1–P7; apostila SEM0571 v0.4, Cristiano Bigonha Tibiriçá, 2025. O levantamento reenviado é idêntico ao já existente, hash `0c0ad68fa68e1b12f5ad37717da460c7c1c1444017b3b24e36319f293d7bb8fc`; seus candidatos CAD nas pp. 6–8 foram reexaminados. O levantamento é referência de aquisição, não autoridade para corrigir requisitos ou comprovar licenças. As consultas usaram textos locais por trechos, sem reenviar os PDFs completos.

## Condições que a integração deve preservar

- São Carlos, céu limpo em 21/06, ambiente 25 °C, UR 50%, vento atmosférico zero, salvo temperaturas especiais. Coordenadas e altitude precisam de fonte; não foram copiadas de exemplo.
- Motorhome para ao menos duas pessoas. A malha de uma van não demonstra que os equipamentos ou a ocupação estão resolvidos.
- I25: eletricidade solar do dia; I26: km/kWh na bateria; I27: alvo final 30%; I29: 7000 km com somente bateria inicial e solar, até 8 h dirigindo por dia de calendário.
- I30/I33: campos multidimensionais dos componentes reais. I33: 30 → 10 m/s em 5 s, início 25 °C. I34: carregadores 20/80 kW. I32: 33 °C externo, 25 °C interno, passageiro e regime permanente.
- O código genérico de agenda permite configurar outros valores: o caso de projeto ainda precisa impor explicitamente os números do enunciado. Não há otimizador pronto nem garantia de viabilidade da viagem.

## Conferência ponto a ponto

“Pendente” indica dado/artefato ainda ausente; “parcial” indica trabalho utilizável com fronteiras explícitas. A coluna de apostila remete às páginas físicas do PDF. Modelos de veículo, solar e elétrica exigem referências adicionais; não se atribuem esses métodos à apostila quando ela não os apresenta.

| Item / dono | Requisito do professor | Evidência atual | Apostila / fundamento | Ação concreta para fechar |
|---|---|---|---|---|
| 01 / P1 | Nome do carro e conceito elétrico solar | Parcial: proposta BEV Aurora Solar, E-Ducato MY25 L3H2; arquitetura e fonte OEM conferidas | Cap. 1, pp. 5–7, requisitos/projeto | Definir nome, arquitetura, duas pessoas e configuração coerente; registrar decisão |
| 02 / P1 | Pneus/rodas, inclusive pressão, material, dimensões e peso | Rodas visuais existem na malha; sem especificação real | Dados do fabricante, fora do escopo da apostila | Escolher pneu/roda com capacidade de carga, pressão e raio efetivo documentados |
| 03 / P1 | Sistema de freios especificado | Peças visuais não são especificação; dados pendentes | Cap. 2 apoia I33, sem dimensionamento completo do sistema | Obter disco/pinça/pastilha, materiais, massas, dimensões e distribuição de frenagem |
| 04 / P4 | Motor: potência máxima, curvas de torque, potência e eficiência por RPM | Parcial: motor OEM elétrico 205 kW/410 Nm; curvas/mapas ainda ausentes | Curvas reais fora da apostila | Selecionar motor elétrico compatível e obter mapas/limites citados |
| 05 / P4 | Transmissão especificada | Pendente | Referências mecânicas externas | Definir relação, rendimento, limites e compatibilidade roda/motor |
| 06 / P2 | Bateria especificada | Parcial: bateria OEM 110/98 kWh, 400 V; célula, BMS, perdas e massa do pack pendentes | Armazenamento térmico não define capacidade elétrica | Definir célula/pack/BMS, tensão, capacidades, massa, curvas e limites |
| 07 / P2 | Fiação elétrica | Pendente; fórmula Joule disponível | Cap. 2 para dissipação, não substitui especificação elétrica | Documentar percursos, bitolas, corrente RMS/DC correta, isolamento, perdas e proteção |
| 08 / P5 | Painéis: área, eficiência e tecnologia | Parcial: JA Solar 450 W; 2/3 módulos; geração condicionada calculada, montagem pendente | Solar/pvlib fora da apostila | Selecionar módulos; descontar aberturas/equipamentos; definir montagem e perdas |
| 09 / P2 | Controladoras e inversores com eficiências | Pendente | Conversão elétrica fora da apostila | Compatibilizar tensão/corrente/MPPT/inversor e mapas de eficiência reais |
| 10 / P7 | Resfriamento de componentes elétricos | Balanços disponíveis, arquitetura pendente | Caps. 2–4, condução/convecção/trocadores/bombas | Receber perdas de motor/inversor/bateria e definir circuitos e limites |
| 11 / P6 | A/C, aquecimento e ventilação | Balanço agregado disponível; equipamento pendente | Cap. 6, pp. 69–72 | Dimensionar ciclo/equipamento após cargas de cabine; fornecer potência elétrica a P5 |
| 12 / P7 | Lubrificação | Pendente; arquitetura não selecionada | Cap. 4 para escoamento, não seleção de lubrificante | Identificar pontos a lubrificar, fluido, circuito, vazão/perdas e fichas |
| 13 / P6 | Materiais/equipamentos internos, incluindo assentos, mobiliário, banheiro, eletrônicos, fogão, geladeira, lavadora/secadora | Delica fornece referência de móveis; não contém toda a lista nem layout adaptado ao Ducato | Cap. 2 e cap. 6 apoiam materiais/HVAC/geladeira | Projetar instalação para duas pessoas com todos os equipamentos prescritos; BOM/cargas/fontes |
| 14 / P1 | Suspensão/direção | Elementos visuais e chassi solar são referências; especificação pendente | Fora da cobertura específica da apostila | Definir eixos, cargas, geometria e compatibilidade com massa montada |
| 15 / P1 | Chassi e dimensões | Parcial: cotas/limite/massa de fábrica E-Ducato L3H2 documentados; CAD atual precisa de adaptação | Cap. 1, definição de arquitetura; dimensionamento estrutural externo | Vincular chassi real à variante escolhida, cotas, massa e limites de carga |
| 16 / P3 | Carenagem, portas, aberturas e vidros | Parcial: exterior Ducato importado com portas, vidros e espelhos | Cap. 2 para propriedades/trocas; CAD não prescrito pela apostila | Conferir escala/variante e definir materiais, espessuras e aberturas do motorhome |
| 17 / P3 | Geometria 3D e três vistas com cotagem principal | Parcial: GLB/STL detalhado adaptado às cotas L3H2; transformações autorais e pneus preservados; revisão física pendente | Enunciado I17; [carroceria](CARROCERIA_DE_TRABALHO.md) | Adaptar interior e instalações; conferir dimensões contra ficha real e completar desenho técnico |
| 18 / P1 | Massa montada com passageiros | Pendente; metadado de massa do ativo 3D não foi adotado | Conservação/contabilidade; sem BOM na apostila | Somar componentes sem sobreposição, incluindo I07/I10, água, carga e passageiros |
| 19 / P3 | Cd e área frontal com CFD | Parcial: silhueta medida, piloto RANS de 29.527 células executado (108 iterações); sem Cd validado | Aerodinâmica externa fora da apostila | Preparar superfície estanque/domínio, executar solver, estudar malha e integrar arrasto |
| 20 / P4 | Coeficiente de rolamento Cr | Pendente; função usa Cr fornecido | Dados pneu/superfície; não é Cr de trocador | Obter coeficiente com carga/pressão/superfície e fonte apropriadas |
| 21 / P4 | Forças aerodinâmica e rolamento versus velocidade | Método simplificado existente; sem curva real integrada | Dinâmica fora da apostila | Receber massa, Cd, área, rho e Cr e gerar curvas com proveniência |
| 22 / P4 | Potência resistiva e tração versus velocidade | Método longitudinal básico; curvas reais ausentes | Dinâmica/motor fora da apostila | Calcular resistência e potência disponível com transmissão, motor e limites elétricos |
| 23 / P2 | Capacidade das baterias em kWh | Parcial: 110 kWh brutos/98 úteis da ficha; adequação à missão ainda pendente | Armazenamento elétrico não se obtém da Eq. térmica 112 | Dimensionar nominal/útil e janela de SOC a partir de componentes e uso definidos |
| 24 / P1 | Custo dos materiais em R$, incluindo impostos | Pendente; não foram feitas compras | Cap. 1 apoia análise de projeto, não preços atuais | Consolidar BOM, cotações datadas, quantidade, transporte e tributação aplicável com fonte |
| 25 / P5 | Autonomia com solar do dia a 40/80 km/h e gráfico versus velocidade | Pendente nesta worktree; não há geração pvlib integrada | Solar/dinâmica fora da apostila | Gerar céu limpo/POA/potência útil e dividir pela demanda; excluir bateria inicial |
| 26 / P5 | km/kWh da bateria a 40/80 km/h | Pendente de dados reais; manter a razão correta | Balanço elétrico e dinâmica externos | Integrar eficiência terminal–rodas e auxiliares, sem trocar km/kWh por kWh/km |
| 27 / P5 | Máxima autonomia diária, SOC final 30%, v(t) e potência instantânea | Parcial: verificador e maximizador MILP em grade testados; faltam curvas reais/caso físico | Conservação; otimização não fornecida pela apostila | Fixar SOC inicial/tolerância, calcular demanda/PV e otimizar perfil, não só validar agenda |
| 28 / P4 | Velocidade máxima e 0–100 no plano e sem vento | Pendente | Dinâmica externa | Integrar torque/forças/inércias e limites; informar se 100 km/h é inalcançável |
| 29 / P5 | Menor tempo em 7000 km, bateria inicial+solar, até 8 h/dia | Parcial: checagem de conservação/capacidade/calendário; sem otimizador | Cap. 1 contextualiza otimização; não resolve a rota | Impor 7.000.000 m e 28.800 s/dia; justificar cenário solar; otimizar e verificar sem recarga externa |
| 30 / P2 | Temperatura nos cabos em potência máxima, campo multidimensional | Parcial: solver 2D e Joule testados, sem cabo real | Fourier p. 9, Newton p. 10 | Inserir geometria/material/isolação, corrente real, rho_e(T), contornos e convergência do componente |
| 31 / P6 | Cabine fechada estacionada ao meio-dia, sem A/C e sem passageiros | Parcial: balanço concentrado, sem caso físico de cabine | Cap. 2; armazenamento sensível p. 74 Eq. 112 | Extrair superfícies, modelar sol/radiação/convecção e justificar regime/condição inicial |
| 32 / P6 | Potência A/C: 33 °C externo, 25 °C interno, passageiro, permanente | Parcial: carga sensível/latente separada; dados sintéticos | Caps. 2 e 6 | Calcular ganhos e psicrometria com ocupação definida; obter COP/capacidade de equipamento |
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

Verificação integrada mais recente (24/10): **90 testes passaram** (dinâmica, auditoria, fontes simuladas, térmica, agenda e geometria). Estrutura: zero erros, 35 itens e 7 responsáveis. Há 17 itens em desenvolvimento parcial e 18 ainda não iniciados nos metadados; os 24 campos `null` da configuração são uma contagem distinta. `config/parametros_globais.yaml` permaneceu byte a byte intacto. A malha de trabalho foi exportada/reaberta e seus hashes foram conferidos. Testes não aprovam a engenharia final.

Primeiro conferir a variante/dimensões da carroceria e resolver chassi, layout e equipamentos (I01–I17), em paralelo aos dossiês de motor/transmissão/bateria/painéis. Consolidar massa/BOM e preparar a superfície externa para CFD. Depois integrar Cd/Cr/dinâmica e geração solar para I18–I29. Os métodos térmicos podem avançar em paralelo, mas só recebem o rótulo de resultado do motorhome quando usam componentes e cenários reais. A cada interface alterada, registrar impacto em massa, energia e térmica e refazer os cálculos dependentes.

As escolhas de componentes devem ser propostas concretas e documentadas; a falta de uma aprovação final não impede preparar métodos e comparações. As respostas dos docentes e a revisão humana permanecem registradas como pendências, não como motivo para interromper todo o trabalho independente.

Atualização elétrica: [arquitetura BEV](ARQUITETURA_ELETRICA.md), proposta `eletrica-0.1`, D003. Tabelas OEM pp.1/4/5 conferidas visualmente; não usar CAD 2014 de 5 m como se já fosse L3H2 elétrica de 5,998 m. Mapas e integração solar/BMS continuam pendentes.

Estado de 24/10: [execução reproduzível](AVANCO_2026-10-24.md) e [artefatos](../entregas/parcial_2026-10-24/README.md). I25 segue pendente de demanda real; gerar PV sozinho não fecha autonomia.
