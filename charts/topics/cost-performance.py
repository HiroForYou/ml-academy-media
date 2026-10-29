"""
Tema 4.2: optimizar costo y rendimiento. Topic 4.2: optimize cost and performance.

    python charts/topics/cost-performance.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, place_icon, plt, save,
    _y_to_x,
)

TEXT = {
    "es": {
        "decimal": ",",
        "eb_title": "Un trabajo diario en un endpoint 24/7 paga capacidad ociosa",
        "endpoint": "Endpoint en tiempo real 24/7",
        "batch": "Batch Transform a las 02:00",
        "instances": "Instancias",
        "hour": "Hora del día",
        "work": "trabajo real (02:00–03:30)",
        "idle": "ociosas: Invocations = 0",
        "ih_ep": "48 instancia-hora/día",
        "ih_bt": "≈ 3 instancia-hora/día (−94 %)",
        "eb_note": "Caso de ejemplo: 2 × ml.m5.xlarge, 1,5 millones de facturas, entrega a las 07:00",
        "deadline": "entrega 07:00",
        "cp_title": "Inference Recommender: la opción más barata por hora no es la más barata por predicción",
        "p95": "Latencia p95 bajo carga (ms)",
        "cpm": "Costo por millón de predicciones (USD)",
        "slo": "objetivo p95 = 200 ms",
        "best": "elegida: cumple la p95 con el menor costo por predicción",
        "options": ["A · CPU pequeña", "B · CPU mediana", "C · CPU grande", "D · GPU"],
        "per_hour": "USD/h",
        "rps": "solic./s",
        "cp_note": "Ilustrativo: costo por millón = precio por hora ÷ (solicitudes/s × 3600) × 10⁶",
        "sp_title": "Savings Plans: comprometer solo el uso base que queda tras quitar el desperdicio",
        "usage": "Gasto por hora en SageMaker AI (USD/h)",
        "day": "Día",
        "covered": "Cubierto por el compromiso (tarifa del Savings Plan)",
        "ondemand": "Excedente a tarifa On-Demand",
        "commit": "compromiso = uso base",
        "over": "sobrecompromiso: la parte no usada se paga igual",
        "sp_note": "Ilustrativo · el compromiso es en USD/h durante 1 o 3 años",
        "days": ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"],
        "ex_title": "Ejemplo: de la señal en CloudWatch al ahorro, en cuatro pasos",
        "ex_steps": [
            ("Paso 1 · Medir", "CloudWatch: Invocations = 0 unas 22 h al día"),
            ("Paso 2 · Cambiar el modo", "Batch Transform a las 02:00, mismo modelo, 2 × ml.m5.xlarge"),
            ("Paso 3 · Comparar", "Misma unidad: termina a las 03:30 con las mismas predicciones"),
            ("Paso 4 · Limitar el gasto", "Tag project=invoice-risk y AWS Budgets con alerta al 80 %"),
        ],
        "ex_unit": "Horas-instancia al día",
        "ex_bars": ["Endpoint 24/7", "Batch Transform"],
        "ex_vals": ["48 (24 h × 2)", "≈ 3 (1,5 h × 2)"],
        "ex_drop": "−94 % horas-instancia, sin cambiar modelo, instancia ni tarifa",
        "ex_note": "Caso del ejemplo · convierte las horas-instancia en dinero con los precios de tu región",
        "ct_title": "Cada herramienta de costo responde una pregunta distinta",
        "ct_cost": "costos",
        "ct_ta": ["Optimización de costos", "Rendimiento", "Seguridad", "Tolerancia a fallos", "Límites de servicio",
                  "Excelencia operacional"],
        "ct_normal": "uso normal",
        "ct_cards": [
            ("Cost allocation tags", "¿De qué proyecto es el gasto?", "activar para filtrar"),
            ("Cost Explorer", "¿Dónde se va el gasto?", "13 meses + pronóstico"),
            ("AWS Budgets", "¿Cómo me aviso al pasar un umbral?", "umbral → alerta"),
            ("Trusted Advisor", "¿Qué buena práctica incumplo?", ""),
            ("Compute Optimizer", "¿Qué endpoint está ocioso?", "0 invocaciones · 14 días"),
            ("Service Quotas", "¿Puedo lanzar más instancias?", "pedir aumento antes"),
        ],
    },
    "en": {
        "decimal": ".",
        "eb_title": "A daily job on a 24/7 endpoint pays for idle capacity",
        "endpoint": "24/7 real-time endpoint",
        "batch": "Batch Transform at 02:00",
        "instances": "Instances",
        "hour": "Hour of day",
        "work": "real work (02:00–03:30)",
        "idle": "idle: Invocations = 0",
        "ih_ep": "48 instance-hours/day",
        "ih_bt": "≈ 3 instance-hours/day (−94%)",
        "eb_note": "Worked example: 2 × ml.m5.xlarge, 1.5 million invoices, due at 07:00",
        "deadline": "due 07:00",
        "cp_title": "Inference Recommender: cheapest per hour is not cheapest per prediction",
        "p95": "p95 latency under load (ms)",
        "cpm": "Cost per million predictions (USD)",
        "slo": "p95 target = 200 ms",
        "best": "chosen: meets p95 at the lowest cost per prediction",
        "options": ["A · small CPU", "B · medium CPU", "C · large CPU", "D · GPU"],
        "per_hour": "USD/h",
        "rps": "req/s",
        "cp_note": "Illustrative: cost per million = hourly price ÷ (requests/s × 3600) × 10⁶",
        "sp_title": "Savings Plans: commit only to the baseline left after removing waste",
        "usage": "SageMaker AI spend per hour (USD/h)",
        "day": "Day",
        "covered": "Covered by the commitment (Savings Plan rate)",
        "ondemand": "Excess at the On-Demand rate",
        "commit": "commitment = baseline",
        "over": "over-commitment: the unused part is still paid",
        "sp_note": "Illustrative · the commitment is in USD/h for 1 or 3 years",
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "ex_title": "Example: from a CloudWatch signal to savings, in four steps",
        "ex_steps": [
            ("Step 1 · Measure", "CloudWatch: Invocations = 0 for about 22 h a day"),
            ("Step 2 · Change the mode", "Batch Transform at 02:00, same model, 2 × ml.m5.xlarge"),
            ("Step 3 · Compare", "Same unit: finishes at 03:30 with the same predictions"),
            ("Step 4 · Limit spend", "Tag project=invoice-risk and AWS Budgets alert at 80%"),
        ],
        "ex_unit": "Instance-hours per day",
        "ex_bars": ["24/7 endpoint", "Batch Transform"],
        "ex_vals": ["48 (24 h × 2)", "≈ 3 (1.5 h × 2)"],
        "ex_drop": "−94% instance-hours, without changing the model, instance or rate",
        "ex_note": "Worked example · turn instance-hours into money with your Region's prices",
        "ct_title": "Each cost tool answers a different question",
        "ct_cost": "cost",
        "ct_ta": ["Cost optimization", "Performance", "Security", "Fault tolerance", "Service limits",
                  "Operational excellence"],
        "ct_normal": "normal use",
        "ct_cards": [
            ("Cost allocation tags", "Which project is the spend from?", "activate to filter"),
            ("Cost Explorer", "Where is the spend going?", "13 months + forecast"),
            ("AWS Budgets", "How do I get alerted at a threshold?", "threshold → alert"),
            ("Trusted Advisor", "Which best practice am I missing?", ""),
            ("Compute Optimizer", "Which endpoint is idle?", "0 invocations · 14 days"),
            ("Service Quotas", "Can I launch more instances?", "request an increase first"),
        ],
    },
}


# ─── 1. Endpoint 24/7 vs Batch Transform ───────────────────────────────────────
def chart_endpoint_vs_batch(t, out):
    fig, (ax1, ax2) = figure(4.4, nrows=2, sharex=True)
    h = np.linspace(0, 24, 2401)
    work = (h >= 2) & (h <= 3.5)
    for ax, name, inst, text in ((ax1, t["endpoint"], np.full_like(h, 2), t["ih_ep"]),
                                 (ax2, t["batch"], np.where(work, 2, 0), t["ih_bt"])):
        ax.fill_between(h, 0, inst, where=~work, color=GRAY, alpha=0.8, lw=0, step="mid")
        ax.fill_between(h, 0, inst, where=work, color=OK, lw=0, step="mid")
        ax.axvline(7, color=ACCENT, lw=1.1, ls=(0, (3, 2)))
        ax.text(7.15, 2.55, t["deadline"], color=ACCENT, fontsize=8.4, va="center")
        ax.set_ylim(0, 3)
        ax.set_yticks([0, 1, 2])
        ax.set_ylabel(t["instances"], fontsize=9)
        ax.set_title(name, fontsize=10, loc="left", color=INK, fontweight="bold")
        ax.text(23.8, 2.55, text, ha="right", va="center", fontsize=10, fontweight="bold",
                color=ACCENT if ax is ax1 else OK)
        clean_axes(ax)
    ax1.text(13, 1, t["idle"], ha="center", va="center", fontsize=9, color=INK_SOFT)
    ax2.annotate(t["work"], xy=(3.5, 1.2), xytext=(9, 1.2), fontsize=9, color=OK, va="center",
                 arrowprops=dict(arrowstyle="-|>", color=OK, lw=1))
    ax2.set_xlim(0, 24)
    ax2.set_xticks(range(0, 25, 2))
    ax2.xaxis.set_major_formatter(lambda v, _: f"{int(v):02d}")
    ax2.set_xlabel(t["hour"])
    fig.suptitle(t["eb_title"], x=0.01, ha="left", fontsize=10.6, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["eb_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1), h_pad=1.2)
    save(fig, out, "endpoint-vs-batch")


# ─── 2. Costo por predicción / cost per prediction ─────────────────────────────
def chart_cost_per_prediction(t, out):
    # (precio USD/h, solicitudes/s sostenidas, p95 ms) — ilustrativo. Illustrative.
    opts = [(0.20, 40, 310), (0.40, 140, 150), (0.80, 230, 95), (1.50, 300, 60)]
    cpm = [p / (r * 3600) * 1e6 for p, r, _ in opts]
    slo = 200
    valid = [i for i, (_, _, l) in enumerate(opts) if l <= slo]
    best = min(valid, key=lambda i: cpm[i])

    fig, ax = figure(4.2)
    ax.axvspan(slo, 360, color=ACCENT, alpha=0.06, lw=0)
    ax.axvline(slo, color=ACCENT, lw=1.2, ls=(0, (3, 2)))
    ax.text(slo + 5, 0.6, t["slo"], color=ACCENT, fontsize=8.8, va="center")
    for i, ((p, r, lat), c) in enumerate(zip(opts, cpm)):
        color = OK if i == best else (MUTED if lat <= slo else ACCENT)
        ax.scatter([lat], [c], s=90 if i == best else 60, color=color, zorder=4)
        txt = f"{t['options'][i]}\n{fmt(p, t, 2)} {t['per_hour']} · {r} {t['rps']}"
        dx, dy, ha = {0: (-10, 0.05, "right"), 1: (-12, -0.02, "right")}.get(i, (10, 0.05, "left"))
        ax.annotate(txt, xy=(lat, c), xytext=(lat + dx, c + dy), fontsize=8.4, color=INK, ha=ha, va="bottom")
    ax.annotate(t["best"], xy=(opts[best][2], cpm[best]), xytext=(118, 0.1), fontsize=8.8, color=OK,
                ha="center", arrowprops=dict(arrowstyle="-|>", color=OK, lw=1))
    ax.set_xlim(40, 360)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel(t["p95"])
    ax.set_ylabel(t["cpm"])
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
    ax.set_title(t["cp_title"], fontsize=10, loc="left", color=INK, fontweight="bold")
    ax.yaxis.grid(True, color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["cp_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "cost-per-prediction")


# ─── 3. Savings Plans sobre el uso base / Savings Plans on the baseline ────────
def chart_savings_plan(t, out):
    h = np.arange(0, 7 * 24)
    day, hod = h // 24, h % 24
    peak = np.exp(-((hod - 15) ** 2) / 14) * np.where(day < 5, 1.0, 0.4)
    usage = 6 + 5 * peak + np.random.default_rng(2).normal(0, 0.15, h.size)
    usage = usage.clip(5.6)
    commit = 5.6
    over = 8.5

    fig, ax = figure(4.0)
    ax.fill_between(h, 0, np.minimum(usage, commit), color=OK, alpha=0.85, lw=0, step="mid", label=t["covered"])
    ax.fill_between(h, commit, usage, where=usage > commit, color=GRAY, lw=0, step="mid", label=t["ondemand"])
    ax.axhline(commit, color=INK, lw=1.3)
    ax.text(1, commit - 0.35, t["commit"], fontsize=8.8, color="white", va="top", fontweight="bold")
    ax.fill_between(h, usage, over, where=usage < over, color=ACCENT, alpha=0.1, lw=0, step="mid")
    ax.axhline(over, color=ACCENT, lw=1.1, ls=(0, (3, 2)))
    # En dos líneas para no pisar el pico del viernes. Two lines so it clears Friday's peak.
    ax.text(h[-1], over + 0.2, t["over"].replace(": ", ":\n", 1), fontsize=8.6, color=ACCENT, ha="right",
            va="bottom", multialignment="right")
    ax.set_xlim(0, h[-1])
    ax.set_ylim(0, 14.5)
    ax.set_xticks(np.arange(12, 7 * 24, 24))
    ax.set_xticklabels(t["days"])
    ax.set_ylabel(t["usage"])
    ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 0))
    ax.set_title(t["sp_title"], fontsize=10, loc="left", color=INK, fontweight="bold")
    ax.legend(frameon=False, loc="upper left", fontsize=8.6, ncol=2)
    clean_axes(ax)
    fig.text(0.99, 0.01, t["sp_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "savings-plan-baseline")


# ─── 4. Los pasos del ejemplo / the worked example's steps ─────────────────────
def chart_example_steps(t, out):
    fig, (top, bot) = figure(4.9, nrows=2, gridspec_kw={"height_ratios": [1.15, 1]})
    fig.subplots_adjust(left=0.03, right=0.98, top=0.92, bottom=0.12, hspace=0.12)
    diagram_axes(top, 16.4, 4.4)
    w, gap = 3.6, 0.6
    icons = ["aws/cloudwatch", "aws/sagemaker-ai", None, "aws/budgets"]  # paso 3 no nombra un servicio / step 3 names no service
    for i, (label, desc) in enumerate(t["ex_steps"]):
        x = 0.1 + i * (w + gap)
        color = OK if i == 2 else INK
        top.text(x + 0.05, 4.05, label, fontsize=9.6, fontweight="bold", color=color, va="center")
        box(top, x, 0.15, w, 3.4, "", edge=OK if i == 2 else RULE, size=10)
        if icons[i]:
            place_icon(top, icons[i], x + w / 2, 2.9, 1.15)
            fit_to(top.text(x + w / 2, 1.2, desc, ha="center", va="center", fontsize=10, color=INK,
                            multialignment="center"), w - 0.5, 1.7)
        else:
            fit_to(top.text(x + w / 2, 0.15 + 1.7, desc, ha="center", va="center", fontsize=10, color=INK,
                            multialignment="center"), w - 0.5, 3.0)
        if i < 3:
            arrow(top, (x + w + 0.08, 1.85), (x + w + gap - 0.08, 1.85))

    vals = [48, 3]
    bot.barh([1, 0], vals, color=[GRAY, OK], height=0.42)
    for y, v, name, txt in zip([1, 0], vals, t["ex_bars"], t["ex_vals"]):
        bot.text(0.3, y + 0.38, name, va="center", fontsize=9.2, color=INK_SOFT)
        bot.text(v + 0.8, y, txt, va="center", fontsize=9.2, color=INK, fontweight="bold")
    bot.set_yticks([])
    bot.spines["left"].set_visible(False)
    bot.set_xlim(0, 64)
    bot.set_ylim(-0.4, 1.75)
    bot.set_xlabel(t["ex_unit"], fontsize=9.2)
    fit_to(bot.text(17, 0, t["ex_drop"], va="center", fontsize=9, color=OK), 46)
    clean_axes(bot)
    bot.spines["left"].set_visible(False)
    fig.suptitle(t["ex_title"], x=0.01, ha="left", fontsize=10.6, fontweight="bold", color=INK)
    fig.text(0.99, 0.01, t["ex_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "example-steps")


# ─── 5. Qué herramienta responde qué pregunta / which tool answers which question ─
def chart_cost_tools_map(t, out):
    fig, ax = figure(5.2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    W, H = 30, 15
    diagram_axes(ax, W, H)
    ax.text(0.3, H - 0.3, t["ct_title"], fontsize=10.4, fontweight="bold", color=INK, va="top")
    cw, ch, gap = 8.9, 6.0, 1.2

    def mini_tags(rx, ry, rw, rh, key):  # chips de etiquetas de costo / cost tag chips
        for text, cx, cy, w, on in (("project=risk", rx, ry + 1.45, 3.75, True), ("team=ml", rx + 3.95, ry + 1.45, 3.6, False),
                                     ("env=prod", rx, ry + 0.1, 3.75, False)):
            box(ax, cx, cy, w, 0.95, text, edge=INK_SOFT if on else GRAY, fill="white", size=8.6,
                color=INK if on else MUTED, weight="bold" if on else "normal", lw=1.5 if on else 1.1)

    def mini_explorer(rx, ry, rw, rh, key):  # gasto histórico y pronóstico / spend history and forecast
        hist = np.array([1.0, 1.15, 1.05, 1.3, 1.25, 1.5, 1.45, 1.7, 1.62, 1.9, 1.85, 2.1, 2.05])
        xs = np.linspace(rx, rx + rw * 0.72, len(hist))
        ys = ry + 0.2 + (hist - 0.8) / 1.5 * (rh - 0.5)
        fx = np.linspace(xs[-1], rx + rw, 5)
        fy = ys[-1] + np.linspace(0, 0.35, 5)
        ax.fill_between(fx, fy - np.linspace(0, 0.55, 5), fy + np.linspace(0, 0.55, 5), color=GRAY, alpha=0.4, lw=0, zorder=3)
        ax.plot(xs, ys, color=INK_SOFT, lw=2.0, zorder=3)
        ax.plot(fx, fy, color=INK_SOFT, lw=1.8, ls=(0, (2, 2)), zorder=3)
        ax.plot([rx, rx + rw], [ry, ry], color=GRAY, lw=1.0)

    def mini_budgets(rx, ry, rw, rh, key):  # barras que cruzan el umbral / bars crossing the threshold
        vals = np.array([0.8, 1.05, 1.3, 1.6, 2.0, 2.4]) / 2.6 * rh
        thr = 1.75 / 2.6 * rh
        bw = rw / 6 * 0.62
        for i, v in enumerate(vals):
            ax.add_patch(plt.Rectangle((rx + i * rw / 6 + 0.1, ry), bw, v, color=ACCENT if v > thr else GRAY, zorder=2))
        ax.plot([rx, rx + rw], [ry + thr, ry + thr], color=INK_SOFT, lw=1.3, ls=(0, (3, 2)), zorder=3)
        ax.plot([rx, rx + rw], [ry, ry], color=GRAY, lw=1.0)

    def mini_advisor(rx, ry, rw, rh, key):  # seis categorías, la de costos resaltada / six categories, cost highlighted
        colw = rw / 2
        for i, name in enumerate(t["ct_ta"]):  # dos columnas, tres filas / two columns, three rows
            cx = rx + 0.2 + (i % 2) * colw
            cy = ry + rh * (0.76 - (i // 2) * 0.4)
            cost = i == 0
            ax.plot([cx], [cy], "o", ms=13 if cost else 10, color=AMBER if cost else GRAY, zorder=3)
            fit_to(ax.text(cx + 0.47, cy, name, ha="left", va="center", fontsize=8.6, color=INK if cost else INK_SOFT,
                           fontweight="bold" if cost else "normal"), colw - 0.75, 0.7)

    def mini_optimizer(rx, ry, rw, rh, key):  # 14 días con invocaciones en cero / 14 days at zero invocations
        base = ry + 0.35
        for i in range(14):
            xx = rx + 0.1 + i * (rw - 0.2) / 13
            ax.plot([xx, xx], [base - 0.18, base + 0.18], color=GRAY, lw=1.0)
        ax.plot([rx, rx + rw], [base, base], color=ACCENT, lw=3.0, solid_capstyle="round", zorder=3)
        ghost = base + 0.6 + 0.9 * np.abs(np.sin(np.linspace(0, 4 * np.pi, 60))) * np.linspace(1, 0.9, 60)
        ax.plot(np.linspace(rx, rx + rw, 60), ghost, color=MUTED, lw=1.4, ls=(0, (2, 3)), zorder=3)
        ax.text(rx, ry + rh + 0.05, t["ct_normal"], ha="left", va="top", fontsize=8.6, color=MUTED)

    def mini_quotas(rx, ry, rw, rh, key):  # cuota usada y ampliación solicitada / used quota and requested increase
        sw, sg = (rw - 0.6) / 7, 0.1
        for i in range(7):
            x0 = rx + i * (sw + sg)
            if i < 4:
                ax.add_patch(plt.Rectangle((x0, ry + 0.9), sw, 1.1, color=INK_SOFT, zorder=2))
            else:
                ax.add_patch(plt.Rectangle((x0, ry + 0.9), sw, 1.1, fill=False, ec=ACCENT if i == 4 else GRAY, lw=1.3,
                                           ls=(0, (2, 2)), zorder=2))
        ax.annotate("", xy=(rx + 6.8 * (sw + sg), ry + 0.35), xytext=(rx + 3.9 * (sw + sg), ry + 0.35),
                    arrowprops={"arrowstyle": "-|>", "color": ACCENT, "lw": 1.5, "mutation_scale": 12}, zorder=3)

    minis = [mini_tags, mini_explorer, mini_budgets, mini_advisor, mini_optimizer, mini_quotas]
    icons = [None, "aws/cost-explorer", "aws/budgets", "aws/trusted-advisor", "aws/compute-optimizer", None]
    for i, (name, question, fact) in enumerate(t["ct_cards"]):
        x = 0.3 + (i % 3) * (cw + gap)
        y = 7.4 if i < 3 else 0.4
        key = i == 4  # el caso del Check: un endpoint ocioso / the Check's case: an idle endpoint
        box(ax, x, y, cw, ch, "", edge=ACCENT if key else RULE, fill=SURFACE, lw=1.8 if key else 1.3)
        icon = icons[i]  # Service Quotas y las etiquetas de costo no tienen ícono oficial / no official icon for those
        nx = x + 0.6
        if icon:
            iw = 1.3 * _y_to_x(ax)  # ancho del ícono en unidades x / icon width in x units
            place_icon(ax, icon, x + 0.6 + iw / 2, y + ch - 0.8, 1.3)
            nx = x + 0.6 + iw + 0.3
        fit_to(ax.text(nx, y + ch - 0.8, name, fontsize=10.6, fontweight="bold", color=INK, va="center"),
               cw - 0.6 - (nx - x))
        fit_to(ax.text(x + 0.6, y + ch - 1.65, question, fontsize=9, color=INK_SOFT, va="top"), cw - 1.2, 1.2)
        minis[i](x + 0.6, y + 1.3, cw - 1.2, 2.4, key)
        ax.text(x + 0.6, y + 0.62, fact, fontsize=8.6, color=ACCENT if key else INK_SOFT, va="center",
                fontweight="bold" if key else "normal")
        if i == 1:  # las tags alimentan a Cost Explorer / tags feed Cost Explorer
            arrow(ax, (0.3 + cw + 0.05, y + ch / 2), (x - 0.05, y + ch / 2), color=MUTED)
    save(fig, out, "cost-tools-map")


CHARTS = [chart_endpoint_vs_batch, chart_cost_per_prediction, chart_savings_plan, chart_example_steps,
          chart_cost_tools_map]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
