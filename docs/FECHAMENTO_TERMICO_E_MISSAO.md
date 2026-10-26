# Bateria, ponto hidráulico e consistência da missão — 26/10/2026

Avanço deI05/I08/I10/I25/I26/I28/I29/I34/I35. **Resultados condicionados;
não é fechamento dos35itens nem autorização de modificação OEM.**
Fontes primárias consultadas online e PDFs locais lidos por trechos/páginas,
sem carregar anexos brutos no contexto.

## Restrição real de velocidade e transmissão

FichaFiatSK20/03/2026, SHA256`e3becec7275a4a13df61aa7fc5e8b0f6eb38ff6c3584d755d5b1bbd5f5e6224f`,
**página3**: limitador90km/h de série em4250kg, códigos0TK/58E.
Conferência visual em`fichas-eletricas/pagina-3.png` do cache externo.
Página4 dá90/130/130 nos modos; conservar o limite específico da versão escolhida,
sem presumir desativação. Não usar curvas100–130km/h antigas como modos viáveis.
`config/limites_operacionais_proposta.yaml` registra a divergência.

- I28: teto operacional≤90km/h. Atingir90 ainda depende das curvas/perdas/massa.
  **0–100 não é alcançável com limitador ativo**, portanto não inventar tempo.
- I33:108→36km/h permanece o ensaio prescrito pelo docente, não um evento de
  condução alegado nesta configuração limitada.
