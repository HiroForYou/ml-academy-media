"""
Paleta, estilo de matplotlib y utilidades compartidas por los gráficos de todos los temas.
Palette, matplotlib style and helpers shared by every topic's charts.

Cada módulo de tema (charts/topics/<topic>.py) define TEXT = {"es": {...}, "en": {...}} y
CHARTS = [funciones]; cada función recibe (t, out) y guarda <nombre>.png en out.
Each topic module defines TEXT and CHARTS; each function takes (t, out) and saves <name>.png.
"""

import argparse
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Rectangle  # noqa: E402
from matplotlib.text import Text  # noqa: E402

# Paleta del sitio / site palette
INK = "#111114"
INK_SOFT = "#3d3d45"
MUTED = "#6a6a74"
SURFACE = "#f3f3f5"
RULE = "#e2e2e6"
ACCENT = "#b3132b"
OK = "#1f7a4d"
AMBER = "#ffb21c"
GRAY = "#c9c9cf"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.edgecolor": RULE,
        "axes.linewidth": 0.8,
        "text.color": INK,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        # Fórmulas con mathtext estilo LaTeX (sin instalar TeX). LaTeX-style mathtext formulas (no TeX install).
        "mathtext.fontset": "cm",
    }
)

DPI = 200
WIDTH_IN = 8.0  # 8 in x 200 dpi = 1600 px


def clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(RULE)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(length=3, labelsize=9.5)


def fmt(value, t, digits=1, suffix=""):
    """Número con el separador decimal del idioma. Number with the language's decimal separator."""
    return f"{value:.{digits}f}".replace(".", t["decimal"]) + suffix


def pct(value, t, digits=0):
    """Porcentaje: «12 %» en español, «12%» en inglés. Percentage in each language's style."""
    return fmt(value, t, digits, " %" if t["decimal"] == "," else "%")


def figure(height, **kwargs):
    return plt.subplots(figsize=(WIDTH_IN, height), dpi=DPI, **kwargs)


def save(fig, out, name):
    """Ajusta el texto de las cajas, revisa que nada se salga y guarda. Fits box text, checks overflow, saves."""
    for job in getattr(fig, "_mla_fit_jobs", []):
        job(fig.canvas.get_renderer())
    check_fit(fig, name)
    fig.savefig(os.path.join(out, f"{name}.png"))
    plt.close(fig)


# ─── Texto que cabe en su caja / text that fits its box ────────────────────────
MIN_FONT = 8.5  # pt; mínimo legible a 200 dpi / legible minimum at 200 dpi
FIT_PAD_PX = 9  # margen interior al ajustar / inner margin when fitting (px at 200 dpi)
CHECK_PAD_PX = 4  # margen exigido por check_fit / margin required by check_fit
_LANG = os.environ.get("MLA_LANG", "")


def _extent(txt, renderer):
    # Text.get_window_extent también para Annotation (sin la flecha). Text only, also for annotations.
    return Text.get_window_extent(txt, renderer)


def _wrap(txt, source, max_w, renderer):
    """Parte cada línea en palabras para que quepa en max_w px, con líneas de largo parecido (sin una palabra
    huérfana al final). Word-wraps each line to max_w px with balanced lines (no orphan last word)."""

    def greedy(words, width):
        lines, cur = [], ""
        for word in words:
            cand = f"{cur} {word}" if cur else word
            txt.set_text(cand)
            if cur and _extent(txt, renderer).width > width:
                lines.append(cur)
                cur = word
            else:
                cur = cand
        return lines + [cur]

    out = []
    for line in source.split("\n"):
        if "$" in line or not line.strip():  # no partir fórmulas / never split mathtext
            out.append(line)
            continue
        words = line.split(" ")
        lines = greedy(words, max_w)
        width = max_w
        # Con una línea por palabra ya no se puede angostar más (evita un bucle infinito).
        # With one line per word it cannot be narrowed any further (avoids an endless loop).
        while 1 < len(lines) < len(words):  # angostar mientras no sume líneas / narrow while the line count holds
            width *= 0.95
            narrower = greedy(words, width)
            if len(narrower) > len(lines):
                break
            lines = narrower
        out += lines
    text = "\n".join(out)
    txt.set_text(text)
    return text


