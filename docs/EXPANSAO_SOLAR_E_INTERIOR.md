# Cobertura ampliada e interior equipado - 25/10/2026

O teto anterior estava subaproveitado. A proposta atual ocupa a região traseira
com **três JA Solar450W** e o trecho sobre a cabine com **um Victron190W**:
**1540W expostos**, contra900W anteriores. Há uma segunda camada de três JA450W
com deslocamento lateral para uso estacionado, chegando a **2890W expostos**.
A cobertura fixa de quatro módulos é a proposta principal mais leve; os sete
módulos estão na alternativa de extensão em CAD. A construção continua condicionada
à estrutura/variante e à integração elétrica.

## Geometria que foi efetivamente testada

- No retângulo de3,705×1,870m, cabem três JA de1,134×1,762m, com folgas de30mm
  e margens mínimas de50mm. Quatro JA iguais não cabem nesse retângulo.
- A sequência traseira ocupa3,462m. O módulo de cabine ocupa X3,592..4,260m,
  largura1,485m e comprimento longitudinal0,668m. Fica além do compartimento,
  sobre a cabine; não foi confundido com espaço de carga extra.
- Os apoios foram prolongados até a primeira interseção vertical com a malha
  externa em cada ponto escolhido. Isso corrige sapatas flutuando no teto curvo,
  mas ainda não prova contato em toda a sapata, compatibilidade com os pontos OEM
  ou resistência da chapa. Travessas, longarinas, guias e pés têm sólidos CAD.
- Extensão lateral1,802m; largura aberta3,564m; altura recolhida aproximada2,805m.
  Os apoios ao solo são tubos telescópicos conceituais, guardados sob a cama.
- Recolhida, a camada superior cobre a inferior. Contam-se só três JA expostos,
  mais o190W; **não** sete módulos produtivos no mesmo espaço coberto.

