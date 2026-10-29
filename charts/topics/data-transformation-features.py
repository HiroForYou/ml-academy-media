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
    box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, pct, save,
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
        "ex_title": "Ejemplo: dividir por tiempo y calcular cada feature solo con el pasado",
        "ex_split": "Ordered split por fecha",
        "ex_months": ["ene", "feb", "mar", "abr", "may"],
        "ex_train": "Entrenamiento (hasta marzo)",
        "ex_val": "Validación (abril)",
        "ex_test": "Prueba (mayo)",
        "ex_fit": "el Standard Scaler y el one-hot se ajustan solo aquí",
        "ex_one": "Un ejemplo alrededor de su fecha de corte",
        "ex_days": "Días respecto a la fecha de corte",
        "ex_feat": "sessions_30d: los 30 días hasta el corte",
        "ex_label": "churn_30d: etiqueta de los 30 días siguientes",
        "ex_cut": "corte",
        "ex_leak": "una sesión posterior al corte nunca entra en las features",
        "ex_note": "Caso del ejemplo · fechas ilustrativas",
        "ep_title": "Codifica según el orden y la cardinalidad; PCA resume en pocos componentes",
        "ep_src": "size",
        "ep_blocks": [("One-hot", "sin orden"), ("Ordinal", "con orden"), ("Target", "media del\nobjetivo")],
        "ep_foot": "Muchos valores o texto con errores: similarity encode",
        "ep_pca": "PCA: varianza acumulada",
        "ep_x": "Componentes principales",
        "ep_y": "Varianza acumulada",
        "ep_thr": "umbral 95 %",
        "ep_k": "{k} de {n} componentes",
        "ep_note": "Ilustrativo: datos sintéticos; en el target encoding, la media se calcula solo con entrenamiento",
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
        "ex_title": "Example: split by time and compute every feature from the past only",
        "ex_split": "Ordered split by date",
        "ex_months": ["Jan", "Feb", "Mar", "Apr", "May"],
        "ex_train": "Training (through March)",
        "ex_val": "Validation (April)",
        "ex_test": "Test (May)",
        "ex_fit": "the Standard Scaler and one-hot are fitted here only",
        "ex_one": "One example around its cutoff date",
        "ex_days": "Days relative to the cutoff date",
        "ex_feat": "sessions_30d: the 30 days up to the cutoff",
        "ex_label": "churn_30d: label over the next 30 days",
        "ex_cut": "cutoff",
        "ex_leak": "a session after the cutoff never enters the features",
        "ex_note": "Worked example · illustrative dates",
        "ep_title": "Encode by order and cardinality; PCA summarizes in a few components",
        "ep_src": "size",
        "ep_blocks": [("One-hot", "no order"), ("Ordinal", "with order"), ("Target", "mean of the\ntarget")],
        "ep_foot": "Many values or typo-prone text: similarity encode",
        "ep_pca": "PCA: cumulative variance",
        "ep_x": "Principal components",
        "ep_y": "Cumulative variance",
        "ep_thr": "95% threshold",
        "ep_k": "{k} of {n} components",
        "ep_note": "Illustrative: synthetic data; in target encoding, the mean is computed on training data only",
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


