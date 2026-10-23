# CAD atual e aderência à apostila — inspeção de 23/10/2026

**Atualização posterior na mesma data:** após a instrução do usuário para usar uma carroceria existente, o [Ducato detalhado](CARROCERIA_DE_TRABALHO.md) passou a ser a geometria de trabalho. O envelope descrito abaixo conserva o histórico da primeira inspeção; deixou de ser o CAD principal. A situação atual de todos os itens está em [revisão dos 35 itens](REVISAO_35_ITENS.md).

**Conclusão: os métodos implementados têm correspondência com a apostila, mas os itens do projeto ainda não estão integralmente atendidos.** Esta inspeção não retoma o desenvolvimento geral pausado, não escolhe veículo nem aprova componentes.

## Qual CAD está sendo usado

O arquivo gerado é `/home/mhc/motorhome_referencias_tarefas/envelope-proposta-02/envelope_PROPOSTA_mm.step`, acompanhado de STL e malha superficial MSH. É um envelope autoral simplificado, configurado em [proposta_envelope.json](../config/proposta_envelope.json), produzido por [gerar_envelope_cad.py](../scripts/gerar_envelope_cad.py). Não é CAD oficial Fiat nem uma montagem completa de motorhome.

- Dimensões nominais da configuração: comprimento 5,998 m, largura 2,050 m e topo em z=2,612 m. A face inferior está em z=0,180 m; portanto a extensão vertical efetiva do sólido é 2,432 m. O desenho anterior denomina 2,612 m como altura, mas esse valor é a cota do topo em relação ao solo.
- A frente inclinada, a altura da frente de 1,400 m e a base de 0,180 m são hipóteses autorais. As dimensões externas registradas como referência Fiat não foram novamente verificadas no fabricante nesta inspeção e não devem ser tratadas como variante selecionada.
- Faltam rodas, espelhos, portas, vidros, estrutura, materiais, interior, equipamentos e painéis. O volume do envelope não é volume habitável nem massa.
- Inspeção nova: hashes de todos os arquivos e da configuração coincidem com o manifesto; STEP reimportado via OpenCASCADE/Gmsh: um sólido; volume 28,3507538 m³. STL: 4.760 triângulos, fechado e orientação consistente. Essas verificações demonstram integridade geométrica do envelope; não demonstram fidelidade ao veículo nem aptidão física para CFD.

Prévia isométrica gerada diretamente dos triângulos do STL: `/home/mhc/motorhome_referencias_tarefas/verificacao-cad-apostila-2026-10-23/cad_current_isometric.png`. Evidência numérica: `cad_checks.json` no mesmo diretório.

O STEP Delica externo está apenas em estudo para interior: `/home/mhc/motorhome_referencias_tarefas/delica/_Delica_Assembly.step`. O registro anterior de importação mostra 68 sólidos e 790 faces, sem validação de unidades/escala ou licença de reuso. Não está integrado ao envelope nem ao produto. Nenhum novo CAD comercial foi comprado, baixado ou incorporado nesta inspeção.

## Conferência dos itens e métodos

Fontes: extração local do enunciado 2026, pp. 1–2, e apostila SEM0571 v0.4, Prof. Cristiano Bigonha Tibiriçá, 2025. Páginas abaixo são físicas do PDF. Foram consultados trechos delimitados e inspecionadas visualmente as páginas 39 e 56; não se carregaram PDFs completos no contexto.

