# CAD online e inspeção local — consulta de 24/10/2026

**Em uso:** malha detalhada GLB/STL derivada do OpenX Ducato, adaptada por scripts,
e OpenFOAM para CFD. O [visualizador local](../entregas/parcial_2026-10-24/visualizador.html)
abre diretamente no navegador e permite girar, aproximar, alternar vistas,
triângulos, módulos solares e reservas de interior. Funciona offline; Chromium
foi testado por Playwright, sem erros de JavaScript nem requisições HTTP.
Isso é inspeção da geometria, não editor CAD paramétrico ou CAD OEM.

Não há documento Onshape/Fusion criado nesta frente nem arquivo enviado a esses
serviços. As opções abaixo foram pesquisadas em documentação primária para
decidir o fluxo, sem fingir acesso a conta/licença ou download de CAD bloqueado.

| Opção verificada | Utilidade para este trabalho | Limite que afeta a escolha |
|---|---|---|
| [Onshape](https://www.onshape.com/en/pricing) | CAD no navegador, colaboração, peças/montagens e importação STEP | Plano Free é não comercial e documentos públicos. Revisar plano educacional para o grupo. A [tabela oficial](https://cad.onshape.com/help/Content/File/supported_file_formats.htm) lista STL como malha para visualização/referência; não contar com árvore paramétrica reconstruída automaticamente |
| [Autodesk Fusion pessoal](https://www.autodesk.com/products/fusion-360/personal) | Modelagem e formatos neutros; útil para componentes com CAD nativo disponível | Não é alternativa integral de CAD/CAE só pelo navegador. A [documentação oficial](https://help.autodesk.com/view/fusion360/ENU/?caas=caas%2Fsfdcarticles%2Fsfdcarticles%2FFusion-360-Free-License-Changes.html) limita documentos ativos/documentação e exclui simulação/cloud rendering do plano pessoal. Elegibilidade educacional deve ser verificada |
| GLB local + scripts + OpenFOAM | Já executável, reprodutível e sem upload; preserva a carroceria detalhada | Não fornece histórico paramétrico, superfícies OEM nem, sozinho, análise estrutural/encaixe completo |

A documentação Onshape também descreve ferramentas recentes de importação/malha;
há diferenças entre páginas de ajuda e dicas. Não se assume uma conversão para
sólido exato com base em publicidade. Fluxo de trabalho proposto: preservar a
carroceria como referência, construir peças internas/fixações como sólidos nativos,
e importar STEP dos fornecedores quando disponível. A troca de plataforma não
resolve mapas de motor, materiais, cargas térmicas ou ausência de dados físicos.

## Interferência encontrada e ajuste

O banheiro inicial reservava 0,90×0,82×1,90 m; seu topo cruzava o teto curvo
na sobreposição 3D com piso assumido Z=0,68 m. `layout-0.2` passou a reservar
0,90×0,76×1,80 m. `scripts/verificar_topo_banheiro.py` amostrou 81 raios
transversais sobre essa reserva: folga mínima **33,0 mm contra a malha externa**,
sem reprovação no critério amostral de 20 mm. Isso não desconta parede/isolamento,
não prova ausência de colisão entre amostras e não resolve a ergonomia da altura
de 1,80 m. Portas, caixas de roda e equipamentos ainda exigem sólidos e revisão.

Alinhamento visual assumido: traseira X=−3,35 m, piso Z=0,68 m, largura de carga
centrada em Y. Não são medições internas homologadas. O visualizador apresenta
essas hipóteses e esconde os painéis ao mostrar o interior para facilitar inspeção.

## Reprodução do visualizador

Three.js **0.180.0**, esbuild **0.25.10**, Playwright **1.56.1**, versões fixadas
em `scripts/visualizador/package-lock.json`. Three.js é MIT; licença íntegra
embutida no HTML e copiada para a entrega. A geometria preserva as licenças
MPL-2.0 AND CC-BY-4.0 e os créditos originais. Sem uso de código gerado por IA
como substituto da malha detalhada.

```bash
cd scripts/visualizador
npm ci --ignore-scripts
npm run build
```

Na raiz do projeto:

```bash
.venv/bin/python scripts/gerar_visualizador.py --glb entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb --layout config/layout_proposto.yaml --bundle scripts/visualizador/build/aurora.bundle.js --licenca-three scripts/visualizador/node_modules/three/LICENSE --destino NOVO
CHROMIUM_BIN=/caminho/chromium node scripts/visualizador/verificar.cjs NOVO/visualizador.html NOVO_QA
.venv/bin/python scripts/verificar_topo_banheiro.py --glb entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb --layout config/layout_proposto.yaml --destino NOVO_TRIAGEM
```

Também se pode usar o Chromium instalado pelo Playwright e omitir CHROMIUM_BIN.
O cache de dependências desta execução fica fora do Git em `software/visualizador-dev/`.
