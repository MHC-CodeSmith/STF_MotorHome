# Motorhome elétrico solar — Registro de decisões

**Atualização de deliberação em 29/10/2026 — DEC-001:** o usuário escolheu **B (circuito solar/DC independente com interface de carga HV autorizada)** como **direção de arquitetura**, substituindo a indecisão entre A e B. **Esta escolha não comprova viabilidade ou compatibilidade técnica.** A alternativa A histórica via bateria auxiliar foi descartada por incompatibilidade com DEC-020. **DEC-002 a DEC-040 permanecem integralmente preservadas** com as comparações e pendências originais. Referências históricas dentro dessas decisões que indiquem “DEC-001 pendente/aberta” dizem respeito à ausência de uma escolha na época; após esta atualização, a *escolha da alternativa* está encerrada, mas a *validação da interface física solar→tração* continua pendente. A DEC-021 (alocação de painéis) e DEC-029 (viabilidade técnica da missão) não foram encerradas.

## DEC-001 — Arquitetura solar → tração
**Status: ALTERNATIVA B SELECIONADA PELO USUÁRIO EM 29/10/2026; VIABILIDADE TÉCNICA, COMPONENTES, PROTOCOLOS, EFICIÊNCIA E INTEGRAÇÃO OEM AINDA NÃO VALIDADOS.** O usuário determinou: “na 1 vamos fazer a B”. A escolha é a **direção de projeto** para a recarga solar da bateria de tração, **não uma autorização para modificar a bateria HV original nem uma comprovação de que o carregamento é possível**.

### B — Arquitetura de projeto escolhida: solar/DC com circuito de carga independente e interface autorizada
**Fluxo funcional proposto:** painéis FV alocados à tração → condicionamento/MPPT adequado → estágio(s) DC/DC com isolamento, regulação, segurança e potência compatíveis → **carregador/interface de recarga DC externa autorizada pelo fabricante** e comunicação/protocolo apropriados → bateria HV por meio das interfaces OEM de carregamento, **sem acesso ou ligação direta aos terminais internos do pack**.

**Condições obrigatórias:**
1. **Bancos independentes (DEC-020):** a bateria de serviços LiFePO₄ 48 V não poderá alimentar a bateria de tração nem receber energia armazenada dela. O circuito solar dedicado à tração deve ser fisicamente e funcionalmente separado do armazenamento dos serviços; qualquer alocação flexível de módulos FV deve usar comutação comprovadamente segura, conforme DEC-021.
2. **Sistema HV OEM inalterado (DEC-026/040):** não abrir, modificar, derivar ou conectar diretamente o pack HV, o BMS ou os cabos originais. Estudar exclusivamente carregamento por interface externa suportada, com comunicações e proteções exigidas. **Não assumir** que qualquer conversor DC/DC, mesmo isolado, constitua sozinho um carregador DC compatível.
3. **Interface e protocolos:** confirmar na variante real do E-Ducato (DEC-036) padrão/conector de recarga DC, parâmetros de tensão, corrente, potência e requisitos de comunicação/handshake e isolamento, incluindo aplicabilidade de IEC 61851-23/24 e normas pertinentes. Documentar autorização/compatibilidade antes de reivindicar integração funcional.
4. **Limite de potência solar:** validar se 1.540 Wp fixos e/ou 1.600 Wp portáteis conseguem alimentar o carregamento DC **com a potência/corrente mínimas reais, inclusive à irradiância variável**. Estudar necessidade de buffer/armazenamento dedicado à arquitetura de carga sem utilizar a bateria auxiliar de serviços; **não adicionar um banco extra sem avaliar massa, custo, operação e aprovar sua inclusão**. Portáteis apenas durante estacionamento (DEC-003).
5. **Segurança e perdas:** modelar MPPT, DC/DC, proteção contra choque e falhas de isolamento, seccionamento, falhas de comunicação, aterramento/equipotencialização aplicável, eficiência, térmica, massa, custo e incertezas com especificações reais. Qualquer desenho é conceitual até validação técnica e de compatibilidade.
6. **Missão solar (DEC-029):** resultados de SOC, autonomia e duração dos 7.000 km permanecem **condicionais** enquanto a interface DC de recarga não for tecnicamente demonstrada. Não classificar a viagem como fisicamente realizável apenas pela seleção B.

### A — Alternativa histórica NÃO escolhida, incompatível com DEC-020 na forma original
Fluxo anteriormente estudado: PV → MPPT → bateria de serviços 48 V → inversor AC → EVSE → OBC OEM → tração HV. Apesar de usar uma interface OEM de recarga AC, essa versão da alternativa A emprega energia armazenada nos serviços para a tração e viola a independência aprovada na DEC-020. **Não executar como arquitetura aprovada**. Suas observações técnicas podem permanecer como histórico de comparação, não como solução ativa.

### Referência comparativa anterior — não validada
Na comparação preliminar, 1,540 kWp × 4 h equivalentes forneceriam 6,16 kWh FV brutos em uma situação **puramente ilustrativa**. Hipóteses anteriores de eficiência global de 73% para A e 89% para B **não são medições ou dados técnicos confirmados** e não devem ser usadas como eficiência real. Diferença de conversão energética não comprova aceitação do carregamento DC com baixa potência solar.

### Entregáveis críticos do P2, integrados com P5 e P4
- Documentar a variante e a interface OEM real de recarga DC; obter diagramas funcionais de equipamentos externos e evidência de compatibilidade/autorização.
- Levantar carregadores DC e soluções de alimentação fotovoltaica **comerciais, documentados**; esclarecer mínimos de corrente/potência de operação, handshake/protocolos, isolamento e disponibilidade real.
- Comparar capacidade FV horário a horário, MPPT, estágios DC e eventuais condições em que o carregamento não inicia ou é interrompido; manter o balanço de energia sem dupla contagem.
- Verificar proteções, limites térmicos, massa, volume, custos e integração no CAD; registrar explicitamente não conformidades e bloqueios.
- Entregar um **parecer de viabilidade**: comprovado / condicionado / não demonstrado / inviável, com evidências e consequências para a DEC-029. Caso a opção B não seja viável, solicitar nova deliberação; **não retornar automaticamente à A**, tampouco modificar o HV OEM.

### Referências já reunidas (exigem conferência para a variante escolhida)
- Stellantis, atualizações de grandes vans: https://www.media.stellantis.com/uk-en/corporate/press/stellantis-announces-key-updates-to-large-van-line-up
- Victron MultiPlus-II 48/5000 (relevante ao sistema de serviços, **não** valida B): https://www.victronenergy.com/media/pg/MultiPlus-II_230V/en/technical-specifications-mp-ii-230v.html
- IEC 61851-23: https://webstore.iec.ch/en/publication/32973
- IEC 61851-24: https://webstore.iec.ch/en/publication/32582

## DEC-002 — Veículo-base e variante
**Status: APROVADA PELO USUÁRIO EM 28/10/2026.** Fixar **Fiat E-Ducato L3H2 como base geométrica** para prosseguir com CAD, envelope externo, interfaces e disposição interna. **Não fixar ainda a variante exata** (ano/modelo, mercado, homologação, PBT, limite de velocidade, motor, pack, tara e dimensões OEM específicas) até conferência técnica e documental.

### Efeitos imediatos
- P3 pode seguir com o CAD L3H2, mas deve marcar como estimados todos os elementos que não sejam geometria OEM confirmada e registrar medidas para validar.
- P1 consolida massas e cargas por eixo com variante em aberto; nenhuma massa/PBT de uma versão deve ser declarada homologação da outra.
- P2/P4 mantêm bateria/motor/transmissão/limitação de velocidade como parâmetros de cenário, não especificação final.
- Não retrabalhar o modelo CAD para outro veículo sem nova decisão expressa do grupo.
- Antes de congelar configuração final, reunir ficha da mesma variante e compatibilidade entre chassi, massa, motor, pack, carga AC e limitador.

## DEC-003 — Configuração solar: painéis fixos e portáteis
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA À VALIDAÇÃO FÍSICA.** Manter **1.540 Wp fixos no teto** e **1.600 Wp portáteis exclusivamente quando estacionado**. Trata-se da arquitetura de geração de referência, não da aprovação da interconexão com a bateria de tração.

### Efeitos e tarefas imediatas
- P3: conferir área real livre do teto L3H2, cotas, sombras, interferência com ar-condicionado/exaustores, suportes, cargas e acesso para manutenção; incluir volume e local de armazenamento dos painéis portáteis no CAD.
- P5: separar geração fixa durante movimento e paradas da contribuição portátil durante paradas explicitamente modeladas; discriminar potência STC (Wp) versus produção real (kWh), sombras, temperatura, inclinação, orientação e perdas.
- P2: confirmar arranjos série/paralelo, faixa MPPT, proteção, inversores e a interface com banco de serviços; não supor ligação ao pack HV enquanto DEC-001 estiver aberta.
- P1: somar massas, fixações e custos dos painéis, suportes, cabos e armazenamento, com referências.
- P5 para item 29: nenhuma recarga externa. Respeitar até 8h de condução/dia; portáteis somente nas paradas e com tempo de montagem/retirada declarado quando material.

### Pendente apesar da aprovação
Dimensões, massas, fixação e viabilidade da instalação; dados elétricos e térmicos dos módulos; perdas reais; condição de implantação dos portáteis. A escolha de painéis **não** resolve a DEC-001 (arquitetura solar → tração).

## DEC-004 — Perfil de uso habitável e autonomia dos serviços
**Status: APROVADA PELO USUÁRIO EM 28/10/2026.** Adotar **uso habitável moderado e energeticamente eficiente como cenário-base**, para duas pessoas. A escolha define o perfil funcional de referência, mas NÃO aprova ainda a capacidade de 10,24 kWh da bateria auxiliar nem a potência nominal do ar-condicionado.

### Perfil funcional aprovado
- Geladeira ligada continuamente, conforme ciclo de funcionamento e ficha técnica real.
- Iluminação, eletrônicos, ventilação e bombas de água conforme horários de uso realistas.
- Cozinha elétrica em períodos definidos, evitando supor todos os aparelhos em potência máxima simultânea.
- Ar-condicionado durante períodos limitados, com duração a definir em perfil de cargas; não presumir funcionamento contínuo.
- Lavadora/secadora contempladas nas especificações do item 13, com uso eventual, contabilizando energia e picos elétricos quando usadas.
- Estudar dois estados separados: deslocamento e estacionamento, especificando quais aparelhos operam em cada um.

### Ações decorrentes
- **P6:** produzir planilha de cargas por equipamento (modelo, potência nominal/média, ciclos, horas/dia, Wh/dia, consumo simultâneo máximo, massa e preço com fonte) e simular perfis diários típicos e de sensibilidade.
- **P2:** conferir tensão, compatibilidade de inversor/cabos/proteções, janela de SOC, necessidade de pico e dimensionar bateria de serviços APÓS receber cargas do P6. Os 10,24 kWh permanecem hipótese preliminar.
- **P5:** considerar consumos auxiliares no balanço energético por período e quando o veículo estiver estacionado/em movimento; não permitir contabilização dupla de energia solar nem transferências solares à tração não verificadas (DEC-001).
- **P1/P3:** conferir massa e volume de equipamentos, isolamento, portas, dutos e interferências físicas com painéis no teto.

### Restrições que continuam obrigatórias independentemente do perfil
- Item 31: cabine **estacionada, fechada, ao meio-dia, sem passageiros e sem ar-condicionado**.
- Item 32: ar externo **33 °C**, temperatura interna desejada **25 °C**, com passageiro, **regime permanente**.
- As durações de utilização do A/C são hipóteses de operação para consumo; NÃO substituem o dimensionamento térmico do item 32.

## DEC-005 — Critério de autonomia da bateria de serviços
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; CAPACIDADE FINAL PENDENTE.** O usuário escolheu a alternativa D: comparar dimensionamento da bateria de serviços para **24 e 48 horas** de uso moderado sem geração solar, antes de escolher a capacidade final. Os 10,24 kWh atuais permanecem hipótese de comparação, não escolha final. Não escolher capacidade fixa sem fechar balanço de energia e potência.

### Alternativas propostas
- **A — 24 horas de serviços:** dimensionar o banco para 24 h de consumo moderado, desconsiderando geração solar nesse teste conservador e preservando reserva de SOC a estabelecer. Ajustar kWh ao resultado.
- **B — 48 horas de serviços:** dimensionar para duas diárias sem geração solar, mantendo o uso moderado; maior massa/custo.
- **C — Manter 10,24 kWh como capacidade-alvo:** verificar a autonomia efetiva do sistema e registrar restrições; não supor que o valor já seja adequado.
- **D — Comparar 24 e 48 horas antes de escolher [ESCOLHIDA]:** P6 estima as cargas, P2 dimensiona ambos os cenários, P1/P5 avaliam massa, preço e autonomia.

### Entregáveis para decidir a capacidade
1. P6 entrega a planilha do perfil moderado com potência instantânea e consumo total diário (Wh), incluindo pelo menos o caso de ar-condicionado por tempo limitado e equipamentos em uso simultâneo.
2. P2 entrega dimensionamento **24 h** e **48 h** sem geração solar, com janela de SOC, perdas no inversor/conversores, autonomia efetiva, pico de potência, células/BMS/proteções e margens explicitadas.
3. P1 estima massas adicionais, espaço no CAD e custo comparável de cada alternativa; P3 verifica o volume físico.
4. P5 compara impacto energético no sistema inteiro, distinguindo bateria de serviços do pack de tração.
5. Montar tabela comparativa: kWh nominal, kWh utilizável, massa, volume, preço, autonomia prevista, eficiência e limitações. O cenário de 10,24 kWh entra como referência, NÃO como escolha.
6. Adotar a capacidade final apenas após aprovação explícita do grupo.

### Regras para qualquer alternativa
Contabilizar potência de pico do inversor, energia utilizável, eficiência e reserva; registrar cargas e ciclos de uso. A DEC-001 (interface solar-tração) permanece pendente e não pode ser assumida como aprovada.

## DEC-006 — Escopo e apresentação da viagem do item 29
**Status: APROVADA PELO USUÁRIO EM 28/10/2026.** Apresentar **7.000 km** como resultado principal, atendendo ao enunciado, e manter a **rota rodoviária aproximada de 7.511 km** encontrada pelo Codex como estudo complementar. Não substituir um número pelo outro.

### Consequências de execução
1. **P5:** reportar explicitamente resultados ao marco de 7.000 km: dias decorridos, dias de condução, horas totais dirigidas, velocidade por trecho, energia solar capturada, consumo da tração, consumo dos serviços, SOC e eventuais restrições; limitar condução a **até 8 h por dia**.
2. **P5:** manter a extensão até aproximadamente 7.511 km (Belém–Chuí na rota OSRM/OSM escolhida) como estudo adicional identificado, sem tratar extensão como nova exigência do professor.
3. Não usar recarga elétrica externa em nenhum dos cenários do item 29. Painéis portáteis de 1.600 Wp só podem operar estacionados, conforme DEC-003.
4. Mostrar as sensibilidades às hipóteses de Cd, Cr, massa, eficiência de tração, consumo habitável e ao clima, sem confundir os cenários.
5. **DEC-001 permanece pendente:** a conexão solar→tração não foi validada; portanto, resultados de chegada e tempo mínimo são *condicionais*, não garantidos fisicamente.
6. Uma busca em grade de velocidades constantes (60/80/90 km/h) **não comprova o ótimo global** do problema. Informar método de otimização e restrições, bem como status de validação.
7. A escolha do ano/calendário, insolação e meteorologia para viagem longa permanece objeto da DEC-007.

## DEC-007 — Cenário de insolação e meteorologia da viagem
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO A).** O enunciado fixa o cenário de céu limpo de **21 de junho em São Carlos**, com **25 °C**, **50% UR** e **vento zero** quando não houver outras condições prescritas. O Codex executou cenários clear-sky e ERA5 ao longo de rota e calendário, tomando 21/06/2025 como partida de estudo; essa data não deve ser chamada de exigência do professor.

### Opções consideradas
- **A (APROVADA):** entregar **dois cenários distintos**: (i) *referência acadêmica* com condições de céu limpo de São Carlos em 21/06, aplicadas como um dia-tipo repetido na idealização multidiária da missão (hipótese declarada); (ii) *sensibilidade realista* com latitude, data, relevo e meteorologia variáveis no percurso, explicitando o ano e a origem dos dados (ERA5 ou equivalente). Repetir o dia-tipo não representa previsão meteorológica real.
- **B:** usar trajetória e calendário com **céu limpo calculado a cada dia/localidade** como resultado principal do item 29, incluindo separadamente o caso de referência de São Carlos 21/06 para os cálculos fixados no enunciado. A escolha do ano de partida será explicitada.
- **C:** manter cenário de referência fixo exigido e cenários de rota apenas como hipótese de sensibilidade até a interpretação ser confirmada com o professor.

### Decisão registrada e instruções
- **Cenário principal acadêmico:** simular o dia-tipo de 21 de junho, céu limpo, coordenadas/altitude de São Carlos, 25 °C (salvo quando outro valor for prescrito), 50% UR e vento zero, repetido como *hipótese idealizada* em todos os dias de viagem. NÃO descrever essa idealização como meteorologia real de Belém a Chuí.
- **Cenário complementar de sensibilidade:** usar coordenadas e datas ao longo da rota, com posição solar e meteorologia variável (por exemplo, ERA5); declarar explicitamente o ano de partida e o recorte histórico. Não apresentar ERA5 como previsão de centenas de dias futuros.
- P5 deve entregar quadros separados para 7.000 km (principal, conforme DEC-006) e aproximadamente 7.511 km (complementar), e comparar desempenho e SOC entre as duas hipóteses climáticas.
- DEC-001 continua aberta: geração fotovoltaica só pode ser computada como energia de tração efetivamente recebida nos cenários condicionais de interfaces comprovadas ou explicitamente hipotéticas.

### Dados e restrições a documentar
- Data/ano da partida (não fornecidos explicitamente no enunciado), fuso, coordenadas e altitude, período de geração, horário de condução e intervalos estacionados.
- Separação clara entre *irradiação idealizada de céu limpo*, *reanálise histórica* e qualquer *previsão* (não há previsão meteorológica de centenas de dias).
- Painéis fixos e portáteis contabilizados conforme estado de movimento; balanço energético separado entre serviços e tração; DEC-001 em aberto.
- Antes de apresentar número de dias como mínimo global, documentar a estratégia de otimização e as limitações.

## DEC-008 — Carga útil e água para o layout do motorhome
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO B, EQUILIBRADA).** Adotar como cenário-base para CAD, dimensionamento e balanço de massa:

- **Ocupantes:** 2 × 80 kg = **160 kg**.
- **Bagagem:** 60 kg no total (30 kg por ocupante).
- **Água limpa:** reservatório de **100 L**.
- **Águas cinzas:** reservatório de **70 L**.
- **Águas negras:** reservatório de **20 L**.
- **Configuração de uso:** duas pessoas, uso habitável moderado (DEC-004).

### Consequências e limites
- No cenário de partida com tanque limpo cheio, tanques residuais vazios e sem consumíveis extras, **160 + 60 + 100 ≈ 320 kg** de ocupantes, bagagens e água (tomando aproximadamente 1 kg/L). **Não é a massa total da conversão**: faltam tanques vazios, fixações, tubulações, móveis, bateria de serviços, painéis, aparelhos, alimentos etc.; massa da tara OEM precisa ser contabilizada sem duplicar.
- A capacidade dos reservatórios **não** significa 100 + 70 + 20 kg simultâneos. Simular níveis consistentes com conservação da massa e uso; incluir massa própria de cada tanque separadamente, inclusive quando vazio.
- **P1:** atualizar tabela de massas, carga útil, momentos/CG e cargas por eixo, mantendo a variante OEM aberta (DEC-002).
- **P3:** conferir espaço e interferências do CAD L3H2; posicionar os tanques para controlar CG e permitir manutenção.
- **P6:** incluir consumo de água e equipamentos no perfil habitável e verificar ergonomia/instalações.
- **P4/P5:** incorporar a massa correspondente nos cenários de consumo e autonomia e executar sensibilidade ao volume realmente transportado.
- **Pendências remanescentes:** PBT e cargas admissíveis da variante real; tara e distribuição por eixo; peso de tanques, aparelhos, fluidos e alimentação; posição/volume e condições de instalação; validação humana.

## DEC-009 — Tratamento da velocidade máxima e aceleração 0–100 km/h
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO C); VARIANTE EXATA PENDENTE.** O Codex identificou como hipótese a configuração com limitador de **90 km/h**. O enunciado exige velocidade máxima e tempo de aceleração de 0 a 100 km/h. Como a variante exata do E-Ducato ainda está em aberto (DEC-002), não presumir que 90 km/h é limite de todas as variantes nem prometer 0–100 km/h sem curva real de tração.

Alternativas para aprovação:
- **A — Priorizar fidelidade ao OEM:** se confirmada a variante limitada a 90 km/h, relatar 0–100 km/h como *não alcançável nessa configuração*, calcular 0–90 km/h com curva documentada; opcionalmente apresentar caso teórico sem limitador claramente separado, sem sugerir alteração real do veículo.
- **B — Buscar variante OEM que alcance 100 km/h:** comparar variantes e fichas para selecionar uma que cumpra 0–100 km/h; exige revalidar massa, PBT, geometria/tração e demais números antes do congelamento.
- **C — Comparar A e B antes de fixar uma variante [ESCOLHIDA]**, preservando cálculos e documentação de ambas; usar 90 km/h apenas como hipótese enquanto não houver evidência da variante real.

Tarefa mínima para P4, conforme a opção C escolhida: obter limites do fabricante, relação do redutor, curvas torque/potência versus RPM, estimativa de eficiência por ponto, forças resistivas, modelo de aceleração respeitando limites elétricos e tração, com rastreabilidade das fontes. Nunca inventar curvas OEM.

### Critérios para resolver DEC-009
1. P4 e P1 devem montar uma tabela de variantes reais L3H2 identificadas por ano, mercado, PBT, código/denominação, motor, bateria, limitador, câmbio/redutor e disponibilidade/documentação.
2. Separar explicitamente variantes homologadas limitadas a 90 km/h daquelas documentadas com capacidade de atingir ou superar 100 km/h; nenhuma hipótese de desbloqueio de velocidade é tratada como especificação OEM.
3. Calcular 0–100 km/h SOMENTE para variante fisicamente capaz e parametrizada, com mapas de torque/potência, perdas e resistência ao movimento. Se não houver curva OEM, relatar estimativa de engenharia e faixa de incerteza, não atribuir ao fabricante.
4. Verificar se a variante escolhida no futuro mantém compatibilidade geométrica e estrutural com o CAD já fixado na DEC-002.
5. A decisão final sobre a variante permanece pendente até comparação e validação pelo grupo.

## DEC-010 — Dimensionamento do ar-condicionado e margem de capacidade
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO C); EQUIPAMENTO FINAL PENDENTE.** O usuário decidiu comparar o FreshWell 3000 com alternativas de maior capacidade antes de escolher, considerando conforto térmico, consumo elétrico, massa e custo. Com os dados preliminares do Codex: FreshWell 3000 com capacidade nominal de resfriamento em torno de **2,7 kW** e carga estimada de **2,646 kW** no cenário de duas pessoas; margem nominal aproximada de **54 W (~2%)**. É uma aproximação condicionada a propriedades da carroceria, vidro, solar, ventilação, COP e instalação; não deve ser tratada como validação de suficiência.

### Alternativas a considerar
- **A — Manter FreshWell 3000 como candidato-base**, sujeitando-o à validação de capacidade real na condição externa de 33 °C, ganhos solares, dutos, carga do item 32, pico elétrico e margem de projeto. Se falhar, redimensionar.
- **B — Priorizar equipamento com capacidade nominal superior (ex. classe 3,5–4 kW)**, após verificar disponibilidade, instalação sob cama/teto, massa, potência elétrica, ruído e custo. Não assumir que já existe modelo que caiba no CAD.
- **C — Comparar A e B em análise de sensibilidade antes da escolha [ESCOLHIDA]**, executando cenários 1 passageiro para atendimento literal do item 32 e 2 pessoas como uso habitável, incluindo casos de maior irradiância e incerteza do isolamento.

### Entregáveis mínimos
1. P6: rever balanço térmico com dimensões/áreas reais entregues por P3; declarar propriedades, cargas, infiltração, ventilação e regime permanente do item 32 (25 °C interno, 33 °C externo, passageiro).
2. P6: executar sensibilidade com duas pessoas, carga solar intensa, isolamento e COP/capacidade dependente da condição; verificar se 2,7 kW realmente sustenta 25 °C.
3. P2/P5: calcular o consumo elétrico e o efeito nas baterias de serviços de 24/48 h (DEC-005) e na autonomia/viagem; verificar potência simultânea e dimensionamento do inversor.
4. P1/P3: conferir massas, custo, dimensões, posicionamento e dutos no modelo CAD.
5. Entregar tabela com FreshWell 3000 versus ao menos uma alternativa maior, dados/fonte, margem térmica e energia diária. Não congelar componente antes da revisão.

## DEC-011 — Estratégia de paradas e horários dos painéis portáteis na viagem
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO C); POLÍTICA FINAL PENDENTE.** O usuário escolheu **comparar uma política de condução em horário fixo com uma política que otimiza os horários de condução e paradas solares antes de selecionar a estratégia final**. Não registrar a política otimizada como aprovada definitivamente.

### Comparação obrigatória
- **Cenário A — horário fixo:** por exemplo 08:00–16:00, limitado a 8 h de direção por dia; os painéis portáteis só geram energia depois de instalados, enquanto o veículo está parado e há sol.
- **Cenário B — horário otimizado:** definir horários de condução e paradas, podendo dividir o período diário de condução, com até 8 h ao volante por dia. Otimizar o tempo total da viagem, considerando geração solar, estado de carga, energia consumida, montagem/desmontagem dos portáteis e duração das paradas.
- **Comparação justa:** aplicar o mesmo veículo, massa, rota, geração solar, baterias, cargas habitáveis, eficiência e estado inicial nas duas políticas; reportar dias para completar 7.000 km, duração na rota de ~7.511 km, SOC, energia solar aproveitada, tempos ao volante/parado e sensibilidade a hipóteses.

### Regras do enunciado e decisões anteriores
1. Não ultrapassar 8 horas de condução por dia, nem usar recarga externa na missão do item 29.
2. Painéis no teto (1.540 Wp): funcionam em movimento e parado, respeitando geometria/orientação e perdas. Portáteis (1.600 Wp): somente parados, após tempo de instalação, sem geração noturna.
3. Principal: 7.000 km conforme DEC-006; complemento: rota real de ~7.511 km; cenários climáticos de DEC-007 apresentados separadamente.
4. Até demonstrar uma interface PV→tração compatível (DEC-001), resultados que presumem essa transferência continuam hipotéticos; não declarar conclusão viável.
5. A comparação pode mostrar qual política é melhor nas hipóteses testadas, mas não provar ótimo global sem demonstrar metodologia e critérios de otimalidade.

### Entregáveis para P5
- Arquivos de configuração das duas políticas; código reproduzível; curvas de velocidade, SOC e potência; demonstrativo de permanência em cada parada; tabela comparativa por rota/clima e hipóteses.
- Recomendação técnica *após* a comparação, identificando restrições da interface elétrica e dos equipamentos.

## DEC-012 — Critério de seleção de componentes e realismo do projeto
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO A).** Priorizar **componentes reais e documentados**, com marca/modelo, ficha técnica, massa, dimensões, desempenho, compatibilidade e preço rastreáveis. Quando faltarem dados, usar hipóteses justificadas e análises de sensibilidade, **sem inventar especificações de fabricante ou apresentar hipótese como dado OEM**.

### Regras para todos os integrantes e para o Codex
1. Para cada componente, registrar fabricante, modelo/variante, URL verificável, data de consulta, especificação, quantidade, massa, dimensões, tensão/potência/eficiência quando aplicável, preço, moeda, impostos e responsável pela verificação.
2. Separar **dado declarado pelo fabricante**, **fonte secundária**, **estimativa de engenharia** e **resultado de simulação**. Toda grandeza crítica deve indicar unidade, fonte, intervalo de incerteza ou justificativa de hipótese.
3. Dar preferência a alternativas comercialmente existentes e fisicamente compatíveis com o E-Ducato L3H2. CAD terceirizado ou inspirado em OEM não equivale a CAD certificado do fabricante.
4. Se não houver mapa OEM de torque/eficiência, modelo de resistência interna de bateria, curva de bomba, coeficiente aerodinâmico final ou eficiência de interface de carregamento, explicitar as premissas e apresentar varredura de sensibilidade. Não preencher lacunas com valores falsamente atribuídos ao fabricante.
5. Incluir no custo do item 24 quantidade, aquisição, frete e tributação/importação aplicável, com cenário-base e premissas explícitas. Não tratar lista sem cotação como orçamento fechado.
6. Não alterar decisões anteriores apenas para forçar viabilidade. Em particular, **DEC-001 (PV→tração) permanece aberta**, e variantes/capacidades/equipamentos ainda não selecionados permanecem em análise.
7. Cada item só recebe aprovação técnica após revisão humana, reprodução dos cálculos e conferência das fontes; ter código ou gráfico executável não equivale a validação física.

### Ações
- **P1:** consolidar BOM e custos com evidências e massa/carga útil sem duplicar partes OEM.
- **P2:** selecionar modelos de bateria, MPPT, cabos/inversores e avaliar compatibilidade da recarga OEM, sem supor interface HV liberada.
- **P3:** conferir cotas CAD, origem/licença dos arquivos e hipóteses CFD.
- **P4:** levantar curvas reais de motor/transmissão/pneus ou demonstrar hipóteses e faixas de incerteza.
- **P5:** integrar balanço energético usando eficiências rastreáveis; distinguir cenários reais/hipotéticos.
- **P6:** validar equipamentos internos, climatização e consumo com fichas de produto.
- **P7:** validar propriedades térmicas, curvas e limites de bomba, radiador, bateria e sistema de arrefecimento.

## DEC-013 — Reservas mínimas de carga (SOC) na viagem de 7.000 km
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; RESERVAS DEFINITIVAS PENDENTES.** O usuário escolheu comparar **10% tração/20% serviços** com **20% tração/30% serviços** antes de fixar os limites operacionais do item 29. O item 27 exige **30% de carga ao final do dia**, e essa condição não deve ser transferida automaticamente ao item 29.

### Alternativas propostas para o usuário
- **A — Preservar 10% tração / 20% serviços como limites operacionais do item 29**, sujeitos a confirmação das janelas úteis e BMS.
- **B — Adotar margens mais conservadoras: 20% tração / 30% serviços**, sujeitos a confirmação.
- **C — Comparar ambos os conjuntos como análise de sensibilidade [ESCOLHIDA]** antes de fixar os limites da missão; usar o mesmo estado inicial, veículo e clima nas duas simulações, explicitando o SOC inicial das duas baterias e documentando o efeito em quilômetros e dias.

### Condições fixas
- Item 27: terminar com 30% da capacidade definida no modelo conforme enunciado.
- Item 29: no máximo 8 h de direção/dia e nenhuma recarga externa; SOC mínimo é decisão de engenharia, não obrigação textual de 30% no fim da missão.
- Não alegar viabilidade da missão com energia solar na tração sem demonstrar a interface DEC-001.


### Entregáveis para decidir as reservas (P2 e P5)
1. Comparar 10%/20% e 20%/30% (tração/serviços) em cada cenário climático relevante, com mesmos dados de entrada e mesma estratégia de paradas; distinguir percentuais da capacidade útil e da nominal.
2. Registrar SOC mínimo atingido, dias para completar 7.000 km, horas dirigidas, tempos de parada, energia solar efetivamente entregue à tração e à habitação e restrições violadas.
3. Verificar limites mínimos seguros e disponibilidade real de energia conforme BMS/fabricantes; não tratar 10% ou 20% como aprovados tecnicamente apenas por haver simulação.
4. Se a interface solar→tração continuar não validada (DEC-001), indicar explicitamente resultados hipotéticos, preservando cenário sem interface.
5. Levar tabela comparativa à revisão humana antes de escolher a reserva operacional final.


## DEC-014 — Estado de carga inicial (SOC) do item 27
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO C).** Para a simulação de autonomia máxima diária do **item 27**, adotar **SOC inicial de 100% como cenário principal** e **SOC inicial de 80% como análise de sensibilidade**. **Ambos devem terminar com SOC de 30%**. Esta escolha não altera os limites de SOC da missão de 7.000 km (item 29; DEC-013), ainda em comparação.

### Cenários aprovados
- **Principal:** SOC inicial da bateria de tração **100%**, SOC final **30%**. Maximizar autonomia diária respeitando desempenho, balanço energético e requisitos do enunciado.
- **Sensibilidade:** SOC inicial **80%**, SOC final **30%**. Para comparação justa, manter as mesmas condições de veículo, solar, consumo, bateria, eficiências, restrições e método de otimização.
- Explicitar **se o percentual é relativo à capacidade nominal, útil ou a uma janela de SOC modelada**; usar a mesma convenção em todos os cálculos. A hipótese atual de 98 kWh úteis não é ficha final homologada da variante, que continua pendente na DEC-002.

### Comparação numérica ilustrativa, não resultado de autonomia
Se for adotada apenas para comparação a hipótese de **98 kWh úteis**, a energia líquida inicial disponível até a reserva obrigatória de 30% é:
- Principal: `(1,00 - 0,30) × 98 = 68,6 kWh`.
- Sensibilidade: `(0,80 - 0,30) × 98 = 49,0 kWh`.
Essas grandezas **não são distâncias percorridas**; faltam perdas, energia solar efetivamente acessível à tração e cargas auxiliares. A interface PV→tração (DEC-001) segue não validada.

### Próximas ações
1. **P5:** produzir, para ambos os casos, distância diária, SOC(t), velocidade(t), potência instantânea do motor, geração solar e consumo de serviços; preservar cenários específicos do professor e decisões DEC-003/DEC-007.
2. **P2:** esclarecer capacidade nominal/útil, limites reais do BMS e SOC dos bancos de tração e de serviços, sem misturar seus estados de carga.
3. **P4:** fornecer curvas de tração e perdas coerentes com as condições simuladas, identificando o que depende da variante ainda não definida (DEC-009).
4. **P2/P4/P5:** executar revisão cruzada e garantir que ambos **terminam em 30%** sem violar outras restrições; diferenciar dado OEM, hipótese e resultado simulado.
5. **Relatório:** apresentar **100%→30% como principal** e **80%→30% como sensibilidade**, com gráficos, tabela de resultados e premissas documentadas.

### Pendências preservadas
DEC-001 (arquitetura de transferência PV→tração); DEC-002/DEC-009 (variante exata, curvas e limitador); DEC-005 (dimensionamento final da bateria auxiliar); DEC-010 (modelo de ar-condicionado); DEC-011 (política final de paradas); DEC-013 (reservas da viagem de 7.000 km). Esta decisão **não** escolhe essas alternativas.

## DEC-015 — Lavadora/secadora compacta 2 em 1 para uso ocasional
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA À VALIDAÇÃO TÉCNICA.** Adotar como solução de referência **um único equipamento compacto que combine as funções de lavar e secar roupa (2 em 1)**, com **uso ocasional**, compatível com o perfil habitável moderado definido na DEC-004. A escolha é de **tipo de equipamento**, não de marca/modelo ou produto aprovado.

