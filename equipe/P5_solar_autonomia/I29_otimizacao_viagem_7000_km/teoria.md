# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Método e limites — item 29

Minimizar o tempo total para 7.000.000 m com bateria inicial e solar, sem recarga externa, até 28.800 s de condução por dia de calendário.

Fonte do requisito: enunciado 2026 p. 2, I29, conferido em extração local em 23/10/2026. A apostila cap. 1 contextualiza projeto e otimização, mas não fornece um solver desta agenda.

O [verificador temporal](../../../src/motorhome/agenda_energia.py) usa intervalos de potência/velocidade constantes, integra distância e energia e divide intervalos nas meias-noites locais. Energia da bateria recebe eta_carga vezes o saldo terminal positivo e fornece o saldo negativo dividido por eta_descarga. SOC é E/E_ref, com capacidade de referência explicitamente definida. Noites/paradas precisam constar da agenda.

O verificador detecta déficit antes do solar posterior, excedente de capacidade e excesso diário de condução. Corte solar é opcional e contabilizado; não há recarga externa no contrato. Fornecer alvo/tolerância de SOC e distância/limite diário com os valores do enunciado: a API genérica não os impõe sozinha.

**Histórico do verificador inicial:** a função isolada verifica uma agenda fornecida. Existem agora otimizadores em grade e a etapa portátil27/10 abaixo; o verificador isolado não prova máxima autonomia nem mínimo tempo. Faltam dados reais de tração/auxiliares/PV/bateria e interpretação solar da rota. Não publicar o resultado sintético como viagem do motorhome.

Revisão humana: **PENDENTE**. Ver [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md).

## Método atual27/10

Continuação do método: [perdas por ramo, EVSE discreto, perfisAC/DC e PV12/48V](../../../docs/INTERFACE_CARGA_2026-10-27.md).
O caminho AC até o pack tem eficiência hipotética81%, sem aceitaçãoOEM comprovada.

[Equações com duas baterias, montagem/recolhimento e transferência hipotética](../../../docs/AGENDA_PORTATIL_2026-10-27.md).
O MILP maximiza distância diária na grade com duração de condução variável.
A construção7000km repete dias com estados finais compatíveis; não minimiza
globalmente o tempo. O verificador reabre CSV e confere também o fim da
condução dentro do passo. Potência mecânica nas rodas é distinta da demanda
terminal; potência no eixo do motor permanece desconhecida.

## Rota e sazonalidade28/10

[Modelo rodoviário, força em rampa, geração horária e política temporal](../../../docs/ROTA_REAL_2026-10-28.md).
O marco7000km é mantido dentro da geometria real7511,282km. A viagem usa
datas e posições variáveis, sem repetirSãoCarlos21jun. Limites por via são
hipóteses com perfilOSRM e tetoOEM90km/h. Falha de reserva da política não
é certificado de inviabilidade global; chegada em céu limpo não prova mínimo de tempo.
