"""
Tema 1.1: recolectar y almacenar datos. Topic 1.1: data collection and storage.

    python charts/topics/data-collection-storage.py --lang es --out <dir>
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from matplotlib.patches import Rectangle  # noqa: E402

from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE,
    DPI, WIDTH_IN, arrow, box, clean_axes, cli, diagram_axes, figure, fit_to, fmt, icon_node, place_icon, plt, save,
    _y_to_x,
)

TEXT = {
    "es": {
        "decimal": ",",
        "row_title": "CSV / JSON (por filas)",
        "col_title": "Parquet / ORC (por columnas)",
        "row_note": "Para leer 3 columnas,\nse leen filas completas",
        "col_note": "Solo se leen las 3 columnas\ny se saltan bloques",
        "query": "Consulta: 3 de 20 columnas, un mes de 12",
        "scanned": "GB escaneados (ilustrativo)",
        "bars": ["CSV sin comprimir", "CSV con gzip", "Parquet: 3 columnas", "Parquet + predicate pushdown"],
        "all_cols": "lee todas las columnas",
        "illustrative": "Valores ilustrativos: tabla de 100 GB en CSV",
        "shard": "Shard",
        "mbps": "Escritura (MB/s)",
        "limit": "Límite por shard: 1 MB/s",
        "bad_title": "Clave de partición: store_id (pocos valores)",
        "good_title": "Clave de partición: customer_id (alta cardinalidad)",
        "throttled": "ProvisionedThroughputExceededException",
        "total": "Total: 4 MB/s de 10 MB/s",
        "illustrative_k": "Ilustrativo: mismo tráfico total, 10 shards",
        "ex_title": "Ejemplo: dos rutas desde los mismos eventos, una por lotes y otra en tiempo real",
        "ex_events": "Eventos de compra\n3.000/s × 2 KB ≈ 6 MB/s",
        "ex_kds": "1 · Kinesis Data Streams\non-demand · clave customer_id",
        "ex_fh": "2 · Firehose\nJSON → Parquet con el esquema de Glue",
        "ex_s3": "Amazon S3\nraw (JSON original) y Parquet en prefijos dt=…",
        "ex_rds": "RDS for PostgreSQL\ntabla products",
        "ex_snap": "3 · exportación de snapshots a S3, cada noche (sin SELECT * en producción)",
        "ex_glue": "4 · Glue ETL\nune por product_id · ventana de 7 días hasta event_time",
        "ex_off": "5 · Feature Store offline\nhistórico de 2 años (conector Spark)",
        "ex_cons": "Consumidor del stream\nPutRecord con features frescas",
        "ex_on": "Feature Store online\nla app lee con GetRecord",
        "ex_train": "Reentrenamiento nocturno: lee solo S3 y el offline store",
        "ex_batch": "Ruta por lotes",
        "ex_rt": "Ruta en tiempo real",
        "ex_note": "Caso del ejemplo · diagrama, no a escala",
        "lc_title": "Regla de ciclo de vida para la zona raw: cada paso baja el costo por GB",
        "lc_cost": "costo por GB (relativo)",
        "lc_freq": "uso frecuente",
        "lc_monthly": "acceso mensual",
        "lc_restore": "restauración en horas",
        "lc_min30": "mínimo 30 días",
        "lc_min180": "mínimo 180 días",
        "lc_lock": "Object Lock · modo compliance · retención de 365 días",
        "lc_nobody": "Nadie, ni siquiera root, puede borrar durante la retención",
        "lc_note": "Ilustrativo: costos relativos por GB, sin cifras de precio",
        "classes": ["S3 Standard", "S3 Standard-IA", "S3 Glacier Deep Archive"],
        "notes": [
            "Entrenamientos frecuentes",
            "Acceso mensual · mínimo 30 días",
            "Archivo · mínimo 180 días\nrestauración en horas",
        ],
        "day_marks": ["día 0", "día 30", "día 180", "día 365"],
        "lock": "Object Lock en modo compliance (retención de 365 días): nadie, ni siquiera root, puede borrar",
        "lake_title": "Una copia en S3, un catálogo que la describe y permisos centralizados",
        "lake_s3": "Amazon S3\nzonas raw y curated",
        "lake_crawler": "Crawler de Glue\ninfiere esquema y particiones",
        "lake_catalog": "Glue Data Catalog\ntablas, esquema y particiones",
        "lake_lf": "Lake Formation",
        "lake_chips": ["filtros por columna, fila y celda", "LF-Tags", "grant / revoke"],
        "lake_consumers": ["Athena", "Redshift Spectrum", "EMR", "Glue ETL", "Amazon Quick"],
        "lake_note": "Los permisos se aplican en cada consumidor · diagrama, no a escala",
        "pp_title": "Filtrar por la partición hace que Athena lea solo un mes",
        "pp_left": "Particiones por mes",
        "pp_root": "s3://lago/eventos/",
        "pp_filter": "WHERE dt = '2026-10'",
        "pp_skip": "se omite",
        "pp_read": "se lee",
        "pp_right": "GB escaneados por la misma consulta",
        "pp_bars": ["CSV sin particiones", "CSV particionado por mes", "Parquet particionado + 3 de 20 columnas"],
        "pp_note": "Valores ilustrativos: tabla de 100 GB con 12 meses de datos",
    },
    "en": {
        "decimal": ".",
        "row_title": "CSV / JSON (row-based)",
        "col_title": "Parquet / ORC (columnar)",
        "row_note": "Reading 3 columns\nreads whole rows",
        "col_note": "Only the 3 columns are read\nand blocks are skipped",
        "query": "Query: 3 of 20 columns, one month of 12",
        "scanned": "GB scanned (illustrative)",
        "bars": ["Uncompressed CSV", "Gzipped CSV", "Parquet: 3 columns", "Parquet + predicate pushdown"],
        "all_cols": "reads every column",
        "illustrative": "Illustrative values: a 100 GB table in CSV",
        "shard": "Shard",
        "mbps": "Writes (MB/s)",
        "limit": "Per-shard limit: 1 MB/s",
        "bad_title": "Partition key: store_id (few values)",
        "good_title": "Partition key: customer_id (high cardinality)",
        "throttled": "ProvisionedThroughputExceededException",
        "total": "Total: 4 MB/s of 10 MB/s",
        "illustrative_k": "Illustrative: same total traffic, 10 shards",
        "ex_title": "Example: two paths from the same events, one batch and one real-time",
        "ex_events": "Purchase events\n3,000/s × 2 KB ≈ 6 MB/s",
        "ex_kds": "1 · Kinesis Data Streams\non-demand · key customer_id",
        "ex_fh": "2 · Firehose\nJSON → Parquet with the Glue schema",
        "ex_s3": "Amazon S3\nraw (original JSON) and Parquet under dt=… prefixes",
        "ex_rds": "RDS for PostgreSQL\nproducts table",
        "ex_snap": "3 · snapshot export to S3, every night (no SELECT * on production)",
        "ex_glue": "4 · Glue ETL\njoin on product_id · 7-day window ending at event_time",
        "ex_off": "5 · Feature Store offline\ntwo-year backfill (Spark connector)",
        "ex_cons": "Stream consumer\nPutRecord with fresh features",
        "ex_on": "Feature Store online\nthe app reads with GetRecord",
        "ex_train": "Nightly retraining: reads only S3 and the offline store",
        "ex_batch": "Batch path",
        "ex_rt": "Real-time path",
        "ex_note": "Worked example · diagram, not to scale",
        "lc_title": "Lifecycle rule for the raw zone: each step lowers the cost per GB",
        "lc_cost": "cost per GB (relative)",
        "lc_freq": "frequent use",
        "lc_monthly": "monthly access",
        "lc_restore": "restore takes hours",
        "lc_min30": "30-day minimum",
        "lc_min180": "180-day minimum",
        "lc_lock": "Object Lock · compliance mode · 365-day retention",
        "lc_nobody": "Nobody, not even root, can delete during the retention",
        "lc_note": "Illustrative: relative cost per GB, no price figures",
        "classes": ["S3 Standard", "S3 Standard-IA", "S3 Glacier Deep Archive"],
        "notes": [
            "Frequent training runs",
            "Monthly access · 30-day minimum",
            "Archive · 180-day minimum\nrestore takes hours",
        ],
        "day_marks": ["day 0", "day 30", "day 180", "day 365"],
        "lock": "Object Lock in compliance mode (365-day retention): nobody, not even root, can delete",
        "lake_title": "One copy in S3, a catalog that describes it, and central permissions",
        "lake_s3": "Amazon S3\nraw and curated zones",
        "lake_crawler": "Glue crawler\ninfers schema and partitions",
        "lake_catalog": "Glue Data Catalog\ntables, schema and partitions",
        "lake_lf": "Lake Formation",
        "lake_chips": ["column, row and cell filters", "LF-Tags", "grant / revoke"],
        "lake_consumers": ["Athena", "Redshift Spectrum", "EMR", "Glue ETL", "Amazon Quick"],
        "lake_note": "Permissions apply in each consumer · diagram, not to scale",
        "pp_title": "Filtering on the partition makes Athena read only one month",
        "pp_left": "Partitions by month",
        "pp_root": "s3://lake/events/",
        "pp_filter": "WHERE dt = '2026-10'",
        "pp_skip": "skipped",
        "pp_read": "read",
        "pp_right": "GB scanned by the same query",
        "pp_bars": ["Unpartitioned CSV", "CSV partitioned by month", "Partitioned Parquet + 3 of 20 columns"],
        "pp_note": "Illustrative values: 100 GB table with 12 months of data",
    },
}


# ─── 1. Formato por filas vs columnar / row vs columnar format ─────────────────
def chart_columnar_scan(t, out):
    fig = plt.figure(figsize=(WIDTH_IN, 6.2), dpi=DPI)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1])
    ax_row, ax_col = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    ax_bar = fig.add_subplot(gs[1, :])

    n_rows, n_cols = 6, 10
    used = {1, 4, 7}
    for ax, columnar in ((ax_row, False), (ax_col, True)):
        diagram_axes(ax, n_cols + 0.4, n_rows + 2.2)
        for r in range(n_rows):
            for c in range(n_cols):
                if not columnar:
                    # Se leen todas las celdas; solo 3 columnas son útiles. Every cell is read; only 3 are useful.
                    color = ACCENT if c in used else "#e7a3ad"
                else:
                    color = ACCENT if (c in used and r < 4) else SURFACE
                ax.add_patch(Rectangle((0.2 + c, 0.3 + (n_rows - 1 - r)), 0.9, 0.85, facecolor=color,
                                       edgecolor="white", lw=1))
        if not columnar:
            # Toda la fila se lee: contorno de cada fila. The whole row is read: outline every row.
            for r in range(n_rows):
                ax.add_patch(Rectangle((0.15, 0.27 + r), n_cols + 0.0, 0.91, fill=False, edgecolor=INK_SOFT, lw=0.9))
        else:
            ax.add_patch(Rectangle((0.15, 0.27), n_cols, 2 * 0.98, fill=False, edgecolor=MUTED, lw=0.9,
                                   ls=(0, (3, 2))))
        ax.text(0.2, n_rows + 1.65, t["col_title"] if columnar else t["row_title"], fontsize=11,
                fontweight="bold", color=INK, va="center")
        ax.text(0.2, n_rows + 0.85, t["col_note"] if columnar else t["row_note"], fontsize=8.6,
                color=INK_SOFT, va="center")

    values = [100, 30, 5.3, 1.2]
    colors = [GRAY, GRAY, ACCENT, OK]
    y = np.arange(len(values))
    bars = ax_bar.barh(y, values, color=colors, height=0.58, zorder=3)
    for b, v in zip(bars, values):
        ax_bar.text(v + 1.2, b.get_y() + b.get_height() / 2, fmt(v, t, 0 if v >= 10 else 1) + " GB",
                    va="center", fontsize=10, fontweight="bold", color=INK)
    for i in (0, 1):
        ax_bar.text(values[i] + 13 + (3 if i == 0 else 0), i, f"({t['all_cols']})", va="center", fontsize=8.6, color=MUTED)
    ax_bar.set_yticks(y)
    ax_bar.set_yticklabels(t["bars"], fontsize=9.5)
    ax_bar.invert_yaxis()
    ax_bar.set_xlim(0, 128)
    ax_bar.set_xlabel(t["scanned"])
    ax_bar.set_title(t["query"], fontsize=10.5, loc="left", color=INK, fontweight="bold")
    clean_axes(ax_bar)
    ax_bar.spines["left"].set_visible(False)
    ax_bar.tick_params(left=False)
    fig.text(0.99, 0.01, t["illustrative"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(h_pad=1.5, rect=(0, 0.02, 1, 1))
    save(fig, out, "columnar-scan")


# ─── 2. Shard caliente / hot shard ─────────────────────────────────────────────
def chart_kinesis_hot_shard(t, out):
    fig, (ax1, ax2) = figure(5.4, nrows=2, sharex=True)
    shards = np.arange(1, 11)
    bad = np.array([0.25, 0.3, 0.2, 1.6, 0.3, 0.25, 0.35, 0.2, 0.3, 0.25])  # total 4.0
    good = np.array([0.41, 0.38, 0.42, 0.39, 0.4, 0.43, 0.37, 0.41, 0.38, 0.41])  # total 4.0

    for ax, vals, title, ok in ((ax1, bad, t["bad_title"], False), (ax2, good, t["good_title"], True)):
        colors = [ACCENT if v > 1 else (OK if ok else GRAY) for v in vals]
        ax.bar(shards, np.minimum(vals, 1), color=colors, width=0.62, zorder=3)
        over = vals > 1
        if over.any():
            ax.bar(shards[over], vals[over] - 1, bottom=1, color="white", edgecolor=ACCENT, hatch="////",
                   width=0.62, lw=1, zorder=3)
            i = int(np.argmax(vals))
            ax.annotate(t["throttled"], xy=(shards[i] + 0.35, 1.45), xytext=(shards[i] + 1.2, 1.55),
                        fontsize=8.8, color=ACCENT, va="center",
                        arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
        ax.axhline(1, color=INK, lw=1, ls=(0, (4, 3)), zorder=4)
        ax.text(10.45, 1.04, t["limit"], ha="right", va="bottom", fontsize=8.6, color=INK)
        ax.set_title(title, fontsize=10.5, loc="left", color=INK, fontweight="bold")
        ax.text(0.99, 0.97, t["total"], transform=ax.transAxes, ha="right", va="top", fontsize=8.6,
                color=INK_SOFT)
        ax.set_ylim(0, 1.95)
        ax.set_ylabel(t["mbps"])
        ax.yaxis.set_major_formatter(lambda v, _: fmt(v, t, 1))
        ax.yaxis.grid(True, color=RULE, lw=0.6, zorder=0)
        clean_axes(ax)
    ax2.set_xticks(shards)
    ax2.set_xlabel(t["shard"])
    fig.text(0.99, 0.01, t["illustrative_k"], ha="right", fontsize=8, color=MUTED)
    fig.tight_layout(h_pad=1.6, rect=(0, 0.03, 1, 1))
    save(fig, out, "kinesis-hot-shard")


# ─── 3. Ciclo de vida de S3 / S3 lifecycle ─────────────────────────────────────
def chart_s3_lifecycle(t, out):
    # Línea de tiempo a escala (0–365 días) con el costo relativo por GB como escalones. Illustrative cost.
    fig, ax = figure(4.9)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    W, H = 395, 11.8
    diagram_axes(ax, W, H)
    ax.set_xlim(-14, 381)
    x365 = 365
    colors = [(OK, "#e8f3ed"), (AMBER, "#fff6e0"), (INK_SOFT, SURFACE)]
    edges = [0, 30, 180, 365]
    top, bot = 10.5, 5.2
    class_icons = ["aws/s3", "aws/s3", "aws/s3-glacier-deep-archive"]  # Standard y Standard-IA comparten el ícono de S3 / share the S3 icon
    levels = [8.0, 6.8, 5.75]
    ax.text(-10, H - 0.35, t["lc_title"], fontsize=10.4, fontweight="bold", color=INK, va="top")
    for i, ((edge, fill), name) in enumerate(zip(colors, t["classes"])):
        x0, x1 = edges[i], edges[i + 1]
        ax.add_patch(Rectangle((x0, bot), x1 - x0, top - bot, facecolor=fill, edgecolor="white", lw=1.5, zorder=1))
        ax.add_patch(Rectangle((x0, top - 0.12), x1 - x0, 0.12, facecolor=edge, edgecolor="none", zorder=2))
        place_icon(ax, class_icons[i], (x0 + x1) / 2, top - 0.8, 1.0)
        fit_to(ax.text((x0 + x1) / 2, top - 1.4, name, fontsize=9.6, fontweight="bold", color=INK, va="top",
                       ha="center", zorder=3, linespacing=1.15), (x1 - x0) - 4, 1.2)
        # Escalón de costo / cost step
        ax.plot([x0, x1], [levels[i]] * 2, color=INK, lw=2.2, zorder=4, solid_capstyle="butt")
        ax.fill_between([x0, x1], bot, levels[i], color=edge, alpha=0.13, zorder=2, lw=0)
        if i:
            ax.plot([x0, x0], [levels[i - 1], levels[i]], color=INK, lw=2.2, zorder=4)
            ax.scatter([x0], [levels[i]], s=48, c=ACCENT, zorder=5, edgecolors="white", linewidths=1.2)
    ax.text(100, levels[1] + 0.4, t["lc_monthly"], fontsize=8.4, color=INK_SOFT, ha="center", va="bottom", zorder=5)
    ax.text(272, levels[2] + 0.4, t["lc_restore"], fontsize=8.4, color=INK_SOFT, ha="center", va="bottom", zorder=5)
    ax.text(105, 8.05, t["lc_cost"], fontsize=8.2, color=MUTED, ha="center", va="center", style="italic", zorder=5)
    # Días en el eje / days on the axis
    for day, label in zip(edges, t["day_marks"]):
        ax.plot([day, day], [bot, bot - 0.2], color=INK, lw=1)
        ax.text(day, bot - 0.3, label, fontsize=8.6, color=INK, va="top",
                ha="left" if day == 0 else ("right" if day == x365 else "center"))
    # Permanencia mínima desde la entrada a cada clase / minimum duration from entry into each class
    for start, length, key in ((30, 30, "lc_min30"), (180, 180, "lc_min180")):
        yb = 3.9
        ax.plot([start, start + length], [yb, yb], color=INK_SOFT, lw=1.3)
        for xx in (start, start + length):
            ax.plot([xx, xx], [yb - 0.14, yb + 0.14], color=INK_SOFT, lw=1.3)
        ax.text(start + length / 2 if length > 30 else start, yb - 0.3, t[key], fontsize=8.4, color=INK_SOFT,
                ha="center" if length > 30 else "left", va="top")
    # Object Lock durante toda la retención / Object Lock across the retention
    lock_w = 1.0 * _y_to_x(ax)  # ancho del ícono en unidades x / icon width in x units
    place_icon(ax, "aws/s3-object-lock", lock_w / 2, 2.95, 1.0)
    ax.text(lock_w + 4, 2.95, t["lc_lock"], fontsize=8.8, color=ACCENT, fontweight="bold", va="center")
    ax.add_patch(Rectangle((0, 1.9), x365, 0.4, facecolor=ACCENT, edgecolor="none", zorder=2))
    ax.text(0, 1.7, t["lc_nobody"], fontsize=8.8, color=INK, va="top")
    ax.text(x365, 0.45, t["lc_note"], fontsize=7.8, color=MUTED, ha="right", va="center")
    save(fig, out, "s3-lifecycle")


# ─── 4. Arquitectura del ejemplo / the worked example's architecture ───────────
def chart_example_paths(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 5.6), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.05)  # antes de los íconos / before icons
    diagram_axes(ax, 16, 10.4)
    c = [0.15, 4.15, 8.15, 12.15]
    w, h = 3.6, 1.75
    r1, r2, r3, r4 = 8.4, 5.7, 3.0, 0.3
    node = dict(edge=RULE, fill=SURFACE, size=8.6, desc_size=7.8)
    icon_node(ax, c[0], r1, w, h, "aws/users", t["ex_events"], **node)
    icon_node(ax, c[1], r1, w, h, "aws/kinesis-data-streams", t["ex_kds"], **node)
    icon_node(ax, c[2], r1, w, h, "aws/data-firehose", t["ex_fh"], **node)
    icon_node(ax, c[3], r2, w, r1 + h - r2, "aws/s3", t["ex_s3"], **node)
    icon_node(ax, c[0], r2, w, h, "aws/rds", t["ex_rds"], **node)
    icon_node(ax, c[3], r3, w, h, "aws/glue", t["ex_glue"], **node)
    icon_node(ax, c[3], r4, w, h, "aws/sagemaker-ai", t["ex_off"], **node)
    box(ax, c[1], r3, w, h, t["ex_cons"], edge=ACCENT, fill="white", size=8.6)
    icon_node(ax, c[2], r3, w, h, "aws/sagemaker-ai", t["ex_on"], edge=ACCENT, fill="white", size=8.6, desc_size=7.8)
    box(ax, c[1] + 0.5, r4 + 0.25, c[2] + w - c[1] - 0.5, 1.25, t["ex_train"], edge=INK_SOFT, fill="white", size=8.6)

    mid = lambda r: r + h / 2  # noqa: E731
    gap = 0.08
    arrow(ax, (c[0] + w + gap, mid(r1)), (c[1] - gap, mid(r1)), color=INK_SOFT)
    arrow(ax, (c[1] + w + gap, mid(r1)), (c[2] - gap, mid(r1)), color=INK_SOFT)
    arrow(ax, (c[2] + w + gap, mid(r1)), (c[3] - gap, mid(r1)), color=INK_SOFT)
    arrow(ax, (c[0] + w + gap, mid(r2)), (c[3] - gap, mid(r2)), color=INK_SOFT)
    fit_to(ax.text(c[2] + 0.5, mid(r2) + 0.18, t["ex_snap"], ha="center", va="bottom", fontsize=8.2,
                   color=INK_SOFT, multialignment="center"), 6.4)
    arrow(ax, (c[3] + w / 2, r2 - gap), (c[3] + w / 2, r3 + h + gap), color=INK_SOFT)
    arrow(ax, (c[3] + w / 2, r3 - gap), (c[3] + w / 2, r4 + h + gap), color=INK_SOFT)
    arrow(ax, (c[3] - gap, r4 + 0.88), (c[2] + w + gap, r4 + 0.88), color=INK_SOFT)
    # Ruta en tiempo real: del stream al online store. Real-time path: stream to online store.
    arrow(ax, (c[1] + 0.6, r1 - gap), (c[1] + 0.6, r3 + h + gap), color=ACCENT)
    arrow(ax, (c[1] + w + gap, mid(r3)), (c[2] - gap, mid(r3)), color=ACCENT)

    for i, (label, color) in enumerate(((t["ex_batch"], INK_SOFT), (t["ex_rt"], ACCENT))):
        y = r3 + 1.35 - i * 0.7
        ax.plot([c[0] + 0.2, c[0] + 0.9], [y, y], color=color, lw=1.6)
        ax.text(c[0] + 1.05, y, label, va="center", fontsize=8.6, color=color)
    ax.set_title(t["ex_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.01, t["ex_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "example-paths")


# ─── 5. Arquitectura del data lake / data lake architecture ────────────────────
def chart_lake_architecture(t, out):
    fig, ax = plt.subplots(figsize=(WIDTH_IN, 5.0), dpi=DPI)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.07)  # antes de los íconos / before icons
    diagram_axes(ax, 16, 9.0)
    node = dict(edge=RULE, fill=SURFACE, size=9.4, desc_size=8.4)
    ya, h = 6.4, 2.2
    xs = [0.2, 5.8, 11.4]
    icon_node(ax, xs[0], ya, 4.4, h, "aws/s3", t["lake_s3"], **node)
    icon_node(ax, xs[1], ya, 4.4, h, "aws/glue-crawler", t["lake_crawler"], **node)
    icon_node(ax, xs[2], ya, 4.4, h, "aws/glue-data-catalog", t["lake_catalog"], **node)
    gap = 0.08
    for a, b in ((0, 1), (1, 2)):
        arrow(ax, (xs[a] + 4.4 + gap, ya + h / 2), (xs[b] - gap, ya + h / 2), color=INK_SOFT)

    # Capa de permisos: la pieza clave, con el acento. Permissions layer: the key piece, in the accent.
    yb, hb = 3.35, 1.95
    box(ax, 0.2, yb, 15.6, hb, "", edge=ACCENT, fill="white", lw=1.8)
    lw_ = 1.15 * _y_to_x(ax)  # ancho del ícono en unidades x / icon width in x units
    place_icon(ax, "aws/lake-formation", 0.6 + lw_ / 2, yb + hb / 2, 1.15)
    ax.text(0.6 + lw_ + 0.25, yb + hb / 2, t["lake_lf"], ha="left", va="center", fontsize=11, color=ACCENT,
            fontweight="bold", zorder=3)
    chips = t["lake_chips"]
    for x, w, text in ((5.5, 4.9, chips[0]), (10.6, 2.0, chips[1]), (12.9, 2.7, chips[2])):
        box(ax, x, yb + 0.45, w, 1.05, text, edge=RULE, fill=SURFACE, size=9.2)
    arrow(ax, (xs[2] + 2.2, ya - gap), (xs[2] + 2.2, yb + hb + gap), color=INK_SOFT)

    # Consumidores: los permisos se aplican en cada uno. Consumers: permissions apply in each.
    yc, hc, w, step = 0.55, 1.55, 2.8, 3.2
    consumer_icons = ["aws/athena", "aws/redshift", "aws/emr", "aws/glue", "aws/quick"]
    for i, name in enumerate(t["lake_consumers"]):
        x = 0.2 + i * step
        icon_node(ax, x, yc, w, hc, consumer_icons[i], name, edge=RULE, fill="white", size=9.4, desc_size=8.2,
                  icon_size=1.05)
        arrow(ax, (x + w / 2, yb - gap), (x + w / 2, yc + hc + gap), color=INK_SOFT)
    ax.set_title(t["lake_title"], fontsize=10.2, loc="left", color=INK, fontweight="bold")
    fig.text(0.99, 0.015, t["lake_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "lake-architecture")


# ─── 6. Poda de particiones / partition pruning ────────────────────────────────
def chart_partition_pruning(t, out):
    fig = plt.figure(figsize=(WIDTH_IN, 3.9), dpi=DPI)
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.4], left=0.02, right=0.98, top=0.78, bottom=0.12, wspace=0.08)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    # Izquierda: el filtro elige una carpeta. Left: the filter picks one folder.
    diagram_axes(ax1, 10, 10)
    iw1 = 1.1 * _y_to_x(ax1)  # ancho del ícono en unidades x / icon width in x units
    place_icon(ax1, "aws/s3", 0.2 + iw1 / 2, 9.3, 1.1)
    ax1.text(0.2 + iw1 + 0.3, 9.3, t["pp_root"], ha="left", va="center", fontsize=9, color=INK_SOFT, family="monospace")
    box(ax1, 0.2, 7.45, 9.6, 1.25, t["pp_filter"], edge=ACCENT, fill="white", size=9.4, color=ACCENT, weight="bold")
    place_icon(ax1, "aws/athena", 0.2 + 0.2 + 1.05 * _y_to_x(ax1) / 2, 8.075, 1.05)
    ax1.text(5, 6.85, "···", ha="center", va="center", fontsize=11, color=MUTED)
    rows = [("dt=2026-09", t["pp_skip"], False), ("dt=2026-10", t["pp_read"], True), ("dt=2026-11", t["pp_skip"], False)]
    for i, (name, tag, hit) in enumerate(rows):
        y = 5.3 - i * 1.75
        box(ax1, 0.2, y, 9.6, 1.25, f"{name}  ·  {tag}", edge=ACCENT if hit else RULE,
            fill="#fdf0f2" if hit else SURFACE, size=9.2, color=ACCENT if hit else MUTED,
            weight="bold" if hit else "normal", lw=1.6 if hit else 1.1)
    ax1.text(5, 1.0, "···", ha="center", va="center", fontsize=11, color=MUTED)
    ax1.set_title(t["pp_left"], fontsize=9.6, loc="left", color=INK, fontweight="bold")

    # Derecha: GB escaneados. Right: GB scanned.
    values = [100.0, 8.3, 1.2]
    colors = [GRAY, ACCENT, ACCENT]
    alphas = [1, 1, 0.5]
    ys = [2.0, 1.0, 0.0]
    for y, v, c, a in zip(ys, values, colors, alphas):
        ax2.barh(y, v, height=0.34, color=c, alpha=a, zorder=3)
    for y, v, label in zip(ys, values, t["pp_bars"]):
        ax2.text(0, y + 0.3, label, ha="left", va="bottom", fontsize=9, color=INK_SOFT)
        share = fmt(v, t, 0 if v >= 10 else 1)
        ax2.text(v + 3, y, f"{share} GB", ha="left", va="center", fontsize=9.4, color=INK, fontweight="bold")
    ax2.set_xlim(0, 150)
    ax2.set_ylim(-0.45, 2.75)
    ax2.set_yticks([])
    ax2.set_xticks([])
    clean_axes(ax2)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.set_title(t["pp_right"], fontsize=9.6, loc="left", color=INK, fontweight="bold")
    fig.suptitle(t["pp_title"], x=0.02, y=0.975, ha="left", fontsize=10.4, color=INK, fontweight="bold")
    fig.text(0.98, 0.02, t["pp_note"], ha="right", fontsize=8, color=MUTED)
    save(fig, out, "partition-pruning")


CHARTS = [chart_columnar_scan, chart_kinesis_hot_shard, chart_s3_lifecycle, chart_example_paths,
          chart_lake_architecture, chart_partition_pruning]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