### Critérios e tarefas
1. **P6 (responsável):** identificar modelos reais e documentados; registrar marca, modelo, dimensões, massa, potência nominal e em cada ciclo, demanda de energia por lavagem/secagem, água por ciclo, requisitos hidráulicos, ventilação/condensação, tensão, ruído e preço; verificar se realmente secam as roupas, não apenas centrifugam.
2. **P3:** reservar volume e área para instalação e manutenção no CAD L3H2, considerando abertura de portas, fixação, vibração, acesso e ventilação exigida pelo fabricante. Não tratar o modelo CAD de equipamento genérico como prova de compatibilidade física.
3. **P1:** incluir massa do equipamento, suportes e água nos modelos de massa/eixos e na BOM, sem contabilizar duplamente a água que migra entre tanques; respeitar DEC-008 (100 L de água limpa, 70 L de cinzas e 20 L de negras, capacidades de tanques).
4. **P2:** verificar compatibilidade com sistema de serviços 48 V/inversor AC, corrente de partida, consumo simultâneo, proteção e disponibilidade real de potência. Não assumir que o MultiPlus-II 48/5000 entrega 5 kW contínuos; confirmar ficha e condições de temperatura.
5. **P5:** incluir ciclos ocasionais em cenário de consumo, comparar dias com e sem lavadora/secadora e avaliar impactos no dimensionamento de 24/48 h (DEC-005); distinguir consumo de serviços de energia de tração, sem supor interconexão ainda não validada (DEC-001).
6. **P7:** conferir necessidade de exaustão/ventilação, calor liberado internamente e eventual gestão de condensado, quando pertinente ao equipamento escolhido.

### Critérios para fechar o modelo definitivo
- Pelo menos um modelo real com documentação de consumo, dimensões e massa; confirmar que cabe no CAD e pode operar com a instalação prevista.
- Balanço de água e energia com ciclo declarado e frequência ocasional explicitamente assumida.
- Registro de limitações, preço e fontes antes de concluir o item 13.
- **Permanecem pendentes:** seleção do modelo exato e comprovação de compatibilidade com os sistemas elétrico, hidráulico, térmico e com a carga útil do veículo.

## DEC-016 — Isolamento térmico do motorhome e controle solar dos vidros
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA À VALIDAÇÃO TÉCNICA.** Adotar **isolamento térmico no teto, nas paredes e no piso**, além de **proteção solar nos vidros**, para o Fiat E-Ducato L3H2 (DEC-002). A decisão aprova o conceito funcional, **não** uma espessura, composição, marca, desempenho ou produto comercial específico.

### Requisitos de projeto e verificação
1. **P6 — Responsável técnico:** pesquisar materiais reais e fichas técnicas de isolamento para teto, paredes e piso; documentar condutividade térmica, resistência térmica por camada, espessura, densidade, absorção/controle de umidade, comportamento ao fogo e aplicabilidade automotiva. Incluir radiação através dos vidros e proteções solares com propriedades rastreáveis.
2. **P3 — CAD e envelope:** incorporar a espessura das camadas, revestimentos, eventuais pontes térmicas, janelas, esquadrias e interferências com dutos, armários, vidros, altura útil e área efetiva do teto. Não contabilizar a carenagem metálica como isolamento suficiente.
3. **P1 — Massa e custo:** estimar área real, quantidade, massa e custo dos isolantes e das proteções solares, com fontes; verificar reflexos em PBT e centro de gravidade.
4. **P6 — Simulações obrigatórias:** para o item 31, manter cabine **estacionada e totalmente fechada ao meio-dia, sem climatização e sem passageiros**; para o item 32, manter **33 °C externos, 25 °C internos, passageiro presente e regime permanente**. Incorporar condução pelo envelope, ganhos solares e hipóteses de convecção/ventilação conforme cada cenário. Usar datas/condições ambientais do enunciado quando aplicáveis.
5. **P2 e P5 — Consumo energético:** receber do P6 a carga térmica calculada e o consumo elétrico estimado do A/C, mantendo compatibilidade com DEC-004 (uso moderado), DEC-005 (24 h × 48 h) e DEC-010 (comparação entre A/C).

### Critérios para fechar a seleção de isolantes
- Tabela de materiais selecionados com marca/modelo, espessura, área, massa, preço, condutividade e fonte verificável, separando valores declarados pelo fabricante das estimativas do grupo.
- Comparação de desempenho térmico e sensibilidade à espessura; explicitação das pontes térmicas e ganhos solares nos vidros.
- Integração das camadas no CAD e na massa, sem exceder limites geométricos e de carga da variante ainda a verificar.
- Revisão humana e aprovação do dimensionamento; **não** fechar espessura ou material antes desta etapa.

### Interdependências preservadas
- DEC-001: conexão da geração solar à tração **continua em análise**.
- DEC-002: base geométrica L3H2 confirmada, mas variante homologada em aberto.
- DEC-003: painéis 1.540 Wp fixos + 1.600 Wp portáteis durante paradas; verificar sombras, suportes e interfaces no teto.
- DEC-004/005: uso moderado e comparação de autonomia de serviços 24 h × 48 h.
- DEC-008: carga de ocupantes, água e bagagem; não duplicar a água dos tanques.
- DEC-009/010/011/013: comparações de variantes, A/C, paradas e reservas permanecem abertas.
- DEC-014: SOC 100%→30% principal, 80%→30% em sensibilidade (item 27).
- DEC-015: lavadora/secadora 2 em 1, uso ocasional, sem modelo comercial aprovado.

## DEC-017 — Boiler elétrico compacto para água quente
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA A DIMENSIONAMENTO E VALIDAÇÃO TÉCNICA.** Adotar **boiler elétrico compacto com reservatório isolado** para aquecimento de água do chuveiro/uso sanitário. A escolha fixa a **tecnologia**; **não** fixa ainda marca, modelo, volume, potência, tensão, horas de uso ou temperatura de armazenamento.

### Interface com decisões anteriores
- **DEC-004:** uso habitável moderado para duas pessoas; especificar perfil de banhos e demanda de água quente em vez de presumir aquecimento contínuo.
- **DEC-008:** água limpa com capacidade de **100 L**, águas cinzas **70 L** e negras **20 L**; o boiler integra o sistema de água, não autoriza somar a mesma água duas vezes. A massa do recipiente, da água efetivamente contida e das conexões deve ser discriminada.
- **DEC-005:** comparar bateria de serviços para **24 h e 48 h sem sol**, incluindo energia de aquecimento, perdas em espera e eficiência de conversão.
- **DEC-012:** priorizar produtos reais, fichas técnicas, preços rastreáveis e hipóteses explicitadas.
- **DEC-001:** a arquitetura solar→tração continua em análise; alimentar o boiler pelo barramento de serviços não demonstra recarga do pack de tração.
- **DEC-015 e DEC-016:** verificar a convivência com lavadora/secadora compacta, isolamento da cabine e espaço físico no CAD.

### Próximas tarefas por responsável
1. **P6 — Responsável:** dimensionar o volume necessário de água aquecida por uso com dois ocupantes; estimar temperatura de entrada, temperatura de armazenamento, mistura com água fria, demanda diária e potência elétrica. Verificar perdas estacionárias e isolamento térmico, além de listar pelo menos dois modelos comerciais que atendam ao volume/potência estimados.
2. **P2:** confirmar tensão, inversor, circuito dedicado, proteção elétrica, corrente de operação/pico e compatibilidade com os demais consumidores simultâneos.
3. **P3:** alocar boiler, tubulação, válvulas, drenos e acesso para manutenção no CAD L3H2; considerar fixação e ventilação/segurança previstas no fabricante.
4. **P1:** incluir massa do equipamento vazio, água contida sem dupla contagem, tubulação, suportes e preço na BOM; verificar carga por eixo.
5. **P5:** incluir consumo térmico convertido em consumo elétrico no perfil moderado e nas comparações de bateria de serviços de 24/48 h.

### Critérios de aprovação final
- Modelo comercial identificado, com documentação de volume, potência, tensão, massa, dimensões, isolamento, condições de instalação e custo.
- Balanço de massa/água e de energia por uso, explicitando hipóteses e perdas; sem contabilização dupla de água ou de energia.
- Verificação de instalação no CAD, fornecimento elétrico, limites térmicos e revisão humana dos cálculos.
- **Pendente:** selecionar modelo, volume, potência e perfil definitivo de uso; a decisão de adotar boiler não fecha esses parâmetros.

## DEC-018 — Vaso sanitário com cassete removível de aproximadamente 20 L
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA A VALIDAÇÃO TÉCNICA.** Adotar **vaso sanitário com cassete removível de aproximadamente 20 L**, utilizando **o próprio cassete como reservatório de águas negras**, **sem adicionar outro tanque fixo de 20 L**. A decisão seleciona a arquitetura do sanitário; fabricante, modelo, volume comercial preciso, massa, dimensões, consumo de água e forma de instalação seguem pendentes.

### Compatibilidade com decisões anteriores
- **DEC-008:** capacidades aprovadas: 100 L de água limpa, 70 L de águas cinzas e 20 L de águas negras. Interpretar o cassete como a capacidade de águas negras da DEC-008; não duplicar reservatório, água nem massa.
- **DEC-002:** verificar a instalação em uma cabine habitável para duas pessoas no envelope geométrico E-Ducato L3H2, sem pressupor que o CAD importado já comporta corretamente o sanitário.
- **DEC-004/005:** verificar perfil de uso moderado e eventual consumo de bomba, descarga e ventilação no balanço de serviços 24 h × 48 h.
- **DEC-012:** usar equipamento real com documentação verificável, não inventar dimensões ou preço.
- **DEC-017:** compatibilizar banheiro, chuveiro, boiler e hidráulica; água consumida no chuveiro vai às águas cinzas, não ao cassete, salvo configuração diferente documentada.

### Próximas tarefas
1. **P6 — Responsável:** levantar ao menos dois vasos com cassete comercialmente disponíveis com capacidade próxima de 20 L; registrar modelo, capacidade útil, dimensões, peso, consumo de descarga, ventilação, sistema de retirada, esvaziamento, preço e fontes. Estimar autonomia sanitária para duas pessoas, com premissas explícitas.
2. **P3:** conferir volume do compartimento sanitário, espaço para sentar, acesso à retirada do cassete, abertura de portas, fixações e rota para esvaziamento/manutenção no CAD.
3. **P1:** incluir vaso/cassete vazio e conteúdo máximo nos casos de carga do veículo, respeitando a conservação de água e a ausência de tanque negro adicional.
4. **P2/P5:** contabilizar cargas elétricas somente se o equipamento escolhido utilizar bomba/descarga/ventilação elétricas; validar integração com o sistema 48 V/AC conforme ficha.
5. **P6/P3:** definir ventilação e manejo de odores conforme o produto escolhido, sem alterar os cenários impostos para as simulações térmicas da cabine.

### Critérios de fechamento
- Modelo e ficha técnica confirmados, incl. capacidade, massa, cotas e manutenção.
- Verificação espacial e de acesso no CAD, balanço de água sem dupla contagem, preços e avaliação de compatibilidade.
- Revisão técnica humana antes de considerar o item 13 finalizado.

**Pendente após DEC-018:** escolher o modelo exato e comprovar acomodação física e operação. **A arquitetura PV→tração (DEC-001) e todas as comparações anteriores permanecem abertas.**

## DEC-019 — Gerenciamento de cargas da habitação e inversor como candidato
**Status: APROVADA PELO USUÁRIO EM 28/10/2026, SUJEITA À VALIDAÇÃO ELÉTRICA.** Adotar **gerenciamento de cargas** para evitar operação simultânea de grandes consumidores (fogão de indução, boiler, lavadora/secadora e ar-condicionado). **Manter o Victron MultiPlus-II 48/5000 como CANDIDATO**, sem aprovar definitivamente o inversor, sua capacidade de atender às cargas ou sua interação com a recarga do veículo de tração.

### Escopo decidido
- Perfil funcional: uso habitável moderado (DEC-004), com cargas prioritárias e cargas adiáveis.
- Priorizar cargas essenciais (geladeira, ventilação necessária, iluminação de segurança e sistemas de monitoramento/proteção), enquanto cargas não essenciais são programadas para horários diferentes.
- Não assumir 5 kW contínuos apenas pela designação 48/5000: verificar ficha, VA versus W, temperatura de operação, tensão, capacidade de pico e curvas de derating. A referência anterior considerava cerca de 4.000 W contínuos a 25 °C, a confirmar para a configuração exata.
- Os 4.500 W exemplificativos exibidos na conversa são **ilustração**, não carga efetivamente medida ou BOM aprovada.

### Tarefas e interfaces
1. **P6:** criar tabela de equipamentos reais com potência elétrica instantânea/nominal, corrente de partida, energia diária, perfil de acionamento, horários de uso, cargas críticas e ordem de prioridade; incorporar boiler (DEC-017), lavadora/secadora (DEC-015), climatização ainda em comparação (DEC-010) e equipamentos do item 13.
2. **P2:** conferir inversor 48/5000, proteção, cabeamento, limites da bateria/BMS, autonomia e simultaneidade máxima em todas as temperaturas de operação relevantes; testar partidas e contingências; levantar alternativa maior apenas se a opção candidata falhar nos critérios de projeto.
3. **P5:** incorporar o controlador de cargas à simulação energética e comparar perfis com/sem gerenciamento e cenários 24 h/48 h da DEC-005. Não contar a mesma energia solar ou o mesmo fluxo entre os bancos duas vezes.
4. **P1/P3:** registrar massa, preço, ventilação, espaço de instalação e manutenção do inversor/cabos, conforme ficha real.
5. **P7:** verificar dissipação térmica do inversor e ventilação do compartimento técnico; esta carga térmica pode afetar o dimensionamento da cabine.

### Condição de fechamento
Entregar tabela de simultaneidade real, estratégia de controle verificável, gráfico de carga AC/48 V versus tempo e energia diária, datasheets e checagem das capacidades contínua e de pico. Se não atender aos requisitos mesmo gerenciando cargas, reabrir seleção do inversor com justificativa. **DEC-001 (solar→tração) permanece pendente e NÃO é resolvida por DEC-019.**

## DEC-020 — Bateria de serviços independente da bateria de tração
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO A), SUJEITA À VALIDAÇÃO DE DIMENSIONAMENTO.** O sistema habitável deve operar com **bateria auxiliar de serviços de 48 V eletricamente independente da bateria de tração de alta tensão**, recebendo energia da **geração fotovoltaica**, sem utilizar a bateria de tração como fonte para geladeira, ar-condicionado, boiler, cozinha, lavadora/secadora ou demais cargas de habitação. Essa decisão **não** define a capacidade final do banco auxiliar, nem confirma a infraestrutura de carregamento solar da tração.

### Consequências arquiteturais obrigatórias
- **Não transferir energia entre os dois bancos de armazenamento** na configuração-base: nem tração → serviços, nem serviços → tração. Não supor conversores bidirecionais, V2L/V2H, acesso ao barramento HV, carregadores DC/DC entre baterias ou conexões autorizadas sem documentação. Uma eventual mudança requer nova decisão explícita.
- **A geração fotovoltaica deve ser alocada de modo físico e contabilizável.** As potências de 1.540 Wp de teto e 1.600 Wp de painéis portáteis (DEC-003) são capacidades de instalação, não energia simultaneamente disponível integralmente para serviços **e** tração. Se houver circuitos distintos ou comutação autorizada, os circuitos devem ser modelados e as frações de potência/energia separadas, sem dupla contagem.
- **Impacto explícito na DEC-001:** a alternativa A original de carregar a tração através de PV → bateria de serviços 48 V → inversor AC → EVSE → OBC **não é compatível com a independência adotada**, pois transfere energia armazenada no banco auxiliar para a tração. Não executá-la como arquitetura aprovada. P2 pode documentá-la historicamente na comparação, mas, para uma solução implementável sob a DEC-020, deve estudar uma alternativa de carregamento **independente do banco de serviços**, compatível com o carregador/interface OEM e com todas as proteções, ou demonstrar que não há solução comprovada. A alternativa B da DEC-001 permanece condicionada à interface segura e autorizada de carregamento HV; ligação direta ao pack é vedada como premissa de projeto.
- **Não confundir cargas de habitação com cargas operacionais do veículo.** Funções OEM do E-Ducato, como gerenciamento próprio de baixa tensão, permanecem sob a arquitetura original do fabricante; esta decisão trata da distribuição energética dos equipamentos adicionados ao motorhome.
- **Sem caminho PV → tração tecnicamente viável e confirmado, os itens 25 e 29 devem ter resultados 'condicionais/hipotéticos', sem alegar funcionamento exclusivamente solar validado.** O relatório deve apresentar separadamente viabilidade física e simulação idealizada.

### Tarefas atribuídas
1. **P2 — Responsável:** detalhar um diagrama elétrico unifilar com geração fotovoltaica, controladores MPPT, circuitos independentes, bateria auxiliar 48 V, inversor candidato Victron MultiPlus-II 48/5000, proteções, seccionamentos e limites de corrente/potência; identificar o que está comprovado e o que requer teste. Propor revisão das alternativas da DEC-001 sem ponte entre os bancos de baterias.
2. **P5:** modelar SOC da tração e SOC dos serviços como estados totalmente separados, com balanços de geração solar explicitamente alocados. Nos itens 25, 27 e 29, não creditar energia solar ao pack de tração se a interface de carregamento não estiver validada, exceto em cenários explicitamente marcados como condicionais.
3. **P6:** dimensionar o consumo e os picos da habitação, incluindo A/C, boiler e lavadora/secadora, conforme gerenciamento de cargas da DEC-019; entregar perfis de 24 h/48 h à DEC-005.
4. **P1/P3:** incluir no balanço de massa e no CAD a bateria auxiliar, seus suportes, inversor, cabos, proteções, eletrônica de potência, área dos painéis e eventuais módulos de carregamento independentes, com fontes reais (DEC-012).
5. **P7:** verificar gerenciamento térmico/ventilação de banco auxiliar, MPPTs e inversor, de acordo com os modelos efetivamente selecionados.

### Limites e pendências preservados
- **DEC-001:** conexão solar → tração NÃO resolvida; revisão de soluções é necessária em consequência da DEC-020.
- **DEC-003:** 1.540 Wp fixos + 1.600 Wp portáteis somente estacionado permanecem como configuração de referência.
- **DEC-005:** comparar capacidade para 24 h versus 48 h; 10,24 kWh continua hipótese inicial.
- **DEC-009, DEC-010, DEC-011 e DEC-013:** variantes de velocidade, A/C, agenda de paradas e reservas da viagem continuam em comparação.
- **DEC-014:** autonomia diária do item 27 usa 100%→30% como principal e 80%→30% como sensibilidade, sem alterar SOC da missão do item 29.
- **DEC-019:** gerenciar simultaneidade, mantendo o inversor atual apenas como candidato.

### Próxima pergunta a deliberar (DEC-021)
Definir a política de **alocação da energia dos painéis solares entre circuitos independentes de serviços e, se tecnicamente possível, recarga da tração**, respeitando a DEC-003 e a independência da DEC-020. Não declarar uma configuração PV→tração viável até sua validação.

## DEC-021 — Comparar alocação fixa e flexível da geração fotovoltaica sem interligar os bancos
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; CONFIGURAÇÃO FINAL PENDENTE DE VALIDAÇÃO TÉCNICA.** O usuário decidiu **comparar a alocação fixa dos painéis solares entre serviços e tração e estudar uma alocação flexível com circuitos independentes e comutação segura, SEM interligar as baterias de tração e serviços**. Trata-se de autorização para estudo comparativo, não aprovação de qualquer conexão PV→tração ainda não demonstrada.

### Configurações a comparar
1. **Cenário A — fixos para serviços; portáteis para tração:** 1.540 Wp de teto destinados ao banco de serviços 48 V; 1.600 Wp portáteis destinados à eventual recarga solar da tração **somente quando estacionado** e apenas se houver circuito/interface validado.
2. **Cenário B — fixos para tração; portáteis para serviços:** 1.540 Wp de teto destinados à eventual recarga da tração com interface comprovada; 1.600 Wp portáteis destinados ao banco de serviços 48 V **somente quando estacionado**. Verificar especialmente a autonomia dos equipamentos durante condução, sem geração portátil.
3. **Cenário C — alocação flexível:** investigar possibilidade de comutar ou particionar os **circuitos de geração fotovoltaica** entre entradas de carregamento independentes e adequadas, com seccionamento, proteção, MPPT compatíveis, prevenção de retorno de corrente e operação segura. **Não** conectar entre si a bateria auxiliar e o pack HV, **não** presumir barramento DC compartilhado nem conectar diretamente um arranjo PV à bateria HV. A comutação, se proposta, requer especificação física, componentes comerciais/documentados e avaliação das transições.
4. **Cenário de controle sem recarga PV→tração comprovada:** simular a geração abastecendo somente os serviços e apresentar como cenário fisicamente suportável apenas o que estiver efetivamente validado; eventuais ganhos de SOC da tração por PV ficam rotulados **hipotéticos/condicionais**.

### Restrições herdadas que NÃO mudaram
- **DEC-003:** 1.540 Wp fixos no teto + 1.600 Wp portáteis apenas parado são capacidades STC; não equivalem a fornecimento contínuo dessa potência. Registrar orientação, sombreamento, temperatura, perdas e montagem dos painéis portáteis.
- **DEC-020:** independência elétrica entre bateria de serviços de 48 V e bateria de tração HV; **nenhuma transferência de energia armazenada entre os bancos**, nem via inversor/EVSE/OBC. Circuitos de PV separados e uma eventual chaveamento da fonte de geração não são autorização de conexão entre baterias.
- **DEC-001:** nenhuma interface PV→tração foi aprovada. O trajeto PV→bateria de serviços→inversor→EVSE→OBC original (alternativa A antiga) **continua incompatível** com DEC-020. Reavaliar somente interfaces independentes viáveis, autorizadas e documentadas; em especial requisitos mínimos de potência/corrente de OBC/EVSE e/ou protocolos e proteções de carga DC. Não assumir que 1,54 ou 1,60 kWp alimentem continuamente o carregador de tração em condições operacionais.
- **DEC-006/007/011/013/014:** manter item 29 principal a 7.000 km, até 8 h de direção/dia, sem carga externa, cronogramas fixo/otimizado e cenários meteorológicos distintos, com limites de SOC do item 29 próprios; item 27 mantém 100%→30% principal e 80%→30% na sensibilidade.
- **DEC-005/012/019:** dimensionar serviços para 24 h versus 48 h, usar componentes reais e verificar gerenciamento de cargas e inversor, sem contabilização duplicada.

### Entregáveis para o Codex e a equipe
1. **P2 — responsável elétrico:** desenhar **três diagramas de potência** (A, B, C), incluindo arranjos, MPPTs, isolamento, proteções, comutação (se existir), interfaces de carregamento reais e limites OEM. Explicitar, para cada um, componentes *comprovados*, *a validar* e *incompatíveis*; obter potência mínima e faixa operável de eventual carregador da tração antes de aceitar recarga solar real.
2. **P5 — modelagem energética:** implementar balanço horário das duas baterias com variáveis e SOC separados. Para cada intervalo, impor `E_PV_gerada = E_PV_serviços + E_PV_tração + E_perdas + E_cortada` (com as eficiências e locais das perdas corretamente definidos), sem usar a mesma energia duas vezes. Portáteis = 0 durante movimento. Simular alocação A, B, flexível e cenário-controle nas mesmas condições de irradiação/cargas e programação de paradas (DEC-011).
3. **P1/P3:** comparar massa, custo, volumes, suportes, cabos, proteções, inversores/carregadores e espaço do teto/compartimentos no CAD L3H2; verificar interferências entre PV, A/C, ventilação e fixações.
4. **P6/P7:** fornecer demanda horária da habitação e perdas/calor gerado pelos equipamentos de conversão, validando ventilação e temperaturas.
5. **Revisão humana conjunta P2/P5:** apresentar tabela das três arquiteturas com geração útil e/ou curtailment, energia entregue separadamente a cada banco, perdas, custos, massas, viabilidade documental, condições de operação e efeitos em dias necessários à missão. **Não escolher vencedor apenas por maior kWh simulado se o hardware não for verificavelmente compatível.**

### Condições para fechar DEC-021
- Caminho elétrico real e compatível para cada fluxo selecionado; comutação segura comprovada por datasheets, diagrama, proteções e integração OEM.
- Demonstrar que não há transferências de energia entre os bancos e nenhuma dupla contagem solar; indicar falhas por potência mínima de carga ou ausência de interface.
- Se nenhuma opção de PV→tração puder ser validada, registrar formalmente a **limitação de viabilidade** dos itens 25 e 29, separando o resultado idealizado do comprovadamente implementável, sem alegar viagem 7.000 km exclusivamente solar como viável.
- **Pendente:** distribuição física final, lógica de chaveamento, modelos comerciais, interface PV→tração e vencedor da comparação. Nenhum desses pontos foi automaticamente aprovado nesta decisão.

### Próxima pergunta a deliberar (DEC-022)
Definir o **critério de viabilidade de massa total e carga por eixo** para a van L3H2 habitável (ocupantes, água, painéis, baterias, A/C, lavadora, boiler, sanitário, mobiliário e cabos), respeitando a variante/PBT OEM ainda pendente da DEC-002.


## DEC-022 — Comparação entre massa operacional típica e massa máxima admissível
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; MASSAS E VARIANTE FINAIS PENDENTES DE VALIDAÇÃO.** Comparar **massa operacional típica** e **massa máxima fisicamente admissível** da configuração habitável E-Ducato L3H2, avaliando **autonomia, aceleração, frenagem, PBT e cargas por eixo**, **sem dupla contagem de água**. Essa autorização não homologa a massa do motorhome nem fixa a versão comercial do veículo (DEC-002).

### Cenários obrigatórios
1. **Massa operacional típica (cenário principal comparativo):** incluir massa em ordem de marcha de variante OEM efetivamente identificada, motor/bateria originais, conversão habitável completa, painéis solares e suportes, bateria de serviços, equipamentos elétricos e térmicos, mobiliário, isolamento, chuveiro, boiler, lavadora/secadora, cassete sanitário e conteúdo, 2 ocupantes de 80 kg cada, 60 kg totais de bagagem e até 100 L de água limpa no início da missão. Registrar explicitamente quais tanques estão cheios e vazios, massa e localização por componente.
2. **Massa máxima fisicamente admissível (caso-limite):** estudar o maior carregamento operacional plausível **dentro** do PBT e das cargas máximas por eixo da variante homologada, incluindo distribuições críticas de ocupantes, água, bagagem, equipamentos e conteúdo dos reservatórios. Se a configuração proposta exceder PBT/eixo, **informar inviabilidade e excesso calculado** em vez de inventar uma massa máxima permitida. Não tratar a soma de todos os reservatórios completamente cheios como uso normal sem justificar a origem da água e a capacidade de carga.
3. **Casos intermediários e sensibilidade:** verificar redistribuição de água durante o uso, bagagens e ocupantes; calcular centro de gravidade longitudinal/vertical, carga estática por eixo e casos críticos de frenagem, com modelos e hipóteses declarados.

### Conservação de massa e de água
- **DEC-008:** 2 × 80 kg de ocupantes, 60 kg de bagagem, reservatório de água limpa de 100 L, águas cinzas de 70 L e águas negras de aproximadamente 20 L. Uma estimativa de carga inicial é **320 kg** para ocupantes + bagagem + 100 L de água limpa, **sem** contabilizar massas dos recipientes, móveis, equipamentos ou outros componentes. Densidade 1 kg/L é aproximação para água; registrar fonte/temperatura se exigir precisão.
- **DEC-018:** o cassete removível **é o próprio reservatório de águas negras de ~20 L**. Não somar outro tanque negro fictício de 20 L.
- **Não somar repetidamente a mesma água:** ao migrar do tanque limpo para o cinza ou para o cassete, a água muda de posição e de reservatório, não é criada. Água potável acrescentada por abastecimento externo mudaria a massa, mas esse abastecimento não deve ser implicitamente tratado como recarga energética da bateria na missão solar.
- Para o caso de água simultaneamente em mais de um tanque, documentar o balanço de entradas/saídas, uso da água, eventual descarte e capacidade efetiva; respeitar limites de carga reais.

### Entregáveis e responsáveis
1. **P1 — responsável pela massa e segurança:** montar planilha de massas rastreável (peça/modelo, quantidade, massa, fonte, posição x/y/z no veículo, momento em relação aos eixos, massa total, PBT, cargas por eixo e margens). Separar massa do veículo-base, estrutura e conversão, passageiros/carga variável. Não assumir tara homologada de versão distinta.
2. **P3 — CAD:** atribuir massas e posições aos equipamentos no CAD L3H2, extrair centro de gravidade e verificações de embalagem; conciliar modelo CAD e planilha de massas e registrar estimativas não confirmadas.
3. **P4 — dinâmica e desempenho:** repetir para ambos os casos os cálculos de resistência ao rolamento, força de tração, consumo/alcance, aceleração e frenagem; explicitar efeito da massa e da distribuição de carga. Na condição de variante limitada a 90 km/h (DEC-009), não alegar 0–100 km/h exequível.
4. **P5 — autonomia e missão:** usar os mesmos cenários de massa nos itens 25, 26, 27 e 29, registrando diferenças de km/kWh, geração solar necessária, SOC e tempo de viagem. Manter claramente condicionais os resultados que dependem de recarga PV→tração não validada (DEC-001/021).
5. **P2/P6/P7:** fornecer as massas efetivas ou intervalos e fichas técnicas de baterias, elétrica, interiores, isolamento, refrigeração e suas posições, compatíveis com a seleção realista da DEC-012.

### Critérios para fechar a análise
- Identificação da variante OEM e documentação **da mesma variante** para PBT, massa em ordem de marcha, limites por eixo, entre-eixos, especificações de motor/bateria e limites operacionais; não misturar fichas de versões diferentes.
- Quadro comparativo por cenário com massa total e margens de PBT/eixos, centro de gravidade, parâmetros de desempenho, frenagem, autonomia e consumo energético.
- Se a conversão ultrapassar os limites, recomendar uma revisão verificável da lista de materiais/equipamentos ou da variante, sujeita a nova aprovação, e **não** ocultar a inviabilidade.

**Pendente após DEC-022:** valores finais de massas, variante homologada, distribuição por eixo, viabilidade do pacote habitável e comparação quantitativa. Mantidas **todas** as decisões DEC-001 a DEC-021, inclusive arquitetura solar→tração e demais comparações ainda abertas.

### Próxima pergunta a deliberar (DEC-023)
Definir o grau de **verificação aerodinâmica e convergência de malha do CFD** antes de adotar o coeficiente de arrasto do veículo como parâmetro de autonomia e dinâmica. O Cd atual de simulações preliminares não deve ser declarado validado sem estudo de convergência e conferência geométrica.

## DEC-023 — Refinamento progressivo e quantificação de incerteza do CFD aerodinâmico
**Status: APROVADA PELO USUÁRIO EM 28/10/2026; Cd FINAL PENDENTE DE CONVERGÊNCIA E VALIDAÇÃO.** Realizar **refinamento progressivo do CFD com pelo menos três malhas**, verificar as condições de contorno e quantificar as incertezas. **Se a convergência não for suficiente, apresentar uma faixa de coeficientes de arrasto (Cd), e NÃO um valor definitivo.** Essa decisão estabelece método de verificação; não valida os resultados preliminares.

### Procedimento exigido para P3 — CAD e CFD
1. **Geometria e domínio:** identificar exatamente a variante geométrica CAD E-Ducato L3H2 da DEC-002, incluindo dispositivos habitáveis instalados, efeito dos painéis fixos, tomadas de ar e outros apêndices externos. Documentar simplificações, área frontal de referência (A), sistema de coordenadas, domínio, velocidade do ar, temperatura, densidade, modelo de turbulência e condições de entrada/saída, laterais, teto e piso. Modelar adequadamente solo/rodas ou registrar e quantificar a limitação da simplificação escolhida.
2. **Estudo de malha com pelo menos três níveis:** executar malhas progressivamente refinadas (grossa, intermediária, fina) com parâmetros e número de células documentados; verificar qualidade de elementos, camadas de parede e resolução apropriada ao tratamento de turbulência (`y+`, se aplicável). Usar condições físicas e critérios de convergência do solucionador compatíveis entre os testes. Registrar históricos de resíduos e estabilidade de Cd/forças, não apenas atingir um número arbitrário de iterações.
3. **Convergência de malha e incerteza:** calcular Cd por malha, variação relativa entre malhas e, quando justificável, estimativa da incerteza numérica por extrapolação/GCI. Não confundir estabilidade numérica com validação contra realidade. Identificar incertezas de geometria, área frontal, modelo de turbulência e contornos; comparar valores com fontes documentadas apenas quando representarem geometrias e condições comparáveis.
4. **Entrega condicional:** se a malha mais refinada não indicar independência de malha suficiente para a finalidade do projeto, **não promover qualquer Cd isolado a valor validado**. Informar intervalo/faixa de Cd com justificativa técnica, limitações e plano de refinamento, sem inventar convergência ou erro percentual universalmente aceitável.
5. **Reprodutibilidade:** registrar geometria/versão, arquivos de malha, configuração de solver, condições de contorno, logs, critérios de parada, máquinas/tempos relevantes e scripts de extração de Cd; salvar curvas e tabelas identificando versões.

### Efeitos nos outros responsáveis e decisões
- **P4 — dinâmica:** aplicar Cd, área frontal e densidade coerentes para força de arrasto (`F_D = 0,5·ρ·Cd·A·v_rel²`) nos itens de velocidade e aceleração. Se houver faixa de Cd, propagar mínimo/central/máximo nos resultados e declarar limitações do caso a 90 km/h (DEC-009).
- **P5 — autonomia:** avaliar sensibilidade do consumo e km/kWh a 40 e 80 km/h, da autonomia diária (item 27) e do tempo da missão 7.000 km (item 29) à faixa de Cd; não ocultar incerteza aerodinâmica com um único resultado. Manter a recarga solar da tração como tecnicamente NÃO validada enquanto DEC-001/021 estiverem abertas.
- **P1/P3:** assegurar que a geometria externa usada no CFD corresponde à configuração e massas/CAD analisados, com especial atenção à instalação real dos painéis, ar-condicionado e ventilação (DEC-003, 010, 016, 022).
- **DEC-012:** usar dados documentados e hipóteses rastreáveis, evitando números simulados apresentados como medições ou especificações do fabricante.

**Pendente após DEC-023:** executar/validar três ou mais malhas, conferir domínio e condições de contorno, quantificar a variação do Cd e incerteza residual; escolher um Cd final apenas se sustentado pelos resultados. Mantidas integralmente DEC-001 a DEC-022 e todas as comparações ainda não resolvidas.

### Deliberação DEC-024 concluída em 28/10/2026
Foi aprovada a combinação de referência OEM documentada com modelagem térmica parametrizada; consultar a DEC-024 abaixo. Os componentes e parâmetros finais do circuito ainda dependem de validação.

## DEC-024 — Modelo térmico da bateria de tração e circuito de arrefecimento
**Status: APROVADA PELO USUÁRIO EM 28/10/2026 (OPÇÃO C), COM DIMENSIONAMENTO E VALIDAÇÃO FINAL PENDENTES.** Utilizar o **sistema térmico OEM do Fiat E-Ducato como referência documentada** e desenvolver **modelo térmico parametrizado** para os casos de carregamento de **20 kW e 80 kW**, contemplando bateria, bomba, radiador, vazão e temperaturas, com todas as hipóteses e incertezas explicitadas. O modelo conceitual não deve ser declarado reprodução fiel ou validação do sistema OEM sem documentação e evidências.

