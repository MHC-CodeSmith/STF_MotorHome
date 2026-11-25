# Leitura integrada das simulações e comparações dos PRs

Revisão de 25/11/2026, posterior a `75202b5`. O usuário pediu que o relatório pudesse
ser entendido pela leitura, com simulações junto da explicação e sem organização em
lista de respostas. A versão anterior de 39 páginas não atendia bem a esse objetivo.

O texto agora mantém a sequência do Cuca — especificações, custo e simulações — com
12 grupos de componentes e 11 análises. Objetivos e discussão são texto corrido.
As análises térmicas abrem as simulações: freios, cabos, cabine, ar-condicionado,
bateria e circuito de arrefecimento. Cada uma liga fenômeno, hipóteses, equações,
figuras e interpretação. Os 35 itens continuam rastreáveis por rótulos e tabela final.
As figuras térmicas permanecem dentro da seção correspondente.

## Fael: comparações executadas e apresentadas

As comparações anteriores de quatro horários solares, quatro candidatos de portátil,
CFD com/sem deck, raios de pneu, velocidades 20,5/40/80 km/h e reservas continuam no
relatório. Não se substituem seus resultados pelo simples registro de um checklist.

Foram acrescentados:

- 20 casos de consumo a 40/80 km/h, alterando um parâmetro por vez: massa, Cd, Cr,
  rendimento ou auxiliares. O cenário nominal permanece inalterado.
- 140 janelas MILP de cinco minutos para pisos de saída CC de 0,5 e 1 kW, com e sem
  habitação, na mesma grade de partidas da análise anterior. Sem habitação a 80 km/h:
  reduzir 1→0,5 kW eleva o crédito 11,34→12,66 kWh e a distância 27,75→30,99 km.
  Com habitação, ambos dão 6,19 kWh/15,15 km. O ganho histórico de 0,78 kWh não é
  confundido com o resultado do cenário atual.
- Seis missões com janela fixa 08–16h, velocidades 40/80 km/h e zero, um ou dois dias
  inteiros parados entre dias de condução. Abertura dos portáteis segue a agenda nos
  dias de condução, sem reabertura adaptativa durante uma parada antecipada; nos dias
  inteiros parados, podem gerar todo o dia. Serviços continuam consumindo energia.
  A condução diária interrompe por reserva de serviços em 7,2 dias. Com uma pausa,
  a chegada leva 628,3/1156,3 dias; com duas, 417,4/765,3 dias. São políticas fixas
  condicionais, não uma otimização global. A comparação controlada entre pausas usa
  o mesmo horário; a estratégia noturna de 214,8 dias é discutida separadamente.
- Figura da inclinação do teto a partir das 20 combinações já executadas, junto da
  interpretação do efeito da orientação. Não se pressupõe mecanismo construído.

Execução: `relatorio/comparar_parametros.py`. Dados, horários, balanços, hashes e
recibo em `relatorio/dados_comparacoes/`; figuras e tabela são regeneradas pelo script.
A extensão de dias parados em `simular_missao` mantém o comportamento anterior no
período padrão de um dia. O teste novo confere conservação, geração nos dias parados,
condução nula nas pausas, reservas e equivalência exata da chamada padrão.

## Alonso e Herick: desenvolvimento térmico visível

As correções e comparações de instalação dos cabos permanecem: contornos de referência,
rota protegida e cofre, bitolas 120/150/185/240 mm², modo normal e pico, transitório e
campo multidimensional. O texto explica por que uma seção que atende ao contorno
antigo deixa de atender no cofre. Não se atribui confirmação ao chicote OEM.

A bateria apresenta a curva nominal de 20/80 kW e uma figura R×entropia extraída dos
486 casos: massa de 500 kg e UA de 125/250 W/K são fixados para isolar os parâmetros
que geram calor. O asterisco identifica interrupção a 45 °C antes do SOC desejado.
O extremo iniciado a 35 °C e o requisito condicional de remoção de calor continuam
explicados após a figura. O modelo é de dois nós, sem campo espacial de células.

O circuito apresenta bomba, perfis térmicos do radiador e nova comparação de vazão
contra perdas dos componentes, além de temperatura de entrada contra UA e rendimento.
Os resultados de 31,9/26,4/23,1 L/min são discutidos no texto; o requisito de 65 °C,
a carga adicional do redutor, o NPSH e os limites térmicos aparecem em parágrafos.

Geração: `relatorio/gerar_complementos_termicos.py`; dados e hashes em
`relatorio/dados_termicos/`, incluindo a fonte do sweep de 486 casos. Não se usa uma
figura do antigo radiador a 80 °C para representar o equilíbrio de 66,8/55,1 °C.

## Verificação

299 testes locais aprovados; oito avisos de depreciação do pvlib. Ruff limpo.
Os dois verificadores numéricos/manifestos passam; malhas, contornos e limitações
físicas continuam declarados. PDF sem código e sem listas itemizadas; vídeo fora
do escopo por instrução do usuário. A existência das simulações e dos testes não
comprova fabricação, homologação ou validação física dos componentes.

PDF compilado: 41 páginas, 6.321.423 bytes (6,32 MB), 38 figuras/diagramas.
Freios na seção 3.3.1 (p. 23); cabos 3.3.2 (p. 24); cabine 3.3.3 (p. 26);
ar-condicionado 3.3.4 (p. 26); bateria 3.3.5 (p. 28); circuito 3.3.6 (p. 29).
As páginas são as impressas no rodapé; o arquivo inclui a capa antes da página 1.
