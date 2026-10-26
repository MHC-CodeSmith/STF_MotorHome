# Verificação integrada dos35itens — 26/10/2026

**35itens revisados,35em desenvolvimento,0aprovados. Projeto não concluído.**
Inventário ponto a ponto:[REVISAO_35_ITENS.md](REVISAO_35_ITENS.md).
Relatório executável:[output/verificacao_integrada_35.json](../output/verificacao_integrada_35.json).

## O que passou nos controles implementados

-158testes em6,37s;ruffsrc/scripts/tests sem erros;estrutura35itens/7equipes e
 auditoria de dependências/responsáveis sem erros.
-124artefatos da entrega e memorial comSHA256 conferidos; entradas dos estudos
 atuais compatíveis com os hashes registrados. Não foram achadas divergências
 de entradas nosJSON que possuem mapa de proveniência; arquivos sem mapa são
 identificados separadamente, não tratados como totalmente rastreáveis.
-I30/I33: balanços, referências analíticas e refinamentos próprios documentados.
 I34: carga20/80kW, SOC, duas temperaturas, limites/eventos e balanços.
 I35: curva primária da bomba +interseção com circuito assumido; perfis térmicos.
-CADportátil324volumes STEP reimportados positivos. TriagemAABB de quatro bolsas
 contra envelopes de equipamentos sem colisão; não verifica todo estrado/acesso.
-Chromium:0errosJS/0requisiçõesHTTP;23seletores,157meshesinterior,
 208elétricos+324portáteis; extensão empilhada e portátil mutuamente exclusivos.
-Memorial25páginas/2741667bytes; nova página mecânica e páginas térmicas
 renderizadas/conferidas. CachesQA`memorial-qa-07/08`,viewer`visualizador-portatil-01/qa`.

Não é validação experimental, análise estrutural completa ou certificação.
O script não infere aprovação humana, compatibilidade OEM ou conclusão física
do número de testes/arquivos. `all_35_finished` permanecefalse.

## Pendências que impedem afirmar fechamento

| Itens afetados | Dado/trabalho concreto ausente |
|---|---|
|02/03/05/12/14/18|Peças/placa da variante, óleo homologado, relação total, massas/eixos/CG, pressão e geometria montada|
|04/06/07/09/10/22/28/30/34/35|Mapas motor/pack/BMS, limites térmicos, curvas de perdas/UA/ventilador e integração elétrica real|
|08/13/16/17/18/19|Fixação dos painéis e das bolsas, acesso/ergonomia, materiais/rotas, CFD equipado com independência de malha|
|20/21/25/26/27/29|Cr do pneu adotado em condição pertinente; consumo/solar/interfaces coerentes; agenda atual com montagem/paradas/8h eSOC|
|24|Cotações completas emR$, frete/tributos aplicáveis e materiais/mão de obra; subtotalR$439é só referência pública não confirmada220V|
|31/32|Envelope térmico extraído doCAD, propriedades/ganhos e curva realHVAC; capacidade nominal deixa pouca margem no caso atual|
|Entrega final|Revisão cruzada, memorial final, seminário e vídeo com integrantes, requisitos de duração/tamanho|

O teto fixo atual não sustenta a habitação/perdas de90/95% no modelo adotado.
A alternativa portátil tem saldo positivo sob hipóteses, mas ainda não é
interfaceHV ou agenda ótima. Não reutilizar a viagem histórica como solução atual.

## Reexecutar

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -m ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py --json
.venv/bin/python scripts/verificar_entrega_integrada.py
```

Se um resultado/entrada mudar, recalcular e consolidar antes de atualizar o
manifesto. Conferir limites registrados no JSON, sem promover cenários a valores
aprovados. GlobalSHA256 preservado:
`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.
