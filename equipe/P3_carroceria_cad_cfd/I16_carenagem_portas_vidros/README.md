# Item 16 — Carenagem, portas, vidros

<!-- revisao-final:inicio -->
> **Revisão de 19/11/2026.** O item 16 e a Figura 6 do [relatório](../../../relatorio/relatorio.pdf) apresentam a configuração revista para o cenário `maxeon1540_independente`. As verificações abaixo usam os dados do commit `5144702`. O aceite pelos integrantes é registrado no [guia de revisão](../../../docs/REVISAO_INTEGRANTES.md).
<!-- revisao-final:fim -->

## Envoltória e aberturas

Mantêm-se a carroceria monobloco de aço do Fiat E-Ducato L3H2, o para-brisa laminado, os vidros da cabine, duas portas dianteiras, uma porta lateral corrediça e duas folhas traseiras com abertura de 270°. Essas peças integram a massa de 2.790 kg do veículo-base.

| Componente da conversão | Especificação e efeito no projeto |
|---|---|
| Janela lateral da habitação | Uma janela projetável com dobradiça superior no painel fixo da área de estar. Referência de projeto Dometic S4 9104104526, acrílico duplo, moldura em poliuretano e tela. Recorte de 499 × 298 mm (L × A), dimensões externas de 544 × 330 mm, parede local de 34 mm e massa de 4,00 kg. O desenho de fabricação deve confirmar o requadro, a posição das nervuras e o curso de abertura. |
| Teto e ventilação | O deck de alumínio com quatro módulos permanece a 40 mm do teto. A faixa central entre a borda dianteira do deck e o início do para-brisa mede cerca de 288 mm no modelo. A Micro Heki 9104117435 tem recorte de 280 × 280 mm, e moldura de 408 × 370 mm. O gabarito de instalação requer 430 × 390 mm de espaço externo. Faltam ao menos 102 mm nessa posição. A configuração revista mantém o teto sem claraboia e usa as janelas e o apoio mecânico do item 11 para ventilação. A Micro Heki, de 1,82 kg, permanece como alternativa para outra disposição do deck. |
| Passagens | Propõe-se uma entrada vedada para os cabos fotovoltaicos e duas travessias de piso no trajeto da tubulação da pia, junto à bomba e ao gabinete da cozinha. O modelo registra o trajeto. Furações, luvas, vedações e estanqueidade dependem do detalhamento da chapa. |

## Conferência de massa e de transmissão térmica

**Massa.** No layout A, o inventário discrimina **16,00 kg** para `janelas_protecao_solar` e **4,00 kg** para `cuba_torneira`. A hipótese de detalhamento aloca **4,00 kg** da primeira parcela à S4 e conserva **12,00 kg** para as demais proteções e arremates dessa mesma rubrica. As duas linhas estão incluídas nos 325,03 kg de interior e envoltória. A claraboia tem quantidade instalada zero. A massa do cenário continua em 3.976,53 kg. [Inventário de massas do cenário](../../../entregas/integrado_maxeon1540/integracao/inventario_massas.csv)

**Parede opaca.** O modelo usa 32 mm de AF/ArmaFlex com condutividade a 40 °C de 0,03828 W/(m·K), revestimento interno de 6 mm com condutividade de 0,13 W/(m·K) e coeficientes de película de 3 e 8 W/(m²·K) no interior e no exterior, respectivamente. A resistência total em série é 1/3 + 0,006/0,13 + 0,032/0,03828 + 1/8 = **1,34043 m²·K/W**, o que resulta em **U = 0,74603 W/(m²·K)**. [Parâmetros da cabine](../../../config/cabine_proposta.yaml)

**Vidros e pontes térmicas.** A caixa térmica equivalente considera 39,1629 m² opacos e 4,60 m² envidraçados, distribuídos em 2,50 m² na frente, 0,50 m² na traseira e 0,80 m² por lado. O teto é modelado como opaco. O modelo adota U do vidro de 5,7 W/(m²·K) e fator solar de 0,60. As pontes térmicas acrescentam 10 W/K em paralelo. O total é **UA = 0,74603 × 39,1629 + 5,7 × 4,60 + 10 = 65,4366 W/K**. A janela proposta detalha a área lateral equivalente já assumida. As propriedades e áreas dos itens 31 e 32 continuam sendo hipóteses da cabine. [Memória de cálculo](../../../scripts/calcular_cabine.py) · [Resultado por face](../../../entregas/etapa_pos_dec061/cabine_31_32_reexecutada.json)

## Histórico do desenvolvimento

**Responsável:** P3 — Carroceria, CAD e CFD  
**Enunciado / tarefa:** Geometria e materiais da envoltória, portas, aberturas e vidros.  
**Depende de:** I15 (P1)  
**Status:** Em desenvolvimento — artefatos parciais; revisão humana pendente.

## Entrega mínima
- `teoria.md`: fenômeno físico, equações, hipóteses e faixa de validade.
- `fontes.md`: referências completas, URL, página/tabela, fabricante e data de acesso.
- `dados/`: entradas com unidades e proveniência; dados desconhecidos continuam como pendentes.
- `codigo/`: notebooks ou scripts com comando exato para executar.
- `resultados/`: tabelas, figuras e logs gerados pelo código. Não inserir resultados fictícios.
- `validacao.md`: testes, revisão humana, limitações, e links para PRs.
- `externos/`: registro dos arquivos de terceiros incorporados legalmente.

## Interface
Entradas oficiais em `config/parametros_globais.yaml`; cada atualização relevante requer registro em `docs/decisoes.md` e deve avisar itens dependentes.

## Aceite
O item só vira **aprovado** quando tiver resultados reproduzíveis, referências e uma revisão por outro integrante.

## Revisão desta frente — 23/10/2026

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). A [carroceria detalhada](../../../docs/CARROCERIA_DE_TRABALHO.md) substitui o bloco como geometria de trabalho. Não há CFD concluído.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
