# Carroceria de trabalho — Ducato detalhado

O exterior usado nesta frente passou a ser a malha **Fiat Ducato 2014**, derivada do modelo de razor24 e distribuída por Dogan Ulus/OpenX Assets, release **20261015**. O bloco autoral anterior fica restrito a teste de exportação; não é mais a geometria de trabalho. A escolha responde à instrução do usuário para aproveitar uma carroceria existente, sem preencher automaticamente dados físicos aprovados do motorhome.

## Referências do PDF reenviado

O arquivo reenviado é idêntico ao levantamento presente no repositório: SHA256 `0c0ad68fa68e1b12f5ad37717da460c7c1c1444017b3b24e36319f293d7bb8fc`. As pp. 6–8 indicam:

| Fonte | Verificação nova e uso |
|---|---|
| [E-Ducato L2H1 camper](https://3dwarehouse.sketchup.com/model/cf4cc175-b7fe-4058-9f2c-3880a144f188/Van-60-Fiat-E-Ducato-l2h1) | Leitura web retornou 403; HTTP direto retornou aplicação genérica de 10.922 bytes, sem binário SKP. Não obtido nem incorporado. |
| [Ducato L3H2 camper](https://3dwarehouse.sketchup.com/model/f5416eef-8f09-44de-82bf-0e1f92074275/L3H2-FIAT-DUCATO-CAMPER-VAN-MODEL2) | Mesma limitação observada. A referência continua registrada, sem alegar que o pacote foi aberto. |
| [MELVING22](https://github.com/MELVING22/solar-vehicle-chassis-design) | A montagem, peças da carroceria e IGES existem. O próprio levantamento p. 7 explica que é um solar car e não recomenda essa carroceria como motorhome final. O IGES local não foi convertido em carroceria de van. |
| Delica já presente no cache local | Interior detalhado preservado como referência: camas, armário, assento, mesa e piso. STEP com 68 sólidos. O STL também é desse interior, não contém o exterior completo. Não foi combinado artificialmente com o Ducato nem reescalado. |

Para avançar além das páginas sem download, foi obtido o [Ducato do OpenX Assets](https://github.com/vevalabs/openx-assets), derivado do [modelo original de razor24](https://sketchfab.com/3d-models/2014-fiat-ducato-8a651ad182414bb0a8b6c6d8d5bd7c01). A release fixada e os arquivos de autoria/licença foram efetivamente baixados e inspecionados. Acesso: 23/10/2026.

## Arquivos efetivamente usados

Originais e saídas permanecem fora do Git e não foram reanexados ao contexto:

- Pacote: `/home/mhc/motorhome_referencias_tarefas/cad-downloads/openx-assets-glb.zip`, 19.887.432 bytes, SHA256 `a89e822fe6be4058150090a2624052c0bc8a4612743784f371f8c25cb9d82cbb`.
- Original: `cad-downloads/openx-20261015/vehicles/fiat_ducato_2014/fiat_ducato_2014.glb`, sob a mesma raiz, 1.007.100 bytes; acompanhado de `.xoma`, `REUSE.toml` e licenças.
- Exterior preparado: `/home/mhc/motorhome_referencias_tarefas/ducato-exterior-04/ducato_exterior_m.glb` e `ducato_exterior_m.stl`.
- Imagens: `ducato_exterior.png` e `ducato_vistas.png` no diretório de saídas.
- Evidência: `manifesto_carroceria.json`, com hash das fontes/saídas, transformações, unidades, dimensões e limites; `ATTRIBUTION.txt` conserva os créditos.

A hierarquia original `Grp_Exterior` foi usada para preservar carroceria, rodas, portas, vidros, faróis e espelhos, excluindo `Grp_Interior`. A transformação é uma rotação rígida de Y-up/glTF para Z-up/projeto, sem escala: `x'=x, y'=-z, z'=y`. Os componentes não foram redesenhados, esticados nem convertidos por convex hull.

## Medições e limites

O exterior contém **32.350 triângulos**. A caixa envolvente mede aproximadamente **5,000 × 2,508 × 2,245 m**, incluindo espelhos na largura. A área frontal por união das projeções triangulares no plano YZ é aproximadamente **4,258 m²**, também com os apêndices. São medições da malha visual obtida, não cotas aprovadas de uma variante E-Ducato e não dados transportados para o YAML global.

O STL foi reaberto e sua caixa envolvente comparada à fonte. A malha **não é fechada**; por isso não se publicou volume interno, massa, Cd nem adequação automática a CFD. Fechar a superfície para o domínio de escoamento exigirá tratamento localizado dos furos/interseções e documentação do que foi alterado. A preparação não substitui essa etapa por uma forma inventada.

O `.xoma` possui massa, desempenho e medidas de eixos do ativo de simulação. Esses campos **não foram adotados** como ficha técnica de fabricante, motor elétrico, bateria, 0–100 ou massa do motorhome montado. A variante e as dimensões devem ser confrontadas antes de integrar o estudo energético. O Delica pertence a outro veículo: sua montagem de interior serve de referência, não como layout já encaixado neste Ducato.

## Reprodução

Instalar o extra `cad` na própria worktree. Em ambientes que herdam o SciPy antigo do sistema, usar NumPy `<2`; nesta execução foi necessário NumPy 1.26.4 para compatibilidade binária. Isso não altera o ambiente da outra conversa.

```bash
uv pip install --python .venv/bin/python -e '.[dev,cad]'
.venv/bin/python scripts/obter_carroceria.py --destino /tmp/ducato-fontes-novo
.venv/bin/python scripts/preparar_carroceria.py --entrada /tmp/ducato-fontes-novo/vehicles/fiat_ducato_2014/fiat_ducato_2014.glb --metadados /tmp/ducato-fontes-novo/vehicles/fiat_ducato_2014/fiat_ducato_2014.xoma --destino /tmp/ducato-exterior-novo
PYTHONPATH=src .venv/bin/python -m pytest tests/test_geometria_malha.py -q
```

Os destinos devem ser novos. O downloader fixa URL e SHA256 e extrai somente o Ducato, metadados e avisos; não executa código do fornecedor. A preparação gera os arquivos e figuras a partir da geometria real. Três testes analíticos verificam seleção por hierarquia, preservação de transformações/escala e área de silhueta sem contar superfícies ocultas duas vezes.

Licença declarada para o ativo: **MPL-2.0 AND CC-BY-4.0**. Créditos: razor24, 2019; Dogan Ulus, 2025. As mudanças feitas por esta frente estão registradas no aviso de atribuição e no manifesto. Os arquivos originais, avisos e licenças foram preservados no cache.
