# Item 17 — CAD 3D e vistas cotadas

## Resultado vigente

O exterior equipado do cenário `maxeon1540_independente` mede 5,981 m de comprimento, 2,079 m de largura na carroceria (2,491 m com espelhos), 2,608 m de altura no teto e 2,688 m com o deck. As vistas lateral, superior e frontal e a perspectiva constam da Figura 9 do [memorial](../../../relatorio/relatorio.pdf).

A Figura 10 usa o layout A da [configuração executada](../../../entregas/integrado_maxeon1540/parametros_resolvidos.json) e os ajustes da [montagem detalhada](../../../relatorio/montagem_cad.py). Os três módulos US5000 foram elevados em 0,320 m para liberar a caixa de roda esquerda. O piso acabado está a 0,680 m do solo. A base do primeiro módulo está a 1,040 m e o topo do terceiro a 1,543 m do solo, ou 0,863 m acima do piso. A geometria das caixas de roda é estimada.

Para gerar a figura a partir da raiz do projeto:

```sh
python -c "from relatorio.gerar_figuras import vistas_layout; vistas_layout()"
```

As notas a seguir documentam etapas anteriores. A validação da geometria de fabricação depende da conferência da carroceria específica.

**Responsável:** P3 — Carroceria, CAD e CFD  
**Enunciado / tarefa:** Geometria 3D; vistas frontal, superior e lateral cotadas; área de teto, área frontal e volume.  
**Depende de:** I15 (P1), I16 (P3), I13 (P6)  
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

## Cobertura e integração interior - 25/10/2026

[CAD, fontes, modelos de sombra, equipamentos e orçamento de massa](../../../docs/EXPANSAO_SOLAR_E_INTERIOR.md). Não promove as propostas a engenharia aprovada.

<!-- execucao-integrada:inicio -->
Execução vigente: fonte única `config/parametros_globais.yaml`,cenário `maxeon1540_independente` e índice local `resultados/execucao_integrada.json`. Referências antigas às propostas elétricas permanecem históricas e não autorizam arquitetura48V→OBC,modificaçãoHV ou aprovação final. Critérios/revisão computacional e bloqueios atuais constam em `docs/REVISAO_TECNICA_EXECUCAO02.md`.
<!-- execucao-integrada:fim -->
