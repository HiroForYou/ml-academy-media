"""
Tema 3.3: MLOps y CI/CD. Topic 3.3: MLOps and CI/CD.

    python charts/topics/mlops-cicd.py --lang es --out <dir>
"""

import sys
from pathlib import Path

from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, icon_node, place_icon, plt, save,
)

TEXT = {
    "es": {
        "minutes": "Minutos desde UpdateEndpoint",
        "share": "Tráfico en la flota nueva (%)",
        "all": "Blue/green all at once",
        "canary": "Blue/green canary (10 %)",
        "linear": "Blue/green linear (4 pasos)",
        "rolling": "Rolling (lotes de capacidad)",
        "bake": "baking period",
        "wait": "espera",
        "alarm": "alarma → auto-rollback",
        "ok_path": "sin alarmas",
        "rolling_note": "no duplica la flota",
        "shift_title": "Deployment guardrails: cuánto tráfico pasa a la flota nueva y cuándo",
        "shift_note": "Ilustrativo: tamaños y tiempos configurables; el rollback necesita alarmas de CloudWatch",
        "week": "Semana",
        "pending": "PendingManualApproval",
        "approved": "Approved",
        "rejected": "Rejected",
        "prod": "En producción",
        "fail": "AUC < 0,82: FailStep,\nno se registra",
        "pipeline": "Ejecuciones",
        "redeploy": "v3 → Rejected:\nvuelve v1",
        "reg_title": "Model Registry: solo una versión Approved llega a producción, y rechazarla la revierte",
        "reg_note": "Ilustrativo; con la plantilla de SageMaker Projects, rechazar la versión vigente redespliega la última Approved",
        "rg_start": "EventBridge\nlunes 6:00",
        "rg_gates": [
            ("QualityCheck", "datos frente a la baseline"),
            ("ConditionStep", "AUC ≥ 0,82 y mejor que producción"),
            ("Aprobación", "Approved + prueba de humo + manual"),
            ("Canary 10 %", "10 min con alarmas"),
        ],
        "rg_runs": ["Ejecución 1", "Ejecución 2", "Ejecución 3"],
        "rg_stop1": "datos malos: el paso falla, no se entrena",
        "rg_stop2": "AUC bajo el umbral: FailStep, no se registra",
        "rg_prod": "Producción",
        "rg_late": "Días después",
        "rg_late1": "versión nueva en producción",
        "rg_rej": "Rejected",
        "rg_late2": "se redespliega la última Approved",
        "gates_title": "Cada puerta frena un fallo distinto: solo la ejecución 3 llega a producción",
        "gates_note": "Tres ejecuciones de ejemplo; el rollback por Rejected usa la plantilla de SageMaker Projects",
        "gc_title": "Prompts y documentos cambian por separado, pero ambos pasan por una evaluación antes de aceptarse",
        "gc_tag1": "Cambia el prompt, el agente o el modelo",
        "gc_tag2": "Cambian los documentos de la knowledge base",
        "gc_change": "Cambio\nprompt o código",
        "gc_pm": "Prompt Management\nversión nueva",
        "gc_ev": "Bedrock Evaluations\nprueba de regresión",
        "gc_gate": "Puerta\numbral de calidad",
        "gc_dep": "Despliegue\nversión del agente",
        "gc_rb": "Rollback: apuntar producción a la versión anterior",
        "gc_docs": "Documentos\nnuevos o editados",
        "gc_ing": "Sincronización\nStartIngestionJob\nhasta COMPLETE",
        "gc_rag": "Evaluación RAG\nrecuperación y respuesta",
        "gc_ok": "Se acepta la actualización",
        "gc_note": "Esquema simplificado del pipeline",
    },
    "en": {
        "minutes": "Minutes since UpdateEndpoint",
        "share": "Traffic on the new fleet (%)",
        "all": "Blue/green all at once",
        "canary": "Blue/green canary (10%)",
        "linear": "Blue/green linear (4 steps)",
        "rolling": "Rolling (capacity batches)",
        "bake": "baking period",
        "wait": "wait",
        "alarm": "alarm → auto-rollback",
        "ok_path": "no alarms",
        "rolling_note": "does not double the fleet",
        "shift_title": "Deployment guardrails: how much traffic moves to the new fleet, and when",
        "shift_note": "Illustrative: sizes and times are configurable; rollback needs CloudWatch alarms",
        "week": "Week",
        "pending": "PendingManualApproval",
        "approved": "Approved",
        "rejected": "Rejected",
        "prod": "In production",
        "fail": "AUC < 0.82: FailStep,\nnot registered",
        "pipeline": "Executions",
        "redeploy": "v3 → Rejected:\nv1 returns",
        "reg_title": "Model Registry: only an Approved version reaches production, and rejecting it rolls back",
        "reg_note": "Illustrative; with the SageMaker Projects template, rejecting the current version redeploys the last Approved one",
        "rg_start": "EventBridge\nMonday 6:00",
        "rg_gates": [
            ("QualityCheck", "data against the baseline"),
            ("ConditionStep", "AUC ≥ 0.82 and better than production"),
            ("Approval", "Approved + smoke test + manual"),
            ("Canary 10%", "10 min with alarms"),
        ],
        "rg_runs": ["Run 1", "Run 2", "Run 3"],
        "rg_stop1": "bad data: the step fails, no training",
        "rg_stop2": "AUC below the threshold: FailStep, not registered",
        "rg_prod": "Production",
        "rg_late": "Days later",
        "rg_late1": "new version in production",
        "rg_rej": "Rejected",
        "rg_late2": "the last Approved is redeployed",
        "gates_title": "Each gate stops a different failure: only run 3 reaches production",
        "gates_note": "Three example runs; the Rejected rollback uses the SageMaker Projects template",
        "gc_title": "Prompts and documents change separately, but both pass an evaluation before they are accepted",
        "gc_tag1": "The prompt, agent or model changes",
        "gc_tag2": "The knowledge base documents change",
        "gc_change": "Change\nprompt or code",
        "gc_pm": "Prompt Management\nnew version",
        "gc_ev": "Bedrock Evaluations\nregression test",
        "gc_gate": "Gate\nquality threshold",
        "gc_dep": "Deployment\nagent version",
        "gc_rb": "Rollback: point production at the previous version",
        "gc_docs": "Documents\nnew or edited",
        "gc_ing": "Sync\nStartIngestionJob\nuntil COMPLETE",
        "gc_rag": "RAG evaluation\nretrieval and answer",
        "gc_ok": "The update is accepted",
        "gc_note": "Simplified pipeline",
    },
}