### Escopo técnico obrigatório — itens 34 e 35
1. **Referência do fabricante:** identificar variante exata do E-Ducato e levantar documentação disponível sobre pack, capacidades, tensões, gerenciamento térmico, faixa de temperaturas e recursos de carregamento; usar apenas informação aplicável à variante e não transferir especificações de outras versões sem identificação. A DEC-002 permanece aberta quanto à variante final.
2. **Geração de calor na bateria:** modelar a energia térmica associada à corrente e perdas internas durante os ensaios de carga **20 kW e 80 kW**; parametrizar resistência interna, perdas por módulos, capacidade térmica, massa, geometria e eficiência de acordo com dados documentados ou faixas plausíveis identificadas como estimativas. Considerar dependência de SOC e temperatura quando houver base para isso, sem inventar curvas OEM.
3. **Modelo transiente e distribuição de temperatura:** calcular evolução da temperatura e, quando viável, distribuição espacial de temperaturas (modelo de múltiplos nós, volumes finitos, FEM ou equivalente) com condições iniciais/de contorno documentadas; distinguir temperatura média, máxima e gradientes e registrar limites de validade.
4. **Circuito hidráulico/térmico:** dimensionar de modo conceitual vazão do fluido, trocas de calor, radiador, perdas de carga, bomba (curva H×Q e ponto de operação), tubulações, fluido e potência elétrica auxiliar. Quando fichas técnicas não identificarem componentes OEM, selecionar **componentes comerciais reais** apenas como candidatos para o modelo, sem atribuí-los ao E-Ducato original.
5. **Validação e sensibilidade:** comparar o modelo com referências físicas/documentadas apropriadas, quando existentes, e executar sensibilidade à resistência interna, coeficientes de troca, vazão, temperatura ambiente, potência de carregamento e propriedades térmicas. Não declarar temperaturas como medições OEM sem evidência; distinguir incerteza de parâmetro, aproximação numérica e extrapolação.
6. **Balanço energético e acoplamento:** contabilizar calor gerado, retirado pelo fluido/radiador, armazenado na bateria e potência consumida por bomba/ventiladores. Integrar consumos auxiliares nos resultados energéticos compatíveis, evitando dupla contagem.

### Restrições e compatibilidade com decisões existentes
- **20 kW e 80 kW** são condições prescritas para o **ensaio térmico do item 34**; não significam capacidade de fornecimento dos painéis solares de **1.540 Wp fixos + 1.600 Wp portáteis** nem permitem recarga externa no cenário da viagem do item 29. A DEC-003, DEC-006, DEC-020 e DEC-021 continuam vigentes.
- **Não confundir o circuito térmico da bateria de tração com o sistema de serviços 48 V**, que segue independente da tração por DEC-020. A modelagem da bomba/ventoinha deve identificar qual sistema elétrico efetivamente a alimenta e se o componente é OEM ou adicional.
- **DEC-001 (solar→tração) segue PENDENTE.** O ensaio térmico a 20/80 kW não valida a interface de carregamento solar HV, nem cria um elo elétrico entre bancos.
- **DEC-012:** fichas reais e fontes identificáveis como primeira escolha; parâmetros ausentes devem ter faixa estimada e análise de sensibilidade. Não apresentar números próprios como dados oficiais.

### Responsabilidades e entregáveis
- **P7 — responsável principal:** modelo de geração/distribuição de calor e circuito de arrefecimento; cálculos de carga 20/80 kW, curva de temperatura × tempo, mapas/gradientes térmicos quando possíveis, dimensionamento e ponto de operação da bomba, vazões, radiador e sensibilidade.
- **P2:** dados elétricos do pack e carregamento aplicáveis à variante, perdas, SOC e limitação de temperatura, integração do consumo dos componentes auxiliares, identificação de proteções e condições operacionais.
- **P3:** geometria representativa/volumes térmicos quando necessária modelagem dimensional, com identificação dos elementos OEM conhecidos e das simplificações.
- **P1/P5:** massas/custos/consumo dos dispositivos adicionais (se houver), coerência com balanços de massa e energia e cenários aprovados.
- **Relatório:** tabela fonte × parâmetro × valor/intervalo × nível de confiança; esquema do circuito, equações, condições iniciais e de contorno, gráficos e discussão das limitações, distinguindo **OEM documentado**, **modelo conceitual** e **hipótese sensível**.

**Pendente após DEC-024:** variante OEM, curvas e parâmetros finais, eventual correspondência do circuito com o veículo real, resultados térmicos dos itens 34 e 35, seleção de bomba/radiador e verificação de faixas seguras. Preservadas integralmente DEC-001 a DEC-023 e todas as comparações não resolvidas.

### Próxima pergunta a deliberar (DEC-025)
Definir a estratégia de modelagem multidimensional do sistema de **freios para o item 33**: frenagem de 30 m/s para 10 m/s em 5 segundos, inicialmente a 25 °C, comparando uma geometria/material reais documentados e um modelo térmico parametrizado com estudo de sensibilidade; distinguir energia dissipada em freios de eventuais parcelas recuperadas pela frenagem regenerativa, que não devem ser presumidas sem dados e condições de controle.

## DEC-025 — Comparação térmica da frenagem por atrito e regenerativa (item 33)
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; DISTRIBUIÇÃO FINAL DE TORQUE, GEOMETRIA E RESULTADOS TÉRMICOS PENDENTES DE VALIDAÇÃO.** O usuário decidiu **comparar frenagem inteiramente por atrito com cenários de frenagem regenerativa tecnicamente limitados**, realizando uma **análise térmica multidimensional dos freios para desaceleração de 30 m/s para 10 m/s em 5 segundos, iniciando a 25 °C**, com hipóteses e incertezas explícitas. A decisão aprova ambos os cenários de estudo; **não** confirma que o veículo OEM consiga aplicar um torque regenerativo específico durante todo o evento.

### Casos obrigatórios
1. **Caso A — frenagem por atrito, regeneração indisponível:** representar o pior caso conservador de demanda de freios mecânicos, contabilizando separadamente perdas aerodinâmicas e de rolamento, quando incluídas, para não imputar toda a variação de energia cinética aos discos sem balanço de energia. Verificar eventual limite de aderência e estabilidade. Utilizar geometria, material, dimensões, massa e propriedades termofísicas documentadas do disco/pastilhas da variante OEM quando disponíveis; caso contrário, marcar explicitamente o modelo como paramétrico/representativo.
2. **Caso B — frenagem com regeneração limitada:** estudar frações/curvas de potência e torque regenerativo **somente na faixa fisicamente compatível** com motor, inversor, bateria, SOC, temperatura e velocidade. Não presumir porcentagem fixa como desempenho OEM sem fonte; quando faltarem curvas, executar *cenários hipotéticos de sensibilidade*, rotulados como tal. A parcela de frenagem por atrito deve ser calculada pela diferença entre demanda de desaceleração e forças resistivas/regeneração disponíveis, respeitando limites de aderência e distribuição entre eixos.
3. **Comparação em condições iguais:** mesma massa operacional e casos-limite da DEC-022, velocidades inicial/final e duração prescritas, temperatura inicial **25 °C**, geometria/materiais e condições de contorno equivalentes. Comparar energia dissipada por eixo/disco, picos de temperatura, mapas de temperatura, gradientes, incertezas, e parcela regenerada efetiva; verificar casos com regeneração indisponível por SOC elevado ou limitação térmica, quando documentado.

### Modelo de física e verificação
- **Balanço básico:** `ΔE_c = 0,5*m*(30² - 10²) = 400*m J`, para massa total `m` em kg, antes de separar recuperação elétrica, dissipação aerodinâmica/rolamento, perdas mecânicas e calor nos freios. A desaceleração média pedida é `(30 - 10)/5 = 4 m/s²`; o perfil real de força/potência deve ser coerente com massa, inclinação assumida e velocidade variável.
- **Análise multidimensional:** modelar pelo menos um disco representativo com condução transiente espacial (2D axissimétrica ou 3D, justificando o nível), fluxo térmico por atrito na(s) superfície(s), convecção/radiação, condição inicial 25 °C e propriedades dependentes da temperatura quando houver dados. Distinguir simulação térmica detalhada do disco de um mero cálculo lumped `Q/(m*c_p)`; caso a representação de pastilha/contato seja simplificada, documentá-la.
- **Repartição da frenagem:** especificar hipóteses de repartição dianteira/traseira, números de discos e limites de torque/aderência, incluindo transferência dinâmica de carga quando pertinente; evitar dividir igualmente a energia entre quatro rodas sem justificativa.
- **Estudo numérico:** executar checagem de malha e de passo temporal, balanço de energia e sensibilidade a coeficiente convectivo, partição de fluxo, massa, propriedades de materiais e regeneração. Não atribuir a resultados de modelo conceitual status de ensaio OEM validado.

### Responsáveis e entregas
- **P1 — responsável:** geometria e materiais dos freios; distribuição de esforços por eixo; modelo térmico multidimensional, curvas `T_max(t)` e mapas/gradientes de temperatura; estudo de sensibilidade e incerteza; comparação entre cenários e verificação de requisitos do item 33.
- **P4 — apoio de dinâmica e regeneração:** perfil temporal de desaceleração, potência e torque nas rodas, participação de recuperação, limites de velocidade/torque e bateria, balanço mecânico–elétrico coerente. Só usar dados OEM da **variante efetivamente identificada**; DEC-009 permanece sem variante definitiva.
- **P2 — apoio elétrico:** limites do pack, SOC, inversor e potência receptiva/recuperável; distinguir recuperação teórica de energia efetivamente aceita na bateria. Não usar a bateria de serviços 48 V como sumidouro da regeneração (DEC-020).
- **P3/P5 — interfaces:** consistência de geometria/massa com CAD e de parcela de energia recuperada nos modelos de autonomia; impedir dupla contagem da energia regenerada e de perdas.

### Compatibilidade e pendências preservadas
- **DEC-008/022:** as massas dos cenários dependem de configurações reais verificadas; não congelar massa/PBT sem confirmação.
- **DEC-012/023/024:** manter documentos e parâmetros rastreáveis, convergência numérica e incertezas; a convergência do CFD aerodinâmico é separada da validação térmica dos freios.
- **DEC-001/020/021:** frenagem regenerativa abastece o sistema OEM de **tração**, quando admitida pelo fabricante, não autoriza conexão à bateria de serviços nem valida recarga solar de tração.
- **Pendente:** identificar variante e discos OEM, parâmetros termofísicos, torque regenerativo justificável, distribuição de frenagem, resultados de temperatura e verificações de sensibilidade. Nenhum desses resultados foi aprovado antecipadamente.

### Próxima pergunta a deliberar (DEC-026)
Definir quais circuitos de **cabos elétricos** terão prioridade na simulação térmica multidimensional do item 30, distinguindo cabos do banco auxiliar 48 V/inversor, condutores fotovoltaicos e cabos HV OEM documentados, e estabelecendo cenários de corrente, temperatura ambiente, instalação e proteção sem inventar capacidades admissíveis.


## DEC-026 — Análise térmica multidimensional dos cabos de serviços 48 V e avaliação fotovoltaica (item 30)
**Status: ESCOPO DE SIMULAÇÃO APROVADO PELO USUÁRIO EM 28/10/2026; SEÇÕES, COMPONENTES, RESULTADOS E LIMITES DE TEMPERATURA A VALIDAR.** O usuário decidiu **realizar análise térmica multidimensional detalhada dos cabos de maior exigência entre a bateria de serviços de 48 V e o inversor, complementada por avaliação térmica dos cabos fotovoltaicos**, considerando componentes reais, cenários de corrente, seção dos condutores, condições de instalação e incertezas. **Manter os cabos de alta tensão (HV) originais do veículo sem alterações.** A decisão fixa o escopo de estudo, não certifica antecipadamente qualquer seção de cabo, corrente admissível ou configuração elétrica.

### Ensaio principal — bateria auxiliar de 48 V → inversor
1. **Identificação do circuito:** traçar bateria de serviços → dispositivos de seccionamento/proteção → cabos positivo/retorno → terminais do inversor candidato (Victron MultiPlus-II 48/5000 sujeito à DEC-019). Validar tensão real e faixa operativa da bateria, comprimentos positivos/negativos, tipo de material condutor, bitola/seção, isolamento, terminações e passagem física no CAD; não assumir que 5.000 VA correspondem a 5.000 W contínuos.
2. **Cenários de corrente e uso:** calcular corrente do lado DC com a potência elétrica **real de entrada**, rendimento, tensão sob carga, SOC e temperatura; ensaiar carga normal contínua, condição mais severa admissível de operação e transitórios/picos documentados, diferenciando os limites do inversor, da bateria e das proteções. Conciliar com gerenciamento de cargas aprovado na DEC-019.
3. **Modelo multidimensional:** realizar condução térmica espacial 2D ou 3D (justificar escolha, particularmente para terminais/conexões), incluindo aquecimento por efeito Joule `I²R`, variação da resistividade com temperatura, camadas de isolamento, condições de contato, dissipação por condução/convecção/radiação pertinentes e restrições de ventilação/agrupamento dos cabos. Avaliar condição de regime permanente e resposta transiente quando pertinente, com malha e passo temporal verificados.
4. **Resultados e segurança:** entregar mapas de temperatura, pontos críticos, `T_max` para condutor e isolamento, queda de tensão, perdas energéticas, comparação de seções comerciais e margens frente às especificações documentadas dos materiais e às regras de instalação aplicáveis. Verificar capacidade de condução, dispositivo de proteção e coordenação, sem inferir certificação apenas de uma simulação térmica.

### Análise complementar — cabos fotovoltaicos
- Analisar os trechos dos painéis fixos e, quando efetivamente utilizados em estacionamento, portáteis, até os controladores/conversores correspondentes; considerar arranjos série/paralelo, tensões e correntes documentadas, rota e comprimento de cabos, sombreamento/exposição solar, temperatura externa, proteções e conexões.
- Simular ou estimar com método físico documentado temperaturas e perdas dos cabos fotovoltaicos, incluindo cenários de exposição e agrupamento, em detalhe proporcional à relevância para o balanço energético. Não exigir que a avaliação secundária tenha necessariamente a mesma complexidade tridimensional do ensaio principal, mas explicitar qualquer simplificação.
- **DEC-001 e DEC-021 seguem abertas:** um trecho fotovoltaico destinado hipoteticamente à tração NÃO comprova a existência de interface segura de recarga HV. Evitar dupla contagem de energia e correntes entre os circuitos independentes.

### Restrições, verificações e atribuições
- **Sem alteração no cabeamento HV OEM da tração** e sem conexão direta aos terminais do pack, respeitando a independência entre baterias da DEC-020. Usar parâmetros HV somente como documentação de referência se necessário; qualquer integração solar–tração continua condicionada à DEC-001.
- Empregar **componentes reais com fichas técnicas** quando possível; não apresentar seção, amperagem ou classes térmicas arbitradas como homologadas (DEC-012). Adotar a condição ambiental-base do enunciado para simulações aplicáveis e acrescentar cenários quentes de sensibilidade quando necessários para segurança.
- **P2 — responsável principal:** definição de circuito, materiais, parâmetros elétricos e térmicos, condução dos casos detalhados e verificação de proteções/temperaturas. **P3:** roteamento e instalação no CAD, dimensões e afastamentos reais; **P5:** perdas nos balanços de energia/autonomia; **P1:** massa, custo e lista de componentes; **P7:** suporte em condições de dissipação e modelagem térmica se necessário.
- Entregar tabelas `componente/fonte/dados/hipótese`, esquema do circuito, modelo multidimensional e parâmetros de malha, curvas `T(t)` quando aplicáveis, mapas de temperatura, quedas de tensão, perdas, análise de seção e incertezas. Nenhum resultado térmico é considerado validado antes de convergência e cotejo com dados admissíveis de fabricantes.

**Pendente após DEC-026:** identificação do circuito/bitola comercial exatos, modelagem das conexões, distâncias no CAD, regime de carga/picos, propriedades térmicas, condições de instalação, resultados da análise e compatibilidade com normas aplicáveis. Preservadas DEC-001 a DEC-025, incluindo todas as comparações pendentes.

### Próxima pergunta a deliberar (DEC-027)
Definir a abordagem de simulação do **item 31** (motorhome fechado e estacionado ao meio-dia, sem ocupantes e sem ar-condicionado): modelo transiente de balanço térmico com radiação solar e transferência por paredes, teto e vidros versus CFD térmico tridimensional com convecção interna, ou uma metodologia combinada com validação e sensibilidade; manter cenário de clima fixado pela DEC-007 e isolamento previsto na DEC-016.

## DEC-027 — Modelo térmico transiente com CFD 3D complementar para cabine fechada (item 31)
**Status: METODOLOGIA APROVADA PELO USUÁRIO EM 28/10/2026; PROPRIEDADES, CONDIÇÕES INICIAIS, RESULTADOS E VALIDAÇÃO AINDA PENDENTES.** O usuário decidiu **combinar um modelo térmico transiente da manhã até o meio-dia com CFD tridimensional complementar da cabine**, considerando radiação solar, isolamento, vidros, convecção natural, convergência e incertezas. A condição do item 31 permanece **motorhome estacionado, fechado, sem ocupantes e sem ar-condicionado**. Utilizar as condições meteorológicas fixadas no enunciado para São Carlos: **céu limpo em 21/06, temperatura externa de 25 °C, umidade relativa de 50% e vento externo nulo**, observando a localização e altitude pertinentes.

### Metodologia obrigatória — evolução térmica até o meio-dia
1. **Balanço térmico transiente:** construir modelo fisicamente consistente de capacidades e resistências térmicas (ou método energético equivalente) para ar interno, teto, paredes, piso, vidros e principais elementos com inércia térmica. Contabilizar condução, convecção natural, radiação de onda curta/longa quando relevante e trocas com o exterior, indicando simplificações e acoplamentos entre partes.
2. **Radiação solar e geometria:** calcular a trajetória/irradiância solar para a localização de São Carlos no dia 21/06, distinguindo hora civil de hora solar; aplicar incidência por orientação da carroceria, transmissividade/absorção dos vidros, sombreamento, proteções solares e presença física de painéis no teto, sem usar potência FV como se fosse diretamente calor absorvido pela cabine. Registrar orientação do veículo ou fazer análise de sensibilidade à orientação.
3. **Configuração física aprovada:** utilizar materiais comerciais e espessuras justificadas do isolamento de teto, paredes e piso, e proteção solar dos vidros conforme DEC-016; modelo e espessura ainda precisam de documentação. Considerar pontes térmicas, janelas, portas e eventuais condições reais de vedação, sem inventar especificações OEM.
4. **Condição inicial e horário:** declarar instante inicial da manhã e temperaturas iniciais do ar e das superfícies (ou condições prévias explicitamente justificadas); executar evolução temporal até o **meio-dia** da definição adotada e entregar `T_ar(t)`, temperaturas de superfícies e temperaturas ao meio-dia. Não assumir temperatura interna inicial igual à externa sem justificar; quantificar sensibilidade a condições iniciais.
5. **Condição fechada, desocupada e sem A/C:** zero aporte de calor metabólico e zero potência do climatizador; não impor troca forçada de ar ou abertura de janelas. Qualquer infiltração residual por frestas deve ser modelada com justificativa e sensibilidade, especialmente porque o vento especificado é zero. Separar cuidadosamente de eventuais fontes térmicas internas existentes e justificadas.

### CFD tridimensional complementar
- Produzir ou aproveitar geometria simplificada fiel ao CAD do E-Ducato L3H2 com isolamento e vidros relevantes, estabelecendo **convecção natural/empuxo** no ar interno, condução e condições térmicas de superfície compatíveis com o modelo transiente no instante do meio-dia. Explicitar o tratamento de radiação no CFD ou a forma pela qual os fluxos radiativos entram como condições de contorno.
- Entregar **mapas espaciais** de temperatura de ar e superfícies, estratificação térmica e zonas de maior aquecimento ao meio-dia; distinguir temperatura pontual, temperatura média de volume e indicadores de conforto/operabilidade quando utilizados.
- Verificar malha, resíduos, conservação de energia, acoplamento térmico e, se transiente, passo temporal; apresentar convergência e análise de sensibilidade das propriedades de isolamento, vidros, orientação, absortividade, condição inicial e infiltração. Usar comparação entre modelos como verificação de consistência, **não como validação experimental OEM**.
- Se não houver convergência ou dados suficientes, reportar **faixas de temperatura** e limitações, sem apresentar estimativa isolada como resultado definitivo validado.

### Integração, responsáveis e fronteiras
- **P6 (responsável principal):** modelo térmico transiente, condições solares/ambientais, materiais e cargas térmicas; preparar temperatura interna ao meio-dia e análises de sensibilidade.
- **P3 (CFD/CAD):** malha e modelo 3D da cabine, condições de contorno, mapas e testes de convergência; manter coerência com o CAD que será validado.
- **P5:** fornecer incidência e sombreamentos solares coerentes com os painéis fixos/portáteis (portáteis não são assumidos em operação no ensaio da cabine estacionada salvo configuração explicitada) e não contabilizar absorção e geração fotovoltaica duas vezes.
- **P1/P2:** conferir materiais, massa, características construtivas e eventuais fontes elétricas modeladas quando houver justificativa.
- **Item 31 versus item 32:** NÃO reutilizar 25 °C de temperatura externa, ausência de ocupantes ou ausência de A/C como condições do item 32. O item 32 tem **33 °C externos, meta interna de 25 °C, um ocupante e regime permanente**; deve ser tratado como ensaio distinto, também considerando DEC-010 (seleção do climatizador pendente).

**Pendente após DEC-027:** definição justificada das temperaturas iniciais, geometria e orientação do veículo, materiais e propriedades reais dos vidros/isolamento, tratamento das condições solares, condições de contorno de CFD, malhas, critérios de convergência, resultados ao meio-dia e análise de incerteza. Preservadas integralmente DEC-001 a DEC-026, incluindo escolhas finais de comparações ainda pendentes.

### Próxima pergunta a deliberar (DEC-028)
Definir como dimensionar a capacidade térmica do ar-condicionado no **item 32**: cumprir primeiramente o ensaio obrigatório de um ocupante a 33 °C externos e 25 °C internos em regime permanente, e avaliar se é preciso também um cenário habitável realista com **dois ocupantes**, exposição solar e variabilidade de cargas, sem escolher antecipadamente FreshWell 3000 ou outra máquina (DEC-010).


## DEC-028 — Dimensionamento do ar-condicionado para um e dois ocupantes (item 32)
**Status: METODOLOGIA DE COMPARAÇÃO APROVADA PELO USUÁRIO EM 28/10/2026; EQUIPAMENTO, CAPACIDADE E RESULTADOS FINAIS PENDENTES.** O usuário decidiu **executar o ensaio obrigatório do item 32 com um ocupante, temperatura externa de 33 °C, meta interna de 25 °C e regime permanente**, além de **comparar com um cenário de dois ocupantes e análises de sensibilidade dos ganhos solares e das cargas internas**. Selecionar e dimensionar o climatizador **somente após validar capacidade térmica, consumo elétrico, massa e impacto na autonomia**. A DEC-010 continua comparação aprovada, sem escolha definitiva entre Dometic FreshWell 3000 e alternativas mais potentes.

### Cenário obrigatório do enunciado — um ocupante
- Modelar o motorhome com um ocupante, **T externa de 33 °C**, **T interna de 25 °C** e **regime permanente**. Não confundir com o item 31, que é veículo fechado, desocupado, sem ar-condicionado e com T externa de 25 °C ao meio-dia.
- Calcular as cargas por condução em teto, paredes, piso, vidros e pontes térmicas; ganhos por radiação solar nas superfícies e pelos vidros, convecção/infiltração justificadas, cargas metabólicas de uma pessoa e cargas internas efetivamente ligadas no cenário. Se o enunciado não fixa uma exposição solar ou outra entrada específica para este teste, explicitar a hipótese e testar sensibilidade, sem apresentar uma condição arbitrada como prescrita pelo professor.
- Obter a **potência térmica de refrigeração requerida (kW térmicos)**, temperatura e fluxos relevantes; declarar fatores de segurança ou margens de capacidade usados no dimensionamento, sem confundi-los com consumo elétrico.

### Cenário operacional complementar — dois ocupantes
- Repetir a modelagem com dois ocupantes, mantendo explícitas as diferenças de cargas metabólicas e de uso dos equipamentos da habitação. Examinar influência de ganhos solares (orientação, proteção dos vidros, sombras e incidência), isolamento decidido na DEC-016, infiltração e outras cargas internas.
- Executar análises de sensibilidade para variáveis de maior incerteza; indicar como cada variação altera a carga térmica e a disponibilidade de margem do ar-condicionado.
- Distinguir **regime permanente para dimensionamento do item 32** do **perfil de operação intermitente e consumo diário** da DEC-004, usado para dimensionamento dos serviços e autonomia.

### Seleção de equipamento e interface com demais decisões
- Comparar o **Dometic FreshWell 3000 (capacidade de refrigeração nominal preliminar de 2,7 kW térmicos; conferir ficha aplicável)** com uma ou mais alternativas comerciais de maior capacidade, conforme DEC-010. Verificar capacidade nas condições de operação, potência elétrica absorvida, eficiência, corrente/pico de partida, massa, dimensões, instalação, custo e disponibilidade, com fonte rastreável (DEC-012).
- Verificar compatibilidade com **bateria de serviços independente de 48 V** (DEC-020), autonomias comparativas de 24/48 h (DEC-005), reservas de SOC da DEC-013, configuração PV da DEC-021 e gerenciamento de cargas/inversor candidato da DEC-019. **Não** utilizar energia da bateria de tração para a climatização, e **não** contabilizar energia solar duas vezes.
- Não selecionar um equipamento por capacidade nominal isoladamente; caso não exista opção comercial validada para a carga calculada, identificar a inviabilidade, revisar hipóteses ou estudar alternativas documentadas, sem inventar especificações ou concluir atendimento sem evidência.
- **P6 (responsável principal):** modelagem térmica do item 32, cenários, especificações de A/C, comparação e recomendação técnica; **P3:** CAD, integração física e isolamento; **P2:** potência elétrica, inversor e bateria auxiliar; **P5:** consumos e autonomia; **P1:** massa e custo.

### Entregáveis e pendências
- Entregar tabela de hipóteses e fontes, balanço de cargas térmicas por mecanismo, cenários 1/2 ocupantes, sensibilidade de radiação solar e cargas internas, dimensionamento de potência térmica, comparação de modelos reais (kW térmicos versus kW elétricos), margens operacionais, impactos sobre bateria de serviços e autonomia, limitações e incertezas.
- **Continuam pendentes:** dados e geometria final de isolamento/vidros, modelos comerciais específicos, temperaturas de superfícies, cargas térmicas calculadas, capacidade mínima recomendada, compatibilidade com o inversor candidato e escolha do climatizador. Preservadas integralmente DEC-001 a DEC-027, inclusive todas as comparações ainda abertas.

### Próxima pergunta a deliberar (DEC-029)
Definir o modo de apresentar a **viabilidade da missão de 7.000 km somente com energia solar** enquanto DEC-001/DEC-021 não comprovarem uma interface solar→tração. Separar uma simulação física validada de hipóteses condicionais sobre interfaces de carga, evitando afirmar que uma viagem pode ser concluída sem caminho energético implementável.

## DEC-029 — Viabilidade energética condicional versus viabilidade técnica da missão de 7.000 km
**Status: METODOLOGIA E CRITÉRIO DE COMUNICAÇÃO APROVADOS PELO USUÁRIO EM 29/10/2026; VIABILIDADE FÍSICA DA RECARGA SOLAR→TRAÇÃO E EXECUÇÃO DA VIAGEM AINDA NÃO COMPROVADAS.** Apresentar separadamente **(i) a viabilidade energética condicional** da missão de 7.000 km por energia solar e **(ii) a viabilidade técnica** da interface de recarga solar da bateria de tração. Simular autonomia, SOC, paradas e duração da viagem usando hipóteses rastreáveis, mas **não declarar a missão fisicamente realizável sem uma arquitetura de recarga efetivamente validada**. Essa decisão não aprova as arquiteturas da DEC-001 nem a alocação da DEC-021; preserva a independência dos bancos da DEC-020.

### Frente 1 — Simulação energética condicional (P5, apoio P2 e P4)
1. **Enunciado principal:** calcular a missão de **7.000 km** apenas com energia solar, sem recargas externas e com **no máximo 8 horas efetivas de condução por dia**, conforme DEC-006. Utilizar a rota geográfica real estimada (~7.511 km) apenas como caso complementar, sem substituir a distância acadêmica exigida.
2. **Entradas rastreáveis:** veículo e Cd com incerteza (DEC-002/023), massa típica versus admissível (DEC-022), consumo por velocidade/trecho (itens 25/26), energia inicial de tração, reservas de SOC da DEC-013, consumo auxiliar separado e geração realista dos 1.540 Wp fixos e 1.600 Wp portáteis (estes apenas nas paradas), perdas em conversores, sombras, temperatura e condições ambientais. Nunca confundir potência Wp com energia diária em kWh.
3. **Cenários solares:** cenário acadêmico principal sob dia de referência de São Carlos em 21/06 repetido explicitamente como abstração e cenário complementar geográfico/histórico ao longo do percurso (DEC-007). Distinguir dados meteorológicos históricos de previsão futura.
4. **Estratégias de condução:** comparar horário fixo e parada solar otimizada da DEC-011, respeitando janela e tempo de implantação/recolhimento dos painéis portáteis, consumos noturnos e energia dos serviços. Comparar reservas 10%/20% e 20%/30% (tração/serviços) conforme DEC-013, sem alterar indevidamente as premissas específicas do item 27 (DEC-014).
5. **Resultados mínimos:** curvas diárias/horárias de SOC da tração e dos serviços, produção FV por origem, energia para propulsão/serviços, perdas, energia de recarga efetiva sob cada hipótese, horas dirigidas e estacionadas, dias e paradas até completar 7.000 km, além de eventuais estados em que a viagem se torna inviável ou interrompida. Registrar balanço energético sem dupla contagem, inclusive se comparar alocação de painéis DEC-021.
6. **Natureza condicional:** se o modelo considerar uma interface solar→tração ainda não comprovada, rotular resultados e tabelas como **'simulação energética condicionada à disponibilidade de interface de recarga compatível'**. Disponibilidade teórica de kWh não comprova que OBC/EVSE/pack aceitem a potência/carregamento previsto; verificar ainda corrente e potência mínimas e operação apenas quando permitida.

### Frente 2 — Auditoria de viabilidade técnica (P2, apoio P5)
1. Examinar interfaces reais de recarga da variante E-Ducato escolhida: conector, OBC/entrada DC autorizada, corrente mínima, tensões, comunicações, BMS, isolamento, neutro/terra, proteção, homologação, disponibilidade comercial de componentes, custo, massa, volume e rendimentos por etapa, conforme DEC-001/012/021.
2. **Compatibilizar com DEC-020:** a bateria auxiliar de 48 V não fornece energia à habitação a partir da bateria de tração; os bancos de tração e serviços permanecem independentes. A **alternativa A original da DEC-001, passando pela bateria de serviços**, não deve ser descrita como aprovada ou compatível com a decisão de independência. Caso seja estudada, requer revisão expressa de arquitetura pelo grupo; explorar caminhos de recarga solar→tração por circuito dedicado e autorizado, sem conexão direta não autorizada aos terminais HV.
3. Dar status explícito por opção: **comprovado por documentação**, **condicional/pendente de dados ou integração**, **não demonstrado** ou **incompatível**. Não inferir viabilidade de recarga do veículo a partir de ficha genérica de inversor ou de um balanço de energia favorável.
4. Se não se comprovar interface compatível e segura, apresentar a missão como **não demonstrada tecnicamente na configuração proposta**, mesmo que a simulação energética condicional conclua o percurso.

### Forma obrigatória de apresentação e responsabilidades
- **Dois veredictos independentes:** 'resultado energético sob hipóteses declaradas' e 'status da implementação elétrica'. Não usar 'viável' de forma absoluta quando apenas um deles for atendido.
- **P5:** consolidar simulação da viagem, SOC, energia FV, paradas, perfis de velocidade e sensibilidades; **P2:** validação documental de interfaces e perdas, segurança, compatibilidade e limites de carregamento; **P4:** dinâmica, resistência ao avanço e consumo; **P1/P3:** compatibilidade de massas, volumes e instalação.
- **Entregáveis:** tabela de hipóteses e fontes, diagrama de fluxos energéticos sem dupla contagem, comparativo entre estratégias e cenários, gráficos SOC versus distância/tempo, tabela de auditoria de interfaces e uma conclusão separada para cada nível de viabilidade.

**Pendente após DEC-029:** variante final do veículo, interface solar→tração documentalmente comprovada, escolha definitiva da alocação FV, validação dos componentes e eficiência de conversão, execução dos cenários de autonomia/rota e relatório dos limites. Preservadas integralmente DEC-001 a DEC-028 e comparações ainda abertas.

### Próxima pergunta a deliberar (DEC-030)
Fixar estratégia para o **layout habitável em CAD do E-Ducato L3H2**, incluindo cama para dois ocupantes, circulação e acesso, chuveiro/cassete, lavadora/secadora 2 em 1, reservatórios, cozinha e volumes técnicos, sem extrapolar dimensões internas verificadas ou cargas por eixo.

## Orientação ao Codex
Não confundir intenção de comparar com escolha. Marcar cada hipótese como provisional e rastrear dados, fontes e seus autores. Não classificar resultados de autonomia de tração solar e viagem como validados sem caminho energético fisicamente compatível. O enunciado 2026 continua sendo a especificação principal.


## DEC-030 — Comparar layout interno com cama fixa versus cama conversível antes de congelar CAD
**Status: COMPARAÇÃO PRELIMINAR APROVADA PELO USUÁRIO EM 29/10/2026; LAYOUT FINAL PENDENTE.** Comparar preliminarmente **dois layouts internos do Fiat E-Ducato L3H2**: (A) cama de casal fixa, preferencialmente na região traseira, e (B) cama de casal conversível integrada à área de convivência. **Não selecionar ainda um layout final**: a escolha depende da validação dimensional, funcional, estrutural e de integração dos equipamentos. A aprovação não altera a decisão de usar o E-Ducato L3H2 apenas como base geométrica (DEC-002).

### Estudos de ocupação e integração física (P3, com apoio P6)
1. Criar **dois estudos preliminares de CAD** ou modelos volumétricos na mesma geometria-base, com escala verificável, cotas e fonte para medidas internas. Identificar todas as geometrias e folgas ainda estimadas.
2. Incluir **cama para duas pessoas**, assentos e circulação, cozinha elétrica, geladeira, banheiro com chuveiro, **cassete sanitário removível de aproximadamente 20 L** (DEC-018), **lavadora/secadora 2 em 1** (DEC-015), **boiler elétrico compacto** (DEC-017), isolamentos térmicos e proteção solar dos vidros (DEC-016), ar-condicionado ainda por escolher (DEC-010/028), quadros elétricos e áreas de manutenção.
3. Representar os tanques já decididos: **100 L de água limpa, 70 L de águas cinzas e cassete de aproximadamente 20 L para águas negras**, sem adicionar um tanque fixo redundante para águas negras. Prever acessos para reabastecimento, drenagem e retirada do cassete, preservando higiene e manutenção (DEC-008/018).
4. Reservar espaço para **bateria auxiliar de 48 V independente da tração**, inversor/circuitos/ventilação e proteções (DEC-019/020), bem como armazenamento dos **1.600 Wp portáteis** quando recolhidos, respeitando a DEC-003. Não presumir que todas as dimensões de equipamentos comerciais já estejam validadas (DEC-012).
5. Verificar **ergonomia, área e largura úteis de circulação, acessibilidade aos equipamentos, altura livre, saídas/acessos e funcionamento das portas**, assim como montagem/desmontagem da cama conversível. Comparar volume de armazenamento e praticidade de uso diário.