def _sizes(size, floor):
    s = size
    while s >= floor - 1e-9:
        yield s
        s = round(s - 0.25, 2)


def fit_text(txt, max_w, max_h, renderer, min_size=MIN_FONT):
    """Parte líneas y, si aún no cabe, reduce la fuente hasta min_size. Devuelve True si cabe.
    Wraps lines and, if still too big, shrinks the font down to min_size. Returns True when it fits."""
    source = getattr(txt, "_mla_source", None) or txt.get_text()
    txt._mla_source = source
    size0 = txt.get_fontsize()
    for size in _sizes(size0, min(size0, min_size)):
        txt.set_fontsize(size)
        _wrap(txt, source, max_w, renderer)
        bb = _extent(txt, renderer)
        if bb.width <= max_w and bb.height <= max_h:
            return True
    return False


def fit_to(txt, width, height=None, min_size=MIN_FONT):
    """Al guardar, parte `txt` (y si hace falta lo reduce) para que quepa en `width` × `height` unidades de
    datos de sus ejes; sin `height`, solo limita el ancho. For hand-placed text: on save, wraps (and if needed
    shrinks) `txt` to fit `width` × `height` data units of its axes; without `height`, only the width."""
    ax = txt.axes

    def job(renderer):
        (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (width, height or 0)])
        fit_text(txt, abs(x1 - x0), abs(y1 - y0) if height else float("inf"), renderer, min_size)

    _defer(ax.figure, job)
    return txt


def _defer(fig, job):
    if not hasattr(fig, "_mla_fit_jobs"):
        fig._mla_fit_jobs = []
    fig._mla_fit_jobs.append(job)


def _figure_texts(fig):
    texts = list(fig.texts)
    for leg in fig.legends:
        texts += [*leg.get_texts(), leg.get_title()]
    for ax in fig.axes:
        if not ax.get_visible():
            continue
        texts += ax.texts + [ax.title, ax._left_title, ax._right_title]
        if ax.axison:
            for axis in (ax.xaxis, ax.yaxis):
                texts += [axis.label, axis.offsetText]
                for tick in axis._update_ticks():
                    texts += [lab for lab in (tick.label1, tick.label2) if lab.get_visible()]
        leg = ax.get_legend()
        if leg:
            texts += [*leg.get_texts(), leg.get_title()]
    return [t for t in texts if t.get_visible() and t.get_text().strip()]


