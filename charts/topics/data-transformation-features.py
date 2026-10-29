"""
Tema 1.2: transformación, feature engineering y preprocesamiento.
Topic 1.2: transformation, feature engineering and preprocessing.

    python charts/topics/data-transformation-features.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np
from scipy.stats import skew

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from matplotlib.patches import Rectangle  # noqa: E402

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    clean_axes, cli, figure, fmt, pct, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "panels": ["Original: monthly_spend", "Solo estandarización", "Logaritmo y después estandarización"],
        "skew": "asimetría",
        "x_raw": "Gasto mensual",
        "x_z": "z-score",
        "x_logz": "z-score de log(gasto)",
        "rows": "Clientes",
        "same_shape": "misma forma, otra escala",
        "illustrative": "Datos sintéticos ilustrativos (lognormal)",
        "scalers": ["Min-Max", "Standard (z-score)", "Robust (mediana e IQR)"],
        "bulk": "99 % de los datos\nentre {} y {}",
        "outlier_at": "► outlier en {}",
        "scaled": "Valor escalado",
        "outlier": "outlier",
        "sc_title": "Mismos datos con un outlier, tres escaladores",
        "width": "ancho",
        "tokens": "Posición en el documento (tokens, ilustrativo)",
        "doc": "Documento",
        "topics": ["Instalación", "Errores", "Garantía"],
        "fixed": "Tamaño fijo\n+ solapamiento",
        "hier": "Jerárquico",
        "sem": "Semántico",
        "overlap": "solapamiento",
        "parent": "padre",
        "child_hit": "el hijo coincide → se devuelve el padre",
        "cut_ignores": "corta sin mirar el tema",
        "cut_meaning": "corta donde cambia el significado (usa un FM)",
    },
    "en": {
        "decimal": ".",
        "panels": ["Original: monthly_spend", "Standardization only", "Log, then standardization"],
        "skew": "skewness",
        "x_raw": "Monthly spend",
        "x_z": "z-score",
        "x_logz": "z-score of log(spend)",
        "rows": "Customers",
        "same_shape": "same shape, new scale",
        "illustrative": "Illustrative synthetic data (lognormal)",
        "scalers": ["Min-Max", "Standard (z-score)", "Robust (median and IQR)"],
        "bulk": "99% of the data\nbetween {} and {}",
        "outlier_at": "► outlier at {}",
        "scaled": "Scaled value",
        "outlier": "outlier",
        "sc_title": "Same data with one outlier, three scalers",
        "width": "width",
        "tokens": "Position in the document (tokens, illustrative)",
        "doc": "Document",
        "topics": ["Installation", "Errors", "Warranty"],
        "fixed": "Fixed-size\n+ overlap",
        "hier": "Hierarchical",
        "sem": "Semantic",
        "overlap": "overlap",
        "parent": "parent",
        "child_hit": "child matches → parent is returned",
        "cut_ignores": "cuts regardless of topic",
        "cut_meaning": "cuts where meaning changes (uses an FM)",
    },
}


# ─── 1. Logaritmo y escalado / log then scale ──────────────────────────────────
def chart_log_then_scale(t, out):
    rng = np.random.default_rng(5)
    spend = rng.lognormal(mean=3.4, sigma=0.9, size=4000)
    z = (spend - spend.mean()) / spend.std()
    logs = np.log(spend)
    lz = (logs - logs.mean()) / logs.std()

    fig, axes = figure(3.6, ncols=3)
    data = [(spend, t["x_raw"], GRAY), (z, t["x_z"], GRAY), (lz, t["x_logz"], OK)]
    for ax, (vals, xlabel, color), title in zip(axes, data, t["panels"]):
        ax.hist(vals, bins=50, color=color, zorder=2)
        ax.set_title(title, fontsize=9.8, loc="left", color=INK, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_yticks([])
        ax.set_ylim(0, ax.get_ylim()[1] * 1.3)
        ax.text(0.97, 0.97, f"{t['skew']} = {fmt(skew(vals), t, 2)}", transform=ax.transAxes, ha="right",
                va="top", fontsize=9, color=ACCENT if color == GRAY else OK, fontweight="bold")
        clean_axes(ax)
        ax.spines["left"].set_visible(False)
    axes[0].set_ylabel(t["rows"])
    axes[1].text(0.97, 0.86, t["same_shape"], transform=axes[1].transAxes, ha="right", va="top", fontsize=8.4,
                 color=INK_SOFT)
    fig.text(0.99, 0.01, t["illustrative"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(w_pad=1.6, rect=(0, 0.03, 1, 1))
    save(fig, out, "log-then-scale")


# ─── 2. Escaladores con outliers / scalers with outliers ───────────────────────
def chart_scalers_outliers(t, out):
    rng = np.random.default_rng(9)
    x = np.append(rng.normal(50, 8, 300), 900.0)  # un outlier extremo / one extreme outlier
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    scaled = [
        (x - x.min()) / (x.max() - x.min()),
        (x - x.mean()) / x.std(),
        (x - med) / (q3 - q1),
    ]
    # Eje común de -3 a 3: se ve cuánto espacio deja cada escalador a los datos normales.
    # Common -3..3 axis: shows how much room each scaler leaves for the normal data.
    fig, axes = figure(4.6, nrows=3, sharex=True)
    for ax, vals, name in zip(axes, scaled, t["scalers"]):
        bulk = vals[:-1]
        lo, hi = np.percentile(bulk, [0.5, 99.5])
        jitter = rng.uniform(-0.3, 0.3, bulk.size)
        good = name == t["scalers"][2]
        ax.axvspan(lo, hi, color=OK if good else AMBER, alpha=0.18, lw=0, zorder=1)
        ax.scatter(bulk, jitter, s=6, color=INK_SOFT, alpha=0.6, lw=0, zorder=3)
        ax.plot([3.1], [0], marker=">", color=ACCENT, ms=8, clip_on=False, zorder=4)
        ax.text(1.03, 0.78, t["outlier_at"].format(fmt(vals[-1], t, 1)), transform=ax.transAxes, ha="left",
                va="center", fontsize=8.4, color=ACCENT, fontweight="bold")
        ax.text(1.03, 0.4, t["bulk"].format(fmt(lo, t, 2), fmt(hi, t, 2)), transform=ax.transAxes, ha="left",
                va="center", fontsize=8.4, color=OK if good else INK_SOFT)
        ax.set_xlim(-3.2, 3.2)
        ax.set_ylim(-0.6, 0.6)
        ax.set_yticks([])
        ax.set_title(name, fontsize=9.8, loc="left", color=INK, fontweight="bold", pad=2)
        ax.xaxis.set_major_formatter(lambda v, _: fmt(v, t, 0))
        clean_axes(ax)
        ax.spines["left"].set_visible(False)
    axes[-1].set_xlabel(t["scaled"])
    fig.suptitle(t["sc_title"], fontsize=11, x=0.02, ha="left", fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["illustrative"].split("(")[0].strip(), ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(h_pad=0.8, rect=(0, 0.03, 0.8, 1))
    save(fig, out, "scalers-outliers")


# ─── 3. Estrategias de chunking / chunking strategies ──────────────────────────
def chart_chunking(t, out):
    fig, ax = figure(4.4)
    total = 1500
    topics = [(0, 420), (420, 1060), (1060, 1500)]
    topic_colors = ["#e8f3ed", "#fff6e0", "#f6e3e6"]
    topic_edges = [OK, AMBER, ACCENT]
    rows = {"doc": 4.2, "fixed": 3.05, "hier": 1.75, "sem": 0.45}
    h = 0.55

    ax.set_xlim(-330, total + 20)
    ax.set_ylim(-0.1, 5.0)
    ax.axis("off")

    # Documento con tres temas. Document with three topics.
    for (a, b), fc, ec, name in zip(topics, topic_colors, topic_edges, t["topics"]):
        ax.add_patch(Rectangle((a, rows["doc"]), b - a, h, facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text((a + b) / 2, rows["doc"] + h / 2, name, ha="center", va="center", fontsize=9, color=INK)
    for s in range(60, total, 60):  # oraciones / sentences
        ax.plot([s, s], [rows["doc"], rows["doc"] + 0.1], color=MUTED, lw=0.6)

    labels = [(t["doc"], "doc"), (t["fixed"], "fixed"), (t["hier"], "hier"), (t["sem"], "sem")]
    for text, key in labels:
        ax.text(-20, rows[key] + h / 2, text, ha="right", va="center", fontsize=9.5, color=INK, fontweight="bold")

    # Tamaño fijo con solapamiento. Fixed size with overlap.
    size, ov = 400, 80
    start, k = 0, 0
    while start < total:
        end = min(start + size, total)
        y = rows["fixed"] + (0.18 if k % 2 else 0)
        ax.add_patch(Rectangle((start, y), end - start, h - 0.18, facecolor=SURFACE, edgecolor=INK_SOFT, lw=1))
        if k > 0:
            ax.add_patch(Rectangle((start, rows["fixed"]), ov, h, facecolor=AMBER, alpha=0.45, lw=0))
        start = end - ov if end < total else total
        k += 1
    ax.text(400 - ov / 2, rows["fixed"] - 0.08, t["overlap"], ha="center", va="top", fontsize=7.8, color=INK_SOFT)
    ax.plot([420, 420], [rows["fixed"] - 0.05, rows["fixed"] + h + 0.05], color=ACCENT, lw=1, ls=(0, (2, 2)))
    ax.text(total, rows["fixed"] + h + 0.08, t["cut_ignores"], ha="right", va="bottom", fontsize=7.8, color=ACCENT)

    # Jerárquico: padres grandes, hijos pequeños. Hierarchical: large parents, small children.
    parents = [(0, 750), (750, 1500)]
    for a, b in parents:
        ax.add_patch(Rectangle((a, rows["hier"]), b - a, h, facecolor="white", edgecolor=INK_SOFT, lw=1.3))
    hit = 3
    for i, c in enumerate(range(750, 1500, 150)):
        fc = OK if i == hit else SURFACE
        ax.add_patch(Rectangle((c + 8, rows["hier"] + 0.08), 134, h - 0.16, facecolor=fc, edgecolor=MUTED, lw=0.6))
    for c in range(0, 750, 150):
        ax.add_patch(Rectangle((c + 8, rows["hier"] + 0.08), 134, h - 0.16, facecolor=SURFACE, edgecolor=MUTED,
                               lw=0.6))
    ax.add_patch(Rectangle((750, rows["hier"]), 750, h, facecolor="none", edgecolor=OK, lw=2.2))
    ax.text(1125, rows["hier"] - 0.08, t["child_hit"], ha="center", va="top", fontsize=7.8, color=OK)
    ax.text(375, rows["hier"] - 0.08, t["parent"], ha="center", va="top", fontsize=7.8, color=INK_SOFT)

    # Semántico: corta en los cambios de tema. Semantic: cuts at topic changes.
    for (a, b), ec in zip(topics, topic_edges):
        ax.add_patch(Rectangle((a + 4, rows["sem"]), b - a - 8, h, facecolor=SURFACE, edgecolor=ec, lw=1.4))
    ax.text(total, rows["sem"] - 0.08, t["cut_meaning"], ha="right", va="top", fontsize=7.8, color=INK_SOFT)

    for x in range(0, total + 1, 300):
        ax.text(x, -0.05, str(x), ha="center", va="top", fontsize=7.6, color=MUTED)
    ax.text(total / 2, -0.38, t["tokens"], ha="center", va="top", fontsize=8.6, color=INK_SOFT)
    ax.set_ylim(-0.6, 5.0)
    fig.tight_layout()
    save(fig, out, "chunking-strategies")


CHARTS = [chart_log_then_scale, chart_scalers_outliers, chart_chunking]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
