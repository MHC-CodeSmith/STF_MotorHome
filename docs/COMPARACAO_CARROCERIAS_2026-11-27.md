# Comparação das três carrocerias — 27/11/2026

Solicitação: simular a geometria original baixada, a adaptação existente e uma
nova tentativa de aproximação da E-Ducato L3H2; executar cada uma com e sem
painéis. São seis casos independentes por nível de malha. O usuário autorizou
transferir a execução à Hipólito Precision e repetir os seis casos com malha
mais refinada após a primeira versão. Resultados novos só serão publicados
depois da execução e da leitura dos logs; nenhum Cd foi escolhido como alvo.

## Geometrias e o que foi corrigido

| Parâmetro | Original OpenX | Adaptação existente | Novo ajuste |
|---|---:|---:|---:|
| Comprimento CAD (m) | 5,000 | 5,998 | 5,998 |
| Altura CAD (m) | 2,245 | 2,612 | 2,612 |
| Entre-eixos (m) | 3,003 | 4,035 | 4,035 |
| Largura da carroceria sem espelhos (m) | aproximadamente 2,107 | aproximadamente 2,107 | 2,050 |
| Largura total com espelhos (m) | 2,508 | 2,508 | 2,690 |
| Balanço dianteiro (m) | aproximadamente 0,958 | aproximadamente 0,958 | 0,948 |
| Balanço traseiro (m) | aproximadamente 1,039 | aproximadamente 1,005 | 1,015 |
| Bitola dianteira/traseira (m) | 1,796/1,796 | 1,796/1,796 | 1,810/1,790 |
| Raio livre dos pneus (m) | 0,350 | 0,350 | 0,37211 |

As cotas vêm da [ficha Fiat SK MY25, p. 5](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf).
A altura de 2,612 m continua sendo o extremo superior da faixa 2,592–2,612 m.
O raio livre é uma hipótese de pneu já usada no projeto, não medida de pneu
carregado. A posição em X das regiões das caixas de roda é preservada por
translação, com o alongamento concentrado na carga; o novo ajuste não estica
as caixas de roda entre os centros dos eixos.

O novo modelo é um **ajuste dimensional aproximado**, não uma reconstrução das
superfícies de fábrica. O perfil superior lateral foi aproximado por pontos
digitalizados manualmente da ilustração da ficha MY25, normalizados pelo
comprimento e altura oficiais. As seções da carroceria original são mapeadas
verticalmente acima da linha de cintura; os pontos e o hash do PDF ficam em
config/perfil_educato_ilustracao_2026-11-27.json. Essa ilustração não é um desenho
de superfície cotado. Curvatura transversal do para-brisa, frente de 2014,
espelhos e assoalho ainda derivam do ativo visual. Os conjuntos dos espelhos
foram transladados lateralmente em aproximadamente 91 mm por lado para ajustar
a largura em rodagem de 2,690 m; isso ajusta o envelope, sem reconstruir a
geometria ou posição angular de fábrica. O perfil digitalizado é aproximado, sem homologação ou precisão de
escaneamento físico.

## Preparação da superfície

O CAD original é mantido em GLB sem alteração dimensional. Como a malha aberta
não define diretamente um volume sólido para CFD, uma cópia para o escoamento é
preparada por partes: carroceria rasterizada a 15 mm, preenchimento, suavização
local, redução de triângulos e reparo; pneus e espelhos tratados separadamente.
A inflação do raster é removida por correspondência de caixas envolventes por
peça. O resultado mantém quatro pneus, dimensões globais e superfícies fechadas.

Um ensaio de reparo direto anterior foi rejeitado: o filtro de área isolado
permitia perder aproximadamente 0,26 m da traseira. Esses ensaios não integram os
seis casos. O reparo antigo do relatório e a nova preparação não são idênticos;
a comparação atual usa a mesma nova preparação para as três carrocerias.

| Geometria | Área frontal CAD (m²) | Área frontal CFD (m²) | Mudança frontal |
|---|---:|---:|---:|
| Original | 4,258337 | 4,253908 | 0,1040% |
| Modificada existente | 5,004665 | 5,014946 | 0,2054% |
| Novo ajuste | 4,874490 | 4,864807 | 0,1986% |

