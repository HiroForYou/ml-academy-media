"""
Tema 4.1: monitorear la inferencia y el rendimiento. Topic 4.1: monitor inference and performance.

    python charts/topics/monitoring-inference.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, icon_node, place_icon, plt, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "lat_title": "La latencia p99 se duplicó, pero el modelo no cambió",
        "hours": "Hora del día",
        "lat_ms": "Latencia p99 (ms)",
        "model_lat": "ModelLatency (dentro del contenedor)",
        "overhead": "OverheadLatency (ruta de SageMaker)",
        "payload": "el payload crece al doble",
        "lat_read": "ModelLatency estable → el cuello de botella\nno es el código del modelo",
        "lat_note": "Ilustrativo · CloudWatch publica ambas métricas en microsegundos",
        "an_title": "Umbral fijo vs. banda de anomaly detection sobre Invocations",
        "day": "Día",
        "inv": "Invocations por hora (miles)",
        "band": "Banda esperada (aprende tendencia y estacionalidad)",
        "static": "Umbral fijo",
        "false_alarm": "falsas alarmas en cada pico diario",
        "real": "caída real: dentro del umbral fijo,\nfuera de la banda → alarma",
        "an_note": "Ilustrativo · el modelo de anomaly detection se entrena con hasta 2 semanas de datos",
        "days": ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"],
        "drift_title": "Deriva de datos: producción (últimos 3 días) frente a la baseline de entrenamiento",
        "age": "customer_age (años)",
        "share": "Proporción de registros",
        "baseline": "Baseline (entrenamiento)",
        "prod": "Producción (últimos 3 días)",
        "psi_by": "PSI por feature",
        "large": "cambio grande",
        "stable": "estable",
        "rule": "0,2: regla práctica, no es un límite de AWS",
        "drift_note": "Datos sintéticos; PSI del caso de ejemplo · la deriva indica qué investigar, no prueba que la calidad bajó",
        "inv_title": "Tras la campaña: cuatro comprobaciones antes de promover un modelo nuevo",
        "steps": [
            ("1 · ¿Falla el servicio?",
             "5XX y 4XX planos, ModelLatency normal. Invocations +40 %, dentro de la banda de anomaly detection",
             "Servicio sano"),
            ("2 · ¿Cambiaron los datos?",
             "PSI frente al baseline:\ncustomer_age 0,31\ndays_since_signup 0,42\nbasket_value 0,04",
             "Drift en 2 features"),
            ("3 · ¿Bajó la calidad?",
             "A los 7 días, con las compras: precision@5 de clientes nuevos 0,21 → 0,12; recurrentes sin cambio",
             "Cae un segmento"),
            ("4 · ¿El modelo nuevo es mejor?",
             "A/B una semana: igual latencia y errores; mejor métrica de negocio en candidate",
             "Promover"),
        ],
        "shift": "Paso 4 · pesos current / candidate con UpdateEndpointWeightsAndCapacities, sin redesplegar el endpoint",
        "current": "current",
        "candidate": "candidate",
        "inv_note": "Cifras del caso de ejemplo",
        "obs_title": "CloudWatch sirve para operar; Quick Sight, para informar al negocio",
        "obs_op": "Operar",
        "obs_biz": "Negocio",
        "obs_ep": "Endpoint SageMaker AI\nmétricas y logs",
        "obs_inst": "EC2 u on-premises\nagente de CloudWatch",
        "obs_app": "Aplicación\nlogs de archivo",
        "obs_cw": "CloudWatch\nMétricas\nLogs\nAlarmas",
        "obs_li": "Logs Insights\nconsultas sobre los logs",
        "obs_dash": "Dashboard\nmétricas, alarmas y consultas",
        "obs_direct": "métricas y alarmas",
        "obs_data": "Predicciones y etiquetas\nguardadas en S3",
        "obs_athena": "se consultan con Athena",
        "obs_quick": "Amazon Quick Sight\nKPIs del negocio",
        "obs_note": "Esquema simplificado del flujo",
    },
    "en": {
        "decimal": ".",
        "lat_title": "p99 latency doubled, but the model did not change",
        "hours": "Hour of day",
        "lat_ms": "p99 latency (ms)",
        "model_lat": "ModelLatency (inside the container)",
        "overhead": "OverheadLatency (SageMaker path)",
        "payload": "payload size doubles",
        "lat_read": "ModelLatency is flat → the bottleneck\nis not the model code",
        "lat_note": "Illustrative · CloudWatch publishes both metrics in microseconds",
        "an_title": "Static threshold vs. anomaly detection band on Invocations",
        "day": "Day",
        "inv": "Invocations per hour (thousands)",
        "band": "Expected band (learns trend and seasonality)",
        "static": "Static threshold",
        "false_alarm": "false alarms at every daily peak",
        "real": "real drop: inside the static threshold,\noutside the band → alarm",
        "an_note": "Illustrative · the anomaly detection model trains on up to 2 weeks of data",
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "drift_title": "Data drift: production (last 3 days) against the training baseline",
        "age": "customer_age (years)",
        "share": "Share of records",
        "baseline": "Baseline (training)",
        "prod": "Production (last 3 days)",
        "psi_by": "PSI per feature",
        "large": "large shift",
        "stable": "stable",
        "rule": "0.2: rule of thumb, not an AWS limit",
        "drift_note": "Synthetic data; PSI from the worked example · drift tells you what to investigate, not that quality dropped",
        "inv_title": "After the campaign: four checks before promoting a new model",
        "steps": [
            ("1 · Is the service failing?",
             "5XX and 4XX flat, ModelLatency normal. Invocations +40%, inside the anomaly detection band",
             "Service healthy"),
            ("2 · Did the data change?",
             "PSI against the baseline:\ncustomer_age 0.31\ndays_since_signup 0.42\nbasket_value 0.04",
             "Drift in 2 features"),
            ("3 · Did quality drop?",
             "After 7 days, with purchases: new-customer precision@5 0.21 → 0.12; returning unchanged",
             "One segment drops"),
            ("4 · Is the new model better?",
             "One-week A/B: same latency and errors; better business metric for candidate",
             "Promote"),
        ],
        "shift": "Step 4 · current / candidate weights with UpdateEndpointWeightsAndCapacities, no endpoint redeploy",
        "current": "current",
        "candidate": "candidate",
        "inv_note": "Figures from the worked example",
        "obs_title": "CloudWatch is for operating; Quick Sight is for informing the business",
        "obs_op": "Operate",
        "obs_biz": "Business",
        "obs_ep": "SageMaker AI endpoint\nmetrics and logs",
        "obs_inst": "EC2 or on premises\nCloudWatch agent",
        "obs_app": "Application\nfile logs",
        "obs_cw": "CloudWatch\nMetrics\nLogs\nAlarms",
        "obs_li": "Logs Insights\nqueries over the logs",
        "obs_dash": "Dashboard\nmetrics, alarms and queries",
        "obs_direct": "metrics and alarms",
        "obs_data": "Predictions and labels\nstored in S3",
        "obs_athena": "queried with Athena",
        "obs_quick": "Amazon Quick Sight\nbusiness KPIs",
        "obs_note": "Simplified flow",
    },
}


# ─── 1. ModelLatency vs OverheadLatency ─────────────────────────────────────────
def chart_latency_breakdown(t, out):
    hours = np.linspace(0, 24, 97)
    rng = np.random.default_rng(7)
    model = 42 + rng.normal(0, 1.2, hours.size)
    step = 1 / (1 + np.exp(-(hours - 12) * 2.2))
    overhead = 12 + 46 * step + rng.normal(0, 1.0, hours.size)

    fig, ax = figure(4.0)
    ax.fill_between(hours, 0, model, color=GRAY, alpha=0.9, lw=0, label=t["model_lat"])
    ax.fill_between(hours, model, model + overhead, color=ACCENT, alpha=0.85, lw=0, label=t["overhead"])
    ax.plot(hours, model + overhead, color=INK, lw=1.2)
    ax.axvline(12, color=INK_SOFT, lw=1, ls=(0, (3, 2)))
    ax.text(12.3, 118, t["payload"], fontsize=8.8, color=INK_SOFT, va="top")
    ax.text(23.6, 20, t["lat_read"], fontsize=8.8, color=INK, ha="right", va="center")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 125)
    ax.set_xticks(range(0, 25, 4))
    ax.xaxis.set_major_formatter(lambda v, _: f"{int(v):02d}:00")
    ax.set_xlabel(t["hours"])
    ax.set_ylabel(t["lat_ms"])
    ax.set_title(t["lat_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper left", fontsize=8.8)
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["lat_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "latency-breakdown")


# ─── 2. Anomaly detection vs umbral fijo / anomaly band vs static threshold ────
def chart_anomaly_band(t, out):
    h = np.arange(0, 7 * 24)
    day, hod = h // 24, h % 24
    weekend = (day >= 5).astype(float)
    daily = np.exp(-((hod - 14) ** 2) / 18)
    expected = (8 + 22 * daily) * (1 - 0.35 * weekend)
    rng = np.random.default_rng(11)
    actual = expected + rng.normal(0, 1.0, h.size)
    # Caída real el jueves al mediodía. Real drop on Thursday at midday.
    drop = (day == 3) & (hod >= 12) & (hod <= 15)
    actual[drop] = expected[drop] * 0.35
    width = 2.5 + 0.12 * expected
    lower, upper = expected - width, expected + width
    static = 26

    fig, ax = figure(4.2)
    ax.fill_between(h, lower, upper, color=OK, alpha=0.16, lw=0, label=t["band"])
    ax.plot(h, actual, color=INK, lw=1.2)
    ax.axhline(static, color=AMBER, lw=1.6, label=t["static"])
    over = actual > static
    ax.scatter(h[over], actual[over], color=AMBER, s=10, zorder=4)
    out_band = (actual < lower) | (actual > upper)
    ax.scatter(h[out_band], actual[out_band], color=ACCENT, s=18, zorder=5)
    peak = int(np.argmax(np.where(day == 1, actual, 0)))
    ax.annotate(t["false_alarm"], xy=(peak, actual[peak]), xytext=(peak + 4, 41), fontsize=8.6, color=INK_SOFT,
                ha="center",
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1))
    i = int(np.flatnonzero(drop)[1])
    ax.annotate(t["real"], xy=(i, actual[i]), xytext=(i - 2, 40), fontsize=8.6, color=ACCENT, va="bottom",
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1))
    ax.set_xlim(0, h[-1])
    ax.set_ylim(0, 52)
    ax.set_xticks(np.arange(12, 7 * 24, 24))
    ax.set_xticklabels(t["days"])
    for d in range(1, 7):
        ax.axvline(d * 24, color=RULE, lw=0.6)
    ax.set_ylabel(t["inv"])
    ax.set_title(t["an_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper left", fontsize=8.6, ncol=2, bbox_to_anchor=(0, 1.02))
    clean_axes(ax)
    fig.text(0.99, 0.01, t["an_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "anomaly-band")


# ─── 3. Deriva con PSI / drift with PSI ────────────────────────────────────────
def _psi(base, prod, edges):
    p = np.histogram(base, edges)[0] / len(base)
    q = np.histogram(prod, edges)[0] / len(prod)
    p, q = np.clip(p, 1e-4, None), np.clip(q, 1e-4, None)
    return float(np.sum((q - p) * np.log(q / p)))


def _age_samples(target=0.31):
    rng = np.random.default_rng(5)
    base = rng.normal(41, 11, 20000).clip(18, 80)
    noise = rng.normal(0, 1, 6000)
    edges = np.quantile(base, np.linspace(0, 1, 11))
    edges[0], edges[-1] = 0, 200
    lo, hi = 0.0, 1.0
    for _ in range(40):  # mezcla de clientes jóvenes hasta PSI ≈ objetivo / young-customer mix until PSI ≈ target
        mix = (lo + hi) / 2
        young = (np.arange(6000) < mix * 6000)
        prod = np.where(young, 25 + 4 * noise, 41 + 11 * noise).clip(18, 80)
        if _psi(base, prod, edges) < target:
            lo = mix
        else:
            hi = mix
    return base, prod, edges


def chart_drift_psi(t, out):
    base, prod, edges = _age_samples()
    psi_age = _psi(base, prod, edges)
    fig = plt.figure(figsize=(WIDTH_IN, 4.1), dpi=DPI)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1], wspace=0.6)
    ax, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    bins = np.arange(18, 82, 3)
    ax.hist(base, bins, weights=np.full(base.size, 1 / base.size), color=GRAY, label=t["baseline"])
    ax.hist(prod, bins, weights=np.full(prod.size, 1 / prod.size), histtype="step", color=ACCENT, lw=2,
            label=t["prod"])
    ax.text(0.97, 0.42, rf"$PSI=\sum_i (q_i-p_i)\,\ln\frac{{q_i}}{{p_i}}$", transform=ax.transAxes, ha="right",
            fontsize=10.5, color=INK, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.text(0.97, 0.3, "PSI = " + fmt(psi_age, t, 2), transform=ax.transAxes, ha="right", fontsize=10,
            fontweight="bold", color=ACCENT)
    ax.set_xlabel(t["age"])
    ax.set_ylabel(t["share"])
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v * 100, t, 0, " %" if t["decimal"] == "," else "%"))
    ax.legend(frameon=False, fontsize=8.4, loc="upper right")
    clean_axes(ax)

    feats = ["customer_age", "days_since_signup", "basket_value"]
    vals = [0.31, 0.42, 0.04]
    colors = [ACCENT, ACCENT, OK]
    y = np.arange(3)
    ax2.barh(y, vals, color=colors, height=0.55, zorder=3)
    for yi, v in zip(y, vals):
        ax2.text(v + 0.01, yi, fmt(v, t, 2) + "  " + (t["large"] if v > 0.2 else t["stable"]), va="center",
                 fontsize=8.8, color=INK, bbox=dict(fc="white", ec="none", pad=0.5), zorder=4)
    ax2.axvline(0.2, color=INK_SOFT, lw=1, ls=(0, (3, 2)))
    ax2.text(0.21, 1.5, t["rule"], fontsize=7.6, color=MUTED, va="center")
    ax2.set_yticks(y)
    ax2.set_yticklabels(feats, fontsize=9)
    ax2.invert_yaxis()
    ax2.set_ylim(2.75, -0.5)
    ax2.set_xlim(0, 0.85)
    ax2.xaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    ax2.set_title(t["psi_by"], fontsize=10, loc="left", color=INK, fontweight="bold")
    clean_axes(ax2)
    ax2.spines["left"].set_visible(False)
    ax2.tick_params(left=False)

    fig.suptitle(t["drift_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["drift_note"], ha="right", fontsize=7.6, color=MUTED)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.86, bottom=0.17)
    save(fig, out, "drift-psi")


# ─── 4. Investigación del ejemplo / the worked example's investigation ─────────
def chart_quality_investigation(t, out):
    fig, ax = figure(4.5)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.06)
    diagram_axes(ax, 10, 6.1)
    results = [(OK, "white"), (AMBER, INK), (ACCENT, "white"), (OK, "white")]
    w, gap = 2.25, 0.27
    for i, ((title, body, result), (fill, color)) in enumerate(zip(t["steps"], results)):
        x = 0.05 + i * (w + gap)
        box(ax, x, 5.3, w, 0.75, title, edge="white", fill="white", size=9.6, weight="bold", lw=0)
        box(ax, x, 3.2, w, 2.0, body, edge=RULE, fill="white", size=9.2, color=INK_SOFT)
        box(ax, x, 2.5, w, 0.6, result, edge=fill, fill=fill, size=9.4, color=color, weight="bold")
        if i < 3:
            arrow(ax, (x + w + 0.03, 4.2), (x + w + gap - 0.03, 4.2), color=INK_SOFT)

    # Cambio de tráfico sin redesplegar / traffic shift without redeploying
    ax.text(0.05, 1.85, t["shift"], fontsize=9, color=INK, va="center")
    stages = [(90, 10), (50, 50), (0, 100)]
    bw, x0 = 2.4, 0.9
    for i, (cur, cand) in enumerate(stages):
        x = x0 + i * (bw + 0.8)
        ax.add_patch(plt.Rectangle((x, 0.45), bw * cur / 100, 0.5, color=GRAY, lw=0))
        ax.add_patch(plt.Rectangle((x + bw * cur / 100, 0.45), bw * cand / 100, 0.5, color=OK, lw=0))
        ax.text(x + bw / 2, 1.18, f"{cur} / {cand}", ha="center", va="center", fontsize=9.5, fontweight="bold",
                color=INK)
        if i < 2:
            arrow(ax, (x + bw + 0.14, 0.7), (x + bw + 0.66, 0.7), color=INK_SOFT)
    ax.text(x0, 0.2, "■ " + t["current"], fontsize=8.6, color=MUTED, va="center")
    ax.text(x0 + 1.4, 0.2, "■ " + t["candidate"], fontsize=8.6, color=OK, va="center")

    fig.suptitle(t["inv_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.012, t["inv_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "quality-investigation")


# ─── 5. Mapa de observabilidad / observability map ──────────────────────────────
def chart_observability_map(t, out):
    W, H = 32, 13
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.6), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.06)  # antes de los íconos / before icons
    diagram_axes(ax, W, H)
    gap, h = 0.08, 2.3
    rows = [9.6, 6.9, 4.2]
    node = dict(edge=RULE, fill=SURFACE, size=9, desc_size=7.8)

    fit_to(ax.text(0.2, 12.5, t["obs_op"], ha="left", va="bottom", fontsize=9, fontweight="bold", color=INK_SOFT), 8)
    icon_node(ax, 0.2, rows[0], 6.6, h, "aws/sagemaker-ai", t["obs_ep"], **node)
    icon_node(ax, 0.2, rows[1], 6.6, h, "aws/ec2", t["obs_inst"], **node)
    icon_node(ax, 0.2, rows[2], 6.6, h, "aws/application", t["obs_app"], **node)
    icon_node(ax, 9.4, rows[2], 6.0, rows[0] + h - rows[2], "aws/cloudwatch", t["obs_cw"], edge=INK_SOFT,
              fill="white", size=9.4, desc_size=8.2)
    icon_node(ax, 17.8, rows[1], 5.6, h, "aws/cloudwatch-logs", t["obs_li"], **node)
    icon_node(ax, 25.8, rows[2], 6.0, rows[0] + h - rows[2], "aws/cloudwatch", t["obs_dash"], edge=ACCENT,
              fill="white", size=9.4, desc_size=8.2)
    for r in rows:
        arrow(ax, (6.8 + gap, r + h / 2), (9.4 - gap, r + h / 2), color=INK_SOFT)
    ymid = rows[1] + h / 2
    arrow(ax, (15.4 + gap, ymid), (17.8 - gap, ymid), color=INK_SOFT)
    arrow(ax, (23.4 + gap, ymid), (25.8 - gap, ymid), color=INK_SOFT)
    arrow(ax, (15.4 + gap, rows[0] + h / 2), (25.8 - gap, rows[0] + h / 2), color=ACCENT)
    fit_to(ax.text(20.6, rows[0] + h / 2 + 0.3, t["obs_direct"], ha="center", va="bottom", fontsize=8.2,
                   color=ACCENT), 8)

    ax.plot([0.2, W - 0.2], [3.55, 3.55], color=GRAY, lw=1.0, ls=(0, (3, 3)))
    fit_to(ax.text(0.2, 2.75, t["obs_biz"], ha="left", va="bottom", fontsize=9, fontweight="bold", color=INK_SOFT), 8)
    # El carril de negocio replica el de operación: datos bajo las fuentes, Quick Sight bajo el dashboard.
    # The business lane mirrors the operations lane: data under the sources, Quick Sight under the dashboard.
    icon_node(ax, 0.2, 0.2, 6.6, 2.3, "aws/s3", t["obs_data"], **node)
    icon_node(ax, 25.8, 0.2, 6.0, 2.3, "aws/quick", t["obs_quick"], edge=INK_SOFT, fill="white", size=9.4,
              desc_size=8.2)
    arrow(ax, (6.8 + gap, 1.35), (25.8 - gap, 1.35), color=INK_SOFT)
    # Athena: ícono sobre la flecha, a la izquierda del texto. Athena icon on the arrow, left of the text.
    place_icon(ax, "aws/athena", 13.35, 1.35 + 0.62, 0.8)
    fit_to(ax.text(16.6, 1.35 + 0.3, t["obs_athena"], ha="center", va="bottom", fontsize=8.2, color=INK_SOFT), 9)

    fig.suptitle(t["obs_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.012, t["obs_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "observability-map")


CHARTS = [chart_latency_breakdown, chart_anomaly_band, chart_drift_psi, chart_quality_investigation,
          chart_observability_map]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
