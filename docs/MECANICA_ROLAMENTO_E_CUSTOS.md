# Mecânica retida, rolamento comparativo e BOM — 26/10/2026

I02/I03/I05/I12/I14/I20/I24. Pesquisa e cálculo reproduzível, **sem aprovação final**.
Não se alterou o trem de força OEM nem o YAML aprovado.

## Fonte primária de suspensão, freios e direção

[FiatUK MY25.5, vigente01/07/2025](https://www.fiat.co.uk/content/dam/fiat2023/professional/uk/tools/pricelist/ducato-and-e-ducato-van.pdf),
p25, seção elétrica110kWh, conferida visualmente. Arquivo3449628bytes,
SHA256`e207632d48d490dd47637cb012f7b7d5d499b4b7c72b3232fcbfe888a5a53a67`.
Cache externo`hidraulica-fontes-01/educato-UK-MY25_5.pdf`/`educato-UK-tecnica.png`.

Arquitetura publicada: dianteira pseudo-MacPherson com molas helicoidais,
amortecedores hidráulicos e barra estabilizadora; traseira reforçada com feixes
duplos/amortecedores acima de3,5t. Freios dianteiros ventilados/traseiros a disco;
transmissão elétrica fixa. Direção elétrica consta da brochura e do
[comunicado primárioStellantis](https://www.media.stellantis.com/uk-en/fiat-professional/press/fiat-professional-unveils-the-new-lineup-a-new-generation-at-work).
Proposta: **reter os conjuntosOEM**, não aumentar PBT por adicionar molas.

Ressalvas de variante: referênciaUK não substitui placa/eixos da unidadeSK505.GG1.2.
Não adotar sem conferir os95Ah/180células listados nessa brochura: não fecham
automaticamente o balanço110kWh/400V e não definem topologia. Não misturar com
diesel p27 ou selecionar peças pelo modelo visual2014. Rigidez, amortecimento,
massas e cargas por eixo montado ainda pendentes.

## Lubrificação correta para a arquitetura elétrica

Não há motor a combustão, portanto não dimensionar bomba/cárter/óleo de motor
diesel. A transmissão elétrica continua tendo engrenagens/diferencial e o veículo
tem rolamentos/juntas: identificar e preservar a lubrificação OEM apropriada.
O motor elétrico não recebe automaticamente óleo de motor ou banho de glicol.
DireçãoEPS não implica reservatório de direção hidráulica.

Consultas a manuais antigos retornaram especificações de caixas diesel,
inadequadas para afirmar a classe/quantidade de óleo do redutorBEV atual.
Sem manual de serviço da variante, **grau, volume e intervalo permanecem null**.
Isso iniciaI12 como especificação de escopo e interface, mas não o fecha.
`config/mecanica_comparativa_proposta.yaml` contém pontos/pendências verificáveis.

## I20 — estimativa com rótulo de pneu real, como alternativa

[ContinentalVanContactCamper0451473](https://www.contimediacenter.com/eulabel/en_GB/04514730000/),
225/75R16CP118R, classe de eficiênciaC. É **outro modelo** do A/S04514690000
anterior; não herda massa16,919kg, raio efetivo ou pressão daquele artigo.

[RegulamentoUE2020/740, AnexoIParteA](https://eur-lex.europa.eu/eli/reg/2020/740/oj)
relaciona classeC de pneusC2 aRRC6,8–8,0N/kN. Coeficiente adimensional da
comparação:0,0068–0,0080; ponto médio0,0074 é escolha explícita, não medição.
Em4250kg assumidos e plano:`F_rol=Cr*m*g`:

| Cr comparativo | F_rol | P_rol a40km/h | P_rol a80km/h |
|---|---:|---:|---:|
|0,0068|283,412N|3,149kW|6,298kW|
|0,0074|308,419N|3,427kW|6,854kW|
|0,0080|333,426N|3,705kW|7,409kW|

Rótulo é ensaio normalizado, nãoCr rodoviário deste motorhome carregado.
Faltam pressão/carga/superfície/temperatura, rodas e raio efetivo doCamper.
**Alternativa não adotada automaticamente:** a grade anteriorCr0,008/0,012/0,016
continua explicitamente uma sensibilidade. Não melhorar a autonomia usando um
pneu e conservar massa/CFD/raio de outro como se fosse o mesmo cenário final.

## I24 — BOM de verdade, custo final ainda aberto

`calcular_bom_e_rolamento.py` extrai27linhas rastreáveis de equipamentos/chassi/
solar. Itens de tração já incluídos no chassi são marcados para não duplicar.
Todas as quantidades e massas conhecidas são separadas das ausências; lista
não substitui levantamento de chapas/mobiliário/isolamento/tubos/cabos/ferragens.

[Electrolux, oferta públicaIE3TP](https://loja.electrolux.com.br/cooktop-de-inducao-portatil-1-zona-electrolux--ie3tp-/p?idsku=310118641)
mostraR$439promocional/R$589referência na consulta26/10/2026. Exige seleção de
tensão e entrega, portanto **não foi confirmada cotação vinculante da versão220V**.
É referência de preço, não custo instalado nem compra realizada. Frete/tributos
discriminados não confirmados. Não adicionar um percentual arbitrário de impostos.

Há20linhas nãoOEM sem oferta registrada no levantamento atual, além dos escopos
faltantes. Subtotal de referênciaR$439 não é custo do motorhome; total final
com tributos/frete permanece **null**. Os€50990 da fichaSK são semIVA e não
preço de importação/homologação brasileira emR$. Não inventar câmbio/tributação
ou tratar preço europeu como custo nacional instalado.

## Reproduzir

```bash
.venv/bin/python scripts/calcular_bom_e_rolamento.py --destino /tmp/aurora-bom-nova
```

Destino novo; configuração`mecanica_comparativa_proposta.yaml`/`custos_proposta.yaml`.
SaídasCSV/JSON comSHA256 de todas as entradas. I12/I14/I20/I24 seguem parciais:
óleo/placa por eixo/cargas/pressão e cotações completas precisam dados reais.