| Item | Correspondência verificada | Situação e lacuna concreta |
|---|---|---|
| I17, CAD e vistas | Enunciado p. 1 exige geometria 3D e vistas lateral/superior/frontal com cotas principais. O envelope tem exportação 3D e figuras com dimensões. A apostila não prescreve uma marca de CAD. | Parcial. Faltam geometria representativa do veículo, layout mínimo para duas pessoas e desenho técnico com cotas adequadas. Os títulos/eixos das figuras não bastam como cotagem final. |
| I19, CFD | Enunciado p. 1 exige Cd, área frontal e simulação CFD. | Não atendido. Não há solução de escoamento, domínio fluido, camada limite, convergência ou estudo de malha CFD. Malhar a superfície não calcula Cd. |
| I30, cabos | Apostila p. 9 Eq. (1), Fourier; p. 10 Eq. (2), Newton. O solver 2D aplica fluxos conservativos e contorno convectivo. Há funções de geração Joule e resistividade linear. | Método verificado em casos sintéticos. Faltam corrente à potência máxima real, seção/material/isolação, geometria, coeficientes térmicos e acoplamento Joule dependente de T. Fonte fixa e material homogêneo do solver não representam automaticamente o cabo. |
| I31, cabine | Balanço concentrado combina convecção, armazenamento sensível (p. 74, Eq. 112) e conservação de energia. | Parcial. Faltam áreas, paredes/vidros, radiação solar/térmica, propriedades e definição do regime. Não existe ainda caso de cabine fechada ao meio-dia sem passageiros/A/C parametrizado com dados reais. |
| I32, A/C | Função separa cargas sensível/latente e eletricidade via COP; consistente com balanço de energia e abordagem de carga térmica do cap. 6. Demonstração usa exterior 33 °C e interior 25 °C. | Parcial. UA, solar, ocupantes e COP são sintéticos. Faltam propriedades, ganho pelas superfícies opacas/vidros, psicrometria e equipamento real. O balanço agregado não resolve o ciclo frigorífico da apostila. |
| I33, freios | Prescrição 30 → 10 m/s em 5 s dá remoção translacional de 400 J/kg e potência média 80 W/kg. Desaceleração média −4 m/s²; distância 100 m somente se desaceleração constante. Condução/convecção seguem cap. 2. | Não há ainda campo térmico do freio real iniciado em 25 °C. Faltam massa, disco/pastilha, partição de calor, regeneração e demais dissipações. Os 400 J/kg não foram atribuídos integralmente ao disco. A demonstração 2D genérica não satisfaz por si só I33. |
| I34, carga da bateria | Eq. (112), p. 74, apoia armazenamento sensível. Parcela I²R é contabilizada como calor, separada da potência elétrica do carregador. | Parcial. Ensaios 20/80 kW usam tensão/resistência sintéticas. Faltam protocolo CC/CV/BMS, dependência com SOC/T, calor reversível, limites e arrefecimento do pack. Não são temperaturas previstas da bateria selecionada. |
| I35, bomba/radiador | Eqs. (49–51), p. 31: balanços; Eqs. (59–62), p. 38: ε-NUT; tabela 4, p. 39: paralelo/contracorrente; Eq. (93), p. 56: interseção bomba/sistema. Fórmulas implementadas de ε são algebricamente equivalentes às impressas para os dois arranjos suportados. | Método parcial. Curvas estão em pressão diferencial [Pa]; converter de altura por Δp=ρgH usando o mesmo fluido quando necessário. Faltam perdas do motor em potência máxima, fluido, curvas reais, NPSH e modelo do radiador. Perfil paralelo não substitui radiador de fluxo cruzado. |
| I27/I29, energia | O verificador integra perdas, limita capacidade, detecta déficit intermediário e divide condução por dias de calendário. | Parcial. SOC final 0,30, distância 7.000.000 m e 28.800 s/dia são entradas configuráveis: o chamador precisa fornecer os valores do enunciado. O alvo SOC é opcional na API genérica. Não existe integração final desses requisitos nem otimizador de velocidade/tempo. A apostila não fornece um modelo pronto dessa viagem. |

As dúvidas registradas em [revisao_apostila.md](revisao_apostila.md), sobretudo fluxo cruzado e índices do perfil em contracorrente, não foram silenciosamente corrigidas nem usadas para declarar um radiador validado. O código aceita apenas os arranjos paralelo e contracorrente na função de trocador; o perfil implementado é apenas paralelo.

## Verificações reproduzidas e documentação ainda incompleta

Na worktree isolada:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m pytest -p no:cacheprovider tests/test_termica_2d.py tests/test_sistemas_termicos.py tests/test_agenda_energia.py -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/auditar_projeto.py
```

Resultado observado nesta inspeção: **38 testes passaram**; zero erros estruturais, 24 parâmetros `null` e veículo sem aprovação. Os testes verificam álgebra, conservação e convergência em casos sintéticos; não constituem validação física do motorhome.

Configuração global preservada, SHA256 `7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.

Faltam incorporar os cenários físicos, completar referências e obter revisão humana. A dívida do docstring para `docs/FRENTE_TERMICA.md` foi resolvida na continuação: a [documentação térmica](FRENTE_TERMICA.md) agora existe e relaciona equações, fontes, testes e limites. A lista dos 35 itens continua em [metadata/itens.csv](../metadata/itens.csv); nenhum item foi declarado aprovado nesta revisão.