- [FiatDE, dados técnicos](https://www.fiat.de/professional/modelle/e-ducato/technical-data)
  confirma transmissão elétrica de relação fixa. Proposta retém redutor/diferencial
  OEM; relação numérica/rotação/eficiência/óleo ainda não obtidos. Não misturar
  97kWh úteisDE com98kWh úteisSK.
- [FiatUK, FAQ](https://www.fiat.co.uk/professional/models/ducato-electric) identifica
  110kWh comoLFP,205kW/410Nm. Referência de mercado, não rastreio do pack/VINSK.

## I34 — carga20/80kW: método e limites

`src/motorhome/bateria_carga.py`; configuração`bateria_termica_proposta.yaml`.
ECM resistivo e dois nós térmicos (bateria/refrigerante). Corrente positiva
na carga; `P=Uoc*I+R*I²`, raiz positiva estável; corrente limitada por potência,
Imax e Vmax. `dSOC/dt=I/(3600*Ah)`, eficiência coulômbica unitária assumida, sem envelhecimento. Resistência hipotética dependente deSOC/T,
OCV(SOC) hipotética e correção de temperatura com coeficiente entrópico.

`Q_irr=I²R`; `Q_rev=+I*T*dUoc/dT` na convenção de carga adotada.
`Cb*dTb/dt=Q_irr+Q_rev-UA_bc*(Tb-Tc)`;
`Cc*dTc/dt=UA_bc*(Tb-Tc)-UA_ca*(Tc-Ta)`.
Não confundir integral`Uoc*I` com calor ou energia química total incluindo entropia.
São verificados separadamente`E_terminal−integral(Uoc*I)−E_ohm` e
`E_ohm+E_rev−E_saida−deltaE_sensivel`.

Fundamento: apostilaSEM0571cap.2 e armazenamento sensívelp74Eq112;
[PyBaMM, modelos térmicos](https://docs.pybamm.org/en/v25.10.2/source/examples/notebooks/models/thermal-models.html)
para distinguir parcelas de aquecimento. Código autoral reduzido: **não foi
executado modelo eletroquímico PyBaMM, nem calibrado packOEM**.

Hipóteses principais: protocolo20→80%,245Ah equivalentes a98kWh/400V;
Rref0,06ohm,650kg×900J/(kgK),refrigerante20kg×3500J/(kgK),UA250/500W/K;
limites ilustrativos250A/450V/45°C; início25°C. Massa650kg não soma à taraOEM.
Nenhum mapaOCV/R/entropia/capacidade térmica/UA/limiteBMS foi medido no pack.

| Potência elétrica nos terminais | Tempo20→80% | T_bateria final | Energia Joule |
|---|---:|---:|---:|
|20kW|2,96287h|25,8705°C|0,45747kWh|
|80kW|0,75580h|31,9663°C|1,66431kWh|

Entropia nominal0;18combinações Rref0,03/0,06/0,12ohm e entropia−0,02/0/+0,02V/K,
mais2casos adiabáticos. Eventos terminam porSOC, temperatura ou tempo; não
continuar a curva além do limite hipotético. Resíduos dos casos nominais<2e−7J.
Refinamento adaptativo: maxstep120/60/30s contra5s/rtol1e−10; maior diferença
observada0,00291s/0,0000166K. Não atribuir ordem monotônica a solver adaptativo
com mudanças de passo e interpolaçãoOCV. Nove testes de energia, limites,
carga ideal, caso adiabático e parada por temperatura.

## I35 — bomba publicada e curva do circuito

[BoschPCE2-XL039202453G, ficha primária](https://www.bosch-ibusiness.com/en-2/products/product-categories/auxiliary-pumps-and-valves/pce-039202453g/pce-039202453g.pdf),
p1:12V/PWM/operaçãoS1/água-glicol50:50/massa0,46kg. Cache`hidraulica-fontes-01/pce2xl.pdf`,
2576254bytes,SHA256`7110a9250eda65f382b00ea7b1fe83f4d754cbcd8e351cef7883820aea2633b9`.
Curva azul é pressão e vermelha corrente; ambas conferidas visualmente.
Pontos lidos aproximadamente, incerteza de leitura assumida±3kPa/±0,2A,
interpolaçãoPCHIP sem extrapolação. Corrente não foi confundida com pressão.

Circuito fechado proposto:6m de mangueira20mmID,rugosidade1,5um,K=8,
rho1050kg/m³,mu1,5mPa·s. Quedas de motor/inversor/radiador20/8/15kPa
a30L/min, quadráticas e **assumidas**, não fichas dos componentesOEM.
Darcy–Weisbach,64/Re laminar/Haaland turbulento/transição interpolada;
gravidade se cancela no percurso fechado, sem somar altura do motorhome como
carga estática. ApostilaEqs49–62/93 fundamenta trocador/bomba, pp31/38/56.

Interseção única dentro do gráfico: **31,85099L/min**,0,557392kg/s,
71,62575kPa,8A/96W elétricos,38,0225W hidráulicos. Eficiência eletro-hidráulica
estimada39,61%; resíduo de pressão1,46e−11Pa. Variar a leitura de pressão±3kPa
dá aproximadamente31,38–32,31L/min; não é intervalo de confiança nem dispersão
de fabricação. Seis testes: Poiseuille, raiz analítica independente, domínio,
monotonicidade do circuito e entradas inválidas.

ComUA1000W/K/ar1kg/s/cp1006 assumidos e perda motor+inversor
`205kW*(1/eta−1)`, mais toda energia elétrica da bomba como calor neste circuito:

| eta combinada assumida | Calor total | Entrada radiador | Retorno refrigerante |
|---|---:|---:|---:|
|85%|36,272kW|91,355°C|72,762°C|
|90%|22,874kW|66,844°C|55,119°C|
|95%|10,885kW|44,913°C|39,334°C|

Perfis cruzados64² computados na vazão da bomba; desvio do calor do campo contra
a referência integral0,10–0,35W. Não é desequilíbrio de energia físico, mas erro
de discretização do trocador.205kW é pico, **não potência contínua comprovada**.
FaltamUA, perda real do núcleo/camisas, limites térmicos, NPSH/cavitação, curva
do ventilador e propriedades do fluido à temperatura de trabalho. Bomba candidata
não substitui circuitoOEM;96W não incluem ventilador/chiller.

## I25/I26/I29 — o teto atual muda a conclusão energética

O consumo residencial usado inclui A/C3h/dia/COP2,5 e lavagem fria1/semana;
**não inclui secagem da lava-seca**. Continua hipótese de operação, não uso medido.
Teto fixo1540W gera5,506849kWh/dia; habitação5,276506kWh/dia antes de perdas.
Com eficiências agregadas da habitação85/90/95/100%, saldos diários ficam
−0,700805/−0,355935/−0,047368/+0,230343kWh, antes de transferir para tração.
Isso impede reutilizar a agenda histórica de7000km como solução desta configuração.

`calcular_missao_atual.py` recalcula20–90km/h com a gradeCd/Cr/eta documentada.
I26 a40km/h:3,248–5,775km/kWh; a80:1,969–3,029. I25, **todo solar fixo reservado
à tração antes da habitação**,17,886–31,804km a40;10,845–16,681km a80.
São limites condicionados, sem interfaceHV demonstrada.

I29: no modelo de dias21jun repetidos, saldo≤0 e energia inicial ideal compartilhada
98+8,192kWh não permitem7000km; a grade mais otimista exige1054,744kWh de tração.
Mesmo100% de eficiência residencial dá limite necessário~4118dias, sem ser agenda
ou ótimo. Não estender um dia de junho por anos como previsão meteorológica real.
Limites necessários não incorporam toda dinâmica, regra8h/dia ou cronologia solar.

## Alternativa para resolver o déficit sem sobrecarregar o teto

Quatro **EcoFlow400W portáteis**, além do teto fixo, substituem como alternativa
a camada empilhada de JA que excedia a referência de carga. Somente no solo/parado.
[Manual primário2022](https://websiteoss.ecoflow.com/website/upload/2022/2/22/400W_Solar_Panel_User_Manual_1645511402758.pdf),
p8 conferida visualmente:400W,48Voc/41Vmp,11Isc/9,8Imp,gamma−0,0039/K,
1,068×2,390m abertos e1,068×0,620×0,024m dobrados. **21kg com bolsa**,15kg só painel.
Manual recomenda armazenamento vertical/sem compressão. SHA256
`d61b79b927ab0903f26d28a30ef352bd9c475e3a48c15f894e54f242fe0f65e0`.

2s2p em **MPPT150/35 dedicado**,48V:1600W vs2000W nominais,22AIsc vs40A,
Voc estimado ao frio−20°C111,552V vs150V máximo. Vmp quente aproximado65,764V
usando betaVoc como substituto: **não certifica partida/MPPT**.35A pode causar
clipping em baixa tensão; conferir curvaIV e coordenaçãoBMS/fusíveis/conectores.
Não ligar em paralelo com a string JA no mesmo rastreador.

pvlib com inclinação45°/norte, sem sombra/Faiman/perdas10%/conversão95% assumidos:
8,119545kWh/dia portáteis, total13,626394; saldo com habitação/90%7,763609kWh/dia.
Não equivale à energia já injetada na tração; sombras entre fileiras e cronologia
de montagem/condução ainda não otimizadas. O CAD de campo é ilustrativo.

Adição conhecida84kg bolsas+1,25kg MPPT=85,25kg; subtotal3458,605kg,
**ainda sem mobiliário/suportes/cabos/tubos/bagagem e eixos consolidados**.
Quatro reservas verticais1,10×0,065×0,65m sob cama não colidem com envelopes de
equipamentos emAABB; bolsa/pegadores não medidos, acesso/estrado/ancoragem pendentes.
CAD autoral324sólidos STEP reimportados positivos,GLBsolo/transporte separados.
Não é cópia do CAD fabricante. Integrado ao visualizador offline:324meshes novos,23seletores de equipamentos preservados, alternativas mutuamente exclusivas; Chromium sem errosJS ou requisiçõesHTTP.

## Reproduzir

Na raiz, destinos novos:

```bash
.venv/bin/python scripts/calcular_bateria_carga.py --destino /tmp/aurora-bateria-nova
.venv/bin/python scripts/calcular_hidraulica.py --destino /tmp/aurora-hidraulica-nova
.venv/bin/python scripts/calcular_missao_atual.py --destino /tmp/aurora-missao-nova
.venv/bin/python scripts/calcular_solar_portatil.py --destino /tmp/aurora-portatil-novo
.venv/bin/python scripts/gerar_cad_solar_portatil.py --resumo /tmp/aurora-portatil-novo/resumo_solar_portatil.json --destino /tmp/aurora-cad-portatil-novo
```

Caches vigentes em`/home/mhc/motorhome_referencias_tarefas/`:
`bateria-carga-01`,`hidraulica-calculo-01`,`missao-atual-02`,`solar-portatil-02`,`cad-portatil-01`.
Consolidador`consolidar_fechamento_termico.py` comparaSHA256 antes das cópias.
Dados estão nos itensI08/I25/I34/I35 e entrega parcial. Revisão humana pendente.

Avanço mecânico eBOM: [MECANICA_ROLAMENTO_E_CUSTOS.md](MECANICA_ROLAMENTO_E_CUSTOS.md), cache`bom-rolamento-02`. O consolidador também exige`--bom` e copia os resultados sem completar preços ausentes.
