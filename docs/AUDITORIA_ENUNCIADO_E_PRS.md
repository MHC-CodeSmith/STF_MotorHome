# Conferência do enunciado, de todos os PRs e da versão enxuta

Revisão de 25/11/2026, após o usuário rejeitar o PDF de 85 páginas e pedir redação
próxima à do Cuca, inclusive frases, sem código no PDF. Esta matriz substitui a
conclusão anterior de que conferir apenas o PR #9 bastava para fechar a entrega.

Fontes conferidas: enunciado `docs/fontes_recebidas/Projeto Sist. Térmicos e Fluídicos
2026.pdf`; PRs #1, #2, #4, #5, #6, #8 e #9 (descrição, commits, arquivos, reviews,
comentários gerais e de linha); issues #3 e #7; parecer P6 registrado no guia.
Todos esses PRs estão mesclados. Isso não é usado como prova de que o texto está correto.

As diffs de #1 e #8 excedem o limite da API do GitHub; foram conferidos os commits e
arquivos locais correspondentes. Os dois commits de #8 importam: a descrição do PR
precede a mudança efetiva para 0,38 kW. Números antigos dos pareceres são históricos;
a cama mudou a massa e os resultados dependentes foram reexecutados.

## Correções por PR e parecer

| Fonte | Cobertura na revisão atual |
|---|---|
| #1 — integração original | Preservados cenário, dois bancos, geometria, 35 itens, conservação e verificações de CAD. 1540/1350 são históricos; 1560 é o cenário vigente. As buscas antigas não substituem o fechamento com primeira saída física. |
| #2/P7 — obrigatória 1 | Figura I35 corresponde ao equilíbrio de 0,557 kg/s e 22,9 kW, conferida com o arquivo do P7. |
| #2/P7 — obrigatória 2 | Referência Bosch 039202453G com URL completo da ficha. |
| #2/P7 — obrigatória 3 | I10 inclui os 96 W da bomba; 90% é hipótese conservadora. I12 explicita 15,2–17,5 kW com motor95%/inversor97–98%. |
| #2/P7 — obrigatória 4 | I12 não atribui rejeição sustentada à convecção isolada do redutor; a carga adicional é separada no I35. |
| #2/P7 — obrigatória 5 | I34 usa 486 casos incluindo R e entropia, nominal dU/dT=0, três cortes a45°C; não apenas a antiga varredura parcial. |
| #2/P7 — obrigatória 6 | Texto e figuras usam “fluido de arrefecimento”. |
| #2/P7 — recomendada 7 | Tabela compacta de bomba, radiador, ventilador, MEG, mangueiras, vaso e circuito da bateria. Ventilação48V recalculada:444W e145m³/h aΔT10K. Cotas/volumes OEM ausentes são identificados, não inventados. |
| #2/P7 — recomendada 8 | Tabela de lubrificantes típicos e perdas de motor/inversor/redutor; viscosidade/volume exatos dependem de VIN. |
| #2/P7 — recomendada 9 | Meta65°C explicitada: UA1000 resulta66,8°C e não atende; mínimo calculado1093W/K. Se o redutor compartilhar o circuito,29,02kW exigem1952W/K. Carga140kW nas rodas distinguida do pico205kW. |
| #2/P7 — recomendada 10 | Δp de componentes reexecutado:48,5kPa/68%; vazões31,9→26,4→23,1L/min. NPSHa2,6/12,3m sob hipóteses explícitas, sem afirmar margem porque NPSHr não foi publicado. |
| #2/P7 — recomendada 11 | Extremos reexecutados: parada45°C em0,66/0,37h ao iniciar25/35°C. Calor interno máximo6,35kW; a sugestão3–5kW não garante o extremo. Critério instantâneo conservador:capacidade≥6,35kW e UA bateria–fluido≥318W/K para45/25°C. Não se afirma que um chiller foi instalado. |
| #2/P7 — interfaces/A14/A15 | Tabela de limites, hipóteses de R/entropia/UA, distinção FreshWell/circuitoOEM, massa dentro da tara e reservas, carga do redutor e redução de potência por temperatura. Integração física/limitesOEM continuam não demonstrados. |
| #4/P3 | Janela S4 com material/cotas/massa, claraboia rejeitada por288<390mm, passagens, parede/vidro/UA; banco sob cama a0,863m; áreas4,8954/4,82784m² e CdA; faixa oscilatória sem “incerteza1%”. |
| #5/P2 | Mantidos contornos reais assumidos,382/489A,158°C em120mm²,185mm² como requisito derivado, pico transitório; faltas10–40mΩ com2,75–16,05kA eBMS; capacidade útil/nominal; eficiência98% do150/60; código sem hardcode de energia e serialização coerente. |
| #5 — pendência software35A | Corrigido `comparar_teto_maxeon.py`: triagem usa60A, inclusive no teto isolado; corrente quente dos portáteis continua desconhecida. Sem aprovação automática do arranjo compartilhado. Verificador confere essa condição. |
| #5 — duas sensibilidadesI34 | Fonte vigente identificada no README do item:486casos do1560. O CSV antigo20linhas fica histórico, com finalidade e escopo diferentes, sem duas fontes concorrentes do mesmo resultado. |
| #5 — energia112,4kWh | Explicada soma98úteis+14,4nominais; reservas20/30% de serviços já impedem usar95%DoD. Nenhuma energia adicional foi criada. |
| #5 — limites físicos | BitolaOEM, ampacidade, curvasI²t e validação dos contornos permanecem pendências reais; não são falhas de software resolvidas por um teste verde. |
| #6/P4 | Raios0,372/0,361m separados; aceleração com transferência dianteira e sem inércia rotacional; Cr0,012 como hipótese conservadora, rótuloC2 apenas no limite inferior. Sensibilidade do raio reexecutada com massa nova. |
| #8/P2 — ambos os commits | Mínimo de saída comumI25/I29; equivalênciaPmin/eta na entrada;0,38kW=1A×380V como hipótese. Não atribuído ao Sungrow nem apresentado como carregador compatível demonstrado. |
| #9/P5 | Matriz integral dos27pedidos e subpedidos em `AUDITORIA_PR9_REESCRITA.md`. No PDF enxuto permanecem geração, portáteis, dimensões, retenção, inclinação, perfis, comparações, quatro fluxogramas, mapa, cama, dinâmica e fórmulas térmicas. |
| Issue#7/P1 | Ficha norte-americana/pressões/estepe; referênciaBrembo e hipótese70/30; eixos atualizados/margemPBT/limitesOEM; caso0,99 e massa bruta33,1kg; custo inclui cortina/montagem; freios com malha96×32,Δ0,026K,ensaio108km/h e regeneração hipotética. |
| P6/Amanda | Déficit sem cortina preservado; solução com cortina é hipótese identificada, com casos1/2pessoas e30/62m³/h. Parecer antigo não é nova aprovação da solução. |

