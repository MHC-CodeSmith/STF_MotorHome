# Retomada técnica — 10/11/2026

**Objetivo aberto:** executar os 35 itens sob DEC-001–061 até o limite técnico demonstrável. O usuário pediu continuar até o fim, com escolhas provisórias autônomas; não devolver apenas planos, pedir aprovações individuais ou preparar relatório/slides. **35 revisados, zero aprovações humanas; etapa integral não concluída.**

## Workspace e leitura

- Exclusivo: `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`. Não editar a outra worktree `/home/mhc/motorhome_solar_codex`.
- HEAD técnico e `main` publicados antes desta nota: **`aae15ff6810777528b2dc82163b603e4318c9e34`**; anterior **`6656858`** (GX/proteções/CFD), **`91be8af`** (despacho I25/água). Árvore estava limpa. Base solicitada `29defc4`; não voltar a ela. Push `git push origin HEAD:main` já autorizado; remoto `git@github.com:MHC-CodeSmith/STF_MotorHome.git`.
- Ler `AGENTS.md`, fim de **`docs/EXECUCAO_TECNICA02.md`**, **`docs/REVISAO_TECNICA_EXECUCAO02.md`** (estado individual dos 35), **`docs/PROTECOES_SERVICOS_MODELO.md`**. Lista única de escolhas finais: `docs/APROVACOES_FINAIS_PENDENTES.md` (A01–A16).
- Fonte única: **`config/parametros_globais.yaml`**, revisão `1.1.0-execucao02`; metadados por parâmetro e hipóteses novas em `development`. Resultados ativos: **`entregas/desenvolvimento_2026-11-09/`**. Datas anteriores no nome não tornam os resultados atuais históricos.

## Invariantes

Arquitetura B por interface **externa DC OEM autorizada**, ainda não demonstrada; nenhum acesso/modificação HV/BMS/cabos, nem transferência armazenada entre tração/serviços. Antiga via serviços48V→inversor/EVSE/OBC descartada. Buffer somente comparação, não instalado. Meta1540Wp fixos+1600Wp portáteis só parados/ângulos fixos; modelos creditam **1350Wp fixos**, pois190W→48V não demonstrado. MPPT compartilhado não validado. Serviços48V/220V60Hz; ventilação natural, A/C sob banco, indicadores comerciais.

I29:7000km plano, velocidades constantes de cenário, ambas SOC100%,≤8h/dia,sem carga elétrica externa; dia São Carlos21junho/céu limpo/25°C/UR50/vento0 repetido. Reservas10/20×20/30. I27 separado100/80→30%,sem importar limite8h. Água100/70/cassete~20L,sem duplicação;2×80kg+60kg bagagem. Entrega02/12/2026 às06h America/Sao_Paulo.

Registro61 original intocado: SHA256 **`1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`**. Não alterar decisões nem atualizar hashes de manifestos históricos para esconder mudanças.

## Estado numérico vigente

