"""
Tema 3.1: infraestructura de despliegue. Topic 3.1: deployment infrastructure.

    python charts/topics/deployment-infrastructure.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, icon_node, place_icon, save,
)

TEXT = {
    "es": {
        "payload": "Tamaño del payload por solicitud",
        "time": "Tiempo de proceso por solicitud",
        "serverless": "Serverless\n≤ 4 MB · 60 s",
        "realtime": "Real-time\n≤ 25 MB\n60 s",
        "streaming": "streaming: 8 min",
        "async": "Asynchronous ≤ 1 GB · 1 h (entrada y salida en S3)",
        "out": "Fuera de los endpoints:\nBatch Transform para\nlotes que ya existen",
        "p1": "JSON de 2 KB, 80 ms",
        "p2": "imagen\n9 MB, 3 s",
        "p3": "PDF de 600 MB, 15 min",
        "lim_title": "Cada opción de inferencia de SageMaker AI tiene un límite de payload y de tiempo",
        "lim_note": "Límites de la documentación de SageMaker AI; ejes logarítmicos",
        "mme": "Multi-model endpoint",
        "mme_sub": "un contenedor, mismo framework",
        "mme_c": "Contenedor XGBoost",
        "loaded": "en memoria",
        "s3": "Amazon S3\nmiles de model.tar.gz",
        "mme_k": "Carga al primer uso y descarga si falta memoria",
        "mc": "Multicontenedor",
        "mc_sub": "hasta 15 contenedores distintos",
        "direct": "Direct: TargetContainerHostname",
        "serial": "Serial: inference pipeline",
        "pre": "preproceso",
        "model": "modelo",
        "post": "posproceso",
        "mc_k": "Frameworks distintos o pasos encadenados",
        "ic": "Inference components",
        "ic_sub": "recursos propios por modelo",
        "ic_a": "LLM A · 2 GPU · 2 copias",
        "ic_b": "LLM B · 1 GPU · 1 copia",
        "ic_c": "modelo C · 0 copias",
        "ic_k": "Cada modelo escala por separado; escala a 0",
        "share_title": "Tres formas de compartir un endpoint, según cuánto se parecen los modelos",
        "instance": "instancia",
        "hour": "Hora del día",
        "row_batch": "Batch Transform\n(2 M textos)",
        "row_async": "Async endpoint\n(expedientes 500 MB)",
        "row_rt": "Alternativa:\nendpoint real-time",
        "batch_on": "lote ≈ 2 h; luego se liberan las instancias",
        "deadline": "plazo 7:00",
        "async_on": "horario laboral: escala con la cola",
        "async_zero": "mínimo 0 instancias",
        "rt_on": "24 h pagadas, y no acepta 500 MB (límite 25 MB)",
        "wl_title": "Un mismo Model, dos cargas: capacidad encendida solo cuando hay trabajo",
        "wl_note": "Ilustrativo: el ejemplo fija el plazo (7:00) y un lote de unas 2 h; el resto de horarios es supuesto",
        "fm_title": "La forma del tráfico decide cómo consumir un FM",
        "fm_h_need": "Si tu caso es…",
        "fm_h_use": "Consume el FM con…",
        "fm_rows": [
            ("Picos breves", "Bedrock on-demand", "por token · backoff + inference profile"),
            ("Datos dentro de la UE", "Perfil geográfico", "cross-Region dentro de la geografía"),
            ("Volumen alto y estable", "Provisioned Throughput", "model units por hora"),
            ("Otro modelo o red privada", "SageMaker JumpStart", "tú eliges y pagas la instancia"),
        ],
        "fm_tag_geo": "perfil global: ~10 % menos",
        "fm_tag_pt": "se cobra aunque no la uses",
        "fm_h_shape": "Forma del tráfico",
        "fm_eu": "UE",
        "fm_private": "red privada",
        "fm_model": "tu modelo",
        "fm_note": "Ilustrativo: formas de tráfico, no datos reales",
    },
    "en": {
        "payload": "Payload size per request",
        "time": "Processing time per request",
        "serverless": "Serverless\n≤ 4 MB · 60 s",
        "realtime": "Real-time\n≤ 25 MB\n60 s",
        "streaming": "streaming: 8 min",
        "async": "Asynchronous ≤ 1 GB · 1 h (input and output in S3)",
        "out": "Beyond endpoints:\nBatch Transform for\nbatches that already exist",
        "p1": "2 KB JSON, 80 ms",
        "p2": "image\n9 MB, 3 s",
        "p3": "600 MB PDF, 15 min",
        "lim_title": "Each SageMaker AI inference option has a payload and a time limit",
        "lim_note": "Limits from the SageMaker AI documentation; log axes",
        "mme": "Multi-model endpoint",
        "mme_sub": "one container, same framework",
        "mme_c": "XGBoost container",
        "loaded": "in memory",
        "s3": "Amazon S3\nthousands of model.tar.gz",
        "mme_k": "Loads on first use, unloads when memory is low",
        "mc": "Multi-container",
        "mc_sub": "up to 15 different containers",
        "direct": "Direct: TargetContainerHostname",
        "serial": "Serial: inference pipeline",
        "pre": "preprocess",
        "model": "model",
        "post": "postprocess",
        "mc_k": "Different frameworks or chained steps",
        "ic": "Inference components",
        "ic_sub": "own resources per model",
        "ic_a": "LLM A · 2 GPUs · 2 copies",
        "ic_b": "LLM B · 1 GPU · 1 copy",
        "ic_c": "model C · 0 copies",
        "ic_k": "Each model scales on its own; scales to 0",
        "share_title": "Three ways to share an endpoint, depending on how alike the models are",
        "instance": "instance",
        "hour": "Hour of day",
        "row_batch": "Batch Transform\n(2 M texts)",
        "row_async": "Async endpoint\n(500 MB case files)",
        "row_rt": "Alternative:\nreal-time endpoint",
        "batch_on": "batch ≈ 2 h; then instances are released",
        "deadline": "7:00 deadline",
        "async_on": "working hours: scales with the queue",
        "async_zero": "minimum 0 instances",
        "rt_on": "24 h paid, and it does not accept 500 MB (25 MB limit)",
        "wl_title": "One Model, two workloads: capacity is on only when there is work",
        "wl_note": "Illustrative: the example sets the 7:00 deadline and a ~2 h batch; other hours are assumed",
        "fm_title": "The traffic shape decides how to consume an FM",
        "fm_h_need": "If your case is…",
        "fm_h_use": "Consume the FM with…",
        "fm_rows": [
            ("Short spikes", "Bedrock on-demand", "per token · backoff + inference profile"),
            ("Data must stay in the EU", "Geographic profile", "cross-Region inside the geography"),
            ("High, steady volume", "Provisioned Throughput", "model units per hour"),
            ("Another model or private network", "SageMaker JumpStart", "you pick and pay for the instance"),
        ],
        "fm_tag_geo": "global profile: ~10% less",
        "fm_tag_pt": "billed even if unused",
        "fm_h_shape": "Traffic shape",
        "fm_eu": "EU",
        "fm_private": "private network",
        "fm_model": "your model",
        "fm_note": "Illustrative: traffic shapes, not real data",
    },
}

KB, MB, GB = 1e3, 1e6, 1e9
SEC, MIN, HOUR = 1, 60, 3600


# ─── 1. Límites de payload y tiempo / payload and time limits ──────────────────
def chart_inference_limits(t, out):
    fig, ax = figure(4.6)
    x0, y0 = 1 * KB, 0.01
    ax.set_xscale("log")
    ax.set_yscale("log")
    # Del mayor al menor para que los pequeños queden encima. Largest first so smaller ones sit on top.
    ax.add_patch(Rectangle((x0, y0), 1 * GB - x0, HOUR - y0, facecolor="#fff4d6", edgecolor=AMBER, lw=1.6))
    ax.add_patch(Rectangle((x0, y0), 25 * MB - x0, 8 * MIN - y0, facecolor="none", edgecolor=INK_SOFT, lw=1.1,
                           ls=(0, (3, 2))))
    ax.add_patch(Rectangle((x0, y0), 25 * MB - x0, 60 * SEC - y0, facecolor=SURFACE, edgecolor=INK_SOFT, lw=1.6))
    ax.add_patch(Rectangle((x0, y0), 4 * MB - x0, 60 * SEC - y0, facecolor="#e3f1e9", edgecolor=OK, lw=1.6))

    ax.text(1.5 * KB, 40, t["serverless"], fontsize=9.4, color=OK, va="top", fontweight="bold")
    ax.text(4.6 * MB, 40, t["realtime"], fontsize=8.8, color=INK_SOFT, va="top", fontweight="bold")
    ax.text(1.5 * KB, 8 * MIN * 0.82, t["streaming"], fontsize=8.6, color=INK_SOFT, va="top")
    ax.text(1.5 * KB, 0.75 * HOUR, t["async"], fontsize=9.4, color="#8a5a00", va="top", fontweight="bold")
    ax.text(3 * GB, 0.02, t["out"], fontsize=8.8, color=MUTED, va="bottom")

    pts = [(2 * KB, 0.08, t["p1"], OK), (9 * MB, 3, t["p2"], INK_SOFT), (600 * MB, 15 * MIN, t["p3"], ACCENT)]
    for x, y, txt, col in pts:
        ax.scatter([x], [y], color=col, s=42, zorder=5, edgecolor="white", lw=0.8)
        right, mid = x > 100 * MB, 1 * MB < x < 100 * MB
        offset = (0, -8) if mid else (-8, 8) if right else (6, -8)
        ax.annotate(txt, (x, y), xytext=offset, textcoords="offset points", fontsize=8.6, color=col,
                    ha="center" if mid else "right" if right else "left", va="bottom" if right else "top")

    ax.set_xlim(x0, 40 * GB)
    ax.set_ylim(y0, 6 * HOUR)
    ax.set_xticks([1 * KB, 1 * MB, 4 * MB, 25 * MB, 1 * GB])
    ax.set_xticklabels(["1 KB", "1 MB", "4 MB", "25 MB", "1 GB"])
    ax.set_yticks([0.1, 1, 60, 8 * MIN, HOUR])
    ax.set_yticklabels(["0,1 s" if t is TEXT["es"] else "0.1 s", "1 s", "60 s", "8 min", "1 h"])
    ax.minorticks_off()
    ax.set_xlabel(t["payload"])
    ax.set_ylabel(t["time"])
    ax.set_title(t["lim_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    clean_axes(ax)
    fig.text(0.99, 0.01, t["lim_note"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, out, "inference-limits")


# ─── 2. Compartir un endpoint / sharing an endpoint ────────────────────────────
def chart_endpoint_sharing(t, out):
    fig, ax = figure(4.6)
    W, H = 30, 15
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # antes de los íconos / before icons
    diagram_axes(ax, W, H)
    ax.text(0.2, H - 0.3, t["share_title"], fontsize=10.2, fontweight="bold", color=INK, va="top")
    cols = [(0.3, t["mme"], t["mme_sub"], t["mme_k"]), (10.3, t["mc"], t["mc_sub"], t["mc_k"]),
            (20.3, t["ic"], t["ic_sub"], t["ic_k"])]
    cw = 9.4
    for x, name, sub, key in cols:
        ax.text(x + cw / 2, 12.8, name, ha="center", fontsize=10.5, fontweight="bold", color=INK)
        ax.text(x + cw / 2, 12.0, sub, ha="center", fontsize=8.8, color=MUTED)
        top = 5.6 if name == t["mme"] else 3.0
        box(ax, x, top, cw, 11.4 - top, "", edge=RULE, fill="white", lw=1.0)
        ax.text(x + 0.3, 10.9, t["instance"], fontsize=8, color=MUTED, va="top")
        fit_to(ax.text(x + cw / 2, 2.55, key, ha="center", va="top", fontsize=8.8, color=INK_SOFT,
                       multialignment="center"), cw)

    # MME: un contenedor con modelos cargados; S3 abajo. One container with loaded models; S3 below.
    x = 0.3
    box(ax, x + 0.6, 6.0, cw - 1.2, 4.3, "", edge=INK_SOFT, fill=SURFACE)
    ax.text(x + cw / 2, 9.75, t["mme_c"], ha="center", fontsize=9, color=INK)
    for i, m in enumerate(["m-0017", "m-0420", "m-1288"]):
        box(ax, x + 1.0 + i * 2.55, 7.0, 2.3, 1.2, m, edge=OK, fill="white", size=8.2)
    ax.text(x + cw / 2, 6.6, t["loaded"], ha="center", fontsize=7.8, color=OK)
    icon_node(ax, x + 0.6, 3.4, cw - 1.2, 1.6, "aws/s3", t["s3"], edge=MUTED, fill="white", size=8.6)
    arrow(ax, (x + cw / 2, 4.95), (x + cw / 2, 5.95), color=OK)
    ax.patches[-1].set_zorder(4)

    # Multicontenedor: Direct arriba, Serial abajo. Multi-container: Direct on top, Serial below.
    x = 10.3
    ax.text(x + 0.6, 9.75, t["direct"], fontsize=8.4, color=INK_SOFT)
    for i, (fw, logo) in enumerate((("TensorFlow", "tools/tensorflow"), ("PyTorch", "tools/pytorch"), ("XGBoost", None))):
        bx = x + 0.5 + i * 2.9
        box(ax, bx, 7.8, 2.7, 1.7, "", edge=INK_SOFT, fill=SURFACE)
        if logo:  # XGBoost no tiene un logo con licencia libre en el set usado / no openly licensed logo
            place_icon(ax, logo, bx + 1.35, 8.95, 0.75)
        ax.text(bx + 1.35, 8.2 if logo else 8.65, fw, ha="center", va="center", fontsize=8, color=INK, zorder=5)
    ax.text(x + 0.6, 6.9, t["serial"], fontsize=8.4, color=INK_SOFT)
    steps = [t["pre"], t["model"], t["post"]]
    for i, s in enumerate(steps):
        box(ax, x + 0.5 + i * 2.95, 4.4, 2.6, 1.6, s, edge=AMBER, fill="#fff4d6", size=7.4)
        if i:
            arrow(ax, (x + 0.5 + i * 2.95 - 0.33, 5.2), (x + 0.5 + i * 2.95 - 0.03, 5.2), color=AMBER)
            ax.patches[-1].set_zorder(4)

    # Inference components: GPU asignadas por modelo. GPUs allocated per model.
    x = 20.3
    gpus = [OK, OK, OK, OK, ACCENT, GRAY, GRAY, GRAY]
    for i, col in enumerate(gpus):
        gx = x + 0.7 + (i % 4) * 2.05
        gy = 8.6 if i < 4 else 6.8
        box(ax, gx, gy, 1.8, 1.4, "GPU", edge=col, fill="white" if col == GRAY else col, size=8,
            color=INK_SOFT if col == GRAY else "white", weight="bold")
    for k, (txt, col) in enumerate(((t["ic_a"], OK), (t["ic_b"], ACCENT), (t["ic_c"], MUTED))):
        ax.add_patch(Rectangle((x + 0.8, 5.55 - k * 0.85), 0.35, 0.35, facecolor=col, edgecolor="none", zorder=3))
        ax.text(x + 1.4, 5.72 - k * 0.85, txt, fontsize=8.4, color=INK, va="center")
    save(fig, out, "endpoint-sharing")


# ─── 3. Ejemplo: dos cargas con el mismo Model / example: two workloads, one Model ─
def chart_two_workloads(t, out):
    fig, ax = figure(3.4)
    rows = {"batch": 2, "async": 1, "rt": 0}
    hgt = 0.46
    # Lote nocturno de unas 2 h antes del plazo de las 7:00. Nightly batch of about 2 h before the 7:00 deadline.
    ax.barh(rows["batch"], 2, left=1, height=hgt, color=OK)
    ax.plot([7, 7], [rows["batch"] - 0.4, rows["batch"] + 0.4], color=ACCENT, lw=1.6, ls=(0, (3, 2)))
    ax.text(7, rows["batch"] + 0.48, t["deadline"], ha="center", va="bottom", fontsize=8.4, color=ACCENT)
    ax.text(7.5, rows["batch"], t["batch_on"], ha="left", va="center", fontsize=8.6, color=INK_SOFT)
    # Async: en horario laboral; fuera de él, 0 instancias. Async: working hours; 0 instances otherwise.
    ax.barh(rows["async"], 11, left=8, height=hgt, color=AMBER)
    ax.text(13.5, rows["async"], t["async_on"], ha="center", va="center", fontsize=8.6, color=INK)
    for a, b in ((0, 8), (19, 24)):
        ax.plot([a, b], [rows["async"]] * 2, color=GRAY, lw=1.2, ls=(0, (2, 2)))
    ax.text(0.3, rows["async"] + 0.1, t["async_zero"], ha="left", va="bottom", fontsize=8.2, color=MUTED)
    # Alternativa descartada: un endpoint real-time siempre encendido. Rejected alternative: an always-on endpoint.
    ax.barh(rows["rt"], 24, left=0, height=hgt, color=SURFACE, edgecolor=GRAY, lw=1, hatch="///")
    ax.text(12, rows["rt"], t["rt_on"], ha="center", va="center", fontsize=8.6, color=ACCENT,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none"))

    ax.set_yticks([rows["batch"], rows["async"], rows["rt"]])
    ax.set_yticklabels([t["row_batch"], t["row_async"], t["row_rt"]], fontsize=9)
    ax.set_ylim(-0.5, 2.8)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 3))
    ax.set_xticklabels([f"{x}:00" for x in range(0, 25, 3)])
    ax.set_xlabel(t["hour"])
    ax.xaxis.grid(True, color=RULE, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title(t["wl_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    clean_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.985, 0.015, t["wl_note"], ha="right", fontsize=7.6, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, out, "two-workloads")


# ─── 4. Cómo consumir un FM / how to consume an FM ─────────────────────────────
# Bedrock para las tres primeras opciones; SageMaker AI para JumpStart. Bedrock for the first three; SageMaker AI for JumpStart.
FM_ICONS = ['aws/bedrock', 'aws/bedrock', 'aws/bedrock', 'aws/sagemaker-ai']

def chart_fm_consumption_options(t, out):
    fig, ax = figure(4.9)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    W, H = 30, 17.5
    diagram_axes(ax, W, H)
    ax.text(0.3, H - 0.3, t["fm_title"], fontsize=10.4, fontweight="bold", color=INK, va="top")
    ax.text(0.3, 15.45, t["fm_h_need"], fontsize=8.8, color=MUTED, va="bottom")
    ax.text(7.9, 15.45, t["fm_h_shape"], fontsize=8.8, color=MUTED, va="bottom")
    ax.text(18.4, 15.45, t["fm_h_use"], fontsize=8.8, color=MUTED, va="bottom")
    rh, gap, top = 3.2, 0.4, 15.2
    px, pw = 7.9, 9.0  # panel de la forma del tráfico / traffic-shape panel
    ox, ow = 18.4, 11.3  # opción / option
    xs = np.linspace(px + 0.6, px + pw - 0.6, 240)

    def dashed_region(cx, cy, w, h, label):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.25",
                                    linewidth=1.3, edgecolor=INK_SOFT, facecolor="none", linestyle=(0, (4, 3)),
                                    zorder=2))
        ax.text(cx - w / 2 + 0.3, cy + h / 2 - 0.3, label, fontsize=8.4, color=MUTED, fontweight="bold",
                va="top", ha="left")

    for i, (need, name, sub) in enumerate(t["fm_rows"]):
        y = top - i * (rh + gap) - rh
        mid = y + rh / 2
        box(ax, 0.3, y, 7.0, rh, need, edge=GRAY, fill="white", size=9.6)
        arrow(ax, (7.35, mid), (px - 0.05, mid), color=MUTED)
        box(ax, px, y, pw, rh, "", edge=RULE, fill="white", lw=1.2)
        y0, hh = y + 0.45, rh - 0.9
        if i == 0:  # picos breves: pagas por token = el área bajo la curva / spikes: pay per token = area under it
            curve = 0.1 + sum(a * np.exp(-((np.linspace(0, 1, 240) - c) / 0.035) ** 2)
                              for a, c in ((0.9, 0.18), (0.7, 0.5), (1.0, 0.82)))
            ax.fill_between(xs, y0, y0 + hh * np.clip(curve, 0, 1), color=GRAY, alpha=0.55, zorder=2, lw=0)
            ax.plot(xs, y0 + hh * np.clip(curve, 0, 1), color=INK_SOFT, lw=1.5, zorder=3)
        elif i == 1:  # datos en la UE: regiones dentro de un límite / EU data: regions inside a boundary
            cx = px + pw / 2
            dashed_region(cx, mid, 6.4, rh - 0.7, t["fm_eu"])
            pts = [(cx - 1.7, mid - 0.35), (cx + 0.2, mid + 0.35), (cx + 1.9, mid - 0.35)]
            for (ax1, ay1), (ax2, ay2) in ((pts[0], pts[1]), (pts[1], pts[2]), (pts[0], pts[2])):
                ax.plot([ax1, ax2], [ay1, ay2], color=GRAY, lw=1.4, zorder=3)
            ax.scatter(*zip(*pts), s=95, c=INK_SOFT, zorder=4, edgecolors="white", linewidths=1.2)
        elif i == 2:  # volumen estable: capacidad reservada fija, se paga haya uso o no / flat reserved capacity
            band_h = hh * 0.9
            ax.add_patch(Rectangle((px + 0.5, y0), pw - 1.0, band_h, facecolor=ACCENT, alpha=0.07, edgecolor="none",
                                   zorder=1))
            ax.add_patch(Rectangle((px + 0.5, y0), pw - 1.0, band_h, facecolor="none", edgecolor=ACCENT, lw=1.3,
                                   linestyle=(0, (4, 2)), zorder=3))
            use = 0.52 + 0.05 * np.sin(np.linspace(0, 14, 240)) + 0.03 * np.sin(np.linspace(0, 41, 240))
            ax.fill_between(xs, y0 + band_h * use, y0 + band_h, color=ACCENT, alpha=0.16, zorder=2, lw=0)
            ax.plot(xs, y0 + band_h * use, color=INK_SOFT, lw=1.5, zorder=4)
        else:  # otro modelo o red privada / other model or private network
            cx = px + pw / 2
            dashed_region(cx, mid, 6.4, rh - 0.7, t["fm_private"])
            box(ax, cx - 1.45, mid - 0.85, 2.9, 0.95, t["fm_model"], edge=INK_SOFT, fill=SURFACE, size=8.8)

        box(ax, ox, y, ow, rh, "", edge=RULE, fill=SURFACE)
        # Ícono del servicio a la izquierda del nombre. Service icon to the left of the name.
        iw = place_icon(ax, FM_ICONS[i], ox + 0.45 + 0.65 * 0.9, y + rh - 1.15, 1.3)
        tx = ox + 0.45 + iw + 0.35
        fit_to(ax.text(tx, y + rh - 0.75, name, fontsize=10.6, fontweight="bold", color=INK, va="center"),
               ox + ow - tx - 0.4)
        fit_to(ax.text(tx, y + rh - 1.55, sub, fontsize=8.8, color=INK_SOFT, va="center"), ox + ow - tx - 0.4)
        if i == 1:
            box(ax, ox + 0.5, y + 0.3, ow - 1.0, 0.8, t["fm_tag_geo"], edge=GRAY, fill="white", size=8.4,
                color=INK_SOFT)
        if i == 2:
            box(ax, ox + 0.5, y + 0.3, ow - 1.0, 0.8, t["fm_tag_pt"], edge=ACCENT, fill="white", size=8.4,
                color=ACCENT, weight="bold")
    ax.text(29.7, 0.45, t["fm_note"], fontsize=7.8, color=MUTED, ha="right", va="center")
    save(fig, out, "fm-consumption-options")


CHARTS = [chart_inference_limits, chart_endpoint_sharing, chart_two_workloads, chart_fm_consumption_options]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