## Enunciado: 35 itens e evidência no PDF

A numeração I01–I35 abaixo é a do enunciado; os títulos do PDF seguem a organização do
Cuca. “Apresentado” significa que existe resposta técnica, não confirmação de peça OEM.

| Item | Evidência / limite |
|---|---|
|01|Nome Aurora Solar, variante E-Ducato, duas pessoas e imagem externa.|
|02|Pneus/rodas, pressões, quantidade, diâmetro, massa e capacidade; etiqueta elétrica/estepe não confirmados.|
|03|Freios, material/propriedades, dimensões/placas, ABS e regeneração; pinças/conjunto traseiro exatos sem VIN.|
|04|Potência/torque/RPM e curvas de eficiência/torque/potência; mapa é modelo assumido.|
|05|Redutor fixo, diferencial e perdas; relação real/massa individual OEM não publicadas.|
|06|Tração 110/98 kWh e serviços com três US5000; tipo, tensão, dimensões, massa e33h.|
|07|Circuitos HV/48V/12V/CA, seções, material, fusíveis, rotas e faltas; comprimento real eI²t exigem detalhamento.|
|08|Área, eficiência, tecnologia, dimensões, massa, quantidade, geração horária e alternativas.|
|09|MPPT/inversor, eficiências, massa, dimensões, fluxograma e mínimo CC; cotas conferidas no manual oficial.|
|10|Circuitos térmicos, tabela de componentes e ventilação48V; várias cotas/volumes mantidos OEM sem desmembramento.|
|11|FreshWell frio/calor, dimensões, massa, ventilação e vazão de CO2; capacidade33/25°C não demonstrada.|
|12|Aplicações, tabela de lubrificantes típicos e perdas; produto/volume exatos do VIN desconhecidos.|
|13|Móveis, cama, banheiro, eletrônicos, indução, geladeira, lava/seca; tabela de dimensões e consumo por aparelho/perfil.|
|14|Suspensão/direção OEM, cargas e estimativa geométrica; cotas, massas e limites individuais não publicados.|
|15|Chassi/cotas, chapas, caso governante e massas; ancoragens OEM não comprovadas.|
|16|Carroceria, portas/janela/vidros, material, aberturas, passagens e resistência térmica.|
|17|Geometria3D, vistas cotadas, layout e corte; montagem por envelopes, não desenho de fabricação.|
|18|Massa4042,8kg incluindo ocupantes, cama, água/bagagem; inventário, CG, eixos e margem.|
|19|CFD, Cd, área, malhas, campos e comparação sem deck; limite de validação eGCI explícitos.|
|20|Cr e justificativa, faixa e força; hipótese sem ensaio.|
|21|Curvas de forças aerodinâmica/rolamento com velocidade.|
|22|Curvas de potência resistiva/demanda e envelope disponível.|
|23|Capacidades nominal/útil, bases de SOC e reservas separadas.|
|24|Tabela por componente, R$, impostos/faixas; inclui montagem identificada.|
|25|40/80km/h só solar, gráfico, balanços e serviços; interface condicional.|
|26|40/80km/h em km/kWh e kWh/km, curva e conversão SI.|
|27|SOC final30%, velocidade e potência instantânea; comparação24h/8h.|
|28|Velocidade limitada90, 0–90 e0–100 teórico, curva, raio eRPM; não é0–100 real da versão limitada.|
|29|7000km, carga inicial+solar, sem rede, até8h/dia, velocidade/partida, comparação eSOCs. Repete o dia claro e pista plana; não simula relevo/clima real do litoral.|
|30|Corrente no pico, curvaT×bitola e campo multidimensionalT(x,y) no pico; contorno uniforme produz simetria radial, não falsa assimetria.|
|31|Cabine fechada, aquecimento desde6h, resultado ao meio-dia, campo CFD e verificação.|
|32|Carga33→25°C, regime, passageiro(s), COP e cortina; casos de uma e duas pessoas.|
|33|30→10m/s em5s, T inicial25°C, campo multidimensional e histórico.|
|34|Cargas20/80kW, temperatura/SOC, histórico, sensibilidade e corte térmico.|
|35|Bomba/ponto, curva, perfis dos fluidos, vazão, calor e redimensionamento/limites.|

