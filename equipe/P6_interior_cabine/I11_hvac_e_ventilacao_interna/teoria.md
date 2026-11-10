# Fundamentação teórica — item 11

## Objetivo e fenômeno
Especificar sistemas e tecnologias de aquecimento, ar-condicionado e ventilação.

## Equações e hipóteses
Q_v=Cd·A_eff·√(2gH·|ΔT|/T); 1/A_eff²=1/A_baixa²+1/A_alta².

## Entradas e unidades
Dependências diretas: I13 (P6), I16 (P3), I17 (P3).

## Modelo / procedimento
Ventilação natural prioritária. Com vento0 eΔT0,modelo produz vazão0. CO2/vapor usam balanços de geração e renovação,sem prometer salubridade.

## Limitações
Vento0 e ΔT0 geram0vazão; ventilação não garantida. ManualFW3000rev2018 admite220–240V50/60Hz;placa adquirida/curva33°C epartidas pendentes.

<!-- execucao-integrada:inicio -->
Método técnico integrado: Q_v=Cd·A_eff·√(2gH·|ΔT|/T); 1/A_eff²=1/A_baixa²+1/A_alta².

Ventilação natural prioritária. Com vento0 eΔT0,modelo produz vazão0. CO2/vapor usam balanços de geração e renovação,sem prometer salubridade.

Escopo: Vento0 e ΔT0 geram0vazão; ventilação não garantida. ManualFW3000rev2018 admite220–240V50/60Hz;placa adquirida/curva33°C epartidas pendentes.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
