# Plano de execução P1–P7 — datas provisórias até02/12/2026 às06h

O trabalho já existente deve ser reaproveitado. As datas abaixo são metas de coordenação propostas, não aceites individuais dos integrantes. O prazo final é o do projeto, no fusoAmerica/Sao_Paulo. Os35itens permanecem sem aprovação final.

|Pacote / itens|Entrada e dependência|Ação concreta e saída revisável|Critério de liberação / revisor|
|---|---|---|---|
|P1 /1,2,3,14,15,18,24,33|VarianteP4; massa/posiçãoP2/P3/P6/P7|Conferir ficha única e limites por eixo; completar BOM com massas e coordenadas; calcular CG/reação típica e máxima, transferência de água, fixações e FEA crítica; completar custos; revisar novos freios2D.|PBT/eixos/pneus identificados; inventário sem dupla água/OEM; faixas e excessos publicados; P3/P4 revisam.|
|P2 /6,7,9,23,30|CargasP6; varianteP4; instalaçãoP3|PrioridadeB01: obter requisitos OEM e fichas de equipamentoDC externo; comparar mínimo real com sérieFV. Revisar3módulos24h vs4/5para48h, inversores, MPPT compartilhado,12/24V, seccionamento e proteções. Preparar unifilar e estados/falhas do controle, sem inventar limiaresBMS.|B01 só libera com evidência do conjunto, não eficiência hipotética. I30 tem campos2D reais, mas falta circuito/terminais/proteções. P5/P7 revisam.|
|P3 /16,17,19|CotasOEM; envelopesP2/P6; massaP1|Conservar CAD existente como configuraçãoA; produzir estudo cotado da cama conversívelB e duas ocupações reais do teto. Atualizar equipamentos/fridge/banco/dutos e armazenamento portátil; extrair áreas/massas/CG. Refinar CFD aerodinâmico e preparar CFD3D térmico da cabine em conjuntoP6.|Não congelar Cd/teto/layout sem malha/contornos e cotas. Registrar discrepância de cabine equivalente versusCAD. P1/P6 revisam.|
|P4 /4,5,20,21,22,28|MassasP1;Cd/áreaP3|Manter comparação separadaSK3500/SK4250/BRnão documentada. Obter redutor e mapas OEM; usar nova varredura40/80como estimativa. Respeitar90km/h da candidata4250 e não calcular0–100atingível. Limitar regeneração conforme curvas reais quando disponíveis.|Sem mapas, publicar faixas e bloqueio de aceleração, não curvaOEM inventada. P2/P5 revisam.|
|P5 /8,25,26,27,29|P1massa/P3Cd/P4tração/P2interface/P6cargas|Reexecutar `conciliar_dec061.py` quando qualquer entrada compartilhada mudar; comparar reservas e alocações. Substituir mínimo1kW hipotético por dado real somente apósB01. Estender busca de horários e velocidade com método de otimização e orientação fixa por parada, sem chamar00–08de ótimo.|Conservação/8h/100%SOC/portátilparado sem dupla contagem. Controle sem interface separado; referência7000kmplana,ERA5/7511km em suplemento. P2/P4 revisam.|
|P6 /11,13,31,32|GeometriaP3; eletricidadeP2|Obter picos/consumo de geladeiraAC/lava-seca/boiler/HVAC compatíveis; substituir faixas por fichas sem omitir secagem. Validar rede potável e água/descarte; natural ventilação/umidade com vento0. Completar sensibilidadeI31/I32 e interfaceCFD3D,1ocupanteprincipal/2complementar.|I31fechado/semocupantes/semAC;I32externa33,interna25. Sem equipamento compatível, manter bloqueio, sem escolher teto automaticamente. P2/P3/P7 revisam.|
|P7 /10,12,34,35|PackOEM/limitesP2/P4; geometriaP3|Conferir sistema térmicoOEM e lubrificante/redutor. Preservar modelos20/80kW e ponto hidráulico, substituirR/UA/propriedades só por dados identificados; sensibilizar incertezas e integrar auxiliares do sistema correto.|Modelo conceitual não vira circuitoOEM ou proposta de alterarHV. P2/P4 revisam.|

## Marcos de integração

- **M1 — até12/11:** ficha da variante e lacunasOEM; interfaces/cargas/BOM e evidênciasB01; manter bloqueios em vez de congelar compatibilidade sem dados.
- **M2 — até20/11:** CAD comparativo, massas/eixos, CFD e modelos térmicos consistentes; reexecução da missão somente com mesma revisão. Publicar condição de viabilidade, inclusive resultados negativos.
- **M3 — até27/11:** reprodução por outro integrante, revisão cruzada dos35itens e fechamento da lista única de aprovações. Aprovação humana final é registrada por item, nunca inferida dos testes.
- **30/11:** integrar memorial, CAD, referências, anexos e roteiro; conferir limites de arquivos e aderência ao enunciado.
- **01/12:** reserva para correções e preparo do envio. **02/12 às06h:** entrega. Envio de e-mail não foi executado por este agente.

## Comandos atuais de reprodução

Executar na raiz da worktree; dependências já disponíveis nesta máquina. A versão e hashes de entradas/saídas ficam em `entregas/etapa_pos_dec061/manifesto.json`.

```bash
PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py
.venv/bin/python scripts/consolidar_pacote_dec061.py
.venv/bin/python scripts/verificar_pos_dec061.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py --json
```

`calcular_interface_carga.py`, `calcular_agenda_portatil.py`, `construir_viagem_condicionada.py` e `simular_rota_real.py` exigem `--historico`. Esse argumento autoriza reproduzir o método antigo, não o torna compatível comDEC001B. Para reprodução exata de artefatos antigos, usar a revisãoGit indicada no registro de cenários. Não atualizar hashes históricos para fazê-los parecer atuais.
