# Aprovações finais pendentes — lista única pós-DEC061

**Nenhuma aprovação final está sendo solicitada agora para suprir falta de evidência.** Esta é a lista consolidada para revisão ao fechar os estudos. A autorização DEC-061 permite as recomendações provisórias abaixo; não as transforma em aprovadas.

Atualização de execução02: [resultados técnicos](EXECUCAO_TECNICA02.md). As16entradas permanecem uma única lista; nenhuma aprovação está sendo solicitada durante o desenvolvimento.

Já aprovados anteriormente e preservados: arquitetura B como direção, bancos independentes, geometria L3H2, pneus e suspensão OEM, metas1540+1.600 Wp, portáteis só parados com ângulo fixo por parada,220 V / 60 Hz, média diária de serviços, gerenciamento automático, ventilação natural prioritária, A/Csob banco prioritário, monitoramento básico, água100/70/cassete~20L,7.000 kmplano, ambosSOC100% e≤8 h/dia sem carga externa. **Não reabrir essas decisões para forçar viabilidade.**

## A01 — Variante OEM

- **Estado / responsável:** provisorio; P1/P4.
- **Opções:** SK505.GG1.2/4.250 kg × SK505.BG1.2/3.500 kg × BR a documentar.
- **Recomendação provisória:** Manter SK505.GG1.2 como candidata integrada; não congelar homologação.
- **Justificativa e fonte:** Ficha única e maior capacidade de carga; 3.500 kg já excede subtotal conhecido. [oem_sk](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf).
- **Impactos e incertezas:** Tara2.790 kg; limite90 km/h; preço50.990 EUR sem IVA. Eixos/importação e configuração final pendentes.
- **Dependências:** B03; A02/A04/A10/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A02 — Recarga DC direta ou buffer dedicado

