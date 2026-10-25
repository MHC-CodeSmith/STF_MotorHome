# Retomada rápida — 25/10/2026

Missão: concluir os35itens do motorhome **elétrico solar**, seguindo enunciado e
apostila, com carroceria detalhada. Usuário autoriza pesquisa/download/instalação
e avanço autônomo. Não repetir credenciais do chat. Não declarar projeto concluído.

- Worktree **`/home/mhc/motorhome_solar_codex_tarefas`**, branch
  **`hub/tarefas-motorhome-com-codex`**. Outra conversa escreve
  `/home/mhc/motorhome_solar_codex`: **não editar**. Push autorizado pelo usuário
  para `https://github.com/MHC-CodeSmith/STF_MotorHome.git` **quando o projeto estiver pronto**.
  Usar a branch desta frente; não houve push. Autorização persiste, sem nova confirmação.
  Merge não solicitado. Ainda não há remoto Git configurado; evitar mudar configuração
  compartilhada com a outra worktree só para registrar este destino.
- Base1a4a750; commits anteriores c088758 e449e482. Continuação atual inclui
  layout, CFD2412, energia, otimizador de menor tempo e visualizador; consultar
  `git log -1` para o checkpoint mais recente, sem reexecutar dados já gerados.
- [Artefatos portáveis](../entregas/parcial_2026-10-24/README.md), inclusive
  `visualizador.html`: funciona offline, carroceria detalhada de5,998m adaptada
  do Ducato OpenX. Não é CAD OEM nem editor paramétrico. Fontes/licenças preservadas.
- Proposta BEV **Aurora Solar / E-Ducato MY25 L3H2 4250kg**, motor205kW/410Nm,
  bateria110brutos/98úteis kWh/400V, conforme ficha OEM já conferida. Não somar
  bateria/motor de novo à massa OEM2790kg. Mapas/perdas/integração solar-HV ausentes.
