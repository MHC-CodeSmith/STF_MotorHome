# Arquitetura sugerida para o hub de agentes

## Coordenador global (chat/hub)
- Lê `docs/HUB_CONTEXT.md`, enunciado, organização P1–P7, matérias, parâmetros e decisões.
- Não calcula tudo sozinho; desbloqueia interfaces, preserva versão única e aprova merges após revisão.
- A cada milestone, identifica bloqueios, responsáveis e mudanças que exigem recálculo.

## 7 agentes técnicos
- **Agente P1** — estrutura/freios (I01, I02, I03, I14, I15, I18, I24, I33).
- **Agente P2** — bateria/elétrica (I06, I07, I09, I23, I30).
- **Agente P3** — carroceria/CAD/CFD (I16, I17, I19).
- **Agente P4** — motor/dinâmica (I04, I05, I20, I21, I22, I28).
- **Agente P5** — solar/autonomia (I08, I25, I26, I27, I29).
- **Agente P6** — interior/HVAC (I11, I13, I31, I32).
- **Agente P7** — arrefecimento/bateria (I10, I12, I34, I35).

## Fluxo de trabalho entre agentes
1. Criar branch/PR por item, com autor principal e revisor diferente.
2. Trabalhar localmente em `equipe/PX.../Ixx...`; manter resultados temporários separados de resultados aprovados.
3. Quando um parâmetro afetar outro grupo, solicitar sua revisão pelo coordenador e registrar em `docs/decisoes.md`.
4. Cada PR inclui: objetivo, arquivos, testes, fonte dos dados, licença dos imports, entradas/saídas, impacto e dúvidas.
5. No gate semanal, consolidar saídas aprovadas; não propagar pressupostos como fatos.

## Três filas de prioridade
- **Bloqueadores iniciais**: veículo-base, chassi, motor, bateria, painel, geometria, massa.
- **Modelos centrais**: Cd/CFD, forças, tração, geração solar, consumo, autonomia.
- **Trabalho paralelo especializado**: CFD com validação, freios 2D, fios 2D, bateria térmica, bomba/radiador, HVAC.

## Prompt para iniciar cada agente
> Leia `AGENTS.md` na raiz, `docs/HUB_CONTEXT.md`, seu `AGENTS.md` de equipe e o README dos seus itens. Faça uma auditoria das entradas pendentes; implemente o máximo que for possível sem inventar dados; cite fontes e licenças; mantenha os outputs reproduzíveis; indique testes e requisitos de revisão humana. Não altere parâmetros globais sem registrar decisão e impacto.
