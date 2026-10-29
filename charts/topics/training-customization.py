"""
Tema 2.2: entrenamiento, ajuste y personalización. Topic 2.2: training, tuning and customization.

    python charts/topics/training-customization.py --lang es --out <dir>
"""

import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, plt, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "rounds": "Rondas de boosting",
        "logloss": "Error (logloss)",
        "train": "Entrenamiento",
        "val": "Validación",
        "best": "mejor ronda",
        "stop": "se detiene: 20 rondas sin mejorar",
        "overfit": "overfitting: el error de validación sube",
        "es_title": "XGBoost con max_depth = 10 y early_stopping_rounds = 20",
        "es_note": "Datos sintéticos; curvas reales de XGBoost",
        "jobs": "Trabajos de entrenamiento completados",
        "best_auc": "Mejor validation:auc hasta ahora",
        "random": "Random",
        "bayes": "Bayesian",
        "hpo_title": "AMT: Bayesian aprende de los trabajos anteriores; Random no",
        "hpo_note": "Ilustrativo: función objetivo sintética, media de 30 repeticiones, 1 trabajo a la vez",
        "hours": "Horas de reloj",
        "progress": "Progreso del entrenamiento (%)",
        "no_ckpt": "Spot sin checkpoints",
        "ckpt": "Spot con checkpoints en /opt/ml/checkpoints",
        "interrupt": "interrupción Spot",
        "spot_title": "Una interrupción sin checkpoints reinicia el trabajo desde cero",
        "spot_note": "Ilustrativo",
        "max_wait": "MaxWaitTimeInSeconds",
        "plan_title": "El ejemplo: cerrar la brecha de overfitting sin tocar el conjunto de prueba",
        "auc": "AUC",
        "start": "Inicio\nmax_depth = 10",
        "after": "Mejor trabajo\nde AMT",
        "gap": "brecha 0,19\n→ overfitting",
        "uses": "Qué decide cada conjunto",
        "split_train": "Entrenamiento",
        "split_train_use": "Ajusta los árboles con fit()",
        "split_val": "Validación",
        "split_val_use": "Early stopping (paso 2), métrica objetivo validation:auc de AMT y elección "
                         "del mejor trabajo (pasos 3 y 5)",
        "split_test": "Prueba",
        "split_test_use": "Una sola medición final frente a la baseline (paso 5)",
        "plan_note": "Cifras del caso de ejemplo · eje vertical desde 0,6",
        "reg_title": "La regularización estrecha la brecha entre entrenamiento y validación",
        "reg_without": "Sin regularización",
        "reg_with": "Con regularización",
        "reg_epoch": "Época",
        "reg_loss": "Error",
        "reg_gap_big": "brecha grande:\noverfitting",
        "reg_gap_small": "brecha pequeña:\ngeneraliza",
        "reg_stop": "early stopping\ncortaría aquí",
        "reg_l1": "L1",
        "reg_l1_use": "lleva pesos a cero",
        "reg_l2": "L2",
        "reg_l2_use": "reduce todos los pesos",
        "reg_drop": "Dropout",
        "reg_drop_use": "apaga neuronas al azar",
        "reg_es": "Early stopping",
        "reg_es_use": "corta cuando la validación no mejora",
        "reg_note": "Ilustrativo: curvas sintéticas",
    },
    "en": {
        "decimal": ".",
        "rounds": "Boosting rounds",
        "logloss": "Error (logloss)",
        "train": "Training",
        "val": "Validation",
        "best": "best round",
        "stop": "stops: 20 rounds without improvement",
        "overfit": "overfitting: validation error rises",
        "es_title": "XGBoost with max_depth = 10 and early_stopping_rounds = 20",
        "es_note": "Synthetic data; real XGBoost curves",
        "jobs": "Training jobs completed",
        "best_auc": "Best validation:auc so far",
        "random": "Random",
        "bayes": "Bayesian",
        "hpo_title": "AMT: Bayesian learns from previous jobs; Random does not",
        "hpo_note": "Illustrative: synthetic objective, mean of 30 runs, one job at a time",
        "hours": "Wall-clock hours",
        "progress": "Training progress (%)",
        "no_ckpt": "Spot without checkpoints",
        "ckpt": "Spot with checkpoints in /opt/ml/checkpoints",
        "interrupt": "Spot interruption",
        "spot_title": "Without checkpoints, an interruption restarts the job from zero",
        "spot_note": "Illustrative",
        "max_wait": "MaxWaitTimeInSeconds",
        "plan_title": "The example: closing the overfitting gap without touching the test set",
        "auc": "AUC",
        "start": "Start\nmax_depth = 10",
        "after": "Best AMT\njob",
        "gap": "0.19 gap\n→ overfitting",
        "uses": "What each split decides",
        "split_train": "Training",
        "split_train_use": "Fits the trees with fit()",
        "split_val": "Validation",
        "split_val_use": "Early stopping (step 2), the AMT objective validation:auc and picking the best job "
                         "(steps 3 and 5)",
        "split_test": "Test",
        "split_test_use": "A single final measurement against the baseline (step 5)",
        "plan_note": "Figures from the worked example · vertical axis starts at 0.6",
        "reg_title": "Regularization narrows the gap between training and validation",
        "reg_without": "Without regularization",
        "reg_with": "With regularization",
        "reg_epoch": "Epoch",
        "reg_loss": "Error",
        "reg_gap_big": "large gap:\noverfitting",
        "reg_gap_small": "small gap:\ngeneralizes",
        "reg_stop": "early stopping\nwould stop here",
        "reg_l1": "L1",
        "reg_l1_use": "drives weights to zero",
        "reg_l2": "L2",
        "reg_l2_use": "shrinks all weights",
        "reg_drop": "Dropout",
        "reg_drop_use": "randomly turns off neurons",
        "reg_es": "Early stopping",
        "reg_es_use": "stops when validation stops improving",
        "reg_note": "Illustrative: synthetic curves",
    },
}


