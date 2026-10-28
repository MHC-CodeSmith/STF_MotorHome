# Método e limites — item 27

Maximizar a distância diária com SOC final igual a 0,30 dentro de tolerância explícita, mostrando v(t) e potência instantânea do motor.

Fonte do requisito: enunciado 2026 p. 2, I27, conferido em extração local em 23/10/2026. A apostila cap. 1 contextualiza projeto e otimização, mas não fornece um solver desta agenda.

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
