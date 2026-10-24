# Aurora Solar — revisão parcial de 24/10/2026

**Projeto em desenvolvimento. Não é entrega final dos 35 itens.**

![Proposta de carroceria elétrica](aurora_L3H2_proposta.png)

[Abrir malha GLB adaptada](aurora_L3H2_proposta_m.glb). Comprimento-alvo 5,998 m, entre-eixos-alvo 4,035 m, teto-alvo 2,612 m. Proposta autoral derivada de modelo detalhado existente; não CAD homologado Fiat. A malha visual continua aberta; uma versão separada reparada serviu somente ao piloto CFD.

![Geração solar estimada](solar_proposta.png)

Estimativa de céu limpo em São Carlos A711, 21/06/2026: **3,23 kWh/dia com dois módulos** ou **4,85 kWh/dia com três**, após perdas assumidas. Eficiência de conversão HV, montagem, sombras e interface BMS não estão validadas. Não equivale à autonomia do motorhome. Entradas em [solar_proposta.yaml](../../config/solar_proposta.yaml), resultados e hipóteses em [resumo_solar.json](resumo_solar.json).

![Campos de CFD piloto](campos_piloto.png)

Campos efetivamente calculados: piloto com 29.527 células, solver atingiu critérios de resíduo em 108 iterações, sem estudo de independência de malha/camadas/y+ nem validação experimental. **Cd não publicado.** Ver [resumo do piloto](resumo_cfd_piloto.json).

Para fontes, método, comandos, limites e o que falta, consultar [registro de execução](../../docs/AVANCO_2026-10-24.md) e [revisão dos 35 itens](../../docs/REVISAO_35_ITENS.md). Dados globais aprovados permanecem intactos. Testes automatizados verificam implementações, não aprovam a engenharia do veículo.

## Atribuição da geometria

Modelo derivado: Fiat Ducato 2014, razor24 (2019), Dogan Ulus (2025), OpenX Assets release 20261015. Licenças conjuntas **MPL-2.0 AND CC-BY-4.0**, textos preservados nesta pasta. Fonte [OpenX Assets](https://github.com/vevalabs/openx-assets/releases/tag/20261015); código-fonte Blender e histórico em [repositório original](https://github.com/vevalabs/openx-assets/tree/1a63f13b5cfee3e01207a84b13b40fc172d92a95/src/vehicles/fiat_ducato_2014). Mudanças: seleção de exterior, rotação dos eixos, alongamento da região de carga, elevação do teto e translação rígida das rodas; todos os passos no [script](../../scripts/adaptar_educato.py). Não se afirma vínculo/endosso dos autores com este projeto.
