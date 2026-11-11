# I14 — suspensão e direção retidas

Arquitetura de referência: suspensão dianteira pseudo-MacPherson, molas
helicoidais, amortecedores hidráulicos/barra estabilizadora; traseira reforçada
com feixes duplos acima de3,5t; direção elétrica. FiatUKMY25.5p25, seção elétrica,
conferida visualmente. Referência de mercado não substitui placa da varianteSK.
Manter conjuntosOEM; mola reforçada não aumenta automaticamente PBT homologado.

Carga estática por eixo exige soma de forças/momentos: Rfr+Rtr=m*g;
Rfr*L=sum(m_i*g*x_i), tomando x_i a partir do eixo traseiro e L=4,035m.
É necessário incluir distribuição da taraOEM, não só equipamentos adicionados.
Sem posição do CGOEM/placa de eixos e BOM total, cargas não estão fechadas.
Rigidezes, amortecimento, frequências e estabilidade em curva ainda pendentes.
Não somar massa OEM novamente. [Fontes](../../../docs/MECANICA_ROLAMENTO_E_CUSTOS.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: R_r=m·g·x_CG/L; R_f=m·g−R_r; ΔR=m·a·h_CG/L; índice≈(t/2−|y_CG|)/h_CG.

Suspensão/pneusOEM inalterados. Índice quaseestático não fornece velocidade segura de curva ou homologação;limites por eixo/rigidez/curso desconhecidos.

Escopo: Limites por eixo/curso/rigidez e comportamento dinâmico OEM faltam; não homologar por estatística.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