### Verificações de massa, centro de gravidade e custo (P1, P3, P6)
- Com base em massas e posições de equipamentos rastreáveis, comparar **massa adicionada, distribuição longitudinal/transversal, centro de gravidade, cargas por eixo e viabilidade diante de PBT homologado** quando identificado (DEC-022). Não afirmar que o veículo atende limites legais sem documentação da variante.
- Comparar **custo, complexidade de montagem, manutenção, mecanismos móveis e interferências** em cada configuração. Considerar impacto das instalações no isolamento, elétrica, água e ventilação.
- Integrar a verificação do **teto com 1.540 Wp FV fixos**, janelas, exaustão e eventuais instalações externas de A/C; não considerar previamente comprovado que tudo cabe (DEC-003/010/016).
- Recomendar **um único layout para o CAD detalhado** com justificativa multicritério e fontes, mas submetê-lo ao grupo como escolha ainda pendente. A simulação energética e as demais análises devem utilizar geometria e massa consistentes com a variante de layout escolhida depois.

### Entregáveis e critérios de aceitação
- Duas plantas/layouts preliminares cotados, tabela comparativa de compatibilidade/ergonomia/volumes, lista de componentes e dimensões documentadas versus hipóteses, massa/CG/cargas por eixo preliminares, estimativa comparativa de custos e riscos/interferências, com proposta de escolha futura.
- **Responsabilidades:** P3 conduz o CAD e a integração; P6 determina requisitos habitáveis e equipamentos; P1 consolida massa, centro de gravidade e custo; P2/P5/P7 verificam interferências de sistema elétrico, FV e arrefecimento.
- **Permanece pendente:** seleção final da cama/layout, verificação OEM das dimensões, confirmação de cabimento de todos os equipamentos, variante de veículo, resultados definitivos de PBT/CG/cargas por eixo e congelamento do CAD detalhado.
- Preservadas as decisões DEC-001 a DEC-029 e **todas as suas comparações ainda em aberto**, inclusive a interface solar→tração, alocação FV, ar-condicionado, SOC e modelagens térmicas.

### Próxima pergunta a deliberar (DEC-031)
Definir o **tratamento de interferências no teto** entre 1.540 Wp de módulos solares fixos (DEC-003), aberturas, ventilação, passagem de cabos, sombreamentos e eventuais unidades de climatização, com critérios de viabilidade física e reavaliação documentada caso a potência instalada não caiba.


## DEC-031 — Comparar configurações reais de ocupação do teto com 1.540 Wp como meta condicionada
**Status: COMPARAÇÃO E ESTUDO DE VIABILIDADE FÍSICA APROVADOS PELO USUÁRIO EM 29/10/2026; ARRANJO DEFINITIVO E CONFIRMAÇÃO DE 1.540 Wp PENDENTES.** Comparar configurações reais de ocupação do teto do **Fiat E-Ducato L3H2** no CAD, usando dimensões de painéis fotovoltaicos comerciais e avaliando **aberturas, sombras, afastamentos, fixação, massa, aerodinâmica e manutenção**. Manter **1.540 Wp de módulos fixos** como meta de projeto, condicionada à comprovação de viabilidade física. **Não alterar a potência nominal aprovada pela DEC-003 sem nova aprovação expressa**. Preservar os **1.600 Wp de painéis portáteis exclusivamente durante as paradas**, conforme DEC-003, sem misturá-los à área de montagem fixa no teto.

### Estudo geométrico documentado (P3, apoio P5 e P6)
1. Utilizar o envelope e as medidas reais documentadas do teto da variante L3H2 compatível; indicar divergências dimensionais da geometria preliminar e não tomar as dimensões externas brutas como área integralmente utilizável.
2. Selecionar **modelos comerciais reais** de módulos fotovoltaicos e registrar fabricante/modelo, ficha técnica, potência STC (Wp), comprimento, largura, espessura, massa, conectores, tolerâncias, custo e fontes. Não inventar modelos ou números de módulos; verificar que a soma de potências efetivamente instaláveis atende ou não à meta de 1.540 Wp.
3. Criar **pelo menos dois estudos de ocupação do teto** em CAD, com plantas cotadas e vistas de interferência, incluindo janelas ou claraboias, exaustores, ventilação, pontos de passagem e vedação de cabos, estruturas de suporte e eventuais componentes externos de climatização, **somente se o equipamento de A/C selecionado realmente exigir espaço no teto** (DEC-010/028).
4. Avaliar afastamentos para fixação, ventilação sob os módulos, inspeção/limpeza, acesso aos pontos de manutenção, abertura de portas/tampas e eventuais obstruções, além de sombreamento entre módulos e equipamentos em diferentes posições solares. Considerar a instalação estática e os esforços durante o movimento.
5. Identificar rotas de cabos e pontos de entrada vedados, separação/proteções elétricas e impactos nos circuitos fotovoltaicos, sem presumir um caminho validado de recarga solar para o pack HV (DEC-001/020/021/029).

### Verificações estrutural, aerodinâmica e energética (P1/P3/P5; consulta P2)
- **P1/P3:** conferir massas de módulos, suportes, fixadores, esforços aerodinâmicos e solicitações admissíveis da carroceria e ancoragens com dados de fabricante ou hipóteses justificadas; contabilizar massa alta e impacto no centro de gravidade e nos eixos (DEC-022). Não declarar homologação/segurança de ancoragens não verificadas.
- **P3:** avaliar impacto da altura e disposição dos painéis e suportes no Cd e nos resultados de CFD; mudanças geométricas relevantes exigem rastrear o cenário correspondente e incerteza (DEC-023).
- **P5:** calcular geração por módulo/arranjo, incluindo efeitos de área realmente livre, orientação horizontal, sombreamento, temperatura, MPPT e perdas; comparar impacto em Wh/dia, itens 25/27/29 e autonomia. Não tratar potência nominal Wp como energia entregue ao pack HV.
- **P2:** verificar tensões/correntes de cada string frente à janela de MPPT, proteção, seccionamento, cabeamento e possibilidade de independência dos bancos de bateria (DEC-020/021/026), mantendo alocação solar definitiva em aberto.

### Critério de decisão futura e entregáveis
- Entregar desenhos CAD cotados de arranjos alternativos, tabela de modelos de módulos (com fontes), mapa de interferências e sombras, lista de suportes/fixações, checagens estruturais preliminares, massa e centro de gravidade, impactos em Cd e estimativas comparativas de geração.
- Distinguir explicitamente: (i) **meta nominal de 1.540 Wp**, (ii) **potência comercial que cabe no modelo CAD**, e (iii) **potência/instalação efetivamente validada**. Os três valores podem divergir e não devem ser confundidos.
- Se nenhum arranjo acomodar fisicamente 1.540 Wp com segurança, apresentar configurações alternativas quantificadas e seus impactos e **solicitar nova decisão do grupo antes de alterar a potência**. Não reduzir silenciosamente a meta, não declarar teto validado somente com desenhos ilustrativos e não assumir A/C de teto antes da seleção comercial.
- **Continua pendente:** seleção final dos módulos e arranjo, viabilidade comprovada dos 1.540 Wp, interferências finais com A/C e ventilação, ancoragens, efeitos aerodinâmicos e distribuição definitiva da geração entre tração e serviços.

### Próxima pergunta a deliberar (DEC-032)
Definir **como validar o modelo de consumo de tração** em velocidade constante a 40 e 80 km/h, integrando arrasto CFD, resistência ao rolamento, massa, eficiência elétrica/mecânica, limites OEM e comparação com referências documentadas, sem confundir autonomia homologada de ciclo de condução com consumo medido a velocidades constantes.

### Integridade do registro
As seções DEC-001 a DEC-030 permanecem **inalteradas**, incluindo todas as comparações e condições pendentes. A DEC-031 **não** escolhe um layout de teto nem altera a DEC-003, e **não** dá como resolvida a DEC-001 (interface solar→tração).


## DEC-032 — Modelo físico de consumo de tração a 40 e 80 km/h, verificação documental e incertezas
**Status: METODOLOGIA APROVADA PELO USUÁRIO EM 29/10/2026; PARÂMETROS E RESULTADOS NUMÉRICOS AINDA PENDENTES DE VALIDAÇÃO.** Desenvolver um **modelo físico de consumo de tração em velocidade constante a 40 e 80 km/h**, incluindo **arrasto aerodinâmico, resistência ao rolamento, massa operacional e eficiência do trem de força**. Verificar plausibilidade frente a **dados oficiais e medições disponíveis**, realizar **análises de sensibilidade com incertezas explícitas** e **separar o consumo de tração do consumo dos equipamentos internos/serviços**. **Não tratar autonomia homologada de um ciclo de condução como medição de consumo a 40 ou 80 km/h constantes.** Esta é uma aprovação metodológica, não uma confirmação de resultado, variante OEM, rendimento ou Cd.

### Modelagem de base — P4 (dinâmica), P5 (energia), apoio P1/P2/P3
1. Nas condições-base de pista plana e velocidade aproximadamente constante, usar uma decomposição rastreável: força aerodinâmica `Fa = 0,5 * rho * Cd * Af * v²`; rolamento `Fr = Crr * m * g` (ou formulação mais específica documentada); potência mecânica nas rodas `P_rodas = (Fa + Fr) * v`. Explicitar hipóteses de densidade do ar, temperatura, altitude, pneus, pressão, carga e pavimento; separar eventuais inclinações, acelerações e vento quando estudados como cenários adicionais.
2. Para passar de \(P_{rodas}\) à potência elétrica da bateria de tração, modelar eficiências do motor, inversor, transmissão e demais auxiliares de tração somente com valores e mapas documentados ou hipóteses justificadas com faixa de sensibilidade. Não confundir potência de pico OEM com eficiência constante, tampouco misturar potência do sistema de serviços com a tração. A capacidade de **98 kWh úteis** e o motor de **205 kW/410 N·m** permanecem **hipóteses provisórias até validar a variante exata** (DEC-002/009).
3. Calcular energia por distância em **kWh/km**, consumo em **km/kWh** e potências a **40 km/h e 80 km/h**; explicitar se as grandezas são na bateria de tração, nas rodas ou no veículo completo. Identificar diferença entre desempenho instantâneo, autonomia por energia inicialmente armazenada e autonomia condicionada à reposição fotovoltaica dos itens 25/27/29.
4. Usar a massa operacional típica e a massa máxima fisicamente admissível como cenários comparativos da DEC-022. Empregar o **Cd e sua incerteza** advindos do estudo com três ou mais malhas da DEC-023; não escolher um Cd definitivo enquanto CFD não estiver convergido. Registrar a área frontal, geometria de teto e alterações de Cd associadas à DEC-031.
5. Confrontar as ordens de grandeza com dados homologados, especificações OEM da **mesma variante** e, se disponíveis, ensaios/medições de veículos equivalentes. **Identificar o ciclo e as condições dos dados externos** (massa, temperatura, velocidade, pneus, trajetos, acessórios) e explicar por que o consumo de um ciclo não constitui medição em velocidade constante. Não ajustar parâmetros artificialmente para fazer a simulação reproduzir números comerciais.
6. Executar análise de sensibilidade pelo menos para **\(C_d\), área frontal, massa, \(C_{rr}\), densidade do ar e eficiência do trem de força**, com valores-base, limites e justificativa. Propagar intervalos de consumo/autonomia e identificar parâmetros dominantes; evitar falsa precisão.
7. Manter **dois balanços energéticos**: tração HV e serviços 48 V, independentes conforme DEC-020; contabilizar a geração FV de cada arranjo apenas uma vez e considerar painéis portáteis somente nas paradas (DEC-003/021). Os resultados energéticos da missão solar continuam **condicionais** até validação física da interface de recarga solar→tração (DEC-001/029).

### Verificações, entregáveis e dependências
- **P4:** equações, parâmetros e velocidades 40/80, checagens de plausibilidade elétrica/mecânica e efeitos da variante de velocidade da DEC-009.
- **P5:** tabelas/curvas potência, kWh/km e km/kWh, sensibilidade e integração às autonomias dos itens 25, 26, 27 e 29, mantendo separados energia de tração, consumos da habitação e reposição FV.
- **P3:** Cd e área frontal obtidos no CFD com incertezas, cenários de montagem dos painéis no teto (DEC-023/031).
- **P1/P2:** massas, cargas por eixo, pneus e parâmetros elétricos reais ou explicitamente estimados, com fontes e variantes compatíveis (DEC-012/022).
- **Entregáveis:** planilha ou script reproduzível com entradas, fontes, equações, unidades, conversões, gráficos por velocidade, tabela de comparação documental, cenários de massa e bandas de incerteza; destacar limitações de homologação e resultados ainda não validados.
- **Permanece pendente:** seleção/validação da variante E-Ducato, curvas OEM, Cd convergido, massa/PBT e pneus reais, rendimento efetivo, resultados finais de km/kWh/autonomia, arquitetura de recarga solar e alocação definitiva dos painéis; preservar todas as comparações abertas das DEC-001 a DEC-031 (especialmente DEC-005, 009, 010, 011, 013, 021, 022, 023, 029, 030 e 031).

### Próxima pergunta a deliberar (DEC-033)
Definir a **estratégia de validação estrutural das instalações de conversão**, especialmente suportes dos módulos FV, ancoragens de baterias auxiliares/tanques/móveis e compatibilidade com a carroceria original: usar somente pontos OEM documentados, projetar subestruturas ou comparar ambas as alternativas com cargas e verificações verificáveis, sem presumir homologação ou resistência sem cálculo.

### Integridade do registro
O conteúdo original anterior à seção DEC-032 foi mantido **sem alterações de caracteres**, incluindo as decisões DEC-001 a DEC-031, todas as comparações em aberto e ressalvas de viabilidade física.


## DEC-033 — Comparar ancoragens OEM documentadas e subestruturas próprias para instalações do motorhome
**Status: COMPARAÇÃO E METODOLOGIA APROVADAS PELO USUÁRIO EM 29/10/2026; SOLUÇÕES E HOMOLOGAÇÃO FINAIS PENDENTES.** Comparar a utilização de **ancoragens originais OEM documentadas** com **subestruturas próprias** para fixação de **painéis solares, baterias auxiliares, reservatórios de água, mobiliário e equipamentos do motorhome**. Priorizar pontos originais **somente onde a capacidade mecânica, o tipo de carregamento e as condições de montagem forem comprovadamente adequados**. Quando necessário, dimensionar suportes adicionais com cálculos e **elementos finitos para pontos críticos**, considerando cargas de **frenagem, curvas e vibração**, massa, custos, segurança e compatibilidade com a carroceria. **Não presumir homologação nem resistência estrutural não demonstradas.** A decisão NÃO seleciona automaticamente uma ancoragem, subestrutura, fator de segurança, modificação da carroceria ou solução final de montagem.

### Escopo e procedimento de engenharia — P1 (principal), P3 (CAD/FEA), P2/P5/P6/P7 (interfaces)
1. **Inventariar as massas e posições reais ou estimadas** de cada conjunto a fixar (módulos e suportes FV fixos, armazenamento dos portáteis, bateria auxiliar de 48 V, inversor, reservatórios e suas condições de enchimento, boiler, lavadora/secadora, móveis e outras cargas pertinentes). Registrar fabricante/modelo, dimensões, massa, posição do CG e fonte; calcular massa total e distribuição por eixo em conjunto com DEC-008/022/030/031.
2. **Identificar pontos e superfícies de ancoragem OEM** da variante L3H2 em manuais e documentos de preparação/conversão da fabricante, quando disponíveis. Distinguir pontos de amarração de carga, fixação de bancos e pontos estruturais: não assumir intercambialidade nem capacidade para esforços de projeto sem comprovação.
3. **Comparar explicitamente pelo menos duas estratégias** por conjunto crítico: (A) fixação em pontos OEM comprovados com suportes mínimos; (B) subestrutura projetada, usando interfaces de carroceria documentadas ou modificações cuja viabilidade estrutural/legal seja demonstrável. Se nenhuma for suficientemente comprovada, registrar **PENDENTE/INVIÁVEL NO ESTADO ATUAL**, sem fabricar margens de segurança.
4. Definir **casos de carga rastreáveis** para frenagem/desaceleração, aceleração lateral em curva, vibração, carga vertical e, para painéis no teto, ações aerodinâmicas; distinguir cargas operacionais de hipóteses conservadoras de projeto. Justificar intensidades, duração, combinações, coeficientes dinâmicos e critérios de avaliação com referências aplicáveis; não apresentar valores hipotéticos como exigências normativas.
5. Realizar **cálculos de pré-dimensionamento**, seleção de materiais e fixadores, verificações de esforço, deformação, flambagem, contato, arrancamento/rasgamento e fadiga quando pertinente, além de simulações por **elementos finitos nos pontos mais críticos**, com verificação de malha, contornos e modelo de ligação, e análise de incerteza. As cargas nos pontos de fixação devem ser coerentes com a estrutura real do veículo, não somente com a resistência isolada dos suportes.
6. Para o teto, verificar integração com DEC-003/023/031: peso elevado, estanqueidade, corrosão galvânica, esforços aerodinâmicos, folgas de manutenção, recortes/vedações e possível alteração do Cd. Para tanques e bateria, verificar deslocamento de massa, contenção durante frenagens, proteção elétrica/mecânica e acesso de manutenção. Para móveis e eletrodomésticos, verificar retenção de objetos e fixações sob cargas dinâmicas.
7. Comparar **massa, custo discriminado, espaço ocupado, dificuldade de montagem, acessibilidade, manutenção, impacto no centro de gravidade e segurança**. Confrontar PBT/cargas por eixo e limitações de fabricante; não extrapolar homologação de outra variante ou país para o veículo escolhido.

### Entregáveis e dependências
- **P1:** matriz de equipamentos × massas × cargas × pontos de fixação; memória de cálculo dos esforços, dimensionamento e critérios de segurança; comparação técnico-econômica e limites de PBT/eixos.
- **P3:** CAD cotado com interfaces reais e propostas, vistas dos suportes e ancoragens, estudos de FEA nos casos críticos, verificação de malha/condições de contorno e integração com teto/layout.
- **P2/P5/P6/P7:** requisitos de manutenção, isolamento elétrico, passagem de cabos, dissipação térmica, acessórios e perfis de uso que afetem fixação e acesso.
- **Entregáveis conjuntos:** lista de ancoragens OEM com citações verificáveis, alternativas de subestrutura com massa/preço, matrizes de cargas e segurança, notas de FEA e declaração explícita de itens não validados.
- **Permanece pendente:** identificação da variante/homologação OEM, limites de ancoragem, dimensionamento e material final de suportes, posição definitiva dos componentes, resultados de FEM, validação física/legal e seleção da estratégia vencedora. Não aprovar automaticamente cortes ou soldas na estrutura original.

### Próxima pergunta a deliberar (DEC-034)
Definir **como apresentar e validar o custo total do motorhome** (veículo-base, conversão, baterias, eletrônica, painéis, equipamentos internos, instalações, materiais e possíveis custos de engenharia), diferenciando preços documentados de estimativas, valores pontuais versus faixas de incerteza e evitando contabilização dupla de componentes OEM e de conversão.

### Integridade do registro
As seções originais **DEC-001 a DEC-032 foram preservadas byte a byte**, incluindo aprovações, comparações ainda em aberto, hipóteses, incompatibilidades de arquitetura e ressalvas de viabilidade. Esta DEC-033 aprova exclusivamente a comparação e o plano de validação estrutural, sem resolver pendências anteriores.


## DEC-034 — Custo total de aquisição e conversão do motorhome, sem dupla contagem OEM
**Status: METODOLOGIA DE ORÇAMENTO TOTAL APROVADA PELO USUÁRIO EM 29/10/2026; PREÇOS, MERCADO, VARIANTE E TOTAL FINAL PENDENTES DE APURAÇÃO.** Calcular o **custo total do motorhome pronto**, incluindo **aquisição do Fiat E-Ducato na variante efetivamente escolhida**, componentes e materiais adicionais, instalação/mão de obra e custos de engenharia, mediante **preços rastreáveis** e sem contabilizar duas vezes componentes e sistemas originais já incluídos no preço OEM. A decisão aprova **a apresentação de um orçamento total**, não um número final sem cotações nem uma mudança automática de variante ou arquitetura. Não exigir múltiplos cenários de preço mínimo/central/máximo como condição formal desta escolha; faixas de incerteza podem ser acrescentadas quando os dados exigirem.

### Estrutura obrigatória do orçamento — P1 (principal), com entradas P2–P7
1. **Preço de aquisição do veículo-base:** identificar fabricante, ano/modelo, variante L3H2, mercado, país, configuração, motorização, capacidade de bateria de fábrica e condições da oferta. O E-Ducato L3H2 está aprovado como **base geométrica** na DEC-002, mas a variante exata, potência, bateria, velocidade máxima e preço continuam sujeitos à documentação OEM. Evitar misturar ofertas de variantes incompatíveis ou conversão de moeda sem referência de data.
2. **Itens adicionais de conversão:** inventário com quantidade, fabricante/modelo, unidade, preço unitário, moeda, fonte/URL ou documento consultado, data da consulta, tributos/frete pertinentes e subtotal. Incluir: painéis fixos/portáteis e estruturas, MPPT e eventuais componentes da interface solar→tração ainda não comprovada, bateria de serviços de 48 V, inversor/proteções/cabos, mobiliário, cozinha/geladeira, boiler, lavadora/secadora 2 em 1, sanitário de cassete, hidráulica e tanques, isolamento/vidros, ar-condicionado, ventilação e refrigeração adicional quando aplicável.
3. **Instalação e engenharia:** discriminar mão de obra, fabricação e montagem de suportes, adequações elétricas e hidráulicas, acabamento, projeto CAD/CFD/FEA e ensaios/verificações quando o orçamento os considerar. Identificar como **estimativas** os custos que não dispõem de cotação documentada; não atribuir preço comercial fictício a serviços não orçados.
4. **Prevenir dupla contagem:** não somar novamente ao preço-base os componentes de fábrica já fornecidos, como **motor de tração, bateria HV OEM, sistema de arrefecimento OEM, freios e cabos HV originais**. Somar apenas modificações adicionais ou substituições realmente especificadas; se substituir uma peça OEM, explicitar custo incremental e eventual crédito/reaproveitamento, sem pressupor valor de revenda.
5. **Consistência com decisões e viabilidade:** a arquitetura de carregamento solar→tração da DEC-001/021/029 **não está comprovada**. Separar custos de componentes de instalação efetivamente especificável dos custos **condicionais de arquiteturas em comparação**, sem fazer preço de um protótipo hipotético parecer uma solução implementada. Os custos de alternativas concorrentes (A/C DEC-010/028, bateria DEC-005, layout DEC-030, teto DEC-031, fixações DEC-033) não devem ser todos somados em duplicata ao mesmo veículo.
6. **Rastreabilidade e data/mercado:** para cada preço, documentar **moeda, país/mercado e data**, eventual câmbio de conversão com fonte/data, presença ou ausência de impostos, frete e instalação. Quando houver apenas cotação estrangeira, identificar limitações de disponibilidade, importação, encargos e compatibilidade com o mercado escolhido; evitar atribuir preço brasileiro a anúncio europeu sem ajuste explícito.
7. **Incertezas e estado de validação:** classificar valores como **oferta/cotação documentada**, **preço de referência** ou **estimativa de engenharia**; expor itens sem preço e intervalo de incerteza quando justificável. Não afirmar orçamento fechado enquanto escolhas críticas de hardware, variante e interface solar não estiverem resolvidas.

### Estrutura de entrega e responsabilidades
- **Tabela consolidada auditável:** subtotal do veículo-base + subtotal de componentes adicionais + subtotal de materiais/instalação + subtotal de engenharia/validação + tributos/frete pertinentes = **custo total estimado do motorhome**, com regra explícita de itens já inclusos no OEM. Apresentar os subtotais também separadamente para permitir inspeção e atualização do projeto.
- **P1:** liderar planilha, custo total, massas e consistência entre decisões. **P2:** custos de sistemas elétricos, bateria de serviços, inversor e soluções de recarga comprovadas ou hipotéticas identificadas. **P3:** custos de CAD, carroceria, fixações, alterações e fabricação. **P4:** informações da variante OEM e desempenho; evitar preço separado de trem de força de fábrica. **P5:** componentes FV e cenários da interface solar–tração. **P6:** habitação, conforto, eletrodomésticos e hidráulica. **P7:** climatização e arrefecimento adicional apenas se realmente previsto.
- **Entregáveis:** planilha ou CSV reproduzível com fórmulas, fonte/data de cada preço, notas de inclusão/exclusão, custos por subsistema, subtotal veículo/conversão/engenharia e total, lista de itens condicionais ou sem cotação e limitações.
- **Permanece pendente:** escolha final de variante e mercado, modelo/quantidade/custo de componentes, serviços, acessórios, custos de projetos/ensaios, confirmação da interface solar→tração e **valor total em qualquer moeda**. Nenhuma comparação ainda em aberto das DEC-001 a DEC-033 fica decidida por esta DEC-034.

### Próxima pergunta a deliberar (DEC-035)
Definir **como integrar os sete pacotes de trabalho e validar as entregas antes do prazo**, especialmente travas de dados entre CAD/massa/CFD, elétrica/FV, dinâmica/autonomia, conforto térmico e custos. Comparar entrega única ao final, marcos de integração periódicos ou processo por portas de validação com bloqueios explícitos para resultados condicionais.

### Integridade do registro
As seções anteriores **DEC-001 a DEC-033 foram preservadas byte a byte**, incluindo aprovações, comparações pendentes, hipóteses e ressalvas de viabilidade física. A DEC-034 só aprova a metodologia de custo total sem dupla contagem e não fecha qualquer preço ou escolha de componente.


## DEC-035 — Integração contínua dos sete pacotes de trabalho, fonte única de parâmetros e marcos de validação
**Status: METODOLOGIA DE INTEGRAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; EXECUÇÃO E RESULTADOS AINDA PENDENTES.** Estabelecer **integração contínua entre os sete pacotes de trabalho P1–P7**, com **fonte única de parâmetros**, três marcos explícitos (**baseline, integração das simulações e auditoria final**), entregas reproduzíveis, responsáveis identificados, rastreabilidade de hipóteses/fontes/resultados e **status de validação e pendências sem mascaramento**. Esta é uma decisão sobre processo e qualidade; não converte automaticamente em aprovadas as alternativas de arquitetura ou os resultados ainda em aberto das DEC-001 a DEC-034.

### Fonte única de verdade e gestão de alterações
1. Manter um arquivo estruturado de parâmetros compartilhados e versionado no repositório (por exemplo, `config/parametros_mestre.yaml`, ou equivalente aberto e legível por scripts), com identificador de revisão e unidades SI. Sua estrutura definitiva pode ser escolhida pelos integrantes, preservando a função de **fonte única de verdade**.
2. Registrar para cada parâmetro: **chave e descrição, valor/faixa, unidade, origem/fonte/documento, data de referência, responsável, versão de configuração, status** (`confirmado/documentado`, `estimado/hipótese`, `em comparação`, `pendente/bloqueado`) e, quando aplicável, incerteza e intervalo de validade.
3. Não substituir um valor compartilhado por outro silenciosamente. Mudanças em massa/PBT/eixos, Cd/área frontal, módulo PV, bateria útil/SOC, eficiência/corrente mínima do OBC, carregamento solar→tração, potência térmica do A/C, isolamento, perfil de cargas ou preço devem gerar histórico de alterações e **disparar reavaliação dos resultados dependentes**.
4. Distinguir claramente **configuração de referência do projeto**, **variante/mercado OEM ainda não congelados**, **cenários comparativos** e **hipóteses condicionais**; jamais mesclar características incompatíveis de versões do E-Ducato em uma mesma configuração sem aviso.

### Três marcos de validação
- **M1 — Baseline de componentes e hipóteses:** consolidar geometria do E-Ducato L3H2, inventário de subsistemas, fichas técnicas e preços quando disponíveis, matriz de massas/cargas, arquitetura energética em análise, cargas habitáveis, cenários ambientais e restrições do enunciado. Registrar lacunas, critérios de aceitação e os bloqueios da recarga solar da tração.
- **M2 — Integração das simulações:** executar e integrar cálculos/arquivos de CAD, massa/eixos, CFD, dinâmica, frenagem, cabos, solar/SOC/viagem, conforto térmico, arrefecimento e custos com **a mesma versão do baseline**, indicando as diferenças entre casos de estudo. Conferir conservação de energia, massas, unidades, consistência da carga e premissas de funcionamento.
- **M3 — Auditoria final e fechamento:** reproduzir os resultados principais a partir dos scripts/dados versionados, revisar gráficos, fórmulas, tabelas, citações, números e aderência aos 35 itens do enunciado. Publicar lista de pendências e limitações, especialmente a **viabilidade técnica ainda não comprovada da interface solar→tração**; não apresentar cálculos condicionais como implementação comprovada.

### Entregas mínimas por pacote P1–P7
- **P1 — Estrutura, freios, massa/eixos e custos:** massas/centro de gravidade, PBT/eixos, fixações/FEA, casos de frenagem, orçamento total com rastreabilidade.
- **P2 — Baterias e elétrica:** bateria auxiliar 24/48h, inversor, proteções, gerenciamento de cargas, cabos, interfaces solar/serviços e estudos de recarga solar→tração sem interligação indevida dos packs.
- **P3 — Carroceria, CAD e CFD:** geometria e arranjos de layout/teto, documentação dimensional, arrasto e incertezas de malha, interfaces de suportes e estudo CFD térmico complementar conforme interação com P6.
- **P4 — Motor e dinâmica:** variantes OEM, motorização/limite de velocidade, modelo de tração a 40/80 km/h, 0–100 km/h quando fisicamente permitido e limites de regeneração.
- **P5 — Solar e autonomia:** perfis de geração fixa/portátil, alocação energética entre sistemas independentes, SOC/autonomia e missão 7.000 km, com distinção entre viabilidade energética condicional e técnica.
- **P6 — Interior e conforto:** cargas habitáveis, layouts, equipamentos/hidráulica, isolamento, modelo de aquecimento da cabine fechado sem A/C e dimensionamento de climatização com um/dois ocupantes.
- **P7 — Arrefecimento:** modelo térmico parametrizado da bateria baseado em OEM documentado, testes de 20/80 kW, radiador, bomba, vazão, temperaturas e apoio térmico pertinente.
- **Regra comum:** cada entrega terá responsável, arquivo(s) de entrada, versão do baseline, script/modelo reproduzível, fonte ou justificativa das hipóteses, resultados com unidade, verificação/convergência apropriada e status explícito.

### Critérios de integração, conflitos e bloqueios
- Implantar uma **matriz de dependências** entre responsáveis e critérios de entrada/saída de cada pacote: por exemplo, `Cd/área frontal P3 → P4/P5`, `massa/eixos P1 → P4/P5/freios`, `cargas P6 → P2/P5`, `elétrica P2 → P5`, `hardware/custos P2–P7 → P1`.
- Classificar divergências como **inconsistência a corrigir**, **hipótese em comparação** ou **limitação não resolvida**. Não tratar diferenças de cenário (p.ex. SOC inicial 100% versus 80%, reserva 10/20 versus 20/30, 24h versus 48h) como erro quando intencionais e identificadas.
- Para a interface solar→tração (DEC-001/020/021/029), estabelecer **bloqueio de conclusão técnica** até haver documentação de componentes, compatibilidade OEM, potência/corrente mínima, controle/proteções, riscos e modo de operação; enquanto isso, resultados do item 29 devem ser claramente rotulados **condicionais**.
- Preservar os requisitos específicos do professor como cenários independentes: itens 25/26 (40/80 km/h), 27 (terminar com 30% SOC), 29 (7.000 km, ≤8 h/dia, sem recarga externa), 31 (fechado sem ocupantes/A-C ao meio-dia), 32 (33→25 °C com um ocupante), 33 (30→10 m/s em 5 s), 34/35 (carregamento de 20/80 kW e sistema térmico).
- A integração contínua não obriga todos os modelos a estarem completos antes de integrar: aceitar entregas parciais desde que versão, escopo, dependências e grau de confiabilidade estejam declarados.

### Próxima pergunta a deliberar (DEC-036)
**Escolha da variante e do mercado de referência do E-Ducato**: DEC-002 aprovou L3H2 como geometria, mas a variante exata e sua documentação (massa/PBT/eixos, motor, pack, limite de velocidade, OBC, disponibilidade e preços) continuam abertas. Definir se priorizar mercado brasileiro, europeu ou triagem técnico-documental com congelamento de uma única variante e orçamento correspondente, sem misturar especificações incompatíveis.

### Integridade do registro
As seções **DEC-001 a DEC-034 foram preservadas byte a byte**. Esta DEC-035 apenas aprova processo de integração e marcos de auditoria; **não aprova** equipamentos/modelos/capacidades ainda pendentes nem resolve comparações em andamento.


## DEC-036 — Comparação documentada de variantes elétricas Fiat E-Ducato L3H2 nos mercados brasileiro e europeu
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; VARIANTE COMERCIAL DEFINITIVA AINDA PENDENTE.** Comparar **variantes reais do Fiat E-Ducato elétrico L3H2** nos mercados **brasileiro e europeu**, antes de congelar **uma única variante coerente** para o projeto integrado. Não misturar características, dados OEM ou preços de versões distintas como se fossem um mesmo veículo.

### Escopo obrigatório da pesquisa e validação
1. **Identificação única de cada candidato:** marca, linha, versão, ano-modelo, carroceria L3H2, mercado/país, motorização, código de configuração quando disponível e status de comercialização/homologação; indicar explicitamente incompatibilidade ou ausência de oferta elétrica L3H2 em determinado mercado, caso confirmada.
2. **Documentação oficial:** obter fichas técnicas/catálogos/configuradores/manuais homologados e registrar URL/documento, data e mercado. Não extrapolar automaticamente dados de variantes térmicas ou de outras carrocerias para o E-Ducato elétrico L3H2.
3. **Massa, estrutura e dimensões:** comprimento/altura/distância entre eixos úteis para o CAD; massa em ordem de marcha/tara, PBT, carga útil, massa rebocável se relevante e limites por eixo. Distinguir convenções de massa e pacote opcional; preservar as comparações operacionais de DEC-022.
4. **Tração e desempenho:** potência/torque do motor, tipo de transmissão, velocidade máxima e eventuais limitadores por versão, bateria HV nominal e útil quando especificadas, e dados necessários para consumo, velocidade e aceleração; manter cenários de DEC-009 e metodologia DEC-032 sem declarar 0–100 km/h viável numa variante limitada abaixo de 100 km/h.
5. **Recarga e compatibilidade:** portas/conectores, carregador de bordo AC, fases/tensões/correntes nominais e mínimas confirmáveis, potência AC/DC permitida, protocolos e restrições oficiais. **Não inferir** que FV/EVSE funcionará com baixa potência só pela potência máxima anunciada. Não criar ligações diretas não autorizadas ao pack HV. A análise é insumo das DEC-001, DEC-020, DEC-021 e DEC-029; não resolve a interface FV→tração.
6. **Preços e aquisição:** preço do veículo-base com moeda, país, data, tributos/opcionais/frete explicitados, e análise da disponibilidade no Brasil ou do impacto de eventual aquisição/importação; não combinar cotação de uma variante com especificações de outra. Integrar ao orçamento DEC-034 após escolha.
7. **Matriz de comparação:** tabela lado a lado com cada candidato e suas fontes, campo `não localizado` quando não houver evidência, divergências e consequências para massa, CAD, frenagem, autonomia, térmico, elétrica, custo e restrições legais.

