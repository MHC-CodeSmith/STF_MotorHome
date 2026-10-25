# Item 25 — Autonomia usando somente solar

**Responsável:** P5 — Solar, autonomia e viagem  
**Enunciado / tarefa:** Calcular geração de 21/06 céu limpo em São Carlos e distância solar a 40/80km/h; curva versus velocidade.  
**Depende de:** I08 (P5), I09 (P2), I22 (P4), I23 (P2), I26 (P5)  
**Status:** Em desenvolvimento — curvas de sensibilidade condicionadas, não aprovadas.

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

## Integração energética e otimização

Métodos, equações, hipóteses e resultados rastreáveis em [ENERGIA_E_OTIMIZACAO.md](../../../docs/ENERGIA_E_OTIMIZACAO.md). Resultados são condicionados; não substituem dados reais nem aprovação. A limitação de oito horas diárias é aplicada a I29, não a I27.
