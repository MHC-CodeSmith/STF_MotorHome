# Item 33 — Freio: campo térmico multidimensional

**Responsável:** P1 — Estrutura, freios, massa e custos  
**Enunciado / tarefa:** Frenagem de 30m/s para 10m/s em 5s, 25°C inicial; calcular energia e campo térmico 2D/3D.  
**Depende de:** I03 (P1), I18 (P1), I28 (P4)  
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

## Alerta de auditoria — 22/10/2026
A aresta I28→I33 foi preservada para revisão P1/P4: a frenagem prescrita no enunciado p. 2 (30→10 m/s em 5 s) permite iniciar o método sem esperar o resultado 0–100. Possível sobre-restrição de integração, não requisito adicional do docente.
