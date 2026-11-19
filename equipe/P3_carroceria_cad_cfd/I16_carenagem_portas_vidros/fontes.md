# Fontes — item 16

## Esquadrias de referência

| Fonte e versão | Dados consultados | Acesso |
|---|---|---|
| Dometic, *Windows & Doors*, tabela de janelas S4 projetáveis, código 9104104526. [Catálogo técnico](https://mediabank.dometic.com/deployedFiles/2e7578a7069c02837a4a975ddc377872.pdf) | Dimensões externas de 544 × 330 mm, recorte de 499 × 298 mm, parede de 34 mm, massa de 4,00 kg. Descrição da família S4 para acrílico duplo e moldura de poliuretano. | 19/11/2026 |
| Dometic, *Micro Heki*, código 9104117435. [Ficha técnica](https://www.dometic.com/en/product/dometic-micro-heki-9104117435) | Claraboia avaliada como alternativa. Conjunto de 408 × 370 mm em planta. O [catálogo B2B da Dometic](https://www.karavan-servis.sk/wp-content/uploads/2026/04/Katalog-Dometic-2026.pdf) indica espaço externo de 430 × 390 mm. Recorte de 280 × 280 mm, espessura local de 23–42 mm, massa de 1,82 kg. | 19/11/2026 |
| Armacell, *AF/ArmaFlex*. [Ficha técnica citada pelo grupo](https://www.armacell.com/en-DE/product/technical-specs/afarmaflex) | Isolante térmico. A entrada do projeto registra a correlação de condutividade e a avaliação a 40 °C. | 25/10/2026, conforme registro do grupo |

## Dados internos do projeto

| Evidência do commit `5144702` | Aplicação |
|---|---|
| [Parâmetros globais](../../../config/parametros_globais.yaml) e [inventário do layout A](../../../entregas/integrado_maxeon1540/integracao/inventario_massas.csv) | Rubrica de 16 kg para janelas e proteção solar. A linha de 4 kg para cuba e torneira é separada. As fichas comerciais acima servem ao pré-dimensionamento da revisão. |
| [Parâmetros da cabine](../../../config/cabine_proposta.yaml), [cálculo](../../../scripts/calcular_cabine.py) e [resultado da cabine](../../../entregas/etapa_pos_dec061/cabine_31_32_reexecutada.json) | Filmes, isolamento, revestimento, áreas equivalentes de vidro, fator solar, transmitância opaca e condutância das pontes térmicas. |
| [Montagem CAD do relatório](../../../relatorio/montagem_cad.py) e [Figura 6 do relatório](../../../relatorio/relatorio.pdf) | Relação entre o deck equipado e a carroceria de trabalho. A medida é da geometria equivalente usada pelo grupo. |

<!-- execucao-integrada:inicio -->
Fontes específicas da execução (não representam aprovação da instalação):

- `oem_sk`: https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf; consulta/revisão: 2026-03-20. Origem: fabricante.
- `history`: historico_repositorio; consulta/revisão: ver YAML. Origem: historico_repositorio.

Evidência técnica: `entregas/integrado_maxeon1540/rotas_instalacoes/layoutA_rotas_reserva.step`. Condições/hipóteses constam no YAML;valoresOEM não publicados permanecem desconhecidos.
<!-- execucao-integrada:fim -->
