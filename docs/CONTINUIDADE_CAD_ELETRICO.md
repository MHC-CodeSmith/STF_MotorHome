# Retomada rápida — CAD elétrico (25/10/2026)

## Pedido ativo e estado real

Concluir o motorhome **elétrico solar**, seguindo enunciado/apostila e os 35 itens.
Último pedido: incluir e estimar no CAD **bateria de tração, motor, inversor,
componentes elétricos e A/C**, pesquisar aproveitamento típico dos espaços e
implementar. Usuário autoriza pesquisa, downloads/instalações e avanço autônomo;
push para `https://github.com/MHC-CodeSmith/STF_MotorHome.git` quando pronto.
**Essa nova etapa física ainda não foi implementada.** Não afirmar que já pesquisou
ou instalou os componentes de tração. A/C FreshWell já existe sob a cama, oculto
na vista normal; melhorar acesso visual e acrescentar dutos/instalações.

Trabalhar somente em `/home/mhc/motorhome_solar_codex_tarefas`, branch
`hub/tarefas-motorhome-com-codex`; a outra worktree pertence a outra conversa.
Último commit de implementação: `de75837`; árvore estava limpa antes desta nota.
Nenhum remote configurado/push realizado. Não publicar projeto incompleto como final.

## O que já está pronto para continuar

- Entrega: `entregas/parcial_2026-10-24/visualizador.html`, offline, carcaça Ducato
  detalhada, interior de **160 sólidos/7 equipamentos**, quatro conjuntos STEP/GLB.
  Usar controles interior/retirar carroceria/retirar cama e seletores de equipamentos.
- Base proposta: **E-Ducato MY25 L3H2 4250 kg**, motor dianteiro 205 kW/410 Nm pico,
  pack 400 V, 110 kWh bruto/98 útil/15 módulos. OEM em ordem de marcha **2790 kg**:
  pack, motor, rodas/transmissão já incluídos; **não somar de novo à massa montada**.
  Dimensões/massas internas do pack/motor e mapas ainda desconhecidos: envelopes
  estimados devem ser marcados como tais, nunca chamados de CAD OEM.
- Solar principal fixo: **1540 W**, 3×JA450 + Victron190 atual; módulos+suportes
  estimados **97,655 kg**, topo 2,745 m; geração modelada **5,50685 kWh/dia**.
  Extensão estacionada 2890 W é alternativa não validada: 171,191 kg no teto,
  largura aberta 3,564 m, geração 9,18891–10,32677 em modelos distintos de sombra.
  Limite de teto da variante exata não confirmado; não aprovar pelo anúncio Fiat200kg.
- Interior: LG CV9011WC4A 73 kg; Dometic NRX80C 20 kg; FreshWell3000 21 kg,
  628×400×286 mm, frio nominal2700 W; indução CVI1350 2300 W/50 Hz;
  Thetford365 4 kg vazio, pia/tanque autorais. Cama topo1,05 m/corredor nominal0,48 m.
  Carga de frio de duas pessoas **2645,90 W** é estimativa de caixa térmica equivalente:
  só2% de margem nominal de A/C, faltam curvas/dutos/compatibilidade elétrica.
- Serviços propostos: 2×MPPT150/35 para3SJA/48V, MPPT100/20 para190W/12V,
  MultiPlus-II48/5000 candidato. **Baterias serviços/BMS/DC-DC/EVSE ainda null**.
  Não ligar MPPT48V direto ao pack400V. Trajeto via inversor/EVSE/OBC não comprovado.
- Massa parcial com pessoas150kg/água100kg assumidos: **3255,655 kg**; faltam móveis,
  bateria serviços, inversor, cabos/tubos/ferragens/bagagem/eixos. Sem preços completos.

## Arquivos e caches essenciais

Ler `docs/EXPANSAO_SOLAR_E_INTERIOR.md`, final de `docs/ESTADO_ATUAL.md`,
`docs/REVISAO_35_ITENS.md`, `docs/ARQUITETURA_ELETRICA.md`, `docs/CABINE_E_HVAC.md`.
Regras gerais em `AGENTS.md`; ler também AGENTS de equipes envolvidas.

- Configs: `config/{layout_proposto,equipamentos_interior,servicos_proposta,
  arquitetura_eletrica_proposta,solar_proposta,cabine_proposta}.yaml`.
- CAD: `scripts/gerar_cad_instalacoes.py` (Gmsh OCC STEP/trimesh GLB),
  `src/motorhome/ocupacao.py`; coordenadas globais X frente/Z cima;
  origem carga X−3,35/Z0,68 e Ylocal0→Yglobal−0,935.
  Carroceria: `entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb`.
