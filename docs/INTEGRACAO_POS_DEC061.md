# Integração pós-DEC061 — execução de 09/11/2026

**A interface solar/DC não está demonstrada. A missão física não foi comprovada. Os 35 itens têm trabalhos iniciados e nenhum tem aprovação humana final.** As recomendações comerciais são provisórias.

## Arquivos e histórico

O registro original foi localizado em Downloads e incorporado, sem alteração de bytes, em `docs/decisoes_motorhome_2026-10-28.md`. Seu SHA-256 é `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`. A revisão de 28/10 e a saída anterior estão em `entregas/etapa_2026-10-28_rota_real/`. O CAD, visualizador, PDF parcial, três malhas CFD e resultados térmicos anteriores permanecem preservados.

A fonte ativa é `config/parametros_globais.yaml`, revisão `1.0.0-pos-DEC061`, com unidade, origem, data, responsável, confiança e estado por parâmetro. O estado anterior pode ser recuperado no commit `2ef84f67c3aa820633b0565e92c0a23ea810302b`. A migração e seus impactos estão em `docs/decisoes.md`.

`config/registro_cenarios.yaml` separa o que é histórico dos modelos constitutivos reutilizados. Quatro executores antigos exigem `--historico`: interface de carga AC, agenda portátil, construção de viagem e rota real. Isso permite reproduzir métodos anteriores, sem promovê-los à arquitetura B. O caminho via energia armazenada nos serviços foi retirado da proposta elétrica vigente.

Entregas principais:

- [Matriz das 61 decisões](MATRIZ_DECISOES_61.md), com parâmetros, evidências, itens, responsáveis e pendências.
- [Estado dos 35 itens](REVISAO_35_ITENS.md), com inventário de arquivos por item no JSON desta etapa.
- [Bloqueios técnicos](BLOQUEIOS_POS_DEC061.md), [plano P1–P7](PLANO_EXECUCAO_POS_DEC061.md) e [diagramas funcionais](ARQUITETURA_POS_DEC061.md).
- [Lista única de aprovações finais](APROVACOES_FINAIS_PENDENTES.md), com 16 escolhas, opções, recomendações, fontes, impactos e dependências.
- [BOM rastreável](../entregas/etapa_pos_dec061/bom_rastreavel.csv), com 26 linhas. Preço desconhecido fica vazio; não se soma EUR a BRL nem se inventa total instalado.

## Resultados numéricos para o memorial

O consumo-base dos serviços é **7,229 kWh/dia na bateria**, incluindo geladeira AC, indução, climatização intermitente, boiler, lavagem e secagem ocasionais, cargas DC e perdas. As horas de uso e várias energias continuam hipóteses explícitas. A secagem não tem dado comercial confirmado; foi sensibilizada em 1–4 kWh por ciclo, com frequência de um ciclo semanal.

O arquivo `servicos_24_48h.csv` compara consumo mínimo, base e máximo, reservas de 20% e 30%, e autonomias sem Sol de 24 h e 48 h. No caso-base, 24 h exigem dois módulos US5000 com reserva de 20%, ou três com 30%; 48 h exigem quatro ou cinco. A recomendação de trabalho é **três módulos, 14,4 kWh e 119,1 kg**, permitindo comparar as duas reservas com o mesmo banco. Uso veicular, fixação, BMS, compatibilidade e picos ainda não estão demonstrados. Esse banco não atende automaticamente ao caso de consumo alto.

A BOM provisória contém **440.0 kg de conversão conhecida**. Com 2.790 kg OEM e 320 kg de ocupantes, bagagem e água, o subtotal é **3550.0 kg**, ainda sem móveis, isolamento, suportes, MPPT, cabos, proteções e outras massas. Restam 700.0 kg até o PBT de 4.250 kg antes desses faltantes. O mesmo pacote excede 3.500 kg em 50.0 kg. Não se trata de massa típica completa nem de aprovação por eixo. A água do boiler e do sanitário integra o balanço dos 100 L; motor, pack HV e demais componentes OEM não são somados novamente.