def check_fit(fig, name="", pad=CHECK_PAD_PX, quiet=False):
    """Revisa con el renderer que cada texto quepa en su caja, dentro de la figura y sin pisar otro texto.
    Imprime «FIT: …» por problema y devuelve la lista. Una caja es el rectángulo más pequeño (sin barras de
    datos ni bandas axvspan/axhspan) que contiene el centro del texto y está debajo de él.
    Checks with the renderer that every text fits its box, stays inside the figure and doesn't overlap
    another text. Prints "FIT: …" per issue and returns the list. A text's box is the smallest rectangle
    (not data bars or axvspan/axhspan bands) that contains the text's centre and is drawn below it."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fb = fig.bbox
    issues = []
    texts = _figure_texts(fig)
    exts = [_extent(t, renderer) for t in texts]
    label = lambda t: t.get_text().replace("\n", " / ")[:70]  # noqa: E731

    boxes = {}
    for ax in fig.axes:
        bars = {id(p) for c in ax.containers for p in c if isinstance(p, Patch)}
        ab = ax.get_window_extent(renderer)
        boxes[ax] = []
        for p in ax.patches:
            if not p.get_visible() or not isinstance(p, (Rectangle, FancyBboxPatch)) or id(p) in bars:
                continue
            pb = p.get_window_extent(renderer)
            if (pb.y0 <= ab.y0 + 1 and pb.y1 >= ab.y1 - 1) or (pb.x0 <= ab.x0 + 1 and pb.x1 >= ab.x1 - 1):
                continue  # banda que cruza los ejes, no una caja / a band across the axes, not a box
            boxes[ax].append((p, pb))

    for t, bb in zip(texts, exts):
        if bb.x0 < fb.x0 + 2 or bb.y0 < fb.y0 + 2 or bb.x1 > fb.x1 - 2 or bb.y1 > fb.y1 - 2:
            issues.append(f"outside figure (or touching its edge): «{label(t)}»")
            continue
        ax = t.axes
        if ax is None or t in (ax.title, ax._left_title, ax._right_title):
            continue
        cx, cy = (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2
        ab = ax.get_window_extent(renderer)
        if t in ax.texts and ab.contains(cx, cy):
            # Solo cuentan los bordes con spine visible (también de ejes gemelos). Only edges with a visible spine.
            spines = {side for a in fig.axes if a.axison and a.get_window_extent(renderer).bounds == ab.bounds
                      for side, sp in a.spines.items() if sp.get_visible()}
            out = {"left": bb.x0 < ab.x0 + pad, "right": bb.x1 > ab.x1 - pad, "bottom": bb.y0 < ab.y0 + pad,
                   "top": bb.y1 > ab.y1 - pad}
            if any(out[side] for side in spines):
                issues.append(f"crosses the axes edge: «{label(t)}»")
                continue
        inside = [(p, pb) for p, pb in boxes.get(ax, []) if pb.contains(cx, cy) and p.get_zorder() <= t.get_zorder()]
        if inside:
            p, pb = min(inside, key=lambda item: item[1].width * item[1].height)
            if bb.x0 < pb.x0 + pad or bb.x1 > pb.x1 - pad or bb.y0 < pb.y0 + pad or bb.y1 > pb.y1 - pad:
                issues.append(f"outside its box: «{label(t)}»")

    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = exts[i], exts[j]
            if texts[i].get_text() == texts[j].get_text() and (a.x0, a.y0) == (b.x0, b.y0):
                continue  # ejes gemelos repiten la misma etiqueta / twin axes repeat the same label
            if min(a.x1, b.x1) - max(a.x0, b.x0) > 1.5 and min(a.y1, b.y1) - max(a.y0, b.y0) > 1.5:
                issues.append(f"overlap: «{label(texts[i])}» × «{label(texts[j])}»")

    # Flechas (de annotate o de arrow()) que atraviesan un texto ajeno. Arrows crossing another text.
    arrows = []
    for ax in fig.axes:
        arrows += [(p, None) for p in ax.patches if isinstance(p, FancyArrowPatch) and p.get_visible()]
        arrows += [(t.arrow_patch, t) for t in ax.texts if getattr(t, "arrow_patch", None) is not None]
    for patch, owner in arrows:
        path = patch.get_path()
        pts = patch.get_transform().transform(path.interpolated(40).vertices)
        for t, bb in zip(texts, exts):
            if t is owner or (t.get_bbox_patch() is not None and t.get_zorder() > patch.get_zorder()):
                continue  # una insignia con fondo tapa la flecha a propósito / a badge covers it on purpose
            if any(bb.x0 + 2 < x < bb.x1 - 2 and bb.y0 + 2 < y < bb.y1 - 2 for x, y in pts):
                issues.append(f"arrow crosses text: «{label(t)}»")

    if not quiet:
        for msg in issues:
            print(f"FIT: {name} ({_LANG}) {msg}")
    return issues


def diagram_axes(ax, width, height):
    """Ejes en blanco con coordenadas de datos para diagramas. Blank axes in data units for diagrams."""
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")


def box(ax, x, y, w, h, text, edge=INK_SOFT, fill=SURFACE, size=10, color=INK, weight="normal", lw=1.3):
    """Caja redondeada con texto centrado. Al guardar, el texto se parte en líneas y, si hace falta, se reduce
    hasta MIN_FONT para que quepa. Rounded box with centred text; on save the text is wrapped and, if needed,
    shrunk down to MIN_FONT so it fits."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", linewidth=lw, edgecolor=edge,
                           facecolor=fill, zorder=2)
    ax.add_patch(patch)
    if text:
        txt = ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color,
                      fontweight=weight, zorder=3, multialignment="center")

        def job(renderer):
            pb = patch.get_window_extent(renderer)
            fit_text(txt, pb.width - 2 * FIT_PAD_PX, pb.height - 2 * FIT_PAD_PX, renderer)

        _defer(ax.figure, job)
    return patch


