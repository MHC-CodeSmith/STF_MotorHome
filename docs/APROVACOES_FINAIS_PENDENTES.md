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
- **Impactos e incertezas:** Mínimos reais, custo, massa, isolamento e autorização nulos; mínimo1 kW nos replays é hipótese.
- **Dependências:** B01; libera missão física somente após evidência.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A03 — Alocação FV e MPPT compartilhado

- **Estado / responsável:** nao_demonstrado; P2/P5/P3.
- **Opções:** Fixosserviços/portáteistração × inverso × comutaçãoflexível; 1MPPT×múltiplosrastreadores.
- **Recomendação provisória:** Selecionar150/60-Tr provisoriamente no estudo compartilhado para serviços:50AIsc>36,48A,145Voperação>135,4Vcold;250/60não escolhido por conflitoIsc35/60A. Mismatch estimado0,18–25,99%; sem liberar associaçãoIV/proteções ou saída paraHV.
- **Justificativa e fonte:** A geração não pode ser duplicada; JA e EcoFlow têmcurvas/tensões distintas; cab190Wnão é string48 V. `config/parametros_globais.yaml:sources.history`.
- **Impactos e incertezas:** Topologia, comutação, Vocfrio/Vmpquente, mismatch e perdas precisamdemonstração; sem ponte entre bancos.
- **Dependências:** B01/B05; A02/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A04 — Autonomia e módulos de serviços

