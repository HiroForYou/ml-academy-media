"""
Gráficos del tema 1.3 (calidad de datos y sesgo), en español e inglés.
Charts for topic 1.3 (data quality and bias), in Spanish and English.

    python charts/make_charts.py --lang es --out output/aws-ml-engineer-associate/data-quality-bias

Cada gráfico es una función independiente; los textos viven en TEXT[lang].
Each chart is an independent function; on-screen text lives in TEXT[lang].
"""

import os

import numpy as np

from style import ACCENT, DPI, GRAY, INK, INK_SOFT, MUTED, OK, RULE, WIDTH_IN, clean_axes, cli, fmt, plt

TEXT = {
    "es": {
        "no_default": "Sin impago",
        "default": "Impago",
        "share": "% de solicitudes",
        "trap": "Predecir siempre «sin impago»:\naccuracy ≈ 91 %, recall = 0",
        "facet_a": "Faceta a\n(edad ≤ 60)",
        "facet_d": "Faceta d\n(edad > 60)",
        "rows": "Filas",
        "rate": "Tasa de impago (q)",
        "rows_title": "Representación",
        "rate_title": "Etiquetas positivas",
        "ci_formula": r"$\mathrm{CI} = \dfrac{n_a - n_d}{n_a + n_d} = +0{,}72$",
        "ci_note": "la faceta d está subrepresentada",
        "dpl_formula": r"$\mathrm{DPL} = q_a - q_d = -0{,}04$",
        "dpl_note": "la faceta d tiene más impagos",
        "income": "Ingreso anual",
        "count": "Solicitudes",
        "before": "Antes: outliers ×50 (escala logarítmica)",
        "after": "Después: recorte a los límites IQR",
        "bounds": "Límites IQR\n" + r"$Q_1 - 1{,}5\,\mathrm{IQR},\ \ Q_3 + 1{,}5\,\mathrm{IQR}$",
        "outliers": "outliers",
        "metric": "Valor en prueba",
        "metrics": ["Accuracy", "Balanced acc.", "Recall", "F1", "ROC AUC"],
        "models": ["Siempre «sin impago»", "XGBoost base", "scale_pos_weight=10,6", "SMOTE (solo train)"],
        "acc_note": "La accuracy esconde el problema:\ncompara recall, F1 y AUC",
        "decimal": ",",
    },
    "en": {
        "no_default": "No default",
        "default": "Default",
        "share": "% of applications",
        "trap": "Always predicting “no default”:\naccuracy ≈ 91%, recall = 0",
        "facet_a": "Facet a\n(age ≤ 60)",
        "facet_d": "Facet d\n(age > 60)",
        "rows": "Rows",
        "rate": "Default rate (q)",
        "rows_title": "Representation",
        "rate_title": "Positive labels",
        "ci_formula": r"$\mathrm{CI} = \dfrac{n_a - n_d}{n_a + n_d} = +0.72$",
        "ci_note": "facet d is underrepresented",
        "dpl_formula": r"$\mathrm{DPL} = q_a - q_d = -0.04$",
        "dpl_note": "facet d has more defaults",
        "income": "Annual income",
        "count": "Applications",
        "before": "Before: ×50 outliers (log scale)",
        "after": "After: clipped to IQR bounds",
        "bounds": "IQR bounds\n" + r"$Q_1 - 1.5\,\mathrm{IQR},\ \ Q_3 + 1.5\,\mathrm{IQR}$",
        "outliers": "outliers",
        "metric": "Test value",
        "metrics": ["Accuracy", "Balanced acc.", "Recall", "F1", "ROC AUC"],
        "models": ["Always “no default”", "XGBoost baseline", "scale_pos_weight=10.6", "SMOTE (train only)"],
        "acc_note": "Accuracy hides the problem:\ncompare recall, F1 and AUC",
        "decimal": ".",
    },
}


# ─── 1. Desbalance de clases / class imbalance ─────────────────────────────────
def chart_class_imbalance(t, out):
    shares = [91.4, 8.6]
    labels = [t["no_default"], t["default"]]

    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.2), dpi=DPI)
    bars = ax.barh(labels, shares, color=[GRAY, ACCENT], height=0.5, zorder=3)
    for b, v in zip(bars, shares):
        ax.text(v + 1.2, b.get_y() + b.get_height() / 2, fmt(v, t, suffix=" %" if t["decimal"] == "," else "%"),
                va="center", fontsize=12, fontweight="bold", color=INK)
    ax.text(26, 1, t["trap"], fontsize=10, color=INK_SOFT, va="center")
    ax.set_xlim(0, 105)
    ax.set_xlabel(t["share"])
    ax.invert_yaxis()
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, labelsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "class-imbalance.png"))
    plt.close(fig)


