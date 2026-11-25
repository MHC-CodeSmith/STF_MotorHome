# Resultados do item 34

Fonte vigente do relatório: [varredura completa de 486 casos](../../../../entregas/integrado_maxeon1560/mecanica_termica/I34_sensibilidades.csv).
Ela usa `development.thermal_sweep` do YAML canônico, variando massa, condutâncias,
resistência, entropia e potência. A varredura antiga de 20 linhas `sensibilidade.csv`
é histórica: varia R/entropia com outras entradas fixas e inclui dois casos adiabáticos.
Não deve ser apresentada como outra fonte do mesmo conjunto de 486 casos.

Os históricos nominais 20/80 kW e a figura local permanecem válidos para o protocolo
20–80% de SOC. O complemento de casos extremos e pré-dimensionamento do chiller está
em [dados térmicos do relatório](../../../../relatorio/dados_termicos/resumo.json).
Nenhum resultado representa ensaio ou calibração do pack OEM.

<!-- execucao-integrada:inicio -->
Execução integrada: `entregas/integrado_maxeon1540/mecanica_termica/I34_sensibilidades.csv`.

486casos20/80kW variando massa/UA/cooler/resistência/entropia;conservação elétrica/térmica conferida;3casos atingem o limite45°C e interrompem a carga.

Limite: ECM2nós não packOEM calibrado;20/80kW não são FV disponível; 45°C é limite hipotético.

Índice local: `execucao_integrada.json`;SHA256da evidência: `100eb7664e2a5d2807ac52661682e8d62f499605178caecdd896d5cbc61a0dfa`. Não aprovado fisicamente.
<!-- execucao-integrada:fim -->