As mudanças das projeções frontal, superior e lateral são menores que 0,35%.
Isso verifica preservação global, não erro local ou convergência geométrica.
Detalhes menores que o passo e frestas pequenas podem mudar. Uma sensibilidade
ao passo da preparação permanece necessária para quantificar essa parcela.

Artefatos em [entregas/comparacao_carrocerias_2026-11-27](../entregas/comparacao_carrocerias_2026-11-27/):
vistas na mesma escala, três GLBs, STLs para CFD, licença/atribuição, manifestos
e verificações geométricas. O ZIP reúne os CADs e as superfícies preparadas.

## Protocolo comum dos seis casos

OpenFOAM v2412, simpleFoam, RANS kOmegaSST; U = 22,222222 m/s (80 km/h),
rho = 1,1 kg/m³ e nu = 1,7e-5 m²/s mantidos como hipóteses comuns. Domínio:
X de −35 a +20 m, Y de −10 a +10 m, Z de 0 a 10 m. Solo móvel na velocidade do
ar e rodas estacionárias, com a mesma orientação nos seis casos.

Malha de fundo 55×20×10, refinamento superficial 5–6, esteira nível 3. São
solicitadas cinco camadas, espessura final de 30% da célula externa e expansão
1,2. A primeira espessura nominal é 14,47% da célula externa e a pilha inteira
tem mínimo de 10% dessa célula. Isso adapta as espessuras às frestas dos painéis.
A cobertura é gerada com displacementMotionSolver/displacementLaplacian,
nGrow=0, buffer=1, até 30 iterações e limite
de não ortogonalidade de 65° sem relaxamento para 75°. A configuração auxiliar
de cellDisplacement usa GAMG, mínimo de cinco iterações, tolerância 1e-8 e
relTol=0,01. Esses parâmetros valem nos dois níveis de malha. A cobertura
real e o y+ precisam ser lidos depois de gerar e resolver cada malha. Quantidade
solicitada não é cobertura obtida. A convecção de U passa de upwind para
linearUpwind grad(U), com gradiente limitado. Resíduos-alvo p=1e-5 e
U/k/omega=1e-6, máximo 2000 iterações. Capacidade de refinamento de 3 milhões de
células, com rejeição se o log indicar truncamento.

Os painéis são quatro caixas de 1,046×1,690×0,040 m, separadas por 20 mm,
com sua face inferior 40 mm acima do topo máximo da carroceria, centralizadas
em Y e com início 25 mm depois da traseira. As regiões de refinamento das
frestas são mantidas no par sem painéis. Essa montagem é uma hipótese comum
de comparação; na carroceria original curta e no novo perfil ajustado há avanço
da fileira sobre a região de transição à cabine/para-brisa. As vistas com
painéis mostram essa condição; não se declara encaixe físico confirmado.
Fixações, suportes e instalação real não estão definidos e não foram inventados.
A comparação é dos módulos; o antigo slab contínuo não é a mesma geometria.

Cada par com/sem painéis usa a mesma área de referência da carroceria sem
painéis. Entre carrocerias, as áreas diferem e são informadas. A comparação de
arrasto usa principalmente **CdA** e força, evitando concluir a partir de Cd
isolado quando a área mudou. São mantidos logs integrais e históricos das forças.

