# Dez trabalhos iniciais — ordem e interfaces

Plano de coordenação em 22/10/2026. P1–P7 mantêm a divisão do PDF de organização (pp. 1, 3–6). Só um worker executou esta auditoria; as frentes paralelas abaixo são trabalho **da equipe**, ainda não executado. A ordenação indica prioridade de abertura, sem impor espera serial para métodos independentes.

| Ordem / prazo 2026 | Dono / apoio e revisor proposto | Trabalho e artefato verificável | Critério de verificação / gate humano |
|---|---|---|---|
| 1 — M0 23/10 | P1 coordena; todos P1–P7 | Registro de requisitos e respostas docentes: 7×10, identidade P1–P7, disponibilidade, SOC inicial I27, regime I31, ocupantes I32, cenário solar da rota I29 | Ata com autor/data e resposta explícita; só docentes/equipe resolvem ambiguidades. Nenhum valor preenchido nesta auditoria |
| 2 — M0 23/10, M1 30/10 | P1/P3/P6; revisão P3/P1 | Matriz comparativa de conceito/envelope, chassi e layout; evidências CAD do cache e relatório de abertura nativa | Equipe aprova veículo-base; P3 verifica unidades/cotas/referências da montagem. ZIP/assinatura não equivalem a CAD aberto; sem licença, usar referência ou obter autorização |
| 3 — M1 30/10 | P4/P2; revisão P6/P7 | Dossiês candidatos de motor/transmissão/bateria/eletrônica: curvas torque/eficiência, tensão, limites e dados térmicos | Fichas reais com unidade, URL e versão; revisão de compatibilidade antes da seleção. Entregar `motor_curves.csv` e `electrical_limits.yaml` quando houver dados, sem valores demonstrativos travestidos de finais |
| 4 — M1 30/10 | P3; entradas P1/P6/P5; revisor P1 | Frente CAD/CFD: método executável de simplificação/malha, vistas cotadas, `vehicle_geometry.yaml`, depois `drag_cfd.csv` | Até 30/10 provar acesso ao solver e execução de caso de verificação; até M2 06/11 primeiro Cd provisório com área, domínio, contornos, resíduos e estudo de malha. Aceite humano antes de Cd final |
| 5 — M1 30/10 | Todos enviam; P1 consolida; P2 confere especificações | `mass_breakdown.csv` e `bill_of_materials.csv` por componente, incluindo I07/I10, passageiros/água/bagagem e impostos documentados | Totais reproduzíveis sem dupla contagem (geometria I17 não é massa adicional à carroceria); cada parcela com dono/fonte/data; atualizar em 13 e 20/11 |
| 6 — M1 30/10, M2 06/11 | P1 I33/P2 I30; revisores P3/P7; P4 fornece condições | Frente térmica independente: equações/contornos de cabo e disco, geradores de malha, testes sintéticos rotulados e plano de estabilidade/convergência | Não aguardar I28 para estudar frenagem prescrita; aresta final I28→I33 fica em revisão. Exigir campos 2D/3D, balanço de energia e malha/tempo; código sem licença só referência, não incorporação |
| 7 — M1 30/10, M2 06/11 | P7; dados P2/P4; revisor P2 | Frente térmica bateria/arrefecimento: `battery_charge_temperature.csv`, `cooling_loop.csv`, curva de bomba e perfis de radiador, após parametrização | Primeiro validar método com caso de referência; em M3 13/11 comparar cargas 20/80 kW e interseção bomba/sistema com dados reais. Não selecionar bomba nem fluido nesta auditoria |
| 8 — M1 30/10, M2 06/11 | P6; entradas P3/P5; revisor P5 | Frente cabine: `cabin_surfaces.csv`, `aux_load_profile.csv`, balanços separados I31/I32 e minuta de relatório | Sem pessoas/sem A/C em I31; 33→25°C permanente com ocupação definida em I32; distinguir carga térmica de elétrica. Superfícies e propriedades citadas; auxiliares provisórios para P5 em 06/11, revisados 13/11 |
| 9 — M2 06/11, M3 13/11 | P4/P5/P2; revisão P6/P4 | Cadeia dinâmica + pvlib + energia: `resistive_forces.csv`, `traction_curve.csv`, `pv_power_timeseries.csv`, `energy_balance.csv`, `range_vs_speed.csv` | Confirmar coordenadas/altitude e convenção 2026; I25 usa energia solar do dia; I26 km/kWh da bateria; I27 alvo SOC 30% com tolerância declarada, v(t), P(t), SOC inicial; revisão de unidades e conservação |
| 10 — M3 13/11 a M6 30/11 | P5 I29; todos validam; P6 PDF/P4 vídeo; P5 índice de códigos | `trip_schedule.csv` com 7000 km, só bateria inicial+solar e ≤8 h/dia; integração, correções e pacote rastreável | M3 decidir incompatibilidades, M4 20/11 congelar/reprocessar, M5 27/11 revisão cruzada e gravações, M6 30/11 conferir PDF<20 MB/vídeo<50 MB (8–10 min, todos), seminário≤8 min. Reserva 01/12. Entrega **02/12/2026 06:00 America/Sao_Paulo**, e-mail aos dois docentes; nada publicado/enviado nesta auditoria |

