> Estado atual: [execução técnica02](EXECUCAO_TECNICA02.md), fonte1.1.0-execucao02. O baseline pósDEC061 abaixo permanece histórico; etapa técnica completa ainda aberta.

# Estado pós-DEC061

Registro original: [61 decisões](decisoes_motorhome_2026-10-28.md). Fonte ativa: `config/parametros_globais.yaml`. Veja [integração atual](INTEGRACAO_POS_DEC061.md), [matriz61](MATRIZ_DECISOES_61.md), [35itens](REVISAO_35_ITENS.md) e [aprovações consolidadas](APROVACOES_FINAIS_PENDENTES.md). ArquiteturaB escolhida; interfaceDC não demonstrada. Nenhum resultado anterior transforma recarga via serviços48V em caminho permitido.

# Contexto central — enviar ao chat geral de agentes

## Missão
Projetar, especificar, avaliar e simular um **motorhome elétrico solar** para **ao menos duas pessoas**, buscando autonomia energética. São **35 itens** no enunciado (leia PDF original). Apresentação e entrega em 02/12/2026, até 06:00 (horário local do projeto).

## Condições ambientais oficiais
- São Carlos, SP: usar coordenadas e altitude identificadas e citadas; não inferir sem registrar fonte.
- Data: 21 de junho, incidência solar com **céu limpo**.
- T ambiente = **25°C** quando o item não especificar outra temperatura.
- Umidade relativa = **50%**.
- Velocidade do vento = **0 m/s**.
- Item 32: exterior 33°C, interior 25°C, ao meio-dia, com passageiro, regime permanente.
- Item 33: 30 m/s → 10 m/s em 5 s; T inicial = 25°C.
- Item 34: carga em 20 kW e em 80 kW.
- Item 25: somente eletricidade solar gerada naquele dia, 40 e 80 km/h; curva de autonomia versus velocidade.
- Item 26: km/kWh na bateria a 40 e 80 km/h.
- Item 27: SOC final 30%; explicitar SOC inicial e perfil de velocidades/potência.
- Item 29: 7000 km Belém–Chuí, máximo 8h dirigindo/dia, apenas carga inicial e energia solar (sem recargas externas).

## Entregas oficiais
Memorial de cálculo com referências, especificações, gráficos, simulações, geometria CAD e vistas cotadas, resumo de resultados, anexos de códigos, relatório PDF (<20MB), seminário de até 8 min (apresentador escolhido no dia) e vídeo de 8 a 10 min com todos os membros aparecendo e tempos semelhantes (<50MB). Envio por e-mail a ambos docentes até 6h de 02/12. Confirmação de grupo de 7 vs 10 ainda pendente.

## Divisão oficial deste kit (prevalece sobre mensagens antigas)
- P1: 1, 2, 3, 14, 15, 18, 24, 33 — Estrutura, freios, massa e custo.
- P2: 6, 7, 9, 23, 30 — Bateria, elétrica, cabos.
- P3: 16, 17, 19 — Carroceria, CAD, CFD.
- P4: 4, 5, 20, 21, 22, 28 — Motor, transmissão, dinâmica.
- P5: 8, 25, 26, 27, 29 — Solar, autonomia e otimização.
- P6: 11, 13, 31, 32 — Interior e conforto térmico.
- P7: 10, 12, 34, 35 — Arrefecimento e térmica da bateria.

## Reuso de fontes encontradas
Fontes iniciais em `fontes_externas/catalogo.csv`. CAD Delica Brad Mitchell oferece link para ZIP FreeCAD/STEP/IGES/STL, mas download interno não validado; adequado sobretudo ao interior. Fiat Ducato L3H2 foi indexado no 3D Warehouse, mas acesso automático retornou 403. Outros: Stella Vita (referência), MELVING22 (SolidWorks/IGS do solar car, sem licença explícita), pvlib (solar), Electric Vehicle Simscape (BEV), FASTSim e EV_sim (dinâmica), PyBaMM e BatteryPack (baterias), autocfd (CFD), brake-thermal-simulation (freios). Cada fonte exige checagem e respeito à licença.

## Princípios de projeto
Um único cenário e configuração aprovada; reprodutibilidade; separação por item; parâmetros compartilhados com interfaces claras; revisões em marcos; origem e licença de cada material externo; agentes nunca declarar 'feito' sem artefato inspecionável e validação humana.

## PDFs de referência
`docs/fontes_recebidas/Projeto Sist. Térmicos e Fluídicos 2026.pdf` (enunciado), `Organizacao_Motorhome_P1_P7.pdf` (divisão/cronograma), `Projetos prontos, CADs e códigos reutilizáveis para o motorhome elétrico solar.pdf` (levantamento anterior).