## Entregáveis gerais e instruções que prevalecem

- Introdução breve, objetivos, revisão bibliográfica, memorial, figuras e resumo final: no PDF.
- Céu claro21/06, SãoCarlos/altitude,25°C,UR50%,vento0: entradas declaradas; exceção33°C doI32 preservada.
- PDF abaixo20MB: conferido após compilar; o total de páginas é registrado no README do relatório.
- **Código no anexo:** pedido pelo enunciado original, retirado do PDF por instrução expressa mais recente do usuário. Arquivos permanecem no repositório. Não afirmar cumprimento literal desse requisito.
- **Vídeo:** pedido original, fora do escopo por instrução expressa do usuário. Não produzido.
- **Grupo de10:** capa usa os oito nomes fornecidos; não se presume autorização docente para a diferença.
- Seminário de até8min e envio por e-mail até02/12às6h: atividades externas ainda não realizadas. Não são concluídas por gerar o PDF.

A cobertura técnica é ampla, mas não significa que todos os dados de catálogo, permissões
acadêmicas ou interfaces físicas estejam demonstrados. As lacunas explícitas acima evitam
confundir resultado de cálculo com informação publicada ou ensaio. Permanecem perguntas
objetivas para o professor em `PERGUNTAS_TERMICAS_PROFESSOR.md`.

## Verificação da versão publicada

PDF de 39 páginas, 6.027.541 bytes (6,03 MB), fonte de 12 pt e 33 figuras/diagramas.
Os 35 itens aparecem na ordem; não há listagens nem anexo de código; citações e
referências estão resolvidas, sem avisos de LaTeX na passagem final.

Suite local: 298 testes aprovados, com oito avisos de depreciação da dependência pvlib.
Ruff, verificação estrutural e os dois verificadores de manifesto em modo de leitura
aprovados. A auditoria de estrutura também expõe os parâmetros OEM não publicados
e a ausência de aprovação final de engenharia; testes não alteram essa condição.
Configuração preservada: SHA-256 `047c725c8f26f5dbf4c824aaffeb92d09272f12a4e5e181e5e059c5eb3a4396b`.