# ─── 2. Sesgo pre-training: CI y DPL / pre-training bias ───────────────────────
def chart_bias_ci_dpl(t, out):
    facets = [t["facet_a"], t["facet_d"]]
    rows = [8582, 1403]
    rates = [0.081, 0.122]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH_IN, 4.6), dpi=DPI)

    b1 = ax1.bar(facets, rows, color=[GRAY, ACCENT], width=0.55, zorder=3)
    for b, v in zip(b1, rows):
        ax1.text(b.get_x() + b.get_width() / 2, v + 180, f"{v:,}".replace(",", "." if t["decimal"] == "," else ","),
                 ha="center", fontsize=11, fontweight="bold")
    ax1.set_ylim(0, 13500)
    ax1.set_title(t["rows_title"], fontsize=11.5, color=INK, pad=10, fontweight="bold")
    ax1.set_ylabel(t["rows"])
    ax1.text(0.97, 0.97, t["ci_formula"], transform=ax1.transAxes, ha="right", va="top", fontsize=13, color=ACCENT)
    ax1.text(0.97, 0.79, t["ci_note"], transform=ax1.transAxes, ha="right", va="top", fontsize=9, color=INK_SOFT)
    clean_axes(ax1)

    b2 = ax2.bar(facets, rates, color=[GRAY, ACCENT], width=0.55, zorder=3)
    for b, v in zip(b2, rates):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.004, fmt(v, t, 3), ha="center", fontsize=11, fontweight="bold")
    ax2.set_ylim(0, 0.2)
    ax2.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 3))
    ax2.set_title(t["rate_title"], fontsize=11.5, color=INK, pad=10, fontweight="bold")
    ax2.set_ylabel(t["rate"])
    ax2.text(0.03, 0.97, t["dpl_formula"], transform=ax2.transAxes, ha="left", va="top", fontsize=13, color=ACCENT)
    ax2.text(0.03, 0.86, t["dpl_note"], transform=ax2.transAxes, ha="left", va="top", fontsize=9, color=INK_SOFT)
    clean_axes(ax2)

    fig.tight_layout(w_pad=3)
    fig.savefig(os.path.join(out, "bias-ci-dpl.png"))
    plt.close(fig)


# ─── 3. Outliers y recorte IQR / outliers and IQR clipping ─────────────────────
def chart_outliers_iqr(t, out):
    rng = np.random.default_rng(7)
    income = rng.lognormal(mean=10.6, sigma=0.5, size=3000)
    extremes = rng.choice(income.size, 12, replace=False)
    income[extremes] *= 50
    q1, q3 = np.percentile(income, [25, 75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    clipped = np.clip(income, low, high)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH_IN, 5.6), dpi=DPI, sharex=False)
    k = 1000

    ax1.scatter(income / k, rng.uniform(-0.35, 0.35, income.size), s=6, color=GRAY, alpha=0.7, lw=0, zorder=2)
    ax1.scatter(income[extremes] / k, rng.uniform(-0.35, 0.35, extremes.size), s=22, color=ACCENT, zorder=3,
                label=t["outliers"])
    ax1.set_xscale("log")
    ax1.xaxis.set_major_formatter(lambda v, _: f"{v:,.0f}k".replace(",", "." if t["decimal"] == "," else ","))
    ax1.axvline(high / k, color=INK, lw=1, ls=(0, (3, 2)))
    ax1.text(high / k * 1.12, 0.46, t["bounds"], fontsize=8.5, color=INK_SOFT, va="top")
    ax1.set_title(t["before"], fontsize=11, loc="left", color=INK, fontweight="bold")
    ax1.set_yticks([])
    ax1.set_ylim(-0.5, 0.5)
    ax1.legend(frameon=False, loc="lower right", fontsize=9)
    clean_axes(ax1)
    ax1.spines["left"].set_visible(False)

    ax2.hist(clipped / k, bins=50, color=INK_SOFT, alpha=0.85, zorder=2)
    ax2.axvline(high / k, color=INK, lw=1, ls=(0, (3, 2)))
    if low > 0:  # con datos sesgados el límite inferior suele ser negativo / often negative on skewed data
        ax2.axvline(low / k, color=INK, lw=1, ls=(0, (3, 2)))
    ax2.set_title(t["after"], fontsize=11, loc="left", color=INK, fontweight="bold")
    ax2.set_xlabel(f"{t['income']} (k)")
    ax2.set_ylabel(t["count"])
    clean_axes(ax2)

    fig.tight_layout(h_pad=2)
    fig.savefig(os.path.join(out, "outliers-iqr.png"))
    plt.close(fig)


# ─── 4. Métricas por estrategia (resultados del laboratorio) / metrics per strategy ──
def chart_imbalance_metrics(t, out):
    # Fuente: ml-academy-labs data-quality-bias, conjunto de prueba (no remuestreado).
    values = np.array(
        [
            [0.914, 0.500, 0.000, 0.000, 0.500],
            [0.915, 0.530, 0.064, 0.115, 0.720],
            [0.732, 0.656, 0.564, 0.266, 0.709],
            [0.688, 0.637, 0.576, 0.241, 0.696],
        ]
    )
    colors = [GRAY, MUTED, ACCENT, OK]
    n_models, n_metrics = values.shape
    x = np.arange(n_metrics)
    width = 0.2

    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.6), dpi=DPI)
    for i in range(n_models):
        ax.bar(x + (i - 1.5) * width, values[i], width=width * 0.92, color=colors[i], label=t["models"][i], zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(t["metrics"], fontsize=10)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel(t["metric"])
    ax.yaxis.grid(True, color=RULE, lw=0.6, zorder=0)
    ax.text(2.0, 1.03, t["acc_note"], ha="center", fontsize=9, color=ACCENT, va="center")
    clean_axes(ax)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, fontsize=8.6,
              handlelength=1.1)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "imbalance-metrics.png"))
    plt.close(fig)


CHARTS = [chart_class_imbalance, chart_bias_ci_dpl, chart_outliers_iqr, chart_imbalance_metrics]


if __name__ == "__main__":
    cli(TEXT, CHARTS)
