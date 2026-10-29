"""
Tema 2.1: elegir el enfoque de modelado. Topic 2.1: choosing a modeling approach.

    python charts/topics/modeling-approaches.py --lang es --out <dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    arrow, box, clean_axes, cli, diagram_axes, figure, fmt, save,
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
    },
}


# ─── 1. Elegir la capa / choose the layer ──────────────────────────────────────
def chart_choose_layer(t, out):
    fig, ax = figure(4.6)
    diagram_axes(ax, 12, 6.2)
    ax.text(0.1, 5.85, t["title"], fontsize=11.5, fontweight="bold", color=INK, va="center")
    ys = [4.45, 2.75, 1.05]
    edges = [OK, INK_SOFT, ACCENT]
    for i, (y, q, a, note, edge) in enumerate(zip(ys, t["q"], t["a"], t["notes"], edges)):
        box(ax, 0.1, y - 0.55, 4.2, 1.1, q, edge=RULE, fill=SURFACE, size=8.6)
        box(ax, 5.4, y - 0.55, 5.6, 1.1, a, edge=edge, fill="white", size=8.8, lw=1.6)
        ax.text(5.5, y - 0.75, note, fontsize=7.8, color=MUTED, va="top")
        arrow(ax, (4.35, y), (5.35, y), color=edge, lw=1.5)
        if i < 2:
            ax.text(4.85, y + 0.12, t["yes"], ha="center", va="bottom", fontsize=8.4, color=INK_SOFT)
            arrow(ax, (2.2, y - 0.6), (2.2, ys[i + 1] + 0.6), color=MUTED)
            ax.text(2.32, (y + ys[i + 1]) / 2, t["no"], va="center", fontsize=8.4, color=INK_SOFT)
    # Eje de control y esfuerzo. Control and effort axis.
    arrow(ax, (11.5, 4.9), (11.5, 0.6), color=INK_SOFT, lw=1.3)
    ax.text(11.75, 2.75, t["axis"], rotation=-90, va="center", ha="center", fontsize=8.4, color=INK_SOFT)
    fig.tight_layout(pad=0.4)
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


CHARTS = [chart_choose_layer, chart_distillation]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