### Critério para congelamento da variante
- **Uma única variante final**, identificada por mercado/ano/versão, deverá alimentar o conjunto coerente de parâmetros de referência (DEC-035). Cenários alternativos permanecem separados e rotulados como comparações ou sensibilidade.
- A seleção final depende de documentação suficiente, compatibilidade do envelope L3H2, PBT/carga por eixo e plausibilidade física dos equipamentos e interfaces; se o mercado brasileiro não apresentar opção correspondente, **não substituir silenciosamente por um Ducato a combustão**.
- Dados ausentes deverão permanecer como hipóteses ou bloqueios declarados, nunca como fatos OEM. A meta de 1.540 Wp no teto e a viabilidade da recarga solar–tração continuam condicionais (DEC-003, DEC-031, DEC-029).
- **P4** lidera variantes e desempenho; **P1** valida massas/PBT e custo; **P2** verifica bateria e interfaces de recarga; **P3** confronta geometria CAD; **P5** atualiza energia/autonomia. Todos usam fontes rastreáveis e revisões versionadas do baseline.

### Pendências preservadas
**DEC-001** mantém arquitetura solar→tração em comparação, sendo que sua opção A original passando pela bateria de serviços contradiz a independência aprovada na **DEC-020** e exige redesenho; **DEC-005** bateria auxiliar 24/48h; **DEC-009** velocidade limitada versus acima de 100 km/h; **DEC-010** ar-condicionado FreshWell versus alternativas; **DEC-011** condução fixa versus otimizada; **DEC-013** reservas SOC; **DEC-021** alocação fotovoltaica fixa/flexível; **DEC-022** massas típicas/máximas; **DEC-029** distinção de viabilidade energética condicional versus técnica; **DEC-030** layouts internos; **DEC-031** ocupação do teto; e demais validações de componentes, modelos e resultados seguem abertas conforme os respectivos registros. Esta decisão **não** escolhe antecipadamente nenhuma variante e **não** comprova a interface FV→tração.

### Próxima pergunta a deliberar (DEC-037)
Definir o **método de cálculo e validação da velocidade máxima e do desempenho 0–100 km/h (item 28)** sem misturar dados de versões: usar apenas valores OEM, apenas modelo longitudinal de tração ou modelo físico validado com ficha/ensaio OEM, respeitando os limitadores reais e declarando o ensaio 0–100 impossível para variante com velocidade máxima inferior a 100 km/h.

### Integridade do registro
As seções **DEC-001 a DEC-035 foram preservadas byte a byte**. DEC-036 aprova somente a **comparação técnico-documental** e os critérios de seleção posterior; o fechamento da variante exata permanece pendente.


## DEC-037 — Modelo longitudinal de velocidade máxima e aceleração 0–100 km/h, verificado com dados OEM (item 28)
**Status: METODOLOGIA DE CÁLCULO E VERIFICAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; RESULTADOS FINAIS, VARIANTE OEM E CURVAS FÍSICAS PENDENTES.** Desenvolver um **modelo físico longitudinal** do Fiat E-Ducato convertido para estimar **velocidade máxima e aceleração**, verificando plausibilidade frente a **dados OEM documentados da variante exata** selecionada conforme DEC-036. Simular separadamente as condições de **massa operacional típica** e **massa máxima fisicamente admissível** da DEC-022. **Respeitar limitadores de velocidade originais**; declarar que o ensaio **0–100 km/h não é realizável** nas variantes cuja velocidade máxima homologada/limitada seja inferior a 100 km/h. **Não inventar curvas de torque, potência, eficiência ou relações de transmissão** e não misturar fichas de variantes distintas.

### Método aprovado — P4 principal; P1/P2/P3/P5 como interfaces
1. **Identificação da variante:** registrar modelo/ano/mercado/versão exatos, motorização, bateria, transmissão, velocidade máxima e limitador publicados; em ausência de documentação suficiente manter configurações candidatas e resultados rotulados como hipóteses. Não transformar cenário hipotético acima de 100 km/h em desempenho da versão limitada.
2. **Modelo físico do movimento:** formular força de tração efetiva nas rodas a partir de motor/transmissão e seus limites; considerar arrasto aerodinâmico (Cd e área frontal, com incerteza DEC-023), resistência ao rolamento, inclinação quando aplicável, massa/inercias equivalentes, limites de aderência e potência/corrente da bateria e do inversor, quando disponíveis. Para a velocidade máxima, encontrar o equilíbrio entre tração disponível e resistências, aplicando depois os limites eletrônicos homologados; explicitar hipóteses de pista plana, vento nulo, pneu, temperatura e condições do ensaio.
3. **Integração temporal:** simular aceleração de 0 a 100 km/h através de integração de velocidade/posição e verificação do passo temporal, quando **100 km/h for atingível**. Se a variante for limitada a velocidade inferior a 100 km/h, registrar o item 28 como **0–100 km/h: não realizável nessa variante** e apresentar, se útil, um ensaio complementar fisicamente alcançável (por exemplo, 0–80 km/h), claramente diferenciado do pedido do professor.
4. **Validação com documentação OEM:** comparar os resultados do modelo com velocidade máxima, potência, torque e tempos de aceleração oficiais **se estiverem publicados para a mesma configuração**. Dados OEM do veículo-base não são automaticamente o desempenho do motorhome convertido. Qualquer curva ausente deve ser explicitamente parametrizada ou substituída por faixa justificada com análise de sensibilidade, nunca apresentada como OEM.
5. **Duas massas:** repetir cálculos para as configurações de massa típica e máxima admissível previstas na DEC-022, considerando variações de centro de gravidade/carga por eixo e limites de tração e segurança quando materialmente pertinentes. Evitar massa superior ao PBT ou extrapolação não identificada.
6. **Rastreabilidade e incertezas:** registrar fontes, dados de entrada, unidades, hipóteses, parâmetros não identificados, curvas/trajetórias de velocidade, aceleração, força e potência, convergência numérica e influência das incertezas de Cd, rolamento, massa e tração. Não apresentar tempo 0–100 numérico quando a variante não puder alcançar 100 km/h ou os dados forem insuficientes para defendê-lo.

### Integrações e produtos esperados
- **P4:** implementação reproduzível do modelo longitudinal, resultados para as duas massas, velocidade máxima (limitada/teórica distinguida), trajetória de aceleração e status do ensaio 0–100; documentação de variantes e curvas utilizadas.
- **P1:** valores consistentes de massa, PBT, carga por eixo e configuração de conversão. **P3:** Cd/área frontal e incertezas CFD. **P2:** limites elétricos comprovados de tração e potência. **P5:** checagem de coerência das resistências e do consumo contra os cálculos de autonomia e energia da DEC-032.
- **Entregáveis:** tabela comparativa por variante/cenário de massa, gráficos e código reproduzíveis, referências OEM e lista de bloqueios para parâmetros não documentados.
- **Pendente:** seleção de variante (DEC-036), massas e Cd validados, curvas documentadas ou intervalos justificáveis, limites eletrônicos e elétricos efetivos, resultados quantitativos de velocidade e aceleração; todas as comparações anteriormente abertas permanecem sem vencedor.

### Próxima pergunta a deliberar (DEC-038)
Definir a **metodologia de cálculo da geração fotovoltaica real versus ideal** para o sistema de 1.540 Wp no teto e 1.600 Wp portátil apenas estacionado: radiação solar horário a horário, geometria/orientação/inclinação, sombreamento, temperatura dos módulos, perdas elétricas e MPPT, efeitos das paradas e incerteza. Decidir entre modelo idealizado, modelo físico realista ou comparação de ambos com sensibilidade, mantendo o balanço energético separado por bateria e sem pressupor recarga da tração tecnicamente viável.

### Integridade do registro
As seções **DEC-001 a DEC-036 foram preservadas byte a byte**. Esta decisão define **metodologia e critérios**, não aprova uma variante, um limitador, curvas OEM não verificadas ou qualquer resultado numérico de desempenho; preserva integralmente as comparações e limitações técnicas anteriores.


## DEC-038 — Comparar geração fotovoltaica idealizada versus modelo físico realista horário
**Status: COMPARAÇÃO METODOLÓGICA APROVADA PELO USUÁRIO EM 29/10/2026; PRODUÇÃO REAL, CONFIGURAÇÃO FINAL DE MÓDULOS E RECARGA SOLAR DA TRAÇÃO PENDENTES DE VALIDAÇÃO.** Desenvolver e comparar um **modelo idealizado de geração fotovoltaica** e um **modelo físico realista de resolução horária**, com posição solar, orientação, inclinação, temperatura das células/módulos, sombreamento, perdas elétricas e eficiência/limites dos controladores MPPT. Quantificar geração diária, sensibilidade e impacto em horários de parada, autonomia e balanço de energia. Manter a instalação nominal de referência de **1.540 Wp fixos no teto** e **1.600 Wp portáteis apenas com o veículo estacionado**, submetidas à comprovação de compatibilidade física da DEC-031. **NÃO presumir viabilidade da transferência de energia fotovoltaica à bateria de tração HV.**

### Dois modelos com a mesma base de comparação — P5 responsável principal
1. **Idealizado, como referência superior ou cenário simplificado explicitamente rotulado:** calcular irradiância de céu limpo e geometria solar para **São Carlos em 21 de junho**, nas condições do enunciado (25 °C de temperatura ambiente, umidade relativa 50%, vento externo nulo salvo ensaio específico), utilizando módulos nominais em condições idealizadas e perdas simplificadas, se adotadas, com cada fator documentado. Não presumir que Wp em STC representa potência contínua real; separar claramente potência nominal e energia diária integrada em kWh. Não chamar o modelo idealizado de previsão meteorológica real ou valor comercial garantido.
2. **Realista, com resolução horária ou menor quando necessário:** determinar posição do Sol, irradiância no plano de cada conjunto, orientação e inclinação no teto e de módulos portáteis montados na parada, temperatura de célula com modelo explicitado, perdas por sombreamento parcial, sujeira, mismatch, cabeamento, conversões e eficiência/limites reais do MPPT. Usar curvas e limites de módulos, arranjos e controladores comerciais documentados (DEC-012); não fabricar especificações técnicas. Observar que temperatura de célula é distinta da temperatura do ar; com **vento nulo** no cenário acadêmico, não supor coeficientes convectivos de vento elevado.
3. **Geometria e instalação:** relacionar geração à posição e distribuição dos módulos no CAD (DEC-031), fixações/altura e sombras dos equipamentos; verificar tensão e corrente de cada string perante MPPT, proteções e temperaturas extremas plausíveis. Caso 1.540 Wp não caibam com segurança, apresentar diferença entre meta, capacidade instalável e potência fisicamente validada, sem alterar meta por conta própria.
4. **Portáteis e estados da viagem:** habilitar os **1.600 Wp portáteis somente quando o motorhome estiver parado**, com montagem, orientação, eventual reposicionamento, segurança e tempo de recolhimento explicitados quando relevantes. Durante deslocamento, produção portátil = **zero**. Vincular horários de parada e direção fixa/otimizada da DEC-011, respeitando até 8 h dirigindo por dia (DEC-006). Não contar como energia utilizável a geração que exceder capacidade de carregamento/aceitação de um circuito.
5. **Dois contextos meteorológicos já definidos na DEC-007:** (a) dia-tipo acadêmico de 21/06 em São Carlos repetido por hipótese na simulação multidiária; (b) estudo complementar com condições geográficas, calendário e meteorologia históricos/variáveis da rota. **Não** apresentar dados ERA5 históricos como previsão de longo prazo. Distinção entre cenário idealizado e físico realista também se aplica a perdas de instalação; não confundir o eixo da comparação das perdas com o eixo meteorológico.
6. **Balanço elétrico sem dupla contagem:** registrar energia incidente, energia DC dos módulos, energia depois dos MPPT/conversões, energia efetivamente armazenada em serviços, energia **eventualmente** entregue à tração **somente em cenários condicionais** e energia perdida/limitada. O banco de serviços de 48 V permanece **independente** do banco de tração HV (DEC-020); nenhuma transferência de energia armazenada entre os bancos é autorizada. A distribuição A/B/flexível ainda é estudo da DEC-021. A arquitetura FV→tração segue pendente da DEC-001, e o item 29 tem viabilidade energética **condicional** separada de viabilidade técnica (DEC-029).
7. **Sensibilidade e incerteza:** comparar radiação/índice de claridade, orientação e inclinação dos portáteis, temperatura dos módulos, sombreamento, sujeira, perdas por cabeamento e MPPT, horário/duração de paradas e capacidade instalável no teto. Justificar limites e publicar intervalos plausíveis de kWh/dia e suas consequências sobre SOC/autonomia, sem apresentar eficiência exemplificativa como dado validado.

### Integrações e entregáveis verificáveis
- **P5:** scripts/planilhas reproduzíveis com série horária de irradiância/energia, curvas PV ideal × realista por conjunto, produção DC e energia utilizável por circuito, tabelas de kWh/dia, comparação entre horários fixos e otimizados de paradas, sensibilidade e impacto nos itens 25/26/27/29.
- **P3:** plantas CAD, orientação, ocupação do teto, sombras e condições reais de fixação; estimar impactos aerodinâmicos sem assumir a geometria final aprovada.
- **P2:** fichas de módulos/controladores, strings, MPPT, perdas, proteção e restrições de aceitação de carga para cada banco; auditar segurança e impossibilidade de conexão direta ao pack HV.
- **P1/P4/P6:** massas e custos dos equipamentos, integração ao consumo/rota e perfis de cargas sem double counting.
- **Fontes e metadados obrigatórios:** local, data e fuso, modelo solar e seus parâmetros, fichas técnicas, inclinações, intervalos temporais, unidades (Wp, W, Wh, kWh, kWh/m²), referências, versão do baseline, status de validação e diferenças entre hipóteses e medições.

### Pendências preservadas
A aprovação é **da comparação e da metodologia**, não de uma potência disponível ao longo do dia, uma produção de energia definitiva, um MPPT/modelo comercial, uma geometria válida de teto ou uma interface de carregamento solar da bateria HV. Preservar especialmente: **DEC-001** arquitetura solar–tração; **DEC-003/031** instalação de 1.540 + 1.600 Wp; **DEC-005** autonomia 24/48 h dos serviços; **DEC-007** dois contextos meteorológicos; **DEC-011** horários fixos/otimizados; **DEC-013/014** SOC; **DEC-020/021** bancos independentes e alocação solar em estudo; **DEC-023/032** aerodinâmica/consumo com incerteza; **DEC-029** viabilidade energética condicional versus interface real; **DEC-035** baseline compartilhado e rastreabilidade; **DEC-036** variante OEM definitiva pendente. Todas as comparações ainda abertas nas DEC-001 a DEC-037 permanecem abertas.

### Próxima pergunta a deliberar (DEC-039)
Definir a **estratégia construtiva e de segurança da bateria auxiliar de serviços de 48 V**: usar módulos comerciais completos com BMS integrado e proteção especificada, projetar banco próprio sob critérios de segurança ou comparar arquitetura comercial modular com banco dedicado; manter a capacidade final pendente até dimensionamento para **24 h versus 48 h sem sol** (DEC-005), compatibilidade com inversor/MPPT, correntes, fusíveis, seccionamento, instalação, temperatura, massa e preço. **Não envolver nem modificar o pack HV OEM.**

### Integridade do registro
As seções **DEC-001 a DEC-037 foram mantidas byte a byte**. A DEC-038 não fecha escolhas de módulos, inclinações, arranjos, MPPT, calendário realista ou conexão FV→tração, nem modifica a independência dos bancos de baterias da DEC-020.


## DEC-039 — Bateria auxiliar LiFePO₄ comercial modular, com BMS integrado
**Status: DIRETRIZ CONSTRUTIVA APROVADA PELO USUÁRIO EM 29/10/2026; MARCAS, MODELOS, QUANTIDADE DE MÓDULOS E CAPACIDADE FINAL AINDA PENDENTES.** Priorizar **módulos comerciais completos de bateria LiFePO₄**, apropriados ao barramento nominal de **48 V**, com **BMS integrado**, ficha técnica, proteções documentadas e possibilidade de composição modular expressamente admitida pelo fabricante. A capacidade útil deverá ser dimensionada somente depois de comparar os cenários de **24 h e 48 h de consumo habitável moderado sem geração solar** (DEC-005), com verificação de compatibilidade com inversor, MPPT, correntes, temperaturas, massa, dimensões e custo. Não considerar o candidato preliminar de **10,24 kWh** como capacidade aprovada.

### Requisitos de dimensionamento e seleção — P2 responsável principal
1. **Dados de entrada compartilhados:** receber de P6 o perfil horário das cargas essenciais e não essenciais para dois ocupantes (DEC-004/015/017/018/019/028), incluindo potência média, duração, picos, eventos ocasionais e consumo em repouso de inversor e controladores. Analisar os dois horizontes (24/48 h) **sem aporte solar**, de forma coerente com a DEC-005.
2. **Energia nominal versus utilizável:** distinguir energia nominal de placa (kWh), capacidade efetivamente acessível na janela operacional de SOC, eficiência da bateria, perdas de conversão DC/AC e redução de capacidade por temperatura/corrente/envelhecimento quando apoiada em dados. Testar as reservas de serviços de **20% e 30%**, ainda em comparação na DEC-013; não fixar reserva única por antecipação. Não transpor automaticamente a condição de SOC do item 27 (DEC-014, bateria de tração) ao banco de serviços.
3. **Compatibilidade elétrica e modularidade:** confirmar limites reais de tensão do banco (sistema comercial «48 V» pode ter tensão nominal e faixa distintas), limites de carga/descarga contínua e de pico, correntes máximas por módulo e conjunto, compatibilidade do BMS e comunicação com inversor/MPPT. Somar módulos somente se a associação em paralelo/série e os requisitos de proteção forem expressamente autorizados pelo fabricante. Não inventar compatibilidade nem supor que todos os módulos «48 V» se associam livremente.
4. **Segurança e instalação:** incluir fusíveis/disjuntores DC apropriados, seccionamento acessível, barramentos e cabos dimensionados, proteção contra curto-circuito e sobretemperatura, isolamento mecânico e elétrico, monitoramento, fixações, localização no CAD, ventilação/gerenciamento térmico e instruções aplicáveis dos fabricantes. O BMS integrado **não dispensa** o projeto de proteção externa. Cabos críticos são tratados também na DEC-026 e pontos de ancoragem na DEC-033.
5. **Massa, volume, custo e manutenção:** verificar especificações e fontes verificáveis de pelo menos uma opção comercial aderente ao perfil; registrar quantidade de módulos, dimensões, peso, custo, vida útil declarada sob condições especificadas, grau de proteção e requisitos de armazenamento/manutenção. Considerar influência sobre PBT, distribuição por eixo e orçamento total (DEC-022/034).
6. **Integração com sistema fotovoltaico:** o banco de serviços permanece **independente** da bateria de tração HV (DEC-020); sua recarga solar via controladores apropriados deve obedecer aos limites do BMS e MPPT. Não autorizar transferência de energia armazenada entre bancos. A alocação FV continua em comparação (DEC-021) e a recarga FV→tração não está validada (DEC-001/029). Os painéis portáteis são utilizados somente estacionados (DEC-003/038).

### Entregáveis e validações
- **P2:** planilha/script reproduzível com cargas, hipóteses, sizing de 24/48 h, SOC, potência de pico e verificação de compatibilidade; esquema funcional do banco modular, BMS, proteções, inversor e MPPT; documentação técnica de candidatos comerciais e lista explícita de não conformidades/dados faltantes.
- **P6:** perfis de carga e prioridades de desligamento e simultaneidade coerentes com a DEC-019; uso ocasional de lavadora/secadora e boiler, carga do A/C ainda sujeita à DEC-010/028.
- **P3/P1/P7/P5:** instalação física e fixações no CAD, massa/custo/CG/eixos, segurança térmica, e integração ao balanço FV/autonomia sem dupla contagem.
- **Portão de aprovação final:** só fixar capacidade, número de módulos e marcas após comprovar energia para ambos os cenários, correntes máximas, integração elétrica, segurança, volume e orçamento. Se nenhuma alternativa satisfizer requisitos físicos ou econômicos, registrar a inviabilidade ou trade-offs para deliberação, sem presumir solução aprovada.

### Pendências anteriores preservadas
Continuam abertas: **DEC-001** (interface FV→tração); **DEC-005** (capacidade 24/48 h); **DEC-009/036/037** (variante OEM e desempenho); **DEC-010/028** (equipamento e carga de A/C); **DEC-011** (horários de direção e paradas); **DEC-013** (reservas SOC); **DEC-021** (alocação FV); **DEC-023** (Cd); **DEC-029** (viabilidade técnica da rota); **DEC-030/031** (layout e instalação); além das demais comparações ou seleções não concluídas. Esta decisão prioriza um **tipo de solução** para os serviços, não define modelo, energia nominal/útil, aprovação elétrica, certificação, homologação ou ligação com o pack HV.

### Próxima pergunta a deliberar (DEC-040)
Definir o **nível de especificação e validação de segurança da distribuição elétrica de serviços em 48 V DC e da rede AC do inversor**, incluindo esquema unifilar, proteção de sobrecorrente/curto, seccionamento, aterramento/equipotencialização, proteção contra choques, segregação de circuitos, ensaios e limites entre projeto acadêmico e instalação homologável. A DEC-039 aprova módulos com BMS, mas não substitui o projeto de segurança dos circuitos, tomadas e aparelhos.

### Integridade do registro
As seções **DEC-001 a DEC-038 foram preservadas byte a byte**. A DEC-039 não fecha comparações pendentes nem altera decisões prévias.


## DEC-040 — Projeto elétrico detalhado 48 V DC e AC, análise de falhas e plano de inspeções/ensaios
**Status: METODOLOGIA E ESCOPO APROVADOS PELO USUÁRIO EM 29/10/2026; DIMENSIONAMENTOS, COMPONENTES, COMPATIBILIDADE, ENSAIOS E CONFORMIDADE FINAL PENDENTES.** Desenvolver **projeto elétrico detalhado dos sistemas de serviços em 48 V DC e AC**, com diagramas unifilares, dimensionamento de cabos e proteções, seccionamento, aterramento/equipotencialização, medidas contra choque, análise de falhas e plano de inspeções e ensaios. **Distinguir rigorosamente projeto acadêmico de instalação construída, ensaiada, homologada ou certificada.** O sistema de alta tensão (HV) OEM do E-Ducato **não será modificado**. Preservar a independência entre bateria auxiliar e bateria de tração (DEC-020).

### Escopo técnico obrigatório — P2 responsável principal
1. **Diagramas e interfaces:** produzir unifilar DC da geração FV/controladores MPPT/banco auxiliar LiFePO₄ de 48 V/BMS/barramentos/inversor e unifilar AC da saída do inversor aos circuitos de serviços, com legenda, tensões nominais e faixas, correntes de projeto, cargas, aterramento/equipotencialização, pontos de seccionamento e identificação dos componentes. Documentar claramente circuitos separados e a interface FV→tração **ainda não validada** como estudo distinto; não desenhar ligação HV não autorizada como instalação aprovada.
2. **Proteção de circuitos DC:** especificar dispositivos adequados à **tensão, corrente de operação e corrente de curto-circuito DC** do conjunto — fusíveis, disjuntores ou outros dispositivos apropriados, seccionamento acessível, proteção contra polaridade invertida e falhas relevantes, distâncias/isolação, barramentos e conexões. Confirmar capacidade de interrupção, coordenação e requisitos reais de fabricantes; o BMS integrado da DEC-039 não substitui proteção externa. Conferir dimensionamento térmico dos cabos 48 V e FV da DEC-026.
3. **Proteção dos circuitos AC:** dimensionar condutores e circuitos por carga, demanda simultânea e condições de instalação; prever proteção contra sobrecorrente/curto e choque elétrico, incluindo medidas adequadas ao **regime de neutro/terra e à topologia do inversor**. Conferir em manuais OEM quando e como se aplicam equipotencialização ao chassi, ligação neutro–PE e dispositivos diferenciais; **não presumir** ligação ao chassi, esquema TN/TT/IT, eficácia de DR/RCD ou aterramento externo sem validar a arquitetura de fonte móvel.
4. **Gerenciamento de cargas e limites reais:** documentar prioridades, bloqueios de simultaneidade e cargas essenciais (DEC-019); confirmar potência contínua, de pico, derating térmico e compatibilidade do inversor candidato **Victron MultiPlus-II 48/5000** antes de aprová-lo. Correlacionar demandas e picos com janela operacional da bateria (DEC-005/013/039), climatização ainda em comparação (DEC-010/028), boiler (DEC-017), lavanderia (DEC-015) e demais cargas P6.
5. **Análise de modos de falha:** elaborar matriz de perigos e mitigação (ao menos curto DC/AC, sobrecorrente, falha de isolamento, conexão frouxa/arco e aquecimento, sobretemperatura, BMS desligado, falha do MPPT/inversor, umidade/ingresso de água, ventilação insuficiente, erro de comutação/alocação FV). Para cada modo indicar consequências, prevenção/detecção, dispositivos e ações de desligamento seguro, risco residual e responsável por validar.
6. **Normas, evidências e rastreabilidade:** identificar **normas e instruções efetivamente aplicáveis** a cada subsistema e ao uso em veículo, verificando escopo e jurisdição sem alegar conformidade automática com normas prediais. Para cada componente comercial registrar ficha/versão, parâmetros elétricos/ambientais, coordenação com dispositivos vizinhos, massa, preço e limites não demonstrados; usar uma única fonte versionada de parâmetros (DEC-035).
7. **Plano de inspeções e ensaios, não execução presumida:** listar inspeção visual, continuidade/equipotencialização onde aplicável, isolação, polaridade, verificação de seccionamento e sobrecorrente, funcionamento do BMS, desligamentos por falha, ensaios funcionais sob carga, elevação térmica de cabos/conexões e proteção contra choques, indicando métodos, instrumentos adequados, critérios de aceitação baseados em normas/manuais e condição segura de realização por profissional habilitado. Resultados devem ser marcados **planejado**, **simulado**, **efetivamente ensaiado** ou **não verificado**; jamais indicar aprovação/certificação de uma instalação não construída.
8. **Limites e interfaces preservados:** manter cabos e bateria HV OEM sem alterações (DEC-026); transferência de energia **armazenada** de tração para serviços permanece proibida pela DEC-020. A alocação FV entre circuitos de bancos independentes continua em comparação (DEC-021) e qualquer solução FV→tração exige interface autorizada e validação da DEC-001/029, não podendo ser declarada viável por existir desenho elétrico conceitual.

### Entregáveis e integração
- **P2:** diagramas unifilares AC/DC, tabela de circuitos e cargas, memorial de cálculo, lista de cabos/proteções/chaves com dados documentados, matriz de falhas, checklist de ensaios e matriz de conformidade/pendências.
- **P6:** inventário e cronogramas de demanda, potência contínua e picos de aparelhos e priorização do gerenciamento de cargas.
- **P3/P1/P7/P5:** rotas de cabos e proteção física no CAD, massa/custo e fixações, dissipação/temperatura e balanço FV sem dupla contagem.
- **Portão de validação:** não fixar dispositivos ou declarar proteção adequada sem verificar tensão/corrente de interrupção, coordenação, compatibilidade elétrica e topologia AC, instalação e segurança. Projeto acadêmico **não equivale** a aprovação da instalação por fabricante, autoridade competente ou certificadora.

### Pendências anteriores preservadas
Permanecem em comparação ou validação, conforme as respectivas seções: **DEC-001** FV→tração; **DEC-005** capacidade 24h×48h; **DEC-009/036/037** variantes/velocidade; **DEC-010/028** A/C; **DEC-011** horários; **DEC-013** reservas; **DEC-021** alocação FV; **DEC-023** Cd; **DEC-029** viabilidade da missão; **DEC-030/031** interior/teto; **DEC-039** número/capacidade de módulos LiFePO₄; e demais comparações pendentes de DEC-001 a DEC-039. Esta DEC-040 aprova o **nível de especificação e procedimento de validação**, não componentes definitivos nem segurança/homologação comprovadas.

### Próxima pergunta a deliberar (DEC-041)
Definir o **tratamento da autonomia de água e do descarte de resíduos na viagem de 7.000 km**. A DEC-008 prevê 100 L de água potável/limpa, 70 L de águas cinzas e 20 L no cassete de águas negras (DEC-018); DEC-015/017 e DEC-004 preveem lavadora/secadora ocasional, banho e uso moderado. Comparar hipóteses de consumo por dois ocupantes e definir se a missão admite reabastecimento de **água e descarte adequado** em paradas (que são distintos de recarga elétrica externa, proibida no item 29). Não assumir abastecimento ilimitado, descarte irregular nem autonomia hidráulica equivalente à autonomia elétrica.

### Integridade do registro
As seções **DEC-001 a DEC-039 foram preservadas byte a byte**. A DEC-040 não altera decisões aprovadas nem fecha comparações ainda abertas.

## DEC-041 — Reabastecimento de água e descarte de resíduos na missão solar
**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; FREQUÊNCIA E TEMPOS DE PARADA A DIMENSIONAR.** O usuário determinou: “permitir abastecimento de água limpa e descarte adequado de resíduos durante as paradas, sem recarga elétrica externa”. A missão de 7.000 km permite manutenção hidráulica e sanitária nas paradas, mas **não admite recarga elétrica externa**, conforme DEC-006/029.

### Requisitos e restrições aprovados
1. **Reservatórios inalterados:** manter 100 L de água limpa, 70 L de águas cinzas e aproximadamente 20 L no cassete removível do sanitário, conforme DEC-008/018. O cassete **é** o reservatório de águas negras, sem tanque adicional duplicado.
2. **Paradas sanitárias permitidas:** reabastecer água limpa em fonte apropriada e descartar águas cinzas e conteúdo do cassete somente em instalações adequadas/autorizadas. Modelar disponibilidade, frequência e duração das paradas, sem presumir suprimento ilimitado.
3. **Proibição absoluta de recarga elétrica externa:** água e descarte não permitem conectar o motorhome a tomada ou estação de recarga. Os balanços de água, SOC de tração, SOC de serviços e geração FV serão independentes e rastreáveis.
4. **Dimensionamento operacional por P6:** calcular consumo diário de dois ocupantes para banho, pia, cozinha, higiene, descargas e lavadora/secadora ocasional (DEC-015/017), com fontes e hipóteses declaradas. Incluir o boiler no balanço hidráulico sem duplicar volume de água.
5. **Conservação de massa:** contabilizar o nível dos três reservatórios e as transferências de água sem dupla contagem; reabastecimento e descarte mudam a massa a bordo e as cargas por eixo (DEC-008/022).
6. **Integração à viagem:** P5 incorpora as paradas de água e descarte ao cronograma de condução/descanso e às paradas solares; respeitar no máximo 8 h de direção por dia. Paradas hidráulicas não provam, por si só, a viabilidade energética da missão.
7. **Compatibilidade com decisões anteriores:** a opção **B da DEC-001** permanece selecionada como arquitetura solar→tração, mas sua interface DC continua sem validação técnica. DEC-020 (independência dos bancos), DEC-021 (alocação FV), DEC-029 (viabilidade energética vs. física) e todas as comparações anteriores continuam vigentes.

### Entregáveis e responsáveis
- **P6:** consumo hídrico, necessidades de reabastecimento e descarte, autonomia entre paradas e critérios sanitários.
- **P5:** inserir as paradas no simulador de rota e verificar tempo de viagem sem adicionar energia elétrica externa.
- **P1/P3:** massa de água conforme níveis, distribuição de carga por eixo, acessos, equipamentos e tubulações no CAD.
- **P2:** manter a contabilidade de energia solar e SOC independente do abastecimento de água.

### Próxima pergunta a deliberar (DEC-042)
Definir o tratamento da **baixa potência e variabilidade solar** na recarga DC da tração escolhida na DEC-001 B: estudar alimentação FV direta (se compatível com os mínimos da interface OEM) versus eventual **buffer/armazenamento dedicado exclusivamente à recarga da tração** e independente da bateria de serviços. A DEC-041 não aprova buffer extra nem altera a tecnologia ou as capacidades dos bancos.

### Integridade do registro
As seções **DEC-001 a DEC-040 foram preservadas sem modificações**. A DEC-041 foi acrescentada ao final, mantendo a DEC-001 B e todas as demais decisões/comparações em aberto.


## DEC-042 — Comparar recarga solar DC direta versus buffer dedicado à tração
**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; NENHUMA DAS IMPLEMENTAÇÕES VALIDADA OU ESCOLHIDA COMO DEFINITIVA.** O usuário determinou: “comparar recarga solar DC direta com recarga por buffer dedicado e independente da bateria de serviços, verificando requisitos OEM, potência mínima, protocolos, eficiência, massa, custo, segurança e operação durante paradas. Não aprovar automaticamente uma bateria extra nem declarar recarga viável sem comprovação técnica.”

### Escopo comparativo aprovado
1. **Cenário A — recarga DC direta sem buffer:** geração fotovoltaica dedicada → MPPT/condicionamento → estágios de conversão e equipamento externo de recarga DC **compatível e autorizado** → conector OEM de carregamento da variante escolhida do E-Ducato. Simular disponibilidade horária de potência, requisitos mínimos de tensão/corrente/potência, interrupções e reinícios, perdas e energia efetivamente entregue. Não assumir que conversor DC/DC isolado substitui EVSE/carregador DC ou seu protocolo.
2. **Cenário B — recarga DC com buffer dedicado:** geração FV dedicada → armazenamento intermediário **separado do banco de serviços 48 V e do pack HV OEM** → equipamento de carga DC compatível e autorizado → interface de recarga OEM. Analisar capacidade energética e potência mínima, BMS, segurança, conversões, ciclagem, eficiência de ida e volta, massa, volume, custo e tempo de parada. **Nenhuma bateria extra está aprovada para aquisição, instalação ou lançamento no CAD como componente definitivo** até validação e nova decisão.
3. **Pré-requisito comum de compatibilidade:** levantar a variante real da DEC-036, conector e padrão de recarga, handshake e comunicação exigidos, janelas de tensão/corrente, potência mínima operacional, limites de temperatura, isolamento, seccionamento e autorização/compatibilidade documental. Se dados não forem obtidos, marcar **não demonstrado**; não inventar equipamento ou parâmetros OEM.
4. **Operação estacionária:** avaliar recarga DC externa com o veículo parado, em paradas solares efetivamente programadas. Painéis portáteis de 1.600 Wp só contribuem durante o estacionamento; painéis fixos de 1.540 Wp continuam sujeitos à validação física (DEC-003/031). Não contabilizar como recarga viável durante o movimento sem evidência de modo autorizado.
5. **Independência dos bancos:** respeitar DEC-020 e DEC-001 B; bateria de serviços 48 V não alimenta a recarga de tração, e bateria de tração não alimenta serviços. Buffer, se vier a ser aprovado, é **exclusivo do circuito solar→tração** e não autoriza alterações/derivações no pack, BMS ou cabeamento HV OEM. Alocação FV ainda em comparação (DEC-021).
6. **Balanço energético e incertezas:** comparar kWh FV gerados, armazenados no buffer se houver, perdidos em conversões/espera e finalmente recebidos pela bateria de tração; incorporar limites de SOC e condições de parada, massa, custo e segurança, sem dupla contagem. Um buffer pode contornar intermitência ou acumular potência mas **não substitui a comprovação de interface/protocolo autorizados**.
7. **Decisão técnica futura:** classificar cada alternativa como comprovada, condicionada, não demonstrada ou inviável, justificando por fontes e verificações. Só então recomendar recarga direta, buffer ou revisão expressa da arquitetura. A missão solar de 7.000 km (DEC-029) permanece **energeticamente condicional** até que a viabilidade técnica seja demonstrada.

### Responsáveis e entregáveis
- **P2 (líder):** quadro comparativo de interfaces OEM/equipamentos reais, potência mínima, protocolo, proteção, isolação, compatibilidade e riscos; dimensionamento preliminar de buffer somente no cenário comparativo.
- **P5:** geração fotovoltaica horária e comparação do aproveitamento nas paradas, com e sem buffer, e impacto no SOC e duração da missão.
- **P1/P3:** estimativas de custo, massa, volume e acomodação apenas em estudo, sem assumir adição definitiva do buffer.
- **P4/P7:** compatibilização de limites de bateria/veículo, perdas e térmica quando necessário.