|Frente|Resultado e limite|
|---|---|
|OEM|Estudo Fiat SK MY25 **505.GG1.2**,4250PBT/2790tara,110/98kWh,400V,205kW/410Nm pico,90km/h,50990EUR semIVA. Mesma variante; eixos/mapas/pressões/óleo/suspensão não obtidos. 0–100 não alcançável.|
|CAD/massa|LayoutA provisório,**3974.02552776kg**,margem275.97447224kg;CGx2.018029021/y.002237209/z.928796684m;eixos1986.491737/1987.533791kg. CGbase/posições estimados,limites por eixo desconhecidos. A sem colisõesAABB;B ainda falha acesso/orientação.|
|Serviços/inversor|**3US5000=14.4kWh/119.1kg**,7.2288254kWh/dia estimados. **MultiPlus-II GX48/5000/70-50,PMP482506000**,31kg565×323×148mm,18Wvazio;220V60Hz configuráveis. GX/visor/BMS-CAN incorporados,sem central própria/gateway externo. CANtipoA/DVCC/firmwares/atuadores não ensaiados;SOC de shedding continua null.|
|I25/I29|I25:630MILP/30–15–5min,crédito solar inicial0;1kW DC hipotético:40/80km/h **48.06652/26.64640km** sótração,**24.15936/13.39311km** com serviços cíclicos;3kW não inicia. GradeI29 **1008** reexecutada:700Waux/20kmh/20–04h **290.875/292.8854167dias**. Não ótimo global ou missão física.|
|Proteções/fixações|324DC/144faltas/256simultaneidades/6históricos de falha/648fixações. JLLN200/080 candidatos125VDC20kA;**56faltas hipotéticas excedem20kA**. I²t/impedância/ampacidade não demonstrados. 10casos de chapa excedem esmagamento;apoiosOEM/fadiga/prying fora do modelo.|
|Rotas/água|STEP/GLB em `rotas_instalacoes/`;laço48V estimado1.783946m,70mm²:5.8636W a4kW/43.5V/90°C. Terminais/passagens reais não confirmados. **9572eventos hídricos/8replays**,sequenciais,só parados,erro≤9.1e−13L;postos/tempos hipotéticos.|
|HVAC|Manual **FW3000-O16s12/12/2018**,p29 visualmente conferida:220–240V50/60Hz,2700Wtérmicos,6.2Anominais60Hz,21kg. **72térmicos+12elétricos**;margens1/2p184.102/54.102W. SKU/placa/curva33°C/partida não confirmados;manual indica5A versus6.2A,coordenação aberta. Triagem agora1364VA,pf1estimado;3kWh/d mantém hipótese. Não misturar4.3A de outra revisão ou HTML6675 com1758/2700W conflitantes.|
|CFD|Cabine3D PIMPLE300s:3malhas+passo,50.3203°Cmédia/53.0744máx;erro energético≤.0482%,nãoCHT/geometriaOEM. **Novas camadas aero rejeitadas**:29527/63668retêm0;fina178298(+12086)diverge−8,GAMG e retryPCG/DIC. Não usarCd4e24. Logs/malhas/campos≈99MB em `aero_camadas/`;faixaCd anterior não validada mantida.|
|BOM|26linhas em `bom_atual/`;lista oficial2026Q2 semVAT:GX1093USD+150/60-Tr393USD=1486USD;50990EUR veículo e439BRL cooktop histórico **separados**. InstaladaBRLnull. MPPT3kg já na reserva15kg,não duplicar.|

## Reprodução e cuidados

**Última QA: PASSOU,227testes,Ruff,403controles,154entradas/922saídas hashadas;estrutura35/7 e auditoria sem erros.** Nenhum processo científico pendente. Nesta condensação não foram reexecutadas simulações.

```bash
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
```

Após mudanças físicas deliberadas,seguir dependências/comandos no fim de `EXECUCAO_TECNICA02.md`,e só então gerar novo manifesto com `--registrar`;conferência normal sem essa opção. Não repetir grade1008/CFD por mudança documental. Scripts novos principais: `desenvolver_despacho_i25.py`, `desenvolver_protecoes_fixacoes.py`, `detalhar_rotas_cad.py`, `comparar_hvac_revisoes.py`, `consolidar_bom_atual.py`, `detalhar_paradas_hidricas.py`. Os16perfis3973kg foram retirados do ativo apósGX;bytes noGit91be8af e lista emoutput. Não misturar novamente.

`conciliar_dec061.py` recusa revisão1.1;executores antigos de elétrica/rota exigem `--historico`. `config/hidraulica_proposta.yaml` é arrefecimento,glicol,não água potável. Não rodar consolidadores antigos sobre a listaA01–A16.

## Retomar sem refazer trabalho

Avançar pendências executáveis da revisão35:geometria/CHT/CFD equipado com nova estratégia de malha,fixações/chaparia e drenagem reais,coordenação I²t/curto/PE-DR/atuadores e confirmação documental OEM/HVAC. Não repetir indefinidamente pesquisa da interfaceDC já delimitada;manter controle sem interface e estudos condicionais. Dados proprietários ausentes não autorizam inventar curvas/homologação. Nenhum componente foi comprado/instalado,nenhum ensaio físico ou contato com terceiros realizado.

Ambiente: shell em geral requer `sandbox_permissions=require_escalated` por falha bwrap;sem rejeição de aprovação pendente. OpenFOAM2412 patch260127 em `/home/mhc/motorhome_referencias_tarefas/software/openfoam2412-local/usr/lib/openfoam/openfoam2412`. Antes de malha grande conferirRAM:último~2.5GBdisponível/swap7.3GBusado. CFD exige destinos novos,preservar tentativas. Web funcional via `mcp__codex_apps__search_service_web_run`;sem BrightData disponível. Downloads podem403. ManualHVAC espelho8MB/hash acima em `/home/mhc/motorhome_referencias_tarefas/freshwell-conferencia-20261110/`;SHA256 **`12246bf2a261161a4b1778780fa59a8ba06edda53ba8670765d1b96f6265680b`**. Não alegar acesso aoPDF primário76MB que falhou.

Histórico anterior completo: [RETOMADA_HISTORICO_ATE_2026-11-10.md](RETOMADA_HISTORICO_ATE_2026-11-10.md). Prevalecem os números e instruções desta nota.
