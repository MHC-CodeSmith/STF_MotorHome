# Revisão técnica da apostila do professor

Fonte lida: Cristiano Bigonha Tibiriçá, *SEM 0571 — Apostila de Auxílio à Disciplina Sistemas Térmicos e Fluídicos*, versão 0.4, São Carlos, 2025; arquivo local `/home/mhc/Downloads/Apostila_SEM0571_Prof_Cristiano_2025.pdf` (76 páginas). As páginas abaixo são as páginas do PDF, contadas a partir da capa. Texto extraído integralmente para leitura; páginas 15, 17, 38, 39, 43, 47, 48, 50 e 75 também inspecionadas visualmente. A apostila se apresenta como apoio e remete à bibliografia original (p. 2).

SHA-256 da apostila consultada: `9b42b782ac52ec9f844de0626751f4f8cfae52195f06d4dfa4796e1e06bc1edc`.

Esta revisão registra verificações e dúvidas; não altera a apostila nem aprova parâmetros de engenharia. A fundamentação principal da disciplina deve continuar citada. Corrigir uma transcrição para implementação exige documentar a fonte e a revisão humana.

| Local | Constatação | Tratamento para implementação |
|---|---|---|
| p. 15, seção 2.2.7 | O limite impresso da correlação Churchill–Bernstein é `Re_D Pr < 0,2`. | Conferir domínio no artigo original antes de programar; não converter este limite em regra automática sem revisão. |
| p. 17, equação 23 | As duas expressões dos coeficientes estão identificadas como C1, embora a equação 22 use C1 e C2. | Conferir a referência de Zoghbi e identificar os dois coeficientes antes de usar. |
| p. 39, Tabela 4, escoamento cruzado | A expressão impressa, avaliada literalmente no caso sintético `Cr=0,5`, `NUT=1`, resulta em efetividade aproximadamente 1,0895, acima do limite físico 1. | Comparar com a bibliografia original para a configuração exata de mistura. Testar limites físicos e balanço; não copiar a expressão literalmente. |
| p. 48, equações 75–76; p. 50, exemplo 6 | A equação 76 usa a temperatura fria no nó i; o código do exemplo usa o nó seguinte. Aplicadas literalmente em conjunto, as equações 75–76 podem produzir desequilíbrio energético. | Manter convenção espacial explícita e impor conservação por elemento; conferir a derivação e a implementação com revisão humana. |
| p. 49–50, exemplo 6 | O enunciado do exemplo informa área de 1,5 m²; o código informa 4,5 m². | Não tratar os dois resultados como referentes à mesma entrada; identificar o conjunto reproduzido. |
| p. 75, Tabela 6 | A linha da água traz 100 °C na coluna de fusão; o cabeçalho de calor específico indica kJ/kg, sem kelvin, e valores como 4180 e 890. | Conferir propriedade, unidade, temperatura e fonte; não importar a tabela diretamente para parâmetros. |

## Evidência numérica independente — somente teste sintético

Nenhum número desta seção representa o motorhome. No teste das equações 75–76, adota-se apenas para verificar a álgebra: efetividade 0,1; capacidades térmicas quente/fria de 100/200 W/K; temperaturas no nó de 90/65,7 °C. A equação 75 fornece a temperatura fria seguinte de aproximadamente 64,421052632 °C. A equação 76 impressa fornece 243 W pelo lado quente, enquanto o lado frio troca aproximadamente 255,789473684 W. Usando o índice do código do exemplo da p. 50, os dois lados trocam aproximadamente 255,789473684 W. Esta verificação localiza a inconsistência de índice; não é uma validação completa do modelo de trocador.

## Comparação adicional por API

Como verificação independente de implementação, foi instalada a biblioteca `ht==1.2.0` em ambiente isolado fora do repositório. A função `ht.hx.effectiveness_from_NTU(NTU=1, Cr=0.5, subtype='crossflow, mixed Cmax')` retorna `0.541968991569`, dentro dos limites físicos, para o mesmo caso sintético da tabela. A [documentação da API](https://ht.readthedocs.io/en/latest/ht.hx.html#ht.hx.effectiveness_from_NTU) identifica explicitamente a configuração `Cmax` misturado e `Cmin` não misturado. Esta comparação apoia a investigação da inconsistência; não dispensa conferência da bibliografia física e aprovação do método adotado.

Foi também instalada `fluids==1.3.1`: `friction_factor(Re=1000, Darcy=True)` retorna `0.064`, igual a `64/Re` no caso laminar sintético. As licenças MIT de ambos os pacotes foram inspecionadas no arquivo de licença das distribuições instaladas. Nenhum dado desses ensaios foi inserido nos parâmetros do motorhome.

## Regras de uso no projeto

- Citar seção, página, hipótese e faixa de validade de cada correlação utilizada.
- Manter propriedades e geometrias do componente real separadas dos exemplos didáticos.
- Usar kelvin em radiação e documentar a área de referência de U/UA.
- Distinguir perfis unidimensionais de trocador (seção 3.4) dos campos multidimensionais obrigatórios dos itens 30 e 33 e do CFD do item 19.
- Não equiparar armazenamento de calor e energia elétrica disponível à tração sem modelo de conversão e perdas.
- Manter o PDF e suas extrações fora do Git até haver autorização para redistribuição.
