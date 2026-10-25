# Cabine e climatização - estimativa de 25/10/2026

Os itens I31/I32 agora têm um caso numérico reproduzível, com fonte de isolamento,
insolação por orientação, psicrometria e teste de passo temporal. **Não é resultado
validado da carroceria**: área de vidros, extensão da cabine dianteira, filmes,
pontes térmicas e capacidade térmica ainda são hipóteses explícitas.

## Entradas e fontes

`config/cabine_proposta.yaml` é uma proposta independente; não modifica o YAML
global aprovado. A caixa equivalente usa as dimensões máximas OEM do compartimento
3,705 × 1,870 × 1,932 m e acrescenta **1,10 m assumidos** para a cabine dianteira.
O volume equivalente é 17,3597 m³. Não foi extraído da malha do Ducato.

- [Armacell AF/ArmaFlex](https://www.armacell.com/en-DE/product/technical-specs/afarmaflex),
  seção Thermal conductivity, consulta 25/10/2026: para chapas até 32 mm,
  `k = (33 + 0,1 T + 0,0008 T²)/1000`, T em °C. Avaliação fixa a 40°C fornece
  **0,03828 W/(m K)**. Não utilizar o valor de 0°C indiscriminadamente.
  Proposta: 32 mm de isolamento e 6 mm de revestimento interno com k assumido
  0,13 W/(m K). A página foi conferida pela ferramenta web; download local teve
  HTTP403, portanto não há hash de um HTML Armacell baixado.
- [Buck Research, manual CR-2, dezembro de 2009](https://www.hygrometers.com/wp-content/uploads/CR-2-users-manual-2009-12.pdf),
  apêndice psicrométrico p.20: coeficientes da expressão de pressão de saturação.
  Aqui se aproxima o enhancement factor por EF=1, declaradamente. Intervalo do
  código restrito a 0–50°C; não é modelo de umidade dinâmica da cabine.
- INMET A711 e pvlib 0.16.1: mesmas coordenadas/altitude/data do estudo solar.
  POA isotrópica por orientação; teto horizontal, quatro paredes verticais e
  piso sem sol. A irradiância de céu limpo já calculada a 25°C é reutilizada em
  I32, cujo balanço térmico usa exterior 33°C.

O código usa h interno 3 e h externo combinado 8 W/(m² K), absorptância 0,3,
UA adicional de pontes térmicas 10 W/K, U de vidros 5,7 W/(m² K), fator solar
0,6 e C efetiva 200 kJ/K: **todos assumidos**, sem atribuição aos fabricantes.
O filme externo engloba convecção natural e radiação linearizada com meio à
temperatura ambiente; não se somou outra troca radiativa sobre ele. Sem crédito
de sombra dos painéis. Não representa estratificação, pontes individuais,
radiação de céu frio, infiltração real nem inércia distribuída das paredes.

## Equações e correspondência com a apostila

Fourier p.9 e Newton p.10: `1/U = 1/hi + soma(d/k) + 1/ho`.
O U opaco calculado é 0,7460 W/(m² K); UA total é 65,4366 W/K.
Para superfície opaca, temperatura sol-ar simplificada `Tsa = Ta + alfa I/ho`,
logo ganho solar equivalente `U A alfa I/ho`. O ganho por vidro é `g A I`.
As parcelas opacas e envidraçadas usam áreas disjuntas, sem dupla contagem.

Armazenamento sensível da p.74, Eq.112: `C dT/dt = Qsolar(t) - UA(T-Ta)`.
I31 começa às 06:00 em 25°C, sem ocupantes, equipamentos, A/C e infiltração.
O início é hipótese necessária porque o enunciado não define histórico térmico.
Solução exponencial exata por intervalo com carga média das pontas. O resultado
é de uma zona térmica concentrada, permitido como estimativa de I31; **não**
substitui os campos multidimensionais obrigatórios de I30 e I33.

I32: balanço permanente com condução, sol, equipamentos, ocupante e ventilação.
UR50% exterior e interior; pressão barométrica pela altitude A711. Ventilação
assumida 30 m³/h, sem recuperação. Razão de umidade `w = 0,621945 pv/(p-pv)`;
ar seco calculado nas condições exteriores. Sensível `m_da (cp_ar+1860 w_ext) ΔT`,
latente `m_da h_fg max(w_ext-w_int,0)`. Por pessoa, 75 W sensíveis e 55 W latentes
assumidos; equipamentos internos 100 W. COP não vem do catálogo: sensibilidade
2 / 2,5 / 3. Os 2.200 W nominais do A/C são capacidade térmica, não consumo.

## Resultados condicionados

| Grandeza | Valor nominal |
|---|---:|
| I31, meio-dia local | 49,079°C |
| I31, pico às 14:07 | 49,597°C |
| Equilíbrio com sol congelado ao meio-dia | 48,767°C |
| Constante de tempo C/UA | 0,849 h |
| Diferença I31 meio-dia, passos 1 e 5 minutos | 0,00081 K |
| Resíduo energético integrado I31 | 6,03 × 10⁻⁹ J |
| I32, capacidade de frio para uma pessoa | 2.515,90 W |
| I32, capacidade de frio para duas pessoas | 2.645,90 W |
| I32, eletricidade com COP assumido 2,5, uma/duas pessoas | 1.006,36 / 1.058,36 W |

A diferença transiente versus equilíbrio de 0,312 K ao meio-dia neste cenário
não prova regime permanente ao longo do dia: há defasagem do pico e histórico
solar variável. A constante de tempo depende fortemente da massa efetiva assumida.

A sensibilidade executa 48 combinações: quatro orientações, absorptâncias
0,3/0,7, fatores solares 0,3/0,6 e C de 100/200/400 kJ/K. Não são intervalos
estatísticos de confiança. JSON inclui cada caso e as respectivas cargas I32.

## Seleção preliminar e interface com energia

O [Dometic FJX4 2200](https://www.dometic.com/en/product/dometic-freshjet-fjx4-2200-9600051002?v=9600051003)
publica 2.200 W de frio; fica abaixo de ambas as cargas nominais calculadas.
O [FJX7 3000](https://www.dometic.com/en/product/dometic-freshjet-fjx7-3000-9600050995)
publica 3.000 W e compressor inverter/bomba de calor; é candidato para revisão,
**não seleção definitiva**. Ainda faltam capacidade e COP nas condições de
projeto, curvas, frequência, partida, massas, dimensões e instalação no teto.
Não concluir que o modelo de 3 kW atende todos os casos da sensibilidade.

Com COP assumido 2,5 e uma pessoa, três horas na carga de meio-dia consumiriam
3,019 kWh antes do inversor: quase os 3,233 kWh solares diários de dois módulos.
É uma comparação de escalas, **não integração diária do A/C**. A agenda anterior
usava somente 100 W estacionado e não deve ser rotulada como habitação com HVAC.
I13, I18, I24, I25–29 precisam receber equipamentos e perfis reais antes do fechamento.

## Reprodução e revisão

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_cabine.py
.venv/bin/python scripts/calcular_cabine.py --destino /tmp/cabine-nova
```

Saída vigente: `/home/mhc/motorhome_referencias_tarefas/cabine-calculo-02`.
CSV, JSON, figura e hashes disponíveis na entrega parcial. `cabine-calculo-01`
foi substituído para corrigir o eixo gráfico na passagem de 24:00 para 00:00;
valores numéricos preservados. As verificações analíticas cobrem resistência,
solução exponencial, equilíbrio, conservação e psicrometria de referência.
Revisão por outro integrante, medição CAD e validação física continuam pendentes.
