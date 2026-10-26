# Frenagem prescrita: campo r–z e pesquisa de componentes

26/10/2026 — I03/I33, liderança P1. **Estudo condicionado; não seleção/homologação.**
Não altera parâmetros globais ou soma freios à tara OEM. Exterior/interior CAD preservados.

## O que veio de fontes reais

- [Brembo09.D018.11](https://www.bremboparts.com/europe/en/catalogue/disc/09-D018-11):
  referência comercial dianteira ventilada, diâmetro300mm, espessura32mm.
  Consulta ao catálogo primário, não cópia da base TecDoc ou do CAD comercial.
  **Compatibilidade com E-DucatoMY25/4250kg não confirmada.** Variante/VIN, pinça,
  pastilha e disco traseiro precisam conferência; não comprar pelo diâmetro.
- [Topczewska et al., Materials2022,15,6821](https://doi.org/10.3390/ma15196821),
  tabela2, material do disco ferroviário a25°C: rho7100kg/m³, cp500J/(kgK),
  k51W/(mK). **Não são propriedades medidas do produtoBrembo.** Artigo abertoCC-BY.
  Página do editor retornou429; PMC apresentou desafio de navegador.
  A tabela foi conferida no XML original disponibilizado pelo
  [EuropePMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9571107/fullTextXML).
  Cache externo`freios-fontes-01/PMC9571107.xml`,212925bytes,
  SHA256`ef5d73b16a00a55a9bb64867e54960a273db128ad4b51baadb48dd924f0b7d21`.
- Enunciado2026p.2/I33:30→10m/s em5s, início25°C. ApostilaSEM0571cap.2,
  Fourier/Newton, páginas físicas9–10: fundamentam condução e convecção.
  Extrações locais consultadas; nenhum PDF bruto foi reinserido no contexto.

## Geometria e hipóteses explícitas

`config/freios_proposta.yaml` é proposta própria. PBT4250kg é cenário, não massa
consolidada. Duas placas anulares iguais e independentes de8mm, canal16mm,
raios90–150mm, faixa de contato100–145mm. Os8/16mm somam32mm, mas **não são
cotas publicadas do produto**. Massa de duas placas5,139143kg, sem cubo/aletas;
não confundir com massa comercial. Sem condução pelo cubo/aletas, radiação,
propriedades variáveis, deformação ou modelo de pastilha.

Simetria axial: resolve uma placa de0≤z≤8mm e duplica energia/massa.
Convecção no canal50 e na face de atrito/borda20W/(m²K), ambiente298,15K;
valores assumidos, constantes. Raio interno adiabático. Fonte média na
circunferência, fluxo uniforme no anel (hipótese de desgaste uniforme), não
pressão uniforme nem contato móvel. Fração dianteira0,7, disco0,9, regeneração0.
Constância de propriedades além de25°C é extrapolação a investigar.

## Equações e discretização

Assume desaceleração constante a=4m/s², v(t)=30−4t,0≤t≤5s.
Distância100m; `E_trans=m*(30²−10²)/2=400*m J`; `P_trans=m*a*v(t)`.
E_trans=1,70MJ, potência510→170kW, média340kW.

Potência de uma placa dianteira:

`P_placa=m*a*v(t)*(1-f_regen)*f_dianteiro*f_disco/4`.

Divide por duas rodas dianteiras e duas placas por disco. Energia por disco
535500J. Balanço da distribuição:1,19MJ dianteiros,1,071MJ nos dois discos,
119kJ restantes nas pastilhas dianteiras;510kJ permanecem no eixo traseiro
sem simulação própria. Regeneração, arrasto e rolamento zerados no cenário;
**inércias rotativas omitidas**, portanto não é limite superior completo.

PDE: `rho*cp*dT/dt = (1/r)*d/dr(r*k*dT/dr)+d/dz(k*dT/dz)`.
Volumes exatos`pi*(r_e²−r_w²)*dz`, faces radiais com resistência logarítmica,
axiais com`dz/(k*A)`. Integração Crank–Nicolson, fonte temporal no ponto médio
(exata para potência linear). Fração de área de contato integrada exatamente
nas células cortadas. Robin usa resistência de meia célula; temperatura da
superfície reconstruída incluindo fluxo aplicado, e não confundida com a do
último centro celular. Convecção inclui parcela da fonte liberada diretamente
pela face. Resíduo=entrada−saída−armazenada.

## Resultados do caso nominal condicionado

Malha96×32, passo0,005s; cada disco recebe535,500kJ, armazena531,689963kJ,
libera3,810037kJ por convecção. Resíduo4,31e−9J. Máximo superficial durante
a frenagem334,990627°C (aos5s, imediatamente antes de retirar a fonte);
máximo dos centros celulares333,111121°C. Temperatura inicial298,15K.
Não se calculou resfriamento posterior nem temperatura instantânea sob pastilha.

| Malha r×z | Máximo superficial °C | Máximo celular °C |
|---|---:|---:|
|12×4|335,606616|320,570809|
|24×8|335,005930|327,487909|
|48×16|335,001141|331,242130|
|96×32|334,990627|333,111121|

Diferença superficial final0,010514K; centros celulares1,868991K, em posições
distintas da superfície. **Não declarar independência de todo o campo ou ordem
espacial2D só pelo máximo superficial.** Faixa de contato descontinua no raio.

Separadamente,96×32 e passos0,079365/0,04/0,02/0,01s contra0,005s dão erros
máximos do campo final0,015979/0,000960/0,000228/0,0000457K.
O passo mais grosso não está na faixa assintótica de ordem temporal.

Verificação independente: série de cossenos de placa1D adiabática, fluxo
linear no tempo, comparação com **médias celulares**, não valores pontuais.
16/32/64células: erros0,016270/0,004270/0,001096K, ordens1,93/1,96.
Esse limite verifica condução axial/tempo/fonte; não substitui validação do
conjunto ventilado real. Testes adicionais: conservação, partição, ausência
de fonte, superposição, energia média analítica e rejeição de entradas inválidas.

Sensibilidades48×16: fração dianteira0,6–0,8 e disco0,8–1 levam261,19–418,65°C.
Alterar ambos filmes entre0/20/50/100W/(m²K) mantém o resultado condicionado;
com h100, saída12,669kJ. **Incerteza física das entradas domina o erro numérico.**
Sem temperatura limite OEM, curva de atrito/fade ou tensão térmica, esses
números não demonstram aprovação/reprovação do componente.

## Reproduzir e localizar

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests/test_freios_axisimetricos.py -q
.venv/bin/python scripts/calcular_freios.py --destino /tmp/aurora-freios-novo
.venv/bin/python scripts/consolidar_freios.py --origem /tmp/aurora-freios-novo
```

Destino deve ser novo. Fonte autoral`src/motorhome/freios_axisimetricos.py`;
script grava SHA256 das entradas e resumo/campos/histórico/convergências/figuras.
Cache vigente`/home/mhc/motorhome_referencias_tarefas/freios-calculo-03/`.
Resultados no itemI33 e na entrega parcial, prefixo`freios_`.

Próximos dados para fecharI03/I33: peça exata dianteira/traseira, pinça/pastilha,
cotas/massa reais, material vsT, centro de gravidade/limites dos eixos,
distribuição hidráulica/EBD, inércias, mapa de regeneração/aderência, contato
móvel e condições de resfriamento. Revisão humana permanece pendente.