def arrow(ax, start, end, color=MUTED, lw=1.4, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=12, linewidth=lw, color=color,
                                 zorder=1, shrinkA=0, shrinkB=0))


# ─── Nodos con ícono / icon nodes ──────────────────────────────────────────────
# Íconos SVG en assets/icons/{aws,tools}/ (ver assets/icons/README.md). Se rasterizan con resvg una vez
# y se guardan en output/_icons/ (no versionado). SVG icons are rasterized once with resvg into output/_icons/.
ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
ICON_CACHE = ROOT / "output" / "_icons"
# Los íconos de Simple Icons son monocromos: se pintan con el color de la marca.
# Simple Icons are monochrome: they are painted with the brand color.
TOOL_COLORS = {"tools/pytorch": "#EE4C2C", "tools/tensorflow": "#FF6F00"}


def icon_png(name, px=256):
    """Ruta del PNG rasterizado de assets/icons/<name>.svg. Path of the rasterized PNG of an icon."""
    ICON_CACHE.mkdir(parents=True, exist_ok=True)
    png = ICON_CACHE / f"{name.replace('/', '__')}-{px}.png"
    if not png.exists():
        import resvg_py

        svg = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
        if name in TOOL_COLORS:
            svg = svg.replace("<svg ", f'<svg fill="{TOOL_COLORS[name]}" ', 1)
        png.write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg, width=px, height=px)))
    return png


def _y_to_x(ax):
    """Unidades x que miden en pantalla lo mismo que una unidad y. x units matching one y unit on the page."""
    bbox = ax.get_window_extent()
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    return (bbox.height / (y1 - y0)) / (bbox.width / (x1 - x0))


def place_icon(ax, name, cx, cy, size):
    """Dibuja el ícono centrado en (cx, cy) con alto `size` en unidades de datos, sin deformarlo.
    Draws the icon centred at (cx, cy), `size` data units tall, keeping it square on the page."""
    w = size * _y_to_x(ax)
    ax.imshow(plt.imread(icon_png(name)), extent=(cx - w / 2, cx + w / 2, cy - size / 2, cy + size / 2),
              aspect="auto", zorder=4, interpolation="antialiased")
    return w


