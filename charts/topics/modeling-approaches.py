"""
Tema 2.1: elegir el enfoque de modelado. Topic 2.1: choosing a modeling approach.

    python charts/topics/modeling-approaches.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import Ellipse, Patch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, icon_node, place_icon, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "q": [
            "¿Una API ya resuelve la tarea?\n(OCR, imágenes, sentimiento, voz)",
            "¿La salida es generativa?\n(texto libre, resumen, chat)",
            "Datos propios etiquetados\ny una métrica clara",
        ],
        "a": [
            "Servicio de IA\nTextract · Rekognition · Comprehend · Transcribe",
            "Amazon Bedrock\nprompt → RAG → fine-tuning o distillation",
            "Amazon SageMaker AI\nalgoritmos integrados · JumpStart · script propio",
        ],
        "notes": [
            "sin experiencia en ML; personalización limitada",
            "FM gestionado; pago por uso",
            "máximo control; más esfuerzo de datos y operación",
        ],
        "yes": "sí",
        "no": "no",
        "axis": "más control, más esfuerzo",
        "title": "Elige la capa más simple que cumpla el requisito",
        "latency": "Latencia p95 (s)",
        "quality": "Correctness en la evaluación RAG (ilustrativo)",
        "teacher": "Teacher (modelo grande)",
        "student": "Student destilado",
        "req": "Requisito: < 3 s",
        "ok_zone": "cumple latencia",
        "drop": "−1 punto de calidad",
        "faster": "p95: 5 s → 1,8 s",
        "dist_title": "Model Distillation con invocation logs: misma evaluación, antes y después",
        "am_title": "Primero el tipo de problema; el algoritmo integrado sale de ahí",
        "am_start": "punto de partida",
        "am_rows": [
            ("Tabla con etiqueta", [("XGBoost", ""), ("LightGBM", ""), ("CatBoost", ""), ("AutoGluon-Tabular", ""), ("TabTransformer", "")]),
            ("Tabla: casos especiales", [("Linear Learner", "explicable"), ("Factorization Machines", "datos dispersos"), ("k-NN", "vecinos")]),
            ("Series de tiempo", [("DeepAR", "cientos de series")]),
            ("Sin etiqueta: agrupar o reducir", [("K-Means", "agrupar"), ("PCA", "reducir columnas")]),
            ("Anomalías", [("Random Cut Forest", "sensores"), ("IP Insights", "IP inusual")]),
            ("Texto y objetos", [("BlazingText", "clasificar"), ("Seq2Seq", "traducir"), ("Object2Vec", "embeddings"), ("LDA", "temas"), ("NTM", "temas")]),
            ("Imágenes", [("Image Classification", "etiqueta"), ("Object Detection", "cajas"), ("Semantic Segmentation", "píxeles")]),
        ],
        "sp_title": "Temperature redistribuye la probabilidad; top-k y top-p recortan candidatos",
        "sp_panels": ["Temperature", "Top-k = 2", "Top-p = 0,7"],
        "sp_subs": [
            "T baja afila la distribución; T alta la aplana",
            "Solo sobreviven los k más probables",
            "Se conservan los más probables hasta sumar p",
        ],
        "sp_low": "T = 0,5",
        "sp_high": "T = 2",
        "sp_keep": "se conserva",
        "sp_cut": "se descarta",
        "sp_prob": "Probabilidad",
        "sp_note": "Ilustrativo: distribución base con temperature 1",
    },
    "en": {
        "decimal": ".",
        "q": [
            "Does an API already solve the task?\n(OCR, images, sentiment, speech)",
            "Is the output generative?\n(free text, summary, chat)",
            "Your own labeled data\nand a clear metric",
        ],
        "a": [
            "AI service\nTextract · Rekognition · Comprehend · Transcribe",
            "Amazon Bedrock\nprompt → RAG → fine-tuning or distillation",
            "Amazon SageMaker AI\nbuilt-in algorithms · JumpStart · your own script",
        ],
        "notes": [
            "no ML expertise; limited customization",
            "managed FM; pay per use",
            "maximum control; more data and operations work",
        ],
        "yes": "yes",
        "no": "no",
        "axis": "more control, more effort",
        "title": "Pick the simplest layer that meets the requirement",
        "latency": "p95 latency (s)",
        "quality": "Correctness in the RAG evaluation (illustrative)",
        "teacher": "Teacher (large model)",
        "student": "Distilled student",
        "req": "Requirement: < 3 s",
        "ok_zone": "meets latency",
        "drop": "−1 quality point",
        "faster": "p95: 5 s → 1.8 s",
        "dist_title": "Model Distillation from invocation logs: same evaluation, before and after",
        "am_title": "Start with the problem type; the built-in algorithm follows",
        "am_start": "starting point",
        "am_rows": [
            ("Labeled table", [("XGBoost", ""), ("LightGBM", ""), ("CatBoost", ""), ("AutoGluon-Tabular", ""), ("TabTransformer", "")]),
            ("Table: special cases", [("Linear Learner", "explainable"), ("Factorization Machines", "sparse data"), ("k-NN", "neighbors")]),
            ("Time series", [("DeepAR", "hundreds of series")]),
            ("No labels: group or reduce", [("K-Means", "cluster"), ("PCA", "reduce columns")]),
            ("Anomalies", [("Random Cut Forest", "sensors"), ("IP Insights", "unusual IP")]),
            ("Text and objects", [("BlazingText", "classify"), ("Seq2Seq", "translate"), ("Object2Vec", "embeddings"), ("LDA", "topics"), ("NTM", "topics")]),
            ("Images", [("Image Classification", "label"), ("Object Detection", "boxes"), ("Semantic Segmentation", "pixels")]),
        ],
        "sp_title": "Temperature reshapes the probabilities; top-k and top-p cut candidates",
        "sp_panels": ["Temperature", "Top-k = 2", "Top-p = 0.7"],
        "sp_subs": [
            "Low T sharpens it; high T flattens it",
            "Only the k most likely survive",
            "Keep the most likely until they add up to p",
        ],
        "sp_low": "T = 0.5",
        "sp_high": "T = 2",
        "sp_keep": "kept",
        "sp_cut": "discarded",
        "sp_prob": "Probability",
        "sp_note": "Illustrative: base distribution at temperature 1",
    },
}


# ─── 1. Elegir la capa / choose the layer ──────────────────────────────────────
def chart_choose_layer(t, out):
    fig, ax = figure(4.6)
    # Márgenes fijos antes de los íconos (no tight_layout). Fixed margins before the icons (no tight_layout).
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    diagram_axes(ax, 12, 6.2)
    ax.text(0.1, 5.85, t["title"], fontsize=11.5, fontweight="bold", color=INK, va="center")
    ys = [4.45, 2.75, 1.05]
    edges = [OK, INK_SOFT, ACCENT]
    icons = [["aws/textract", "aws/rekognition", "aws/comprehend", "aws/transcribe"], "aws/bedrock", "aws/sagemaker-ai"]
    for i, (y, q, a, note, edge) in enumerate(zip(ys, t["q"], t["a"], t["notes"], edges)):
        box(ax, 0.1, y - 0.55, 4.2, 1.1, q, edge=RULE, fill=SURFACE, size=8.6)
        icon_node(ax, 5.4, y - 0.55, 5.6, 1.1, icons[i], a, edge=edge, fill="white", size=9, desc_size=8.2, lw=1.6)
        ax.text(5.5, y - 0.75, note, fontsize=7.8, color=MUTED, va="top")
        arrow(ax, (4.35, y), (5.35, y), color=edge, lw=1.5)
        if i < 2:
            ax.text(4.85, y + 0.12, t["yes"], ha="center", va="bottom", fontsize=8.4, color=INK_SOFT)
            arrow(ax, (2.2, y - 0.6), (2.2, ys[i + 1] + 0.6), color=MUTED)
            ax.text(2.32, (y + ys[i + 1]) / 2, t["no"], va="center", fontsize=8.4, color=INK_SOFT)
    # Eje de control y esfuerzo. Control and effort axis.
    arrow(ax, (11.5, 4.9), (11.5, 0.6), color=INK_SOFT, lw=1.3)
    ax.text(11.75, 2.75, t["axis"], rotation=-90, va="center", ha="center", fontsize=8.4, color=INK_SOFT)
    save(fig, out, "choose-layer")


# ─── 2. Distillation: calidad vs latencia / quality vs latency ─────────────────
def chart_distillation(t, out):
    fig, ax = figure(4.2)
    teacher = (5.0, 0.86)
    student = (1.8, 0.85)
    ax.axvspan(0, 3, color=OK, alpha=0.07, lw=0, zorder=0)
    ax.axvline(3, color=INK, lw=1, ls=(0, (4, 3)))
    ax.text(2.92, 0.905, t["req"], ha="right", va="top", fontsize=8.8, color=INK)
    ax.text(0.12, 0.905, t["ok_zone"], ha="left", va="top", fontsize=8.4, color=OK)
    ax.scatter(*teacher, s=160, color=GRAY, edgecolor=INK_SOFT, zorder=3)
    ax.scatter(*student, s=160, color=OK, zorder=3)
    ax.annotate("", xy=(student[0] + 0.12, student[1]), xytext=(teacher[0] - 0.12, teacher[1]),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4, connectionstyle="arc3,rad=0.15"))
    ax.text(teacher[0], teacher[1] + 0.012, t["teacher"], ha="center", fontsize=9, color=INK, fontweight="bold")
    ax.text(student[0], student[1] - 0.016, t["student"], ha="center", va="top", fontsize=9, color=OK,
            fontweight="bold")
    ax.text(3.5, 0.833, f"{t['faster']}\n{t['drop']}", ha="center", va="top", fontsize=8.8, color=ACCENT)
    ax.set_xlim(0, 6)
    ax.set_ylim(0.78, 0.91)
    ax.set_xlabel(t["latency"])
    ax.set_ylabel(t["quality"], fontsize=9)
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 2))
    ax.xaxis.set_major_formatter(lambda v, _: fmt(v, t, 0))
    ax.set_title(t["dist_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.grid(True, color=RULE, lw=0.6, zorder=0)
    clean_axes(ax)
    fig.tight_layout()
    save(fig, out, "distillation-tradeoff")


# ─── 3. Mapa de algoritmos integrados / built-in algorithm map ─────────────────
def _text_width(ax, text, size, weight="normal"):
    """Ancho de un texto en unidades de datos del eje. Width of a text in the axes' data units."""
    r = ax.figure.canvas.get_renderer()
    tx = ax.text(0, 0, text, fontsize=size, fontweight=weight)
    w = tx.get_window_extent(r).width
    tx.remove()
    (x0, _), (x1, _) = ax.transData.inverted().transform([(0, 0), (w, 0)])
    return abs(x1 - x0)


