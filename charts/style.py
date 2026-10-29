"""
Paleta, estilo de matplotlib y utilidades compartidas por los gráficos de todos los temas.
Palette, matplotlib style and helpers shared by every topic's charts.

Cada módulo de tema (charts/topics/<topic>.py) define TEXT = {"es": {...}, "en": {...}} y
CHARTS = [funciones]; cada función recibe (t, out) y guarda <nombre>.png en out.
Each topic module defines TEXT and CHARTS; each function takes (t, out) and saves <name>.png.
"""

import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

# Paleta del sitio / site palette
INK = "#111114"
INK_SOFT = "#3d3d45"
MUTED = "#6a6a74"
SURFACE = "#f3f3f5"
RULE = "#e2e2e6"
ACCENT = "#b3132b"
OK = "#1f7a4d"
AMBER = "#ffb21c"
GRAY = "#c9c9cf"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.edgecolor": RULE,
        "axes.linewidth": 0.8,
        "text.color": INK,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        # Fórmulas con mathtext estilo LaTeX (sin instalar TeX). LaTeX-style mathtext formulas (no TeX install).
        "mathtext.fontset": "cm",
    }
)

DPI = 200
WIDTH_IN = 8.0  # 8 in x 200 dpi = 1600 px


def clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(RULE)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(length=3, labelsize=9.5)


def fmt(value, t, digits=1, suffix=""):
    """Número con el separador decimal del idioma. Number with the language's decimal separator."""
    return f"{value:.{digits}f}".replace(".", t["decimal"]) + suffix


def pct(value, t, digits=0):
    """Porcentaje: «12 %» en español, «12%» en inglés. Percentage in each language's style."""
    return fmt(value, t, digits, " %" if t["decimal"] == "," else "%")


def figure(height, **kwargs):
    return plt.subplots(figsize=(WIDTH_IN, height), dpi=DPI, **kwargs)


def save(fig, out, name):
    fig.savefig(os.path.join(out, f"{name}.png"))
    plt.close(fig)


def diagram_axes(ax, width, height):
    """Ejes en blanco con coordenadas de datos para diagramas. Blank axes in data units for diagrams."""
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")


def box(ax, x, y, w, h, text, edge=INK_SOFT, fill=SURFACE, size=10, color=INK, weight="normal", lw=1.3):
    ax.add_patch(
        FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", linewidth=lw, edgecolor=edge,
                       facecolor=fill, zorder=2)
    )
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
                fontweight=weight, zorder=3)


def arrow(ax, start, end, color=MUTED, lw=1.4, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=12, linewidth=lw, color=color,
                                 zorder=1, shrinkA=0, shrinkB=0))


def cli(text, charts):
    """Interfaz común: --lang es|en --out <dir>. Common CLI used by every topic module."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=text, default=os.environ.get("MLA_LANG", "es"))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for chart in charts:
        chart(text[args.lang], args.out)
    print(f"{len(charts)} charts ({args.lang}) -> {args.out}")
