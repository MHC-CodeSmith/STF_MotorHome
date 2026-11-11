# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# I28 — limite operacional e 0–100

FichaFiatSK20/03/2026p3: limitador90km/h de série nas versões4250kg.
P4 indica90/130/130km/h genericamente nos modosECO/NORMAL/SPORT; a proposta
preserva a restrição específica da versão, sem alegar retirada do limitador.
Página3 renderizada e conferida. Fonte/hash emconfig/limites_operacionais_proposta.yaml.

Logo v_max_operacional <=25m/s. Atingir o próprio limite90km/h exige curvas
reais/perdas/massa; não é provado apenas pela ficha. Com limitador ativo,
100km/h não é alcançável: tempo0–100 não finito/aplicável; campoJSON permanece null
com motivo explícito, nunca0s. Não inventar curva de aceleração.

Sem limitador, a integração seria m_equiv*dv/dt=F_tracao(v)-F_aero(v)-F_rol,
com F_tracao limitada por torque/RPM, transmissão, corrente, potência e aderência.
Essas entradas continuam pendentes; não confundir picos205kW/410Nm com mapa.

I33 usa30→10m/s por exigência do professor, equivalente108→36km/h;
é ensaio térmico prescrito, não evento operacional alegado nesta versão limitada.
[Integração](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: m·dv/dt=min(F_torque,F_potência,F_aderência)−F_resistiva.

Tração dianteira inclui transferência dinâmica de carga. Variante limitada90km/h não atinge100km/h;0–90 hipotético não é mediçãoOEM.

Escopo: Esses tempos não são desempenhoOEM: relação, raio,aderência e envelope não calibrados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
