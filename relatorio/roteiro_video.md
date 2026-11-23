# Roteiro do vídeo — Aurora Solar (9 min, 7 integrantes)

Regras do enunciado: vídeo de 8 a 10 min, arquivo < 50 MB, todos os membros aparecendo
com tempos semelhantes. Cada bloco abaixo tem cerca de 75 s (≈ 180 palavras faladas) e
usa os slides de `slides.pdf` como fundo. Total previsto: 7 × 75 s + 30 s de abertura e
fechamento ≈ 9 min.

Dica de arquivo: gravar em 720p e exportar em H.264 a ~600 kbit/s (vídeo) + 64 kbit/s
(áudio); 9 min ≈ 45 MB. Exemplo: `ffmpeg -i bruto.mp4 -vf scale=-2:720 -c:v libx264 -b:v 600k -c:a aac -b:a 64k video.mp4`.

---

## Abertura — P1 (15 s) · slide 1

"Olá, somos o grupo do Aurora Solar, um motorhome elétrico solar para duas pessoas.
Cada um de nós vai apresentar a parte do projeto que desenvolveu."

## P1 — Estrutura, freios, massa e custo (75 s) · slides 2, 3, 11 · itens 1, 2, 3, 14, 15, 18, 24, 33

- Partimos de um furgão elétrico homologado, o Fiat E-Ducato L3H2 de 4250 kg, e o
  convertemos em motorhome. Isso mantém o trem de força e a segurança do fabricante.
- Pneus 225/75 R16C a 4,5 bar na frente e 5,0 bar atrás; freios a disco ventilados de
  300 mm com ABS; suspensão McPherson na frente e feixe de molas atrás.
- Somando cada componente da conversão, o veículo montado com duas pessoas, bagagem e
  100 litros de água tem 3976,5 kg, 273 kg abaixo do peso bruto total.
- Na frenagem de 30 para 10 m/s em 5 s, a simulação r–z do disco dá pico de 293 °C;
  com regeneração de 80 kW cai para 213 °C.
- O custo com impostos de importação é de R$ 789 mil; o veículo importado, com 35 %
  de imposto de importação, responde por R$ 619 mil.

## P2 — Bateria, elétrica e cabos (75 s) · slides 2, 8 · itens 6, 7, 9, 23, 30

- Temos duas baterias LFP: a de tração, de 98 kWh úteis a 400 V, do fabricante, e um
  banco de serviços de 14,4 kWh nominais (13,7 kWh úteis) a 48 V com três módulos
  Pylontech US5000.
- O banco de serviços tem controladores MPPT Victron (99 % no 250/60 e 98 % no 150/60) e um
  inversor de 5 kVA a 220 V e 60 Hz.
- No item 30, calculamos a corrente de fase do motor na potência máxima: 489 A RMS.
  Resolvemos o campo de temperatura r–θ no cabo, com convecção natural, radiação e
  contorno completo (conduíte, três fases agrupadas, perdas AC). O resultado depende
  do contorno: em cabo isolado a 25 °C dá 85 °C, mas no cofre do motor o cabo de
  120 mm² chega a 158 °C, acima da ficha de 150 °C. A menor bitola que atende o
  critério de 125 °C é 185 mm².

## P3 — Carroceria, CAD e CFD (75 s) · slide 4 · itens 16, 17, 19

- A carroceria de aço do furgão é mantida; adicionamos isolamento de 32 mm, claraboia,
  janela e o deck solar 4 cm acima do teto.
- As vistas cotadas mostram 5,98 m de comprimento, 2,08 m de largura e 2,69 m de altura
  com os painéis.
- Simulamos o escoamento a 80 km/h no OpenFOAM, com solo móvel. Descobrimos que as
  malhas antigas tinham atingido o limite de células do gerador de malha, por isso o Cd
  variava. Refizemos uma família de três malhas sem esse limite.
- O resultado é Cd = 0,622 ± 0,006, com área frontal de 4,83 m²; as malhas oscilam em
  torno do valor, então a incerteza vem da amplitude da oscilação, cerca de 1 %.

## P4 — Motor, transmissão e dinâmica (75 s) · slides 5, 6 · itens 4, 5, 20, 21, 22, 28

- O motor síncrono de ímãs permanentes tem 205 kW e 410 N·m de pico, com redutor de
  relação fixa.
- Com Cr de 0,012, a força de rolamento é 468 N; o arrasto passa o rolamento a partir de
  60 km/h.
- A 80 km/h são 28,6 kW nas rodas e 32,5 kW na bateria.
- A velocidade máxima é 90 km/h, porque essa versão tem limitador de série; então
  0 a 100 km/h não é alcançável. De 0 a 90 km/h, o tempo é 10,6 s.

## P5 — Solar, autonomia e otimização (75 s) · slides 5, 6, 7 · itens 8, 25, 26, 27, 29

- Em 21 de junho em São Carlos, o teto de 1540 Wp gera 5,9 kWh e os portáteis 8 kWh.
- Só com o sol do dia, o veículo anda 57,6 km a 40 km/h ou 31,9 km a 80 km/h. O
  consumo é de 4,44 km/kWh a 40 km/h e 2,46 km/kWh a 80 km/h.
- Com a bateria cheia indo até 30 %, a autonomia máxima em um dia é de 351 km, a
  20,7 km/h constantes.
- Para os 7000 km de Belém ao Chuí só com sol, o tempo é dominado pela espera para
  recarregar. O ótimo é a velocidade que gasta menos energia por km, 20,7 km/h,
  partindo às 17h45: a viagem leva cerca de 249 dias.

## P6 — Interior e conforto térmico (75 s) · slide 9 · itens 11, 13, 31, 32

- O interior tem cama fixa de casal, banheiro com cassete e chuveiro, cooktop de
  indução, frigobar de 93 litros e lava e seca.
- A climatização é um Dometic FreshWell sob o banco, de 2,7 kW, com ventilação natural
  como prioridade.
- Fechado ao meio-dia, sem ar e sem pessoas, o interior chega a 49 °C no modelo de zona
  única e 50 °C em média na simulação CFD 3D.
- Para manter 25 °C com 33 °C fora e duas pessoas dentro, precisamos de 2,65 kW de frio,
  ou 2,87 kW com a renovação de ar necessária para o CO₂. Quase 40 % disso é sol pelo
  para-brisa: com uma cortina refletiva fechada no veículo parado, a carga cai para 2,3 kW,
  dentro dos 2,7 kW do aparelho.

## P7 — Arrefecimento e térmica da bateria (75 s) · slide 10 · itens 10, 12, 34, 35

- Por ser elétrico, o veículo não tem óleo de motor; a lubrificação fica no redutor e nas
  graxas.
- Na carga de 20 a 80 %, a bateria sai de 25 °C e chega a 25,9 °C com 20 kW e a 32 °C
  com 80 kW, num modelo de circuito equivalente com dois nós térmicos.
- No circuito de arrefecimento do motor, a bomba elétrica opera a 31,9 L/min e 71,6 kPa.
  O radiador de fluxo cruzado rejeita 22,9 kW na potência máxima, com o fluido entrando
  a 67 °C e saindo a 55 °C.

## Fechamento — P7 (15 s) · slide 12

"Em resumo: o sol sustenta a habitação com folga, mas para mover 4 toneladas ele rende
dezenas de quilômetros por dia. Todo o código está no repositório do grupo. Obrigado!"
