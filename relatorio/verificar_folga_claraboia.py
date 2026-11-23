"""Verifica em planta a faixa central entre o último módulo e o para-brisa.

A pele externa provém do GLB do relatório. O STL do deck está no mesmo referencial.
Micro Heki 9104117435: Dometic, catálogo Windows & Roof Windows 2025, seção 3.42,
espaço exterior de montagem 430 × 390 mm. O desenho DOK 1203, seção 24.3,
indica 408 × 370 mm para o corpo e 280 × 280 mm para o recorte.
"""
import json
import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
GLB = ROOT / "entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb"
DECK = ROOT / "entregas/aero_equipado1540/malha1/constant/triSurface/pvdeck.stl"

def vidro_dianteiro():
    """Lê o grupo de vidro do GLB métrico, cujas coordenadas já são globais."""
    raw = GLB.read_bytes()
    length, = struct.unpack_from("<I", raw, 12)
    gltf = json.loads(raw[20:20+length])
    binary = memoryview(raw)[28+length:]
    if any(set(node) & {"matrix", "translation", "rotation", "scale"} for node in gltf["nodes"]):
        raise ValueError("Esta versão do GLB exige aplicar transformações de nós.")
    def vetor(index):
        access = gltf["accessors"][index]
        view = gltf["bufferViews"][access["bufferView"]]
        if "byteStride" in view or view["buffer"] != 0:
            raise ValueError("Buffer incompatível com este GLB.")
        tipo = {5125: "<u4", 5126: "<f4"}[access["componentType"]]
        dim = {"SCALAR": 1, "VEC3": 3}[access["type"]]
        offset = view.get("byteOffset", 0) + access.get("byteOffset", 0)
        return np.frombuffer(binary, dtype=tipo, offset=offset,
                             count=access["count"]*dim).reshape(-1, dim)
    node = next(node for node in gltf["nodes"] if node["name"] == "Exterior_Static_313fb3")
    prim = gltf["meshes"][node["mesh"]]["primitives"][0]
    faces = vetor(prim["indices"]).reshape(-1, 3)
    tri = vetor(prim["attributes"]["POSITION"])[faces].astype(float)
    # O mesmo material aparece também em lanternas e vidros laterais, fora da faixa.
    return tri[(tri[:, :, 0].min(axis=1)>0) & (np.abs(tri[:, :, 1]).min(axis=1)<0.89)]

def borda_vidro(triangulos, lateral):
    borda = []
    for face in triangulos:
        for a, b in zip(face, np.roll(face, -1, axis=0)):
            if a[1] != b[1] and min(a[1], b[1]) <= lateral <= max(a[1], b[1]):
                borda.append(a[0] + (b[0]-a[0]) * (lateral-a[1]) / (b[1]-a[1]))
    return min(borda)

def dimensao(ax, xi, xf, y, texto, cor, acima=True):
    ax.annotate("", (xf,y), (xi,y), arrowprops={"arrowstyle": "<->","color": cor,"lw": 1.2,"shrinkA": 0,"shrinkB": 0})
    ax.vlines((xi,xf),y-.023,y+.023,colors=cor,lw=.85)
    ax.text((xi+xf)/2,y+(.037 if acima else -.036),texto,ha="center",va="center",
            fontsize=10,weight="bold",color=cor)

def main():
    tri = vidro_dianteiro()
    dtype = np.dtype([("normal","<f4",3),("vertices","<f4",(3,3)),("attr","<u2")])
    verts = np.frombuffer(DECK.read_bytes(), dtype=dtype, offset=84)["vertices"]
    ponta = float(verts[:,:,0].max())
    vidro = borda_vidro(tri,0.0)
    vao = vidro-ponta
    corpo_x, montagem_x, montagem_y = .370, .390, .430
    print(f"Deck x={ponta:.6f} m, para-brisa (y=0) x={vidro:.6f} m.")
    print(f"Faixa {vao:.6f} m; falta {corpo_x-vao:.6f} m para o corpo e {montagem_x-vao:.6f} m para a montagem.")
    azul, vermelho = "#25506b","#9d3c20"
    fig, ax = plt.subplots(figsize=(6.7,2.65))
    ax.set_facecolor("#f4f3ed")
    ax.add_patch(Rectangle((0,-1),ponta,2,facecolor="#dce5eb",edgecolor="#8298a4",lw=1))
    ax.add_collection(PolyCollection(tri[:,:,:2],facecolors="#bad8db",edgecolors="face",lw=.25))
    ax.plot([ponta,vidro],[0,0],color="#69818c",lw=.65,ls=":")
    ax.add_patch(Rectangle((ponta,-montagem_y/2),montagem_x,montagem_y,
                           facecolor="none",edgecolor=vermelho,linestyle="--",lw=1.5))
    ax.text(.52,0,"Deck solar",ha="center",va="center",fontsize=11,color=azul)
    ax.text(1.36,0,"Para-brisa",ha="center",va="center",fontsize=11,color=azul)
    dimensao(ax,ponta,vidro,.290,f"Vão no eixo  {vao*1000:.0f} mm",azul)
    dimensao(ax,ponta,ponta+montagem_x,-.28,"Montagem  390 mm",vermelho,acima=False)
    ax.set(xlim=(.32,1.55),ylim=(-.355,.365),aspect="equal")
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_color("#a3afb2")
    fig.subplots_adjust(left=.015,right=.985,bottom=.025,top=.985)
    dest=ROOT/"relatorio/figuras/i16_folga.png"
    fig.savefig(dest,dpi=220,bbox_inches="tight",pad_inches=.02)
    plt.close(fig)

if __name__ == "__main__":
    main()