def _glyph(ax, kind, cx, cy, w=0.82, h=0.62):
    """Icono mínimo del tipo de problema, centrado en (cx, cy). Minimal glyph of the problem type."""
    x0, y0 = cx - w / 2, cy - h / 2
    if kind in ("table", "sparse"):
        cw, ch = w / 3.3, h / 3.3
        filled = {(0, 1), (1, 2), (2, 0)}
        for r in range(3):
            for c in range(3):
                label_col = kind == "table" and c == 2
                if kind == "table":
                    fc = ACCENT if label_col else GRAY
                else:
                    fc = INK_SOFT if (r, c) in filled else "white"
                ax.add_patch(Rectangle((x0 + c * (cw + 0.05), y0 + (2 - r) * (ch + 0.05)), cw, ch, facecolor=fc,
                                       edgecolor=GRAY if fc == "white" else fc, linewidth=0.8, zorder=3))
    elif kind == "series":
        xs = np.linspace(0, 1, 40)
        ys = 0.5 + 0.28 * np.sin(xs * 9) + 0.25 * xs
        k = 28
        ax.plot(x0 + xs[:k] * w, y0 + ys[:k] * h * 0.95, color=INK_SOFT, lw=1.6, zorder=3)
        ax.plot(x0 + xs[k - 1:] * w, y0 + ys[k - 1:] * h * 0.95, color=MUTED, lw=1.4, ls=(0, (2, 2)), zorder=3)
    elif kind == "cluster":
        rng = np.random.default_rng(3)
        for (gx, gy), col in (((0.27, 0.55), INK_SOFT), ((0.74, 0.42), GRAY)):
            pts = rng.normal(0, 0.085, (7, 2)) + (gx, gy)
            ax.scatter(x0 + pts[:, 0] * w, y0 + pts[:, 1] * h, s=16, color=col, zorder=4, linewidths=0)
            ax.add_patch(Ellipse((x0 + gx * w, y0 + gy * h), w * 0.5, h * 0.72, fill=False, edgecolor=col, lw=0.9,
                                 ls=(0, (2, 2)), zorder=3))
    elif kind == "anomaly":
        ax.add_patch(Rectangle((x0, y0 + h * 0.18), w, h * 0.42, facecolor=RULE, edgecolor="none", zorder=2))
        xs = np.linspace(0, 1, 30)
        ax.plot(x0 + xs * w, y0 + h * (0.39 + 0.12 * np.sin(xs * 12)), color=INK_SOFT, lw=1.3, zorder=3)
        ax.scatter([x0 + 0.68 * w], [y0 + h * 0.92], s=26, color=ACCENT, zorder=4, linewidths=0)
    elif kind == "text":
        for i, frac in enumerate((1.0, 0.82, 0.92, 0.55)):
            yy = y0 + h * (0.9 - i * 0.28)
            ax.plot([x0, x0 + w * frac], [yy, yy], color=INK_SOFT if i < 3 else GRAY, lw=2.0, solid_capstyle="round",
                    zorder=3)
    elif kind == "image":
        ax.add_patch(Rectangle((x0, y0), w, h, facecolor="white", edgecolor=INK_SOFT, lw=1.2, zorder=3))
        ax.fill([x0 + 0.08 * w, x0 + 0.38 * w, x0 + 0.62 * w, x0 + 0.78 * w, x0 + 0.92 * w, x0 + 0.08 * w],
                [y0 + 0.1 * h, y0 + 0.62 * h, y0 + 0.3 * h, y0 + 0.5 * h, y0 + 0.1 * h, y0 + 0.1 * h],
                color=GRAY, zorder=4)
        ax.scatter([x0 + 0.76 * w], [y0 + 0.78 * h], s=14, color=INK_SOFT, zorder=4, linewidths=0)