- Viewer: `scripts/visualizador/{scene.js,verificar.cjs}` e
  `scripts/gerar_visualizador.py`. QA atualmente exige7seletores: atualizar ao ampliá-los.
  Câmera dos componentes corrigida para lado frontal `(2,2.5,1.8)`.
- Caches fora do Git, raiz `/home/mhc/motorhome_referencias_tarefas/`:
  **instalacoes-04**, **visualizador-08/qa**, **solar-calculo-03**,
  **expansao-solar-02**, **cabine-calculo-02**, **memorial-qa-03**, **expansao-fontes**.
  `scripts/consolidar_expansao.py` contém caminhos desses caches: atualizar antes de
  reutilizar, senão sobrescreve novos artefatos com antigos.
- Memorial parcial: `output/pdf/memorial_revisao_aurora.pdf`,16páginas/1550830bytes;
  gerador `scripts/gerar_memorial_revisao.py`. Renderizar/verificar ao alterar.
  `scripts/atualizar_manifesto_entrega.py` recalcula hashes após últimas mudanças.
- Fontes locais extraídas: `/home/mhc/motorhome_referencias/textos/`;
  enunciado `Projeto Sist. Térmicos e Fluídicos 2026.txt` (~6KB), apostila consultar
  por `rg` e trechos. Não inserir PDFs/ZIP/STEP pesados no contexto.
- Ficha OEM já baixada: cache `fichas-eletricas/e-ducato-MY25-SK-20260320.pdf`;
  fontes e hashes no catálogo e docs existentes. Carcaça OpenX atribuída/licenciada.

## Próximas ações concretas

1. Pesquisar fontes primárias: ficha de resgate/bodybuilder E-Ducato para localização
   pack, motor/transaxle, inversor, OBC/DC-DC, porta de carga e arrefecimento.
   Obter dimensões reais quando públicas; registrar hipóteses para lacunas.
2. Escolher armazenamento/BMS de serviços, inversor, MPPT e DC-DC com dimensões/massas
   oficiais. Pesquisar garagem sob cama, passagem de roda, armário elétrico ventilado,
   separação da água e acesso para manutenção; implementar nos espaços disponíveis.
3. Acrescentar conjuntos paramétricos ao CAD e controles de tração/sob piso/elétrica
   ao viewer; A/C, dutos, ventilação, circuitos e acessos devem ficar identificáveis.
   Conferir rodas, solo, volumes, acesso e conservação da massa OEM; triagem AABB
   não prova colisão com carcaça/estrutura nem homologação.
4. Regerar STEP/GLB e inspecionar reimportação/volumes positivos + browser offline;
   atualizar estimativas/BOM/fontes/notas/memorial/manifestos, testar e commitar.
5. Prosseguir nas lacunas físicas: cabos/freios/bateria/motor I30/33/34/35,
   CFD equipado e missão energética; não declarar completo só por preencher o CAD.

## Verificação e limites que não podem se perder

Última verificação: **112 testes passaram**, ruff geral OK, estrutura35itens/7equipes.
Comandos na worktree:

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -m ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
```

Shell normal falha no bwrap/loopback; `exec_command` com
`sandbox_permissions=require_escalated` funcionou. Expiração de revisão automática
não significa comando executado: conferir arquivos após timeout; comandos curtos ajudam.
Node/esbuild/Playwright externos em `software/visualizador-dev/node_modules` no cache;
Chromium `/snap/bin/chromium`, usar `NODE_PATH` e `CHROMIUM_BIN` nos comandos de QA.

**26 itens parciais/9 não iniciados/0 aprovados**. Global YAML aprovado intacto,
24nulls. CFD Cd0,6530/0,6249/0,5807: mudança7,075%, sem independência/camadas/novo teto.
Agendas históricas usavam2painéis/100W estacionado: não aplicar ao novo layout.
I27 SOCfinal **exatamente30%**, sem limite8h; I29 7000km sem recarga externa,
máximo8h de condução/dia. Resultado1621,77dias é construtivo não ótimo/rota real.
I26 km/kWh na bateria. I33 30→10m/s em5s:400J/kg translacionais, não tudo no disco.
I34 carga20/80kW não equivale a calor. I35 exige bomba/radiador e curva operacional.
Entrega humana: PDF<20MB, seminário≤8min, vídeo8–10min<50MB com integrantes; não fabricar.
