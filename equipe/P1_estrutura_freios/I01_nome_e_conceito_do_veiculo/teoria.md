# Fundamentação teórica — item 01

## Objetivo e fenômeno
Definir nome, referência e requisitos de veículo habitável para pelo menos duas pessoas.

## Equações e hipóteses
Tração por motor elétrico alimentado pela bateria; geração solar convertida e controlada por interface compatível com BMS. A conservação de energia será aplicada com perdas de conversão, tração, auxiliares e limites de armazenamento; ainda não há balanço integrado validado. Não confundir os 110 kWh brutos com os 98 kWh úteis publicados na ficha da variante escolhida.

## Entradas e unidades
Dependências diretas: Requisitos gerais e decisões de conceito.

## Modelo / procedimento
Conceito, fonte OEM, fluxos e verificação dos requisitos em [arquitetura elétrica](../../../docs/ARQUITETURA_ELETRICA.md). Cenários e lacunas em [configuração proposta](../../../config/arquitetura_eletrica_proposta.yaml). Para I29, somente bateria inicial e solar ao longo de 7000 km, até 8 h de direção por dia.

## Limitações
Escolha ainda em desenvolvimento: mapas, integração solar, layout, massa montada, CAD adaptado e revisão humana pendentes. Os picos de motor e a capacidade da bateria não demonstram sozinhos a viabilidade energética da viagem.

<!-- execucao-integrada:inicio -->
Método técnico integrado: Balanço funcional E_inicial+E_FV=E_final+E_consumida+E_perdas+E_cortada.

BEV AuroraSolar para2p,arquiteturaB por interfaceDCexternaOEM. Serviços48V independentes;interface física não demonstrada.

Escopo: A identidade técnica está definida; homologação da conversão e aprovação humana continuam separadas.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
