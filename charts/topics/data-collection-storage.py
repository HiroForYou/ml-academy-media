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
    DPI, WIDTH_IN, clean_axes, cli, diagram_axes, figure, fmt, plt, save,
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
        "lc_title": "Regla de ciclo de vida para la zona raw (ejemplo, no a escala)",
        "classes": ["S3 Standard", "S3 Standard-IA", "S3 Glacier Deep Archive"],
        "notes": [
            "Entrenamientos frecuentes",
            "Acceso mensual · mínimo 30 días",
            "Archivo · mínimo 180 días\nrestauración en horas",
        ],
        "day_marks": ["día 0", "día 30", "día 180", "día 365"],
        "lock": "Object Lock en modo compliance (retención de 365 días): nadie, ni siquiera root, puede borrar",
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
        "lc_title": "Lifecycle rule for the raw zone (example, not to scale)",
        "classes": ["S3 Standard", "S3 Standard-IA", "S3 Glacier Deep Archive"],
        "notes": [
            "Frequent training runs",
            "Monthly access · 30-day minimum",
            "Archive · 180-day minimum\nrestore takes hours",
        ],
        "day_marks": ["day 0", "day 30", "day 180", "day 365"],
        "lock": "Object Lock in compliance mode (365-day retention): nobody, not even root, can delete",
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
    # Esquema (no a escala): tres tramos de igual ancho. Schematic (not to scale): three equal-width spans.
    fig, ax = figure(2.9)
    diagram_axes(ax, 12, 3.45)
    ax.set_ylim(0.4, 3.45)
    colors = [(OK, "#e8f3ed"), (AMBER, "#fff6e0"), (INK_SOFT, SURFACE)]
    x0, w, y, h = 0.1, 3.9, 0.85, 1.25
    for i, ((edge, fill), name, note) in enumerate(zip(colors, t["classes"], t["notes"])):
        x = x0 + i * w
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor=edge, lw=1.4, zorder=2))
        ax.text(x + 0.18, y + h * 0.68, name, fontsize=10, fontweight="bold", color=INK, va="center", zorder=3)
        ax.text(x + 0.18, y + h * 0.3, note, fontsize=7.9, color=INK_SOFT, va="center", zorder=3)
    for i, day in enumerate(t["day_marks"]):
        x = x0 + i * w
        ax.plot([x, x], [y - 0.12, y], color=INK, lw=1)
        ax.text(x, y - 0.2, day, ha="center" if 0 < i < 3 else ("left" if i == 0 else "right"), va="top",
                fontsize=8.6, color=INK)
    ax.text(x0, 3.2, t["lc_title"], fontsize=11, fontweight="bold", color=INK, va="center")
    # Object Lock a lo largo de toda la retención. Object Lock across the whole retention period.
    ax.add_patch(Rectangle((x0, 2.3), 3 * w, 0.16, facecolor=ACCENT, edgecolor="none", zorder=2))
    ax.text(x0, 2.6, t["lock"], fontsize=8.6, color=ACCENT, va="bottom")
    fig.tight_layout()
    save(fig, out, "s3-lifecycle")


CHARTS = [chart_columnar_scan, chart_kinesis_hot_shard, chart_s3_lifecycle]

if __name__ == "__main__":
    cli(TEXT, CHARTS)
