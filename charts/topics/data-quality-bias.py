"""
Tema 1.3: los gráficos de sesgo y desbalance viven en charts/make_charts.py; este módulo los expone al
descubrimiento y añade el flujo de reglas de calidad de datos.
Topic 1.3: the bias and imbalance charts live in charts/make_charts.py; this module exposes them to discovery
and adds the data quality rules flow.

    python charts/topics/data-quality-bias.py --lang es --out <dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from make_charts import CHARTS as BIAS_CHARTS, TEXT as BIAS_TEXT  # noqa: E402
from style import (  # noqa: E402
    ACCENT, INK, INK_SOFT, MUTED, RULE, SURFACE, WIDTH_IN, DPI,
    arrow, box, cli, diagram_axes, fit_to, icon_node, plt, save,
)

FLOW_TEXT = {
    "es": {
        "dq_title": "Cuando una regla falla: detener, aislar o avisar",
        "dq_data": "Dataset\nen el trabajo ETL",
        "dq_rules": "Reglas DQDL\nrecomendadas o propias",
        "dq_eval": "Evaluate Data Quality\nscore + resultado por regla",
        "dq_situations": ["Lote entero roto", "Pocas filas malas", "Cambio sin regla"],
        "dq_actions": ["Fallar sin cargar el destino", "Marcar filas: las Failed a cuarentena",
                       "Anomalías y alertas"],
        "dq_note": "Acciones del transform en una ejecución de Glue · diagrama, no a escala",
    },
    "en": {
        "dq_title": "When a rule fails: stop, isolate or alert",
        "dq_data": "Dataset\nin the ETL job",
        "dq_rules": "DQDL rules\nrecommended or your own",
        "dq_eval": "Evaluate Data Quality\nscore + result per rule",
        "dq_situations": ["Whole batch broken", "A few bad rows", "Change with no rule"],
        "dq_actions": ["Fail without loading the target", "Flag rows: send Failed to quarantine",
                       "Anomalies and alerts"],
        "dq_note": "Transform actions in a Glue run · diagram, not to scale",
    },
}

TEXT = {lang: {**BIAS_TEXT[lang], **FLOW_TEXT[lang]} for lang in BIAS_TEXT}


# ─── Flujo de Glue Data Quality / Glue Data Quality flow ───────────────────────
def chart_dq_rules_flow(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.8), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.07)  # antes de los íconos / before icons
    diagram_axes(ax, 16, 8.4)
    node = dict(edge=RULE, fill=SURFACE, size=9.4, desc_size=8.4)
    gap = 0.08
    # Entrada: dataset y reglas llegan al transform. Input: dataset and rules reach the transform.
    icon_node(ax, 0.2, 3.1, 3.7, 2.0, "aws/s3", t["dq_data"], **node)
    icon_node(ax, 4.7, 6.0, 4.7, 1.9, "aws/glue-data-quality", t["dq_rules"], **node)
    icon_node(ax, 4.7, 3.0, 4.7, 2.2, "aws/glue-data-quality", t["dq_eval"], edge=ACCENT, fill="white", size=9.4,
              desc_size=8.4, lw=1.8)
    arrow(ax, (3.9 + gap, 4.1), (4.7 - gap, 4.1), color=INK_SOFT)
    arrow(ax, (7.05, 6.0 - gap), (7.05, 5.2 + gap), color=INK_SOFT)

    # Salida: tres acciones según la situación. Output: three actions by situation.
    x, w, h = 10.8, 5.0, 1.5
    ys = [6.05, 3.45, 0.85]
    for y, situation, action, hit in zip(ys, t["dq_situations"], t["dq_actions"], (True, False, False)):
        box(ax, x, y, w, h, action, edge=ACCENT if hit else INK_SOFT, fill="white", size=9.2,
            color=ACCENT if hit else INK, weight="bold" if hit else "normal", lw=1.6 if hit else 1.2)
        fit_to(ax.text(x, y + h + 0.12, situation, ha="left", va="bottom", fontsize=8.8, color=MUTED), w)
        arrow(ax, (9.4 + gap, 4.1), (x - gap, y + h / 2), color=ACCENT if hit else INK_SOFT)
    ax.set_title(t["dq_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.015, t["dq_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "dq-rules-flow")


CHARTS = [*BIAS_CHARTS, chart_dq_rules_flow]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
