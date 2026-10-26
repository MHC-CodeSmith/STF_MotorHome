# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# I10 — arquitetura térmica proposta

Reter a instalação OEM de tração, sem substituir componentes com base nos
resultados condicionados. Estudar circuito motor+inversor em série separado
do circuito de bateria: níveis de temperatura e controles distintos.

I35 agora inclui interseção da curva BoschPCE2-XL039202453G com circuito
proposto; perdas das camisas/radiador/tubos ainda assumidas. I34 tem dois nós
bateria/refrigerante, R(SOC,T), calor reversível e eventos de parada.
[Equações, fontes, hipóteses e limites](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).

Serviços: inversor/MPPT/DC-DC em armário seco separado da água. Perda estimada
P_out*(1/eta-1):4000W/eta0,90 exige dissipar444,4W no cenário. Para10K de
aquecimento do ar e rho1,1kg/m³, cp1006J/(kgK), mínimo ideal de vazão0,0402m³/s
(144,6m³/h). É balanço de ar ideal, não seleção de ventilador: faltam pressão,
recirculação, mapa real e derating térmico. Manter100mm de reserva do manual
inversor não comprova ventilação. Não ligar circuito de água a armário elétrico.

Auxiliares: bomba candidata96W a12V; ventilador/chiller/controladores ainda sem
curvas e orçamento fechado. Não duplicar trem de força OEM na massa. Revisão
P2/P4/P7, limites térmicos e integração física PENDENTES.
