"""Visualización del terreno y de las rutas encontradas."""
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from src.modelo import LIBRE, LEVE, MEDIA, BLOQUEADA

# Escala de un solo tono (azul): más oscuro = más inundado.
COLORES_NIVEL = {
    LIBRE: "#f4f3ef",
    LEVE: "#b9d4f2",
    MEDIA: "#5f9be3",
    BLOQUEADA: "#1f3a5f",
}
NOMBRES_NIVEL = {
    LIBRE: "Seco",
    LEVE: "Inundación leve",
    MEDIA: "Inundación media",
    BLOQUEADA: "Bloqueada",
}
COLOR_RUTA = "#eb6834"   # naranja: contrasta con la escala azul
COLOR_TEXTO = "#0b0b0b"

_CMAP = ListedColormap([COLORES_NIVEL[n] for n in (LIBRE, LEVE, MEDIA, BLOQUEADA)])
_NORM = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], _CMAP.N)


def dibujar_terreno(terreno, inicio=None, refugios=None, ruta=None,
                    titulo="", ax=None):
    """Dibuja el terreno por nivel de inundación y, opcionalmente, una ruta.

    - Las celdas bloqueadas llevan además un rayado, para no depender solo del color.
    - I marca el inicio y R cada refugio.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(terreno.shape[1] * 0.5 + 1,
                                      terreno.shape[0] * 0.5 + 1),
                             layout="constrained")
    filas, columnas = terreno.shape
    ax.imshow(terreno, cmap=_CMAP, norm=_NORM)

    # Rayado en celdas bloqueadas
    for f in range(filas):
        for c in range(columnas):
            if terreno[f, c] == BLOQUEADA:
                ax.add_patch(plt.Rectangle((c - 0.5, f - 0.5), 1, 1, fill=False,
                                           hatch="//", edgecolor="#f4f3ef",
                                           linewidth=0))

    # Cuadrícula tenue
    ax.set_xticks([x - 0.5 for x in range(1, columnas)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, filas)], minor=True)
    ax.grid(which="minor", color="white", linewidth=1)
    ax.tick_params(which="both", length=0)
    ax.set_xticks(range(columnas))
    ax.set_yticks(range(filas))
    ax.tick_params(labelsize=7, colors="#52514e")
    for borde in ax.spines.values():
        borde.set_visible(False)

    if ruta:
        columnas_ruta = [p[1] for p in ruta]
        filas_ruta = [p[0] for p in ruta]
        ax.plot(columnas_ruta, filas_ruta, color=COLOR_RUTA, linewidth=2.5,
                solid_capstyle="round", solid_joinstyle="round", zorder=3)
        ax.scatter(columnas_ruta, filas_ruta, s=14, color=COLOR_RUTA, zorder=4)

    for pos, letra in ([(inicio, "I")] if inicio else []) + \
                      [(r, "R") for r in (refugios or [])]:
        ax.text(pos[1], pos[0], letra, ha="center", va="center", fontsize=10,
                fontweight="bold", color=COLOR_TEXTO, zorder=5,
                bbox=dict(boxstyle="circle,pad=0.25", facecolor="white",
                          edgecolor=COLOR_TEXTO, linewidth=1))

    if titulo:
        ax.set_title(titulo, fontsize=10, color=COLOR_TEXTO, loc="left")
    return ax


def leyenda(fig, con_ruta=True):
    """Agrega la leyenda de niveles (y de la ruta) debajo de la figura."""
    elementos = [Patch(facecolor=COLORES_NIVEL[n], edgecolor="#c3c2b7",
                       hatch="//" if n == BLOQUEADA else None, label=NOMBRES_NIVEL[n])
                 for n in (LIBRE, LEVE, MEDIA, BLOQUEADA)]
    if con_ruta:
        elementos.append(Line2D([0], [0], color=COLOR_RUTA, linewidth=2.5, label="Ruta"))
    fig.legend(handles=elementos, loc="outside lower center", ncol=len(elementos),
               frameon=False, fontsize=8)