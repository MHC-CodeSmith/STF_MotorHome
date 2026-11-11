"""Revisão técnica dos35itens e índice das saídas, sem relatório acadêmico."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/desenvolvimento_2026-11-09'

# Each statement is an engineering review, not a human approval. Prior files
# remain linked via the original item inventory; no fabricated new evidence.
UPDATES={
1:('especificado_provisorio','Aurora Solar, BEV duas pessoas; E-DucatoSK505.GG1.2 mantido como variante de estudo.','A identidade técnica está definida; homologação da conversão e aprovação humana continuam separadas.','../integrado_maxeon1540/integracao/layouts_massas.json'),
2:('documentacao_OEM_incompleta','Pneus/rodasOEM preservados. Crr sensibilizado sem trocar pneus.','Medida/índices/pressões da varianteSK exata e massa da roda não obtidos; não copiar de UK/NL.','../integrado_maxeon1540/integracao/dinamica_massa_integrada.csv'),
3:('modelo_condicionado','Disco representativo300mm, partição70/30 e transferência dinâmica calculadas.','Brembo/espessura/cubo/pastilha/compatibilidadeMY25 e limitesABS não demonstrados.','../integrado_maxeon1540/freios_integrados/transferencia_carga_aderencia.csv'),
4:('mapas_OEM_incompletos','Pico205kW/410Nm conservado;36 envelopes hipotéticos de força/rotação implementados.','Envelope não é curvaOEM; eficiência/RPM/mapas reais e potência contínua faltam.','../integrado_maxeon1540/mecanica_termica/I28_envelope_0_90_sensibilidade.csv'),
5:('modelo_condicionado','RedutorOEM preservado; relações8/10/12 e eficiências.95/.97/.99 explicitamente sensibilizadas.','Relação/rotação/óleo real não publicados para varianteSK.','../integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv'),
6:('dimensionado_provisorio','Tração98kWh úteis;3US5000=14.4kWh/119.1kg noCAD. Bancos independentes.','Uso móvel, fixação/BMS e corrente/partidas documentais faltam; buffer não instalado.','../integrado_maxeon1540/integracao/inventario_massas.csv'),
7:('triagem_eletrica_e_rotas_executadas','324casosDC com queda acoplada à carga;144faltas e cabos70/95/120mm²;rotasCAD de reserva.','56faltas hipotéticas excedem20kA;impedância real/I²t/ampacidade/PE-DR/terminais ainda não validados.','../integrado_maxeon1540/protecoes_fixacoes/resumo.json'),
8:('alternativa1540_integrada_condicional','4Maxeon1540Wp integrados emCAD/massa/séries solares;72comparações MPPT preservadas.','Retângulo estimado/curvatura/ancoragens/estoque não comprovados;rastreadores independentes são comparadorDEC054,compartilhamento não aprovado.','../integrado_maxeon1540/solar/resumo.json'),
9:('controladores_comparados_condicionalmente','InversorGX220/60;comparador250/60teto+150/60portáteis;compartilhado72I–V estimadas.','250/60 usa35A conservador;saídas48V não são interfaceHV. BMS/proteções/comutação e interfaceDC não demonstrados.','../integrado_maxeon1540/energia_sistemas/mppt_parecer.json'),
10:('modelo_termico_condicionado','Balanço separado de perdas motor/inversor/redutor e radiador reexecutados.','η/UA/vazão são hipóteses; não reprodução do circuitoOEM.','../integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv'),
11:('ventilacao_natural_e_mecanica_sensibilizadas','48casos de chaminé natural mais648 sensibilidades de vazão de apoio,potência,CO2 e carga térmica sensível; comparação nominal30m³/h incluída.','18L/h·pessoa,alvoCO2,pressão/eficiência do ventilador e operação são hipóteses; sem norma demonstrada,umidade latente,SKU,curva elétrica,ruído ou instalação.','../integrado_maxeon1540/ventilacao_mecanica_sensibilidade/resumo.json'),
12:('escopo_OEM_e_perdas_definidos','BEV não requer óleo de motor diesel; perdas do redutor separadas sem dupla contagem.','Grau/volume/intervalo de óleo e pontos lubrificados OEM não confirmados; não propor substituição.','../integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv'),
13:('CAD_e_inventario_integrados','GeladeiraAC e3US5000 substituem envelopes antigos; água14dias e lavanderia68.8L/ciclo incluídas.','256picos,6históricos e72autonomias por orçamento previsto;partidas reais/atuadores e limiaresSOC continuam não demonstrados.','../integrado_maxeon1540/integracao/agua_operacao_14dias.csv'),
14:('estatica_condicionada','162casos de massa/CG/eixos/índice lateral; suspensãoOEM sem alteração.','Limites por eixo/curso/rigidez e comportamento dinâmico OEM faltam; não homologar por estatística.','../integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv'),
15:('interfaces_espaciais_e_FEM_comparados','378alternativas216cargas por geometria;inversor em planovertical;11Tet4+3Tet10 de tiras e18chapas STEP.','Chassi/ancoragensOEM/furação/contato/fadiga não demonstrados;seleções locais não homologam carroceria.','fixacoes_redimensionadas/resumo.json'),
16:('CAD_equivalente_com_rotas','NovoCAD inclui rotas reservadas de cabo/água e inversor vertical com envelope de acesso livre.','Passagens/terminais/chapariaOEM e drenagem/estanqueidade ainda não demonstrados.','../integrado_maxeon1540/rotas_instalacoes/layoutA_rotas_reserva.step'),
17:('CAD_comparativo_executado','2layouts e2tetos STEP/GLB;3vistas com escala e cotas;A sem colisõesAABB,com inversor corrigido vertical e acesso100mm de estudo.','B tem acesso de lavagem6mm insuficiente e portáteis altos;A selecionado provisoriamente. Não é CADOEM.','../integrado_maxeon1540/integracao/A_fixa_vistas.png'),
18:('massa_estimada_integrada','Inventário1540Wp,doisMPPT,móveis,2p/bagagem;água85Ltanque+15Lboiler sem duplicação;162casos.','Tara/CGbase e posições assumidos; não pesagem. Limites por eixo permanecem desconhecidos.','../integrado_maxeon1540/integracao/inventario_massas.csv'),
19:('CFD_equipado_com_malha_adicional','Malha4 com1.034.158 células passou checkMesh;SIMPLE paralelo394 iterações;Cd diagnóstico0,60058 e faixa relativa0,0175% nas últimas50.','Limite900s atingido sem residualControl: Uy inicial4,65e-5 e p1,22e-4 na última iteração completa; sem y+, independência/GCI ou Cd definitivo.','../aero_equipado1540/malha_adicional_1/resumo.json'),
20:('calculado_com_sensibilidade','Crr.008/.012/.016 estimado, propagado ao modelo; sem alterar pneus.','Não apresentar Crr como ensaio dos pneusOEM.','../integrado_maxeon1540/integracao/dinamica_massa_integrada.csv'),
21:('sensibilidade_estrada_parametrica','Grade de8100 combinações de massa típica/PBT, velocidade, rampa, vento longitudinal, Crr, Cd e densidade; inclui resistência ao rolamento, gravidade e arrasto relativo ao ar.','Rampa/vento e coeficientes são hipóteses, não rota medida; sem aceleração, mapas OEM ou limites de pneus/eixos.','../integrado_maxeon1540/dinamica_resistiva_sensibilidade/resumo.json'),
22:('potencia_roda_com_sensibilidade','Potência mecânica assinada nas rodas e demanda de bateria a velocidade constante; ponto plano40km/h reproduzido, aclive e vento avaliados sem creditar regeneração.','Eficiência0,90 e auxiliares700W estimados; potência na roda não é mapa/potência contínua do motor, sem validação OEM ou física.','../integrado_maxeon1540/dinamica_resistiva_sensibilidade/resumo.json'),
23:('bancos_24_48_CAD_suporte_comparados','24h2/3módulos e48h4/5 por reservas20/30%;4CADs e12cargas suporte inteiro com peso dos trilhos.','Massa/rack/CAD estimados;uso móvel/BMS/folgas/retençãoOEM e capacidade final não validados.','../integrado_maxeon1540/bancos_24_48_cad/resumo.json'),
24:('BOM27_rastreada_por_moeda','BOMcanônica1540regenerada;GX1093USD+MPPT393USD+250/60USD465=1951USDlista2026Q2;veículoEUR50990 separado.','Preços lista semVAT não são cotação instalada;BRL439cooktop é histórico,frete/tributos/câmbio permanecemnull.','../integrado_maxeon1540/bom_atual/resumo.json'),
25:('despacho_temporal_condicional','630alocações MILP,grade de partidas,30/15/5min;40/80 e curva10–90km/h,crédito solar inicial zero.','Uma parada+carga seguida de condução;serviços cíclicos separados,mínimosDC hipotéticos,sem provaOEM/ótimo global.','../integrado_maxeon1540/despacho_i25/resumo.json'),
26:('calculado_condicionado','km/kWh40/80 com3976.53kg e700W auxiliares de tração; serviços separados.','Eficiência constante e dados de rolamento/aerodinâmica estimados.','../integrado_maxeon1540/energia_sistemas/I25_I26_autonomia_solar_consumo.csv'),
27:('otimizado_no_modelo_restrito','Jensen+min e(v) resolvem velocidade/duração≤24h no controle sem reposiçãoHV;100/80→30% exatos.','Não otimiza política solarDC não comprovada;duração17h é idealização acadêmica,não escala operacional segura.','../integrado_maxeon1540/energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv'),
28:('resposta_limitador_e_sensibilidade','0–100inalcançável por limitador90;36envelopes hipotéticos0–90=9.23–14.19s.','Esses tempos não são desempenhoOEM: relação, raio,aderência e envelope não calibrados.','../integrado_maxeon1540/mecanica_termica/I28_envelope_0_90_sensibilidade.csv'),
29:('busca_finita_com_sensibilidade_temporal','Grade1008, busca densa5268, refinamentos e294 políticas locais a15/5/1min; líderes 10/20%:242,802/248,764/248,784d e20/30%:244,802/250,760/250,780d.','Diferença≈6d mostra interação do mínimoDC1kW hipotético com passo temporal; comparações finitas, sem ótimo global, interface autorizada ou viabilidade física.','../integrado_maxeon1540/otimizacao_resolucao_temporal/resumo.json'),
30:('campo_multidimensional_condicionado','Camposrθ de serviços e referênciaHV documentada reexecutados;malha/analítica/sensibilidade.','Corrente de faseOEM na potência máxima desconhecida;DC569.4A não equivale a RMSde fase.Não modificarcabos.','cabos_HV_referencia/resumo_cabos.json'),
31:('CFD3D_complementar_executado','Rede matinal preservada;3malhas3D RANSkε e4replaysPIMPLE;conservação por faces verificada.','SIMPLErejeitado;CFDtransiente é complemento com contornos congelados,sem CHT/mobiliário/y+convergente.','cabine_transiente/balanco_convergencia.json'),
32:('carga_e_revisao_comercial_verificadas','72sensibilidadescapacidade/envelope/solar e12elétricas;manualFW3000rev2018220–240V50/60Hzconferido.','Margem nominal1p184W/2p54W não valida33°C;SKU/placa,partida e fusível5A versus6.2A precisam confirmação.','hvac_revisao/resumo.json'),
33:('simulado_com_massa_integrada','24casos r-z com3976.53/4250kg,atrito e regen0/40/80kW;resistências subtraídas e carga dinâmica.','Disco/material/repartição/regenOEM não confirmados;108km/h é ensaio prescrito,acima limitador90.','../integrado_maxeon1540/freios_integrados/convergencia.csv'),
34:('simulado_com_sensibilidade','54novoscasos20/80kW variando massa/UA/cooler;conservação elétrica/térmica conferida.','ECM2nós não packOEM calibrado;20/80kW não são FV disponível.','../integrado_maxeon1540/mecanica_termica/I34_54sensibilidades.csv'),
35:('modelo_comercial_condicionado','CurvaBosch e radiador2D reexecutados;campos e ponto de operação conservados.','Bomba é candidata de modelo,não equipamentoOEM comprovado;curva de perdas/UA/ar ainda estimados.','arrefecimento/resumo_hidraulica.json'),
}


def main():
    old=json.loads((ROOT/'entregas/etapa_pos_dec061/matriz_itens_35.json').read_text())
    items=[]
    for prior in old['items']:
        num=prior['item'];status,work,missing,path=UPDATES[num]
        target=(OUT/path).resolve()
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
