# Agendas atuais com solar portátil — 27/10/2026

**Continuação posterior:** [interface discreta e PV12/48V separado](INTERFACE_CARGA_2026-10-27.md).
Os351,997km/202dias abaixo pertencem à hipótese agregada desta primeira etapa;
a continuação usa344,768km/276dias sob perdas/perfis e barramentos explícitos.
Ambas são condicionadas, sem validação OEM. Arquivos anteriores preservados.

Retomada do commit `fd8ae1e`, exclusivamente nesta worktree. Etapa técnica
condicionada de I27/I29: **35 itens em desenvolvimento, nenhum aprovado**.
Nenhum PDF/CAD/ZIP bruto foi carregado; foram usados resumos e dois CSV solares
da entrega anterior, conferidos contra o manifesto e suas integrais.

## Modelo e hipóteses

`src/motorhome/agenda_portatil.py` maximiza distância em um horizonte diário.
Mantém separadas a janela útil de tração98kWh e a bateria de serviços10,24kWh.
Tração inicia100%, reserva10%; I27 termina30% exatamente. Serviços inicia/termina
80%, reserva20% compatível com DoD máximo80% da proposta elétrica. Frações não
são uma calibração de SOC/BMS OEM. O alvo90% à meia-noite foi rejeitado pelo
modelo: a bateria cheia ao entardecer não sustentaria a noite e esse alvo final.

Estados: guardado → montagem → aberto → recolhimento → guardado/condução.
Montagem/recolhimento levam30min cada por hipótese, arredondados para cima à
grade. Portátil gera somente aberto; nenhuma condução ocorre nesse estado.
São permitidos vários ciclos, cada um pagando seus tempos. Portátil inicia e
termina guardado. O teto fixo pode gerar em movimento, sob o perfil de orientação
assumido. Não há geração da alternativa de teto empilhado.

Em horas/kW/kWh, com `h_drive` como tempo efetivamente conduzido em cada passo:

```
E_tração_next = E_tração + eta_HV * P_transferência * dt - P_tração * h_drive
E_serviços_next = E_serviços + (P_fixo + P_portátil - P_casa - P_transferência - P_corte) * dt
```

Transferência unidirecional **hipotética**, até2kW, eficiência90%, bloqueada em
todo passo com condução. Não é componente dimensionado, conexão OEM comprovada
ou energia livre de perdas. Há também cálculo com transferênciazero. Não se
somam as capacidades. Potência de tração já inclui800W auxiliares e eficiência
terminal–rodas90% assumidas; habitação é carga distinta, sem deduzir sobreposição.

Casa:5,276506kWh/dia divididos por90% =5,862784kWh/dia, distribuídos uniformemente.
Falta o perfil real de HVAC/equipamentos e a energia de secagem. Sem perdas
adicionais de bateria, limites de corrente, BMS, rampas, acelerações, relevo ou
dinâmica térmica. Massa4250kg, Cd0,62487678 e Cr0,012 são cenários anteriores,
não medições finais. Velocidades20/30/40/60/80/90km/h respeitam o limitador.

Cada passo contém uma velocidade escolhida, conduzida no início por duração
variável; o restante é parado/guardado. Não se misturam velocidades dentro do
passo. Os CSV exportam velocidade, duração, demanda terminal e potência mecânica
nas rodas. **Potência no eixo do motor permanece null**: perdas da transmissão
ainda não permitem calculá-la. Esse requisito de I27 continua pendente.

## Resultados reproduzidos

| Caso condicionado | Resultado | Alcance da otimização |
|---|---:|---|
| I27, sem transferência HV | 326,402651km;16,320133h conduzindo | Máximo na grade30min; tração100→30%, serviços80→80% |
| I27, transferência hipotética | 351,997229km;14,399908h conduzindo | Máximo na grade30min; mesmos SOC finais |
| I27, grade15min, mesma montagem30min | 352,145527km | Diferença+0,148298km/+0,04213%; não prova ótimo contínuo |
| I29, primeiro dia, até8h | 318,533458km | Maximização diária, tração100→30% |
| I29, ciclo diário, até8h | 33,245721km/dia | Tração30→30%, serviços80→80% |
| I29, construção de7000km | 202dias inteiros | Primeiro dia+200ciclos+último32,322377km; **não minimização global** |