Fontes primárias: [JA450](https://www.jasolar.com/uploadfile/2024/0112/20240112034704258.pdf),
[Victron, modelos atuais](https://www.victronenergy.com/upload/documents/Datasheet-BlueSolar-Monocrystalline-Panels-current-models-EN-.pdf),
consulta25/10. O antigo175W encontrado primeiro está descontinuado na ficha antiga;
adotou-se como candidato o **SPM041903903190W**,10,5kg,1,485×0,668×0,030m,
Vmp21,8V/Voc25,5V/Isc9,17A/gamma−0,0045/K. Não aumentar potência de um painel
arbitrariamente mantendo dimensões e massa do anterior.

## Geração e sombra

`scripts/calcular_expansao_solar.py` usa o dia solar e as hipóteses já documentados:
São CarlosA711/21junho,25°C,vento0,Ineichen/Faiman/PVWatts,10% de perdas adicionais
e conversão95% assumida. Estes valores não são eficiência validada da arquitetura.

| Estado/cálculo condicionado | Energia após perdas assumidas |
|---|---:|
| Histórico: doisJA450 | 3,2325kWh/dia |
| Recolhido: trêsJA450+190W | 5,5068kWh/dia |
| Aberto, sem nenhuma sombra entre placas | 10,3556kWh/dia |
| Aberto, correção geométrica de sombra direta | 10,3268kWh/dia |
| Aberto, desligando toda string inferior sempre que algum módulo recebe sombra | 9,1889kWh/dia |

A sombra direta é projeção de retângulos horizontais separados verticalmente
por60mm, com vetor solar do pvlib, orientação assumida X=norte/Y=leste. União
de sombras evita dupla contagem. A radiação difusa não teve fator de vista
calculado; o modelo de área sombreada não resolve diodos, mismatch nem curvas
I–V. Por isso9,19–10,33 é uma comparação entre modelos, **não faixa garantida**
ou intervalo de confiança. Árvore, antena, sujeira real e temperatura da montagem
empilhada ainda podem reduzir a geração.

O ensaio de habitação assume geladeira55W/duty50%, indução2,3kW por0,5h,
HVAC no ponto condicionado de duas pessoas/COP2,5 por3h, lavagem fria semanal
e0,4kWh/dia de outros serviços: **5,4265kWh/dia**, antes de perdas de armazenamento.
Não inclui energia de secagem. É cenário de uso, não perfil medido. Recolhido
restam apenas0,0803kWh/dia nesse balanço agregado; aberto restam3,7624–4,9003.
Os barramentos12/48V ainda precisam ser compatibilizados; saldo agregado não
comprova energia efetivamente transferível ao pack400V.

## Montagem e carga no teto

O desenho contém perfis tubulares30×30×3mm/40×40×3mm, travessas, sapatas,
guias e seis apoios telescópicos. **É conceito de integração**, ainda sem FEM,
travas de transporte, vedação, fixação OEM ou certificado de resistência.
O volume sólido CAD dos suportes equivale a **28,691kg**, assumindo alumínio2700kg/m³.
Sem parafusos, cabos e ferragens adicionais; não é pesagem nem BOM completa.
Módulos142,5kg + suportes28,691kg = **171,191kg no teto**, antes desses adicionais.

A [Fiat UK](https://www.fiat.co.uk/professional/models/ducato) publica teto até200kg,
dependendo da configuração e50kg por barra fixa. Isso **não confirma** o limite
da variante elétrica eslovacaMY25 escolhida. Há [rack Fiamma Ducato150kg](https://www.fiamma.it/en/product/roof-rail-ducato/).
Se o limite aplicável for150kg, esta montagem empilhada está **acima dele** e
deve ser rejeitada/reprojetada. Para200kg sobra28,809kg nominal, sem prova de
distribuição por barra, fixação, forças aerodinâmicas ou solicitação dinâmica.
Não aprovar simplesmente pela soma171<200.

Alternativas de execução: quatro módulos expostos sem segunda camada pesam76,5kg
antes do rack e liberam muita margem; transportar os três complementares em
suporte interior dimensionado e montá-los ao estacionar; ou pesquisar módulos
leves com subestrutura real. A primeira opção já cabe na geometria de cobertura,
mas o mecanismo completo de transporte da segunda ainda não foi dimensionado.
Não extrapolar estas opções como montagem pronta.

## Interior: agora há equipamentos reconhecíveis

`config/equipamentos_interior.yaml` e `scripts/gerar_cad_instalacoes.py` geram
GLB e STEP com sólidos autorais de integração, não CAD OEM copiado da internet.
Foi preferida essa solução para manter dimensões e procedência verificáveis
sem redistribuir geometrias de terceiros sem licença.

| Item | Dimensões de integração X/Y/Z | Origem / restrição |
|---|---|---|
| GeladeiraDometic NRX80C | 475×537×625mm;20kg | [Fabricante](https://www.dometic.com/en-gb/outdoor/motorhome-and-van/fridges/camper-van-refrigerators/dometic-nrx-80c-333351);12/24V,55W nominais, sem duty garantido |
| Lava-secaLG CV9011WC4A | 600×620×850mm;73kg | [LG](https://www.lg.com/br/lavanderia/lava-e-seca/cv9011wc4a/?search=%7B%7D);620mm total, não565mm; porta aberta1100mm |
| HVACDometic FreshWell3000 | 628×400×286mm;21kg | [Manualp13](https://www.dometic.com/externalassets/dometic-freshwell-3000-_104014.pdf);2700W de frio,230V50/60Hz,4,3A; não inferir potência ativa de corrente AC |
| InduçãoDometic CVI1350 | 350×350×55mm | [Manualp18](https://media.dometic.com/externalassets/cvi1525_9600050571_117210.pdf);2300W,versão50Hz; massa não preenchida sem ficha |
| SanitárioThetford365 | 383×427×414mm;4kg vazio | [Fabricante](https://www.thetford.com/au/products-and-support/porta-potti-365-portable-toilet/);15L descarga/21L resíduos |
| Pia/reservatório | Cuba400×380×160mm; tanque100L ideal | Desenhos autorais; parede, sifão, volume útil, massa e conexões pendentes |

A LG publica0,29kWh/ciclo frio e68,8L de lavagem; não usar0,29 como energia de
lavagem+secagem. Uma lavagem consome grande parte dos100L propostos, exigindo
planejamento de abastecimento. A profundidade com porta aberta pode bloquear
o acesso; isso foi registrado, não tratado como volume permanentemente livre.

Estrado longitudinal1,95×1,35m, colchão modelado1,91×1,31m, topo1,05m, lava-seca e HVAC sob o estrado;
cozinha1,40×0,58m, banheiro0,90×0,70m/H1,80m, mesa rebatível e dois assentos
ilustrativos na cabine. Dimensões de colchão versus reserva/estrutura, altura
sentada, manutenção, rodas e espessuras ainda precisam de revisão física.

O FreshWell3000 libera o teto, mas sua capacidade nominal2700W supera a carga
condicionada de duas pessoas2646W por apenas2%. Curva real em33°C, dutos e
cenários de maior ganho podem exigir outro aparelho ou redução de carga por
proteção solar. Ele não foi declarado solução térmica definitiva.

## Verificação e reprodução

- Sete envelopes de equipamentos sem interseção volumétrica entre si no retângulo
  OEM. Não é inspeção completa de sólidos/serviços contra a carroceria.
- Banheiro:81raios, folga externa amostrada mínima40,850mm na nova posição.
- STEP reimportado:160sólidos interior/239cobertura recolhida/311aberta; volumes
  positivos. Isso não verifica FEM, colisões intencionais ou topologia da montagem.
- Visualizador: sete seletores de itens, opção de retirar cama, abrir extensão
  e ocultar carcaça; abriu viafile:// comChromium,sem erros nem requisições HTTP.
- Métodos novos:4testes de envelopes/grades +3de sombra direta passaram.

```bash
.venv/bin/python scripts/gerar_cad_instalacoes.py --destino /tmp/instalacoes-novas
.venv/bin/python scripts/calcular_expansao_solar.py --destino /tmp/solar-ampliado
PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_ocupacao.py tests/test_sombra.py
```

Resultados vigentes em cache: `instalacoes-04`, `solar-calculo-03`,
`expansao-solar-02`, `layout-03`, `triagem-banho-03`, `visualizador-08`.
Documentos externos brutos ficam fora do Git; `expansao-fontes/manifesto.json`
registra downloads/hash e403 de LG/Fiat local, cujas páginas foram lidas viaweb.
Arquitetura elétrica proposta em `config/servicos_proposta.yaml`: duas strings
JA independentes a48V e módulo190W a12V com terceiroMPPT. Baterias de serviços,
DC/DC, EVSE, frequência, proteções e curvas continuam pendentes. Não ligaMPPT
diretamente aos400V nem promove estes estudos ao YAML global aprovado.

Cobertura fixa alternativa já exportada em `cobertura_fixa.step/.glb`: módulos76,5kg + suportes21,155kg estimados =97,655kg, sem ferragens adicionais. É a vista inicial do visualizador; a extensão é opcional. A sombra/energia fixa e recolhida têm a mesma potência exposta, mas estrutura e massa diferentes.

Área externa dos módulos expostos: **6,9863m² fixa** e **12,9806m² aberta**, contra3,9962m² nos doisJA iniciais. Área do módulo inclui moldura; não é área de células nem área projetada aerodinâmica.

Para reconstruir o visualizador a partir dos arquivos de código (os diretórios
de saída precisam ser novos):

```bash
npm --prefix scripts/visualizador ci
npm --prefix scripts/visualizador run build
.venv/bin/python scripts/gerar_visualizador.py \
  --glb entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb \
  --layout config/layout_proposto.yaml \
  --bundle scripts/visualizador/build/aurora.bundle.js \
  --licenca-three scripts/visualizador/node_modules/three/LICENSE \
  --instalacoes /tmp/instalacoes-novas --destino /tmp/visor-reproduzido
cp /tmp/instalacoes-novas/*.step /tmp/visor-reproduzido/
```

Python: extras `solar,cad,reports` do pyproject; ambiente desta execução usa
NumPy1.26.4,pvlib0.16.1,Gmsh4.15.2,trimesh4.12.2. `consolidar_expansao.py` é o
empacotamento específico dos diretórios de cache desta sessão, não um baixador
dos PDFs nem um requisito para abrir os arquivos portáteis já entregues.