- **Estado / responsável:** provisorio_condicionado; P2/P6/P1/P3.
- **Opções:** 24 h ×48 h; reservas20%×30%; candidatoantigo10.24kWh×US5000modular.
- **Recomendação provisória:** 3 × US5000/14,4 kWh como banco provisório24 h; base48 h comparar4/5módulos.
- **Justificativa e fonte:** 3módulos cobrem consumo-base em ambas reservas; massa119,1 kg; 48 h amplia massa/volume. [pylon](https://en.pylontech.com.cn/products/c23/134.html).
- **Impactos e incertezas:** Uso veicular, vibração, fixação, BMS e compatibilidade ainda não demonstrados. Caso alto de consumo requer mais capacidade.
- **Dependências:** B06; A05/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A05 — Inversor de serviços

- **Estado / responsável:** provisorio_condicionado; P2.
- **Opções:** MultiPlusII48/5000/70-50 × Inverter Smart48/5000.
- **Recomendação provisória:** MultiPlusII ajustado220 V / 60 Hz provisoriamente.
- **Justificativa e fonte:** Preserva candidato existente; ambos4000W25°C/3700W40°C e ajustáveis210–245V50/60Hz. Smartdispensa carregadorAC. [multi](https://www.victronenergy.com/media/pg/MultiPlus-II_230V/en/technical-specifications-mp-ii-230v.html).
- **Impactos e incertezas:** Vazio18Wvs20W; massas30vs28kg; eficiênciasmáximasnão são curvas. EntradaACnão usada na missão; partidas/proteções pendentes.
- **Dependências:** B06; A04/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A06 — Climatização

- **Estado / responsável:** nao_demonstrado; P6/P2/P3.
- **Opções:** FreshWell 3000/2.7kWsob banco × CoolTopTrail35/3.5kWde teto × outra compatível.
- **Recomendação provisória:** Não congelar modelo. FreshWell segue referência dimensional; Webasto50Hz/teto rejeitado para baseline.
- **Justificativa e fonte:** Comparação comercial maior foi feita, mas nenhuma compatibilidade220 V / 60 Hz sob banco demonstrada. [freshwell](https://www.dometic.com/externalassets/dometic-freshwell-3000-_104014.pdf).
- **Impactos e incertezas:** Carga térmica1/2p e margens calculadas por rede equivalente; faltamcurvas33°C, dutos, picos e alimentação220V.
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
- **Recomendação provisória:** LayoutA de cama fixa selecionado provisoriamente; massa3973,03kg, corredor0,454m e reserva da porta0,59m. ComparadorB não recomendado sem corrigir acesso/84kg elevados. Fixações e geometriaOEM continuam condicionadas.
- **Justificativa e fonte:** AproveitaCAD preexistente; não afirma que cama conversível foi comparada emCAD. `config/parametros_globais.yaml:sources.history`.
- **Impactos e incertezas:** Folgas, ergonomia, compartimentos, áreas, vidros, fogo/umidade, manutenção e segundoestudo faltam.
- **Dependências:** B08/B09; A04/A06/A07/A08/A09.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A11 — Módulos e ocupação do teto

- **Estado / responsável:** condicionado_nao_validado; P3/P2/P5/P1.
- **Opções:** 3JA450+190Wcabine × novo arranjo comercial1.540 Wp comprovável.
- **Recomendação provisória:** Preferir estudar arranjoJA3+190W transversal; alternativo190Wlongitudinal excede envelope estimado. Meta1540Wp mantida; apenas1350Wp têm caminho48Vprincipal creditado. Não congelar instalação.
- **Justificativa e fonte:** 190Wdebaixa tensão ainda sem caminho48 V; não reduzir silenciosamente a meta. `config/parametros_globais.yaml:sources.history`.
- **Impactos e incertezas:** Falta duasocupações/ancoragens/sombras; BOMconta massa190Wmasreplaynão promete aproveitamento48 V.
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
- **Recomendação provisória:** Usar melhor política da grade1008 apenas como hipótese:20–04h,20km/h paraauxiliartração700W estimado;290,875/292,885dias conforme reservas. Não declarar ótimo global, operação rodoviária recomendada ou sessãoDCreal.
- **Justificativa e fonte:** Novos replays coerentes permitem avaliar tendências; horárioalternativo não é políticaotimizadademonstrada. `config/parametros_globais.yaml:sources.hyp`.
- **Impactos e incertezas:** Dias, soc e conclusão mudam com consumo, interface e clima; somente hipóteses de dia-tipo idealizado.
- **Dependências:** B01/B04; A02/A03/A04/A11.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A14 — Parâmetros físicos e validação

- **Estado / responsável:** nao_demonstrado_em_partes; P1/P3/P4/P6/P7.
- **Opções:** FaixaCd × Cdconvergido; massatípica ×PBT; modelostérmicosrepresentativos ×dadosOEM.
- **Recomendação provisória:** Adotar provisoriamente faixas deCd/Crr e verificação numérica. CFD3Dcabine+FEMtrilhos executados; média50,32°C é complemento condicionado. y+aerodinâmicomédio516,6 não sustenta Cd definitivo. Nenhuma validação física inferida.
- **Justificativa e fonte:** 3 malhas não independentes; campostérmicos reais não validam seusparâmetros; 100km/hnãoatingívelna4250. `config/parametros_globais.yaml:sources.cfd`.
- **Impactos e incertezas:** ExigeCAD/massa, eixos, FEA, CFD 3Dcabine, curvasmotor, propriedadescabos/freios/bateria e revisão cruzada.
- **Dependências:** B03/B08/B09/B11; libera resultados finais poritem.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A15 — Proteções, controle e monitoramento

- **Estado / responsável:** nao_demonstrado; P2/P6/P7.
- **Opções:** Indicadores comerciais e atuadores documentados × integração a definir.
- **Recomendação provisória:** Manter monitoramento básico comercial e shedding automático como requisitos, sem central própria.
- **Justificativa e fonte:** DEC047/056 já aprovadas; implementação e patamares ainda dependemBMS e hardware. [multi](https://www.victronenergy.com/media/pg/MultiPlus-II_230V/en/technical-specifications-mp-ii-230v.html).
- **Impactos e incertezas:** Circuitos, DR/PE, curto, fusíveis, contatores, falhas e plano de ensaios ainda precisam memorial; nenhum ensaio físico realizado.
- **Dependências:** B06; A04/A05/A12.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.

## A16 — Orçamento instalado

- **Estado / responsável:** nao_demonstrado; P1.
- **Opções:** AquisiçãoSK/importação × aquisiçãoBRdocumentada; conversão+montagem+engenharia+encargos.
- **Recomendação provisória:** BOM aberta com preços desconhecidosnull; não aprovar total numérico.
- **Justificativa e fonte:** Somente referências parciais, sem câmbio/frete/tributos e várias massas/componentes faltantes. [oem_sk](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf).
- **Impactos e incertezas:** Motor, packHV, freios e arrefecimentoOEM não são somados novamente. Alternativas não se somam entre si.
- **Dependências:** B12; depende deA01–A15.
- **Aprovação necessária:** revisão técnica das evidências e aprovação humana final da escolha; enquanto houver bloqueio, não liberar instalação, homologação ou conclusão física.