I27 não recebe o limite8h/dia. O caso com transferência captura13,210133kWh,
contra13,626394kWh se estacionado com portátil aberto durante todo o sol.
Transferência7,347348kWh, perda0,734735kWh; tração consome75,212613kWh,
incluindo68,6kWh da carga inicial. Serviços terminam com a energia inicial.

No ciclo de I29,7,763609kWh/dia entram na transferência e6,987249kWh/dia chegam
à tração. O CSV completo preserva noites, montagem, recolhimento, reservas e
corte solar. O limite202dias inclui serviços/esperas até meia-noite final;
não afirma que a chegada precise esperar até esse instante. A data nominal de
2027 é consequência de repetir o mesmo dia claro de São Carlos21jun, **não
previsão climática/solar da rota Belém–Chuí**. Usar esse resultado como política
construtiva e limite superior somente no modelo explicitado.

Sem transferência HV, a tração dispõe apenas da carga inicial. Mesmo usando
100→10% e o melhor km/kWh dos modos, o teto matemático é419,660551km. Assim,
7000km são inviáveis **neste modelo sem interface**, apesar de haver energia
solar para serviços. Não é prova de inviabilidade de toda arquitetura possível.

Todos os casos diários retornaram certificado ótimo do MILP na grade; o último
dia apenas satisfaz distância fixa. A viagem repetida **não possui certificado
de menor tempo**. A verificação reconstitui energia sem usar o SOC exportado
como entrada; confere também o fim da condução dentro do passo, transições,
fonte solar do horário, corte, limites e condução por dia de calendário.

## Artefatos e reprodução

Entrega separada: [etapa27/10](../entregas/etapa_2026-10-27_agenda_portatil/README.md).
Caches:`agenda-portatil-03` e `agenda-portatil-grade15-01`, sob
`/home/mhc/motorhome_referencias_tarefas`. Tentativas01/02 são históricas.

```bash
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 .venv/bin/python scripts/calcular_agenda_portatil.py --destino /tmp/aurora-agenda-portatil-nova
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 .venv/bin/python scripts/calcular_agenda_portatil.py --daily-only --step-minutes 15 --destino /tmp/aurora-agenda-portatil-grade15-nova
.venv/bin/python scripts/verificar_agenda_portatil.py entregas/etapa_2026-10-27_agenda_portatil/grade30
.venv/bin/python scripts/verificar_agenda_portatil.py entregas/etapa_2026-10-27_agenda_portatil/grade15
```

Fontes/versões permanecem as dos estudos [solar/missão](FECHAMENTO_TERMICO_E_MISSAO.md)
e [dinâmica/energia](ENERGIA_E_OTIMIZACAO.md), com URLs/hashes anteriores; não houve
nova consulta de fabricante nesta etapa. Novos valores de operação são hipóteses
no YAML próprio, sem promoção ao global aprovado. O PDF/visualizador26/10 foram
preservados; este suplemento ainda precisa ser integrado ao memorial seguinte.

Verificação desta etapa:166testes passaram em2,44s;ruffsrc/scripts/testsOK;
estrutura35itens/7equipes e auditoria sem erros. Os dois conjuntos exportados
foram reabertos e seus CSV/hashes conferidos. Na viagem, distância reconstruída
7000,000000km, condução máxima8h/dia e maior resíduo por banco1,42e−14kWh.
O controle anterior de124artefatos+PDF também passou, sem entradas alteradas;
relatório no cache`agenda-portatil-03/qa_entrega_anterior.json`. Global manteve
SHA256`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.
Esses controles verificam implementação/integridade, sem aprovar dados físicos.

Próximo passo físico: verificar interface serviços48V→carga OEM, suas potências
mínimas/máximas, perdas e operação simultânea; substituir cargas uniformes por
perfis reais, extrair massa/Cd/Cr/mapas e só então otimizar tempo na rota.