# ─── 4. Línea de tiempo del ejemplo / the worked example's timeline ────────────
def chart_example_timeline(t, out):
    fig, (a1, a2) = figure(4.4, nrows=2, gridspec_kw={"height_ratios": [1, 1.25]})
    # Meses de ene a may (días desde el 1 de enero). Months Jan to May (days since Jan 1).
    edges = [0, 31, 59, 90, 120, 151]
    bands = [(0, 90, t["ex_train"], OK), (90, 120, t["ex_val"], AMBER), (120, 151, t["ex_test"], GRAY)]
    for x0, x1, label, color in bands:
        a1.barh(0, x1 - x0, left=x0, height=0.5, color=color, edgecolor="white", lw=2)
        a1.text((x0 + x1) / 2, 0, label, ha="center", va="center", fontsize=8.8,
                color="white" if color == OK else INK, fontweight="bold")
    fit_to(a1.text(45, -0.55, t["ex_fit"], ha="center", va="top", fontsize=8.6, color=OK), 88)
    a1.set_xlim(0, 151)
    a1.set_ylim(-1.15, 0.5)
    a1.set_yticks([])
    a1.set_xticks([(a + b) / 2 for a, b in zip(edges, edges[1:])])
    a1.set_xticklabels(t["ex_months"])
    a1.tick_params(axis="x", length=0)
    a1.set_title(t["ex_split"], fontsize=9.8, loc="left", color=INK, fontweight="bold")
    clean_axes(a1)
    a1.spines["left"].set_visible(False)

    a2.barh(1, 30, left=-30, height=0.42, color=OK)
    a2.text(-15, 1.38, t["ex_feat"], ha="center", va="bottom", fontsize=8.6, color=OK)
    a2.barh(0, 30, left=0, height=0.42, color=INK_SOFT)
    a2.text(15, -0.38, t["ex_label"], ha="center", va="top", fontsize=8.6, color=INK_SOFT)
    a2.axvline(0, color=ACCENT, lw=1.4, ls=(0, (3, 2)))
    a2.text(0.8, 2.0, t["ex_cut"], color=ACCENT, fontsize=8.8, va="center", fontweight="bold")
    a2.scatter([9], [1], marker="x", s=60, color=ACCENT, zorder=4, lw=2)
    a2.annotate(t["ex_leak"], xy=(9.5, 1), xytext=(13, 1), fontsize=8.4, color=ACCENT, va="center",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    a2.set_xlim(-34, 34)
    a2.set_ylim(-1.0, 2.35)
    a2.set_yticks([])
    a2.set_xticks(range(-30, 31, 10))
    a2.set_xlabel(t["ex_days"], fontsize=9)
    a2.set_title(t["ex_one"], fontsize=9.8, loc="left", color=INK, fontweight="bold")
    clean_axes(a2)
    a2.spines["left"].set_visible(False)

    fig.suptitle(t["ex_title"], x=0.01, ha="left", fontsize=10.6, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["ex_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1), h_pad=1.4)
    save(fig, out, "example-timeline")


# ─── 5. Codificación y PCA / encoding and PCA ──────────────────────────────────
def chart_encoding_pca(t, out):
    fig, axes = figure(4.1, ncols=2, gridspec_kw={"width_ratios": [1.3, 1]})
    ax, pc = axes
    diagram_axes(ax, 9.7, 8)
    cw, ch = 1.35, 0.9
    src, onehot_x, ord_x, tgt_x = 0.1, 1.95, 6.4, 8.15
    rows = ["S", "M", "L", "M"]
    cats = ["S", "M", "L"]
    ys = [5.0 - i * 1.0 for i in range(4)]  # centros de fila / row centres

    def cell(x, y, text, fill=SURFACE, color=INK, weight="normal", edge=RULE):
        box(ax, x, y - ch / 2, cw - 0.1, ch, "", edge=edge, fill=fill)
        ax.text(x + (cw - 0.1) / 2, y, text, ha="center", va="center", fontsize=9, color=color, fontweight=weight,
                zorder=3)

    ax.text(src + (cw - 0.1) / 2, 6.1, t["ep_src"], ha="center", va="center", fontsize=8.6, color=MUTED)
    for y, v in zip(ys, rows):
        cell(src, y, v, fill="white", edge=INK_SOFT, weight="bold")

    # One-hot: una columna por valor / one column per value
    ax.text(onehot_x + 1.5 * cw - 0.05, 7.55, t["ep_blocks"][0][0], ha="center", va="center", fontsize=9.8,
            fontweight="bold", color=INK)
    ax.text(onehot_x + 1.5 * cw - 0.05, 7.0, t["ep_blocks"][0][1], ha="center", va="top", fontsize=8.2,
            color=MUTED)
    for j, c in enumerate(cats):
        ax.text(onehot_x + j * cw + (cw - 0.1) / 2, 6.1, c, ha="center", va="center", fontsize=8.6, color=MUTED)
        for y, v in zip(ys, rows):
            on = v == c
            cell(onehot_x + j * cw, y, "1" if on else "0", fill="#f7e1e5" if on else SURFACE,
                 color=ACCENT if on else MUTED, weight="bold" if on else "normal",
                 edge=ACCENT if on else RULE)

    # Ordinal y target / ordinal and target
    order = {"S": 0, "M": 1, "L": 2}
    mean = {"S": 0.40, "M": 0.25, "L": 0.10}
    for (title, cue), bx, fn in ((t["ep_blocks"][1], ord_x, lambda v: str(order[v])),
                                 (t["ep_blocks"][2], tgt_x, lambda v: fmt(mean[v], t, 2))):
        ax.text(bx + (cw - 0.1) / 2, 7.55, title, ha="center", va="center", fontsize=9.8, fontweight="bold",
                color=INK)
        ax.text(bx + (cw - 0.1) / 2, 7.0, cue, ha="center", va="top", fontsize=8.2, color=MUTED,
                multialignment="center")
        for y, v in zip(ys, rows):
            cell(bx, y, fn(v))
    foot = ax.text(0.1, 0.55, t["ep_foot"], ha="left", va="center", fontsize=8.4, color=INK_SOFT)
    fit_to(foot, 9.4)

    # PCA: varianza acumulada con umbral del 95 % / cumulative variance with the 95 % threshold
    n = 40
    var = 0.78 ** np.arange(n)
    cum = np.cumsum(var / var.sum())
    kstar = int(np.argmax(cum >= 0.95)) + 1
    comps = np.arange(1, n + 1)
    pc.plot(comps, cum, color=INK_SOFT, lw=1.8, zorder=2)
    pc.axhline(0.95, color=ACCENT, lw=1.1, ls=(0, (4, 3)), zorder=1)
    pc.plot([kstar, kstar], [0, cum[kstar - 1]], color=ACCENT, lw=1.1, ls=":", zorder=1)
    pc.scatter([kstar], [cum[kstar - 1]], s=46, color=ACCENT, zorder=4)
    pc.text(1.5, 0.965, t["ep_thr"], fontsize=8.4, color=ACCENT, va="bottom", ha="left")
    pc.text(kstar + 1.6, 0.62, t["ep_k"].format(k=kstar, n=n), fontsize=8.8, color=ACCENT, fontweight="bold",
            va="center", ha="left")
    pc.set_xlim(1, n)
    pc.set_ylim(0, 1.08)
    pc.set_xlabel(t["ep_x"], fontsize=9)
    pc.set_ylabel(t["ep_y"], fontsize=9)
    pc.yaxis.set_major_formatter(lambda v, _: pct(v * 100, t, 0))
    pc.set_title(t["ep_pca"], fontsize=10, loc="left", color=INK, fontweight="bold")
    pc.grid(True, color=RULE, lw=0.6, zorder=0)
    clean_axes(pc)

    fig.suptitle(t["ep_title"], x=0.01, ha="left", fontsize=10.6, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["ep_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94), w_pad=1.6)
    save(fig, out, "encoding-pca")


CHARTS = [chart_log_then_scale, chart_scalers_outliers, chart_chunking, chart_example_timeline, chart_encoding_pca]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
