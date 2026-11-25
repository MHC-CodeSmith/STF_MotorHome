# Item 19 — Coeficiente de arrasto e CFD

<!-- revisao-final:inicio -->
**Resultado conferido com os arquivos do commit `5144702`.** Para o motorhome com o deck fotovoltaico, o coeficiente de arrasto da malha fina é **0,621536**, com **4,827840 m²** como área de referência de `forceCoeffs`. Esse valor de área corresponde à projeção frontal da carroceria, inclusive espelhos. A silhueta equipada, obtida pela união das projeções dos triângulos da carroceria e do deck no plano YZ, mede **4,895440 m²**. As forças de ambas as superfícies já entram no cálculo do coeficiente. A área de arrasto é **3,000678 m²**. O coeficiente equivalente normalizado pela silhueta equipada é **0,612954**. O par original dos modelos de energia continua sendo Cd nominal **0,62487678** e área **4,827840 m²**.

| Malha | Células | Iterações SIMPLE | Cd no último passo | Variação relativa de Cd nas últimas 50 iterações |
|---|---:|---:|---:|---:|
| Grossa | 291.219 | 298 | 0,621971 | 0,00275% |
| Intermediária | 522.986 | 335 | 0,633751 | 0,01790% |
| Fina | 750.513 | 344 | 0,621536 | 0,01390% |

O intervalo **0,621536–0,633751** reúne os três valores finais. A razão entre as diferenças sucessivas é −1,037. A sequência oscila, com razão de refinamento efetiva de 1,128 entre a fina e a intermediária e de 1,216 entre a intermediária e a grossa. Esses três valores permitem descrever a variação observada. A incerteza de discretização e a validação experimental permanecem em aberto.

Na carroceria da malha fina, o y⁺ varia de **5,88 a 1.321,68**, com média **304,60**. No deck, varia de **98,63 a 792,91**, com média **315,79**. Os extremos e as médias são os de cada superfície no passo final de SIMPLE. O estudo usa solo móvel, rodas paradas e modelo de turbulência k–ω SST.

**Reprodução do pós-processamento.** A partir da raiz do projeto, executar `python scripts/calcular_gci_aero.py` com NumPy, Matplotlib e PyYAML instalados. A execução lê a contagem de células e o critério de convergência dos logs, o Cd de `postProcessing/forces1/0/coefficient.dat`, o y⁺ de `postProcessing/yPlus/0/yPlus.dat` e a área de referência do `system/controlDict` de cada malha. Ela gera o resumo JSON, o gráfico e as macros do relatório. Para reproduzir o escoamento, o executor original requer OpenFOAM 2412 e o caso-base externo `cfd-aurora-refino-semcamadas-02`. O ZIP contém o histórico e as configurações utilizados para a conferência.

[Resultados das três malhas](../../../entregas/aero_equipado1540/familia_gci/resumo_gci.json) · [Executor do CFD](../../../scripts/executar_aero_malha_adicional.py) · [Pós-processamento](../../../scripts/calcular_gci_aero.py) · [Geometria CFD de referência](../../../entregas/aero_equipado1540/malha_adicional_1/case/constant/triSurface) · [Relatório](../../../relatorio/relatorio.pdf)

As notas de desenvolvimento a seguir documentam as etapas anteriores.
<!-- revisao-final:fim -->

**Responsável:** P3 — Carroceria, CAD e CFD  
**Enunciado / tarefa:** Simular CFD; obter Cd, área frontal; documentar malha, domínio, solver, contornos e convergência.  
**Depende de:** I17 (P3)  
**Status:** Em desenvolvimento — artefatos parciais; revisão humana pendente.

## Entrega mínima
- `teoria.md`: fenômeno físico, equações, hipóteses e faixa de validade.
- `fontes.md`: referências completas, URL, página/tabela, fabricante e data de acesso.
- `dados/`: entradas com unidades e proveniência; dados desconhecidos continuam como pendentes.
- `codigo/`: notebooks ou scripts com comando exato para executar.
- `resultados/`: tabelas, figuras e logs gerados pelo código. Não inserir resultados fictícios.
- `validacao.md`: testes, revisão humana, limitações, e links para PRs.
- `externos/`: registro dos arquivos de terceiros incorporados legalmente.

## Interface
Entradas oficiais em `config/parametros_globais.yaml`; cada atualização relevante requer registro em `docs/decisoes.md` e deve avisar itens dependentes.

## Aceite
O item só vira **aprovado** quando tiver resultados reproduzíveis, referências e uma revisão por outro integrante.

## Revisão desta frente — 23/10/2026

Consulte a [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md). A [carroceria detalhada](../../../docs/CARROCERIA_DE_TRABALHO.md) substitui o bloco como geometria de trabalho. Não há CFD concluído.

## Execução de 24/10/2026

Progresso e limites atualizados em [geometria, CFD, solar e otimização](../../../docs/AVANCO_2026-10-24.md). Artefatos de revisão em [entrega parcial](../../../entregas/parcial_2026-10-24/README.md); não há aprovação final de engenharia.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1560_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