- **112 testes passaram**; ruff dos scripts novos/alterados passou. Status
  **26 parciais /9 não iniciados /0 aprovados**. YAML global intacto,24nulls,
  SHA256`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.

## Evidências que não repetir

Cache **`/home/mhc/motorhome_referencias_tarefas`**, sem anexar PDFs/ZIP/CAD ao contexto.

| Área | Evidência atual |
|---|---|
| Geometria | `aurora-L3H2-01/`:5,998m/WB4,035m/topo2,612m; área aberta5,004665m². `aurora-cfd-superficie-02/`:10444triângulos fechados por componente, pneus preservados, área4,827840m²; ainda forma não validada |
| CFD | `comparacao-cfd-01/`:29527/63668/166212células,108/187/179iterações, Cd0,65303585/0,62487678/0,58066680. Última mudança7,07%: **sem independência de malha**. Sem camadas/y+ e rodas girantes. Casoscomcamadas `cfd-aurora-refino-01/02` divergem: **rejeitados** |
| Software CFD | OpenFOAM2412patch260127 em`software/openfoam2412-local/usr/lib/openfoam/openfoam2412`; pacotes SHA verificados. Wrapper`executar_openfoam.py` valida MeshOK e convergência, não sóexit0. v1912 falha SHA1/forceCoeffs; não repetir diagnóstico. Último solver terminou, forças pós-processadas comexit0; wrapper externo havia retornado143, não ocultar isso ao auditar logs |
| Solar | `solar-calculo-02/`:INMET A711−21,98027777/−47,88388888/859,29m; JA Solar450W/22kg/1,762×1,134m. Dois/três módulos3,2325/4,8488kWh/dia após perdas assumidas. pvlib0.16.1, ano2026,21/06,25°C,0vento. `solar-calculo-01` tem erro temporal já corrigido, descartar |
| Layout | `layout-02/`, configlayout0.2: banheiro inicial0,90×0,82×1,90m interferia no teto. Reserva atual0,90×0,76×1,80m;81raios,folga amostral externa mínima33mm. Não resolve isolamento/ergonomia/caixas de roda. PisoZ0,68/traseiraX−3,35m são **alinhamento assumido**. `triagem-banho-01/` |
| Energia | `energia-sensibilidade-02/`:324cenários,Cr/eta/cargas assumidos;40km/h3,25–5,78km/kWh,80km/h1,97–3,03. Dois módulos solar-only10,5–18,7km@40 e6,4–9,8@80. Não são resultados validados |
| I27 | `agendas-condicionadas-03/`:335kmótimo na grade30min/modos, SOC100→30%**exato**, dia completo. **300km anteriores aplicavam indevidamente8h a I27**, superados. Gráfico é potência terminal, não mecânica de motor |
| I29 | `otimizacao_viagem.py`:MILP menor tempo, distância exata, chegada fracionária, energia causal/8hporcalendário;6testes analíticos. Caso100km4500s. `viagem-condicionada-01/`:agenda construtiva7000km,1621,77dias/1622datas,SOCfinal12,94%,8hmax,resíduo−0,00186J,verificador independente. **Não ótimo**, repete sol21/06/SãoCarlos todo dia/ano; não previsão da rota. CSV~78000intervalos só emcache;hash noresumo. Limite inferior otimista171dias, não certificado do ótimo físico |

## Próximo trabalho real

1. Ler [revisão35itens](REVISAO_35_ITENS.md), [energia/métodos](ENERGIA_E_OTIMIZACAO.md),
   [CAD/pesquisa online](CAD_ONLINE_E_VISUALIZACAO.md). Notas antigas de RETOMADA são históricas.
2. Resolver cadeia solar→armazenamento serviços→carga OEM estacionado e orçamento
   de equipamentos; nunca ligar MPPT48V diretamente ao pack400V. Carga simultânea
   à tração não foi comprovada; cenários atuais desabilitam solar em movimento.
3. Obter pneus/Cr, freios, transmissão/mapas de motor, pack/BMS/perdas, massas/BOM,
   equipamentos/HVAC e custos; fechar I02/03/05/07/09–14/18/20/24/28 com fontes reais.
4. CFD: resolver camadas/y+, rodas, geometria e independência antes de Cd final.
   Térmica I30–35 ainda tem métodos verificados, **não componentes reais resolvidos**.
5. Otimizar missão física7000km depois de resolver consumo/geração/integração;
   refinamento de grade e modelo de acelerações necessários. Não chamar heurística de ótimo.
6. Memorial de revisão **parcial** gerado em `output/pdf/memorial_revisao_aurora.pdf`:13páginas/1045274bytes, todas renderizadas em `memorial-qa-02/`. Não é relatório final. Seminário8min e vídeo8–10min<50MB seguem pendentes; vídeo exige integrantes. Nenhum envio aos docentes.

Ambiente: `.venv` própria herda sistema; **NumPy1.26.4** evita quebra binária;
Gmsh4.15.2,MeshFix0.18.1--no-deps,VTK9.1,pvlib0.16.1,h5py3.16.0.
Shell comum falha bwrap/loopback; `sandbox_permissions=require_escalated` funciona.
Uma revisão automática expirou na cópia final; repetição curta autorizada funcionou,
sem bloqueio atual. Nenhum solver/download/servidor deve ficar rodando ao encerrar;
consultar sessões antes de afirmar isso.

## Continuação de 25/10 - não repetir pesquisa nem simulações

- `config/cabine_proposta.yaml`, `src/motorhome/cabine.py`, `scripts/calcular_cabine.py`,
  `tests/test_cabine.py` (9 novos testes analíticos), `docs/CABINE_E_HVAC.md`.
  Último resultado **cabine-calculo-02/**:I31 49,079°C ao meio-dia/pico49,597°C14:07;
  I32 2515,90/2645,90W de frio para1/2pessoas;UA65,4366W/K/C200kJ/K assumido.
  48cenários,passo1/5min diferença0,00081K/resíduo6,03e-9J. Caixa equivalente com
  extensão dianteira1,10m, vidro/filmes/massas térmicas assumidos: não CAD validado.
  **cabine-calculo-01** substituído só pelo eixo gráfico24:00; não usar figura antiga.
- Armacell AF oficial consultado via web; k(T)=(33+0,1T+0,0008T²)/1000, chapas≤32mm;
  k40=0,03828W/mK. Download403, não inventar hash. Dometic FJX4 catálogo2,2kW abaixo
  da carga nominal estimada; FJX7 oficial3kW candidato, sem curvas/COP/instalação.
  Cache `conforto-fontes/`: HTMLFJX4 e manualAPAC4MB; manual NÃO fichaEMEA.
  Buck CR-2 dezembro2009p20, psicrometria EF=1 aproximado.
- `docs/PNEUS_E_MASSA.md`: Continental artigo04514690000 225/75R16C121R,
  29,3in=0,74422m/37,3lb=16,919kg/709rev-milha→raio0,361262m/90psi MÁXIMOS,
  **pressão operacional ausente**, não substituirCAD sem revisar6,18%diâmetro maior.
  Fonte primary HTML cache `pneus-fontes/continental-vancontact-as.html`, hash catalogado.
- Reserva de carga1460kgOEM;1166kg após44kgPV+150kgpessoas+100kgágua assumidos;
  não massa montada/BOM. Não duplicar pack/motor/rodas OEM.
- PDF por `scripts/gerar_memorial_revisao.py`, usa JSON/figuras da entrega e matriz35.
  ReportLab/fontsDejaVu do sistema; fonte fonte1,045MB, não adiciona PDFs brutos.
  `scripts/atualizar_manifesto_entrega.py` recalcula todos os hashes + PDF externo.
  Documentação/interfaces D005 e `docs/INTERFACES_2026-10-25.md` atualizadas.
- **105passed** com `PYTHONPATH=src .venv/bin/python -m pytest -q`. Sem PYTHONPATH,
  pytest falha import motorhome; não é defeito físico do módulo. Ruff usa `python -m ruff`.
- Próximo avanço físico: equipamentos/BOM e solar-serviços-cargaOEM; medir cabine/vidros
  e instalarHVAC noCAD; obter mapas/pack/transmissão/freios/cabos/bomba/radiador,
  executar I30/33/34/35 reais e corrigirCFD. PerfilHVAC ainda NÃO integrado às agendas.

## Prioridade de retomada - ampliação solar e interior (último avanço)

- Usuário pediu aproveitar teto e equipar interior; executado `layout-0.3` + `interior-0.1`.
  Ler primeiro **docs/EXPANSAO_SOLAR_E_INTERIOR.md**; dados e CAD não são homologação.
- **Proposta principal fixa1540W**:3JA450 + Victron190SPM041903903 (ficha de modelos
  atuais,175W antigo era descontinuado).76,5kg módulos +21,155kg suporteCAD a2700kg/m³
  =97,655kg antes ferragens; altura2,745m. QuartoJA grande não cabe no retângulo cargo.
- Alternativa estacionada2890W: +3JA móveis, sete módulos142,5kg+28,691kg suportes
  =171,191kg recolhidos. Excede referência150kg; FiatUK200kg/50kg-barra dependem da
  configuração, **variante elétrica exata não confirmada**. Não aprovar por171<200.
  Recolhida,3JA inferiores sombreados; produtivos só3JA superiores+190W. Largura
  aberta3,564m/altura recolhida2,805m. Apoios tubulares telescópicos guardados sob cama.
- `instalacoes-04/`: quatro STEP/GLB, interior160sólidos e cobertura fixa/empilhada/aberta.
  Três casos anteriores foram reimportados:160/239/311sólidos positivos, `instalacoes-03/qa_step.json`.
  Apoios nascem de raios verticais contra malha externa; não pontos OEM/estrutura validada.
  Cabeceira/colchão: estrado1,95x1,35, colchãoCAD1,91x1,31m, topo1,05m; lava-seca abaixo.
- `visualizador-08/qa`:7seletores/160meshes/readytrue/errors[]/HTTPrequests[].
  Último teste também seleciona geladeira e depois lava-seca; câmera corrigida para
  frente do equipamento. `visualizador-04..07` históricos. Cópia vigente na entrega.
- `solar-calculo-03/`:JA2/3/6 =3,2325/4,8488/9,6975kWh/dia, ainda sem190W.
  `expansao-solar-02/`:inclui190W → fixa5,50685; aberta semsombra10,3556,
  sombra direta geométrica10,3268; string inferior desligada ao sombrear9,18891kWh/dia.
  Modelo de área sombreada não simula diodos/mismatch/difusa; orientaçãoXnorte/Yleste
  assumida, não faixa garantida. **Não energia comprovada na tração**.
- Habitação assumida sem secagem5,42651kWh/dia → saldo fixo0,08034; aberta3,7624..4,9003.
  Energia secagem ausente; lavagemLG0,29kWh frio/68,8L, não ciclo completo lavado/seco.
- Equipamentos selecionados como candidatos:LGCV9011WC4A73kg (total620mm, não565;
  aberta1100),NRX80C20kg12/24V55Wnom,FreshWell3000 21kg628x400x286/2700Wfrio,
  CVI1350 2300W350x350x55 versão50Hz (compatibilizar frequência),Thetford3654kgvazio,
  pia/tanque100Lautorais. HVAC nominal só2%acima de carga2pessoas estimada: não definitivo.
- `config/servicos_proposta.yaml`:2MPPT150/35 para3SJA/48V +100/20 para190W/12V;
  MultiPlus-II48/5000 candidato. Armazenamentos/BMS/DC-DC/EVSE/proteções ainda null.
- BOMparcial:118kg equipamentos conhecidos; OEM+equip+pessoas150+água100+fixa97,655
  =3255,655kg; faltam móveis, baterias, inversor, ferragens/cabos/tubos/bagagem/eixos.
- Scripts:gerar_cad_instalacoes/calcular_expansao_solar/consolidar_expansao;
  módulosocupacao/sombra com7testes novos. **112passed**,ruff geral passou.
- Cachefontes `expansao-fontes/`:fichasVictron/FreshWellp13/CVIp18 baixadas+hash;
  LG/Fiat download403 mas páginas lidas viaweb. Não carregar12MB dePDFs no contexto.
- Memorial atualizado16páginas/1550830bytes; conferir última QAem`memorial-qa-03/`.
  Manifesto da entrega deve ser recalculado após últimas alterações. Não fezpush,
  projeto continua incompleto; autorização de envio final ao GitHub permanece válida.
- Próximo: fechar montagem de teto/estrutura, storage/DC-DC/EVSE/frequências, custos,
  perfil de habitação comsecagem; medir envelope térmico real; mapas e simulações
  físicas I30/33/34/35; CFD da carroceria equipada e missão física7000km. Não reusar
  Cd/agendas históricos de2painéis/100W estacionado como configuração ampliada atual.

## Mais recente — tração, elétrica e compatibilização da indução

- Ler `docs/CAD_TRACAO_E_SERVICOS.md`. Integração geométrica: pack110kWh com15módulos
 ilustrativos, motor/redutor, inversor/OBC/radiador dianteiros; **cotas estimadas, não OEM**.
- `config/instalacoes_eletricas_proposta.yaml`, `scripts/gerar_cad_eletrico.py`:
 208sólidos STEP reimportados positivos. Cache `cad-eletrico-02/`.
- Serviços:2NG51,2V100Ah paralelo10,24kWh/200Ah/74kg publicados estimados,
 LynxBMSNG500A,MultiPlus-II48/5000,MPPTs,Orion48/12-30 eAGM22Ah12V;
 gabinete metálico lateral e gaveta autoral sob cama. Circuitos/proteções/ventilação
 e fixação ainda não aprovados. Não somar trem de força de novo à massaOEM2790kg.
- Indução substituída por **IE3TP220V60Hz2000W**,280x358x62mm/2,3kg, portátil em
 bancada contínua; manual2025p17 conferido visualmente. Loja mistura1500W genéricos
 com220V: seguir manual da variante. `interior-0.2`,cache`instalacoes-05/`,157sólidos.
- `visualizador-eletrico-03/qa`:23seletores,157meshes interior+208elétrica,
 erros[]/HTTPrequests[]; vista técnica retira corpo/interior/teto, HVAC isolável.
 Copiado na entrega com STEP/GLB e novas figuras.
- `integracao-eletrica-02`:23envelopes equipamentos semsobreposição AABB; não
 inclui estrutura/cabos/portas. Incremento115,4kg serviços fixos; subtotal3373,355kg,
 saldo876,645kg antes do restante. Temperaturas de cabos são entradas de sensibilidade,
 não campoI30. `expansao-solar-03`:habitação5,276506kWh/dia semsecagem;
 saldo fixo0,230343kWh/dia antes de perdas de armazenamento/interbarramento.
- Fontes primárias e hashes:cache`tracao-fontes-01/`, catálogo e
 `proveniencia_eletrica.json`. PDFbrutos fora doGit. Ficha antiga2021não aplicada ao packMY25.
- **117passed**,ruffsrc/scripts/tests e estruturaOK. Memorial parcial18páginas,
 1903237bytes; renderização em`memorial-qa-04/`. YAML global intacto.
- Geradores novos:calcular_integracao_eletrica/consolidar_eletrica; consolidação
 recebe caches por argumentos. **Não rodar consolidar_expansao antigo**, sobrescreveria
 entregas com versão anterior. Referências históricas de massa/energia foram superadas.
- Próximo:fechar circuitos/EVSE/tensões e simultaneidade, desenhosOEM/folgas/estrutura,
 custos/eixos, casos físicosI30/33/34/35,CFD equipado e missões. Logo/grafismos externos
 sódepois de terminar a parte técnica, conforme usuário. Sempush/entrega final.