def icon_node(ax, x, y, w, h, icon, text, edge=RULE, fill=SURFACE, size=9, color=INK, desc_size=None,
              desc_color=INK_SOFT, lw=1.3, icon_size=None, title_lines=1):
    """Caja redondeada con el logo a la izquierda, título en negrita y descripción corta debajo.
    `text` = "Título\\ndescripción…": las primeras `title_lines` líneas son el título. Devuelve las anclas.
    Al guardar, título y descripción se parten al ancho libre y, si aún no caben, se reducen hasta MIN_FONT.
    Llama a fig.subplots_adjust y diagram_axes antes: el ícono se ajusta al tamaño final de los ejes.
    Rounded box with the logo on the left, a bold title and a short description below it. The first
    `title_lines` lines are the title. On save, both are wrapped to the free width and, if still too big,
    shrunk down to MIN_FONT. Call subplots_adjust and diagram_axes first. Returns the anchors."""
    ax.add_patch(
        FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", linewidth=lw, edgecolor=edge,
                       facecolor=fill, zorder=2)
    )
    s = icon_size or min(h * 0.62, 1.15)
    pad = min(0.22, h * 0.18)
    iw = s * _y_to_x(ax)  # ancho del ícono en unidades x / icon width in x units
    if isinstance(icon, (list, tuple)):  # varios servicios: cuadrícula 2×2 / several services: 2×2 grid
        k = s * 0.47
        for i, name in enumerate(icon[:4]):
            dx, dy = (i % 2 - 0.5) * s * 0.53, (0.5 - i // 2) * s * 0.53
            place_icon(ax, name, x + pad + iw / 2 + dx * _y_to_x(ax), y + h / 2 + dy, k)
    else:
        place_icon(ax, icon, x + pad + iw / 2, y + h / 2, s)
    tx = x + pad + iw + pad * 0.9
    lines = text.split("\n")
    title, desc = "\n".join(lines[:title_lines]), "\n".join(lines[title_lines:])
    dsize = desc_size or size - 1.2
    title_txt = ax.text(tx, y + h / 2, title, ha="left", va="top", fontsize=size, color=color, fontweight="bold",
                        zorder=5, linespacing=1.3)
    desc_txt = ax.text(tx, y + h / 2, desc, ha="left", va="top", fontsize=dsize, color=desc_color, zorder=5,
                       linespacing=1.3) if desc else None

    def job(renderer):
        # Medir con el tamaño final de los ejes. Measure with the final axes size.
        to_px = ax.transData.transform
        left, right = to_px((tx, 0))[0], to_px((x + w, 0))[0] - FIT_PAD_PX
        bottom, top = to_px((0, y))[1] + FIT_PAD_PX * 0.6, to_px((0, y + h))[1] - FIT_PAD_PX * 0.6
        max_w, max_h = right - left, top - bottom
        title_txt._mla_source = title
        if desc_txt:
            desc_txt._mla_source = desc
        diff = size - dsize
        for ts in _sizes(size, min(size, MIN_FONT)):
            ds = ts - diff
            title_txt.set_fontsize(ts)
            _wrap(title_txt, title, max_w, renderer)
            tb = _extent(title_txt, renderer)
            width, height, gap = tb.width, tb.height, 0
            if desc_txt:
                desc_txt.set_fontsize(ds)
                _wrap(desc_txt, desc, max_w, renderer)
                db = _extent(desc_txt, renderer)
                gap = 0.35 * ds * ax.figure.dpi / 72
                width, height = max(width, db.width), height + gap + db.height
            if width <= max_w and height <= max_h:
                break
        # Bloque título + descripción centrado en vertical. Title + description block, vertically centred.
        inv = ax.transData.inverted().transform
        mid = to_px((0, y + h / 2))[1]
        y_top = mid + height / 2
        title_txt.set_y(inv((0, y_top))[1])
        if desc_txt:
            desc_txt.set_y(inv((0, y_top - tb.height - gap))[1])

    _defer(ax.figure, job)
    return {"left": (x, y + h / 2), "right": (x + w, y + h / 2), "top": (x + w / 2, y + h),
            "bottom": (x + w / 2, y)}


def cli(text, charts):
    """Interfaz común: --lang es|en --out <dir>. Common CLI used by every topic module."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=text, default=os.environ.get("MLA_LANG", "es"))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    global _LANG
    _LANG = args.lang
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # avisos FIT con «» y → / FIT warnings
    os.makedirs(args.out, exist_ok=True)
    for chart in charts:
        chart(text[args.lang], args.out)
    print(f"{len(charts)} charts ({args.lang}) -> {args.out}")