GLYPHS = ["table", "sparse", "series", "cluster", "anomaly", "text", "image"]


def chart_algorithm_map(t, out):
    fig, ax = figure(5.0)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    diagram_axes(ax, 12, 9.0)
    ax.text(0.1, 8.65, t["am_title"], fontsize=11.5, fontweight="bold", color=INK, va="center")
    # Los algoritmos integrados son de SageMaker AI. The built-in algorithms belong to SageMaker AI.
    place_icon(ax, "aws/sagemaker-ai", 11.62, 8.65, 0.62)
    ax.text(11.25, 8.65, "SageMaker AI", ha="right", va="center", fontsize=8.6, color=MUTED, fontweight="bold")
    pitch, h, label_w, gap = 1.12, 0.86, 3.4, 0.16
    x_chip0 = 0.1 + label_w + 0.42

    def chip_cue(name, cue):
        return t["am_start"] if name == "XGBoost" else cue

    # Relleno de los chips: el más ancho que deje la fila más larga dentro del lienzo.
    # Chip padding: the widest that keeps the longest row inside the canvas.
    pad = 0.4
    while pad > 0.2:
        ends = []
        for _, chips in t["am_rows"]:
            xx = x_chip0
            for name, cue in chips:
                c = chip_cue(name, cue)
                xx += max(_text_width(ax, name, 8.6, "bold"), _text_width(ax, c, 7.4) if c else 0) + pad + gap
            ends.append(xx - gap)
        if max(ends) <= 11.9:
            break
        pad -= 0.02

    for i, (label, chips) in enumerate(t["am_rows"]):
        y = 7.6 - i * pitch
        box(ax, 0.1, y - h / 2, label_w, h, "", edge=ACCENT, fill="white", lw=1.5)
        _glyph(ax, GLYPHS[i], 0.1 + 0.62, y)
        lt = ax.text(0.1 + 1.2 + (label_w - 1.2 - 0.12) / 2, y, label, ha="center", va="center", fontsize=8.8,
                     fontweight="bold", color=INK, zorder=3, multialignment="center")
        fit_to(lt, label_w - 1.2 - 0.2, h - 0.14)
        arrow(ax, (0.1 + label_w, y), (x_chip0 - 0.08, y), color=ACCENT, lw=1.4)
        x = x_chip0
        for name, cue in chips:
            c = chip_cue(name, cue)
            key = name == "XGBoost"
            w = max(_text_width(ax, name, 8.6, "bold"), _text_width(ax, c, 7.4) if c else 0) + pad
            box(ax, x, y - h / 2, w, h, "", edge=ACCENT if key else RULE, fill="white" if key else SURFACE,
                lw=1.6 if key else 1.3)
            ax.text(x + w / 2, y + (0.15 if c else 0), name, ha="center", va="center", fontsize=8.6,
                    fontweight="bold", color=INK, zorder=3)
            if c:
                ax.text(x + w / 2, y - 0.2, c, ha="center", va="center", fontsize=7.4,
                        color=ACCENT if key else MUTED, fontweight="bold" if key else "normal", zorder=3)
            x += w + gap
    save(fig, out, "algorithm-map")