# ─── 1. Desplazamiento de tráfico / traffic shifting ───────────────────────────
def chart_traffic_shifting(t, out):
    T = 40
    panels = [
        ("all", [(0, 0), (2, 100), (T, 100)], [(2, 32)], None),
        ("canary", [(0, 0), (2, 10), (14, 10), (14, 100), (T, 100)], [(2, 14, "wait"), (14, 34)],
         [(0, 0), (2, 10), (8, 10), (8, 0), (T, 0)]),
        ("linear", [(0, 0), (2, 25), (8, 25), (8, 50), (14, 50), (14, 75), (20, 75), (20, 100), (T, 100)],
         [(20, 34)], None),
        ("rolling", [(0, 0), (2, 25), (8, 25), (8, 50), (14, 50), (14, 75), (20, 75), (20, 100), (T, 100)],
         [(20, 34)], None),
    ]
    fig, axes = figure(4.8, nrows=2, ncols=2, sharex=True, sharey=True)
    for ax, (key, pts, bakes, rollback) in zip(axes.flat, panels):
        for b in bakes:
            lbl = t["wait"] if len(b) == 3 else t["bake"]
            ax.axvspan(b[0], b[1], color=GRAY if len(b) == 3 else OK, alpha=0.14, lw=0)
            ax.text((b[0] + b[1]) / 2, 50, lbl, ha="center", fontsize=7.8, color=MUTED, va="center")
        x, y = zip(*pts)
        ax.plot(x, y, color=OK, lw=2.2, label=t["ok_path"] if rollback else None)
        if rollback:
            rx, ry = zip(*rollback)
            ax.plot(rx, ry, color=ACCENT, lw=1.6, ls=(0, (3, 2)), label=t["alarm"])
            ax.scatter([8], [10], color=ACCENT, s=22, zorder=4)
            ax.legend(frameon=False, fontsize=7.6, loc="center right", bbox_to_anchor=(1, 0.62))
        if key == "rolling":
            ax.text(T - 1, 8, t["rolling_note"], ha="right", fontsize=7.8, color=INK_SOFT)
        ax.set_title(t[key], fontsize=9.4, loc="left", color=INK, fontweight="bold")
        ax.set_xlim(0, T)
        ax.set_ylim(-5, 110)
        ax.set_yticks([0, 50, 100])
        ax.yaxis.grid(True, color=RULE, lw=0.6)
        clean_axes(ax)
    for ax in axes[1]:
        ax.set_xlabel(t["minutes"], fontsize=9)
    for ax in axes[:, 0]:
        ax.set_ylabel(t["share"], fontsize=8.6)
    fig.suptitle(t["shift_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["shift_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.subplots_adjust(top=0.88)
    save(fig, out, "traffic-shifting")


# ─── 2. Versiones en Model Registry / Model Registry versions ──────────────────
def chart_registry_timeline(t, out):
    colors = {"P": AMBER, "A": OK, "R": ACCENT}
    rows = [
        ("v1", [(0, 0.4, "P"), (0.4, 8, "A")]),
        ("v2", [(2.6, 3.2, "P"), (3.2, 8, "R")]),
        ("v3", [(4.6, 5.0, "P"), (5.0, 7.0, "A"), (7.0, 8, "R")]),
    ]
    prod = [(0.4, 5.0, "v1"), (5.0, 7.0, "v3"), (7.0, 8, "v1")]

    fig, ax = figure(3.8)
    ys = {name: 4 - i for i, (name, _) in enumerate(rows)}
    for name, segs in rows:
        for a, b, s in segs:
            ax.barh(ys[name], b - a, left=a, height=0.5, color=colors[s], alpha=0.9, edgecolor="white", lw=1)
    for a, b, v in prod:
        ax.barh(0, b - a, left=a, height=0.5, color=INK_SOFT if v == "v1" else OK, edgecolor="white", lw=1.5)
        ax.text((a + b) / 2, 0, v, ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    # Ejecuciones del pipeline; una no pasa la ConditionStep. Pipeline runs; one fails the ConditionStep.
    ax.scatter([0.05, 2.6, 4.6], [1, 1, 1], marker="o", color=OK, s=28, zorder=4)
    ax.scatter([1.6], [1], marker="x", color=ACCENT, s=60, lw=2, zorder=4)
    ax.text(1.6, 0.8, t["fail"], fontsize=8, color=ACCENT, va="top", ha="center")
    ax.annotate(t["redeploy"], xy=(7.0, 0.25), xytext=(6.2, 1.1), fontsize=8, color=INK, ha="center",
                va="center", arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.9))
    ax.set_yticks([4, 3, 2, 1, 0])
    ax.set_yticklabels(["v1", "v2", "v3", t["pipeline"], t["prod"]])
    ax.set_ylim(-0.5, 4.5)
    ax.set_xlim(0, 8)
    ax.set_xticks(range(0, 9))
    ax.set_xticklabels([str(i + 1) for i in range(9)])
    ax.set_xlabel(t["week"])
    # Leyenda manual / manual legend
    handles = [Patch(color=colors[k], label=t[n]) for k, n in (("P", "pending"), ("A", "approved"), ("R", "rejected"))]
    ax.legend(handles=handles, frameon=False, fontsize=8.2, loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=3)
    ax.set_title(t["reg_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold", pad=24)
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.99, 0.01, t["reg_note"], ha="right", fontsize=7.6, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "registry-timeline")


# ─── 3. Ejemplo: las puertas del pipeline / example: the pipeline gates ───────
def chart_release_gates(t, out):
    W, H = 32, 16.8
    fig, ax = figure(4.93)  # misma escala que antes (15 unidades en 4,4 in) más una franja para los íconos
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.07)
    diagram_axes(ax, W, H)

    gx = [8.6, 13.9, 19.2, 24.5]   # una columna por puerta / one column per gate
    x0, xp = 5.0, 27.3            # inicio de cada ejecución y producción / run start and production
    lanes = [10.0, 7.3, 4.6]
    top = 12.2
    r = 0.62

    # Íconos de servicio sobre cada columna: EventBridge, SageMaker Pipelines (dos pasos), Model Registry y el endpoint.
    # Service icons above each column: EventBridge, SageMaker Pipelines (two steps), Model Registry and the endpoint.
    for icon_name, x in zip(("aws/eventbridge", "aws/sagemaker-ai", "aws/sagemaker-ai", "aws/sagemaker-model",
                             "aws/cloudwatch-alarm"), [3.4] + gx):  # Canary: alarmas de CloudWatch / Canary: CloudWatch alarms
        place_icon(ax, icon_name, x, top + 3.55, 1.35)

    # Encabezados: inicio y cuatro puertas. Headers: start and four gates.
    fit_to(ax.text(3.4, top + 1.45, t["rg_start"], ha="center", va="center", fontsize=8.6, color=INK_SOFT,
                   multialignment="center"), 5.0, 2.2)
    for (name, detail), x in zip(t["rg_gates"], gx):
        ax.text(x, top + 2.2, name, ha="center", va="center", fontsize=9.2, fontweight="bold", color=INK)
        fit_to(ax.text(x, top + 1.0, detail, ha="center", va="center", fontsize=8.6, color=INK_SOFT,
                       multialignment="center"), 5.0, 2.0)
        ax.plot([x, x], [lanes[-1] - 1.3, top - 0.1], color=RULE, lw=1.0, ls=(0, (2, 3)), zorder=0)

    stops = {0: (0, t["rg_stop1"]), 1: (1, t["rg_stop2"]), 2: (None, None)}
    for lane, y in enumerate(lanes):
        fit_to(ax.text(0.3, y, t["rg_runs"][lane], ha="left", va="center", fontsize=9, fontweight="bold",
                       color=INK_SOFT), 4.4)
        stop, reason = stops[lane]
        end = gx[stop] if stop is not None else xp
        ax.plot([x0, end], [y, y], color=OK, lw=3.2, solid_capstyle="round", zorder=2)
        ax.plot([x0], [y], "o", color=OK, ms=5.5, zorder=3)
        for k, x in enumerate(gx):
            if stop is not None and k > stop:  # puerta no alcanzada / gate not reached
                ax.plot([x], [y], "o", ms=7, mfc="white", mec=GRAY, mew=1.4, zorder=3)
                continue
            failed = stop == k
            ax.add_patch(plt.Circle((x, y), r, color=ACCENT if failed else OK, zorder=4))
            if failed:  # ✗ dibujada / drawn cross
                ax.plot([x - 0.24, x + 0.24], [y - 0.24, y + 0.24], color="white", lw=2.2, zorder=5, solid_capstyle="round")
                ax.plot([x - 0.24, x + 0.24], [y + 0.24, y - 0.24], color="white", lw=2.2, zorder=5, solid_capstyle="round")
            else:  # ✓ dibujada / drawn check
                ax.plot([x - 0.27, x - 0.07, x + 0.3], [y - 0.02, y - 0.23, y + 0.24], color="white", lw=2.2, zorder=5,
                        solid_capstyle="round", solid_joinstyle="round")
        if stop is not None:  # motivo bajo el marcador, sin pisar las demás puertas / reason under the marker
            fit_to(ax.text(gx[stop] - 0.7, y - 1.0, reason, ha="left", va="center", fontsize=8.8, color=ACCENT,
                           bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5}, zorder=6), W - gx[stop] - 0.5)
        else:
            box(ax, xp, y - 0.8, W - xp - 0.2, 1.6, t["rg_prod"], edge=OK, fill="#e3f1e9", size=9.2, color=OK,
                weight="bold")

    # Días después: Rejected y vuelta atrás. Days later: Rejected and rollback.
    yl = 1.1
    ax.plot([0.3, W - 0.2], [2.75, 2.75], color=GRAY, lw=1.0, ls=(0, (3, 3)))
    fit_to(ax.text(0.3, yl, t["rg_late"], ha="left", va="center", fontsize=9, fontweight="bold", color=INK_SOFT),
           4.4)
    box(ax, 5.0, yl - 0.8, 10.6, 1.6, t["rg_late1"], edge=GRAY, fill=SURFACE, size=8.8, color=INK_SOFT)
    arrow(ax, (15.7, yl), (17.1, yl), color=ACCENT)
    box(ax, 17.2, yl - 0.8, 4.4, 1.6, t["rg_rej"], edge=ACCENT, fill=ACCENT, size=9, color="white", weight="bold")
    arrow(ax, (21.7, yl), (23.1, yl), color=OK)
    box(ax, 23.2, yl - 0.8, W - 23.4, 1.6, t["rg_late2"], edge=OK, fill="#e3f1e9", size=8.8, color=OK)

    fig.suptitle(t["gates_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.985, 0.015, t["gates_note"], ha="right", fontsize=7.6, color=MUTED)
    save(fig, out, "release-gates")


# ─── 4. CI/CD de IA generativa / generative AI CI/CD ───────────────────────────
def chart_genai_cicd(t, out):
    W, H = 32, 10
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.3), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.06)  # antes de los íconos / before icons
    diagram_axes(ax, W, H)
    w, h, gap = 5.5, 2.8, 0.08
    xs = [0.1 + k * 6.55 for k in range(5)]
    y1, y2 = 5.9, 0.5
    node = dict(edge=RULE, fill=SURFACE, size=8.8, desc_size=7.8, icon_size=0.95)

    fit_to(ax.text(0.2, 9.25, t["gc_tag1"], ha="left", va="bottom", fontsize=9, fontweight="bold", color=INK_SOFT), 16)
    box(ax, xs[0], y1, w, h, t["gc_change"], edge=INK_SOFT, fill="white", size=9)
    icon_node(ax, xs[1], y1, w, h, "aws/bedrock", t["gc_pm"], **node)
    icon_node(ax, xs[2], y1, w, h, "aws/bedrock", t["gc_ev"], **node)
    box(ax, xs[3], y1, w, h, t["gc_gate"], edge=ACCENT, fill="#fbeaec", size=9.4, color=ACCENT, weight="bold")
    icon_node(ax, xs[4], y1, w, h, "aws/bedrock-agentcore", t["gc_dep"], **{**node, "fill": "white", "edge": INK_SOFT})
    for i in range(4):
        arrow(ax, (xs[i] + w + gap, y1 + h / 2), (xs[i + 1] - gap, y1 + h / 2), color=INK_SOFT)
    fit_to(ax.text(xs[4] + w / 2, y1 - 0.35, t["gc_rb"], ha="center", va="top", fontsize=8.2, color=MUTED,
                   multialignment="center"), w + 1.0, 1.4)

    ax.plot([0.2, W - 0.2], [4.7, 4.7], color=GRAY, lw=1.0, ls=(0, (3, 3)))
    fit_to(ax.text(0.2, 3.75, t["gc_tag2"], ha="left", va="bottom", fontsize=9, fontweight="bold", color=INK_SOFT), 16)
    icon_node(ax, xs[0], y2, w, h - 0.4, "aws/s3", t["gc_docs"], **node)
    icon_node(ax, xs[1], y2, w, h - 0.4, "aws/bedrock", t["gc_ing"], **node)
    icon_node(ax, xs[2], y2, w, h - 0.4, "aws/bedrock", t["gc_rag"], **node)
    box(ax, xs[3], y2, w, h - 0.4, t["gc_ok"], edge=OK, fill="#e3f1e9", size=9.2, color=OK, weight="bold")
    for i in range(3):
        arrow(ax, (xs[i] + w + gap, y2 + (h - 0.4) / 2), (xs[i + 1] - gap, y2 + (h - 0.4) / 2),
              color=OK if i == 2 else INK_SOFT)

    fig.suptitle(t["gc_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.012, t["gc_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "genai-cicd")


CHARTS = [chart_traffic_shifting, chart_registry_timeline, chart_release_gates, chart_genai_cicd]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
