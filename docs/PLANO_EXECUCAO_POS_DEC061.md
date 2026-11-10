# Execução reproduzível P1–P7 — cenário integrado1540Wp

O trabalho computacional abaixo já foi executado. Este documento define reprodução e fronteiras entre pacotes;as pendências remanescentes são evidências específicas em [BLOQUEIOS_POS_DEC061.md](BLOQUEIOS_POS_DEC061.md),sem transferir tarefas genéricas ao usuário ou solicitar aprovações individuais.

|Pacote / itens|Integração efetivamente executada|Limite externo de validação|
|---|---|---|
|P1/1,2,3,14,15,18,24,33|Identidade/variante de estudo;inventário,CAD/CG/eixos/água85+15L;162sensibilidades;378interfaces,14FEM3D de tiras;freios24casos;BOMpor moeda.|LimitesOEM por eixo/pneu/apoios,material do chassi,ancoragem/fadiga,disco real e orçamento instalado.|
|P2/6,7,9,23,30|Serviços3US5000/GX;comparação24/48h;324circuitos/144faltas/256picos;estados/falhas;12/24V e rotas;cabos com campos;MPPTs independentes/compartilhado e32buffercomercial.|B01;uso móvel/BMS,partidas,coordenaçãoI²t/PE-DR/ampacidade/atuadores e correnteRMSfaseOEM.|
|P3/16,17,19|Dois layouts/tetos,CADcomFV e rotas,vistas cotadas;trêsCFDequipados com logs/forças/y+;tentativas numéricas anteriores preservados como rejeitados.|Geometria/curvatura/apoiosOEM,embalagem detalhada e validação aerodinâmica;Cd apenas intervalo condicional.|
|P4/4,5,20,21,22,28|36envelopes de aceleração;resistências/potência/massas;972pontos de caixa de incerteza;limitador90km/h respeitado.|MapasOEM/relação/óleo/pressões e regeneração reais;0–100inalcançável na variante de estudo.|
|P5/8,25,26,27,29|FV1540+1600séries próprias;630MILP;I27SOC30%;1008políticas,32replays,120sensibilidades,36DCdiários,32buffercomercial;água8004eventos.|Interface/autorizaçãoDC;políticas finitas não provam ótimo global;dadosERA5/rota7511km permanecem complementares.|
|P6/11,13,31,32|Consumo médio e simultaneidade separados;água/boiler/ventilação/CO2/umidade;rede matinal+CFD3Dcomplementar;72HVAC+12partidas hipotéticas.|SKU/capacidade/partidasHVAC,uso veicular/instalação hidráulica/renovação de ar e propriedades reais do envelope.|
|P7/10,12,34,35|Perdas/circuito de referência;54térmicos20/80kW;multinós,bomba/radiador2D,sensibilidade/conservação.|R(SOC,T),UA/vazões/fluido/óleo e componentesOEM reais;não alterar circuitoHV.|

## Fonte única e comandos válidos

`config/parametros_globais.yaml` contém o cenário histórico de estudo1350Wp e a sobreposição nomeada `development.integrated_scenarios.maxeon1540_independente`. A sobreposição é resolvida pelo código;`parametros_resolvidos.json` é saída derivada,não uma segunda fonte editável. Os arquivos de entrada por executor e snapshotshashados preservam a proveniência.

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
PYTHONPATH=src .venv/bin/python scripts/verificar_estrutura.py
PYTHONPATH=src .venv/bin/python scripts/auditar_projeto.py --json
```

A cadeia registra17comandos e interrompe por falha ou mudança de configuração durante execução. Reproduzir CFD requer destino novo em `executar_aero_equipado.py`,preservando tentativas/logs;não executar novamente sobre diretório já entregue. Metodologia e comandos especializados constam em `EXECUCAO_TECNICA02.md`.

`conciliar_dec061.py` e consolidadores dobaseline29defc4 são históricos,limitados por revisão/flags;não são comandos atuais de atualização. Não sobrescrever a listaA01–A16 ou hashes antigos. Relatório acadêmico,ABNT,slides e envio não fazem parte desta execução técnica. Entrega02/12/2026 às06h America/Sao_Paulo permanece registrada.