### Próxima pergunta a deliberar (DEC-043)
Definir o tratamento de **altimetria, aclives, declives e regeneração na rota Belém–Chuí/7.000 km**, sem confundir os resultados acadêmicos a 40/80 km/h constantes em pista plana com o consumo de um percurso real. Comparar eventualmente modelo plano de referência e rota com perfil altimétrico validado, velocidades e limites físicos de regeneração, separando dados reais de aproximações.

### Integridade do registro
As seções **DEC-001 a DEC-041 foram preservadas byte a byte**; a DEC-042 foi acrescentada ao final. Permanecem vigentes a escolha da DEC-001 B, a independência dos bancos e todas as demais comparações pendentes.


## DEC-043 — Percurso plano e velocidade constante como cenário principal da missão de 7.000 km
**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026.** O usuário determinou: “utilizar percurso plano e velocidades constantes como cenário principal de consumo da viagem de 7.000 km, declarando explicitamente as limitações da simplificação”. A decisão define a **hipótese de referência do cálculo de consumo de tração da missão**, sem alegar que a rota física Belém–Chuí tenha relevo plano nem que permita velocidade constante ininterrupta.

### Escopo aprovado e regras para o Codex
1. **Cenário principal plano:** considerar declividade longitudinal nula (`i = 0`, `sin(theta) = 0`) na modelagem de tração para a distância de 7.000 km exigida pelo enunciado, com **velocidades constantes explicitamente especificadas em cada execução**. Utilizar o modelo da DEC-032/037 com resistência aerodinâmica, rolamento, massa, eficiência do trem de força e perdas; não introduzir potência de rampa no cenário principal.
2. **Velocidades de referência:** calcular e reportar separadamente consumo energético a 40 km/h e 80 km/h conforme itens 25 e 26 do enunciado; se outras velocidades forem usadas em estudos da viagem, rotulá-las e verificar compatibilidade com o limitador da variante escolhida (DEC-009/036/037). Não supor que a velocidade média real da rota seja idêntica à constante usada no cálculo físico.
3. **Distância da missão:** manter **7.000 km como resultado principal obrigatório** da DEC-006; eventual rota geográfica de aproximadamente 7.511 km continua suplemento, não a distância que substitui o item do professor. Dados geográficos e altimétricos reais não são mandatórios para o consumo no cenário principal desta DEC-043.
4. **Limitação explicitamente declarada:** o cenário plano ignora acréscimos de demanda em aclives, possibilidades de regeneração em declives, variação real de velocidade e trânsito, curvas, acelerações/frenagens ao longo da rota, restrições locais e efeitos de altitude. Portanto, **não é uma simulação fiel da topografia da rota** nem uma previsão validada de consumo real. Diferenciar simplificação acadêmica de desempenho físico na estrada.
5. **Regeneração:** nenhuma recuperação de energia de descidas deve ser creditada em percurso plano; a DEC-025 sobre frenagem regenerativa permanece válida como **ensaio de frenagem separado**. Não confundir esse ensaio com geração líquida adicional na missão.
6. **Energia solar, SOC e operação continuam detalhados:** mesmo com consumo de tração simplificado, manter geração fotovoltaica horária, perdas, operação dos painéis portáteis **somente nas paradas**, independência dos serviços, limites de SOC, limite de **8 horas dirigindo por dia**, e comparação de políticas de paradas da DEC-011. Não converter 7.000 km em uma única viagem contínua sem paradas.
7. **Viabilidade da recarga não presumida:** manter DEC-001 B selecionada e DEC-042 comparando DC direto × buffer, ainda sem interface OEM comprovada. Separar consumo teórico da recarga solar efetivamente possível (DEC-029), sem energia de recarga externa ou dupla contabilização.
8. **Coexistência com DEC-007:** os cenários de condições solares acadêmicas de 21/06 em São Carlos e de meteorologia geográfica complementar continuam conforme DEC-007, mas **não alteram a opção por percurso plano como base energética principal**. Um estudo altimétrico posterior só será acrescentado se expressamente solicitado/aprovado; não substituir a decisão atual automaticamente.

### Responsáveis e entregáveis
- **P4 (dinâmica e tração):** curvas/modelos de força e consumo em pista plana, com parâmetros identificados e resultados por velocidade e massa típica/máxima; explicitar ausência de rampas e de regeneração por declive.
- **P5 (FV e autonomia):** integrar consumo plano ao simulador diário da missão, com energia solar efetivamente gerada, horários de movimento/parada, SOC, reservas e tempo total, mantendo os resultados condicionais à recarga OEM.
- **P2 (arquitetura elétrica):** manter perdas, interfaces de carregamento, limites de potência/corrente e incompatibilidades eventuais claramente sinalizados; não transformar cálculo de energia em viabilidade elétrica comprovada.
- **P1/P3:** fornecer massas/coeficiente de arrasto/área frontal consistentes com a fonte única de parâmetros.

### Próxima pergunta a deliberar (DEC-044)
Determinar os **estados de carga iniciais das baterias de tração e serviços especificamente para a simulação de 7.000 km (item 29)**, de forma independente do estudo do item 27 (DEC-014), que já usa 100% como referência e 80% como sensibilidade **com SOC final de 30%**. Proposta de comparação: começar ambos os bancos em 100% no cenário principal e repetir com 80% no cenário de sensibilidade, respeitando reservas da DEC-013, limites do BMS e ausência de recarga elétrica externa durante a missão. Não incluir qualquer buffer extra enquanto DEC-042 não o aprovar.

### Integridade do registro
O conteúdo binário do arquivo até o fim da DEC-042 foi preservado sem modificações. A DEC-043 foi acrescentada ao final; permanecem vigentes **DEC-001 B**, as decisões DEC-002 a DEC-042 e todas as comparações ainda pendentes, sem seleção automática de alternativas.


## DEC-044 — SOC inicial de 100% na missão solar de 7.000 km (item 29)
**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026.** O usuário determinou: “iniciar a simulação da viagem de 7.000 km com SOC de 100% nas baterias de tração e serviços, respeitando as reservas operacionais definidas e sem recarga elétrica externa durante a missão”. A escolha se aplica à **condição inicial da missão completa (item 29)**; não modifica os cenários próprios do item 27.

### Configuração de referência aprovada
1. **Tração:** adotar SOC inicial igual a **100%** da capacidade utilizável definida para a variante OEM validada (DEC-036), respeitando a interpretação e os limites de SOC do fabricante e do BMS. A capacidade de cerca de 98 kWh úteis é **provisória**, não um dado de fabricante validado para qualquer variante.
2. **Serviços:** adotar simultaneamente **100% de SOC inicial** no banco auxiliar LiFePO₄ de 48 V, fisicamente e eletricamente independente da tração (DEC-020/039). A capacidade preliminar de 10,24 kWh não está aprovada; dimensionamento para 24/48 h segue em comparação (DEC-005), com correntes, proteções e segurança ainda a validar.
3. **Reservas mínimas:** respeitar a comparação ainda **não concluída** entre reservas de tração/serviços de **10%/20%** e **20%/30%** (DEC-013). Não escolher silenciosamente uma das reservas nem equiparar essas reservas ao SOC final de 30% definido para o estudo diário do item 27.
4. **Sem recarga elétrica externa durante a missão:** nenhuma energia da rede ou de carregadores externos poderá ser incorporada ao balanço da viagem após o instante inicial. A energia inicialmente armazenada em ambos os bancos constitui uma **condição de contorno explícita**, não energia solar produzida ao longo do trajeto; discriminar separadamente energia inicial, geração FV, energia consumida e perdas. Não afirmar que toda energia da missão foi gerada durante a viagem.
5. **Operação FV e carregamento de tração:** manter 1.540 Wp fixos como meta sujeita à validação e 1.600 Wp portáteis somente estacionado (DEC-003/031), com modelos horários e perdas (DEC-038), política de paradas ainda comparada (DEC-011), limite de 8 h de condução por dia (DEC-006), e **arquitetura DC B selecionada** mas interface OEM e eventual buffer ainda não validados (DEC-001/042). Não utilizar a bateria auxiliar como fonte da tração.
6. **Modelo de deslocamento:** utilizar como principal o percurso plano a velocidades constantes explicitamente informadas, conforme DEC-043; manter os cenários de geração meteorológica da DEC-007 sem transformar a simplificação de relevo em previsão da estrada real.
7. **Resultados e condição de viabilidade:** simular separadamente SOC da tração e dos serviços, consumo, kWh solares gerados e efetivamente aproveitados, paradas, tempo total, energia remanescente e eventuais falhas operacionais. Manter a distinção da DEC-029 entre **balanço energético condicional** e **viabilidade técnica da recarga solar DC**, ainda não comprovada. Se o modelo cruzar reserva mínima, indicar a limitação em vez de ocultá-la.
8. **Não adicionar cenários sem aprovação:** não exigir cenário principal de 80% nem comparação 100% × 80% **para o item 29**, pois a alternativa aprovada foi A. A análise de SOC inicial **100% principal × 80% sensibilidade para o item 27** da DEC-014 permanece plenamente válida.

### Responsáveis e entregáveis
- **P5:** definir SOC inicial em 100% para os dois bancos no modelo da missão, com séries temporais de SOC, geração FV e consumo, e relatório de duração e paradas; separar claramente energia inicial da energia produzida durante a viagem.
- **P2:** fornecer capacidades úteis e limites efetivamente documentados, perdas, disponibilidade de carregamento DC e bloqueios de interface, além da independência entre bancos e das hipóteses de eventual buffer ainda não aprovado.
- **P4/P6:** fornecer respectivamente consumo de tração no cenário plano e perfis horários das cargas habitáveis sem dupla contabilização.
- **P1/P3:** manter a massa e a instalação dos sistemas coerentes com os componentes efetivamente selecionados.

### Próxima pergunta a deliberar (DEC-045)
Definir como implantar e orientar **os 1.600 Wp de painéis portáteis apenas nas paradas**: orientação/ângulo fixos em cada parada, reposicionamento manual periódico ou comparação dessas estratégias, considerando kWh captados, sombras, tempo de montagem, área segura disponível e efeito na duração da missão. Nenhuma política de implantação deve presumir viabilidade da recarga DC de tração antes da validação OEM.

### Integridade do registro
As seções **DEC-001 a DEC-043** foram preservadas byte a byte nesta atualização. Permanecem vigentes a escolha **DEC-001 B**, as comparações ainda pendentes (incluindo DEC-005, DEC-009, DEC-010, DEC-011, DEC-013, DEC-021, DEC-030, DEC-031, DEC-036 e DEC-042) e todas as decisões de DEC-002 a DEC-043.


## DEC-045 — Orientação e inclinação fixas dos painéis portáteis durante cada parada
**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026.** O usuário determinou: “utilizar painéis portáteis com orientação e inclinação fixas durante cada parada, calculadas conforme a geometria solar local, com operação somente estacionado”. Esta escolha encerra a comparação de **reposicionamento periódico** versus **montagem fixa por parada** para o cenário principal; não altera a quantidade de módulos, a estratégia de horários de parada ainda comparada na DEC-011 nem valida a interface solar→tração.

### Regra operacional aprovada
1. **Painéis portáteis:** manter a potência de referência de **1.600 Wp**, sujeita às validações de componentes e armazenamento. Montar/desmontar exclusivamente com o veículo **estacionado**, nunca gerar energia com os portáteis durante deslocamento. Os **1.540 Wp fixos de teto** mantêm seus critérios próprios, incluindo aprovação condicionada à instalação real (DEC-003/031).
2. **Ângulos de montagem:** calcular para cada parada a **orientação azimutal e inclinação** de montagem conforme latitude, longitude, data, horário e trajetória solar locais, com método documentado. Preferir orientação/ângulo que maximizem a energia ao longo da **janela efetiva da parada**, sujeitos às restrições do suporte, das sombras e do terreno; não presumir que um ângulo genérico sirva para toda a rota.
3. **Sem rastreamento intraparada:** após posicionados no começo da parada, manter azimute e inclinação **fixos até a desmontagem**; não modelar ajustes manuais periódicos ou rastreamento solar contínuo como operação aprovada. Para outra parada, uma nova orientação fixa poderá ser calculada.
4. **Energia produzida:** modelar geração **hora a hora** conforme DEC-038, usando irradiância no plano do arranjo, temperatura dos módulos, sombras, curvas/especificações dos módulos e perdas de MPPT, cabos e conversores. Distinguir potência nominal STC (Wp), energia bruta FV (kWh) e energia aproveitável entregue ao circuito efetivo (kWh); proibir dupla contagem entre serviços/tração conforme DEC-020/021.
5. **Logística e segurança:** considerar tempo realista de retirada, montagem, conexão, desligamento, inspeção e armazenamento dos portáteis, área livre sem obstrução de passagem, estabilidade dos suportes, proteção contra toque e falhas elétricas, e sua massa, volume, custo e fixação para transporte. Qualquer possibilidade de montagem depende de verificação do espaço e dos componentes comerciais. No cenário de referência com vento nulo, ainda documentar limitações de segurança para operação real com vento.
6. **Tração e buffer:** manter a **arquitetura B de recarga solar DC** da DEC-001 como direção escolhida, **sem comprovação da interface OEM**. A comparação entre recarga direta e buffer independente segue pendente na DEC-042; a decisão sobre orientação dos painéis não torna a recarga tecnicamente viável nem autoriza adicionar uma bateria intermediária.
7. **Missão de 7.000 km:** manter o máximo de 8 horas de condução por dia (DEC-006), SOC inicial de 100% em tração e serviços (DEC-044), ausência de recarga elétrica externa, condições meteorológicas da DEC-007 e **percurso plano de referência** da DEC-043. A comparação entre horários **fixos ou otimizados de direção e paradas** continua aprovada e inconclusa na DEC-011: em ambos os casos os portáteis não mudam de orientação durante a mesma parada.

### Responsáveis e entregáveis
- **P5:** implementar cálculo do azimute/ângulo fixo ótimo para cada janela de parada e contabilizar a geração horária, perdas, duração da parada e efeitos na autonomia, sem atribuir à tração energia que não possa ser carregada por interface validada.
- **P3:** definir modelos e suportes comerciais, área disponível durante montagem e volume/local de armazenamento com integração ao CAD; verificar interferências e circulação.
- **P2:** especificar MPPT, cabos, seccionamento e conexão/desconexão segura dos arranjos; não assumir recarga HV validada.
- **P1:** adicionar massas, fixações durante transporte e custos; **P6** ajuda a estabelecer o perfil de uso durante paradas.

### Pendências mantidas
As decisões anteriores **DEC-001 a DEC-044 permanecem integralmente preservadas**, inclusive todas as escolhas condicionais e comparações ainda em aberto: variante do E-Ducato (DEC-036), capacidade auxiliar 24/48 h (DEC-005), reservas 10/20 vs 20/30 (DEC-013), alocação de painéis (DEC-021), interface DC OEM e eventual buffer (DEC-001/042), horários de condução/paradas (DEC-011), desempenho e envelope CAD.

### Próxima pergunta a deliberar (DEC-046)
Escolher o nível de detalhamento do **perfil horário de consumo dos serviços elétricos** (cozinha, geladeira, ar-condicionado, boiler, lavanderia, iluminação, bombas e eletrônicos) durante condução e paradas: cargas médias simplificadas, perfil operacional horário ou perfil horário com cenários de sensibilidade. Esta decisão é diferente da DEC-004, que já aprovou uso moderado, e da DEC-019, que já aprovou o gerenciamento de simultaneidade; agora o foco é o **método de quantificação dos kWh consumidos** para dimensionar os bancos LiFePO₄ de 24/48 h (DEC-005), respeitando prioridades e limites do inversor.

### Verificação de integridade
A DEC-045 foi acrescentada ao fim do arquivo sem alterar os bytes das seções DEC-001 a DEC-044.


---

## DEC-046 — Consumo médio diário simplificado dos equipamentos internos

**Status: METODOLOGIA APROVADA PELO USUÁRIO EM 29/10/2026; POTÊNCIAS, HORAS DE USO, ENERGIA DIÁRIA E CAPACIDADE FINAL DA BATERIA AINDA PENDENTES DE DADOS COMERCIAIS E CÁLCULO.**

**Deliberação do usuário:** “Decisão 46: utilizar consumo médio diário simplificado dos equipamentos internos para dimensionar a bateria auxiliar, com valores documentados e incertezas explícitas.”

### Requisitos aprovados
1. **Método de energia diária:** construir uma tabela por equipamento com identificação comercial, potência elétrica ou energia por ciclo, fator de utilização/tempo médio diário, consumo em kWh/dia, fonte e faixa de incerteza. Adotar a soma dessas parcelas como **consumo diário médio de referência** para o banco de serviços independente de 48 V. Empregar, quando adequado, \(E_{dia}=\sum_i P_{i,el}\,t_{i,dia}\), considerando ciclos do compressor, aparelhos intermitentes e consumos em espera sem fingir funcionamento contínuo dos aparelhos.
2. **Equipamentos:** contemplar geladeira, iluminação, eletrônicos, bombas, cozinha, boiler elétrico, ar-condicionado e lavadora/secadora 2 em 1 **de uso ocasional**. Para lavanderia, declarar frequência média semanal e converter para consumo diário médio, sem assumir que funciona todos os dias; verificar também a energia de um dia com operação da lavanderia, como limitação pontual, se necessária ao dimensionamento.
3. **Perdas de conversão:** diferenciar potência elétrica de entrada do ar-condicionado de sua capacidade nominal de refrigeração; incluir perdas documentadas do inversor, dos conversores e consumos auxiliares necessários à operação. Evitar somar perdas em duplicidade.
4. **Incertezas obrigatórias:** onde não houver dados comerciais, identificar estimativas e utilizar faixas justificadas de potência, tempo de uso e consumo, sem apresentar valores inferidos como especificações do fabricante. Distinguir dados medidos, ficha técnica, estimativa e hipótese de projeto.
5. **Autonomia sem Sol (DEC-005):** dimensionar e comparar os bancos para **24 h e 48 h sem geração fotovoltaica**, com energia utilizável real, SOC mínimo/limites permitidos pelo fabricante, eficiência elétrica e margens necessárias. A capacidade preliminar de **10,24 kWh** não é escolha final; usar somente como candidato de comparação até a seleção de módulos LiFePO₄ comerciais (DEC-039).
6. **Verificação de potência distinta da energia média:** o método simplificado **não autoriza dispensar** o dimensionamento de potência instantânea, correntes de partida, simultaneidade e correntes dos cabos: respeitar o gerenciamento de cargas já aprovado (DEC-019), o inversor candidato ainda não validado e os requisitos detalhados de segurança (DEC-040). Não transformar média de kWh/dia em alegação de capacidade de atender todos os equipamentos simultaneamente.
7. **Separação energética:** os equipamentos habitáveis são alimentados pelo banco de serviços de 48 V independente do banco HV de tração (DEC-020); não computar energia do pack HV como recurso de serviços. A alocação da geração solar segue em análise (DEC-021), e a viabilidade de recarga solar da tração por arquitetura B (DEC-001, DEC-042) continua não demonstrada.

### Responsáveis e entregáveis
- **P6 — Líder dos consumos de serviços:** fornecer inventário de cargas, dados comerciais, hábitos médios, tabelas kWh/dia com fontes e incertezas; considerar o perfil moderado da DEC-004 e o uso ocasional da lavadora/secadora da DEC-015.
- **P2 — Dimensionamento:** consolidar eficiência e perdas, comparar capacidades utilizáveis de 24 h e 48 h dos módulos LiFePO₄, checar potências, correntes, inversor e proteções sem depender de perfil horário detalhado.
- **P5 — Balanço de energia:** integrar consumo médio de serviços à simulação de geração e à missão solar, mantendo separação da tração e coerência nas paradas.
- **P1/P3 — Integração:** atualizar massa, custo e volume dos equipamentos e baterias quando selecionados, respeitando a fonte única de parâmetros da DEC-035.

### Pendências e preservação
Esta decisão **escolhe o método simplificado de consumo médio diário**; **não aprova** os valores finais de consumo, a capacidade da bateria auxiliar, o modelo final de inversor ou a viabilidade de recarga FV→tração. Mantidas integralmente **DEC-001 a DEC-045**, inclusive **DEC-001 B** e as comparações pendentes de capacidade 24/48 h, reservas 10/20 × 20/30, variantes OEM, paradas, painéis e interface de carregamento.

### Próxima pergunta a deliberar (DEC-047)
Definir a **prioridade de cargas e a estratégia de redução automática ou manual de consumo quando o SOC da bateria auxiliar estiver baixo**, preservando o gerenciamento de simultaneidade da DEC-019. Comparar: apenas avisos para operação manual; desligamento escalonado automático de cargas não essenciais; ou modelagem comparativa antes de escolher. Não pressupor operação do ar-condicionado/boiler/lavanderia abaixo dos limites seguros do sistema.

### Verificação de integridade
A DEC-046 foi acrescentada ao final do arquivo, sem modificar os bytes preexistentes das decisões DEC-001 a DEC-045.


---

## DEC-047 — Gerenciamento automático escalonado de cargas por SOC da bateria auxiliar

**Status: ESTRATÉGIA APROVADA PELO USUÁRIO EM 29/10/2026; PATAMARES DE SOC, PRIORIDADES INDIVIDUAIS, HARDWARE E LÓGICA DE IMPLEMENTAÇÃO SUJEITOS À SELEÇÃO E VALIDAÇÃO DOS COMPONENTES.**

**Deliberação textual do usuário:** “Decisão 47: adotar gerenciamento automático escalonado das cargas de serviços por prioridade em função do SOC da bateria auxiliar de 48 V, desligando primeiro cargas não essenciais e preservando cargas prioritárias conforme a energia disponível e os limites do BMS. Definir limites concretos somente após seleção e validação da bateria.”

### Regras e critérios aprovados
1. **Escalonamento automático:** monitorar o SOC e os alarmes/estados do BMS do banco auxiliar LiFePO₄ de 48 V, e desconectar progressivamente cargas não essenciais quando a energia disponível se aproximar dos patamares de proteção operacionais. A gestão deve respeitar os limites de tensão, corrente, temperatura e SOC documentados pelo fabricante e a capacidade real de controle do inversor/distribuição.
2. **Prioridade funcional proposta, pendente de validação:** preservar enquanto tecnicamente possível cargas críticas de segurança, monitoramento, comunicação e iluminação essencial; manter a geladeira em prioridade alta conforme o balanço energético e o tempo de preservação de alimentos; atribuir prioridade intermediária, condicionada à necessidade, a bombas e tomadas; desligar antecipadamente cargas adiáveis ou de alta demanda, como lavadora/secadora, boiler e climatização não essencial. Não transformar essa ordem indicativa em especificação fechada sem validação com o P6.
3. **Limiares não escolhidos:** não fixar arbitrariamente SOC de alarme, desligamento, religamento ou reserva. Definir esses valores **somente após** selecionar módulos comerciais, obter limites e telemetria do BMS e concluir a comparação de reservas de tração/serviços da DEC-013 (10%/20% versus 20%/30%). Usar histerese/condições de religamento que evitem chaveamento repetitivo e respeitem recomendações do fabricante.
4. **Hierarquia de proteção:** a lógica de gerenciamento energético não substitui o BMS, fusíveis, disjuntores, desligamento de emergência ou proteções dos circuitos. Em falha de comunicação, medida inválida ou condição insegura, o comportamento deverá ser especificado para um estado seguro. Nenhuma carga prioritária pode ser garantida indefinidamente caso falte energia.
5. **Compatibilidade com decisões anteriores:** complementar o gerenciamento de simultaneidade/limites de potência da DEC-019 e as proteções e análise de falhas da DEC-040. Manter o método de consumo médio diário da DEC-046; **não exigir** perfil horário detalhado para dimensionar energia, mas verificar picos, arranque e priorização para o projeto elétrico. Preservar a independência da bateria de serviços em relação ao pack HV (DEC-020); nunca usar a tração para suprir serviços.
6. **Cenários de análise:** estimar quais cargas são retiradas em cada estágio, impacto na autonomia de serviços de 24 e 48 horas sem Sol (DEC-005), possibilidade de manter cargas críticas acima dos limites mínimos e comportamento perante baixo SOC e falhas, sempre declarando dependência de dados técnicos reais.
7. **Segurança e condição acadêmica:** apresentar diagrama funcional, matriz preliminar de prioridades, requisitos de sensores/atuadores, avisos aos ocupantes, estados e plano de validação; não alegar que o gerenciamento foi implementado fisicamente, ensaiado ou certificado antes de evidências.

### Responsáveis e entregáveis
- **P2 (líder):** selecionar arquitetura de medição/comando, levantar limites do BMS e inversor, definir comutação segura, matriz SOC × estágio × cargas e plano de falhas e ensaios.
- **P6:** classificar as cargas habitáveis e documentar consequências do desligamento para segurança, conforto e preservação de alimentos; relacionar ao consumo médio diário aprovado.
- **P5:** simular efeito das prioridades na autonomia dos serviços e paradas, sem dupla contagem de energia ou uso do banco HV.
- **P1/P3:** incorporar massa, custo, integração e espaço dos módulos de proteção/comando. **P7:** avaliar limitações térmicas pertinentes aos equipamentos de potência.

### Pendências explícitas e preservação
A DEC-047 **aprova o gerenciamento automático escalonado, não os limites de SOC**. Permanecem pendentes o modelo e capacidade da bateria auxiliar, comparação 24 h × 48 h (DEC-005), reservas (DEC-013), escolha/compatibilidade de inversor (DEC-019), definição de equipamentos e ensaios de proteções (DEC-040). **DEC-001 a DEC-046 preservadas integralmente**, incluindo seleção da alternativa B na DEC-001, validação da recarga DC ainda inconclusa e todas as comparações sem vencedor definido.

### Próxima pergunta a deliberar (DEC-048)
Definir o grau de detalhamento do **sistema hidráulico de água limpa, água quente e águas residuais**: dimensionamento básico por fichas técnicas; modelo hidráulico completo; ou projeto documentado de referência com bomba, vazão, pressão, tubulações, perdas e cenários de uso. Manter 100 L limpos, 70 L cinzas e cassete de aproximadamente 20 L (DEC-008/018/041), boiler elétrico compacto (DEC-017), abastecimento/descarte nas paradas sem recarga elétrica externa e compatibilidade com lavadora/secadora eventual (DEC-015).

### Verificação de integridade
Esta seção DEC-047 foi acrescentada em operação de anexação, sem alteração dos bytes preexistentes das decisões DEC-001 a DEC-046.


---

## DEC-048 — Projeto hidráulico documentado, com dimensionamento essencial e componentes comerciais

**Status: ALTERNATIVA C APROVADA PELO USUÁRIO EM 29/10/2026; COMPONENTES, PRESSÕES, VAZÕES, DIÂMETROS E PREÇOS AINDA PENDENTES DE SELEÇÃO E VALIDAÇÃO.**

**Deliberação textual do usuário:** “Decisão 48: desenvolver projeto hidráulico documentado com componentes comerciais e cálculos essenciais de bomba, vazão, pressão, tubulações e perdas de carga críticas, considerando chuveiro, boiler, pia, lavadora/secadora, drenagem, consumo elétrico, integração ao CAD e manutenção, sem exigir simulação hidráulica complexa de toda a rede.”

### Diretrizes e escopo aprovados
1. **Arquitetura hidráulica:** elaborar diagrama funcional da distribuição de água limpa, água quente e águas residuais. Manter **100 L de água limpa**, **70 L de águas cinzas** e **sanitário com cassete removível de aproximadamente 20 L**, este último sem tanque adicional de águas negras (DEC-008/018). Separar corretamente os circuitos de resíduos do banheiro e de águas cinzas.
2. **Componentes reais e documentados:** selecionar candidatos comerciais para bomba pressurizadora, válvulas, conexões, filtros, tubos/mangueiras, reservatórios, instrumentos de nível/pressão e acessórios pertinentes; registrar marca, modelo, dados de fabricante, materiais adequados, dimensões, massa, tensão, potência, custos, fontes e disponibilidade. Não inventar especificações OEM/comerciais (DEC-012).
3. **Cálculos essenciais, não rede completa de alta fidelidade:** estimar vazões e pressões de projeto de chuveiro e pia, requisitos hidráulicos da lavadora/secadora, perdas de carga nos **trechos críticos** e diâmetros de tubulações, compatibilizando com a **curva da bomba selecionada** e a altura geométrica. Verificar desempenho em cenários representativos de operação, sem exigir CFD de fluidos ou simulação transitória extensa da rede.
4. **Água quente:** integrar o **boiler elétrico compacto aprovado na DEC-017** ao circuito de chuveiro e demais pontos previstos, com capacidade/potência ainda a dimensionar. Considerar mistura, temperatura segura de utilização, isolamento, pressão admissível, expansão/alívio e requisitos do fabricante. Não confundir energia térmica exigida com potência elétrica instantânea.
5. **Lavadora/secadora 2 em 1:** integrar abastecimento e drenagem do equipamento **de uso ocasional** da DEC-015, condicionando conexões e necessidades de vazão/pressão às fichas técnicas do modelo escolhido; contabilizar água e energia sem assumir que funciona diariamente (DEC-004/046).
6. **Drenagem e salubridade:** dimensionar caminhos de drenagem e conexões do reservatório de águas cinzas, prevenindo refluxo, vazamentos, odores, congelamento quando pertinente e dificuldade de acesso. O cassete sanitário deve manter sua lógica de retirada e descarte independente. Estabelecer inspeções, limpeza, acesso e manutenção preventiva; não afirmar certificação não demonstrada.
7. **Balanço de água e massa:** calcular consumos médios para **dois ocupantes** com perfil moderado, frequência estimada de reabastecimento/descarga e níveis de reservatórios. A água deslocada entre tanques muda de posição e não deve ser contabilizada duas vezes como massa (DEC-008/022). **Reabastecer água limpa e descartar resíduos nas paradas está permitido pela DEC-041; recarga elétrica externa permanece proibida na missão solar.**
8. **Integração elétrica e CAD:** incluir consumo elétrico da bomba/controles no banco independente **LiFePO4 48 V** por conversão compatível, ou circuito DC de serviço autorizado conforme equipamento real, sem presumir que bombas comerciais operem diretamente a 48 V. Verificar proteções elétricas (DEC-040), gerenciamento de carga (DEC-019/047), compatibilidade com inversor candidato e disposição física/centro de gravidade/ancoragem de reservatórios e componentes no CAD (DEC-030/033).
9. **Limites e incertezas:** explicitar pressão e vazão nas condições consideradas, hipóteses de perdas e simultaneidade, margem de dimensionamento, disponibilidade das peças e incertezas. **Não exigir simulação hidráulica complexa de toda a rede**; nenhuma capacidade de bomba, diâmetro ou reservatório novo está aprovado além dos volumes já decididos.

### Responsáveis e entregáveis
- **P6 — líder dos equipamentos hidráulicos:** diagrama do sistema, lista comercial, requisitos de consumo de água/água quente e operação de chuveiro, pia e lavanderia, cálculos essenciais de vazão, pressão e perdas críticas.
- **P2 — integração elétrica:** tensão de alimentação da bomba, potência média e pico, proteção, acionamento e compatibilidade com inversor e gerenciamento de cargas.
- **P3 — integração CAD:** rotas de tubulação, dimensões, acessibilidade/manutenção, reservatórios, posição/centro de gravidade e interfaces do banheiro/cozinha.
- **P1 — massa e custo:** consolidar massa dos reservatórios, água, acessórios e suportes, custo rastreável e validação das fixações críticas.
- **P5 — missão solar:** integrar demanda de água e paradas de reabastecimento/descarte sem inserir recarga elétrica externa.

### Comparações e pendências preservadas
A decisão fixa **o nível de detalhamento do projeto hidráulico**, não aprova modelos comerciais, valores finais de vazão/pressão, boiler, bomba ou dimensionamento das tubulações. Preservar todas as decisões **DEC-001 a DEC-047**, especialmente a **alternativa B de recarga solar DC escolhida na DEC-001**, a independência da bateria auxiliar e a validação ainda não comprovada de interface OEM, além das comparações pendentes (capacidade 24/48 h, reservas, variantes de E-Ducato, ar-condicionado, isolamento/instalação, layouts e estratégias solares).

### Próxima pergunta a deliberar (DEC-049)
Definir a **estratégia de ventilação e controle de umidade** no interior do motorhome para dois ocupantes, cozinha, chuveiro e lavadora/secadora: ventilação natural passiva, ventilação mecânica com exaustão, ou solução híbrida. Verificar interferência das aberturas com a meta de 1.540 Wp no teto (DEC-031), consumo dos ventiladores, proteção contra ingresso de água, isolamento e conforto. **Não confundir operação normal ventilada com o ensaio térmico do item 31, que exige o veículo fechado, sem ocupantes e sem ar-condicionado (DEC-027).**

### Verificação de integridade
A DEC-048 foi acrescentada somente ao final do arquivo; os bytes anteriores das decisões DEC-001 a DEC-047 foram preservados sem alterações.


---

## DEC-049 — Ventilação natural por aberturas e janelas

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; DIMENSIONAMENTO, POSIÇÃO DAS ABERTURAS E VERIFICAÇÃO DA RENOVAÇÃO DE AR AINDA PENDENTES.**

**Deliberação textual do usuário:** “Decisão 49: priorizar ventilação natural por aberturas e janelas, avaliando renovação de ar, umidade, conforto e integração ao CAD. Registre a decisão 49, preserve integralmente as decisões 1 a 48, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretrizes aprovadas
1. **Arquitetura escolhida:** priorizar a renovação natural de ar do habitáculo por **aberturas e janelas**, sem adotar como baseline um sistema de exaustão mecânica ou ventilação híbrida. Aberturas e sua geometria, quantidade, localização e modos de operação serão dimensionados e verificados, não arbitrados. A escolha não comprova, por si só, vazão de ar suficiente.
2. **Qualidade do ar e umidade:** avaliar renovação de ar para **dois ocupantes** em uso habitável normal, vapor e condensação de banho, cozinha e lavanderia 2 em 1 de uso ocasional. Considerar diferenças térmicas, vento disponível nos cenários operacionais, ventilação cruzada, privacidade, proteção contra chuva, insetos, ruído e exigências de segurança. **Com vento externo nulo** não assumir ventilação cruzada impulsionada pelo vento; investigar possível efeito chaminé e informar limites ou insuficiência de vazão.
3. **Isolamento e conforto:** verificar compromisso entre ventilação, perdas/ganhos térmicos, controle de condensação e potência do ar-condicionado; não presumir que ventilação natural isoladamente garanta condições interiores de conforto e salubridade em todas as situações. Se a verificação demonstrar insuficiência ou exigência normativa de ventilação permanente, **registrar a não conformidade e propor revisão específica para aprovação**, em vez de incluir ventiladores ou exaustores sem decisão.
4. **Integração geométrica:** P3 e P6 deverão incluir as aberturas, telas, vedações e mecanismos reais no CAD e verificar interferências com teto, painéis fixos de **1.540 Wp como meta condicional à viabilidade física** (DEC-003/031), painéis portáteis estacionários, isolamento (DEC-016), layout interno ainda pendente (DEC-030), massas, acesso e estanqueidade.
5. **Separação de cenários:** o ensaio obrigatório do **item 31** permanece com motorhome **estacionado, fechado, sem ocupantes e sem ar-condicionado**, nas condições de 21 de junho em São Carlos, conforme DEC-027. Isso é distinto do cenário operacional com janelas/aberturas abertas; não adicionar vazão de ventilação natural no ensaio fechado sem suporte explícito nas condições de contorno.
6. **Escopo elétrico e de custos:** a escolha prioritária por ventilação passiva **não aprova nem demanda automaticamente exaustores motorizados**. Descrever mecanismos passivos reais e seus custos, massas e manutenção. Caso componentes elétricos auxiliares sejam futuramente propostos, tratar como nova decisão e incorporar consumos ao balanço energético apenas após aprovação.
7. **Evidência e incertezas:** documentar dimensões e mecanismos por fichas técnicas, hipóteses de vazões e diferenças térmicas, cenários de umidade, limites das estimativas e critérios de verificação; não alegar ventilação adequada sem cálculo/justificativa.

