"""Memorial PDF de revisão, a partir dos artefatos locais, sem anexos brutos."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, default=Path('output/pdf/memorial_revisao_aurora.pdf'))
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    delivery = root/'entregas/parcial_2026-10-24'
    cabin = json.loads((delivery/'resumo_cabine.json').read_text())
    n = cabin['nominal']
    solar = json.loads((delivery/'resumo_solar.json').read_text())
    expansion = json.loads((delivery/'resumo_expansao_solar.json').read_text())
    installations = json.loads((delivery/'manifesto_instalacoes.json').read_text())
    electrical = json.loads((delivery/'resumo_integracao_eletrica.json').read_text())
    electrical_cad = json.loads((delivery/'manifesto_cad_eletrico.json').read_text())
    pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
    pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVuBold')
    styles = getSampleStyleSheet()
    for name in ('Normal', 'BodyText', 'Title', 'Heading1', 'Heading2'):
        styles[name].fontName = 'DejaVu'
    styles['BodyText'].fontSize = 9
    styles['BodyText'].leading = 13
    styles['BodyText'].spaceAfter = 9
    styles['Heading1'].fontSize = 17
    styles['Heading1'].textColor = colors.HexColor('#106b75')
    styles['Heading1'].spaceAfter = 13
    styles['Heading2'].fontSize = 11
    styles['Heading2'].textColor = colors.HexColor('#106b75')
    styles.add(ParagraphStyle('Small', fontName='DejaVu', fontSize=7.5, leading=10, spaceAfter=6))
    styles.add(ParagraphStyle('Banner', fontName='DejaVuBold', fontSize=10, leading=14,
                              textColor=colors.HexColor('#8d3b11'), alignment=TA_CENTER, spaceAfter=14))
    story = []

    def para(text, style='BodyText'):
        # O texto é autoral; só títulos/links externos são escapados nos pontos de uso.
        text = re.sub(r'(?<=\d)(?=(?:°C|kW\b|kWh\b|W\b|kg\b|mm\b|V\b|h\b|min\b|kJ\b))', ' ', text)
        story.append(Paragraph(text, styles[style]))

    def heading(text):
        para(text, 'Heading1')

    def pic(name, height_cm):
        path = delivery/name
        im = Image(str(path))
        scale = min(17*cm/im.imageWidth, height_cm*cm/im.imageHeight)
        im.drawWidth, im.drawHeight = im.imageWidth*scale, im.imageHeight*scale
        story.append(im)
        story.append(Spacer(1, .2*cm))

    def table(rows, widths, font='Small'):
        content = [[Paragraph(escape(str(v)), styles[font]) for v in row] for row in rows]
        t = Table(content, colWidths=[v*cm for v in widths], repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3eff0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), .3, colors.HexColor('#bacbce')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, .25*cm))

    def page():
        story.append(PageBreak())

    para('AURORA SOLAR', 'Title')
    para('Motorhome elétrico solar<br/>Memorial de revisão técnica', 'Title')
    para('VERSÃO PARCIAL - SEM APROVAÇÃO FINAL DE ENGENHARIA', 'Banner')
    para('Projeto acadêmico SEM0571 - Sistemas Térmicos e Fluídicos. '
         'Base proposta: Fiat E-Ducato MY25, L3H2, PBT 4.250 kg, ao menos duas pessoas. '
         'Documento compilado de cálculos, fontes e figuras locais; os PDFs e CAD brutos '
         'permanecem em cache externo ao repositório.')
    pic('aurora_L3H2_proposta.png', 8)
    para('A geometria detalhada é uma adaptação autoral do Ducato 2014 OpenX Assets. '
         'Não constitui CAD OEM, homologação ou comprovação de encaixe dos equipamentos.', 'Small')
    para('O que esta revisão permite avaliar', 'Heading2')
    para('Arquitetura BEV, carroceria e layout, estudos CFD exploratórios, geração solar, '
         'consumo em cenários, agendas verificadas e balanço térmico de cabine. '
         'A matriz ao final explicita as lacunas de cada um dos 35 itens.')
    para('Não há conclusão de viabilidade física da missão de 7.000 km. Faltam mapas OEM, '
         'integração solar com a tração, componentes térmicos, BOM/custos e validações. '
         'Os testes de software verificam métodos; não aprovam o veículo.')
    para('Entrega oficial: 02/12/2026 às 06:00 local. PDF abaixo de 20 MB, seminário de até '
         '8 minutos e vídeo de 8 a 10 minutos com os integrantes, abaixo de 50 MB. '
         'Este arquivo não foi enviado aos docentes.')
    page()

    heading('1. Requisitos e método de trabalho')
    table([['Condição', 'Aplicação'],
           ['São Carlos, 21/06, céu limpo', 'A711 INMET: -21,98027777°, -47,88388888°, 859,29 m.'],
           ['25°C, UR50%, vento atmosférico nulo', 'Condição geral; não implica convecção nula.'],
           ['I25 / I26', 'Solar gerado no dia; eficiência em km/kWh na bateria, respectivamente.'],
           ['I27', 'Maximizar distância diária; SOC final exatamente 30%; sem limite extra de 8h.'],
           ['I29', '7.000 km, menor tempo, bateria inicial + solar, sem carga externa; até 8h de condução por dia de calendário.'],
           ['I30 / I33', 'Campos multidimensionais reais dos cabos e freios; não substituir por modelos concentrados.'],
           ['I31 / I32', 'Cabine fechada sem ocupantes/AC; depois regime permanente 33°C fora/25°C dentro com ocupante.'],
           ['I34 / I35', 'Carga de bateria 20/80 kW; circuito de refrigeração no máximo do motor.']], [5, 12])
    para('Hierarquia: enunciado original 2026; divisão P1-P7; parâmetros globais aprovados; '
         'fontes primárias; adaptações externas. A configuração global permanece intacta, '
         'com 24 campos desconhecidos. Propostas independentes não são promovidas a dados aprovados.')
    para('Apostila SEM0571, Cristiano B. Tibiriçá, 2025: Fourier p.9, Newton p.10; '
         'balanços de trocadores p.31, efetividade-NUT pp.38-39; bombas p.56; '
         'armazenamento sensível p.74, Eq.112. Curvas de motor, solar, pneus e CFD '
         'requerem referências externas e não são atribuídas à apostila.')
    para('A revisão da apostila registrou possíveis inconsistências de limites e índices '
         'nas pp.15,17,39,48-50,75. O código não adota uma expressão de efetividade que '
         'produza valores acima de 1 nem soma fluxos sem conservação. Ver docs/revisao_apostila.md.')
    para('Rastreabilidade', 'Heading2')
    para('Cada cenário mantém unidades SI, configuração, script, fontes e hashes. '
         'Os JSON e CSV permitem inspecionar números além das figuras. Fontes protegidas '
         'são citadas; documentos brutos de terceiros não foram incorporados ao relatório. '
         'A fonte primária Fiat foi conferida nas pp.1,4,5; o isolamento é dado técnico de '
         'fabricante, mas sua aplicação automotiva ainda requer verificação.')
    page()

    heading('2. Plataforma, pneus e massa')
    table([['Parâmetro OEM da proposta', 'Valor'],
           ['Variante', 'E-Ducato MY25 L3H2 4250 kg, código 505.GG1.2'],
           ['Motor elétrico / tração', '205 kW de pico / 410 Nm / dianteira'],
           ['Armazenamento / tensão', '110 kWh brutos / 98 kWh úteis / 400 V'],
           ['Comprimento / largura sem espelhos', '5,998 / 2,050 m'],
           ['Entre-eixos / altura OEM', '4,035 m / 2,592 a 2,612 m'],
           ['Massa sem motorista / PBT', '2790 / 4250 kg'],
           ['Recarga', 'CCS2, DC até 150 kW; AC OEM 11 kW MY25']], [9, 8])
    para('Os picos de torque e potência não definem uma curva de eficiência ou uma potência '
         'contínua admissível. Faltam redução, mapas, limites térmicos, massa/resistência do '
         'pack e protocolo BMS. A massa OEM já inclui os conjuntos de tração; não somá-los de novo.')
    para('Pneu candidato - sem seleção final', 'Heading2')
    para('Continental VanContact A/S, artigo 04514690000, 225/75 R16C, 121R. Fonte primária '
         'publica aro de 6 a 7 in, diâmetro 29,3 in, massa 37,3 lb, carga máxima 3195 lb, '
         '709 rev/milha e pressão máxima de 90 psi. Conversões: diâmetro 0,74422 m; '
         'massa 16,919 kg; raio efetivo 0,361262 m; pressão máxima 620,5 kPa. '
         '<b>A pressão máxima não é pressão operacional do motorhome.</b>')
    para('A malha atual apresenta pneus de aproximadamente 0,700895 m de diâmetro. '
         'O candidato é 6,18% maior: adoção exige rever CAD, contato com o solo, transmissão '
         'e CFD. Capacidade por eixo, roda completa e placa de pressões seguem pendentes.')
    para('Orçamento preliminar de carga', 'Heading2')
    para(f"Reserva total OEM:4250-2790=1460kg. Com equipamentos internos conhecidos, "
         f"serviços, teto fixo, duas pessoas e água assumidas, subtotal{electrical['new_known_mass_subtotal_kg']:.1f}kg; "
         f"restam{electrical['unallocated_mass_kg']:.1f}kg antes dos itens faltantes. "
         'Não equivale à massa montada: é preciso '
         'BOM sem duplicações, posições de massas e verificação de limites por eixo. '
         'Custos em R$ com impostos ainda não foram consolidados.')
    page()

    heading('3. CAD e ocupação')
    pic('layout_proposto.png', 9)
    para('A carroceria foi estendida nas regiões de carga/teto para comprimento 5,998 m, '
         'entre-eixos 4,035 m e topo 2,612 m. Rodas deslocadas rigidamente, preservando '
         'tamanho original. Não é uma reprodução certificada da variante elétrica.')
    table([['Reserva interna', 'Dimensões e restrições'],
           ['Cama para duas pessoas', 'Estrado1,95 x 1,35 m; colchão modelado1,91 x 1,31 m; topo1,05 m, instalações sob estrado.'],
           ['Cozinha', '1,40 x 0,58 x 0,92 m; geladeira, pia e indução com envelopes especificados.'],
           ['Banheiro', '0,90 x 0,70 x 1,80 m; sanitário e ducha; ergonomia/espessuras ainda pendentes.'],
           ['Dinette', 'Mesa rebatível em reserva0,65 x 0,70 m; assentos de cabine ilustrativos.'],
           ['Painéis no teto', 'Fixa:3JA450 + Victron190 =1540 W; extensão opcional+3JA450 só estacionado.']], [5, 12])
    para('A triagem do topo do banheiro usou 81 raios e folga mínima externa de 40,85 mm. '
         'Não considera espessura/isolamento, caixas de roda, ergonomia ou colisão completa. '
         'O piso Z=0,68 m e a traseira X=-3,35 m são alinhamentos assumidos.')
    para('visualizador.html contém a carroceria GLB e equipamentos reconhecíveis em CAD autoral, funciona offline '
         'e permite inspeção de vistas. É visualizador, não editor CAD paramétrico. '
         'Onshape e Fusion foram pesquisados em documentação oficial; não houve upload '
         'a serviços públicos. Onshape gratuito implica documentos públicos/não comerciais. '
         'O exterior OpenX preserva MPL-2.0 e CC-BY-4.0 com atribuição na entrega.')
    page()

    heading('3A. Equipamentos internos e CAD de integração')
    pic('cad_interior.png', 8)
    rows = [['Equipamento', 'X / Y / Z [mm]', 'Massa de fabricante']]
    for item in installations['equipment']:
        rows.append([item['label'], ' x '.join(str(round(v*1000)) for v in item['dimensions_xyz_m']),
                     f"{item['mass_kg']} kg" if item['mass_kg'] is not None else 'Pendente'])
    table(rows, [8, 5, 4])
    para('Lava-seca sob cama: profundidade total620 mm e porta aberta1100 mm segundo LG; '
         'não usar565 mm como envelope total. Uma lavagem fria consome68,8 L/0,29 kWh; '
         'energia de secagem ainda desconhecida. Fixação automotiva e acesso precisam de revisão. '
         'As dimensões da geladeira, HVAC, indução e sanitário vêm de fabricantes; '
         'os sólidos e detalhes visuais são autorais, não CAD OEM. Pia e tanque são propostas próprias.')
    para('O HVAC sob cama libera o teto. FreshWell3000:2700 W de frio,21 kg,230 V50/60 Hz, '
         '4,3 A de corrente. Corrente AC não define potência ativa nem COP. Sua margem '
         'nominal sobre2646 W condicionados para duas pessoas é de apenas2%; '
         'curva33°C, dutos e sombreamento de vidros precisam fechar a seleção.')
    page()

    heading('3B. Ampliação solar, montagem e peso')
    pic('cad_solar_aberto.png', 7.5)
    pic('expansao_solar.png', 7)
    para('Proposta principal: cobertura fixa1540 W, quatro módulos. Alternativa de '
         'estudo: seis JA450 e um Victron190,2890 W expostos quando aberta. '
         'Recolhida, a camada superior sombreia a inferior: apenas três JA mais190 W produtivos. '
         'Módulo menor:SPM041903903, ficha atual; o175 W encontrado na pesquisa estava descontinuado.')
    para(f"Após perdas assumidas: fixa/recolhida{expansion['energy_kwh']['mixed_stowed_w']:.3f} kWh/dia; "
         f"aberta{expansion['energy_kwh']['mixed_open_lower_string_off_if_shaded_w']:.3f} a"
         f"{expansion['energy_kwh']['mixed_open_geometric_beam_shading_w']:.3f} kWh/dia nos dois modelos de sombra. "
         'Não é faixa garantida: difusa, diodos/mismatch e térmica da montagem não foram validados. '
         'OrientaçãoX=norte/Y=leste e operação estacionada durante o sol são hipóteses.')
    page()
    heading('3C. Limites de execução da cobertura')
    table([['Caso', 'Potência exposta STC', 'Massa de teto estimada'],
           ['Fixa, proposta principal', '1540 W', f"{installations['fixed_roof_mass_estimate_kg']:.2f} kg"],
           ['Extensão empilhada recolhida', '1540 W', f"{installations['stacked_roof_mass_estimate_kg']:.2f} kg"],
           ['Extensão aberta estacionado', '2890 W', 'Apoios ao solo; vento/fixação ainda não dimensionados']], [7, 5, 5])
    para('Massas de suporte usam volume sólido CAD e densidade2700 kg/m³ assumida, '
         'sem ferragens adicionais. O desenho inclui longarinas/travessas tubulares, '
         'guias, sapatas com altura ajustada à malha e apoios telescópicos. '
         'Não é FEM, mecanismo homologado ou montagem validada nos pontos OEM.')
    para('O arranjo empilhado171,19 kg excede uma referência de teto/rack150 kg. '
         'A Fiat UK menciona até200 kg e50 kg por barra dependendo da configuração; '
         'isso não confirma a variante E-DucatoMY25 escolhida nem a distribuição entre barras. '
         'A versão fixa mais leve é a proposta principal. Extensão requer teto/fixação '
         'compatíveis, módulos mais leves ou transporte dos complementares em suporte interior dimensionado.')
    para('Serviços: duas strings3JA em MPPT150/35 independentes para48 V; o190 W '
         'exige terceiro MPPT100/20 a12 V proposto. Não unir strings diferentes em série. '
         'Banco de serviços10,24kWh e DC/DC agora têm candidatos dimensionados na seção3D; '
         'EVSE, proteções e compatibilidade OEM ainda faltam. '
         'O diagrama funcional éPV-serviços-inversor-EVSE-cargaOEM estacionada; '
         'não há conexão solar400 V aprovada.')
    para(f"Orçamento parcial de massa: equipamentos internos conhecidos{sum(i['mass_kg'] or 0 for i in installations['equipment']):.1f} kg; "
         f"soma OEM+componentes+duas pessoas+100 kg água+telhado fixo"
         f"{electrical['base_known_mass_subtotal_kg']:.1f} kg antes da elétrica de serviços da seção3D. "
         'Não é massa montada: faltam mobiliário, cabos, '
         'tubos, ferragens e bagagens; verificar eixos, centro de massa e custo com impostos.')
    para(f"Habitação assumida, sem secagem:{expansion['household_total_excluding_dryer_kwh_day']:.3f} kWh/dia. "
         f"Saldo agregado fixo de apenas{expansion['remaining_after_household_before_storage_losses_kwh_day']['mixed_stowed_w']:.3f} kWh/dia; "
         'aberta permite saldo maior nas hipóteses, antes de armazenamento e transferência entre barramentos. '
         'Não equivale a energia garantida para tração ou viabilidade da missão7000 km.')
    page()

    heading('3D. Tração e instalações elétricas no CAD')
    pic('cad_tracao.png', 8)
    para(f"Conjunto autoral com{electrical_cad['parts']} sólidos, reimportados em STEP "
         'com volumes positivos. Pack sob piso com15módulos ilustrativos, motor dianteiro, '
         'redutor/diferencial, inversor, carregador e radiador/ventiladores; rotas de alta '
         'tensão, refrigeração e serviços indicadas. O viewer offline oferece23seletores e vista técnica.')
    para('As cotas de tração não foram obtidas do OEM. Pack2,90x1,44x0,32m, '
         'motor cilíndrico0,36x0,42m e demais envelopes/posições são estimativas de integração. '
         'Vão livre230mm e folga130mm até piso são hipóteses, não especificações Fiat. '
         '15módulos5x3 são ilustração; química, fixações, massa e trocas térmicas seguem pendentes.')
    para('Pack/motor/transmissão já integram os2790kg OEM. A sensibilidade hipotética '
         '110000Wh/(140,170,200Wh/kg) dá785,7/647,1/550kg; não foi somada ao veículo, '
         'usada como massa térmica ou atribuída ao fabricante.')
    para('A triagem dos envelopes dos23equipamentos não encontrou sobreposição. '
         'Não abrange estrutura OEM, isolamento, portas, terminais e todas as rotas. '
         'Reimportar sólidos não valida colisões, montagem, arrefecimento ou resistência.')
    page()

    heading('3E. Banco de serviços e uso dos espaços')
    pic('cad_eletrica_servicos.png', 7)
    table([['Conjunto candidato', 'Proposta e fonte'],
           ['Banco principal', '2 Lithium NG51,2V100Ah em paralelo:200Ah/10,24kWh;74kg, massa estimada publicada.'],
           ['Inversor', 'MultiPlus-II48/5000/70-50 230V:30kg;4000W25°C/3700W40°C.'],
           ['Gestão', 'Lynx Smart BMS NG500A,1,9kg; pré-carga/contator; não substitui fusíveis.'],
           ['Solar e12V', 'MPPT150/35 +100/20; Orion48/12-30; AGM22Ah/5,8kg. MPPTextra só extensão.']], [6, 11])
    para('Manual do inversor recomenda200Ah mínimos, fusível200A e70mm² por polo '
         'até5m. A escolha atende capacidade nominal; não fecha ampacidade, coordenação '
         'de proteção ou corrente de partida. Estimativas de queda/Joule de serviços '
         'constam do JSON; temperatura de entrada não é campo multidimensionalI30.')
    para('Armário lateral seco com anteparo/teto metálicos, acesso removível e reserva '
         'de ventilação100mm no inversor; baterias baixas separadas da água. Gaveta '
         'autoral acima do tanque inspira-se no aproveitamento sob cama da Hymer. '
         'Ventilação ao exterior, fixação/vibração e dutos de A/C ainda precisam de dimensionamento.')
    para('A indução passou para ElectroluxIE3TP220V/60Hz/2000W sobre bancada contínua. '
         'Manual2025p17 distingue2000W220V de1500W127V; loja genérica mistura os valores. '
         'Massa2,3kg220V e dimensões280x358x62mm. Retenção para transporte e ventilação pendentes; '
         'confirmar tensão/frequência de todos os demais aparelhos e configurar o inversor.')
    para(f"Serviços fixos acrescentam{electrical['known_added_service_mass_kg']:.1f}kg conhecidos; "
         f"subtotal atualizado{electrical['new_known_mass_subtotal_kg']:.1f}kg, "
         f"saldo atéPBT{electrical['unallocated_mass_kg']:.1f}kg antes de móveis, quadro, suportes, "
         'cabos/tubos/ferragens/bagagem e itens sem massa publicada. Não massa final/eixos. '
         'ComDoD80%assumido,8,192kWhDC úteis antes de perdas; não energia extra de tração.')
    para('Fontes: fichas/manuais Victron NG,MultiPlus-II,Lynx,MPPT,Orion/catálogoAGM2025; '
         'ElectroluxmanualIE3TP2025; Hymergaveta sob cama. URLs/hashes/datas em '
         'proveniencia_eletrica.json e docs/CAD_TRACAO_E_SERVICOS.md. '
         'Solar→EVSE→carregadorOEM continua não comprovado; não há circuito de tração liberado.')
    page()

    heading('3F. Cabos com isolamento: campo multidimensional I30')
    pic('cabos_campo_e_sensibilidade.png', 7)
    para('Volumes finitos r-theta, feixe e isolamento, resistividade dependente da temperatura '
         'acoplada à solução. Fonte integrada por metro I²R(T), referência de resistência '
         'máxima da ficha RADOX155 STD718404G de25/09/2026. '
         'Cabo120mm²: feixe máximo15,1mm/externo nominal18mm/R20máx0,153ohm/km. '
         'Propriedades térmicas, coeficiente elétrico e filme são hipóteses.')
    table([['Triagem condicionada', 'h [W/m²K]', 'Tmax [°C]'],
           ['1x120mm²; DC569,44A', '10', '178,77 (extrapolação)'],
           ['1x150mm²; DC569,44A', '10', '119,80'],
           ['1x150mm²; DC569,44A', '5', '300,54 (extrapolação)'],
           ['2x120mm²;600A repartidos', '5', '89,45 por cabo']], [8.5, 3.3, 5.2])
    para('DC569,44A deriva de205kW mecânicos/400V/eficiência combinada90% <b>assumida</b>; '
         'não é corrente de fase. Fases300/450/600A são sensibilidades independentes. '
         'Paralelo pressupõe corrente igualmente dividida e resfriamento independente. '
         'A ficha indica150°C/3000h; valores superiores são extrapolações sem material '
         'qualificado. Cabo preto/vermelho não blindado não foi aprovado para substituir OEM.')
    para('Caso assimétrico450A: Tmax104,4249°C;41,26075W/m; variação superficial5,3734K. '
         '512/2048/8192células: mudança final deTmax0,000069K e de amplitude superficial0,004764K; '
         'resíduo1,93e-8W/m. Verificação analítica radial e harmônica2D, ordens1,84–1,86/2,00. '
         'Faltam corrente real/tempo de pico, k do produto, contatos, agrupamento, perdasAC e EMC. '
         'Não é chicote OEM resolvido. Fontes/hipóteses/scripts/hashes: resumo_cabos.json e '
         'docs/CABOS_E_RADIADOR_2D.md.')
    page()

    heading('3G. Radiador cruzado: perfis e capacidade condicionada I35')
    pic('radiador_campos_radiador.png', 7)
    para('Modelo autoral de uma passagem, ambos fluidos não misturados, conservação por célula; '
         'não CFD/geométrico de aletas. Entrada quente80°C, ar25°C; refrigerante0,5kg/s ecp3500J/(kgK), '
         'ar1kg/s ecp1006J/(kgK), UA1000W/K, <b>todos parâmetros de equipamento assumidos</b>. '
         'Capacidade29,5679kW; saídas médias63,1040°C/54,3916°C. Não confundir capacidade sob '
         'entradas fixas com equilíbrio do circuito fechado.')
    table([['Eficiência combinada assumida', 'Perda motor+inversor', 'Margem de capacidade'],
           ['85%', '36,176kW', '-6,609kW'],
           ['90%', '22,778kW', '+6,790kW'],
           ['95%', '10,789kW', '+18,778kW']], [7.5, 4.5, 5])
    para('Perda=P_mec(1/eta-1), com205kW mecânicos de pico. Não atribuir toda perda ao motor; '
         'faltam mapa, duração e partição térmica. Há27combinações independentes deUA/vazões, '
         'que não representam pontos de uma curva real de radiador. O envelope CAD não determinaUA.')
    para('Malhas16²/32²/64²: erros absolutos emefetividade8,05e-5/2,01e-5/5,03e-6 contra integral '
         'independente ht.hx, ordem2; diferença final0,835W e resíduo5,83e-11W. '
         'Apostila pp.31/38-39 fundamenta conservação/epsilon-NUT; ressalva da tabela4 mantida. '
         'Não foi usada sua expressão problemática. Fonte integral: documentação oficial '
         'ht.readthedocs.io/en/stable/ht.hx.html, consulta26/10/2026.')
    para('Faltam UA e perdas de pressão versus vazões reais, curva da bomba/ventilador, fluido, '
         'temperaturas permitidas e ponto hidráulico. A Rheinmetall confirma aplicações daCWA400, '
         'mas comunicado não fornece curva para selecionar a bomba. Dados, hipóteses e hashes em '
         'resumo_radiador.json; item permanece parcial.')
    page()

    heading('3H. Freios: frenagem prescrita e campo r–z I33')
    brakes = json.loads((delivery/'resumo_freios.json').read_text())
    pic('freios_campo_freio.png', 6.5)
    para('Condição oficial: 30 → 10 m/s em 5 s, início 25 °C; desaceleração constante assumida. '
         'Cenário no PBT de 4250 kg: energia translacional de 1,70 MJ e potência média de 340 kW. '
         'Sem regeneração, arrasto/rolamento ou inércias rotativas. Fração dianteira de 70% '
         'e partição disco de 90% são hipóteses; dois discos dianteiros recebem 535,5 kJ cada. '
         'Não é limite superior completo: falta energia rotativa.')
    para('Brembo 09.D018.11 fornece referência de diâmetro de 300 mm e espessura ventilada de 32 mm, '
         'não compatibilidade confirmada com MY25. Modelo autoral: duas placas anulares '
         'de 8 mm, canal de 16 mm, raios de 90–150 mm e contato de 100–145 mm, todos detalhes internos '
         'assumidos. Ferro fundido do artigo ferroviário DOI 10.3390/ma15196821, tabela 2: '
         'rho = 7100 kg/m³, cp = 500 J/(kg K), k = 51 W/(m K), não medidos no produto Brembo. '
         'Robin de 20/50 W/(m² K) assumido; raio interno isolado; sem cubo/aletas/radiação.')
    para(f'Pico superficial reconstruído: {brakes["pico_superficie_k"]-273.15:.2f} °C; '
         f'massa de apenas duas placas: {brakes["massa_duas_placas_kg"]:.3f} kg. '
         f'Energia armazenada: {brakes["energia_armazenada_disco_j"]/1000:.3f} kJ; '
         f'convecção: {brakes["energia_saida_disco_j"]/1000:.3f} kJ. '
         'Não somar massa de freios à tara OEM. Média circunferencial não prevê hot spots '
         'sob pastilhas nem fade, tensões, pinça ou homologação.')
    para('Malhas 12×4 / 24×8 / 48×16 / 96×32; diferença superficial final de 0,0105 K, '
         'máximo de centros celulares ainda difere 1,869 K por resolução da camada próxima '
         'à face. Série analítica axial independente e refinamento temporal documentados '
         'em docs/FREIOS_2D.md. Não declarar independência de todo o campo com base apenas '
         'no máximo superficial. Fontes/hipóteses/hashes em resumo_freios.json; I03/I33 parciais.')
    page()

    heading('4. Aerodinâmica exploratória')
    pic('comparacao_cfd.png', 8)
    table([['Células', 'Iterações', 'Cd exploratório'],
           ['29.527', '108', '0,65303585'], ['63.668', '187', '0,62487678'],
           ['166.212', '179', '0,58066680']], [5.5, 5.5, 6])
    para('Área frontal da superfície reparada: 4,827840 m². Os três solvers convergiram '
         'nos critérios declarados, mas a mudança de Cd nas duas últimas malhas é 7,07%. '
         '<b>Não há independência de malha nem Cd final validado.</b> As malhas não formam '
         'uma sequência uniforme apta a uma extrapolação de Richardson direta.')
    para('OpenFOAM 2412, SST k-omega, velocidade 22,222 m/s, rho 1,1 kg/m³ e nu '
         '1,7e-5 m²/s assumidos no piloto. Solo móvel e rodas fixas. Não inclui módulos '
         'fotovoltaicos como geometria externa. Camadas de parede/y+ e rodas girantes '
         'não estão resolvidos. Casos com camadas divergiram e foram rejeitados.')
    para('Superfície original visual aberta: área projetada 5,004665 m²; após reparo '
         '4,827840 m², diferença de -3,53%. Fechamento por componente não garante '
         'fidelidade física nem ausência de auto-interseções. Não combinar estes resultados '
         'com a roda candidata nova sem nova geometria e ensaio.')
    para('A cobertura solar e os suportes novos não integraram estes pilotos; '
         'não reutilizar o Cd exploratório como coeficiente validado da carroceria equipada.')
    page()

    heading('5. Referência JA e consumo histórico')
    pic('solar_proposta.png', 8)
    para('JA Solar JAM54D41-450/LB/1500V: 450 W STC, 22 kg, 1,762 x 1,134 m; '
         'coeficiente térmico -0,003/K. Plano horizontal, pvlib 0.16.1, Ineichen e '
         'climatologia Linke; Faiman U0=25 e U1=6,84 assumidos. Sem ganho bifacial '
         'nem sombra modelada. Perdas adicionais 10% e conversão 95% assumidas.')
    rows = [['Módulos', 'Potência STC', 'Energia após perdas assumidas']]
    for count, row in solar['arrays'].items():
        rows.append([count, f"{row['p_stc_array_w']:.0f} W", f"{row['terminal_energy_assumed_kwh']:.4f} kWh/dia"])
    table(rows, [4, 5, 8])
    para('Esses valores não comprovam energia acessível ao pack de tração. Um MPPT de '
         '48 V não pode ser ligado diretamente ao pack de 400 V. Falta arquitetura de '
         'serviços, armazenamento intermediário/conversão e autorização de carga OEM. '
         'Os cenários energéticos atuais bloqueiam geração aproveitada durante a condução.')
    para('Nos 324 cenários de sensibilidade, a 40 km/h: 3,25 a 5,78 km/kWh; a 80 km/h: '
         '1,97 a 3,03 km/kWh. Com dois módulos, solar-only 10,5 a 18,7 km a 40 km/h e '
         '6,4 a 9,8 km a 80 km/h. Não são intervalos medidos: variam Cd dos pilotos, '
         'Cr=0,008/0,012/0,016 e rendimento=0,85/0,90/0,95 assumidos, a massa de 4250 kg '
         'e auxiliares de condução de 800 W. Sem consumo completo de habitação.')
    para('Esses cenários e as agendas seguintes são a referência histórica de dois '
         'módulos/100 W estacionado. A expansão e os equipamentos novos estão nas '
         'seções3A-3C; falta integrar os barramentos e refazer aerodinâmica/demanda para uma missão atualizada.')
    page()

    heading('6. Agendas e missão de 7.000 km')
    pic('agenda_i27.png', 7.5)
    para('I27: 335 km no cenário condicionado, grade temporal de 30 minutos e conjunto '
         'discreto de velocidades, SOC100% para exatamente30%. Este resultado é ótimo '
         'na grade e nas hipóteses, não no veículo físico. A curva exportada representa '
         'potência nos terminais; ainda falta a potência mecânica instantânea do motor '
         'e modelagem de acelerações. O limite de oito horas não foi imposto a I27.')
    para('I29: o minimizador de tempo foi verificado em casos analíticos e inclui chegada '
         'fracionária, causalidade energética e oito horas por dia local. A agenda '
         'construtiva de 7.000 km foi verificada separadamente: 1621,77 dias, 1622 datas, '
         'SOC final de 12,94% e resíduo energético de -0,00186 J. <b>Não é mínimo global '
         'nem previsão da rota.</b> Repete o sol de São Carlos em 21/06 para todo dia e '
         'ano, a 20 km/h noturnos, com apenas100 W estacionado e reserva adicional.')
    para('O limite inferior otimista de171 dias considera apenas rolamento, bateria inicial '
         'e geração solar repetida; ignora arrasto, auxiliares e perdas e não certifica '
         'o ótimo físico. A missão requer modelo solar sazonal/geográfico, perfis '
         'de habitação e componentes reais antes de uma conclusão de viabilidade.')
    para('A carga de HVAC calculada nesta revisão é da ordem de1 kW elétrico sob COP '
         'assumido2,5, muito acima dos100 W usados quando estacionado na agenda anterior. '
         'Não apresentar a agenda anterior como cenário de habitação com climatização.')
    page()

    heading('7. Cabine e seleção preliminar de A/C')
    pic('cabine_termica.png', 10)
    table([['Saída condicionada', 'Resultado'],
           ['I31, sem ocupantes e sem A/C, meio-dia', f"{n['i31_noon_c']:.3f} °C"],
           ['Pico I31', f"{n['i31_peak_c']:.3f} °C às 14:07"],
           ['I32, exterior33°C / interior25°C, uma pessoa', f"{n['i32'][0]['cooling_required_w']:.1f} W de frio"],
           ['I32, duas pessoas', f"{n['i32'][1]['cooling_required_w']:.1f} W de frio"],
           ['Eletricidade, COP2,5 assumido, uma pessoa', f"{n['i32'][0]['electrical_w_by_assumed_cop']['2.5']:.1f} W"]], [11, 6])
    para('Estas são estimativas de uma zona térmica equivalente com parâmetros propostos, '
         'não medições da van. A área de vidro, extensão dianteira, capacidade térmica '
         'e filmes precisam ser obtidos/revistos. Sem ocupação, ventilação ou equipamentos '
         'em I31; I32 é permanente e contém ventilação/ocupante/equipamentos explícitos.')
    page()

    heading('8. Método térmico e decisões resultantes')
    para('Isolamento: Armacell AF/ArmaFlex32 mm, k40°C=0,03828 W/(m K); '
         'revestimento6 mm/k0,13 assumido. Resistências de Fourier/Newton em série '
         'levam a U opaco0,7460 W/(m² K). UA total65,4366 W/K inclui vidros e '
         'pontes térmicas assumidos. A fonte do fabricante não comprova a adequação automotiva.')
    para('Solar: parede opaca por temperatura sol-ar Ta+alfa I/ho e vidro por fator solar '
         'gAI. A parcela de vidro é retirada da área opaca. Irradiação de cada parede '
         'calculada por pvlib, com albedo0,2; piso sem sol e sem crédito de sombra PV. '
         'Filme externo combinado8 W/(m² K) incorpora convecção natural e radiação '
         'linearizada para meio na temperatura ambiente; não há radiação duplicada.')
    para('I31: C dT/dt = Qsolar - UA(T-Ta), C=200 kJ/K assumido, início06:00 em25°C. '
         'Integração exponencial por intervalo. A constante C/UA é0,849 h e o resíduo '
         'de energia é6,03e-9 J. A diferença do resultado ao meio-dia entre passos1/5 min '
         'é0,00081 K. Isso verifica a integração, mas não a capacidade térmica assumida. '
         'Equilíbrio com sol congelado ao meio-dia48,767°C; a curva transiente tem pico '
         'mais tarde, de modo que não se adotou regime permanente ao longo do dia.')
    para('I32: sensível por condução, ganhos solares,100 W de equipamentos e75 W/pessoa; '
         'latente55 W/pessoa, valores assumidos. Ventilação30 m³/h e UR50% dentro/fora. '
         'Pressão91,419 kPa pela altitude; razão de umidade0,017606/0,010968 kg/kg. '
         'Buck Research CR-2 (2009), com EF=1 aproximado. Ventilação sensível70,06 W '
         'e latente137,10 W. Não simula umidade acumulada da cabine.')
    sensitiv = cabin['sensitivity']
    low = min(row['i32'][0]['cooling_required_w'] for row in sensitiv)
    high = max(row['i32'][0]['cooling_required_w'] for row in sensitiv)
    para(f'Sensibilidade em48 combinações de orientação/absorptância/fator solar/C: '
         f'carga I32 para uma pessoa de{low/1000:.2f} a{high/1000:.2f} kW. '
         'São alternativas de parâmetros, não intervalo estatístico. Alterar C '
         'afeta I31, mas não o balanço permanente de I32.')
    para('O candidato atual é FreshWell3000 sob cama:2700W nominais de frio e230V/50-60Hz; '
         'a ficha não fornece COP verificado no ponto de33°C. A carga condicionada para duas '
         'pessoas2645,9W deixa apenas54,1W de margem nominal, aproximadamente2%. '
         'Não demonstra atendimento real com dutos/retorno/condensador e tolerâncias. '
         'FJX4 2200 foi descartado por capacidade insuficiente; FJX7 3000 é alternativa '
         'histórica não instalada. Três horas da carga de uma pessoa/COP2,5 assumido '
         'consumiriam3,019kWh antes de perdas do inversor; não é simulação diária de HVAC.')
    page()

    heading('9. Situação dos 35 itens')
    para('Matriz gerada da revisão local. Nenhum item foi aprovado. “Parcial” significa '
         'evidência utilizável com lacunas, e não conclusão do requisito completo.')
    text = (root/'docs/REVISAO_35_ITENS.md').read_text()
    rows = [['Item / dono', 'Evidência atual', 'Necessário para fechar']]
    for line in text.splitlines():
        if re.match(r'\| \d{2} / P\d', line):
            cols = [x.strip() for x in line.strip('|').split('|')]
            rows.append([cols[0]+' - '+cols[1], cols[2], cols[4]])
    if len(rows) != 36:
        raise ValueError(f'Matriz deve conter35 itens, encontrou{len(rows)-1}')
    table(rows, [4.2, 6.3, 6.5])
    page()

    heading('10. Reprodução e trabalho que permanece')
    para('Executar na worktree motorhome_solar_codex_tarefas. Dependências científicas '
         'na .venv; NumPy1.26.4, pvlib0.16.1, OpenFOAM2412 e visualizadorThree0.180.0. '
         'O ambiente de testes precisa de PYTHONPATH=src. Não carregar os arquivos '
         'brutos do cache no contexto de uma conversa.')
    for command in [
            'PYTHONPATH=src .venv/bin/python -m pytest -q',
            '.venv/bin/python scripts/verificar_estrutura.py',
            '.venv/bin/python scripts/calcular_cabine.py --destino /tmp/cabine-reproducao',
            '.venv/bin/python scripts/gerar_memorial_revisao.py --destino /tmp/memorial-reproducao.pdf']:
        para(escape(command), 'Small')
    para('Prioridades de execução', 'Heading2')
    for item in [
            '1. Especificar equipamentos reais, componentes de tração e serviço, massas, posições e custos. Resolver solar-serviços-carga OEM estacionado, sem ligar48 V diretamente ao pack400 V.',
            '2. Integrar interior, roda, isolamento e HVAC em CAD; concluir vistas cotadas, aberturas, manutenção e ergonomia. Medir áreas/vidros para substituir a caixa térmica equivalente.',
            '3. Resolver a superfície CFD, camadas/y+, rodas e independência de malha. Atualizar Cd/área/massa/Cr e integrar mapa motor/transmissão, vmax e0-100.',
            '4. Fechar dados reais I30-I35: cabo polar e radiador cruzado já calculados sob hipóteses; obter correntes/materiais/contornos, disco/pastilha, perdas pack/motor e curvas de bomba/radiador. Métodos condicionados não são casos físicos finais.',
            '5. Atualizar geração e cargas reais, otimizar I27/I29, revisar energia causal e grade; concluir memorial final, revisão cruzada e apresentações. Vídeo requer participação dos integrantes.']:
        para(item)
    para('Fontes e documentos locais', 'Heading2')
    refs = [
        ('Enunciado original2026 e apostila SEM0571/2025', 'Textos locais consultados por seção; originais preservados fora do pacote.'),
        ('Fiat E-Ducato MY25, ficha SK20/03/2026', 'https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf'),
        ('JA Solar, ficha450W p.2', 'https://www.jasolar.com/uploadfile/2024/0112/20240112034704258.pdf'),
        ('INMET cadastro estações', 'https://apitempo.inmet.gov.br/estacoes/T'),
        ('Continental especificações', 'https://continentaltire.com/tires/vancontact-as/specs'),
        ('Armacell AF/ArmaFlex, consulta25/10/2026', 'https://www.armacell.com/en-DE/product/technical-specs/afarmaflex'),
        ('Dometic FJX4 2200 / FJX7 3000, consulta25/10/2026', 'URLs completas em config/cabine_proposta.yaml e fontes_externas/catalogo.csv.'),
        ('Buck Research CR-2 manual2009, p.20', 'https://www.hygrometers.com/wp-content/uploads/CR-2-users-manual-2009-12.pdf'),
        ('CAD OpenX, licenças e alterações', 'entregas/parcial_2026-10-24/ATTRIBUTION.txt; docs/CAD_ONLINE_E_VISUALIZACAO.md'),
        ('Métodos, dados e hipóteses completos', 'docs/CABINE_E_HVAC.md; docs/PNEUS_E_MASSA.md; docs/ENERGIA_E_OTIMIZACAO.md; docs/FRENTE_TERMICA.md'),
    ]
    for title, url in refs:
        para(escape(title)+': '+escape(url), 'Small')
    date = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M %Z')

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#b6c9cc'))
        canvas.line(1.8*cm, 1.6*cm, 19.2*cm, 1.6*cm)
        canvas.setFont('DejaVu', 7)
        canvas.setFillColor(colors.HexColor('#55666b'))
        canvas.drawString(1.8*cm, 1.2*cm, 'Aurora Solar | revisão parcial - não aprovada | '+date)
        canvas.drawRightString(19.2*cm, 1.2*cm, str(doc.page))
        canvas.restoreState()

    args.destino.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(args.destino), pagesize=(21*cm, 29.7*cm),
                            rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm,
                            bottomMargin=2*cm, title='Aurora Solar - memorial de revisão parcial',
                            author='Projeto acadêmico motorhome - frente de integração',
                            pageCompression=1)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f'{args.destino}: {args.destino.stat().st_size} bytes')


if __name__ == '__main__':
    main()
