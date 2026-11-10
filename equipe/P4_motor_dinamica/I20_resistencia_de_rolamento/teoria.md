# I20 — coeficiente de rolamento comparativo

Pneu alternativo ContinentalVanContactCamper0451473/225-75R16CP118R,
classeC2/eficiênciaC. UE2020/740AnexoIParteA: RRC6,8–8,0N/kN;
Cr=RRC/1000=0,0068–0,0080. Ponto médio0,0074 assumido para comparação,
não medido. F_rol=Cr*m*g; em4250kg e plano, F=283,412–333,426N;
P_rol=F*v. CSV reproduzido por scripts/calcular_bom_e_rolamento.py.

Não é o pneuA/S04514690000 documentado antes. Não transferir massa/raio/pressão
entre artigos. Adoção doCamper depende de roda, capacidade por eixo, pressão,
raio e compatibilidade. Rótulo em laboratório não éCr real no asfalto local,
com temperatura/carga/velocidade variáveis. Grade dinâmica anterior permanece
sensibilidade, sem alterar parâmetros aprovados.
[Fontes e dados](../../../docs/MECANICA_ROLAMENTO_E_CUSTOS.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: F_rol=Crr·m·g em pista plana; P_rol=F_rol·v.

Crr0,008/0,012/0,016 é caixa de hipóteses,não ensaio de pneusOEM;variar massa e condição de uso mantendo pneus de fábrica.

Escopo: Não apresentar Crr como ensaio dos pneusOEM.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
