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
    para('Reserva total OEM: 4250 - 2790 = 1460 kg. Descontando dois módulos JA de '
         '44 kg, duas pessoas de 75 kg e 100 kg de água assumidos, restam 1166 kg '
         'para conversão, serviços e bagagens. Não equivale à massa montada: é preciso '
         'BOM sem duplicações, posições de massas e verificação de limites por eixo. '
         'Custos em R$ com impostos ainda não foram consolidados.')
    page()

    heading('3. CAD e ocupação')
    pic('layout_proposto.png', 9)
    para('A carroceria foi estendida nas regiões de carga/teto para comprimento 5,998 m, '
         'entre-eixos 4,035 m e topo 2,612 m. Rodas deslocadas rigidamente, preservando '
         'tamanho original. Não é uma reprodução certificada da variante elétrica.')
    table([['Reserva interna', 'Dimensões e restrições'],
           ['Cama para duas pessoas', '1,35 x 1,87 m antes de acabamentos; altura 0,65 m.'],
           ['Cozinha', '1,40 x 0,60 x 0,90 m; equipamentos reais ainda não selecionados.'],
           ['Banheiro', '0,90 x 0,76 x 1,80 m; reduzido após interferência com teto curvo.'],
           ['Dinette', '0,90 x 0,80 x 0,80 m; mesa rebatível e reserva de assento.'],
           ['Painéis no teto', 'Dois módulos 1,134 x 1,762 m; suportes e abertura HVAC por revisar.']], [5, 12])
    para('A triagem do topo do banheiro usou 81 raios e folga mínima externa de 33 mm. '
         'Não considera espessura/isolamento, caixas de roda, ergonomia ou colisão completa. '
         'O piso Z=0,68 m e a traseira X=-3,35 m são alinhamentos assumidos.')
    para('visualizador.html contém a carroceria GLB e reservas internas, funciona offline '
         'e permite inspeção de vistas. É visualizador, não editor CAD paramétrico. '
         'Onshape e Fusion foram pesquisados em documentação oficial; não houve upload '
         'a serviços públicos. Onshape gratuito implica documentos públicos/não comerciais. '
         'O exterior OpenX preserva MPL-2.0 e CC-BY-4.0 com atribuição na entrega.')
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
    page()

    heading('5. Geração e consumo')
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
    para('FJX4 2200: catálogo oficial2200 W, abaixo de2516/2646 W calculados. '
         'FJX7 3000: candidato oficial3000 W com compressor inverter/bomba de calor, '
         'a revisar. A capacidade e o COP em33°C, alimentação e montagem ainda faltam; '
         'não se conclui atendimento de todos os casos. Três horas de carga nominal '
         'de meio-dia com COP2,5 consumiriam3,019 kWh antes do inversor, comparáveis '
         'aos3,233 kWh/dia solares de dois módulos. Não é simulação diária de HVAC.')
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
            '4. Executar I30-I35 com componentes reais: cabo isolado, disco/pastilha, perdas de pack e motor, refrigerante, bomba/radiador e curvas. Métodos genéricos não são casos físicos finais.',
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
