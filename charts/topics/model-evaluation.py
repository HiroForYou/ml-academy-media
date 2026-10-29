"""
Tema 2.3: analizar y evaluar el rendimiento del modelo. Topic 2.3: analyze and evaluate model performance.

    python charts/topics/model-evaluation.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, pct, place_icon, plt, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "thr": "Umbral de decisión (probabilidad de fraude)",
        "rate": "Recall / precision",
        "alerts": "Alertas por día",
        "recall": "Recall",
        "precision": "Precision",
        "alerts_l": "Alertas/día",
        "capacity": "capacidad del equipo: 2.000 alertas/día",
        "chosen": "umbral elegido en validación",
        "thr_title": "Con 0,8 % de fraude, el umbral se elige por recall y capacidad, no por accuracy",
        "acc_note": "Un modelo que nunca alerta tiene accuracy = 99,2 % y recall = 0",
        "thr_note": "Ilustrativo: scores sintéticos, 60.000 transacciones/día",
        "thousands": ".",
        "feature": "Importe de la transacción (USD)",
        "density": "Proporción",
        "baseline": "Línea base (entrenamiento)",
        "current": "Datos capturados, día 30",
        "day": "Día en producción",
        "psi": "PSI frente a la línea base",
        "psi_thr": "umbral de alerta 0,2 (convención habitual)",
        "alarm": "alarma → SNS",
        "drift_title": "Data quality drift: comparar los datos capturados con la línea base, sin etiquetas",
        "dist_sub": "Distribución de una feature",
        "psi_sub": "Drift diario de esa feature",
        "drift_note": "Ilustrativo: datos sintéticos; PSI calculado con 10 intervalos de la línea base",
        "epoch": "Epoch",
        "loss": "Loss",
        "train": "Entrenamiento",
        "val": "Validación",
        "p1": "Loss que explota (NaN)",
        "p1_fix": "baja el learning rate,\nrecorta gradientes",
        "p2": "Gradientes casi cero",
        "p2_fix": "revisa activaciones\ne inicialización",
        "p3": "Overfitting",
        "p3_fix": "early stopping\no regularización",
        "loss_title": "Leer la curva de loss: tres fallos de convergencia que el examen describe",
        "loss_note": "Ilustrativo. Antes: reglas de Debugger ExplodingTensor, VanishingGradient y Overfit",
        "cur": "Actual",
        "cand": "Candidato",
        "metric_sub": "Métricas en el mismo conjunto de validación",
        "alerts_sub": "Alertas por día frente a la capacidad",
        "cap_line": "capacidad: 2.000",
        "cmp_title": "El candidato mejora AUC y recall sin superar las 2.000 alertas diarias",
        "cmp_note": "Valores del ejemplo. La accuracy se omite: con 0,8 % de fraude, no alertar nunca da 99,2 %",
        "ev_title": "Tres formas de evaluar un FM en Bedrock: elige según escala y riesgo",
        "ev_who": "Quién puntúa",
        "ev_what": "Qué mide",
        "ev_use": "Úsala para",
        "ev_auto": "Automática",
        "ev_auto_who": "Métricas programáticas",
        "ev_auto_what": "Accuracy, robustness, toxicity",
        "ev_auto_use": "Comparar modelos con datasets integrados o propios",
        "ev_judge": "LLM-as-a-judge",
        "ev_judge_who": "Un modelo evaluador",
        "ev_judge_what": "Correctness, Faithfulness…",
        "ev_judge_use": "Puntuar a escala: hasta 1.000 prompts por trabajo",
        "ev_human": "Humana",
        "ev_human_who": "Tu equipo (Cognito), hasta 2 modelos",
        "ev_human_what": "Thumbs, Likert, ordinal rank",
        "ev_human_use": "Casos de riesgo y calibrar al juez",
        "ev_left": "Más escala",
        "ev_right": "Más criterio humano",
        "ev_note": "Ilustrativo: las barras y los puntajes no son resultados reales",
        "ev_prompt": "Prompt",
        "ev_resp": "Respuesta",
        "ev_judge_box": "Juez",
        "ev_score": "puntaje + explicación",
        "ev_correct": "Correctness",
        "ev_thumbs": "Thumbs",
        "ev_rank": "Ordinal rank",
    },
    "en": {
        "decimal": ".",
        "thr": "Decision threshold (fraud probability)",
        "rate": "Recall / precision",
        "alerts": "Alerts per day",
        "recall": "Recall",
        "precision": "Precision",
        "alerts_l": "Alerts/day",
        "capacity": "team capacity: 2,000 alerts/day",
        "chosen": "threshold chosen on validation",
        "thr_title": "With 0.8% fraud, pick the threshold by recall and capacity, not accuracy",
        "acc_note": "A model that never alerts has accuracy = 99.2% and recall = 0",
        "thr_note": "Illustrative: synthetic scores, 60,000 transactions/day",
        "thousands": ",",
        "feature": "Transaction amount (USD)",
        "density": "Share",
        "baseline": "Baseline (training)",
        "current": "Captured data, day 30",
        "day": "Day in production",
        "psi": "PSI versus the baseline",
        "psi_thr": "alert threshold 0.2 (common convention)",
        "alarm": "alarm → SNS",
        "drift_title": "Data quality drift: compare captured data with the baseline, no labels needed",
        "dist_sub": "Distribution of one feature",
        "psi_sub": "Daily drift of that feature",
        "drift_note": "Illustrative: synthetic data; PSI computed over 10 baseline bins",
        "epoch": "Epoch",
        "loss": "Loss",
        "train": "Training",
        "val": "Validation",
        "p1": "Exploding loss (NaN)",
        "p1_fix": "lower the learning rate,\nclip gradients",
        "p2": "Near-zero gradients",
        "p2_fix": "check activations\nand initialization",
        "p3": "Overfitting",
        "p3_fix": "early stopping\nor regularization",
        "loss_title": "Reading the loss curve: three convergence failures the exam describes",
        "loss_note": "Illustrative. Formerly Debugger rules ExplodingTensor, VanishingGradient and Overfit",
        "cur": "Current",
        "cand": "Candidate",
        "metric_sub": "Metrics on the same validation set",
        "alerts_sub": "Alerts per day against capacity",
        "cap_line": "capacity: 2,000",
        "cmp_title": "The candidate improves AUC and recall without exceeding 2,000 daily alerts",
        "cmp_note": "Values from the example. Accuracy is left out: with 0.8% fraud, never alerting scores 99.2%",
        "ev_title": "Three ways to evaluate an FM in Bedrock: choose by scale and risk",
        "ev_who": "Who scores",
        "ev_what": "What it measures",
        "ev_use": "Use it for",
        "ev_auto": "Automatic",
        "ev_auto_who": "Programmatic metrics",
        "ev_auto_what": "Accuracy, robustness, toxicity",
        "ev_auto_use": "Comparing models with built-in or custom datasets",
        "ev_judge": "LLM-as-a-judge",
        "ev_judge_who": "An evaluator model",
        "ev_judge_what": "Correctness, Faithfulness…",
        "ev_judge_use": "Scoring at scale: up to 1,000 prompts per job",
        "ev_human": "Human",
        "ev_human_who": "Your team (Cognito), up to 2 models",
        "ev_human_what": "Thumbs, Likert, ordinal rank",
        "ev_human_use": "High-risk cases and calibrating the judge",
        "ev_left": "More scale",
        "ev_right": "More human judgment",
        "ev_note": "Illustrative: bars and scores are not real results",
        "ev_prompt": "Prompt",
        "ev_resp": "Response",
        "ev_judge_box": "Judge",
        "ev_score": "score + explanation",
        "ev_correct": "Correctness",
        "ev_thumbs": "Thumbs",
        "ev_rank": "Ordinal rank",
    },
}


def _thousands(v, t):
    return f"{v:,.0f}".replace(",", t["thousands"])


def _title(ax, text):
    ax.set_title(text, fontsize=10.2, loc="left", color=INK, fontweight="bold")


# ─── 1. Umbral, recall y capacidad / threshold, recall and capacity ────────────
def chart_threshold_capacity(t, out):
    n_day, prev, mu = 60_000, 0.008, 2.6
    rng = np.random.default_rng(7)
    neg = rng.normal(0, 1, 400_000)
    pos = rng.normal(mu, 1, 40_000)

    def prob(x):  # probabilidad calibrada: LLR normal + prior / calibrated probability
        return 1 / (1 + np.exp(-(mu * x - mu ** 2 / 2 + np.log(prev / (1 - prev)))))

    p_neg, p_pos = prob(neg), prob(pos)
    thr = np.linspace(0.005, 0.6, 400)
    recall = np.array([(p_pos >= h).mean() for h in thr])
    fpr = np.array([(p_neg >= h).mean() for h in thr])
    tp = recall * n_day * prev
    alerts = tp + fpr * n_day * (1 - prev)
    precision = tp / np.maximum(alerts, 1e-9)
    ok = np.where(alerts <= 2000)[0]
    i = ok[0]

    fig, ax = figure(4.3)
    ax2 = ax.twinx()
    ax2.fill_between(thr, 0, alerts, color=GRAY, alpha=0.35, lw=0, label=t["alerts_l"])
    ax2.axhline(2000, color=INK, lw=1, ls=(0, (3, 2)))
    ax2.text(0.59, 2080, t["capacity"], ha="right", va="bottom", fontsize=8.5, color=INK)
    ax2.set_ylim(0, 6000)
    ax2.set_ylabel(t["alerts"])
    ax2.yaxis.set_major_formatter(lambda v, _: _thousands(v, t))
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color(RULE)
    ax2.tick_params(length=3, labelsize=9.5)

    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.plot(thr, recall, color=ACCENT, lw=2.3, label=t["recall"])
    ax.plot(thr, precision, color=OK, lw=2.3, label=t["precision"])
    ax.axvline(thr[i], color=INK_SOFT, lw=1.2)
    ax.scatter([thr[i]], [recall[i]], color=ACCENT, s=36, zorder=5)
    ax.scatter([thr[i]], [precision[i]], color=OK, s=36, zorder=5)
    ax.annotate(f"{t['chosen']}: {fmt(thr[i], t, 2)}\n{t['recall']} {fmt(recall[i], t, 2)} · "
                f"{t['precision']} {fmt(precision[i], t, 2)} · {_thousands(alerts[i], t)} {t['alerts_l'].lower()}",
                xy=(thr[i], recall[i]), xytext=(thr[i] + 0.06, 0.93), fontsize=8.6, color=INK, va="top",
                arrowprops=dict(arrowstyle="-|>", color=INK_SOFT, lw=0.9))
    ax.text(0.59, 0.02, t["acc_note"], ha="right", va="bottom", fontsize=8.6, color=ACCENT)
    ax.set_xlim(0, 0.6)
    ax.set_ylim(0, 1)
    ax.set_xlabel(t["thr"])
    ax.set_ylabel(t["rate"])
    ax.xaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    _title(ax, t["thr_title"])
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="center right", fontsize=9)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["thr_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "threshold-capacity")


# ─── 2. Drift frente a la línea base (PSI) / drift versus the baseline (PSI) ───
def _psi(base, cur, edges):
    b = np.histogram(base, edges)[0] / len(base)
    c = np.histogram(cur, edges)[0] / len(cur)
    b, c = np.clip(b, 1e-4, None), np.clip(c, 1e-4, None)
    return float(np.sum((c - b) * np.log(c / b)))


def chart_drift_psi(t, out):
    rng = np.random.default_rng(11)
    base = rng.lognormal(3.6, 0.55, 20_000)
    edges = np.quantile(base, np.linspace(0, 1, 11))
    edges[0], edges[-1] = 0, np.inf
    days = np.arange(1, 31)
    # El importe medio sube despacio desde el día 12. Mean amount rises slowly from day 12.
    shift = np.where(days < 12, 0.0, (days - 12) * 0.028)
    psi, last = [], None
    for d, s in zip(days, shift):
        cur = rng.lognormal(3.6 + s, 0.55 + s * 0.3, 3_000)
        psi.append(_psi(base, cur, edges))
        last = cur
    psi = np.array(psi)
    first = int(np.argmax(psi > 0.2))

    fig, (a1, a2) = figure(4.0, ncols=2, gridspec_kw={"width_ratios": [1, 1.25]})
    bins = np.linspace(0, 220, 45)
    a1.hist(base, bins, density=True, color=GRAY, alpha=0.9, label=t["baseline"])
    a1.hist(last, bins, density=True, histtype="step", color=ACCENT, lw=1.8, label=t["current"])
    a1.set_xlim(0, 220)
    a1.set_yticks([])
    a1.set_xlabel(t["feature"])
    a1.set_ylabel(t["density"])
    a1.set_title(t["dist_sub"], fontsize=9.5, loc="left", color=INK_SOFT)
    a1.legend(frameon=False, fontsize=8.4, loc="upper right")
    clean_axes(a1)

    a2.plot(days, psi, color=INK_SOFT, lw=1.6, marker="o", ms=3.2)
    a2.axhline(0.2, color=ACCENT, lw=1, ls=(0, (3, 2)))
    a2.text(1, 0.215, t["psi_thr"], fontsize=8.3, color=ACCENT, va="bottom")
    a2.scatter(days[psi > 0.2], psi[psi > 0.2], color=ACCENT, s=16, zorder=4)
    a2.annotate(t["alarm"], xy=(days[first], psi[first]), xytext=(days[first] - 9, psi.max() * 0.85),
                fontsize=8.6, color=ACCENT, arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=0.9))
    a2.set_xlim(0, 31)
    a2.set_ylim(0, max(psi.max() * 1.12, 0.3))
    a2.set_xlabel(t["day"])
    a2.set_ylabel(t["psi"])
    a2.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    a2.set_title(t["psi_sub"], fontsize=9.5, loc="left", color=INK_SOFT)
    a2.yaxis.grid(True, color=RULE, lw=0.6)
    clean_axes(a2)
    fig.suptitle(t["drift_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["drift_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.subplots_adjust(top=0.84)
    save(fig, out, "drift-psi")


# ─── 3. Diagnóstico de curvas de loss / loss-curve diagnostics ─────────────────
def chart_loss_diagnostics(t, out):
    rng = np.random.default_rng(5)
    ep = np.arange(1, 41)
    fig, axes = figure(3.4, ncols=3, sharey=False)

    # 1) Learning rate alto: oscila y diverge a NaN. High LR: oscillates and diverges to NaN.
    a = axes[0]
    y = 1.0 * np.exp(0.09 * ep) * (1 + 0.35 * np.sin(ep * 1.3)) * 0.35
    y[:4] = [0.9, 0.7, 0.95, 0.8]
    cut = 22
    y[cut - 3:cut] = [y[cut - 4] * 1.5, y[cut - 4] * 2.2, y[cut - 4] * 3.2]
    a.plot(ep[:cut], y[:cut], color=ACCENT, lw=2)
    a.scatter([ep[cut - 1]], [y[cut - 1]], color=ACCENT, s=28, zorder=4)
    a.text(ep[cut - 1] + 1.2, y[cut - 1], "NaN", color=ACCENT, fontsize=10, fontweight="bold", va="center")
    a.set_ylim(-y[:cut].max() * 0.3, y[:cut].max() * 1.12)

    # 2) Vanishing gradient: la loss apenas se mueve. Loss barely moves.
    b = axes[1]
    y2 = 0.69 - 0.02 * (1 - np.exp(-ep / 3)) + rng.normal(0, 0.002, ep.size)
    b.plot(ep, y2, color=AMBER, lw=2.2)
    b.set_ylim(-0.25, 0.9)

    # 3) Overfitting.
    c = axes[2]
    tr = 0.15 + 0.6 * np.exp(-ep / 7)
    va = 0.32 + 0.45 * np.exp(-ep / 6) + 0.0045 * np.clip(ep - 12, 0, None) ** 1.3
    c.plot(ep, tr, color=MUTED, lw=1.8, label=t["train"])
    c.plot(ep, va, color=ACCENT, lw=2.2, label=t["val"])
    c.axvline(12, color=OK, lw=1.1, ls=(0, (3, 2)))
    c.legend(frameon=False, fontsize=8, loc="upper right")
    c.set_ylim(-0.25, 0.9)

    for ax, key, fix, col in ((a, "p1", "p1_fix", ACCENT), (b, "p2", "p2_fix", AMBER), (c, "p3", "p3_fix", OK)):
        ax.set_title(t[key], fontsize=9.6, loc="left", color=INK, fontweight="bold")
        ax.text(0.36 if key == "p3" else 0.04, 0.05, t[fix], transform=ax.transAxes, fontsize=8.3, color=INK_SOFT, va="bottom")
        ax.set_xlabel(t["epoch"])
        ax.set_yticks([])
        ax.set_xlim(0, 41)
        clean_axes(ax)
    axes[0].set_ylabel(t["loss"])
    fig.suptitle(t["loss_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.015, t["loss_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.subplots_adjust(top=0.8)
    save(fig, out, "loss-diagnostics")


# ─── 4. Ejemplo: candidato frente al modelo actual / example: candidate vs current ─
def chart_candidate_vs_current(t, out):
    metrics = [("AUC", 0.91, 0.94), ("Recall", 0.62, 0.74), ("Precision", 0.18, 0.20)]
    alerts = (1650, 1780)

    fig, (a1, a2) = figure(3.9, ncols=2, gridspec_kw={"width_ratios": [1.5, 1]})
    x = np.arange(len(metrics))
    w = 0.36
    for k, (label, color) in enumerate(((t["cur"], GRAY), (t["cand"], OK))):
        vals = [m[1 + k] for m in metrics]
        bars = a1.bar(x + (k - 0.5) * w, vals, w, color=color, label=label)
        for b, v in zip(bars, vals):
            a1.text(b.get_x() + b.get_width() / 2, v + 0.02, fmt(v, t, 2), ha="center", va="bottom",
                    fontsize=8.6, color=INK_SOFT)
    a1.set_xticks(x)
    a1.set_xticklabels([m[0] for m in metrics])
    a1.set_ylim(0, 1.12)
    a1.set_yticks([0, 0.5, 1])
    a1.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    a1.yaxis.grid(True, color=RULE, lw=0.6)
    a1.set_axisbelow(True)
    a1.legend(frameon=False, fontsize=8.6, loc="upper right", ncol=2)
    a1.set_title(t["metric_sub"], fontsize=9.4, loc="left", color=INK_SOFT)
    clean_axes(a1)

    y = np.arange(2)[::-1]
    a2.barh(y, alerts, height=0.5, color=[GRAY, OK])
    for yy, v, col in zip(y, alerts, (INK, "white")):
        a2.text(v - 60, yy, _thousands(v, t), ha="right", va="center", fontsize=8.8, color=col, fontweight="bold")
    a2.axvline(2000, color=ACCENT, lw=1.4, ls=(0, (3, 2)))
    a2.text(1960, 1.55, t["cap_line"], ha="right", va="center", fontsize=8.4, color=ACCENT)
    a2.set_yticks(y)
    a2.set_yticklabels([t["cur"], t["cand"]])
    a2.set_ylim(-0.6, 1.9)
    a2.set_xlim(0, 2300)
    a2.set_xticks([0, 1000, 2000])
    a2.xaxis.set_major_formatter(lambda v, _: _thousands(v, t))
    a2.set_title(t["alerts_sub"], fontsize=9.4, loc="left", color=INK_SOFT)
    clean_axes(a2)
    a2.tick_params(axis="y", length=0)

    fig.suptitle(t["cmp_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["cmp_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.subplots_adjust(top=0.82)
    save(fig, out, "candidate-vs-current")


# ─── 5. Enfoques de evaluación de FMs / FM evaluation approaches ────────────────
def chart_eval_approaches(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 5.7), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.05)
    diagram_axes(ax, 16, 10.2)
    w, gap, x0 = 4.9, 0.55, 0.1
    top, bottom = 9.9, 3.0
    cols = ["auto", "judge", "human"]
    cx = [x0 + k * (w + gap) + w / 2 for k in range(3)]

    def chip(x, y, text, width, size=8.4):
        box(ax, x - width / 2, y - 0.38, width, 0.76, text, edge=RULE, fill=SURFACE, size=size, color=INK_SOFT)

    for k, key in enumerate(cols):
        x = x0 + k * (w + gap)
        box(ax, x, bottom, w, top - bottom, "", edge=RULE, fill="white", lw=1.2)
        box(ax, x, top - 0.9, w, 0.9, t[f"ev_{key}"], edge=RULE, fill=SURFACE, size=10.4, color=INK, weight="bold")
        # Servicio de cada enfoque: Bedrock (automática y juez) y Cognito (equipo humano).
        # Each approach's service: Bedrock (automatic and judge) and Cognito (human team).
        place_icon(ax, ("aws/bedrock", "aws/bedrock", "aws/cognito")[k], x + 0.62, top - 0.45, 0.62)
        fit_to(ax.text(cx[k], top - 1.3, t[f"ev_{key}_who"], fontsize=8.6, color=MUTED, ha="center", va="top"),
               w - 0.5, 0.9)
        ax.plot([x + 0.3, x + w - 0.3], [bottom + 1.3, bottom + 1.3], color=RULE, lw=0.9)
        fit_to(ax.text(cx[k], bottom + 0.65, t[f"ev_{key}_use"], fontsize=8.6, color=INK, fontweight="bold",
                       ha="center", va="center", linespacing=1.25), w - 0.5, 1.0)

    # 1) Automática: barras de métricas y chips de NLP / Automatic: metric bars and NLP chips
    x = x0
    for j, (name, frac) in enumerate((("Accuracy", 0.78), ("Robustness", 0.6), ("Toxicity", 0.28))):
        y = 7.35 - j * 0.75
        ax.text(x + 0.35, y, name, fontsize=8.2, color=INK_SOFT, va="center")
        ax.add_patch(plt.Rectangle((x + 1.85, y - 0.18), 2.7, 0.36, facecolor=SURFACE, edgecolor="none", zorder=1))
        ax.add_patch(plt.Rectangle((x + 1.85, y - 0.18), 2.7 * frac, 0.36, facecolor=INK_SOFT, edgecolor="none",
                                   zorder=2))
    for q, (name, wd) in enumerate((("BERTScore", 1.5), ("ROUGE", 1.2), ("BLEU", 1.0))):
        chip(x + 0.35 + (0.75, 2.2, 3.4)[q] + 0.0, 4.95, name, wd)

    # 2) Juez: prompt → respuesta → juez → puntaje con explicación / Judge: flow, then score
    x = x0 + (w + gap)
    bw, y = 1.3, 7.45
    for q, (key, fill, edge) in enumerate((("ev_prompt", SURFACE, RULE), ("ev_resp", SURFACE, RULE),
                                           ("ev_judge_box", "white", INK_SOFT))):
        bx = x + 0.3 + q * 1.55
        box(ax, bx, y - 0.4, bw, 0.8, t[key], edge=edge, fill=fill, size=8.4, color=INK,
            weight="bold" if q == 2 else "normal")
        if q < 2:
            arrow(ax, (bx + bw + 0.02, y), (bx + 1.55 - 0.02, y), color=MUTED, lw=1.1)
    jx = x + 0.3 + 2 * 1.55 + bw / 2
    ax.plot([jx, jx], [y - 0.42, 6.72], color=INK_SOFT, lw=1.2, zorder=4)
    ax.scatter([jx], [6.62], marker="v", s=26, c=INK_SOFT, zorder=4, edgecolors="none")
    box(ax, x + 0.3, 4.55, w - 0.6, 1.95, "", edge=RULE, fill=SURFACE, lw=1.0)
    ax.text(x + 0.6, 5.85, t["ev_correct"], fontsize=8.2, color=INK_SOFT, va="center")
    ax.scatter([x + 2.25 + i * 0.5 for i in range(5)], [5.85] * 5, s=34, c=[INK_SOFT] * 4 + [GRAY], zorder=3,
               edgecolors="none")
    fit_to(ax.text(x + 0.6, 5.1, t["ev_score"], fontsize=8.2, color=MUTED, va="center", style="italic"),
           w - 1.2, 0.6)

    # 3) Humana: tira Likert 1–5 y chips / Human: Likert strip and chips
    x = x0 + 2 * (w + gap)
    for i in range(5):
        px = x + 0.9 + i * 0.78
        ax.scatter([px], [7.45], s=150, facecolors=ACCENT if i == 3 else "white",
                   edgecolors=ACCENT if i == 3 else GRAY, linewidths=1.4, zorder=3)
        ax.text(px, 6.8, str(i + 1), fontsize=8, color=INK_SOFT, ha="center", va="center")
    ax.text(cx[2], 6.2, "Likert", fontsize=8.2, color=INK_SOFT, ha="center", va="center", fontweight="bold")
    chip(x + 1.5, 4.95, t["ev_thumbs"], 1.5)
    chip(x + 3.35, 4.95, t["ev_rank"], 1.85)

    # Eje de escala frente a criterio humano / scale versus human-judgment axis
    ay = 1.75
    arrow(ax, (x0, ay), (15.9, ay), color=INK_SOFT, lw=1.5)
    for k in range(3):
        ax.plot([cx[k]] * 2, [bottom - 0.05, ay + 0.15], color=RULE, lw=1.0, ls=(0, (3, 2)), zorder=0)
        ax.scatter([cx[k]], [ay], s=70, c=ACCENT, zorder=4, edgecolors="white", linewidths=1.2)
    ax.text(x0, 0.95, t["ev_left"], fontsize=8.6, color=INK_SOFT, va="center")
    ax.text(15.9, 0.95, t["ev_right"], fontsize=8.6, color=INK_SOFT, va="center", ha="right")
    fig.text(0.99, 0.012, t["ev_note"], ha="right", fontsize=7.6, color=MUTED)
    ax.set_title(t["ev_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    save(fig, out, "eval-approaches")


CHARTS = [chart_threshold_capacity, chart_drift_psi, chart_loss_diagnostics, chart_candidate_vs_current,
          chart_eval_approaches]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
