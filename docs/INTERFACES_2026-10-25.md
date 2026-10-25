# Interfaces de integração - 25/10/2026

Todas as alterações abaixo são propostas, sem promoção ao YAML global aprovado.

| Origem → destino | Informação nova | Ação de integração necessária |
|---|---|---|
| P6 → P5 | I32 condicionado2,516/2,646kW frio; COP2–3assumido | Criar perfil horário real de HVAC; não usar100W estacionado como consumo da habitação climatizada |
| P6 → P3/P1 | Candidato HVAC3kW; isolamento32mm e revestimento6mm propostos | Obter dimensões/massa e modelar abertura/suporte, altura externa e redução do volume livre; não concluir encaixe pelo visualizador atual |
| P3 → P6 | Áreas/vidros ainda não extraídos da malha | Substituir caixa equivalente/vidros assumidos antes de fechar I31/I32 |
| P1 → P3/P4 | Pneu candidato diâmetro0,74422m/raio efetivo0,361262m | Rever roda no CAD, folga, contato, redução e ensaios CFD; não atualizar parcialmente como se fosse um veículo validado |
| P1 → todos | Reserva OEM1460kg;1166kg após painéis/pessoas/água no orçamento | Enviar BOM com massa/quantidade/posição; não duplicar componentes já incluídos no curb OEM |
| P2/P5 → todos | Interface solar48V→pack400V segue ausente | Dimensionar conversão/serviços e carga OEM estacionada; não adotar energia PV como acessível ao pack sem esta verificação |

Ver [cabine/HVAC](CABINE_E_HVAC.md), [pneus/massa](PNEUS_E_MASSA.md) e
[matriz35itens](REVISAO_35_ITENS.md). Não foram enviados avisos externos aos integrantes.

## Ampliação subsequente

P3/P5→P1/P2/P4/P6: cobertura fixa1540W/97,655kg estimados, extensão171,191kg recolhida/2890W aberta; conferir limite do teto exato. P6→P1: componentes conhecidos118kg, sete itens modelados, cargas de secagem ainda desconhecidas. P2→P5: trêsMPPT/barramentos12/48V propostos; transferência à tração400V não verificada. P3→P4: novo exterior equipado exige CFD atualizado; não reusar Cd antigo como validado. P1→todos: massa montada/custos/eixos ainda pendentes.
