# Cabos e radiador — avanço técnico de 26/10/2026

Os itens I30/I35 avançaram com simulações reproduzíveis; continuam **parciais**.
Não foram alterados os parâmetros globais aprovados nem o circuito OEM. Os campos
calculados são condicionados às entradas abaixo, não temperaturas medidas no E-Ducato.

## I30: cabo circular com isolamento

Fonte realmente baixada e tabela p.2 inspecionada: [HUBER+SUHNER RADOX 155,
STD718404G/PIM-P8937,25/09/2026](https://www.hubersuhner.com/Asset/eyJpZGVudGlmaWVyIjoxMjkzNjUsInR5cGUiOiJhc3NldCJ9/Cw_PM-5rAg0CEAkH/H%2BS_RADOX155_FLR4GANDFLHR4G__EN.PDF).
120mm²: diâmetro máximo do feixe15,1mm; externo nominal18±0,3mm;
R20máx0,153Ω/km; massa1,147kg/m; classe1500VDC. Alternativa150mm²:
17mm/20±0,3mm/0,122Ω/km/1,434kg/m. Faixa térmica da ficha até150°C
**para3000h**, não vida útil contínua demonstrada. A variante120mm² da tabela
é preta/vermelha, sem blindagem; não foi escolhida como substituição OEM.
PDF original permanece só no cache; hash/proveniência em
[configuração](../config/cabos_tracao_proposta.yaml).

O feixe de fios não é um cilindro maciço de120mm²: sua área geométrica máxima é
maior por causa dos vazios. A fonte é distribuída sobre esse envelope de forma que
sua integral seja `I²R20[1+alpha(Tmédia_feixe−293,15)]` W/m. Isso evita criar cobre
ou perdas a partir da área externa. Hipótese de corrente espacialmente uniforme;
não se resolve redistribuição entre fios/efeitos AC, pelicular/proximidade/PWM.

Solver próprio [cabos_polares.py](../src/motorhome/cabos_polares.py): volumes finitos
em r e theta, dois materiais, periodicidade angular, fluxo central nulo e Robin
externo. Resistências logarítmicas radiais em série mantêm continuidade na interface.
Fourier/Newton da apostila pp.9–10 e geração Joule são os fundamentos. Lei linear
R(T) acoplada diretamente na matriz estacionária; não é fonte calculada com uma
temperatura final prescrita. Faces axiais adiabáticas, por metro de comprimento.
Não se adicionam radiação, contatos/terminais, conduíte, vizinhos ou percurso CAD.

Entradas **assumidas**: k_feixe200W/(mK), k_isolamento0,2W/(mK), alpha0,00393/K.
Sensibilidades k_feixe100/200/385 e k_isolamento0,15/0,20/0,30W/(mK).
Ambiente25°C oficial. h5/10/20W/(m²K) é parâmetro de filme, não vento externo.
Não há fonte de fabricante para essas condutividades; não confundir material RADOX
com polietileno genérico. Fonte elétrica é resistência máxima de catálogo, não
medição da instalação; as temperaturas altas extrapolam as propriedades.

A ficha Fiat dá205kW mecânicos de pico e400Vnominais. Com eficiência combinada
**hipotética90%**, o exemplo DC resulta569,444A. Isso **não fornece corrente RMS de
fase**. Fases300/450/600A são cenários independentes. Duração de pico e limites do
inversor/cabos reais permanecem desconhecidos.

| Estudo por condutor | h assumido | Tmax estacionária condicionada |
|---|---:|---:|
| 1×120mm²; exemplo DC569,444A | 10W/(m²K) | 178,77°C, extrapolação acima da referência da ficha |
| 1×150mm²; mesmo exemplo DC | 10W/(m²K) | 119,80°C |
| 1×150mm²; mesmo exemplo DC | 5W/(m²K) | 300,54°C, extrapolação; não atende esta triagem |
| 2×120mm² paralelos;600Atotais | 5W/(m²K) | 89,45°C por cabo, **separados e corrente igualmente dividida** |

O paralelo é alternativa para estudo, não cabo aprovado. Em DC seriam quatro cabos
(dois por polo); nas três fases seriam seis. A tabela pressupõe resfriamento
independente: agrupá-los pode invalidar o resultado. Falta confirmar compatibilidade
de terminais, repartição/proteção, EMC, flexão e integração OEM. Massa dos cabos OEM
já pertence à massa original; a proposta não foi somada novamente ao orçamento.
Não usar os casos matemáticos >150°C como previsão de material íntegro.

Campo assimétrico450A/h(theta)=10[1+0,5sen(theta)]: Tmax104,4249°C,41,26075W/m,
variação superficial5,3734K. Malhas512/2048/8192células: alteração deTmax das últimas
duas6,90e−5K; variação superficial muda0,004764K; resíduo global1,93e−8W/m.
Verificações **sintéticas separadas**: perfil radial de dois materiais semfeedback,
ordens1,84/1,86; solução harmônica realmente2D, ordens1,997/1,999. Isso verifica o
método, não mede o isolamento do produto nem valida seu desempenho OEM.

## I35: campos cruzados de refrigerante e ar

Novo [radiador_cruzado.py](../src/motorhome/radiador_cruzado.py) resolve escoamento
cruzado ideal, uma passagem, ambos fluidos não misturados, propriedades constantes.
Cada célula trocaQ com balanço igual/oposto nos dois canais. O quente avança em+x,
o frio em+y; UA distribui-se uniformemente. Temperaturas médias entre entrada/saída
fecham a troca local. Não é CFD, nem simulação de aleta/tubo real.

Base: apostila pp.31/38–39, conservação e ε-NUT. A ressalva da tabela4 continua em
[revisao_apostila.md](revisao_apostila.md); não foi copiada uma expressão com
ε>1. A integral de referência da [documentação oficial ht.hx](https://ht.readthedocs.io/en/stable/ht.hx.html#ht.hx.effectiveness_from_NTU)
foi implementada de maneira independente, sem copiar código da biblioteca. Não foi
usada a correlação aproximada com transcrição problemática que também aparece no
HTML dessa documentação. Teste compara diretamente campo discreto e integral.

**Todas as propriedades/vazões/UA a seguir são hipóteses**:
refrigerante0,5kg/s ecp3500J/(kgK), ar1kg/s ecp1006J/(kgK), UA1000W/K,
entrada quente80°C e ar25°C. Capacidade condicionada29,5679kW;
saídas médias63,1040°C/54,3916°C. Ar de saída superar refrigerante de saída
médio é possível no cruzado; cada troca local usa temperaturas dos canais que
se encontram. Não significa igualdade de carga e capacidade no circuito fechado.
Malhas16²/32²/64²: erro absoluto emε8,05e−5/2,01e−5/5,03e−6 contra integral;
ordem aproximadamente2; diferença de calor nas últimas duas0,835W; resíduo5,83e−11W.
Há27combinações deUA/vazões, **sem afirmar que sejam pontos de um mesmo radiador**.

Para205kW mecânicos e efic. combinadas85/90/95% hipotéticas, as perdas combinadas
motor+inversor são36,176/22,778/10,789kW. **Não atribuir todas ao motor.**
O caso-base não atenderia36,176kW às temperaturas assumidas; atenderia a triagem
de22,778kW com margem6,790kW, antes de bombas/ventiladores e limites reais.
Faltam mapa de perdas, separação de circuitos, composição do fluido, temperatura
permitida, curvaUA(vazões), curvasΔp e bomba/ventilador, operação e cavitação.
Não inferirUA ou perdas de pressão do bloco radiador desenhado no CAD.

Pesquisa adicional: a [Rheinmetall confirma aplicação da família CWA400 em
sistemas térmicos elétricos](https://www.rheinmetall.com/en/media/news-watch/news/2021/2021-09-08_innovative-thermal-management-for-electric-and-hybrid-drives).
Esse comunicado não fornece curva hidráulica para selecionar a bomba. Tecomotive
mostra candidatos e linksCAD, mas não foi incorporado CAD de licença não verificada
nem atribuída uma curva de variante a outra. Bomba permanece **não selecionada**.

## Reprodução e entrega

```bash
.venv/bin/python scripts/calcular_cabos_tracao.py --destino /tmp/cabos-novo
.venv/bin/python scripts/calcular_radiador_cruzado.py --destino /tmp/radiador-novo
.venv/bin/python scripts/consolidar_termica.py --cabos /tmp/cabos-novo --radiador /tmp/radiador-novo
PYTHONPATH=src .venv/bin/python -m pytest tests/test_cabos_polares.py tests/test_radiador_cruzado.py -q
```

Os destinos de cálculo precisam ser novos. JSONs guardam configuração/script/módulo
comSHA256, dataUTC e hipóteses; CSVs contêm campos/malhas/sensibilidades. Cópias nos
resultados dos itens e no pacote`entregas/parcial_2026-10-24/`. Não alterar arquivos
gerados à mão. **Revisão humana continua pendente; nenhum item foi aprovado.**
