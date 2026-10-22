# Item 27 — Autonomia diária com SOC final 30%

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Determinar autonomia máxima diária, perfil v(t), Pmotor(t) e SOC final alvo de 30%, com tolerância numérica do solver a declarar e justificar.
**Depende de:** I23 (P2), I25 (P5), I26 (P5)  
**Status:** Não iniciado (estrutura criada automaticamente).

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

## Proveniência da correção — 22/10/2026
Enunciado original, p. 2, item 27: carga final de 30% da carga máxima. O antigo `>=30%` ampliava o cenário; foi corrigido para alvo de 30%, sem definir tolerância nem SOC inicial. O YAML preserva o nome histórico `minimum_soc_fraction_daily`; esta auditoria não o altera nem aprova outra interpretação.