O consumo de tração abaixo usa percurso plano, sem serviços, Cd de 0,62488, Crr de 0,012, densidade de 1,1 kg/m³ e eficiência de 0,90, todos como parâmetros provisórios:

|Massa de estudo|Velocidade|Energia na bateria|Distância por energia|
|---|---|---|---|
|3500 kg|40 km/h|0.190 kWh/km|5.25 km/kWh|
|4250 kg|40 km/h|0.218 kWh/km|4.60 km/kWh|
|3500 kg|80 km/h|0.380 kWh/km|2.63 km/kWh|
|4250 kg|80 km/h|0.407 kWh/km|2.46 km/kWh|

Foram calculados **972 pontos** variando Cd, área, massa, Crr, densidade e eficiência. A massa de 3.500 kg é apenas um ponto de sensibilidade; 4.250 kg é o teto de PBT candidato. Não se apresentou nenhum deles como massa operacional típica validada. As três malhas CFD anteriores não demonstram independência: a variação final de Cd é 7,07%, sem camadas e y+ verificados. A faixa observada não é intervalo de confiança ou erro físico quantificado.

Foram executados **56 replays** de 7.000 km, com percurso plano, velocidades constantes de 40/80 km/h, dia-tipo de São Carlos em 21/06 repetido, SOC inicial de 100% nos dois bancos, até oito horas de direção por dia e nenhuma recarga elétrica externa. Os 8 controles sem interface interrompem por reserva de tração. Há 12 chegadas condicionais, com mínimo de carregamento de **1 kW hipotético**, nunca atribuído ao OEM. O erro máximo de fechamento energético fica abaixo de 10⁻⁶ kWh. As séries completas e os diários estão em `entregas/etapa_pos_dec061/`.

A comparação de horários cobre 08–16 e 00–08. A segunda janela é uma alternativa, não uma política otimizada demonstrada. Os dias calculados não são previsão meteorológica nem tempo mínimo global. Os painéis portáteis só geram nos períodos estacionados planejados, descontando montagem/desmontagem, com orientação e inclinação fixas em cada parada. Os 190 W de baixa tensão do arranjo histórico não são creditados ao banco de 48 V sem conversão comprovada: o replay usa a string principal de 1.350 Wp e mantém a meta de 1.540 Wp em aberto, sem reduzi-la como decisão.

Há **36 comparações** de DC direta versus buffer dedicado, com mínimos hipotéticos de 0,5/1/2/3/5/10 kW e buffers de 0/2/5 kWh inicialmente vazios. Esses estados não recebem energia da bateria de serviços. O despacho tem resolução de 15 minutos, que não representa tempo mínimo de sessão OEM. O resultado demonstra conservação sob hipóteses, sem inventar carregador compatível ou instalar banco extra.

I25 permanece sem autonomia solar fisicamente demonstrada. No controle, o crédito de FV à tração é zero. I26 separa o consumo de tração dos serviços. I27 mantém 100%→30% como principal e 80%→30% como sensibilidade no cálculo sem reposição solar, sem alegar otimização global. A reserva final de 30% não foi imposta ao item 29.

I30 reutiliza o solver de volumes finitos r–theta para cabos de serviços de 70/95 mm², corrente de 102,17 A e três malhas; os campos espaciais e resíduos estão salvos. Geometria, propriedades e contornos são estimados, sem certificação de bitola ou proteção. O enunciado pede cabos do motor; a DEC-026 prioriza os serviços de 48 V. A referência HV anterior foi preservada e essa diferença de escopo continua explícita.

I33 reutiliza o solver r–z com a potência por atrito após descontar arrasto, rolamento e regeneração mecanicamente limitada a 0/40/80 kW. Há comparação de massa, malha e passo temporal. As curvas de regeneração, aceitação no pack, geometria, materiais e repartição OEM continuam pendentes. O ensaio de 30 m/s (108 km/h) foi preservado como requisito acadêmico do componente, acima do limitador de 90 km/h da candidata; não se alega que essa velocidade seja atingível pelo veículo limitado.

