# Fundamentação teórica — item 07

## Objetivo e fenômeno
Seções, material, isolação, correntes, perdas e critérios de proteção.

## Equações e hipóteses
Para correnteDC, I=P_AC/(eta_inversor V_bateria). Com cobre de áreaA e comprimento
total dos dois polosL, R(T)=rho20[1+alpha(T−20)]L/A; quedaDeltaV=IR e calorJoule=I²R.
Resistividade1,724e−8Ωm ealpha0,00393K⁻¹ são hipóteses explícitas de cobre equivalente,
não medições do cabo comprado. Temperatura é entrada de sensibilidade; não se calcula
o campo multidimensional requerido porI30 neste item.

## Entradas e unidades
Dependências diretas: I04 (P4), I06 (P2), I09 (P2).

## Modelo / procedimento
Avaliar4kWAC, eta0,90 assumida,44,8/51,2/56,8V e20/60/90°C;70mm² por polo e2m
de percurso por polo. A bitola e fusível200A são recomendação do manual do
MultiPlus-II48/5000 para ligaçõesaté5m, não especificação da tração400V.

## Limitações
Faltam cabo real/isolação/ampacidade/agrupamento/curto-circuito/terminais/proteções
coordenadas e vibração. RotasCAD não são chicotes com passagens aprovadas. Corrente
de tração máxima não se obtém simplesmente de205kW/400V sem mapa/perdas e limites reais.

<!-- execucao-integrada:inicio -->
Método técnico integrado: V_carga=V_fonte−I·R; P_DC=V_carga·I; R=ρ(T)·L/A; P_Joule=I²R.

Resolver a raiz estável da carga de potência constante. Ampacidade instalada,terminais,I²t e corrente prospectiva real exigem dados não substituídos pela queda de tensão.

Escopo: 56faltas hipotéticas excedem20kA;impedância real/I²t/ampacidade/PE-DR/terminais ainda não validados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
