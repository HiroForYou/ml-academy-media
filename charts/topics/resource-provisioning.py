"""
Tema 3.2: aprovisionar recursos de cómputo. Topic 3.2: provision compute resources.

    python charts/topics/resource-provisioning.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, icon_node, plt, save,
)

TEXT = {
    "es": {
        "decimal": ",",
        "thousands": ".",
        "hour": "Hora del día",
        "inv": "Invocaciones/min",
        "traffic": "Tráfico",
        "target_cap": "capacidad al objetivo (instancias × 700)",
        "sat_cap": "saturación medida (instancias × 1.000)",
        "inst": "Instancias",
        "sp": "base cubierta por Savings Plan",
        "od": "picos bajo demanda",
        "minmax": "MinCapacity = 2 · MaxCapacity = 6",
        "plan_title": "Target tracking con objetivo de 700 invocaciones por instancia",
        "plan_note": "Ilustrativo, idealizado: sin el retraso real del escalado",
        "req": "Solicitudes por día (miles)",
        "cost": "Costo diario relativo",
        "rt": "Endpoint real-time (1 instancia 24 h)",
        "rt_sp": "Real-time con Savings Plan (1 o 3 años)",
        "sl": "Serverless (pagas por tiempo de proceso)",
        "sl_zone": "tráfico esporádico:\nserverless",
        "rt_zone": "uso sostenido:\nreal-time + Savings Plan",
        "cost_title": "Serverless gana con poco tráfico; una instancia siempre encendida gana con uso sostenido",
        "cost_note": "Ilustrativo: forma de las curvas, sin precios reales",
        "time": "Tiempo (min:s)",
        "pct": "% del objetivo de la métrica",
        "burst": "ráfaga de solicitudes",
        "c10": "ConcurrentRequestsPerModel (cada 10 s)",
        "i60": "InvocationsPerInstance (cada 60 s)",
        "first": "primer dato sobre el objetivo",
        "target": "objetivo",
        "res_title": "Con streaming, la métrica de alta resolución detecta la ráfaga antes",
        "res_note": "Ilustrativo: respuestas de 30 s; el tráfico se duplica en 2:00",
        "dbc_title": "Cambiar un endpoint = una EndpointConfig nueva + UpdateEndpoint, sin cortar el servicio",
        "dbc_model": "Model\nECR · S3 · rol",
        "dbc_cfg": "EndpointConfig\nvariantes · instancias",
        "dbc_ep": "Endpoint\nHTTPS · InService",
        "dbc_app": "Aplicación\nsagemaker-runtime",
        "dbc_lane": "No se edita: se crea una EndpointConfig nueva",
        "dbc_cfg2": "EndpointConfig nueva\ntipo o número de instancias",
        "dbc_upd": "UpdateEndpoint\nUpdating → InService",
        "dbc_ok": "Sin pérdida de disponibilidad",
        "dbc_note": "Nombres de Boto3; la CLI usa los equivalentes con guiones",
    },
    "en": {
        "decimal": ".",
        "thousands": ",",
        "hour": "Hour of day",
        "inv": "Invocations/min",
        "traffic": "Traffic",
        "target_cap": "capacity at target (instances × 700)",
        "sat_cap": "measured saturation (instances × 1,000)",
        "inst": "Instances",
        "sp": "base covered by a Savings Plan",
        "od": "on-demand peaks",
        "minmax": "MinCapacity = 2 · MaxCapacity = 6",
        "plan_title": "Target tracking with a target of 700 invocations per instance",
        "plan_note": "Illustrative, idealized: no real scaling delay",
        "req": "Requests per day (thousands)",
        "cost": "Relative daily cost",
        "rt": "Real-time endpoint (1 instance, 24 h)",
        "rt_sp": "Real-time with a Savings Plan (1 or 3 years)",
        "sl": "Serverless (pay for processing time)",
        "sl_zone": "sporadic traffic:\nserverless",
        "rt_zone": "sustained use:\nreal-time + Savings Plan",
        "cost_title": "Serverless wins with little traffic; an always-on instance wins with sustained use",
        "cost_note": "Illustrative: curve shapes only, no real prices",
        "time": "Time (min:s)",
        "pct": "% of the metric target",
        "burst": "request burst",
        "c10": "ConcurrentRequestsPerModel (every 10 s)",
        "i60": "InvocationsPerInstance (every 60 s)",
        "first": "first datapoint above target",
        "target": "target",
        "res_title": "With streaming, the high-resolution metric detects the burst sooner",
        "res_note": "Illustrative: 30 s responses; traffic doubles at 2:00",
        "dbc_title": "Changing an endpoint = a new EndpointConfig + UpdateEndpoint, with no downtime",
        "dbc_model": "Model\nECR · S3 · role",
        "dbc_cfg": "EndpointConfig\nvariants · instances",
        "dbc_ep": "Endpoint\nHTTPS · InService",
        "dbc_app": "Application\nsagemaker-runtime",
        "dbc_lane": "You don't edit it: you create a new EndpointConfig",
        "dbc_cfg2": "New EndpointConfig\ninstance type or count",
        "dbc_upd": "UpdateEndpoint\nUpdating → InService",
        "dbc_ok": "No loss of availability",
        "dbc_note": "Boto3 names; the CLI uses the hyphenated equivalents",
    },
}


def _thousands(v, t):
    return f"{v:,.0f}".replace(",", t["thousands"])


def _title(ax, text):
    ax.set_title(text, fontsize=10.2, loc="left", color=INK, fontweight="bold")


# ─── 1. Plan de autoescalado del ejemplo / the example's auto scaling plan ─────
def chart_autoscaling_plan(t, out):
    h = np.linspace(0, 24, 24 * 12 + 1)
    traffic = 300 + 3700 * np.exp(-(((h - 12.5) / 3.3) ** 2))
    inst = np.clip(np.ceil(traffic / 700), 2, 6)

    fig, (a1, a2) = figure(5.0, nrows=2, sharex=True, gridspec_kw={"height_ratios": [1.7, 1]})
    a1.fill_between(h, 0, traffic, color=GRAY, alpha=0.45, lw=0, label=t["traffic"])
    a1.plot(h, traffic, color=INK_SOFT, lw=1.6)
    a1.step(h, inst * 700, where="post", color=OK, lw=2, label=t["target_cap"])
    a1.step(h, inst * 1000, where="post", color=ACCENT, lw=1.2, ls=(0, (3, 2)), label=t["sat_cap"])
    a1.set_ylim(0, 6600)
    a1.set_ylabel(t["inv"])
    a1.yaxis.set_major_formatter(lambda v, _: _thousands(v, t))
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")
    a1.yaxis.grid(True, color=RULE, lw=0.6)
    _title(a1, t["plan_title"])
    clean_axes(a1)

    a2.fill_between(h, 0, np.minimum(inst, 2), step="post", color=OK, alpha=0.85, lw=0, label=t["sp"])
    a2.fill_between(h, 2, inst, step="post", color=AMBER, alpha=0.9, lw=0, label=t["od"])
    a2.set_ylim(0, 7)
    a2.set_yticks([0, 2, 4, 6])
    a2.set_ylabel(t["inst"])
    a2.set_xlim(0, 24)
    a2.set_xticks(range(0, 25, 3))
    a2.set_xticklabels([f"{x}:00" for x in range(0, 25, 3)])
    a2.set_xlabel(t["hour"])
    a2.legend(frameon=False, fontsize=8.5, loc="upper left")
    a2.text(23.8, 6.2, t["minmax"], ha="right", fontsize=8.5, color=INK_SOFT)
    clean_axes(a2)
    fig.text(0.99, 0.01, t["plan_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "autoscaling-plan")


# ─── 2. Serverless frente a real-time / serverless versus real-time ────────────
def chart_serverless_vs_realtime(t, out):
    req = np.linspace(0, 1000, 200)
    realtime = np.full_like(req, 1.0)
    savings = np.full_like(req, 0.6)
    serverless = req / 380

    fig, ax = figure(4.0)
    ax.plot(req, serverless, color=OK, lw=2.4, label=t["sl"])
    ax.plot(req, realtime, color=INK_SOFT, lw=2.2, label=t["rt"])
    ax.plot(req, savings, color=INK_SOFT, lw=1.4, ls=(0, (4, 2)), label=t["rt_sp"])
    x_cross = 380
    ax.axvspan(0, 228, color=OK, alpha=0.07, lw=0)
    ax.axvspan(x_cross, 1000, color=GRAY, alpha=0.18, lw=0)
    ax.text(12, 1.55, t["sl_zone"], fontsize=8.8, color=OK, va="top")
    ax.text(990, 1.55, t["rt_zone"], fontsize=8.8, color=INK_SOFT, va="top", ha="right")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1.7)
    ax.set_yticks([])
    ax.set_xlabel(t["req"])
    ax.set_ylabel(t["cost"])
    ax.legend(frameon=False, fontsize=8.8, loc="lower right")
    _title(ax, t["cost_title"])
    clean_axes(ax)
    fig.text(0.99, 0.01, t["cost_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "serverless-vs-realtime")


# ─── 3. Resolución de la métrica / metric resolution ───────────────────────────
def chart_metric_resolution(t, out):
    rng = np.random.default_rng(2)
    dur, horizon = 30, 300
    base_rate = 2.0  # solicitudes por segundo / requests per second
    starts = []
    for s in range(-60, horizon):
        rate = base_rate * (2 if s >= 120 else 1)
        starts += list(s + rng.uniform(0, 1, rng.poisson(rate)))
    starts = np.array(starts)
    # Objetivo = 1,5 × la carga base. Target = 1.5 × the base load.
    conc_target = base_rate * dur * 1.5
    inv_target = base_rate * 60 * 1.5

    t10 = np.arange(10, horizon + 1, 10)
    conc = np.array([((starts <= x) & (starts + dur > x)).sum() for x in t10]) / conc_target * 100
    t60 = np.arange(60, horizon + 1, 60)
    inv = np.array([((starts > x - 60) & (starts <= x)).sum() for x in t60]) / inv_target * 100

    fig, ax = figure(4.0)
    ax.axvline(120, color=AMBER, lw=1.4)
    ax.text(122, 172, t["burst"], fontsize=8.5, color=INK_SOFT, va="top")
    ax.axhline(100, color=INK, lw=0.9, ls=(0, (2, 3)))
    ax.text(4, 103, t["target"], fontsize=8.4, color=INK_SOFT)
    ax.step(t60, inv, where="post", color=MUTED, lw=1.6)
    ax.scatter(t60, inv, color=MUTED, s=34, zorder=4, marker="s", label=t["i60"])
    ax.plot(t10, conc, color=ACCENT, lw=1.2, alpha=0.6)
    ax.scatter(t10, conc, color=ACCENT, s=16, zorder=4, label=t["c10"])
    fc = t10[np.argmax((conc > 100) & (t10 > 120))]
    fi = t60[np.argmax((inv > 100) & (t60 > 120))]
    # El texto gris va arriba del rojo para que su flecha no cruce el rojo. Grey label above the red one so
    # its arrow doesn't cross it.
    for x, col, y in ((fc, ACCENT, 40), (fi, MUTED, 62)):
        ax.annotate(f"{t['first']}: {x // 60}:{x % 60:02d}", xy=(x, 100), xytext=(x + (8 if col == ACCENT else 15), y),
                    fontsize=8.4, color=col, arrowprops=dict(arrowstyle="-|>", color=col, lw=0.9))
    ax.set_xlim(0, horizon)
    ax.set_ylim(0, 180)
    ax.set_xticks(range(0, horizon + 1, 60))
    ax.set_xticklabels([f"{x // 60}:{x % 60:02d}" for x in range(0, horizon + 1, 60)])
    ax.set_xlabel(t["time"])
    ax.set_ylabel(t["pct"])
    ax.legend(frameon=False, fontsize=8.6, loc="upper left")
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    _title(ax, t["res_title"])
    clean_axes(ax)
    fig.text(0.99, 0.01, t["res_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "metric-resolution")


# ─── 4. Desplegar e invocar por código / deploy and invoke by code ────────────
def chart_deploy_by_code(t, out):
    W, H = 32, 11.2
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 4.3), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.06)  # antes de los íconos / before icons
    diagram_axes(ax, W, H)
    h, top, bot, gap = 3.0, 6.7, 1.7, 0.08
    xs, ws = [0.2, 8.6, 17.4, 25.8], [7.0, 7.4, 7.0, 6.0]
    node = dict(edge=RULE, fill=SURFACE, size=9, desc_size=7.8)

    # Model = imagen (ECR) + artefacto (S3) + rol (IAM): cuadrícula de logos.
    # Model = image (ECR) + artifact (S3) + role (IAM): logo grid.
    icon_node(ax, xs[0], top, ws[0], h, ["aws/ecr", "aws/s3", "aws/iam-role", "aws/sagemaker-model"],
              t["dbc_model"], icon_size=1.75, **node)
    icon_node(ax, xs[1], top, ws[1], h, "aws/sagemaker-ai", t["dbc_cfg"], **node)
    icon_node(ax, xs[2], top, ws[2], h, "aws/sagemaker-ai", t["dbc_ep"], edge=INK_SOFT, fill="white", size=9,
              desc_size=7.8)
    icon_node(ax, xs[3], top, ws[3], h, "aws/application", t["dbc_app"], **node)
    ymid = top + h / 2
    for i in range(3):
        arrow(ax, (xs[i] + ws[i] + gap, ymid), (xs[i + 1] - gap, ymid), color=INK_SOFT)
    for x, w, call in zip(xs, ws, ("create_model", "create_endpoint_config", "create_endpoint", "invoke_endpoint")):
        fit_to(ax.text(x + w / 2, top + h + 0.5, call, ha="center", va="bottom", fontsize=8.4, color=MUTED,
                       family="monospace"), w)

    box(ax, xs[0], bot, ws[0], h, t["dbc_lane"], edge=RULE, fill="white", size=8.8, color=INK_SOFT)
    icon_node(ax, xs[1], bot, ws[1], h, "aws/sagemaker-ai", t["dbc_cfg2"], edge=ACCENT, fill="white", size=9,
              desc_size=7.8)
    icon_node(ax, xs[2], bot, ws[2], h, "aws/sagemaker-ai", t["dbc_upd"], edge=ACCENT, fill="white", size=9,
              desc_size=7.8)
    box(ax, xs[3], bot, ws[3], h, t["dbc_ok"], edge=OK, fill="#e3f1e9", size=9, color=OK, weight="bold")
    y2 = bot + h / 2
    arrow(ax, (xs[0] + ws[0] + gap, y2), (xs[1] - gap, y2), color=ACCENT)
    arrow(ax, (xs[1] + ws[1] + gap, y2), (xs[2] - gap, y2), color=ACCENT)
    arrow(ax, (xs[2] + ws[2] + gap, y2), (xs[3] - gap, y2), color=ACCENT)
    # UpdateEndpoint actúa sobre el mismo endpoint. UpdateEndpoint acts on the same endpoint.
    arrow(ax, (xs[2] + ws[2] / 2, bot + h + gap), (xs[2] + ws[2] / 2, top - gap), color=ACCENT)
    for x, w, call in ((xs[1], ws[1], "create_endpoint_config"), (xs[2], ws[2], "update_endpoint")):
        fit_to(ax.text(x + w / 2, bot - 0.5, call, ha="center", va="top", fontsize=8.4, color=MUTED,
                       family="monospace"), w)

    fig.suptitle(t["dbc_title"], x=0.01, ha="left", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.99, 0.012, t["dbc_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "deploy-by-code")


CHARTS = [chart_autoscaling_plan, chart_serverless_vs_realtime, chart_metric_resolution, chart_deploy_by_code]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
