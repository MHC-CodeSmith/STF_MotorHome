# Métodos térmicos implementados — revisão física pendente

Os módulos [sistemas_termicos.py](../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../src/motorhome/termica_2d.py) são implementações próprias de balanços. Não incorporam o código de freios externo sem licença. Dados da demonstração são explicitamente **SYNTHETIC**; as propriedades reais do motorhome continuam pendentes.

## Fontes e equações

Base local: apostila SEM0571 v0.4, Cristiano Bigonha Tibiriçá, 2025. Páginas físicas 9/10: Fourier e Newton; p. 31, Eqs. (49–51): balanços de trocador; p. 38, Eqs. (59–62), e p. 39, tabela 4: ε-NUT paralelo e contracorrente; p. 56, Eqs. (92–93): bomba e curva do sistema; p. 74, Eq. (112): armazenamento sensível. Consulta dos trechos em 23/10/2026; tabela 4 e página de bombas conferidas visualmente. [Mapa](mapa_teorico.md) e [ressalvas de transcrição](revisao_apostila.md) conservam as referências e dúvidas.

### I30 e I33 — campo multidimensional

O balanço usado é `rho cp dT/dt = div(k grad T) + qv`. O solver usa volumes finitos cartesianos em duas dimensões, espessura constante, sólido homogêneo e propriedades constantes. Fluxos internos entram em uma célula e saem da vizinha; fontes são dadas em W/m³. Faces em z são adiabáticas. Cada uma das quatro bordas aceita isolamento, temperatura prescrita, fluxo de entrada ou convecção. Para convecção, a condutância inclui a resistência condutiva de meia célula e a do filme. Euler explícito exige `dt <= C_cel / soma(G)`; o código rejeita passo instável e temperatura absoluta não positiva.

O teste analítico `T=T0+A cos(pi x/Lx) cos(pi y/Ly) exp[-alpha pi²(1/Lx²+1/Ly²)t]` com bordas isoladas verifica a variação nas duas direções. Refinamentos 8/16/32 verificam convergência espacial; comparação com o autovalor espacial discreto verifica a primeira ordem temporal. Há testes adicionais de solução linear, resistência convectiva, fonte uniforme e conservação.

Para cabos, `qv=(I/A)² rho_e`; a lei linear `rho_e=rho_ref[1+alpha_e(T-Tref)]` está disponível, mas o solver de fonte fixa não faz seu acoplamento automático. Cabo com isolamento requer malha/material compatíveis; motor trifásico exige corrente RMS/perdas apropriadas, sem substituir isso por corrente DC presumida.

Para freios, a remoção translacional prescrita é `(30²−10²)/2=400 J/kg` e a potência média é 80 W/kg em 5 s. Isso não é calor integral de disco: faltam massa, inércias, partição disco/pastilha, regeneração e dissipações. Um caso de freio deve iniciar em 298,15 K e distribuir a potência no espaço/tempo com fonte. A demonstração retangular genérica não é uma simulação do disco.

### I31 e I34 — armazenamento concentrado

A solução exata implementada usa `C dT/dt = Q − UA(T−Ta)` para coeficientes constantes, incluindo o limite adiabático UA=0. O balanço integrado separa energia gerada, armazenada e perdida. O uso concentrado exige justificar gradientes internos desprezíveis, por exemplo por análise de Biot com geometria e h reais. A cabine ainda requer radiação, superfícies e regime definidos. Para o pack, a função elétrica calcula apenas a parcela I²R: não resolve calor reversível, química, CC/CV ou BMS. Os carregadores de 20/80 kW não são fontes térmicas de 20/80 kW.

### I32 — A/C

A carga permanente separa `Q_s=UA(Te−Ti)+Q_solar+Q_equip+N Q_pessoa,s+Q_vent,s` e `Q_l=N Q_pessoa,l+Q_vent,l`. A conversão para eletricidade exige COP fornecido. Os termos devem ser obtidos de superfícies, propriedades, psicrometria e equipamentos reais, evitando dupla contagem da radiação e da absorção em superfícies opacas. A função agregada não resolve o ciclo de refrigeração e não estabelece COP de fabricante.

### I35 — trocador e bomba

O trocador usa capacidades `Ch=m_dot_h cp_h`, `Cc=m_dot_c cp_c`, `NTU=UA/Cmin` e efetividade apropriada para **paralelo ou contracorrente**, sem mudança de fase/perdas externas. O limite Ch=Cc tem ramo explícito. As temperaturas respeitam conservação em ambos os lados; o perfil analítico disponível é somente paralelo. Isso não seleciona o arranjo de radiador automotivo.

A bomba é tratada por interseções lineares entre pressões diferenciais de bomba/sistema numa malha de vazões comum; não se extrapola nem se escolhe uma interseção automaticamente. Se o catálogo fornece altura H, converter por `dp=rho g H` com o mesmo fluido. Perdas de tubulações/radiador, NPSH, eficiência e ponto em potência máxima do motor ainda precisam ser fornecidos.

## Reprodução

```bash
uv pip install --python .venv/bin/python -e '.[dev,thermal]'
PYTHONPATH=src .venv/bin/python -m pytest tests/test_termica_2d.py tests/test_sistemas_termicos.py tests/test_agenda_energia.py -q
.venv/bin/python scripts/demonstrar_frente_termica.py --sintetico --destino /tmp/motorhome-thermal-novo
```

O destino deve ser novo. Resultados já executados estão fora do Git em `/home/mhc/motorhome_referencias_tarefas/verificacao-termica-01/`: entradas JSON com hash, CSV do campo/histórico/convergência, figura e resumo. A ordem espacial mínima registrada foi 2,002. `frenagem_prescrita_por_kg.json` fica separado dos resultados sintéticos por ser derivação direta do enunciado. Todos os itens continuam exigindo validação humana e dados físicos antes de fechamento.