# ─── 4. Parámetros de muestreo / sampling parameters ───────────────────────────
def chart_sampling_params(t, out):
    toks = ["horses", "zebras", "unicorns"]
    base = np.array([0.7, 0.2, 0.1])

    def temp(T):
        p = base ** (1 / T)
        return p / p.sum()

    fig, axes = figure(3.9, ncols=3, sharey=True)
    x = np.arange(3)
    for k, ax in enumerate(axes):
        ax.set_title(t["sp_panels"][k], fontsize=10, loc="left", color=INK, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(toks, fontsize=8.6)
        ax.set_ylim(0, 1.32)
        ax.set_xlim(-0.55, 2.55)
        ax.set_yticks([0, 0.5, 1])
        ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
        ax.grid(True, axis="y", color=RULE, lw=0.6, zorder=0)
        clean_axes(ax)
        sub = ax.text(-0.5, 1.3, t["sp_subs"][k], fontsize=8.2, color=INK_SOFT, va="top", ha="left")
        fit_to(sub, 3.0, 0.3)
    axes[0].set_ylabel(t["sp_prob"], fontsize=9)

    a = axes[0]
    w = 0.36
    a.bar(x - w / 2, temp(0.5), w, color=ACCENT, zorder=2, label=t["sp_low"])
    a.bar(x + w / 2, temp(2), w, color=GRAY, zorder=2, label=t["sp_high"])
    a.legend(loc="upper right", bbox_to_anchor=(1.0, 0.72), frameon=False, fontsize=8.4, handlelength=1.2)

    for ax, keep in ((axes[1], [True, True, False]), (axes[2], [True, False, False])):
        for xi, (v, kp) in enumerate(zip(base, keep)):
            ax.bar(xi, v, 0.55, color=OK if kp else GRAY, alpha=1 if kp else 0.55, zorder=2)
            ax.text(xi, v + 0.03, fmt(v, t, 1), ha="center", va="bottom", fontsize=8.6,
                    color=INK if kp else MUTED, fontweight="bold" if kp else "normal")
    axes[2].legend(handles=[Patch(color=OK, label=t["sp_keep"]), Patch(color=GRAY, alpha=0.55, label=t["sp_cut"])],
                   loc="upper right", bbox_to_anchor=(1.0, 0.72), frameon=False, fontsize=8.4, handlelength=1.2)

    fig.suptitle(t["sp_title"], x=0.01, ha="left", fontsize=10.6, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["sp_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94), w_pad=1.2)
    save(fig, out, "sampling-params")


CHARTS = [chart_choose_layer, chart_distillation, chart_algorithm_map, chart_sampling_params]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