I31 foi reexecutado com cabine fechada, sem ocupantes ou A/C: a rede térmica equivalente estima **49.08 °C ao meio-dia**. O CFD 3D de convecção natural ainda não foi executado. I32 estima **2.516 kW térmicos com um ocupante** e **2.646 kW com dois**, a 33 °C externos e 25 °C internos. A vazão exterior de 30 m³/h é hipótese do dimensionamento, sem prova de ventilação natural com vento nulo, e não foi aplicada ao ensaio fechado de I31. Falta equipamento sob banco compatível com 220 V/60 Hz e com a capacidade requerida sob incerteza.

A triagem potável é nova e distinta de `hidraulica_proposta.yaml`, que modela água/glicol do arrefecimento. Ela compara um trecho crítico hipotético de 10/13 mm com a curva documentada da bomba Shurflo de 12 V. Os pontos calculados são próximos de 5,47/5,57 L/min; materiais, rotas, pressão admissível, conexões e proteções ainda exigem validação. Com consumo hipotético de 60 L/dia, os 100 L durariam 1,67 dias sem lavanderia. Um ciclo de 68,8 L quase enche sozinho o tanque cinza de 70 L. As paradas sanitárias ainda não estão completamente integradas ao replay energético.

Também foram calculadas comparações de cabos em 12/24 V e sensibilidade do indicador lateral com alturas e deslocamentos hipotéticos do CG. Esses cálculos não demonstram segurança dinâmica, eixo admissível, curso de suspensão ou homologação. Os ensaios térmicos de bateria de 20/80 kW permanecem modelos parametrizados anteriores, sem nova validação OEM e sem representar potências solares disponíveis.

## Parecer da interface DC

A [ficha Fiat SK](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf) documenta CCS2 e potência DC máxima, mas não o mínimo de sessão solar nem a autorização para um equipamento proposto. O [relato primário 4x4electric/Venema](https://4x4electric.com/charging-technique/) e seu teste de 2022 dizem respeito a outro conjunto. Seus 30 kW máximos e 10 kWp de painéis não são mínimos do E-Ducato.

O [Sungrow IDC30E](https://uk.sungrowpower.com/upload/file/20221215/EN%20FS%20IDC30E%20DC%20Charger%20Factsheet.pdf) informa ajuste até 1 kW na FAQ, mas sua alimentação é AC trifásica de 400 V/50 Hz. Isso não comprova a arquitetura direta FV/DC escolhida. Não se propõe alimentá-lo pela bateria de serviços. A [página brasileira do Ducato](https://ducato.fiat.com.br/) apresenta versões diesel; não se transplantaram seus preços ou especificações para o E-Ducato.

**DC direta: não demonstrada. Buffer dedicado: não demonstrado e não instalado. Caminho via armazenamento dos serviços: inviável sob DEC-020.** Falta documentação de tensão, corrente e potência mínimas, comunicação, isolamento, proteções, resposta à intermitência e autorização/compatibilidade do conjunto exato. Se o mínimo real exceder a potência disponível, o cenário direto será inviável nessa condição, sem inferir impossibilidade universal da arquitetura B.

## Reprodução e verificações

Execute os comandos do [plano P1–P7](PLANO_EXECUCAO_POS_DEC061.md). Os scripts numéricos, consolidação e verificação têm manifestos próprios. Resultados de testes e auditorias estão em `output/`.

A suíte passou em **197 testes**, o Ruff passou e a estrutura dos 35 itens foi conferida. A verificação atual checa as 61 decisões, 15 hashes de entrada e 138 saídas numéricas, além do pacote documental. A verificação histórica conferiu os 124 hashes da entrega antiga, mas apontou uma divergência de proveniência em `resumo_freios.json` porque o código dos freios mudou. O artefato e o hash antigos foram preservados; não se ocultou a desatualização.

Ainda faltam a interface DC autorizada, massa e limites por eixo completos, mapas OEM, segundo layout cotado, duas ocupações finais de teto, ancoragens/FEA críticas, CFD convergido, CFD 3D da cabine, projeto elétrico e automação finais, logística sanitária completa e orçamento instalado. Essas pendências estão atribuídas por responsável e não foram convertidas em aprovações.
