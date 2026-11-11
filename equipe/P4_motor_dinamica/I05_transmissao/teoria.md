# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# I05 — transmissão elétrica retida

Proposta: manter redutor de relação fixa, diferencial e semieixos dianteiros OEM.
A [Fiat DE](https://www.fiat.de/professional/modelle/e-ducato/technical-data)
confirma transmissão elétrica de relação fixa. Consulta26/10/2026. Isso não
fornece relação total, rendimento, rotação máxima ou curva de perdas da varianteSK.
Não importar97kWh úteis da páginaDE para98kWh da fichaSK.

Equações SI: omega_motor=i_total*v/r_efetivo;
T_roda=eta_trans*i_total*T_motor; P_roda=eta_trans*P_motor.
Raio efetivo do pneu candidato0,361262m, conforme documentação Continental;
não é raio da malha visual. Sem i_total/n_max/mapas, não se geram curvas reais.
Nenhum câmbio manual de Ducato diesel foi adotado por analogia.

Limite de90km/h na versão4250kg da fichaSKp3 deve ser preservado.
[Proveniência e interfaces](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Relação, óleo homologado, limites e revisão humana PENDENTES.

<!-- execucao-integrada:inicio -->
Método técnico integrado: n_motor=60·i·v/(2πr); P_perdas=(1−η_red)·P_entrada.

Relações8/10/12 e eficiências sensibilizadas;redutorOEM permanece intacto. Relação real/óleo/volume não demonstrados.

Escopo: Relação/rotação/óleo real não publicados para varianteSK.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
