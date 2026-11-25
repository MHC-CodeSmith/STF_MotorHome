# Instrução editorial vigente — 25/11/2026

O usuário rejeitou o PDF de 85 páginas por ser longo. A versão final deve seguir de perto
a redação do Cuca, inclusive frases aplicáveis, adaptadas com atribuição, sem copiar
resultados de outro projeto. Manter simulações, gráficos e imagens. **Nenhum código ou
anexo de listagens no PDF final**; fontes permanecem no repositório. Vídeo segue excluído.
Conferir todos os PRs e o enunciado, não só o Fael: `docs/AUDITORIA_ENUNCIADO_E_PRS.md`.
Os complementos P7 não mudam massa nem missão: são campos/verificações e requisitos
condicionais, sem fingir instalação de chiller, ventilador ou peças OEM não selecionadas.

# Revisão do relatório em 25/11/2026

Para a continuação mais recente, leia `docs/HANDOFF_PROXIMA_SESSAO.md` e
`docs/AUDITORIA_PR9_REESCRITA.md`. A revisão segue o modelo Cuca; o cenário ativo é
`maxeon1560_independente`, incluindo a cama no inventário e nos resultados derivados.
Os nomes da capa são os oito fornecidos pelo usuário em `relatorio/autores.tex`; preservar
essas grafias. O vídeo foi retirado do escopo por instrução explícita do usuário.
As instruções e cenários anteriores abaixo são históricos quando divergirem desse estado.

# Fechamento e entregáveis (16/11/2026)

O usuário pediu para terminar os 35 itens e o trabalho todo: relatório, slides e roteiro do vídeo estão em `relatorio/` (ver `relatorio/README.md`) e as lacunas fechadas em `docs/FECHAMENTO_35_ITENS.md`. A instrução antiga de não preparar relatório/slides está revogada. Comece por `docs/HANDOFF_PROXIMA_SESSAO.md`.

# Integração1540Wp reproduzida

Ocenário `maxeon1540_independente` está definido no únicoYAML canônico e foi executado pela cadeia `scripts/executar_cenario_integrado.py`. Resultados em `entregas/integrado_maxeon1540/`,CFDequipado em `entregas/aero_equipado1540/`;base1350Wp preservada como comparação,não misturar entradas/saídas. Usar plano atualizado e revisão35;executores históricos não atualizam o projeto ativo. Aprovação humana e interfaceDC continuam não demonstradas. Não reiniciar pesquisa repetitiva nem preparar relatório/slides agora.

# Execução técnica02 ativa

Leia o registro integral das61decisões e `docs/EXECUCAO_TECNICA02.md`. Fonte única: `config/parametros_globais.yaml`, revisão1.1.1-execucao1540. CAD/massa/CG e auxiliares de tração estimados integram os novos modelos. Revisão35atual: `docs/REVISAO_TECNICA_EXECUCAO02.md`. Baseline29defc4 e seus manifestos são históricos; não atualizar seus hashes para mascarar mudança de entradas. Nenhuma aprovação humana final ou interfaceDCfísica demonstrada.

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