# ─── 1. Early stopping con curvas reales / early stopping with real curves ─────
def _xgb_curves():
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier

    X, y = make_classification(n_samples=3000, n_features=20, n_informative=6, flip_y=0.08, random_state=3)
    X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)
    model = XGBClassifier(n_estimators=300, max_depth=10, learning_rate=0.1, eval_metric="logloss",
                          random_state=3, n_jobs=1)
    model.fit(X_tr, y_tr, eval_set=[(X_tr, y_tr), (X_va, y_va)], verbose=False)
    res = model.evals_result()
    return np.array(res["validation_0"]["logloss"]), np.array(res["validation_1"]["logloss"])


def chart_early_stopping(t, out):
    train, val = _xgb_curves()
    rounds = np.arange(1, len(train) + 1)
    best = int(np.argmin(val))
    stop = best + 20

    fig, ax = figure(4.2)
    ax.plot(rounds, train, color=MUTED, lw=1.8, label=t["train"])
    ax.plot(rounds, val, color=ACCENT, lw=2.2, label=t["val"])
    ax.axvspan(stop + 1, rounds[-1], color=GRAY, alpha=0.18, lw=0)
    ax.axvline(best + 1, color=OK, lw=1.2, ls=(0, (3, 2)))
    ax.axvline(stop + 1, color=INK, lw=1.2)
    ax.scatter([best + 1], [val[best]], color=OK, s=40, zorder=4)
    ymax = max(val.max(), train[0]) * 1.05
    ax.annotate(f"{t['best']}: {best + 1}", xy=(best + 1, val[best]), xytext=(stop + 30, ymax * 0.3), color=OK,
                fontsize=8.8, va="center", arrowprops=dict(arrowstyle="-|>", color=OK, lw=1))
    ax.text(stop + 4, ymax * 0.88, t["stop"], color=INK, fontsize=8.8, va="top")
    ax.text(rounds[-1] - 4, val[-1] + ymax * 0.04, t["overfit"], color=ACCENT, fontsize=8.8, ha="right",
            va="bottom")
    ax.set_xlim(0, rounds[-1])
    ax.set_ylim(0, ymax)
    ax.set_xlabel(t["rounds"])
    ax.set_ylabel(t["logloss"])
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    ax.set_title(t["es_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 0.24), fontsize=9)
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["es_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "early-stopping")


# ─── 2. Random vs Bayesian / random vs Bayesian search ─────────────────────────
def _objective(p):
    # Superficie suave tipo AUC sobre (log10 eta, max_depth normalizado) en [0, 1]^2.
    # Smooth AUC-like surface over normalized (log10 eta, max_depth) in [0, 1]^2.
    a, b = p[..., 0], p[..., 1]
    return 0.70 + 0.16 * np.exp(-((a - 0.32) ** 2) / 0.02 - ((b - 0.4) ** 2) / 0.05)


def _search_curves(n_jobs=40, reps=30):
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel
    from scipy.stats import norm

    rand, bayes = [], []
    grid = np.stack(np.meshgrid(np.linspace(0, 1, 41), np.linspace(0, 1, 41)), -1).reshape(-1, 2)
    for r in range(reps):
        rng = np.random.default_rng(100 + r)
        pts = rng.uniform(size=(n_jobs, 2))
        rand.append(np.maximum.accumulate(_objective(pts)))

        X = list(rng.uniform(size=(5, 2)))  # arranque aleatorio / random warm-up
        y = [float(_objective(np.array(x))) for x in X]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for _ in range(n_jobs - len(X)):
                gp = GaussianProcessRegressor(Matern(length_scale=0.2, nu=2.5) + WhiteKernel(1e-5),
                                              normalize_y=True, random_state=r).fit(np.array(X), np.array(y))
                mu, sd = gp.predict(grid, return_std=True)
                z = (mu - max(y)) / np.maximum(sd, 1e-9)
                ei = (mu - max(y)) * norm.cdf(z) + sd * norm.pdf(z)
                nxt = grid[int(np.argmax(ei))] + rng.normal(0, 0.005, 2)
                X.append(nxt)
                y.append(float(_objective(nxt)))
        bayes.append(np.maximum.accumulate(y))
    return np.mean(rand, axis=0), np.mean(bayes, axis=0)


def chart_hpo_strategies(t, out):
    rand, bayes = _search_curves()
    jobs = np.arange(1, len(rand) + 1)
    fig, ax = figure(4.0)
    ax.plot(jobs, rand, color=MUTED, lw=2, label=t["random"])
    ax.plot(jobs, bayes, color=OK, lw=2.4, label=t["bayes"])
    ax.axhline(0.86, color=INK, lw=0.8, ls=(0, (2, 3)))
    ax.text(len(jobs), 0.862, "máx. = 0,86" if t["decimal"] == "," else "max = 0.86", ha="right", va="bottom",
            fontsize=8.4, color=INK_SOFT)
    ax.set_xlim(1, len(jobs))
    ax.set_ylim(0.72, 0.875)
    ax.set_xlabel(t["jobs"])
    ax.set_ylabel(t["best_auc"])
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 2))
    ax.set_title(t["hpo_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="lower right", fontsize=9.5)
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["hpo_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "hpo-strategies")


# ─── 3. Spot con y sin checkpoints / Spot with and without checkpoints ─────────
def _progress(interrupts, checkpoint_every, total=8.0, outage=0.5, horizon=16.0, dt=0.01):
    ts, ps = [0.0], [0.0]
    t, p, last_ckpt = 0.0, 0.0, 0.0
    pending = list(interrupts)
    while p < total and t < horizon:
        t += dt
        if pending and t >= pending[0]:
            pending.pop(0)
            p = last_ckpt if checkpoint_every else 0.0
            ts += [t, t + outage]
            ps += [p, p]
            t += outage
            continue
        p += dt
        if checkpoint_every and p - last_ckpt >= checkpoint_every:
            last_ckpt = p
        ts.append(t)
        ps.append(p)
    return np.array(ts), np.array(ps) / total * 100


def chart_spot_checkpoints(t, out):
    interrupts = [3.0, 7.0]
    t1, p1 = _progress(interrupts, None)
    t2, p2 = _progress(interrupts, 0.5)
    fig, ax = figure(3.9)
    ax.plot(t1, p1, color=ACCENT, lw=2, label=t["no_ckpt"])
    ax.plot(t2, p2, color=OK, lw=2.4, label=t["ckpt"])
    for x in interrupts:
        ax.axvline(x, color=AMBER, lw=1.4)
        ax.text(x + 0.1, 103, t["interrupt"], fontsize=8.2, color=INK_SOFT, va="bottom")
    ax.scatter([t2[-1]], [100], color=OK, s=30, zorder=4)
    ax.scatter([t1[-1]], [p1[-1]], color=ACCENT, s=30, zorder=4)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 112)
    ax.set_xlabel(t["hours"])
    ax.set_ylabel(t["progress"])
    ax.set_title(t["spot_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["spot_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "spot-checkpoints")


# ─── 4. Plan del ejemplo / the worked example's plan ───────────────────────────
def chart_tuning_plan(t, out):
    fig = plt.figure(figsize=(WIDTH_IN, 4.1), dpi=DPI)
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.25], wspace=0.12)
    ax, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    # AUC del caso / AUC from the case
    x = np.array([0, 1])
    ax.bar(x[0] - 0.19, 0.97, 0.36, color=GRAY, label=t["train"], zorder=3)
    ax.bar(x + 0.19, [0.78, 0.86], 0.36, color=[ACCENT, OK], label=t["val"], zorder=3)
    for xi, v in ((x[0] - 0.19, 0.97), (x[0] + 0.19, 0.78), (x[1] + 0.19, 0.86)):
        ax.text(xi, v + 0.008, fmt(v, t, 2), ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=INK)
    ax.annotate("", xy=(x[0] + 0.45, 0.97), xytext=(x[0] + 0.45, 0.78),
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=1.2))
    ax.text(x[0] + 0.52, 0.875, t["gap"], fontsize=8.6, color=ACCENT, va="center")
    ax.set_xticks(x)
    ax.set_xticklabels([t["start"], t["after"]], fontsize=9)
    ax.set_ylim(0.6, 1.04)
    ax.set_yticks([0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xlim(-0.6, 1.6)
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    ax.set_ylabel(t["auc"])
    ax.legend(frameon=False, fontsize=8.6, loc="upper right", ncol=2, bbox_to_anchor=(1.0, 1.1))
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    clean_axes(ax)

    # Qué decide cada conjunto / what each split decides
    diagram_axes(ax2, 10, 9)
    ax2.text(0.1, 8.6, t["uses"], fontsize=9.6, fontweight="bold", color=INK, va="center")
    rows = [(t["split_train"], t["split_train_use"], GRAY, INK_SOFT),
            (t["split_val"], t["split_val_use"], OK, INK),
            (t["split_test"], t["split_test_use"], AMBER, INK)]
    for i, (name, use, edge, color) in enumerate(rows):
        y = 5.7 - i * 2.75
        box(ax2, 0.1, y, 2.6, 2.3, name, edge=edge, fill=edge, size=9.2, color="white" if edge == OK else INK,
            weight="bold")
        box(ax2, 2.9, y, 7.0, 2.3, use, edge=RULE, fill="white", size=8.8, color=color)

    fig.suptitle(t["plan_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["plan_note"], ha="right", fontsize=8, color=MUTED)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.84, bottom=0.17)
    save(fig, out, "tuning-plan")


# ─── 5. Regularización / regularization ────────────────────────────────────────
def chart_regularization_curves(t, out):
    rng = np.random.default_rng(11)
    e = np.arange(1, 61)

    def noisy(y):
        wiggle = np.convolve(rng.normal(0, 0.012, e.size + 4), np.ones(5) / 5, mode="valid")
        return y + wiggle

    train_raw = noisy(0.04 + 0.86 * np.exp(-e / 9))
    val_raw = noisy(0.30 + 0.60 * np.exp(-e / 6) + 0.0065 * np.maximum(e - 16, 0))
    train_reg = noisy(0.24 + 0.66 * np.exp(-e / 10))
    val_reg = noisy(0.31 + 0.62 * np.exp(-e / 9) + 0.0005 * np.maximum(e - 30, 0))

    fig = plt.figure(figsize=(WIDTH_IN, 4.9), dpi=DPI)
    gs = fig.add_gridspec(2, 2, height_ratios=[3.2, 1], hspace=0.55, wspace=0.12)
    panels = [(fig.add_subplot(gs[0, 0]), t["reg_without"], train_raw, val_raw, False),
              (fig.add_subplot(gs[0, 1]), t["reg_with"], train_reg, val_reg, True)]
    for ax, title, train, val, regularized in panels:
        ax.plot(e, train, color=MUTED, lw=1.8, label=t["train"])
        ax.plot(e, val, color=ACCENT, lw=2.2, label=t["val"])
        gap_x = 57
        i = gap_x - 1
        lo, hi = sorted((train[i], val[i]))
        if regularized:  # brecha pequeña: un trazo, sin puntas de flecha / small gap: a bar, no arrowheads
            ax.plot([gap_x, gap_x], [lo, hi], color=OK, lw=3, solid_capstyle="butt")
        else:
            ax.annotate("", xy=(gap_x, lo), xytext=(gap_x, hi),
                        arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=1.2))
        ax.text(gap_x - 2.5, (lo + hi) / 2 + (0.02 if not regularized else 0.12),
                t["reg_gap_small"] if regularized else t["reg_gap_big"], ha="right", va="center", fontsize=8.6,
                color=OK if regularized else ACCENT, linespacing=1.3)
        if not regularized:
            best = int(np.argmin(val)) + 1
            ax.axvline(best, color=INK, lw=1.1, ls=(0, (3, 2)))
            ax.text(best + 1.5, 0.93, t["reg_stop"], fontsize=8.6, color=INK, va="top", linespacing=1.3)
        ax.set_xlim(0, 60)
        ax.set_ylim(0, 1.0)
        ax.set_title(title, fontsize=9.8, loc="left", color=INK, fontweight="bold")
        ax.set_xlabel(t["reg_epoch"])
        ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
        ax.yaxis.grid(True, color=RULE, lw=0.6)
        ax.set_axisbelow(True)
        clean_axes(ax)
    panels[0][0].set_ylabel(t["reg_loss"])
    panels[1][0].tick_params(labelleft=False)
    panels[0][0].legend(frameon=False, fontsize=8.6, loc="upper right", bbox_to_anchor=(1, 0.8))

    # Dónde actúa cada técnica / where each technique acts
    strip = fig.add_subplot(gs[1, :])
    diagram_axes(strip, 16.2, 2.4)
    items = [(t["reg_l1"], t["reg_l1_use"]), (t["reg_l2"], t["reg_l2_use"]), (t["reg_drop"], t["reg_drop_use"]),
             (t["reg_es"], t["reg_es_use"])]
    w, gap = 3.6, 0.55
    for k, (name, use) in enumerate(items):
        x = 0.1 + k * (w + gap)
        box(strip, x, 0.2, w, 1.9, "", edge=RULE, fill=SURFACE, lw=1.1)
        strip.text(x + w / 2, 1.72, name, ha="center", va="center", fontsize=9.4, fontweight="bold", color=INK)
        fit_to(strip.text(x + w / 2, 1.28, use, ha="center", va="top", fontsize=8.6, color=INK_SOFT,
                          multialignment="center"), w - 0.4, 0.95)

    fig.suptitle(t["reg_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["reg_note"], ha="right", fontsize=8, color=MUTED)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.88, bottom=0.07)
    save(fig, out, "regularization-curves")


CHARTS = [chart_early_stopping, chart_hpo_strategies, chart_spot_checkpoints, chart_tuning_plan,
          chart_regularization_curves]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