## Interfaces que bloqueiam dados finais

| Fornecedor → consumidor | Entrega / unidade e bloqueio atual | Prazo / gate |
|---|---|---|
| P1/P6 → P3 | Chassi/layout, dimensões m; base ainda não aprovada | 23–30/10, equipe aprova envelope |
| P3 → P4/P5/P6 | Cd, área frontal/teto/vidros m², volume m³; CAD/CFD final inexistente | 30/10 geometria, 06/11 CFD provisório, 20/11 final; revisão P1 |
| P4 → P2/P5/P7 | Torque N·m, potência/perdas W, eficiência e RPM; curvas não fornecidas | 30/10 dossiê, 06/11 curvas, 13/11 revisão; seleção humana |
| P2 → P5/P7 | V, Ah/kWh, correntes A, SOC, limites e propriedades térmicas; bateria indefinida | 30/10 base, 06/11 lacunas registradas; revisão P7 |
| P5 → P2/P3 | Área m², montagem PV e potência W; teto e painel indefinidos | 30/10 preliminar, alterações maiores decididas 13/11 |
| P6/P7 → P5 | Potência elétrica W e horários s/h de auxiliares; perfis ausentes | 06/11 provisório, 13/11 revisado |
| Todos → P1 | Massas kg/quantidades/preços BRL/fontes; BOM não preenchida | 30/10, 13/11, 20/11; revisão de somas/fontes |
| P5 → todos | Incompatibilidades energia/massa/área; resultados inexistentes | M2 integrar, M3 decidir, M4 congelar |
| Autores → P6/P4 | Seções, figuras, código e gravações; não transferir redação técnica ao editor | 20/11 textos, 27/11 correções/gravações |

Cada entrega registra fonte, unidade, condição, versão, dono, provisório/final e revisão. A auditoria lista dependências de **dados finais**; preparar equações, testes e casos de verificação pode começar com dados sintéticos rotulados. Não confundir essa independência de método com aprovação de dados.

## Decisões humanas em aberto

1. Docentes: autorizar sete integrantes versus dez do enunciado; esclarecer SOC inicial, regime/estado inicial I31, ocupantes I32 e aplicação do dia de São Carlos ao percurso I29. Equipe: associar nomes e disponibilidade a P1–P7 em M0.
2. Equipe e donos: escolher conceito, veículo-base e componentes após comparar fontes; aprovar cenário, tolerância do solver I27 e convenção temporal. A chave YAML `minimum_soc_fraction_daily` não altera o alvo de 30% do enunciado.
3. P1/P4: avaliar se I28→I33 é dependência de integração necessária; a auditoria preserva a aresta. P1: evitar dupla contagem de massas de CAD/componentes.
4. P3/P1 e P2/P7: provar acesso às ferramentas e revisar CAD/CFD/campos térmicos; licenças e experiência de estudantes continuam desconhecidas. Solicitar autorização ao autor antes de redistribuir CAD/código sem licença.
5. Todos: aceitar linha de base provisória M1, resultados M3, congelamento M4 e revisão M5; confirmar P6/P4 como editores e autorização de distribuição de documentos antes de publicação futura. Nenhum gate foi aprovado aqui.
