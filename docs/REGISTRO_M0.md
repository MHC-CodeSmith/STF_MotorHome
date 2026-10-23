# Registro M0 — decisões pendentes

Preparado em 22/10/2026 para o marco interno de 23/10/2026. P1 coordena a coleta; os donos abaixo são funções P1–P7, pois nomes e disponibilidade ainda não foram registrados. Este documento não altera requisitos, atribuições nem parâmetros aprovados.

Base: [plano dos dez trabalhos](PLANO_10_TRABALHOS.md), [marcos](marcos_e_revisoes.md), [dependências](dependencias.md) e [decisões existentes](decisoes.md). Requisitos conferidos na extração local de 5.990 bytes `~/motorhome_referencias/textos/Projeto Sist. Térmicos e Fluídicos 2026.txt`, páginas 1–2; PDF original preservado em `docs/fontes_recebidas/`. Organização consultada por trechos em `~/motorhome_referencias/textos/Organizacao_Motorhome_P1_P7.txt`. Não houve consulta nova a fontes externas nem contato com docentes.

## Pauta para a equipe e os docentes

Todas as linhas começam **PENDENTES**. Prazo de encaminhamento: M0, 23/10; especificações preliminares de componentes: M1, 30/10. Esses são prazos internos, não aprovações já obtidas.

| ID | Questão a resolver / evidência esperada | Quem decide; quem prepara | Impacto |
|---|---|---|---|
| M0-01 | Autorizar grupo de sete frente aos dez do enunciado p. 1; guardar resposta com autor e data | Docentes; P1 encaminha | D000, todos os itens e distribuição da apresentação |
| M0-02 | Associar nomes, disponibilidade e revisores a P1–P7, preservando a divisão mais recente | Equipe; P1 consolida | Interfaces e cronograma dos 35 itens |
| M0-03 | Escolher conceito e veículo-base após comparação de envelope, chassi, ocupação e evidências CAD/licença; registrar alternativas e justificativa | Equipe; P1/P3/P6 preparam | D001; I01/I15/I16/I17 e toda a cadeia de massa/energia |
| M0-04 | Explicitar SOC inicial de I27 e tolerância numérica para o alvo final de 30%; esclarecer com docentes as hipóteses de uso não prescritas | Docentes esclarecem; P2/P5 propõem e equipe revisa | I23/I27; `battery.initial_soc_fraction`; a chave histórica de SOC mínimo não substitui o alvo final |
| M0-05 | Definir se I31 será transiente ou permanente e, se transiente, condição inicial/horário; manter cabine fechada, estacionada, sem A/C e sem passageiros | Docentes esclarecem; P6 prepara | I31; propriedades, geometria e balanço térmico |
| M0-06 | Confirmar ocupação e carga térmica humana de I32; o item diz passageiro e exige regime permanente com exterior 33 °C e interior 25 °C | Docentes esclarecem; P6 prepara | I11/I32 e potência auxiliar fornecida a P5 |
| M0-07 | Esclarecer aplicação do cenário solar de São Carlos, 21/06, à rota Belém–Chuí; registrar cenário geográfico/temporal a usar | Docentes esclarecem; P5 prepara | I08/I29; manter 7000 km, só bateria inicial + solar e até 8 h de condução/dia |
| M0-08 | Documentar coordenadas/altitude e a convenção de ano solar 2026, com fonte e revisão; não preencher por aproximação sem registro | P5 propõe; equipe revisa | I08/I25/I27/I29/I31/I32 e campos geográficos globais |
| M0-09 | Registrar acesso real a CAD/CFD e solvers térmicos, pessoa responsável e caso de verificação reexecutável; disponibilidade no host não prova acesso dos estudantes | P3/P1 para CAD/CFD; P1/P2/P7 para térmica | I17/I19/I30/I33/I34/I35; ver [software](software_disponivel.md) |
| M0-10 | Revisar necessidade da aresta final I28 → I33; a frenagem de I33 já prescreve 30 → 10 m/s em 5 s, início 25 °C | P1/P4; revisão cruzada | I33 pode desenvolver método sem esperar aceleração; não remover dependência silenciosamente |

## Como registrar uma resolução

Para cada ID, acrescentar resposta literal curta ou síntese fiel, autor, data, referência da evidência local, itens afetados e revisor. Registrar qualquer nova decisão em `decisoes.md`, citando o ID M0. Não substituir a pergunta pelo texto da resposta: conservar o histórico.

Se houver alteração de parâmetro, registrar valor anterior/proposto, unidade, fonte e impacto antes de revisar `config/parametros_globais.yaml`. O fechamento de um ID exige resposta e revisão registradas; preparar a pauta não fecha o marco. A escolha de veículo, componentes e a aprovação de resultados exigem validação humana conforme `PROMPT_INICIAL_CODEX.md`.

## Trabalho que pode avançar enquanto as decisões aguardam

- P1/P3/P6: preparar a matriz de conceito/envelope com dados ausentes marcados e evidências locais do catálogo; não selecionar base por disponibilidade de um ZIP.
- P4/P2: estruturar dossiês de motor/transmissão/bateria e fontes das curvas; não preencher limites elétricos com números demonstrativos.
- P3, P1/P2/P7 e P6: desenvolver métodos e casos de verificação identificados como sintéticos, com revisão de unidades, contornos e conservação.

A ordem completa, os donos e os critérios de cada entrega continuam no plano existente. A base comum de cálculos está em desenvolvimento na outra conversa e depende de integração posterior dos respectivos commits.