A execução foi transferida à Hipólito Precision por autorização explícita do
usuário em 27/11. A tentativa no Lenovo ficou sem memória na adição de camadas;
sua malha salva de 1.343.857 células passou no checkMesh. As malhas encaixadas
dos quatro primeiros casos foram preservadas e verificadas antes de refazer as
camadas; o par do novo ajuste parte da malha base. O coordenador inicial CPU
foi interrompido antes de soluções de produção. A preparação atual usa até
quatro malhas simultâneas, CPUQuota=400%, MemoryMax=40G, sem swap e Nice=15.
O usuário pediu em seguida execução com GPU: foi construída uma instalação isolada OGL v0.5.4
(69387eeffa02aa614085ced705ecd8a2f59ddd6c), Ginkgo no commit
fc86d48b78cebd2b2c5833a2dcf0fe40f615cf19 e CUDA 12.8 para arquitetura sm_86.
OGL permite descarregar os sistemas lineares no CUDA; isso não transfere o
snappyHexMesh à GPU. Foram necessários ajustes locais na comunicação MPI via
memória do host e no tratamento de escala de matrizes; os patches e licenças
ficam em software_patches na entrega. Os benchmarks usam escala padrão 1.
O ensaio de 40 iterações foi concluído nas duas GPUs: a diferença relativa
máxima de Cd nas dez iterações finais foi 0,2028%, dentro do limite de 0,5%.
Os processos simpleFoam foram observados nas duas placas pelo nvidia-smi.
O CPU MPI2 levou 337,22 s; GPU 0, 449,12 s; GPU 1, 453,29 s. Portanto, neste
ensaio em máquina compartilhada, CUDA foi aproximadamente 33–34% mais lento.
Isso demonstra execução e concordância limitada do backend, sem demonstrar
aceleração ou validar o Cd da van. Logs, configurações e históricos estão em
backend_benchmark na entrega. A produção usa as mesmas tolerâncias lineares
do ensaio: absoluta 1e-9, relativa 0,001, com escala 1. A fila GPU aguarda as
malhas verificadas; a preparação de malha continua no CPU.

Uma tentativa inicial com displacementMedialAxis foi rejeitada antes de
qualquer solução de produção: a malha original sem painéis ficou com 1.686.207
células, mas 1.173 volumes negativos e cinco verificações reprovadas. As oito
camadas solicitadas resultaram em média de 2,2 na carroceria; isso não foi
aceito como oito camadas realizadas. Logs e malha rejeitada ficam preservados
no cache, separados dos resultados. As malhas encaixadas anteriores passaram
no checkMesh e são usadas para reconstruir as camadas com o método acima.

Os dois benchmarks CPU usam a mesma cópia de malha encaixada válida, com 40
iterações, sem representar um Cd final. O backend CUDA deve completar as mesmas
40 iterações em cada GPU, com processo observado pelo nvidia-smi e diferença
máxima de Cd inferior a 0,5% nas dez iterações finais em relação ao CPU com dois
processos MPI. Essa verificação é de equivalência do backend; não valida a van.
Após a aprovação, cada GPU recebe um caso com dois processos MPI, e a geração
de malhas seguintes pode ocorrer em paralelo. O serviço da campanha permite
CPUQuota=600%, MemoryMax=48G, sem swap e Nice=15. A segunda fase começa depois
dos seis casos iniciais; os logs e tabelas são coletados automaticamente.

A segunda fase usa fundo 77×28×14: espaçamento 0,7143 m em vez de 1 m, mantendo
níveis e condições físicas. Portanto o espaçamento local cai 28,6%; em regiões
uniformemente refinadas são aproximadamente 2,74 vezes mais células por volume.
O limite de refinamento sobe a 10 milhões de células. Isso não prediz o total
final após adaptação e camadas. As mesmas cinco camadas relativas acompanham
o refinamento também na direção normal às paredes. Geometrias, painéis e
condições físicas são pareados. A comparação entre
as duas malhas mede sensibilidade; dois níveis não estabelecem por si só uma
extrapolação de Richardson ou independência de malha.

## Interpretação dos coeficientes

A relação é Fd = 0,5 rho U² Cd A. A possui unidade m² e Cd é adimensional.
CdA representa a área de arrasto e permite comparar forças sob rho/U iguais.
O incremento dos painéis é obtido subtraindo CdA no mesmo par, não aplicando a
razão antiga 0,622/0,555 como uma correção universal.

O coeficiente normaliza a força pela pressão dinâmica q = 0,5 rho U² e pela
área frontal projetada. Não basta a carroceria ter o comprimento e a altura
certos: inclinação e curvatura da frente, transição do teto, espelhos,
assoalho e separação da esteira também mudam a força. A adaptação existente
tem área frontal CFD de 5,014946 m²; o novo ajuste, 4,864807 m². Essa redução
de aproximadamente 2,99% da área já afeta a força para um mesmo Cd; o efeito
da mudança de forma sobre o próprio Cd exige a solução do escoamento.

