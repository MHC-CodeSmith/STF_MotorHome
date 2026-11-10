# Execução técnica02 ativa

Leia o registro integral das61decisões e `docs/EXECUCAO_TECNICA02.md`. Fonte única: `config/parametros_globais.yaml`, revisão1.1.0-execucao02. CAD/massa/CG e auxiliares de tração estimados integram os novos modelos. Revisão35atual: `docs/REVISAO_TECNICA_EXECUCAO02.md`. Baseline29defc4 e seus manifestos são históricos; não atualizar seus hashes para mascarar mudança de entradas. Nenhuma aprovação humana final ou interfaceDCfísica demonstrada.

# Instruções gerais para Codex / agentes

Para esta frente, comece por `docs/RETOMADA_TAREFAS.md`: consulte resumos e trechos de textos locais, sem carregar PDFs, ZIPs ou CAD brutos no contexto. Preserve a outra conversa em `/home/mhc/motorhome_solar_codex`; alterações desta frente pertencem à worktree `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`.

Você está trabalhando no projeto acadêmico **motorhome elétrico solar** do grupo de 7 integrantes. Esta raiz contém o escopo oficial e as regras para qualquer agente. Leia primeiro `docs/HUB_CONTEXT.md`, `docs/dependencias.md`, `docs/marcos_e_revisoes.md`, `docs/PROMPT_INICIAL_CODEX.md` e `docs/fontes_recebidas/`.

## Hierarquia de fontes
1. Enunciado original de 2026: fonte autoritativa dos **requisitos**.
2. `Organizacao_Motorhome_P1_P7.pdf`: fonte autoritativa da **divisão mais recente**, substitui versões antigas no chat.
3. `config/parametros_globais.yaml`: fonte autoritativa dos **parâmetros já aprovados**.
4. Documentação do fabricante/artigos/dados revisados: fontes para os componentes e hipóteses.
5. Repositórios externos: candidatos a adaptar, não resultados finais automaticamente válidos.

## Regras obrigatórias
- Não inventar dados, CAD, resultados CFD, convergência, validação, custo, curva de motor ou licença. Marcar lacunas claramente.
- Trabalhar com unidades do SI e documentar todas as conversões e hipóteses; salvar resultados numéricos com unidade, cenário, data, versão de configuração e script que os reproduz.
- Se precisar de parâmetro ainda não definido, deixar `null`, expor bloqueio, ou testar valores **explicitamente demonstrativos**, jamais publicá-los como resultado do projeto.
- Não modificar `config/parametros_globais.yaml` silenciosamente; quando alterar, registrar motivo e itens afetados em `docs/decisoes.md`.
- Cada item deve ter: teoria, entradas, fontes com URL e data de acesso, método, código, resultados rastreáveis, figuras e validação humana registrada.
- Reaproveitamento: registrar URL, commit/versão, licença, arquivos importados, mudanças realizadas e atribuição em `fontes_externas/catalogo.csv` e na pasta `externos` do item. Respeitar direitos autorais; sem copiar texto de teses integralmente.
- Fornecer script reexecutável que gere cada gráfico/resultado; distinguir resultado estimado, simulado, medido e retirado de fabricante.
- A autonomia de **7000 km (item 29)** usa somente bateria inicial e geração solar, **sem recarga externa**. Máximo de 8 h de condução/dia.
- CFD, freios e cabos exigem resultados de simulação multidimensional de verdade e revisão de malha/contorno/convergência; não substituir CFD por um Cd hipotético sem avisar.
- Colaborar com PRs por responsável e revisão por outro integrante; atualizar o registro de interfaces sempre que entrada compartilhada mudar.

## Estado inicial desta entrega
Repositório é um **scaffold validado**, sem componentes finais nem simulações rodadas. O trabalho subsequente é pesquisa/importação legítima, parametrização, desenvolvimento e validação.
