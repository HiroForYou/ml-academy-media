"""
Gráficos del tema 1.3 (calidad de datos y sesgo), en español e inglés.
Charts for topic 1.3 (data quality and bias), in Spanish and English.

    python charts/make_charts.py --lang es --out output/aws-ml-engineer-associate/data-quality-bias

Cada gráfico es una función independiente; los textos viven en TEXT[lang].
Each chart is an independent function; on-screen text lives in TEXT[lang].
"""

import numpy as np
from matplotlib.patches import Rectangle

from style import ACCENT, DPI, GRAY, INK, INK_SOFT, MUTED, OK, RULE, WIDTH_IN, clean_axes, cli, fmt, plt, save

TEXT = {
    "es": {
        "no_default": "Sin impago",
        "default": "Impago",
        "share": "% de solicitudes",
        "trap": "Predecir siempre «sin impago»:\naccuracy ≈ 91 %, recall = 0",
        "dots_title": "1 punto = 1 de cada 100 solicitudes",
        "cm_rows": ["Real:\nsin impago", "Real:\nimpago"],
        "cm_cols": ["Predice\nsin impago", "Predice\nimpago"],
        "round_note": "Redondeado: 91,4 % ≈ 91 y 8,6 % ≈ 9 de cada 100",
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
        "dots_title": "1 dot = 1 in 100 applications",
        "cm_rows": ["Actual:\nno default", "Actual:\ndefault"],
        "cm_cols": ["Predicts\nno default", "Predicts\ndefault"],
        "round_note": "Rounded: 91.4% ≈ 91 and 8.6% ≈ 9 in 100",
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

    fig = plt.figure(figsize=(WIDTH_IN, 5.0), dpi=DPI)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.05], height_ratios=[1, 1.15], hspace=0.28, wspace=0.12,
                          left=0.14, right=0.985, top=0.96, bottom=0.18)

    # Barras: lo que ya se veía / the bars as before
    ax = fig.add_subplot(gs[:, 0])
    bars = ax.barh(labels, shares, color=[GRAY, ACCENT], height=0.5, zorder=3)
    for b, v in zip(bars, shares):
        ax.text(v + 1.5, b.get_y() + b.get_height() / 2, fmt(v, t, suffix=" %" if t["decimal"] == "," else "%"),
                va="center", fontsize=12, fontweight="bold", color=INK)
    ax.set_xlim(0, 128)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel(t["share"])
    ax.invert_yaxis()
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, labelsize=11)

    # Cuadrícula de 100 solicitudes, 9 con impago / grid of 100 applications, 9 defaults
    axd = fig.add_subplot(gs[0, 1])
    rng = np.random.default_rng(7)
    bad = set(rng.choice(100, 9, replace=False).tolist())
    xs, ys = np.meshgrid(np.arange(10), np.arange(9, -1, -1))
    cols = [ACCENT if i in bad else GRAY for i in range(100)]
    axd.scatter(xs.ravel(), ys.ravel(), s=46, c=cols, linewidths=0, zorder=3)
    axd.set_xlim(-0.8, 9.8)
    axd.set_ylim(-0.7, 10.9)
    axd.axis("off")
    axd.text(4.5, 10.6, t["dots_title"], ha="center", va="center", fontsize=9.5, color=INK_SOFT, fontweight="bold")

    # Matriz de confusión de «siempre sin impago» / confusion matrix of "always no default"
    axc = fig.add_subplot(gs[1, 1])
    axc.set_xlim(0, 4.6)
    axc.set_ylim(0, 4.0)
    axc.axis("off")
    cw, ch, x0, y0 = 1.35, 0.8, 1.6, 1.15
    cells = [[("91", GRAY, INK), ("0", "white", MUTED)], [("9", ACCENT, "white"), ("0", "white", MUTED)]]
    for r in range(2):
        for c in range(2):
            label, fill, fg = cells[r][c]
            axc.add_patch(Rectangle((x0 + c * (cw + 0.08), y0 + (1 - r) * (ch + 0.08)), cw, ch, facecolor=fill,
                                    edgecolor=ACCENT if (r == 1 and c == 1) else GRAY, linewidth=1.4, zorder=2))
            axc.text(x0 + c * (cw + 0.08) + cw / 2, y0 + (1 - r) * (ch + 0.08) + ch / 2, label, ha="center",
                     va="center", fontsize=13, fontweight="bold", color=fg, zorder=3)
        axc.text(x0 - 0.12, y0 + (1 - r) * (ch + 0.08) + ch / 2, t["cm_rows"][r], ha="right", va="center",
                 fontsize=8.5, color=INK_SOFT, multialignment="right")
    for c in range(2):
        axc.text(x0 + c * (cw + 0.08) + cw / 2, y0 + 2 * ch + 0.08 + 0.14, t["cm_cols"][c], ha="center", va="bottom",
                 fontsize=8.5, color=INK_SOFT, multialignment="center")
    axc.text(x0 + cw + 0.04, 0.55, t["trap"], ha="center", va="center", fontsize=9.5, fontweight="bold",
             color=ACCENT, multialignment="center")

    fig.text(0.14, 0.035, t["round_note"], fontsize=8.5, color=MUTED, va="center")
    save(fig, out, "class-imbalance")


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
    save(fig, out, "bias-ci-dpl")


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
    save(fig, out, "outliers-iqr")


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
    save(fig, out, "imbalance-metrics")


CHARTS = [chart_class_imbalance, chart_bias_ci_dpl, chart_outliers_iqr, chart_imbalance_metrics]


if __name__ == "__main__":
    cli(TEXT, CHARTS)