O relatório numérico separa Cd de pressão e Cd viscoso. O primeiro integra a
pressão nas superfícies e inclui o efeito da esteira; o segundo integra as
tensões de atrito. A soma é o arrasto total, com parcela porosa nula nestes
casos. Cl normaliza a força vertical pela mesma qA e usa Z positivo para cima.
Coeficientes de momento dependem também do comprimento de referência e do
ponto escolhido: CofR=(0,0,0) é uma origem de cálculo, não um centro de
gravidade validado para avaliar estabilidade do veículo.

Com rho=1,1 kg/m³ e 80 km/h, q é aproximadamente 271,60 Pa. Logo, cada
0,1 m² de diferença em CdA corresponde a aproximadamente 27,16 N de arrasto
e 604 W de potência aerodinâmica nessa velocidade. Essa potência é Fd vezes U;
não inclui rolamento, transmissão ou auxiliares. Os números de exemplo são
conversões da equação, não resultados das simulações em andamento.

O comunicado [Fiat de 22/05/2006](https://www.media.stellantis.com/em-en/fiat-professional/press/new-fiat-ducato-2)
publica Cd=0,31 para a família Ducato daquela época, sem estabelecer neste estudo
a identidade da variante, área ou ensaio com a E-Ducato SK MY25 L3H2.
É contexto para investigar a diferença, não valor de substituição ou calibração.

Uma solução residual convergida, Cd estabilizado e checkMesh aprovado ainda não
demonstram independência de malha, adequação de parede, fidelidade da forma ou
validação física. Os seis casos são a primeira comparação controlada. A fonte
canônica de energia e o relatório publicado não recebem Cd novo antes da análise.

## Reprodução

No ambiente com os extras cad/cfdprep e NumPy 1.26.4:
1. scripts/obter_carroceria.py fixa a release e verifica o hash.
2. scripts/preparar_carroceria.py extrai o exterior sem reescala.
3. scripts/adaptar_educato.py reproduz a modificação existente.
4. scripts/ajustar_carroceria_cotas_oem.py gera o novo ajuste.
5. scripts/preparar_superficie_comparacao.py prepara cada superfície por partes.
6. scripts/preparar_comparacao_carrocerias.py --com-e-sem-paineis gera seis casos.
7. scripts/executar_comparacao_carrocerias.py executa e registra as ferramentas.
8. scripts/renderizar_comparacao_carrocerias.py gera as vistas comparativas.

Parâmetros e caminhos exatos ficam nos manifestos e nos casos da entrega.
As entradas anteriores à conversão do solver para CUDA ficam em entradas_cfd;
a coleta de cada fase preserva também os dicionários efetivamente executados.
Documentação de método: [camadas snappyHexMesh](https://doc.openfoam.com/2312/tools/pre-processing/mesh/generation/snappyhexmesh/layers/),
[encolhimento Laplaciano](https://doc.openfoam.com/2212/tools/pre-processing/mesh/generation/snappyhexmesh/layers/),
[linearUpwind](https://doc.openfoam.com/2312/tools/processing/numerics/schemes/divergence/rtm/linearUpwind/),
[forceCoeffs](https://doc.openfoam.com/2212/tools/post-processing/function-objects/forces/forceCoeffs/).

## Retomada da execução na Precision

Checkpoint em 27/11/2026, aproximadamente 11h55 BRT: benchmark CUDA aprovado
no escopo limitado acima; quatro malhas iniciais adicionando camadas, par do
ajuste OEM aguardando sua vez. Nenhuma solução de produção concluída nesse
checkpoint. O monitor atualiza estado_campanha.json na entrega a cada 30 s;
gpu_process_observations.jsonl registra somente processos simpleFoam desta
campanha encontrados nas GPUs. São arquivos de acompanhamento, não aceite
dos resultados. O coeficiente validado permanece null.

Worktree: /home/hipolito/stf-aero-review, branch fix/aero-geometry-review-20261127.
Cache de execução: /home/hipolito/stf-aero-cache. Casos iniciais em precision_v1;
refinados em precision_v2_refined. Os serviços de usuário sobrevivem ao fim da
conversa: stf-aero-relative-layers-v1-20261127 prepara as primeiras malhas;
stf-aero-gpu-campaign-20261127 aguarda verificação, resolve e coleta v1, depois
prepara, resolve e coleta v2; stf-aero-campaign-monitor-20261127 salva o estado.
Consultar com XDG_RUNTIME_DIR=/run/user/1000 systemctl --user status e journalctl.
Logs principais: relative-layers-v1.log e gpu-campaign.log no cache.

Não reiniciar cegamente serviços ou regenerar diretórios: os executores recusam
sobrescrever logs. Conferir resultado_malha.json, reuse_verified_mesh.json,
resultado_execucao.json e os logs por caso. Preservar qualquer nova falha em
diretório separado antes de corrigir/reexecutar. A malha de produção só é
liberada após checkMesh aprovado e hashes conferidos. O script de coordenação
usado está copiado em software_patches/run-gpu-campaign.sh; cada solução tem
limite de 24 h. A passagem à malha refinada não representa aceitação física
ou convergência iterativa automática da fase inicial.

## Correção após as primeiras soluções — 27/11, 18h BRT

As seis malhas iniciais terminaram e passaram no checkMesh. Entretanto, o
original sem painéis divergiu, chegando ao limite de 2000 iterações com força
absurda; o original com painéis divergiu e sofreu exceção de ponto flutuante
na iteração 1081. O modificado sem painéis foi interrompido durante a solução;
seu Cd momentâneo de aproximadamente 0,418 não foi aceito como convergido.
Esses logs e estados ficam em rejected_production_v1 na entrega; os campos
integrais permanecem no cache precision_v1. Nenhum desses números é um novo
coeficiente do projeto. O ensaio anterior de 40 iterações conferia somente
um trecho curto e não demonstrava estabilidade de soluções longas.

A recuperação preserva os hashes das malhas e todas as condições físicas.
Os novos casos, precision_v1_recovery, recebem inicialização potencial,
relaxação de pressão 0,2 e de U/k/omega 0,3, com gradiente padrão cellLimited
Gauss linear 1. Mantém-se a convecção linearUpwind de U. As referências de
método são [potentialFoam](https://doc.openfoam.com/2306/tools/processing/solvers/rtm/basic/potentialFoam/)
e [under relaxation](https://doc.openfoam.com/2212/tools/processing/numerics/solvers/under-relaxation/).
Isso é uma tentativa de estabilização numérica, sem selecionar Cd-alvo.
A inicialização potencial não substitui o modelo viscoso SST.

Um par CPU/CUDA usa a mesma malha original e os mesmos campos potencialmente
inicializados, em stability_diagnostic. A comparação longa deve preceder a
aceitação do backend recuperado. O caso GPU desse par é acessível também pelo
link precision_v1_recovery/01_original_a_sem_paineis, evitando descartar suas
iterações: não há segunda solução independente nesse link. O CPU tem limite
de 600 iterações; o GPU, 4000, sujeito à convergência ou guarda de divergência.
O original com painéis roda na GPU 1 com o mesmo protocolo recuperado.
Os coeficientes de ambos continuam provisórios até a verificação final.

O executor agora interrompe Cd não finito ou |Cd|>10 depois da inicialização
(iteração>100), como guarda ampla de falha. Isso não é limite físico universal,
critério de convergência ou alvo de calibração. Saída zero sem convergência
SIMPLE e sem estabilização de Cd é reprovada. FieldMinMax registra extremos
locais de U, p, k, omega e nut a cada 25 iterações para localizar instabilidades.

O serviço stf-aero-refined-meshes-20261127 prepara a malha fina no CPU em paralelo;
stf-aero-stability-diagnostic-20261127 executa a referência CPU e o original
GPU 0; stf-aero-recovery-original-panels-20261127 executa o par com painéis
na GPU 1. O coordenador stf-aero-recovery-campaign-20261127 aguarda os primeiros
casos recuperados e os compara com o CPU antes de liberar os demais quatro e,
por fim, os seis casos refinados recuperados. Script copiado na entrega em
software_patches/run-recovery-campaign.py. O monitor foi estendido para registrar
todos esses serviços e casos. Não reiniciar a campanha inicial antiga.