### Responsáveis e entregáveis
- **P6 (líder):** estudo de renovação de ar e umidade, modos operacionais com banho/cozinha/lavanderia, avaliação de condensação e conforto, eventual apontamento de insuficiências.
- **P3:** CAD com janelas, aberturas, interferências no teto, fixações, estanqueidade e acesso.
- **P1:** massa e custo dos componentes, verificações de instalação e de modificações da carroceria quando aplicáveis.
- **P2/P5:** avaliar eventuais cargas elétricas apenas se futuramente aprovadas; preservar balanços de energia existentes.

### Comparações e pendências preservadas
Todas as decisões **DEC-001 a DEC-048 permanecem integralmente preservadas**, incluindo a **alternativa B escolhida na DEC-001** (carga solar/DC por interface HV externa autorizada, **ainda sem viabilidade técnica comprovada**), independência dos bancos de baterias (DEC-020), comparação de recarga direta versus buffer (DEC-042), capacidades 24 h/48 h, reservas, variantes E-Ducato, layouts, ar-condicionado e demais comparações sem alternativa final. A DEC-049 escolhe ventilação natural como prioridade, **não** resolve automaticamente vazões, umidade, segurança ou necessidade futura de exceções.

### Próxima pergunta a deliberar (DEC-050)
Definir a **tecnologia e alimentação elétrica da geladeira habitável**, que opera continuamente: compressor DC de baixa tensão alimentado por conversor apropriado desde o barramento de serviços 48 V; geladeira AC pelo inversor; ou comparação entre as alternativas usando **consumo médio diário documentado** (DEC-046), eficiência, potência de partida, massa, volume, dimensões do CAD, custo e compatibilidade com o gerenciamento de cargas automático (DEC-047). Não presumir ligação direta de equipamento 12/24 V ao barramento 48 V.

### Verificação de integridade
A DEC-049 foi acrescentada somente ao final do arquivo, sem modificar os bytes preexistentes das seções DEC-001 a DEC-048.


---

## DEC-050 — Geladeira comercial AC compacta alimentada pelo inversor de serviços

**Status: ALTERNATIVA B APROVADA PELO USUÁRIO EM 29/10/2026; MODELO, CAPACIDADE, CONSUMO, PICO DE PARTIDA, COMPATIBILIDADE, MASSA E CUSTO AINDA SUJEITOS A VALIDAÇÃO.**

**Deliberação textual do usuário:** “Decisão 50: priorizar geladeira comercial AC compacta alimentada pelo inversor dos serviços, validando consumo, potência de partida, perdas do inversor, capacidade, massa e custo. Registre a decisão 50, preserve integralmente as decisões 1 a 49, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretrizes aprovadas
1. **Tecnologia e arquitetura escolhidas:** priorizar uma **geladeira comercial AC compacta, preferencialmente com compressor e consumo documentado**, alimentada pela **saída AC do inversor conectado ao banco de serviços independente de 48 V**. Não escolher como solução principal uma geladeira DC 12/24 V alimentada por conversor DC/DC. A especificação definitiva depende de verificação técnica, não apenas de disponibilidade comercial.
2. **Operação contínua e energia:** a geladeira deverá ser capaz de funcionar continuamente durante deslocamentos e paradas, com o compressor ciclando conforme temperatura e condições ambientais. Para a DEC-046, computar **consumo médio diário documentado (kWh/dia)** sob condições de teste identificadas e corrigir ou realizar sensibilidade para a temperatura ambiente e a instalação real. Não confundir potência nominal instantânea com consumo médio de 24 horas.
3. **Inversor e perdas:** verificar tensão/frequência AC do modelo comercial e compatibilidade com a saída do inversor candidato **Victron MultiPlus-II 48/5000**, cuja seleção final ainda não foi aprovada (DEC-019). Considerar **consumo em vazio/standby do inversor durante 24 h**, eficiência em cargas parciais, perdas de conversão e a energia total efetivamente drenada da bateria. Avaliar picos/transitórios de partida do compressor, simultaneidade com cargas maiores e capacidade contínua/sobrecarga do inversor em condições ambientais relevantes.
4. **Gerenciamento de cargas e segurança:** tratar a geladeira como **carga habitável de prioridade alta** na lógica de desligamento escalonado por SOC da DEC-047, mas sem prometer alimentação indefinida abaixo dos limites seguros da bateria/BMS. Identificar as consequências de interrupção para alimentos e definir alertas/regras de religamento após restabelecimento de energia. Todas as proteções AC e conexões serão detalhadas conforme DEC-040.
5. **Escolha comercial rastreável:** P6 selecionará modelos candidatos comparáveis com marca/modelo, capacidade interna (L), dimensões, massa, faixa de temperatura, demanda média, tensão e frequência, potência/partida, ruído, ventilação recomendada, preço e fonte/data. Não inventar especificações para equipamentos ou inverter não verificados; se dados de partida não existirem, manter hipótese e incerteza explícitas e solicitar documentação adicional.
6. **Integração física e térmica:** P3/P6 devem reservar no CAD o volume de montagem, abertura de portas, folgas de circulação de ar/ventilação do condensador, fixações para frenagem e acesso de manutenção, sem presumir que modelos domésticos se adequem automaticamente ao uso veicular. Avaliar impacto do calor rejeitado pela geladeira sobre a cabine e seu sistema de climatização (DEC-010/028), bem como ruído e estabilidade em viagem.
7. **Capacidade e autonomia:** escolher volume útil adequado a **dois ocupantes** e ao perfil moderado (DEC-004), computar perdas no inversor e contribuição no balanço total de consumo médio (DEC-046), e incorporar nos cenários de **24 versus 48 horas** sem geração solar para a bateria LiFePO4 auxiliar modular (DEC-005/039). Não fixar por esta decisão a capacidade final da bateria, potência do inversor ou marca da geladeira.
8. **Independência e limites:** preservar a **DEC-020**: não utilizar bateria de tração HV para suprir geladeira ou qualquer carga habitável. A **DEC-001 alternativa B** continua como arquitetura aprovada para investigação da recarga solar DC da tração, mas não está tecnicamente demonstrada. Não transferir energia entre os bancos nem contabilizar duas vezes a geração solar.

### Responsáveis e entregáveis
- **P6 (líder):** shortlist documentada de geladeiras AC compactas, critérios de volume útil, energia média diária, ruído, integração de uso, massa, preço e carga térmica dissipativa.
- **P2:** validação de alimentação AC, picos de partida, consumo e eficiência do inversor em operação 24 h, proteções e prioridade da carga conforme DEC-047.
- **P3:** integração CAD, espaço de ventilação, acesso, fixações e distribuição de massa.
- **P1:** massa final, suportes e custo documentado.
- **P5:** contabilização da energia drenada da bateria de serviços e impacto nas autonomias de 24/48 horas, respeitando independência do pack HV.

### Comparações e pendências preservadas
A DEC-050 **aprova a prioridade da geladeira AC pelo inversor**, e não um modelo definitivo ou a aprovação do inversor. Preservar integralmente **DEC-001 a DEC-049**, sobretudo DEC-001 **alternativa B** selecionada (interface solar→tração ainda não validada), DEC-020 (bancos independentes), DEC-019 e DEC-040 (inversor e projeto elétrico), DEC-046 (consumo médio simplificado), DEC-047 (gestão automática de prioridades), DEC-005 e DEC-039 (capacidade e módulos auxiliares ainda por dimensionar) e todas as demais comparações pendentes.

### Próxima pergunta a deliberar (DEC-051)
Definir a **configuração de cozinha elétrica**, já prevista na DEC-004 e considerada no gerenciamento de simultaneidade da DEC-019: cooktop de indução portátil com uma zona, cooktop de indução embutido com duas zonas, ou comparar ambas quanto a consumo médio diário, potência de pico, simultaneidade, requisitos de ventilação/segurança, integração CAD, massa, preço e compatibilidade com o inversor ainda candidato. Não aprovar cargas adicionais, potência total ou dispositivos sem validação comercial.

### Verificação de integridade
A DEC-050 foi acrescentada por anexação ao final do arquivo. Os bytes anteriormente presentes — incluindo todas as decisões DEC-001 a DEC-049, suas comparações e pendências — não foram alterados.


---

## DEC-051 — Cooktop de indução portátil com uma zona e potência ajustável

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; MODELO, POTÊNCIA MÁXIMA E AJUSTÁVEL, CONSUMO, MASSA, DIMENSÕES, SEGURANÇA, CUSTO E COMPATIBILIDADE ELÉTRICA AINDA SUJEITOS À VALIDAÇÃO.**

**Deliberação textual do usuário:** “Decisão 51: priorizar cooktop de indução portátil com uma zona de aquecimento, de potência ajustável, sujeito à seleção comercial e validação elétrica, térmica e dimensional. Registre a decisão 51, preserve integralmente as decisões 1 a 50, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretrizes aprovadas
1. **Tecnologia e configuração escolhidas:** priorizar **cooktop comercial portátil de indução com uma única zona de aquecimento**, dotado de ajuste de potência efetivo e documentado. Esta decisão não seleciona marca ou modelo específico, não fixa a potência máxima ou mínima e não aprova automaticamente um segundo queimador ou cooktop embutido. A mobilidade do aparelho não implica uso durante a condução: deverá haver armazenamento e retenção seguros para o deslocamento.
2. **Alimentação elétrica:** o cooktop será tratado como **carga AC alimentada pelo inversor do banco independente de serviços de 48 V**, sem conexão à bateria de tração HV (DEC-020). Validar tensão, frequência, forma de onda, potência contínua, fatores de partida/transitórios e demais exigências da ficha técnica perante o inversor candidato **Victron MultiPlus-II 48/5000** (DEC-019), sem pressupor que seja a seleção final. Verificar potência nominal contínua e derating do conjunto, corrente real do banco e eficiência em cargas parciais.
3. **Uso moderado e consumo diário:** inserir o cooktop no cenário de cozinha elétrica de uso programado da DEC-004 e calcular **energia média diária (kWh/dia)** conforme a metodologia simplificada da DEC-046, baseada em potência efetiva, tempo de utilização e eficiência do inversor. Separar o consumo médio da exigência de **potência instantânea máxima**, que deve ser verificada adicionalmente. Documentar hipóteses e análise de sensibilidade quando faltarem dados reais.
4. **Gerenciamento de cargas:** compatibilizar a potência escolhida com a DEC-019 e a lógica automática de prioridades da DEC-047, evitando simultaneidade imprópria com boiler, lavadora/secadora, ar-condicionado ou outras cargas elevadas. O cooktop não é carga essencial em situação de baixo SOC; validar critérios e condições de desligamento com os limites reais do banco/BMS antes de programar limiares definitivos.
5. **Segurança e integração:** dimensionar circuito AC, cabo, conectores, proteção contra sobrecorrente e choque elétrico, disjuntores, dispositivos de proteção aplicáveis, pontos de desligamento e aterramento/equipotencialização segundo DEC-040 e requisitos do fabricante. Avaliar superfície quente, afastamento de materiais combustíveis, estabilidade sobre bancada, uso de panelas compatíveis e eventual aquecimento/umidade da cabine. Preservar DEC-049 (ventilação natural como prioridade), verificando se será suficiente em uso real, sem assumir conformidade já demonstrada.
6. **Integração CAD e massa:** P3/P6 deverão verificar área de uso sobre bancada, folga para panelas, acesso a tomada, armazenamento seguro durante deslocamento, ergonomia, massa e fixação/retentores pertinentes (DEC-030/033). Incluir custo e acessórios obrigatórios no orçamento da DEC-034 sem dupla contagem.
7. **Rastreabilidade de componentes:** a seleção comercial deverá indicar marca, modelo, potência máxima e faixas reais de ajuste, alimentação (tensão/frequência), dimensões, massa, consumo/eficiência, certificações e advertências aplicáveis, custo, mercado e data/fonte; dados não publicados deverão permanecer como hipóteses explicitadas, conforme DEC-012 e DEC-035.
8. **Dependências preservadas:** a capacidade final da bateria auxiliar 24/48 h permanece pendente (DEC-005/039); a compatibilidade e seleção do inversor permanecem pendentes (DEC-019/040); não alterar as condições do ensaio térmico de cabine fechado sem ocupantes da DEC-027 nem a independência dos bancos (DEC-020). A escolha da DEC-001 é **arquitetura B solar/DC com interface de carregamento autorizada, ainda não validada tecnicamente**.

### Responsáveis e entregáveis
- **P6 (líder):** selecionar candidatos comerciais de uma zona, potência ajustável e consumo médio diário; definir rotina de uso, segurança térmica e compatibilidade com o layout interno.
- **P2:** verificar saída AC do inversor, correntes/picos, proteções, tensão/frequência, lógica de controle de cargas e limites do BMS.
- **P3:** integração no CAD da bancada, tomada, distância a superfícies e espaço de armazenamento/retensão durante viagem.
- **P1:** consolidar massa e custo no orçamento do motorhome.
- **P5:** incorporar consumo e perdas ao balanço energético e ao dimensionamento de 24/48 h da bateria auxiliar.

### Comparações e pendências preservadas
A DEC-051 **aprova a prioridade por cooktop portátil de indução de uma zona e potência ajustável**, não a marca/modelo, a potência total admissível, o inversor definitivo ou uma instalação certificada. Preservar integralmente as **DEC-001 a DEC-050**, inclusive DEC-001 **alternativa B** selecionada (interface solar→tração não validada), DEC-005/039 (capacidade de serviços), DEC-010/028 (ar-condicionado), DEC-019 (inversor e gerenciamento), DEC-020 (bancos independentes), DEC-021/042 (alocação dos painéis e recarga DC com/sem buffer), DEC-036 (variante do E-Ducato), DEC-040 (projeto elétrico), DEC-046/047 (consumo médio e prioridades) e todas as demais comparações pendentes.

### Próxima pergunta a deliberar (DEC-052)
Definir o **padrão de tensão e frequência da rede AC habitável** (p. ex., 220 V/60 Hz no padrão brasileiro, 230 V/50 Hz no padrão europeu ou comparar ambos e congelar uma única configuração após a comparação de equipamentos e da variante veicular), para não misturar geladeira, cooktop, boiler, lavadora/secadora e inversor incompatíveis. Esta questão pertence exclusivamente ao sistema de serviços independente; não modifica a arquitetura HV OEM nem significa recarga externa autorizada.

### Verificação de integridade
A DEC-051 foi acrescentada ao final do arquivo por anexação. Os bytes anteriormente presentes, incluindo DEC-001 a DEC-050, não foram modificados. SHA-256 do arquivo antes da anexação: `b4ecddc718a7282d61196ff513936d934deae71f72ae4a6b2f5fba3da5b777ab`.


---

## DEC-052 — Padrão AC dos serviços: 220 V / 60 Hz

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; MODELOS COMERCIAIS, CONFIGURAÇÃO DO INVERSOR, POTÊNCIAS, PROTEÇÕES E COMPATIBILIDADE AINDA SUJEITOS A VALIDAÇÃO.**

**Deliberação textual do usuário:** “Decisão 52: adotar 220 V / 60 Hz como padrão principal da rede AC dos serviços do motorhome, selecionando inversor e equipamentos comerciais comprovadamente compatíveis. Registre a decisão 52, preserve integralmente as decisões 1 a 51, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretrizes aprovadas
1. **Padronização da rede habitável:** adotar **220 V em corrente alternada e frequência nominal de 60 Hz** como padrão de projeto para os circuitos AC de serviços do motorhome. Esta decisão pertence exclusivamente à instalação habitável e **não altera a arquitetura HV OEM**, a bateria de tração, interfaces de recarga ou os sistemas originais do veículo.
2. **Seleção do inversor:** selecionar e validar um inversor adequado para barramento de serviços LiFePO4 nominal de 48 V e **saída efetivamente compatível com 220 V / 60 Hz**. O Victron MultiPlus-II 48/5000 permanece **candidato** conforme DEC-019, não escolhido nem homologado automaticamente pela DEC-052; verificar a variante exata do fabricante, programabilidade de frequência/tensão, potência contínua, transitórios, rendimento e proteções antes da decisão final.
3. **Compatibilidade de cargas comerciais:** selecionar geladeira AC compacta (DEC-050), cooktop portátil de indução de uma zona (DEC-051), boiler elétrico (DEC-017), lavadora/secadora 2 em 1 (DEC-015), climatização ainda em comparação (DEC-010/028), tomadas e eletrônicos somente quando suas fichas técnicas confirmarem alimentação **220 V / 60 Hz**, ou quando a adaptação necessária for justificada e formalmente validada. Evitar misturar equipamentos 230 V / 50 Hz sem comprovação explícita de compatibilidade. Cada ficha técnica deve indicar mercado, data e fonte.
4. **Dimensionamento elétrico e térmico:** P2 deverá verificar correntes AC por circuito, demanda simultânea com gerenciamento de cargas da DEC-019/047, potência de pico e partida, seção de cabos, temperaturas, curto-circuito, sobrecorrentes, proteções diferenciais quando aplicáveis, seccionamento, aterramento/equipotencialização e requisitos do esquema de distribuição conforme DEC-040. Não presumir que a potência indicada pelo nome comercial do inversor corresponda à potência contínua ativa disponível em todas as temperaturas.
5. **Energia e autonomia:** quantificar a energia diária média demandada pelos equipamentos AC e as perdas do inversor, inclusive consumo em vazio quando aplicável, de acordo com a metodologia simplificada da DEC-046. Manter separados consumo de serviços e de tração (DEC-020/032) e continuar a comparação de 24 h/48 h sem geração solar para o banco de 48 V (DEC-005/039).
6. **Condições da missão:** a padronização **não autoriza recarga elétrica externa** durante a missão de 7.000 km (DEC-006/029/041/044). Qualquer entrada AC potencial do inversor/carregador deverá ser claramente representada e não utilizada nas simulações da missão, respeitando separação energética dos bancos e registros de fluxo sem dupla contagem.
7. **Segurança, instalação e rastreabilidade:** distinguir projeto acadêmico de instalação ensaiada/certificada, preservar a integridade do sistema HV OEM e as exigências de proteção do projeto de serviços (DEC-040). Registrar na fonte única de parâmetros da DEC-035 o padrão **AC_SERVICOS_TENSAO_NOMINAL=220 V** e **AC_SERVICOS_FREQUENCIA_NOMINAL=60 Hz**, indicando versões e tolerâncias documentadas dos equipamentos efetivamente selecionados.
8. **Dependências não solucionadas:** DEC-052 não congela o modelo/versão do inversor, a capacidade final LiFePO4, o ar-condicionado, a variante E-Ducato ou a interface DC solar→tração. A **alternativa B da DEC-001** permanece escolhida como arquitetura-alvo, porém sem viabilidade técnica comprovada, e as comparações DEC-021/042 ainda aguardam validação.

### Responsáveis e entregáveis
- **P2 (líder):** especificação única 220 V / 60 Hz; matriz de compatibilidade por carga/inversor; dimensionamento e proteção dos circuitos e validação do candidato MultiPlus-II 48/5000 frente a alternativas, caso necessário.
- **P6:** confirmar versões comerciais de geladeira, cooktop, boiler, lavadora/secadora, equipamentos térmicos e respectivas potências, consumo, dimensões e custos.
- **P3/P1:** integrar distribuição e equipamentos no CAD; verificar massa, fixação, custo e manutenção sem dupla contagem de componentes.
- **P5:** atualizar balanço de serviços e perdas de conversão; manter as simulações de tração e geração solar separadas.

### Comparações e pendências preservadas
As decisões **DEC-001 a DEC-051 permanecem integralmente preservadas**. Em particular: DEC-001 **alternativa B DC solar→interface de recarga HV autorizada** (ainda não validada), DEC-005/039 (capacidade auxiliar 24/48 h), DEC-010/028 (modelo de ar-condicionado), DEC-019/040 (inversor candidato, gerenciamento e proteção elétrica), DEC-020 (bancos independentes), DEC-021/042 (alocação FV, recarga direta ou buffer dedicado), DEC-036 (variante E-Ducato), DEC-046/047 (consumo médio e priorização de cargas), DEC-050/051 (geladeira AC e cooktop de indução prioritários, modelos ainda a selecionar). Não apresentar como concluídas comparações ainda em andamento.

### Próxima pergunta a deliberar (DEC-053)
Definir estratégia de seleção e validação do **inversor do banco de serviços nominal de 48 V para a rede 220 V / 60 Hz**, tendo o Victron MultiPlus-II 48/5000 apenas como candidato: (A) mantê-lo como referência sujeito a dados de versão/compatibilidade e potência, (B) priorizar alternativa comercial de maior potência, ou (C) comparar ao menos dois inversores comerciais reais usando simultaneidade, picos de partida, consumo em vazio, perdas, proteções, massa e custo, respeitando a DEC-019. Qualquer seleção depende de validação documental, não altera os bancos nem a arquitetura solar da tração.

### Verificação de integridade
A DEC-052 foi anexada ao final do arquivo sem alterar os bytes anteriores DEC-001 a DEC-051. SHA-256 do arquivo antes da anexação: `8d57f5ca77ad729fd1fe22067e4adf737ad68c5444c6f4d2a85b7add6c6b08c5`.


---

## DEC-053 — Comparação de inversores comerciais para serviços 48 V DC → 220 V / 60 Hz AC

**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; MODELO COMERCIAL DEFINITIVO NÃO SELECIONADO.** O usuário deliberou: “Decisão 53: comparar o Victron MultiPlus-II 48/5000 com pelo menos uma alternativa comercial para o sistema de serviços 48 V e 220 V / 60 Hz, avaliando potência contínua, picos, simultaneidade, consumo em vazio, eficiência, segurança, massa e custo antes de escolher o inversor definitivo.”

### Escopo e critérios obrigatórios da comparação
1. **Candidatos verificáveis:** comparar **Victron MultiPlus-II 48/5000** e **ao menos uma alternativa comercial real**, com fabricante, modelo, código/variante exata, mercado e ficha técnica atualizada e rastreável. O Victron é somente **candidato**, e nem a cifra “5000” nem o nome comercial devem ser tratados automaticamente como potência contínua ativa em watts.
2. **Compatibilidade elétrica:** verificar de forma documental que cada candidato opera com a **faixa real de tensões** do banco LiFePO₄ nominal de **48 V**, BMS e proteções (DEC-039/040), e entrega **220 V AC / 60 Hz** conforme DEC-052, seja nativamente, seja mediante configuração admitida pelo fabricante. Não inferir compatibilidade de 230 V/50 Hz sem documentação.
3. **Potência contínua e simultaneidade:** dimensionar pelo conjunto de cargas realmente selecionadas, com **gerenciamento de simultaneidade** da DEC-019. Diferenciar potência contínua em W, potência aparente em VA, fator de potência, derating por temperatura/ventilação e limites de corrente do banco de 48 V; separar cargas essenciais e programáveis.
4. **Picos e partidas:** verificar picos transitórios de geladeira AC (DEC-050), ar-condicionado ainda em comparação (DEC-010/028), lavadora/secadora (DEC-015), boiler (DEC-017) e cooktop portátil de indução de uma zona com potência ajustável (DEC-051). Não inventar correntes de partida nem assumir que todas as cargas funcionam juntas.
5. **Eficiência e consumo em vazio:** registrar curva de rendimento conforme carga, autoconsumo em repouso, perdas térmicas e efeitos sobre o **consumo médio diário** da DEC-046 e a autonomia de **24 h versus 48 h sem sol** da DEC-005. A DEC-046 não exige cronograma horário completo; picos e simultaneidade ainda devem ser conferidos separadamente.
6. **Segurança e integração:** comparar seccionamento DC, fusíveis e proteção contra curto/sobrecorrente, requisitos de aterramento/equipotencialização, proteção contra choque, falhas e isolamento, instalação/ventilação, dimensões, massa, ruído, custo, disponibilidade e manutenção. Integrar ao projeto elétrico acadêmico detalhado e plano de ensaios da DEC-040, sem afirmar certificação não obtida.
7. **Funções de carregador AC:** se um candidato também puder receber energia AC externa, representar essa função explicitamente e mantê-la **desabilitada/não utilizada na missão de 7.000 km**, conforme DEC-006/029/041/044; a escolha do inversor não autoriza recarga elétrica externa. Não alimentar a bateria de tração pelo banco auxiliar (DEC-020) nem utilizar o inversor como atalho para a alternativa A já descartada na DEC-001.
8. **Critério de decisão:** apresentar tabela comparativa de pelo menos dois produtos, com limites verificáveis, não conformidades, intervalos de custo, massa e eficiência e impactos na autonomia. **Não selecionar o vencedor automaticamente**; preparar recomendação tecnicamente fundamentada para deliberação posterior. Se nenhuma variante atender a 220 V / 60 Hz, documentar o bloqueio e solicitar nova decisão, sem alterar silenciosamente a DEC-052.

### Responsáveis e entregáveis
- **P2 (líder):** matriz de fichas técnicas e compatibilidade, dimensionamento W/VA e picos, eficiência/autoconsumo, proteções e análise comparativa reproduzível.
- **P6:** fornecer potências e consumos médios documentados da geladeira AC, cooktop e demais equipamentos, sem antecipar modelos pendentes.
- **P5:** incorporar perdas e consumo em vazio ao balanço de energia de serviços, sem dupla contagem com a tração.
- **P1/P3:** incluir massa, dimensões, ventilação, instalação e custo dos candidatos nos estudos de CAD e orçamento.

### Dependências e pendências preservadas
As **DEC-001 a DEC-052 permanecem integralmente preservadas**, inclusive a **alternativa B solar/DC para recarga de tração escolhida na DEC-001, ainda sem comprovação de interface física**, bancos de serviços e tração independentes (DEC-020), alocação FV em comparação (DEC-021), eventual buffer específico ainda não aprovado (DEC-042), comparações de capacidade de serviços (DEC-005/039), ar-condicionado (DEC-010/028), variante OEM (DEC-036) e a padronização AC de 220 V/60 Hz (DEC-052). A DEC-053 **autoriza apenas comparar inversores**, não autoriza aquisição, mudança de banco, recarga HV nem seleção definitiva.

### Próxima pergunta a deliberar (DEC-054)
Definir a **estratégia de controladores MPPT para os arranjos fotovoltaicos fixos (1.540 Wp meta sujeita ao CAD) e portáteis (1.600 Wp somente estacionado)**: (A) controladores independentes por arranjo, (B) estudar um MPPT compartilhado condicionado à compatibilidade elétrica e de sombreamento, ou (C) comparar tecnicamente ambas as topologias antes de selecionar componentes, considerando orientação solar distinta, tensões/correntes, comutação segura, eficiência, custos e independência dos bancos da DEC-020. Nenhuma topologia valida por si só a interface solar/DC de recarga da tração.

### Verificação de integridade
A DEC-053 foi acrescentada ao final do arquivo por anexação, sem modificar os bytes anteriores DEC-001 a DEC-052. SHA-256 do arquivo antes da anexação: `57f32a3fb714260af420a8178a594f9012409133121657fed8dd354a3ddbb98e`.


---

## DEC-054 — Estudar MPPT compartilhado entre os arranjos fotovoltaicos fixos e portáteis

**Status: ALTERNATIVA B DE ESTUDO APROVADA PELO USUÁRIO EM 29/10/2026; TOPOLOGIA, MODELO E INTEGRAÇÃO AINDA NÃO VALIDADOS.** Deliberação literal: “Decisão 54: estudar controlador MPPT compartilhado entre arranjos fixos e portáteis, condicionado à comprovação de compatibilidade elétrica, eficiência e segurança. Registre a decisão 54, preserve integralmente as decisões 1 a 53, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Escopo e condicionantes
1. **Diretriz escolhida:** estudar a viabilidade técnica de um **controlador MPPT compartilhado** entre os dois conjuntos FV, como hipótese de arquitetura a avaliar, e **não** declarar essa ligação aprovada nem escolher componentes sem evidências. A configuração com controladores separados permanece uma referência de verificação técnica, mas não foi a alternativa aprovada para desenvolvimento prioritário nesta deliberação.
2. **Arranjos distintos:** manter como referências **1.540 Wp fixos no teto**, condicionados à validação dimensional da DEC-003/031, e **1.600 Wp portáteis exclusivamente durante estacionamento**, com inclinação e orientação fixadas para cada parada conforme DEC-045. Verificar corrente/tensão de circuito aberto nos extremos de temperatura, Vmp/Imp, topologia de strings, número de módulos e conectores.
3. **Operação com duas condições solares:** os conjuntos podem ter incidência, inclinação, temperatura e sombreamento diferentes. Uma entrada MPPT única pode operar fora do ponto de máxima potência de um ou ambos os conjuntos ou ser incompatível com a associação elétrica. **Não conectar strings heterogêneas em paralelo/série sem verificar curvas I–V, faixas do equipamento, proteções e perda de geração.** Se necessário, avaliar controlador com rastreadores MPPT múltiplos em um mesmo equipamento e distinguir isso de um MPPT único compartilhado.
4. **Conexão e desconexão dos portáteis:** dimensionar seccionamento, polaridade, arcos DC, conectores apropriados e procedimento seguro de montagem/desmontagem durante paradas; proteger contra retroalimentação, sobretensão e sobrecorrente. Avaliar funcionamento do sistema com apenas os painéis fixos em movimento e com ambos os conjuntos estacionado.
5. **Bancos de bateria independentes (DEC-020):** **um MPPT compartilhado na entrada FV não autoriza ligar sua saída simultaneamente aos bancos de serviços 48 V e de tração HV.** Qualquer distribuição entre circuitos independentes deve ser demonstrada por uma topologia de conversão/distribuição e comutação comprovadamente segura (DEC-021), sem ligação cruzada de bancos nem dupla contagem de energia. A decisão não aprova nenhum conversor ou interface de carga HV.
6. **Recarga DC da tração ainda pendente:** a alternativa B da DEC-001 é a direção escolhida, mas requer interface externa OEM autorizada, comunicação, isolamento e potência mínima. O MPPT compartilhado, isoladamente, **não comprova recarga DC funcional**; manter a comparação direta versus buffer da DEC-042, sem aprovação automática de banco extra.
7. **Comparação quantitativa e critérios de descarte:** P2/P5 devem levantar modelos comerciais documentados, eficiência e limites de tensão/corrente, estimar geração útil sob operação diária realista e perdas por mismatch, custo, massa, disponibilidade e segurança. Se o MPPT compartilhado não for compatível ou apresentar perda relevante, **registrar não conformidade e retornar para deliberação**, sem forçar a configuração.
8. **Rastreabilidade:** distinguir potência nominal Wp, energia gerada FV, energia útil após MPPT e energia efetivamente entregue a cada circuito. Usar dados e hipóteses versionados da DEC-035 e resultados idealizado versus realista da DEC-038.

### Responsáveis e entregáveis
- **P2 (líder):** diagrama funcional de arranjos, estudo de MPPT compartilhado/entrada múltipla, fichas técnicas, limites elétricos, proteções, comutação, compatibilidade e matriz de riscos.
- **P5:** curvas de geração hora a hora e perdas por mismatch dos arranjos orientados de forma distinta, incluindo os portáteis somente nas paradas; balanço sem dupla contagem.
- **P3/P1:** integração dos módulos, cabos e equipamentos ao CAD, massa, volumes, fixações e orçamento.
- **Resultado exigido:** parecer **viável / condicionado / não demonstrado / inviável** para a topologia compartilhada e alternativas documentadas, com solicitação de nova decisão quando necessário.

### Histórico e pendências preservados
As decisões **DEC-001 a DEC-053 permanecem integralmente preservadas**. Em especial, ficam inalteradas: DEC-001 (direção B solar/DC para interface de carga HV OEM, não validada), DEC-003/031 (meta do teto sujeita ao CAD), DEC-020 (bancos independentes), DEC-021 (alocação FV ainda pendente), DEC-029 (viabilidade energética condicional distinta da técnica), DEC-042 (direta versus buffer dedicado ainda em comparação), DEC-045 (portáteis só estacionado, sem reposicionamento dentro de uma parada), DEC-052 (rede AC de serviços 220 V/60 Hz) e DEC-053 (comparação de inversores, sem vencedor).

### Próxima pergunta a deliberar (DEC-055)
Definir a **localização e modalidade de instalação do ar-condicionado do habitáculo** com base na ocupação do teto e no layout: (A) priorizar equipamento compacto instalado sob banco/armário, condicionado à capacidade de refrigeração, dutos e espaço; (B) priorizar equipamento de teto, condicionando-o à compatibilidade com os painéis e estrutura; (C) comparar layouts físico/energético de instalação sob banco e no teto, antes de selecionar localização e modelo. Manter a seleção de capacidade do DEC-010/028 e a meta FV DEC-031 ainda pendentes; estudar as cargas elétricas compatíveis com DEC-052/053.

### Verificação de integridade
A DEC-054 foi acrescentada por anexação ao final do arquivo, sem editar os bytes das decisões DEC-001 a DEC-053. SHA-256 antes da anexação: `b82fcb2b1fd13be02b90b4f489837a659219a25427db10cd206d7c577b4b6748`.


---

## DEC-055 — Priorizar instalação de ar-condicionado compacto sob banco ou armário

**Status: DIRETRIZ DE LOCALIZAÇÃO APROVADA EM 29/10/2026; MODELO, CAPACIDADE E INSTALAÇÃO NÃO VALIDADOS.** Deliberação do usuário: “Decisão 55: priorizar ar-condicionado compacto instalado sob banco ou armário, preservando o teto para painéis solares, sujeito à validação de capacidade, dutos, ventilação, consumo, dimensões e massa. Registre a decisão 55, preserve integralmente as decisões 1 a 54, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretrizes aprovadas
1. **Localização prioritária:** buscar equipamento de climatização comercial compacto para instalação **sob banco ou dentro de armário técnico**, para evitar a ocupação do teto e preservar a meta de **1.540 Wp fotovoltaicos fixos** da DEC-003/031. Essa prioridade não equivale à comprovação de que o equipamento cabe ou refrigera adequadamente.
2. **Capacidade térmica ainda em comparação:** manter a **DEC-010** (FreshWell 3000 versus unidades mais potentes) e a **DEC-028** (caso obrigatório de 1 ocupante e cenário adicional de 2 pessoas) abertos. Validar potência frigorífica efetiva e carga térmica do habitáculo antes de selecionar modelo. Não confundir kW de refrigeração com consumo elétrico.
3. **Instalação e circulação de ar:** verificar nas fichas técnicas e no CAD entrada/descarga de ar dos circuitos do evaporador e condensador, dutos, grelhas, distâncias de manutenção, ruído, vibração, fixação, estanqueidade e drenagem do condensado. O circuito que rejeita calor deve ter trajetória funcional para o exterior quando o fabricante exigir; **não lançar calor do condensador dentro do volume habitável**.
4. **Espaço e massa:** confrontar dimensões reais do equipamento, dutos, folgas técnicas e acesso à manutenção com os dois estudos preliminares de layout DEC-030. Atualizar massa, centro de gravidade, fixações, custo e distribuição de carga por eixo (DEC-022/033/034).
5. **Energia e compatibilidade:** considerar consumo médio e picos de partida, eficiência e funcionamento sob **220 V/60 Hz** (DEC-052), inversor ainda não escolhido (DEC-053), autonomia dos serviços 24/48 h (DEC-005/039/046) e gerenciamento de cargas (DEC-019/047). Não assumir compatibilidade elétrica sem ficha técnica da versão exata.
6. **Se a instalação prioritária falhar:** caso não haja modelo comercial sob banco/armário que cumpra simultaneamente capacidade, volume, ventilação, segurança e consumo, documentar a restrição, estudar alternativas e solicitar nova decisão. **Não alterar automaticamente a meta solar do teto nem selecionar unidade de teto sem aprovação.**
7. **Ensaio térmico item 31:** preservar a condição obrigatória com o veículo fechado, sem ocupantes e sem ar-condicionado (DEC-027), distinta do estudo de conforto do item 32.