- **Estado / responsável:** nao_demonstrado_bloqueante; P2/P5.
- **Opções:** DC direto × buffer exclusivo × controle sem recarga.
- **Recomendação provisória:** Manter controle sem interface como referência; não instalar buffer. Comparação matemática preservada.
- **Justificativa e fonte:** Não existe equipamento/conjuntoOEM demonstrado para a potênciaFV; buffer não resolve protocolo. [venema](https://4x4electric.com/charging-technique/).
- **Impactos e incertezas:** Mínimosreais/conversor/isolamento/autorização desconhecidos;32comparações deUS5000dedicado4,56kWh créditoFV+39,7kg como limite inferior,sem instalação. Mínimos1/3kW são hipóteses;massadehardwareextra/custo não fechados.
- **Dependências:** B01; libera missão física somente após evidência.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A03 — Alocação FV e MPPT compartilhado

- **Estado / responsável:** nao_demonstrado; P2/P5/P3.
- **Opções:** Fixosserviços/portáteistração × inverso × comutaçãoflexível; 1MPPT×múltiplosrastreadores.
- **Recomendação provisória:** Para cenário1540Wp usar250/60teto+150/60portáteis como comparador independente. Manter estudo prioritário compartilhado:2S2Pportáteis excede35A conservador;4Sportáteis reduz corrente,masmismatch estimado0,657–27,272%. Nenhuma topologia compartilhada aprovada;saída48V não alimentaHV.
- **Justificativa e fonte:** Geração sem dupla contagem;Maxeon eEcoFlow têm curvas/temperaturas/orientações distintas. Fontesmaxeon3_2022/mppt250_60/mppt150_60;arquivos72casos emteto_maxeon e cenário integrado1540Wp. ArranjoJA+190permanece comparador histórico1350Wpúteis.
- **Impactos e incertezas:** Topologia, comutação, Vocfrio/Vmpquente, mismatch e perdas precisamdemonstração; sem ponte entre bancos.
- **Dependências:** B01/B05; A02/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A04 — Autonomia e módulos de serviços

- **Estado / responsável:** provisorio_condicionado; P2/P6/P1/P3.
- **Opções:** 24 h ×48 h; reservas20%×30%; candidatoantigo10.24kWh×US5000modular.
- **Recomendação provisória:** 3×US5000/14,4kWh provisório24h,atende ambas reservas no perfilbase. 24h2módulos só comreserva20%;48h4/5módulos por20/30%. QuatroCADs/12suportes do banco inteiro executados;capacidade final não aprovada.
- **Justificativa e fonte:** 3módulos cobrem consumo-base em ambas reservas; massa119,1 kg; 48 h amplia massa/volume. [pylon](https://en.pylontech.com.cn/products/c23/134.html).
- **Impactos e incertezas:** Uso veicular/vibração seguem não demonstrados; integraçãoUS5000–Victron requerGX/CAN-BMS/DVCC;novo candidatoMultiPlusII GX trazGX evisor incorporados,sem gateway externo. Cabeamento/firmware/partidas/uso móvel não ensaiados. Caso alto requer mais capacidade. Ganho de48hcomcortes de cargas não equivale a48hdo perfilcompleto;72cenários de prioridades e5/15Wextras sensibilizados.
- **Dependências:** B06; A05/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A05 — Inversor de serviços

- **Estado / responsável:** provisorio_condicionado; P2.
- **Opções:** MultiPlusII48/5000/70-50 × Inverter Smart48/5000 × MultiPlusII GX48/5000.
- **Recomendação provisória:** MultiPlusII GX48/5000 ajustado220 V / 60 Hz provisoriamente,paraBMS-CAN evisor comerciais integrados;sem central própria.
- **Justificativa e fonte:** GX documenta4000/3700W,5000VA,18Wvazio,31kg e565×323×148mm;210–245V e50/60Hz configuráveis. IntegraGX/BMS-CAN/visor;Smart sozinho não satisfaz integraçãoPylontech documentada. [multi](https://www.victronenergy.com/media/pg/MultiPlus-II_GX/en/technical-specifications-mp-ii-gx-230v.html).
- **Impactos e incertezas:** GX31kg versus30kgregular/28kgSmart;18Wvazio deGX preserva energia de serviços. Eficiênciasmáximasnão são curvas. EntradaACnão usada na missão; partidas/proteções pendentes.
- **Dependências:** B06; A04/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A06 — Climatização

- **Estado / responsável:** documentado_por_revisao_condicionado; P6/P2/P3.
- **Opções:** FreshWell 3000/2.7kWsob banco × CoolTopTrail35/3.5kWde teto × outra compatível.
- **Recomendação provisória:** FreshWellFW3000 da revisãoO16s2018 selecionado provisoriamente para estudo220–240V50/60Hz;correspondência deSKU/placa antes aquisição. Webasto50Hz/teto rejeitado.
- **Justificativa e fonte:** ManualDometic2018/p29,espelhoJacksons,documenta220–240V50/60Hz,6.2Anominais60Hz e2700WISO5151;variante exata adquirida não confirmada. [freshwell](https://www.jacksonsleisure.com/content/pdf/dometic/dometic-freshwell-3000-manual.pdf).
- **Impactos e incertezas:** Carga térmica1/2p e margens calculadas por rede equivalente; 72sensibilidades executadas;faltamcurvas33°C,dutos,partida,SKU/placa e coordenaçãofusível5A do manual versus6.2Anominais. Não usar4.3A de outra revisão.
- **Dependências:** B07/B08; A04/A05/A10/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A07 — Geladeira AC

- **Estado / responsável:** provisorio; P6/P2/P3.
- **Opções:** MideaMRC10B2 × sucessorMDRD142FGD303 × antigoNRXDCdescartado como principal.
- **Recomendação provisória:** MRC10B2/93L220 V / 60 Hz provisório.
- **Justificativa e fonte:** Manual/página documentam alimentação, massa20.8kg e14.1 kWh/mês; não misturar18kg do sucessor. [fridge](https://www.midea.com/br/refrigeracao/frigobares/frigobar-branco-93l-midea).
- **Impactos e incertezas:** 0.47kWh/dreferência antes perdas; testar calor/instalação×1–2; partida, retenção, ventilação e disponibilidade pendentes.
- **Dependências:** B06; A04/A05/A10.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A08 — Cozinha e lavanderia

- **Estado / responsável:** provisorio_condicionado; P6/P2/P3.
- **Opções:** IE3TP1zona × outros1zona; LG11/7kg × compacta documentada.
- **Recomendação provisória:** IE3TP220 V / 60 Hz2kW e LGCV9011WC4A como candidatos; lavanderia1vez/semana.
- **Justificativa e fonte:** Cooktopmanual rastreável; LGjá noCAD; secagem não foi omitida do balanço. [cooktop](https://api.electrolux-medialibrary.com/asset/e295c711-5ce0-44d6-8d54-265bb08e664a/E4RM3Q/250717TCLQ/PDF/250717TCLQ.pdf).
- **Impactos e incertezas:** Cooktop2.3kg; LG73kg,68.8L/ciclo e secagem1–4kWh hipotética. Uso da lavanderia quase enche tanque cinza sozinho.
- **Dependências:** B06/B10; A04/A05/A10.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A09 — Boiler e rede potável

- **Estado / responsável:** provisorio_condicionado; P6/P2/P3.
- **Opções:** QuickB31505S × ElgenaKB6; Shurflo12 V×24 V; trecho10×13mm.
- **Recomendação provisória:** Quick15L500W como candidato condicionado; Shurflo4008-101-E65/12 V provisória; comparar tubulações.
- **Justificativa e fonte:** CurvaShurflo tem aplicaçãoRV; Quick220Vpressurizado documentado. ElgenaKB6max0.8bar incompatível com rede pressurizada. [potable_pump](https://www.pentair.com/content/dam/extranet/web/nam/shurflo/data-sheets/pds-4008-101-X65.pdf).
- **Impactos e incertezas:** Boiler7kgvazio +água dentro100L; manter sem ligaçãoarrefecimentoOEM. Quick60Hz/veicular e rotas/proteções/expansão/alívio pendentes.
- **Dependências:** B10; A04/A05/A10/A12.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A10 — Layout e isolamento

- **Estado / responsável:** provisorio_com_comparacao_incompleta; P3/P6/P1.
- **Opções:** Cama fixa existente × conversível; isolamento32mm × espessuras alternativas.
- **Recomendação provisória:** LayoutA de cama fixa selecionado provisoriamente; massa3976,53kg no cenário1540Wp, corredor0,454m e reserva da porta0,59m. ComparadorB não recomendado sem corrigir acesso/84kg elevados. Fixações e geometriaOEM continuam condicionadas.
- **Justificativa e fonte:** Doislayouts foram comparados emCAD;A atualizado com inversor vertical,comparadorB ainda falha acesso/orientação e portáteis altos. `config/parametros_globais.yaml:sources.history`.
- **Impactos e incertezas:** Comparação geométrica executada;faltam geometriasOEM/vidros/fogo/umidade e validação de manutenção. InversorAvertical565mm e rotas de reserva atualizados.
- **Dependências:** B08/B09; A04/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A11 — Módulos e ocupação do teto

- **Estado / responsável:** condicionado_nao_validado; P3/P2/P5/P1.
- **Opções:** 3JA450+190Wcabine × 2SPR-MAX3-380-COM+2SPR-MAX3-390-COM.
- **Recomendação provisória:** Alternativa preferida para próxima integração:2Maxeon380+2Maxeon390,total1540Wp/76kg,sem módulo190W de baixa tensão. Cabe no retângulo estimado com6mm extras,mas instalação/estoque/proteções pendentes. Cenário integrado1540Wp executado com3976,53kg,250/60teto+150/60portáteis como comparador independente;referência1350Wp preservada separadamente. Curvatura/ancoragens e disponibilidade continuam condicionadas.
- **Justificativa e fonte:** FichaMaxeon544454revA/2022 conferida,fonte única sources.maxeon3_2022;CADteto_maxeon e72comparações I–V estimadas. Meta1540Wp preservada.
- **Impactos e incertezas:** 150V incompatível comVocfrio171,48V;250/60 apenas triagem telhado13,96A. Comportáteis2S2P chega35,96A>35A conservador;4S fica24,96A mas mismatch/curvas reais permanecem abertos. Não háMPPT compartilhado aprovado.
- **Dependências:** B05/B09; A03/A06/A10.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A12 — Barramento DC secundário

- **Estado / responsável:** provisorio_condicionado; P2/P6.
- **Opções:** 12 V ×24 V com conversor desde48 V.
- **Recomendação provisória:** 12 V provisório por bomba/comandos; 24 V permanece comparação.
- **Justificativa e fonte:** Mesma carga/cabo em24 V reduz perdasJoule para1/4; conversor e catálogo podem alterar vencedor. [potable_pump](https://www.pentair.com/content/dam/extranet/web/nam/shurflo/data-sheets/pds-4008-101-X65.pdf).
- **Impactos e incertezas:** CurvaShurflo12 V não pode ser transplantada para24 V; vazio/eficiência de conversor e corrente total pendentes.
- **Dependências:** B06; A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A13 — Política e reservas da missão

- **Estado / responsável:** em_comparacao; P5/P2/P4.
- **Opções:** 08–16 × horário alternativo00–08 × otimização futura; 10/20×20/30.
- **Recomendação provisória:** Conservar a grade histórica de 1.008 políticas (243,84375/244,88542 dias), o comparador de velocidade fixa com 796 pontos (242,885417 dias a 20,4 km/h para reservas 10/20%; 244,885417 dias a 19,8 km/h para 20/30%), a busca densa de 5.268 pontos com partida variável (242,802083/244,802083 dias) e o refinamento extra de 286 pontos. Esses métodos distintos não devem ser fundidos nem interpretados como ótimo global. Uma análise local posterior de 294 políticas a 15/5/1 min encontrou 242,802083/244,802083 dias a 15 min, 248,763889/250,760417 dias a 5 min e 248,784028/250,779861 dias a 1 min para reservas 10/20% e 20/30%, respectivamente. A quase coincidência entre 5 e 1 min, e a diferença de cerca de 6 dias frente a 15 min, mostram que o mínimo de potência DC hipotético de 1 kW interage materialmente com a discretização temporal. Todos dependem de interface DC hipotética e não demonstram missão fisicamente viável. Os 290,875/292,885 dias pertencem à comparação anterior de 1.350 Wp.
- **Justificativa e fonte:** Novos replays coerentes permitem avaliar tendências; horárioalternativo não é políticaotimizadademonstrada. `config/parametros_globais.yaml:sources.hyp`.
- **Impactos e incertezas:** Dias, soc e conclusão mudam com consumo, interface e clima; somente hipóteses de dia-tipo idealizado.
- **Dependências:** B01/B04; A02/A03/A04/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A14 — Parâmetros físicos e validação

- **Estado / responsável:** nao_demonstrado_em_partes; P1/P3/P4/P6/P7.
- **Opções:** FaixaCd × Cdconvergido; massatípica ×PBT; modelostérmicosrepresentativos ×dadosOEM.
- **Recomendação provisória:** Adotar provisoriamente faixas deCd/Crr e verificação numérica. CFD3Dcabine+FEMtrilhos executados; média50,32°C é complemento condicionado. Aero equipado: 3 malhas-base e novas variantes. Grading4 (510.281 células) convergiu; grading2 (743.286) chegou a1800 sem residualControl; malha1 (1.034.158) também não convergiu. Cd diagnóstico0,60051/0,64287/0,70047; y+ alto/heterogêneo. Malhas não aninhadas, sem independência/GCI/Cd definitivo; faixa anterior segue apenas sensibilidade. Nenhuma validação física inferida.
- **Justificativa e fonte:** 3 malhas não independentes; campostérmicos reais não validam seusparâmetros; 100km/hnãoatingívelna4250. `config/parametros_globais.yaml:sources.cfd`.
- **Impactos e incertezas:** 378alternativas com planovertical do inversor eCGnormal derivadoCAD;11Tet4+3Tet10 locais.18chapas somam33,138kg brutos de comparação;substituição líquida/apoiosOEM não demonstrados. TanqueTet4varia1,144% e inversorTet10varia0,550%;Tet4inversor insuficiente permanece identificado. Sem tensão de engaste convergida. ExigeCAD/massa,eixos,CFDequipado e revisão cruzada.
- **Dependências:** B03/B08/B09/B11; libera resultados finais poritem.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A15 — Proteções, controle e monitoramento

- **Estado / responsável:** nao_demonstrado; P2/P6/P7.
- **Opções:** Indicadores comerciais e atuadores documentados × integração a definir.
- **Recomendação provisória:** Manter monitoramento básico comercial,sem central própria. Máquina de estados/falhas,256combinações de simultaneidade e72autonomias de prioridades por orçamento previsto simuladas;GX exigido pela combinaçãoUS5000/Victron é incorporado no novo inversorGX candidato;nenhumgateway/central externa própria. ConectorCANtipoA/firmware/DVCC eatuadores seguem a validar.
- **Justificativa e fonte:** DEC047/056 já aprovadas; implementação e patamares ainda dependemBMS e hardware. [multi](https://www.victronenergy.com/media/pg/MultiPlus-II_230V/en/technical-specifications-mp-ii-230v.html).
- **Impactos e incertezas:** 324casosDC/144faltas calculados;JLLN200/80A candidatos125VDC20kA,mas56faltas hipotéticas excedem20kA;dadoPylonUSSeries2024<2000A/1ms é teto de saída declarado,não prova de corrente prospectiva ou coordenaçãoI²t. CurvasI²t/seletividade/impedância real/contatores/DR-PE permanecem não demonstrados. PatamaresSOCnull;nenhum ensaio físico.
- **Dependências:** B06; A04/A05/A12.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A16 — Orçamento instalado

- **Estado / responsável:** nao_demonstrado; P1.
- **Opções:** AquisiçãoSK/importação × aquisiçãoBRdocumentada; conversão+montagem+engenharia+encargos.
- **Recomendação provisória:** BOM aberta com preços desconhecidosnull; não aprovar total numérico.
- **Justificativa e fonte:** Referências primáriasUSD1951 paraGX+doisMPPTs no cenário1540;EUR50990veículo eBRL439cooktop separados. Câmbio/frete/tributos e várias massas/componentes faltantes. [oem_sk](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf).
- **Impactos e incertezas:** Motor, packHV, freios e arrefecimentoOEM não são somados novamente. Alternativas não se somam entre si.
- **Dependências:** B12; depende deA01–A15.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.
