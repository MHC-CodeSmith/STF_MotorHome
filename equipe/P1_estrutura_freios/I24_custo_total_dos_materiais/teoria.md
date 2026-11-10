# I24 — BOM e custo em reais

BOM parcial27linhas derivadas das configurações de equipamentos/elétrica/solar,
com quantidade, massa conhecida, inclusãoOEM, opção e preço de referência quando
consultado. Custo final=sum(q_i*p_i)+fretes+instalação+tributos aplicáveis sem
dupla contagem; insumos ausentes permanecem null, nunca zero.

Oferta pública ElectroluxIE3TPR$439/R$589referência,26/10/2026, exige seleção
devoltagem/entrega; não é cotação vinculante220V ou custo instalado. Tributos
não foram discriminados. SubtotalR$439 não é o preço do motorhome.
ChassiSK€50990semIVA não é custo nacional de importação emR$.

Preços, fretes, câmbio e tributos de aquisição efetiva, além de mobiliário,
fixações/cabos/tubos/quadros/mão de obra, precisam completar o orçamento.
[scripts/calcular_bom_e_rolamento.py](../../../scripts/calcular_bom_e_rolamento.py)
reproduz CSV/JSON comhashes. [Fontes e limitações](../../../docs/MECANICA_ROLAMENTO_E_CUSTOS.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: C_ref,moeda=Σq_i·preço_i conhecido; total instalado não existe se faltam linhas/frete/tributos.

BOM separaEUR/USD/BRL,conversão e componentesOEM. Valores de lista não são cotação importada;preços desconhecidos continuamnull.

Escopo: Preços lista semVAT não são cotação instalada;BRL439cooktop é histórico,frete/tributos/câmbio permanecemnull.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
