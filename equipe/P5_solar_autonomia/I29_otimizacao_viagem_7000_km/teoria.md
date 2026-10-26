# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Método e limites — item 29

Minimizar o tempo total para 7.000.000 m com bateria inicial e solar, sem recarga externa, até 28.800 s de condução por dia de calendário.

Fonte do requisito: enunciado 2026 p. 2, I29, conferido em extração local em 23/10/2026. A apostila cap. 1 contextualiza projeto e otimização, mas não fornece um solver desta agenda.

O [verificador temporal](../../../src/motorhome/agenda_energia.py) usa intervalos de potência/velocidade constantes, integra distância e energia e divide intervalos nas meias-noites locais. Energia da bateria recebe eta_carga vezes o saldo terminal positivo e fornece o saldo negativo dividido por eta_descarga. SOC é E/E_ref, com capacidade de referência explicitamente definida. Noites/paradas precisam constar da agenda.

O verificador detecta déficit antes do solar posterior, excedente de capacidade e excesso diário de condução. Corte solar é opcional e contabilizado; não há recarga externa no contrato. Fornecer alvo/tolerância de SOC e distância/limite diário com os valores do enunciado: a API genérica não os impõe sozinha.

**Ainda não existe otimizador.** A função verifica uma agenda fornecida; não prova máxima autonomia nem mínimo tempo. Faltam dados reais de tração/auxiliares/PV/bateria, SOC inicial e interpretação solar da rota. Não publicar o resultado sintético como viagem do motorhome.

Revisão humana: **PENDENTE**. Ver [revisão dos 35 itens](../../../docs/REVISAO_35_ITENS.md).
