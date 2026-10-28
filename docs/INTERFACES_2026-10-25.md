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

## Integração elétrica posterior — substitui valores de massa/consumo acima

P2/P3→todos: banco51,2V200Ah10,24kWh/BMS,MPPTs,inversor e conversor noCAD;
208sólidos adicionais, cotas de tração estimadas. P6→P2/P5: induçãoIE3TP220V60Hz2000W
substituiCVI1350EMEA; consumo assumido semsecagem5,276506kWh/dia, saldo solar fixo
0,230343kWh antes do armazenamento/conversão. P2/P6→P1: serviços115,4kg adicionais,
indução2,3kg; subtotal3373,355kg ainda incompleto. Manual do inversor recomenda
200Ah/200A/70mm² por poloaté5m; não cabo de tração nem circuito aprovado.
P2/P7: radiador/bomba/HV noCAD são reservas, sem curvas/perdas/cálculoI35.
Ver`docs/CAD_TRACAO_E_SERVICOS.md`; nenhum aviso externo foi enviado.

## Agendas27/10 — proposta, sem alteração de componentes

P5→P2/P7: transferência serviços→tração2kW/90% é apenas hipótese de cálculo,
só parado. Sem interface, tração não recebe solar e7000km não fecham neste modelo.
Serviços10,24kWh/SOC80→80%/reserva20%; tração98kWh com SOC final30% exato emI27.
P5→P6: demanda residencial uniforme5,862784kWh/dia após perdas90%; faltam
perfil horário e secagem. P5→P3/P1: montagem/recolhimento30min cada e massa4250kg
são hipóteses; não validam fixações/acesso/eixos. P5→P4: potência nas rodas
exportada, eixo motor desconhecido. I29 tem política construtiva202dias, não
ótimo global ou previsão da rota. [Método/evidências](AGENDA_PORTATIL_2026-10-27.md).
Nenhum aviso externo foi enviado; parâmetros globais preservados.

## InterfaceAC e solar separado — continuação27/10

P5→P2: candidatoEVSE16A50/60Hz não comprova OBCMY25 monofásico60Hz; confirmar
faixas, PE/DR/proteções, corrente aceita e handshake. PV190W/12V deixa de entrar
no balanço48V/HV sem conversão demonstrada. P5→P6: A/C12–15h/fogão19–19h30 e
cargasDC uniformes assumidos; casa/perdas/standby6,428118kWh/dia, sem secagem.
P5→P1: EVSE~2,55kg é candidato, ainda sem incorporação a massa/eixos/custos.
P5→todos: novo cenário344,768kmI27/276diasI29; anterior352km/202dias é comparação
sob hipóteses agregadas. Sem interface real ou ótimo global demonstrados.
[Resultados, fontes e fronteiras](INTERFACE_CARGA_2026-10-27.md).

## Rota geográfica28/10

P5→P4/P1: corredorOSRM7511,282km e marco7000km, velocidades aproximadas por via,
relevoDEM5km e consumo por trecho com massa4250kg/Cd/Cr ainda condicionados.
P5→P2/P6:ERA5 e sol variável por calendário/local revelam falha da política
de serviços após4112,66km no caso60km/h, sequência nublada com geração<6,428kWh/dia.
Implementar reserva/previsão e rever demanda/armazenamento antes de afirmar
viagem realizável. P5→todos: céu limpo60km/h chega em330,93dias; não mínimo
global. Roteamento não verifica placas/estacionamentos/ancoragens.
[Método, dados e revisão35](ROTA_REAL_2026-10-28.md). Nenhum aviso externo enviado.
