# Dados OEM do E-Ducato: variante de estudo e comparação MY24

Consulta documental em **12/11/2026**. Esta nota separa a ficha da variante usada no projeto de uma ficha oficial de outro mercado/ano, porque o código de opção `505.GG1.2` se repete e não basta, isoladamente, para identificar a homologação.

## Variante atualmente estudada — Eslováquia MY25

A ficha/catálogo Fiat E-Ducato válido a partir de 20/03/2026 para a Eslováquia lista `L3H2`, `4.250 kg`, `110 kWh`, motor de `205 kW` e código `505.GG1.2`. A cópia preservada fora desta worktree é `/home/mhc/motorhome_referencias_tarefas/fichas-eletricas/e-ducato-MY25-SK-20260320.pdf`, SHA-256 `e3becec7275a4a13df61aa7fc5e8b0f6eb38ff6c3584d755d5b1bbd5f5e6224f`; o YAML `config/arquitetura_eletrica_proposta.yaml` já identifica essa origem.

O documento informa para MY25: bateria 110/98 kWh bruta/líquida, 400 V nominal, tração dianteira, motor até 205 kW/410 Nm, carregador AC de 11 kW, carga DC até 150 kW com Combo CCS2, 0–80% em 55 min a 150 kW e limitador de 90 km/h para 4.250 kg. Dimensões publicadas: L3H2, 5.998 mm de comprimento, 4.035 mm entre eixos, 2.050 mm sem espelhos, altura 2.592–2.612 mm, piso de carga de 3.705 mm, largura entre caixas de roda 1.422 mm e altura interna 1.932 mm. A massa operacional sem motorista publicada para L3H2 é 2.790 kg, carga útil máxima 1.460 kg. O documento **não fornece limites por eixo** nem dados de CG da unidade, mapas contínuos do motor, corrente/tensão DC mínimas, handshake, curva de aceitação em baixa potência, topologia de isolamento ou permissão de fonte PV externa.

Esses valores são evidência oficial da oferta eslovaca MY25, não prova de que o E-Ducato MY25 brasileiro tenha essa configuração. O projeto continua usando-os como variante hipotética explicitamente escolhida, pendente de identificação/validação local. O limite de 150 kW é máximo anunciado: não permite inferir que 1, 20 ou 80 kW serão aceitos em qualquer condição.

## Comparador oficial — Polônia, especificação MY24 (edição 06/2024)