### Responsáveis e entregáveis
- **P6 (líder):** shortlist de climatizadores sob banco/armário, fichas técnicas, balanço térmico e requisitos de fluxo de ar/dutos/condensado, conforto e ruído.
- **P3:** envelopes de instalação no CAD, interferências, fixações e integração com os layouts, piso e teto.
- **P2/P5:** alimentação 48 V → inversor → 220 V/60 Hz, corrente de partida, eficiência, energia diária e impacto nas baterias e geração solar.
- **P1:** massa, centro de gravidade e custo; **P7:** auxílio térmico se necessário.
- **Critério de aceite:** modelo real documentalmente compatível, que caiba e possa ser instalado com segurança, com carga térmica, ventilação, potência elétrica, massa e custo verificáveis. Sem essa demonstração, status permanece **condicionado**.

### Comparações e decisões preservadas
As **DEC-001 a DEC-054** são mantidas integralmente por anexação; continuam em aberto, sem vencedores automáticos, as comparações sobre variantes OEM (DEC-036), ar-condicionado (DEC-010/028), arranjos FV (DEC-021/031/038/054), bateria e serviços (DEC-005/013/039), inversor (DEC-053), recarga DC da tração (DEC-001/029/042), layouts internos (DEC-030) e outras pendências históricas. A arquitetura B solar/DC autorizada apenas como direção de estudo continua sem viabilidade de recarga HV comprovada.

### Próxima pergunta a deliberar (DEC-056)
Definir a **estratégia de instrumentação e monitoramento energético, térmico e hídrico** para integração dos sete subprojetos: (A) medições e registros mínimos (SOC dos bancos, potências, temperaturas críticas e volumes), (B) monitoramento amplo integrado com telemetria/registro e alarmes, ou (C) monitoramento essencial com possibilidade de expansão conforme a viabilidade, preservando separação elétrica e limites do BMS. Não exigir integração indevida com CAN/BMS OEM nem apresentar dados simulados como telemetria real.

### Verificação de integridade
A DEC-055 foi acrescentada por anexação ao final do arquivo, sem modificar bytes anteriores da DEC-001 à DEC-054. SHA-256 do arquivo antes da anexação: `a4e7dba8413fd0205cb0c073404a311e7405b732bb8f9aea46823654c6a8d73f`.


---

## DEC-056 — Monitoramento básico por indicadores comerciais existentes

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; SELEÇÃO E DISPONIBILIDADE DOS INDICADORES AINDA SUJEITAS À DOCUMENTAÇÃO DOS FABRICANTES.** Deliberação: “Decisão 56: adotar monitoramento básico dos sistemas do motorhome, usando indicadores disponíveis nos equipamentos comerciais, sem desenvolver central própria de telemetria. Registre a decisão 56, preserve integralmente as decisões 1 a 55, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Escopo da decisão
1. **Monitoramento básico aprovado:** aproveitar visores, aplicativos locais, controladores e indicadores **já previstos pelos componentes comerciais selecionados** — como BMS/bateria auxiliar, inversor, MPPT e instrumentos integrados. Não desenvolver central própria de telemetria, gateway dedicado, rede de aquisição avançada nem dashboard central como requisito do projeto.
2. **Informações prioritárias, quando disponibilizadas pelo produto:** SOC e alarmes do banco auxiliar de 48 V; tensão/corrente/potência ou energia FV; estados e falhas do inversor; temperaturas relevantes disponíveis; nível dos reservatórios se os componentes comerciais selecionados possuírem indicação. Não exigir sensores ou medidores adicionais como decorrência automática desta decisão. Diferenciar dados **medidos, disponibilizados, estimados e não disponíveis**.
3. **Tração OEM:** dados do veículo somente pelos displays e interfaces documentadas/autorizadas. Não acessar indevidamente barramentos internos, modificar BMS, chicotes, CAN ou sistema HV original para obter telemetria (DEC-001/020/026/040).
4. **Autonomia e segurança:** monitoramento básico **não elimina** a necessidade de controle automático de cargas priorizadas da DEC-047, nem as proteções físicas e elétricas da DEC-039/040. Documentar quais funções de desligamento e alarmes realmente existem nos dispositivos comerciais e quais requerem hardware/integração adicional previamente aprovada; não afirmar que a automação está implementada sem comprovação.
5. **Validação acadêmica:** os modelos de energia, CFD, hidráulica e térmica continuam devendo entregar parâmetros, códigos, resultados e rastreabilidade sob DEC-035, mas **resultados de simulação não serão apresentados como telemetria do veículo real**. Não prometer validação experimental em hardware inexistente.
6. **Consumo e custos:** contabilizar o consumo próprio dos indicadores escolhidos quando material; incluir seus custos apenas se não vierem no equipamento-base. Não acrescentar indevidamente uma central, sensores redundantes ou outros custos que não foram aprovados (DEC-034/046).

### Responsáveis e entregáveis
- **P2 (líder):** tabela de indicadores disponíveis por componente, fontes/fichas técnicas, alarmes comerciais existentes e sua interface com o gerenciamento de cargas; separar requisitos atendidos e não atendidos.
- **P5:** distinguir dados/saídas do modelo simulado de eventuais medições; uso dos dados energéticos documentados.
- **P6/P7:** identificar se equipamentos térmicos e hidráulicos possuem indicadores próprios, sem pressupor sensores adicionais.
- **P3/P1:** tratar somente o espaço, massa e custo de indicadores realmente escolhidos, evitando novos projetos de hardware.
- **Critério de aceite:** lista reproduzível de parâmetros monitoráveis com hardware comercial, sua origem e status; lacunas explicitadas. **Nenhuma central própria de telemetria está aprovada.**

### Compatibilidade e pendências anteriores
**As DEC-001 a DEC-055 foram preservadas sem alterações por anexação.** Permanecem a arquitetura solar/DC B escolhida na DEC-001 (interface de recarga da tração não validada), os bancos independentes (DEC-020), as comparações de capacidades e reservas (DEC-005/013), modelos de equipamentos e inversores ainda não selecionados (DEC-010/053), estudo de MPPT compartilhado ainda condicionado (DEC-054), localização prioritária do A/C sob banco (DEC-055), bem como as demais comparações e pendências estabelecidas nas decisões anteriores.

### Próxima pergunta a deliberar (DEC-057)
Definir como alimentar **consumidores de baixa tensão DC** do sistema habitável (por exemplo iluminação LED, bomba d'água e eventuais comandos), sem usar indevidamente o circuito OEM do veículo: (A) padronizar barramento auxiliar em **12 V DC** alimentado por conversor 48→12 V, sujeito à escolha de produtos; (B) padronizar **24 V DC** alimentado por conversor 48→24 V, sujeito às tensões nominais dos equipamentos; (C) comparar 12 V e 24 V a partir de cargas e produtos comerciais, perdas, conversor, cabos e compatibilidade, antes de fixar a tensão DC de distribuição. Manter 220 V/60 Hz para as cargas AC (DEC-052), banco principal de serviços 48 V e independência da bateria de tração (DEC-020).

### Verificação de integridade
A DEC-056 foi acrescentada por anexação ao final do arquivo, sem alterar os bytes das decisões DEC-001 a DEC-055. SHA-256 antes da anexação: `3e3c7113146ce2e1b24c4fa6d4b0ae0a05cb1184223469b7994e2021fe4cc18a`.


---

## DEC-057 — Comparação de barramentos auxiliares de 12 V e 24 V DC a partir do banco de serviços de 48 V

**Status: COMPARAÇÃO APROVADA PELO USUÁRIO EM 29/10/2026; TENSÃO DO BARRAMENTO DC DE BAIXA TENSÃO NÃO SELECIONADA.** Deliberação literal: “Decisão 57: comparar barramentos auxiliares de distribuição de 12 V e 24 V DC alimentados pela bateria de serviços de 48 V, considerando equipamentos reais, correntes, perdas, conversores, proteções, cabos, massa e custo antes de escolher. Manter a rede AC 220 V/60 Hz e não utilizar indevidamente o sistema elétrico OEM do veículo. Registre a decisão 57, preserve integralmente as decisões 1 a 56, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretriz e escopo aprovados
1. **Comparação, não seleção:** estudar dois barramentos habitáveis candidatos, **12 V DC** versus **24 V DC**, alimentados por conversores comerciais **48→12 V** e **48→24 V**, respectivamente, a partir do banco independente de serviços LiFePO₄ nominal de 48 V (DEC-020/039). **Nenhuma tensão de distribuição DC secundária foi fixada como definitiva.**
2. **Inventário de cargas reais:** P6/P2 devem selecionar ou relacionar equipamentos que podem demandar DC de baixa tensão, como LEDs, bomba pressurizadora e possíveis controles/indicadores. Para cada um, documentar tensão e tolerância admitidas, potência nominal e de partida, corrente e disponibilidade comercial. Não pressupor que todas as cargas aprovadas são DC: geladeira AC e cooktop AC, e demais equipamentos AC confirmados, permanecem na rede do inversor.
3. **Dimensionamento elétrico comparável:** para as mesmas cargas e comprimentos de cabos, calcular correntes, quedas de tensão, perdas Joule, seções comerciais, isolação, proteções contra curtos/sobrecorrentes, seccionamento e custo total. Avaliar efeito da tensão na seleção de dispositivos, sem confundir 48 V nominal com tensão constante em toda a faixa de SOC.
4. **Conversores DC/DC documentados:** comparar modelos comerciais reais com entrada compatível com a **faixa de tensão do banco LiFePO₄**, saída regulada apropriada, potência contínua/picos, rendimento em regime de carga real, perdas em vazio, dissipação térmica, proteção e instalação. Não assumir conexão direta de equipamentos 12/24 V ao banco de 48 V; não improvisar tap de módulos/células de série.
5. **Impactos sistêmicos:** incorporar massa, volume, ventilação/temperatura, perdas no balanço médio de serviços (DEC-046), custo total (DEC-034) e layout/CAD (DEC-030). Verificar carga simultânea de equipamentos essenciais no contexto da gestão automática da DEC-047, sem exigir um novo perfil horário detalhado.
6. **Rede AC preservada:** cargas AC utilizam a rede de **220 V / 60 Hz** aprovada na DEC-052 e o inversor a definir pela DEC-053. Esta comparação não altera a padronização AC e não transforma o conversor DC/DC habitável em interface de carga do veículo.
7. **Separação OEM e alta tensão:** **não utilizar indevidamente nem modificar** a rede OEM de 12/24 V do veículo, o BMS de tração, chicotes ou circuito HV. A bateria de serviços permanece independente da tração (DEC-020). A arquitetura B da DEC-001 para recarga solar DC autorizada da tração continua como diretriz, mas sua interface não está comprovada; tampouco a comparação de conversores auxiliares valida essa recarga.
8. **Resultado e decisão futura:** apresentar matriz 12 V versus 24 V com lista de equipamentos compatíveis, quedas de tensão, eficiência/perdas, proteções, comprimentos e seções de cabos, massa, volume e custo, com fontes, hipóteses e lacunas. Recomendar uma alternativa somente com evidências; **a escolha final exige nova deliberação**, não substituição automática de componentes já aprovados.

### Responsáveis e entregáveis
- **P2 (líder):** diagramas unifilares comparativos, inventário de conversores e proteções, dimensionamento de correntes, perdas e cabos para 12 V e 24 V, fichas técnicas e recomendação condicionada; integrar ao projeto elétrico da DEC-040 e à análise térmica da DEC-026 quando aplicável.
- **P6:** relação de cargas DC habitáveis documentadas, potência e simultaneidade essencial, especialmente iluminação e bomba definida no projeto hidráulico da DEC-048.
- **P5:** perdas de conversão no balanço energético da bateria de serviços, sem contaminar consumo de tração.
- **P1/P3:** massa, custo, volume, acesso e posicionamento dos conversores, cabos e dispositivos nos layouts do CAD.

### Comparações e pendências mantidas
As **DEC-001 a DEC-056 permanecem integralmente preservadas**. Em particular, a alternativa B solar/DC da DEC-001 foi escolhida somente como direção de estudo e continua sem interface OEM comprovada; as baterias permanecem independentes (DEC-020); os cenários de autonomia 24/48 h da DEC-005, reservas da DEC-013, inversor da DEC-053 e MPPT compartilhado da DEC-054 ainda requerem validação/escolha conforme seus próprios critérios. A DEC-057 não aprova compra nem instalação de conversor ou circuito DC novo.

### Próxima pergunta a deliberar (DEC-058)
Definir os **pneus e a resistência ao rolamento** usados no modelo de consumo e desempenho, sem fixar uma dimensão incompatível com a variante OEM ainda aberta (DEC-036): (A) priorizar pneus e medidas homologadas/documentadas da variante OEM com coeficiente de rolamento estimado e sensibilidade; (B) estudar pneus comerciais de baixa resistência ao rolamento, apenas se forem compatíveis com capacidade de carga, velocidade, medidas e requisitos da variante; (C) comparar pneus homologados de referência com alternativa de baixa resistência ao rolamento fisicamente compatível, considerando consumo a 40/80 km/h, frenagem, massa, custo e segurança. A escolha final depende de dados do modelo exato e de conformidade com cargas por eixo (DEC-022).

### Verificação de integridade
A DEC-057 foi adicionada por anexação ao final do arquivo, sem modificar os bytes das decisões DEC-001 a DEC-056. SHA-256 do arquivo antes da anexação: `cefc7a513b4a9bb1825367c20f054aa82ab06be962434d8724d7f64df03551fd`.


---

## DEC-058 — Pneus homologados da variante OEM e resistência ao rolamento rastreável

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; DIMENSÕES, MODELO EXATO E COEFICIENTE DE ROLAMENTO PENDENTES DA SELEÇÃO DA VARIANTE.** Deliberação literal: “Decisão 58: manter como referência os pneus homologados da variante escolhida do Fiat E-Ducato, utilizando resistência ao rolamento documentada ou estimada com incerteza explícita, sem alterar as especificações originais. Registre a decisão 58, preserve integralmente as decisões 1 a 57, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretriz aprovada e limites
1. **Referência obrigatória:** utilizar as medidas, índices de carga e velocidade, características e especificações de pneus **homologados/documentados para a variante exata do Fiat E-Ducato elétrico L3H2** que venha a ser selecionada na DEC-036. Não escolher prematuramente aro, medida, marca, tipo de pneu ou pressão de inflação de outra versão/mercado; não misturar fichas técnicas de variantes distintas.
2. **Sem modificação de especificações OEM:** preservar a configuração homologada de rodas/pneus como referência do projeto. **Não foi aprovada** troca por modelos alternativos de baixa resistência ao rolamento; estudos opcionais de sensibilidade de Crr são permitidos e não equivalem a recomendar pneus não homologados.
3. **Coeficiente de resistência ao rolamento (Crr):** buscar primeiro dados técnicos rastreáveis para pneus, carga, pressão, temperatura, velocidade e piso compatíveis com o caso de estudo. Quando Crr específico não estiver disponível, utilizar hipótese de engenharia identificada como **estimativa**, com justificativa, intervalo de incerteza e análise de sensibilidade. Não apresentar um Crr genérico como ensaio ou especificação OEM.
4. **Modelo físico:** incorporar F_rol ≈ Crr·m·g em pista plana, e P_rol ≈ F_rol·v, explicitando que aproximações dependem de condições de utilização. Avaliar efeitos sobre kWh/km e km/kWh a **40 e 80 km/h**, consumo da missão em percurso plano da DEC-043, autonomia solar condicional, potência solicitada e desempenho longitudinal das DEC-032/037. Não misturar energia de tração com serviços (DEC-020/032).
5. **Massas e segurança:** calcular ou conferir condições de carga **típica e máxima fisicamente admissível**, limites de carga por eixo, índices de carga, pressões recomendadas pela fabricante da variante e compatibilidade com distribuição de massa e sistema de frenagem (DEC-022/025/033). Não declarar conformidade sem ficha técnica e cálculo compatível.
6. **Condições de referência:** documentar tipo de pavimento e temperatura e distinguir a resistência ao rolamento de efeitos de aclive, vento e outras resistências. O cenário principal da viagem de **7.000 km é plano e a velocidade é constante** (DEC-043), sem representar toda a topografia real. Manter análise de incerteza quando dados não estiverem disponíveis.
7. **Saída requerida:** tabela de medida/índices homologados da variante, fontes e versão documental, hipótese Crr com unidade adimensional e intervalo, verificações de carga por eixo, e resultados de sensibilidade do consumo/autonomia a 40 e 80 km/h. Valor final somente após escolher a variante e confirmar os dados do fabricante.

### Responsáveis
- **P4 (líder):** implementar Crr no modelo longitudinal, justificar hipóteses e propagar incerteza nos resultados de consumo/desempenho.
- **P1:** conferir peso por eixo, pneus homologados, índices de carga e requisitos de segurança na conversão.
- **P5:** utilizar resultados coerentes no modelo de autonomia e na viagem solar.
- **P3:** manter CAD coerente com geometria/rodas da variante sem alterações não aprovadas.

### Compatibilidade e pendências mantidas
As **DEC-001 a DEC-057 foram integralmente preservadas**. A escolha da variante do veículo permanece aberta na DEC-036, assim como outras comparações e condicionantes já registrados. Em especial, a arquitetura solar/DC B da DEC-001 é uma diretriz escolhida sem interface de recarga HV comprovada; as decisões sobre gerenciamento de energia, bateria auxiliar e MPPT mantêm seus próprios critérios de validação. A DEC-058 não seleciona automaticamente pneu, Crr ou variante OEM nem muda a hipótese de percurso plano da DEC-043.

### Próxima pergunta a deliberar (DEC-059)
Definir **como verificar suspensão, distribuição de cargas e estabilidade após a conversão**, complementando o PBT e os eixos (DEC-022), as fixações (DEC-033) e os pneus homologados (DEC-058): (A) manter a suspensão OEM, verificar documentalmente limites de carga por eixo, curso, altura e distribuição de massa sem presumir alterações; (B) projetar reforços/alterações de suspensão com avaliação estrutural, dinâmica e de homologação; (C) manter OEM como caso principal e comparar, apenas como estudo, necessidade de adequações quando exceder requisitos, sem aprovar modificação sem evidência. Uma modificação não é autorização para exceder o PBT homologado.

### Verificação de integridade
A DEC-058 foi acrescentada **por anexação** ao final do arquivo, sem modificar os bytes das decisões DEC-001 a DEC-057. SHA-256 do arquivo antes da anexação: `47dafbe4fd9808ad3f592a1dfac6a888ef463a1364e12c11ff4cc2a49c466510`.


---

## DEC-059 — Preservar suspensão OEM e verificar limites com massas típica e máxima

**Status: ALTERNATIVA A APROVADA PELO USUÁRIO EM 29/10/2026; VERIFICAÇÕES DIMENSIONAIS/ESTRUTURAIS E VARIANTE OEM AINDA PENDENTES.** Deliberação literal: “Decisão 59: manter a suspensão original homologada do Fiat E-Ducato e verificar cargas por eixo, centro de gravidade, curso e limites estruturais para as massas típica e máxima, sem modificações na suspensão. Registre a decisão 59, preserve integralmente as decisões 1 a 58, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretriz aprovada e escopo de verificação
1. **Suspensão de fábrica preservada:** manter a suspensão OEM homologada **da variante exata que vier a ser escolhida na DEC-036**, sem reforçar molas, substituir amortecedores, modificar geometria, curso, pontos de fixação ou elevar limites originais por suposição. A comparação entre mercados/modelos não autoriza combinação de especificações incompatíveis.
2. **Massas de referência:** avaliar os dois casos de carregamento da **DEC-022**, operacional típico e máximo fisicamente admissível. Somar corretamente veículo-base, painéis fixos/portáteis e suportes, bateria auxiliar e eventuais componentes de recarga DC, equipamentos habitáveis, ocupantes (2 × 80 kg), bagagem e distribuição real dos volumes de água; **não duplicar a massa da água que migra do reservatório limpo para cinzas/cassete**.
3. **Distribuição de massas por eixo:** calcular centro de gravidade longitudinal, lateral e vertical a partir do CAD, posições dos equipamentos e dados documentados. Calcular as cargas estáticas dianteira e traseira nas duas condições; conferir PBT, carga útil e **limites de cada eixo e pneu**, sem assumir que estar abaixo do PBT comprova adequação por eixo. Considerar carga mínima/máxima de reservatórios e as posições alternativas dos layouts da DEC-030.
4. **Curso e altura de operação:** verificar, conforme dados OEM disponíveis, altura livre, curso/compressão de suspensão, interferências com reservatórios, baterias e fixações, e possíveis variações de altura quando carregado. Quando curvas de mola, rigidez, bump-stop, amortecimento e curso não forem publicadas, **não inventar valores OEM**; documentar hipóteses e limites do que pode ser comprovado numericamente.
5. **Limites estruturais e operacionais:** confrontar massas e pontos de apoio dos equipamentos com restrições de carroceria/chassi e ancoragens da DEC-033, além da especificação de pneus da DEC-058. Avaliar qualitativamente os efeitos do centro de gravidade e da altura adicionada na estabilidade, mas **não declarar aprovação dinâmica, segurança em manobras nem homologação apenas pelos cálculos estáticos**.
6. **Se houver incompatibilidade:** apresentar de modo rastreável o eixo, massa, curso, componente ou condição que excede o limite e propor **redistribuição, redução de carga ou alteração de layout** para nova avaliação. Não alterar a suspensão, PBT, limites por eixo ou outros itens já aprovados automaticamente; solicitar decisão posterior se a configuração não for viável.
7. **Entregáveis:** tabela da variante OEM (PBT, tara, eixos e, se disponível, dados de suspensão), tabela de massas e coordenadas, CG em configurações típica/máxima, reações por eixo, margens até limites e pendências de documentação, com origem dos dados, unidades e incertezas. Integrar aos modelos de consumo (DEC-032), desempenho (DEC-037), frenagem (DEC-025), CAD/layout (DEC-030) e orçamento (DEC-034).

### Responsáveis
- **P1 (líder):** inventário de massas, centro de gravidade, reações por eixo e verificações contra PBT/limites OEM; registrar margens e incompatibilidades.
- **P3:** coordenadas de componentes no CAD, envelopes de instalação, interferências e apoio ao cálculo de centro de gravidade.
- **P4:** propagar os casos de massa aprovados para dinâmica, frenagem, consumo e desempenho; não simular alterações de suspensão como aprovadas.
- **P2/P5/P6/P7:** fornecer massa, dimensões e localização de seus equipamentos, identificando estimativas e fontes.
- **Critério de aceite:** somente considerar o conjunto compatível com a suspensão OEM quando documentação e cálculos nas condições crítica e típica sustentarem PBT, limites por eixo/pneus e instalação física. Não afirmar homologação ou ensaio realizado.

### Decisões anteriores e comparações preservadas
As **DEC-001 a DEC-058 permanecem integralmente preservadas**. A arquitetura B solar/DC da DEC-001 continua apenas como diretriz condicionada à interface externa HV autorizada; não existe comprovação da recarga da tração. A variante OEM definitiva depende da DEC-036; a capacidade da bateria auxiliar e reservas, equipamentos de conforto, MPPT e inversor mantêm comparações próprias em aberto. Esta decisão não modifica pneus OEM (DEC-058), suspensão OEM, baterias independentes (DEC-020) ou demais escolhas anteriores.

### Próxima pergunta a deliberar (DEC-060)
Definir **como avaliar a estabilidade lateral e o risco de tombamento** após a conversão, uma vez que a DEC-059 exige CG e cargas por eixo: (A) análise quase-estática simplificada, com altura do CG, bitola documentada, limiar geométrico e hipóteses; (B) simulação dinâmica detalhada de manobras/curvas baseada em modelo veicular parametrizado e dados OEM; (C) análise quase-estática como principal mais sensibilidade para distribuições de massa e eventual avaliação dinâmica complementar quando existirem dados confiáveis. Distinguir margens calculadas de comportamento experimental/homologado; não presumir estabilidade real com base apenas no índice geométrico.

### Verificação de integridade
DEC-059 adicionada **por anexação** ao final do registro, sem modificar os bytes das decisões DEC-001 a DEC-058. SHA-256 antes da anexação: `382c4640620f8346b6973a3ce7b7e09e186838bdb9aeeab76900d1c1cc8e39c0`.


---

## DEC-060 — Estabilidade lateral quase-estática e sensibilidade do centro de gravidade

**Status: ALTERNATIVA C APROVADA PELO USUÁRIO EM 30/10/2026; RESULTADOS, DADOS OEM E EVENTUAL SIMULAÇÃO DINÂMICA PENDENTES.** Deliberação literal: “Decisão 60: avaliar a estabilidade lateral por modelo quase-estático nas condições de massa típica e máxima, com análise de sensibilidade da altura e posição do centro de gravidade e bitola documentada. Executar simulação dinâmica complementar somente se houver dados confiáveis, sem declarar segurança ou homologação a partir do índice geométrico. Registre a decisão 60, preserve integralmente as decisões 1 a 59, incluindo todas as comparações pendentes, e faça a próxima pergunta das pendências do motorhome.”

### Diretriz aprovada e metodologia
1. **Cenários obrigatórios:** avaliar a configuração de massa operacional típica e a configuração de massa máxima fisicamente admissível da DEC-022, usando a mesma variante OEM validada na DEC-036 e a suspensão original sem modificações da DEC-059.
2. **Centro de gravidade (CG):** calcular posição longitudinal, transversal e altura do CG com dados de massa e coordenadas do CAD. Incluir ocupantes, água, bagagem, bateria auxiliar, estruturas, painéis, equipamentos e suas posições reais. Não duplicar massa de água que passa entre reservatórios; verificar também estados relevantes de enchimento.
3. **Bitola documentada:** utilizar bitolas e outras dimensões da variante exata do E-Ducato; distinguir bitola dianteira e traseira, caso necessário. Dados não publicados devem ser apresentados como estimativas e não como informações OEM verificadas.
4. **Modelo quase-estático:** calcular indicador geométrico de estabilidade lateral e estimativa de transferência de carga usando hipóteses explícitas, por exemplo a_y/g ≈ t/(2 h_CG), somente dentro das limitações do modelo e para o eixo/geometria pertinentes. Não usar esse índice isoladamente como limite real de tombamento, velocidade segura de curva ou prova de homologação.
5. **Sensibilidade:** variar, com intervalos justificados, a altura e a posição transversal do CG, o nível dos reservatórios e a massa/carregamento. Comparar casos típico e máximo, além de situações de assimetria de carga que sejam relevantes. Mostrar margens e tendências e, quando aplicável, incertezas em gráficos/tabelas.
6. **Condição para modelo dinâmico complementar:** executar simulação de curva/manobra transiente apenas se estiverem disponíveis parâmetros confiáveis de pneus, suspensão, amortecimento, geometria e características da variante. Sem esses dados, declarar a impossibilidade de uma validação dinâmica rigorosa em vez de inventar curvas OEM.
7. **Segurança e escopo:** não inferir certificação, homologação, conformidade experimental nem aprovação de manobra apenas a partir de cálculo quase-estático. Não aprovar modificações na suspensão nem ultrapassar PBT, limites de eixo ou pneus. Se houver incompatibilidade, documentar redistribuição ou redução de massa a ser submetida a nova decisão.
8. **Integração:** utilizar massas, centro de gravidade e cargas por eixo comuns à DEC-022/059, pneus OEM da DEC-058, fixações da DEC-033, layout/CAD da DEC-030 e dinâmica da DEC-037, sem introduzir dados incompatíveis entre as áreas.

### Responsáveis e entregáveis
- **P1 (líder):** consolidar massas e posições, CG nos dois casos, verificação estática de reações por eixo e índice quase-estático, faixa de incerteza e conclusões com limitações.
- **P3:** gerar posições e envelopes no CAD, estudar impacto de redistribuição de equipamentos e fornecer geometria/bitolas documentadas.
- **P4:** avaliar coerência física do índice e decidir se há parâmetros suficientes para simulação dinâmica complementar, sem presumir resposta dinâmica real.
- **P2/P5/P6/P7:** fornecer massas, alturas e posições dos subsistemas, identificando lacunas de documentação.
- **Saída:** tabelas de CG e cargas, fontes OEM, intervalos dos parâmetros, análise de sensibilidade e registro explícito do que está calculado, estimado, não validado ou inviável.

### Comparações e pendências preservadas
As **DEC-001 a DEC-059 foram preservadas integralmente**. Continuam abertas todas as comparações não resolvidas, como a escolha da variante exata do E-Ducato (DEC-036), a interface externa autorizada para recarga solar DC da tração (DEC-001/029/042), a capacidade da bateria auxiliar (DEC-005/039), o layout (DEC-030), os equipamentos, MPPT e inversor (DEC-010/053/054), e as demais validações condicionais. A DEC-060 não modifica decisões já aprovadas, não representa certificação e não fixa uma velocidade segura para curvas.

### Próximo encaminhamento sugerido
Com 60 decisões, o documento já é suficiente para conduzir a fase de execução dos 35 itens do enunciado. Em vez de abrir indefinidamente novas decisões, recomenda-se uma **deliberação de encerramento do levantamento de requisitos**: (A) congelar agora o conjunto DEC-001–060 e emitir matriz de pendências técnicas por responsável; (B) fazer no máximo três a cinco perguntas finais estritamente bloqueantes e então congelar o baseline. As verificações que dependem de pesquisa, cálculos e documentação devem se tornar tarefas do Codex e dos responsáveis, não novas perguntas genéricas ao usuário.

### Verificação de integridade
DEC-060 adicionada por anexação ao fim do arquivo, sem modificar os bytes anteriores DEC-001 a DEC-059. SHA-256 antes da anexação: `5ec788607590a98448d7ad0dc45791acb5e9935ae9db3de1be2f7334036232a3`.


---

## DEC-061 — Autonomia técnica provisória do Codex com aprovação final consolidada

**Status: ALTERNATIVA C APROVADA PELO USUÁRIO EM 30/10/2026.** Deliberação literal: “Decisão 61: permitir que o Codex selecione provisoriamente componentes e configurações pendentes com base em evidências, integre os resultados e apresente uma única lista consolidada de aprovações finais. Preservar todas as decisões já tomadas e não considerar validadas interfaces ou soluções sem comprovação técnica. Registre a decisão 61 preservando as decisões 1 a 60. Faça a pergunta final 2 de no máximo 5, somente se estritamente necessária para concluir o planejamento do motorhome.”

### Regra de autonomia e aprovação
1. **Escolha técnica provisória autorizada:** os agentes do Codex e os responsáveis P1–P7 podem pesquisar, classificar e selecionar provisoriamente componentes comerciais e configurações que ainda estavam pendentes de comparação, usando dados documentados, critérios transparentes e análises de sensibilidade, sem exigir nova pergunta para cada componente. A seleção provisória é uma hipótese integrada de trabalho, **não uma aprovação definitiva do usuário**.
2. **Fonte única de parâmetros:** registrar cada opção selecionada e seus dados (marca/modelo/versão, mercado, referência/fonte, características, unidades, custos, massa, dimensões, eficiência, incerteza, responsável, data e versão) na fonte única de parâmetros da DEC-035, com rastreabilidade entre simulações e entregáveis. Marcar substituições e consequências para P1–P7.
3. **Respeito às DEC-001 a DEC-060:** nenhuma deliberação já aprovada será alterada automaticamente. As comparações em aberto continuam comparações, mas o Codex poderá recomendar sua opção preferida de forma provisória e documentada, sem apresentar a recomendação como escolha definitivamente aprovada. Em caso de conflito, não sobrescrever a decisão anterior: apontar conflito e solicitar deliberação explícita.
4. **Lista única de aprovações finais:** após os estudos e a integração, apresentar ao usuário um pacote consolidado com alternativas comparadas, recomendações, critérios, impactos em massa/custo/autonomia/CAD/segurança, fontes, incertezas e itens dependentes uns dos outros. Separar **“aprovado anteriormente”**, **“selecionado provisoriamente / aguardando aprovação final”**, **“não demonstrado”**, **“inviável”** e **“bloqueante”**.
5. **Limites técnicos e de segurança:** nenhum agente pode declarar validada, homologada, certificada ou implementada uma interface que não tenha evidência técnica suficiente. A arquitetura B solar/DC da DEC-001 continua sendo a direção escolhida, mas a compatibilidade com carregamento HV via interface OEM autorizada **segue pendente**, conforme DEC-029 e DEC-042. Não conectar diretamente o pack HV, não alterar a instalação OEM, não usar o banco de 48 V para tração e não declarar a viagem solar de 7.000 km fisicamente realizável sem comprovação.
6. **Bloqueios e impossibilidades:** quando faltarem dados do fabricante, usar estimativas identificadas apenas para estudo condicional e análise de sensibilidade; nunca inventar dados OEM. Quando uma escolha violar segurança, capacidade, compatibilidade ou decisões anteriores, registrar o bloqueio, os efeitos nas simulações e eventual necessidade de aprovação humana de mudança de escopo. Não substituí-la silenciosamente.
7. **Integridade e auditabilidade:** manter os 35 itens do enunciado vinculados a responsáveis e resultados reproduzíveis; registrar qual cenário e versão de parâmetros alimentam cada saída. Respeitar massa, PBT, cargas por eixo, 220 V/60 Hz dos serviços, arquitetura 48 V LiFePO4 provisória, painéis e prioridades de uso definidas nas decisões anteriores.

### Consequência para o encerramento do planejamento
Esta decisão **elimina a necessidade de uma nova pergunta para cada opção comercial ainda não selecionada**. As questões restantes são, em sua maioria, tarefas de pesquisa, dimensionamento, verificação e consolidação. Não formular novas perguntas genéricas: perguntar ao usuário apenas se restar uma deliberação estritamente necessária que não possa ser resolvida por aplicação das DEC-001 a DEC-061, pesquisa técnica ou escolha provisória documentada.

### Responsáveis e próximos entregáveis
- **Coordenação P1–P7 / Codex:** consolidar registro de parâmetros, matriz de decisões e pendências e lista única de aprovações finais com recomendação e evidência por item.
- **P2 + P5:** priorizar verificação e documentação da interface solar/DC de recarga da tração; não presumir sua viabilidade.
- **P1/P3/P4/P6/P7:** avançar com as seleções provisórias, integrar CAD, massa, dinâmica, consumo, conforto, térmico e orçamento sem alterar deliberações aprovadas.

### Integridade e pendências preservadas
As **DEC-001 a DEC-060 foram mantidas integralmente**. Permanecem as comparações técnicas e aprovações finais pendentes (variante E-Ducato, capacidade da bateria de serviços, MPPT, inversor, ar-condicionado, layout, modelos comerciais, arquitetura de recarga DC direta versus buffer, etc.). A autonomia provisória não equivale à aprovação definitiva das escolhas nem à validação física da missão.

### Verificação de integridade
DEC-061 adicionada por anexação, mantendo os bytes anteriores DEC-001 a DEC-060 inalterados. SHA-256 antes da anexação: `fc7862178a03e9989ba9ecdb2b5b84cc2c2579708ddbb40659b3767887fccac4`.
