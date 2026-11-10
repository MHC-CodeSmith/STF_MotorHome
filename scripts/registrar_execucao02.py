"""Revisão técnica dos35itens e índice das saídas, sem relatório acadêmico."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/desenvolvimento_2026-11-09'

# Each statement is an engineering review, not a human approval. Prior files
# remain linked via the original item inventory; no fabricated new evidence.
UPDATES={
1:('especificado_provisorio','Aurora Solar, BEV duas pessoas; E-DucatoSK505.GG1.2 mantido como variante de estudo.','A identidade técnica está definida; homologação da conversão e aprovação humana continuam separadas.','integracao/layouts_massas.json'),
2:('documentacao_OEM_incompleta','Pneus/rodasOEM preservados. Crr sensibilizado sem trocar pneus.','Medida/índices/pressões da varianteSK exata e massa da roda não obtidos; não copiar de UK/NL.','integracao/dinamica_massa_integrada.csv'),
3:('modelo_condicionado','Disco representativo300mm, partição70/30 e transferência dinâmica calculadas.','Brembo/espessura/cubo/pastilha/compatibilidadeMY25 e limitesABS não demonstrados.','freios_integrados/transferencia_carga_aderencia.csv'),
4:('mapas_OEM_incompletos','Pico205kW/410Nm conservado;36 envelopes hipotéticos de força/rotação implementados.','Envelope não é curvaOEM; eficiência/RPM/mapas reais e potência contínua faltam.','mecanica_termica/I28_envelope_0_90_sensibilidade.csv'),
5:('modelo_condicionado','RedutorOEM preservado; relações8/10/12 e eficiências.95/.97/.99 explicitamente sensibilizadas.','Relação/rotação/óleo real não publicados para varianteSK.','mecanica_termica/I10_I12_balanco_perdas.csv'),
6:('dimensionado_provisorio','Tração98kWh úteis;3US5000=14.4kWh/119.1kg noCAD. Bancos independentes.','Uso móvel, fixação/BMS e corrente/partidas documentais faltam; buffer não instalado.','integracao/inventario_massas.csv'),
7:('triagem_eletrica_e_rotas_executadas','324casosDC com queda acoplada à carga;144faltas e cabos70/95/120mm²;rotasCAD de reserva.','56faltas hipotéticas excedem20kA;impedância real/I²t/ampacidade/PE-DR/terminais ainda não validados.','protecoes_fixacoes/resumo.json'),
8:('estudo_comparativo_executado','Duas ocupaçõesCAD do teto;1540Wp mantido como meta. MPPTmismatch36cenários.','Um arranjo excede envelope; outro depende do teto de cabine/ancoragens.190W→48V não demonstrado.','integracao/teto_duas_configuracoes.json'),
9:('selecao_provisoria_condicionada','MultiPlusII GX48/5000 vertical220/60,BMS-CAN/visor integrados;150/60-Tr em estudo;JLLN200/080 candidatos condicionados.','150/60 suporta50AIsc frente36.48A e135.4Vcold<145V;IV/proteções/BMS não demonstrados.250/60 rejeitado provisoriamente por conflito35/60A.','energia_sistemas/mppt_parecer.json'),
10:('modelo_termico_condicionado','Balanço separado de perdas motor/inversor/redutor e radiador reexecutados.','η/UA/vazão são hipóteses; não reprodução do circuitoOEM.','mecanica_termica/I10_I12_balanco_perdas.csv'),
11:('calculado_condicionado','Vazão natural,CO2 e vapor48cenários, sem ventilador novo.','Vento0 e ΔT0 geram0vazão; ventilação não garantida. ManualFW3000rev2018 admite220–240V50/60Hz;placa adquirida/curva33°C epartidas pendentes.','integracao/ventilacao_natural_co2_umidade.csv'),
12:('escopo_OEM_e_perdas_definidos','BEV não requer óleo de motor diesel; perdas do redutor separadas sem dupla contagem.','Grau/volume/intervalo de óleo e pontos lubrificados OEM não confirmados; não propor substituição.','mecanica_termica/I10_I12_balanco_perdas.csv'),
13:('CAD_e_inventario_integrados','GeladeiraAC e3US5000 substituem envelopes antigos; água14dias e lavanderia68.8L/ciclo incluídas.','256combinações de picos e6históricos de falha simulados;partidas reais/atuadores e limitesSOC ainda não demonstrados.','integracao/agua_operacao_14dias.csv'),
14:('estatica_condicionada','162casos de massa/CG/eixos/índice lateral; suspensãoOEM sem alteração.','Limites por eixo/curso/rigidez e comportamento dinâmico OEM faltam; não homologar por estatística.','integracao/massa_cg_eixos_sensibilidade.csv'),
15:('geometria_de_estudo_definida','Mesma varianteSK; envelope útil desconta32mm+6mm por face.','Posição de eixos/piso/caixas de roda ainda estimadas; apoiosOEM e documentação de conversão faltam.','integracao/layouts_massas.json'),
16:('CAD_equivalente_com_rotas','NovoCAD inclui rotas reservadas de cabo/água e inversor vertical com envelope de acesso livre.','Passagens/terminais/chapariaOEM e drenagem/estanqueidade ainda não demonstrados.','rotas_instalacoes/layoutA_rotas_reserva.step'),
17:('CAD_comparativo_executado','2layouts e2tetos STEP/GLB;3vistas com escala e cotas;A sem colisõesAABB,com inversor corrigido vertical e acesso100mm de estudo.','B tem acesso de lavagem6mm insuficiente e portáteis altos;A selecionado provisoriamente. Não é CADOEM.','integracao/A_fixa_vistas.png'),
18:('massa_estimada_integrada','Inventário inclui conversão, móveis, revestimentos,100kg água,2p e bagagem;162casos.','Tara/CGbase e posições assumidos; não pesagem. Limites por eixo permanecem desconhecidos.','integracao/inventario_massas.csv'),
19:('CFD_refinado_rejeitado','Nova tentativa3malhas:2não retêm camadas;fina178298 retém mas diverge;retryPCG/DIC também rejeitado.','Cdvalidado permanecenull;geometria equipada/novamesha estável e independência não demonstradas.','aero_camadas/resumo.json'),
20:('calculado_com_sensibilidade','Crr.008/.012/.016 estimado, propagado ao modelo; sem alterar pneus.','Não apresentar Crr como ensaio dos pneusOEM.','integracao/dinamica_massa_integrada.csv'),
21:('calculado_com_sensibilidade','164pontos força de arrasto/rolamento10–90km/h para2layouts×2massas.','Cd/Crr/ρ condicionais; pista plana e vento0.','integracao/dinamica_massa_integrada.csv'),
22:('calculado_com_sensibilidade','Potência nas rodas e bateria separadas;700W de auxiliares de tração hipotéticos.','AuxiliaresOEM0/300/700/1500W sensibilizados, não confundidos com serviços.','integracao/dinamica_massa_integrada.csv'),
23:('dimensionado_provisorio','98úteis/110brutosOEM;14.4kWhserviços;24/48h comparação anterior reproduzível.','3módulos atendem24hbase/reserva30%,48h exige4/5; não aprovar capacidade final.','energia_sistemas/I29_missoes_massas_integradas.json'),
24:('BOM26_rastreada_por_moeda','BOMcanônica regenerada;GX1093USD+MPPT393USD de lista oficial2026Q2;veículoEUR50990 separado.','Preços lista semVAT não são cotação instalada;BRL439cooktop é histórico,frete/tributos/câmbio permanecemnull.','bom_atual/resumo.json'),
25:('despacho_temporal_condicional','630alocações MILP,grade de partidas,30/15/5min;40/80 e curva10–90km/h,crédito solar inicial zero.','Uma parada+carga seguida de condução;serviços cíclicos separados,mínimosDC hipotéticos,sem provaOEM/ótimo global.','despacho_i25/resumo.json'),
26:('calculado_condicionado','km/kWh40/80 com3973kg e700W auxiliares de tração; serviços separados.','Eficiência constante e dados de rolamento/aerodinâmica estimados.','energia_sistemas/I25_I26_autonomia_solar_consumo.csv'),
27:('otimizado_no_modelo_restrito','Jensen+min e(v) resolvem velocidade/duração≤24h no controle sem reposiçãoHV;100/80→30% exatos.','Não otimiza política solarDC não comprovada;duração17h é idealização acadêmica,não escala operacional segura.','energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv'),
28:('resposta_limitador_e_sensibilidade','0–100inalcançável por limitador90;36envelopes hipotéticos0–90=9.23–14.19s.','Esses tempos não são desempenhoOEM: relação, raio,aderência e envelope não calibrados.','mecanica_termica/I28_envelope_0_90_sensibilidade.csv'),
29:('busca_finita_e_replays_executados','1008casos e32replays corrigidos para700Waux;9572eventos hídricos sequenciais em paradas efetivas.','Melhor da grade, não ótimo global; mínimoDC1kW hipotético e fontes sanitárias por parada presumidas.','otimizacao_grade/resumo.json'),
30:('campo_multidimensional_condicionado','Camposrθ de serviços e referênciaHV documentada reexecutados;malha/analítica/sensibilidade.','Corrente de faseOEM na potência máxima desconhecida;DC569.4A não equivale a RMSde fase.Não modificarcabos.','cabos_HV_referencia/resumo_cabos.json'),
31:('CFD3D_complementar_executado','Rede matinal preservada;3malhas3D RANSkε e4replaysPIMPLE;conservação por faces verificada.','SIMPLErejeitado;CFDtransiente é complemento com contornos congelados,sem CHT/mobiliário/y+convergente.','cabine_transiente/balanco_convergencia.json'),
32:('carga_e_revisao_comercial_verificadas','72sensibilidadescapacidade/envelope/solar e12elétricas;manualFW3000rev2018220–240V50/60Hzconferido.','Margem nominal1p184W/2p54W não valida33°C;SKU/placa,partida e fusível5A versus6.2A precisam confirmação.','hvac_revisao/resumo.json'),
33:('simulado_com_massa_integrada','24casos r-z com3973/4250kg,atrito e regen0/40/80kW;resistências subtraídas e carga dinâmica.','Disco/material/repartição/regenOEM não confirmados;108km/h é ensaio prescrito,acima limitador90.','freios_integrados/convergencia.csv'),
34:('simulado_com_sensibilidade','54novoscasos20/80kW variando massa/UA/cooler;conservação elétrica/térmica conferida.','ECM2nós não packOEM calibrado;20/80kW não são FV disponível.','mecanica_termica/I34_54sensibilidades.csv'),
35:('modelo_comercial_condicionado','CurvaBosch e radiador2D reexecutados;campos e ponto de operação conservados.','Bomba é candidata de modelo,não equipamentoOEM comprovado;curva de perdas/UA/ar ainda estimados.','arrefecimento/resumo_hidraulica.json'),
}


def main():
    old=json.loads((ROOT/'entregas/etapa_pos_dec061/matriz_itens_35.json').read_text())
    items=[]
    for prior in old['items']:
        num=prior['item'];status,work,missing,path=UPDATES[num]
        target=OUT/path
        if not target.exists() and num==30:
            candidates=list((OUT/'cabos_HV_referencia').glob('resumo*.json'))
            target=candidates[0];path=str(target.relative_to(OUT))
        if not target.exists():raise FileNotFoundError(target)
        items.append({'item':num,'owner':prior['owner'],'requirement':prior['requirement'],
                      'status':status,'executed_or_reviewed':work,'remaining_limit':missing,
                      'evidence':str(target.relative_to(ROOT)),'historical_inventory':prior['folder'],
                      'human_approval_recorded':False})
    items.sort(key=lambda x:x['item'])
    (OUT/'revisao_35_itens.json').write_text(json.dumps({'items':items,'reviewed':35,'final_human_approved':0,
        'technical_stage_complete':False},indent=2,ensure_ascii=False)+'\n')
    lines=['# Revisão técnica dos35itens — execução02','',
           'Checkpoint de desenvolvimento, sem aprovação humana final. Modelos condicionados não são validação física. A etapa técnica completa continua aberta.','',
           '|Item/dono|Estado e execução/revisão|Limitação remanescente|Evidência|','|---|---|---|---|']
    for row in items:
        lines.append(f'|{row["item"]:02d}/{row["owner"]}|{row["status"]}: {row["executed_or_reviewed"]}|{row["remaining_limit"]}|[arquivo](../{row["evidence"]})|')
    (ROOT/'docs/REVISAO_TECNICA_EXECUCAO02.md').write_text('\n'.join(lines)+'\n')
    print('35 itens revisados;0 aprovações inferidas.')


if __name__=='__main__':main()