A [ficha técnica Fiat Professional Ducato/E-Ducato 2024 MCA, edição 06/2024](https://www.media.stellantis.com/uploads/pl/model-document/noweducatokatalog-66cd888c29081.pdf) lista E-Ducato L3H2 Maxi 4,25 t, bateria de 110,6 kWh brutos e 108 kWh úteis, tensão nominal 400 V e carga DC máxima de 150 kW. Para o furgão elétrico 4,25 t a mesma ficha publica limites máximos de eixo dianteiro/traseiro de **2.100/2.400 kg**, velocidade limitada a 90 km/h para N2 e carga admissível no teto de 0 kg para L3H2 N2; a tabela L3H2 de 3,5 t mostra 150 kg no teto. A tabela de massas não publica massa em ordem de marcha/carga útil para L3H2 elétrico 4,25 t (`b.d.`).

A lista de preços polonesa MY24 também relaciona `L3H2, 4,25 t, 110 kWh` ao código `505.GG1.2` ([catálogo](https://www.media.stellantis.com/uploads/pl/model-pricelist/noweducatocennik-65800b3362bc0.pdf)). Isso estabelece coincidência de código e classe comercial, não identidade técnica com a variante eslovaca MY25 nem com uma unidade brasileira. A divergência líquida (98 vs. 108 kWh) e a diferença de ano/mercado impedem substituir os 98 kWh do cenário atual. Não usar `0 kg` de teto como limite da SK MY25; registrar como dado da combinação polonesa MY24 indicada pela tabela.

## Triagem estática condicional das cargas por eixo

Como comparação de engenharia, apliquei os limites poloneses 2.100/2.400 kg aos **162 casos existentes** em `entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos/casos.csv`. O envelope existente varia layout, fator de massa, fração traseira OEM assumida, altura de CG e distribuição de água; as cargas dianteira/traseira OEM e o CG-base não foram medidos. A operação é uma filtragem simples, sem transferência dinâmica:

| Resultado da comparação condicional | A fixa (81 casos) | B conversível (81 casos) | Total |
|---|---:|---:|---:|
| Casos acima de 2.100 kg no eixo dianteiro | 27 | 27 | 54/162 |
| Casos acima de 2.400 kg no eixo traseiro | 0 | 0 | 0/162 |
| Menor margem dianteira ao comparador | -123,1 kg | -142,9 kg | -142,9 kg |
| Menor margem traseira ao comparador | 105,7 kg | 107,5 kg | 105,7 kg |

As margens são limite menos carga calculada; valor negativo indica excedência. **Não é avaliação de conformidade**: os limites não foram confirmados para SK MY25/Brasil e os casos são determinísticos hipotéticos. O resultado dá prioridade técnica à confirmação da etiqueta/homologação e à pesagem por eixo: a massa total abaixo do PBT não evita possível sobrecarga dianteira se os limites do comparador forem aplicáveis. No ponto-base integrado anterior (1.987,96/1.988,56 kg), as margens comparativas seriam 112,04/411,44 kg, também apenas condicionais.

Reprodução do filtro (no diretório raiz; sem alterar dados):

```bash
python3 -c 'import csv; p="entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos/casos.csv"; r=list(csv.DictReader(open(p))); print(sum(float(x["front_kg"])>2100 for x in r), sum(float(x["rear_kg"])>2400 for x in r))'
```

## Carga e interface externa

A [ficha eslovaca MY25](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf) especifica Combo CCS2 e potência DC máxima de 150 kW; a ficha polonesa MY24 especifica 400 V nominal e 50 kW/150 kW como condições de recarga pública, com tempos de 0–80% de 115/55 minutos. A Stellantis confirma para a oferta britânica a partir de 01/05/2025 carregador AC embarcado de 22 kW como padrão e 0–80% em 55 min num carregador DC de 150 kW ([comunicado UK de 09/04/2025](https://www.media.stellantis.com/uk-en/corporate/press/stellantis-announces-key-updates-to-large-van-line-up)); isso não altera o carregador AC de 11 kW listado para SK MY25.

As fontes confirmam o conector e máximos em mercados/configurações específicos. Não documentam os mínimos operacionais, protocolo e mensagens de sessão da unidade brasileira, aceitação de fonte DC solar variável, conversor/isolation design ou autorização Stellantis para adaptar a entrada externa. Arquitetura B permanece hipótese de estudo; a interface não é comprovadamente compatível ou autorizada.

## Registros oficiais consultados

- [Fiat Professional Slovakia — e-Ducato price list, válido desde 20/03/2026 (PDF)](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf): mercado SK, MY25 e MY26 no mesmo catálogo; cache/hash indicados acima.
- [Fiat Professional Poland — ficha técnica Ducato/E-Ducato 2024 MCA, ed. 06/2024 (PDF)](https://www.media.stellantis.com/uploads/pl/model-document/noweducatokatalog-66cd888c29081.pdf): especificações L3H2 4,25 t e tabela de eixos.
- [Fiat Professional Poland — tabela de preços E-Ducato MY24 (PDF)](https://www.media.stellantis.com/uploads/pl/model-pricelist/noweducatocennik-65800b3362bc0.pdf): associação do código `505.GG1.2` à classe L3H2/4,25 t.
- [Fiat Professional UK — anúncio do carregador embarcado 22 kW para veículos elétricos a partir de maio de 2025](https://www.media.stellantis.com/uk-en/corporate/press/stellantis-announces-key-updates-to-large-van-line-up).
- [Fiat Brasil — lançamento Ducato 2025](https://www.media.stellantis.com/br-pt/fiat/press/fiat-ducato-ganha-nova-versao-em-sua-linha-2025): descreve Ducato 2.2 diesel; não oferece especificação E-Ducato brasileira.

## Conclusão que altera o estado técnico

1. As dimensões, massa de base, 110/98 kWh, 205 kW/410 Nm, carregador AC 11 kW, CCS2, 150 kW máximo e 90 km/h continuam sustentados **somente para a referência eslovaca MY25**, e não como validação brasileira.
2. Surgiu um comparador oficial MY24 que publica os limites de eixo 2.100/2.400 kg. A grade condicional mostra possíveis excedências dianteiras em 54/162 cenários; não converter em reprovação da hipótese SK até confirmar que os limites se aplicam à variante exata.
3. A identidade do SKU brasileiro, cargas por eixo do SK MY25, capacidade do teto, cargas mínimas/protocolo DC e autorização OEM continuam sem evidência local. Não se alteraram parâmetros canônicos nem as 61 decisões.
