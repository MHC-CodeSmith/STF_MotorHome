# Pneu candidato e orçamento de carga - 25/10/2026

I02 passa de não iniciado para desenvolvimento com especificação verificável.
**Ainda falta roda completa, pressão operacional, compatibilidade OEM e carga
por eixo.** Não alterar o CAD ou a dinâmica com este candidato sem decisão.

Fonte primária: [Continental VanContact A/S, especificações](https://continentaltire.com/tires/vancontact-as/specs),
consulta 25/10/2026, artigo **04514690000**, 225/75 R16C, índice121R.
Existem outros artigos com a mesma medida e massas/pressões distintas; não misturar
as linhas. HTML em cache, SHA256
`f7a620f37e0d60503594d8a8e75164e70c73e49a29a890fd9bc744c4ec671c73`.

| Especificação publicada | Conversão SI |
|---|---:|
| Aro admissível 6–7 in | 0,1524–0,1778 m de largura |
| Diâmetro 29,3 in | 0,74422 m |
| Massa por pneu 37,3 lb | 16,9190 kg |
| Carga máxima 3.195 lb | 1.449,23 kg por pneu |
| Pressão **máxima** 90 psi | 620.528 Pa |
| 709 revoluções por milha | circunferência efetiva 2,26988 m; raio 0,361262 m |

Conversões: 1 in = 0,0254 m; 1 lb = 0,45359237 kg; 1 milha = 1609,344 m;
1 psi = 6894,757293 Pa. Raio geométrico e raio de rolamento não são intercambiáveis.
A página não fornece a curva Cr versus carga/pressão, materiais constituintes
completos nem pressão a adotar para este motorhome. Os 90 psi não devem virar
pressão de uso. A ficha Fiat consultada inclui 215/75R16C de base e opção reforçada
225/75R16C; configuração/placa de pressões devem ser obtidas para a variante exata.

A malha visual atual tem pneus com diâmetro aproximado de 0,700895 m. O candidato
é cerca de 6,18% maior. Necessário revisar folga, diâmetro no CAD, transmissão,
contato com solo e todos os casos CFD antes de adotá-lo. Não combinar a área/Cd
de uma roda antiga com geometria nova como se fosse o mesmo veículo validado.

## Limite de massa que já pode ser estabelecido

Ficha OEM da variante proposta: 2790 kg sem motorista e máximo4250 kg, reserva
1460 kg. Pack, motor, freios e rodas OEM já integram os 2790 kg; somar só
diferenças por substituição, além da conversão. Dois módulos JA450 pesam44 kg.
Assumindo duas pessoas de75 kg e100 kg de água, restam **1166 kg** para conversão,
armazenamento de serviços, mobiliário, utensílios e bagagens. Não é massa montada
calculada nem reserva garantida: limites por eixo e distribuição longitudinal
podem restringir antes do PBT. Passageiros e água são hipóteses de orçamento.

I18/I24 continuam pendentes de BOM com quantidades, massas, posições e custos
reais. Não somar novamente quatro pneus candidatos se apenas substituem pneus
originais já incluídos na massa OEM; computar a diferença quando ambas as massas
forem conhecidas. A massa de uma roda completa não é a massa isolada do pneu.
