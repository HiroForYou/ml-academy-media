"""
Paleta y utilidades compartidas por las escenas de Manim de cada tema.
Palette and helpers shared by every topic's Manim scenes.

Cada videos/<course>/<topic>/scenes.py declara VIDEOS = {"nombre-publicado": "ClaseDeEscena"}
(un literal que scripts/render_all.py lee sin importar Manim) y elige sus textos con pick(TEXT).
Each scenes.py declares VIDEOS (a literal render_all.py reads without importing Manim) and picks
its on-screen text with pick(TEXT).
"""

import os
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, WHITE, Circumscribe, FadeIn, FadeOut, MarkupText, MathTex, RoundedRectangle, Scene,
    SingleStringMathTex, SVGMobject, Text, VGroup, config,
)
from manim.animation.animation import Wait, prepare_animation
from manim.animation.fading import _Fade
from manim.animation.transform import ApplyFunction, ApplyMethod, FadeTransform, MoveToTarget, ReplacementTransform, Transform

config.background_color = WHITE

INK = "#111114"
INK_SOFT = "#3d3d45"
MUTED = "#6a6a74"
SURFACE = "#f3f3f5"
RULE = "#e2e2e6"
ACCENT = "#b3132b"
OK = "#1f7a4d"
AMBER = "#ffb21c"
GRAY = "#c9c9cf"

LANG = os.environ.get("MLA_LANG", "es")
# Familia genérica de Pango: usa la sans del sistema en cualquier SO. Generic Pango family: system sans on any OS.
FONT = os.environ.get("MLA_FONT", "Sans")


def pick(text):
    return text[LANG]


def label(text, size=24, color=INK, weight="NORMAL", max_width=None):
    txt = Text(text, font=FONT, font_size=size, color=color, weight=weight)
    if max_width and txt.width > max_width:
        txt.scale_to_fit_width(max_width)
    return txt


def math(tex, size=30, color=INK):
    return MathTex(tex, font_size=size, color=color)


def node(text, width=3.0, height=1.0, stroke=INK_SOFT, fill=SURFACE, size=22, color=INK):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=stroke, stroke_width=2)
    box.set_fill(fill, opacity=1)
    txt = label(text, size, color, max_width=width - 0.3)
    if txt.height > height - 0.15:
        txt.scale_to_fit_height(height - 0.15)
    return VGroup(box, txt.move_to(box))


# ─── Nodos con ícono / icon nodes ──────────────────────────────────────────────
# Íconos SVG en assets/icons/{aws,tools}/ (ver assets/icons/README.md). SVG icons, see assets/icons/README.md.
ICON_DIR = Path(__file__).resolve().parents[1] / "assets" / "icons"
TOOL_COLORS = {"tools/pytorch": "#EE4C2C", "tools/tensorflow": "#FF6F00"}


def icon(name, height=0.6):
    """Ícono vectorial (SVGMobject) de assets/icons/<name>.svg. Vector icon from assets/icons/<name>.svg."""
    mob = SVGMobject(str(ICON_DIR / f"{name}.svg"), height=height)
    if mob.width > height:  # íconos anchos caben en el mismo cuadrado / wide icons fit the same square
        mob.scale_to_fit_width(height)
    if name in TOOL_COLORS:  # Simple Icons: monocromo / monochrome
        mob.set_fill(TOOL_COLORS[name], opacity=1).set_stroke(width=0)
    return mob


def icon_node(icon_name, title, desc=None, width=3.2, height=1.1, stroke=RULE, fill=SURFACE, title_size=20,
              desc_size=15, title_color=INK, desc_color=INK_SOFT, icon_height=None, stroke_width=2):
    """Caja redondeada con el logo a la izquierda, título en negrita y descripción corta debajo.
    Rounded box with the logo on the left, a bold title and a short description below it.
    Partes / parts: node.box, node.icon, node.title, node.desc (puede ser None / may be None)."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=stroke,
                           stroke_width=stroke_width)
    box.set_fill(fill, opacity=1)
    ic = icon(icon_name, icon_height or min(height * 0.62, 0.8))
    ic.move_to(box.get_left() + RIGHT * (0.16 + ic.width / 2))
    text_w = width - ic.width - 0.5
    ttl = label(title, title_size, title_color, "BOLD")
    if ttl.width > text_w / 0.85 and " " in title and "\n" not in title:
        # Título mucho más largo que el espacio: dos líneas, cortando en el espacio más cercano al centro.
        # (Si sobra poco, solo se reduce.) Title much longer than the room: two lines split at the space
        # closest to the middle. (If it barely overflows, it is only scaled down.)
        cut = min((i for i, ch in enumerate(title) if ch == " "), key=lambda i: abs(i - len(title) / 2))
        ttl = label(title[:cut] + "\n" + title[cut + 1:], title_size, title_color, "BOLD")
    if ttl.width > text_w:
        ttl.scale_to_fit_width(text_w)
    parts = [ttl]
    dsc = None
    if desc:
        dsc = label(desc, desc_size, desc_color, max_width=text_w)
        parts.append(dsc)
    block = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    if block.height > height - 0.16:
        block.scale_to_fit_height(height - 0.16)
    block.next_to(ic, RIGHT, buff=0.18)
    node = VGroup(box, ic, block)
    node.box, node.icon, node.title, node.desc = box, ic, ttl, dsc
    return node


def pulse(node, color, **kwargs):
    """Destaca un nodo con un contorno que aparece y se desvanece, sin teñir el logo.
    Highlights a node with an outline that appears and fades, without tinting the logo."""
    box = getattr(node, "box", node)
    return Circumscribe(box, color=color, buff=0.06, stroke_width=4, fade_out=True, **kwargs)


def icon_title(icon_name, title, size=18, color=INK, icon_height=0.4, max_width=None):
    """Encabezado «logo + título en negrita» para cajas contenedoras. Logo + bold title header for containers."""
    ic = icon(icon_name, icon_height)
    ttl = label(title, size, color, "BOLD", max_width=(max_width - ic.width - 0.12) if max_width else None)
    return VGroup(ic, ttl).arrange(RIGHT, buff=0.12)


def num(value, digits=1, suffix=""):
    s = f"{value:.{digits}f}"
    return (s.replace(".", ",") if LANG == "es" else s) + suffix


def pct(value, digits=1):
    return num(value, digits, " %" if LANG == "es" else "%")


def tex_num(value, digits=1):
    """Número para MathTex: la coma decimal va entre llaves para que no añada espacio.
    Number for MathTex: the decimal comma is braced so it adds no space."""
    return num(value, digits).replace(",", "{,}")


# ─── Ritmo de lectura / reading pace ───────────────────────────────────────────
# Todas las escenas heredan de PacedScene en lugar de Scene. Sin cambiar la historia:
#   1. Ralentiza cada transición (SPEED) y da al menos MIN_TEXT_RUN_TIME a las que muestran o quitan texto.
#   2. Tras un paso que muestra texto, espera reading_time() de todo ese texto antes del siguiente cambio de
#      texto; las animaciones sin texto (puntos que se mueven, barras) cuentan como tiempo de lectura.
#   3. Si un play() quita un texto y muestra otro, primero lo quita y después muestra el nuevo: los subtítulos
#      nunca se superponen. Al final mantiene el último cuadro al menos FINAL_HOLD s.
# Every scene inherits PacedScene instead of Scene: slower transitions, a reading wait after each step that
# shows text (non-text animations count as reading time), fade-out before fade-in when one play() swaps texts,
# and a final hold. Waits come from the actual strings of the active language, so Spanish gets longer waits.
# Con MLA_PACING_LOG=<archivo> escribe cuándo aparece y desaparece cada texto (para verificar el ritmo).
# With MLA_PACING_LOG=<file> it logs when each text appears and disappears (to verify the pacing).

SPEED = 1.5               # transiciones 1,5 veces más lentas / transitions 1.5x slower
MIN_TEXT_RUN_TIME = 0.8   # s, mínimo para animaciones con texto / minimum for animations carrying text
FINAL_HOLD = 2.5          # s, último cuadro fijo / final still frame
FORMULA_WORDS = 6         # una fórmula cuenta como ~6 palabras / a formula counts as ~6 words
STEP_CAP = 6.0            # s, tope para muchas etiquetas cortas a la vez / cap for many short labels at once
LABEL_WORDS = 2           # hasta aquí un texto es una etiqueta (cifra, nombre), no un subtítulo / up to here a text is a label
LABEL_EXTRA = 1.0         # s, lo máximo que suman las etiquetas junto a un subtítulo / most labels add next to a caption


def reading_time(words):
    """Segundos para leer `words` palabras: max(1,8 s; 0,38 s por palabra + 0,8 s).
    Seconds to read `words` words: max(1.8 s, 0.38 s per word + 0.8 s)."""
    return 0.0 if words <= 0 else max(1.8, 0.38 * words + 0.8)


def step_reading_time(word_counts):
    """Lectura de un paso que muestra varios textos. Los subtítulos (más de LABEL_WORDS palabras) reciben su
    tiempo completo; las etiquetas que los acompañan (cifras, nombres) se miran de reojo y suman como mucho
    LABEL_EXTRA s. Un paso solo de etiquetas (p. ej. el diagrama inicial) suma sus palabras con tope STEP_CAP.
    Reading time of a step that shows several texts. Captions (more than LABEL_WORDS words) get their full
    time; the labels with them (numbers, names) are glanced at and add at most LABEL_EXTRA s. A labels-only
    step (e.g. the initial diagram) sums its words, capped at STEP_CAP."""
    captions = [w for w in word_counts if w > LABEL_WORDS]
    labels = sum(w for w in word_counts if w <= LABEL_WORDS)
    if not captions:
        return min(reading_time(labels), STEP_CAP)
    return max(min(reading_time(sum(captions)), STEP_CAP), reading_time(max(captions))) + min(0.38 * labels, LABEL_EXTRA)


def _text_leaves(mob):
    if isinstance(mob, (Text, MarkupText, SingleStringMathTex)):
        yield mob
        return
    for sub in mob.submobjects:
        yield from _text_leaves(sub)


def _has_text(mob):
    return mob is not None and next(_text_leaves(mob), None) is not None


def _string(leaf):
    if isinstance(leaf, SingleStringMathTex):
        return leaf.tex_string
    return getattr(leaf, "original_text", None) or getattr(leaf, "text", "")


def _strings(mob):
    return [_string(leaf) for leaf in _text_leaves(mob)] if mob is not None else []


def same_text(a, b):
    """True si dos textos muestran lo mismo, en la misma posición y color. Same strings, position and color."""
    return (_strings(a) == _strings(b) and abs(a.get_center() - b.get_center()).max() < 1e-3
            and a.get_color() == b.get_color())


def text_words(leaf):
    """Palabras con letras cuentan 1, números sueltos 0,5, símbolos 0; una fórmula, FORMULA_WORDS.
    Words with letters count 1, bare numbers 0.5, symbols 0; a formula counts FORMULA_WORDS."""
    if isinstance(leaf, SingleStringMathTex):
        return FORMULA_WORDS
    return sum(1 if any(c.isalpha() for c in tok) else 0.5 if any(c.isalnum() for c in tok) else 0
               for tok in _string(leaf).split())


class PacedScene(Scene):
    def setup(self):
        super().setup()
        self._clock = 0.0   # s transcurridos / elapsed
        self._debt = 0.0    # lectura pendiente / reading time still owed
        self._idle = 0.0    # s quietos desde el último cambio / still time since the last change
        self._open = {}     # id(texto) -> registro / text record
        self._records = []

    def _show(self, leaf, key=None):
        words = text_words(leaf)
        rec = {"text": _string(leaf), "words": words, "need": round(reading_time(words), 2),
               "t_in": round(self._clock, 3), "t_out": None}
        self._records.append(rec)
        self._open[key if key is not None else id(leaf)] = rec

    def _hide(self, leaf):
        rec = self._open.pop(id(leaf), None)
        if rec is not None:
            rec["t_out"] = round(self._clock, 3)

    def remove(self, *mobjects):
        for m in mobjects:
            for leaf in _text_leaves(m):
                self._hide(leaf)
        return super().remove(*mobjects)

    def _hold(self, duration):
        if duration > 1e-3:
            Scene.play(self, Wait(run_time=duration))
            self._clock += duration
            self._debt -= duration
            self._idle += duration

    def beat(self, seconds):
        """Termina la lectura pendiente y añade una pausa real para mirar el resultado (wait() la absorbe).
        Finishes the pending reading and adds a real pause to look at the result (wait() absorbs it)."""
        self._hold(self._debt)
        self._hold(seconds)

    def play(self, *args, **kwargs):
        anims = [prepare_animation(a) for a in args]
        if all(isinstance(a, Wait) for a in anims):  # self.wait()
            self._hold(kwargs.get("run_time", max(a.run_time for a in anims)))
            return
        on_screen = {id(m) for m in self.get_mobject_family_members()}
        outs, morphs, ins, others = [], [], [], []
        order = []  # orden original: decide quién se dibuja encima / original order: decides what draws on top

        def put(kind, anim):
            kind.append(anim)
            order.append(anim)

        for a in anims:
            src = getattr(a, "mobject", None)
            if isinstance(a, FadeTransform) and _has_text(a.mobject[0]):
                put(outs, FadeOut(a.mobject[0]))  # fundido cruzado -> salir y entrar / cross-fade -> out, in
                put(ins, FadeIn(a.to_add_on_completion))
            elif isinstance(a, ReplacementTransform) and _has_text(src):
                put(outs, FadeOut(src))
                put(ins, FadeIn(a.target_mobject))
            elif isinstance(a, (MoveToTarget, ApplyMethod, ApplyFunction)):
                put(others, a)  # .animate: mueve o recolorea / moves or recolors
            elif getattr(a, "remover", False) and _has_text(src):
                put(outs, a)
            elif (isinstance(a, Transform) and not isinstance(a, _Fade) and a.target_mobject is not None
                  and _strings(src) != _strings(a.target_mobject)):
                put(morphs, a)  # Transform que cambia un texto (no Indicate) / changes a text (not Indicate)
            elif src is not None and any(id(t) not in on_screen for t in _text_leaves(src)):
                put(ins, a)
            else:
                put(others, a)
        touches = bool(outs or morphs or ins)
        # Un paso que solo añade, cambia o quita etiquetas (cifras, nombres cortos) se lee junto con el
        # subtítulo en pantalla: no espera a que termine, solo prolonga la lectura pendiente si hace falta.
        # A step that only adds, changes or removes labels (numbers, short names) is read alongside the
        # caption on screen: it does not wait for it, it only extends the pending reading time if needed.
        touched = [leaf for a in outs for leaf in _text_leaves(a.mobject)]
        touched += [leaf for a in morphs for m in (a.mobject, a.target_mobject) for leaf in _text_leaves(m)]
        touched += [leaf for a in ins for leaf in _text_leaves(a.mobject) if id(leaf) not in on_screen]
        only_labels = bool(touched) and all(text_words(leaf) <= LABEL_WORDS for leaf in touched)
        if touches and not only_labels:
            self._hold(self._debt)  # termina de leer el texto anterior / finish reading the previous text
        run_time = (kwargs.pop("run_time", None) or max(a.run_time for a in anims)) * SPEED
        if touches:
            run_time = max(run_time, MIN_TEXT_RUN_TIME)
        if (outs or morphs) and ins:  # primero sale, luego entra / out first, then in
            phases = [[a for a in order if a in outs or a in morphs], [a for a in order if a in ins or a in others]]
        else:
            phases = [order]
        words = {}  # texto -> palabras: un texto repetido se lee una vez / repeated text is read once
        for phase in phases:
            new = []
            for a in phase:
                if a in outs:
                    for leaf in _text_leaves(a.mobject):
                        self._hide(leaf)
                elif a in morphs:
                    src_leaves = list(_text_leaves(a.mobject))
                    for leaf in src_leaves:
                        self._hide(leaf)
                    tgt_leaves = list(_text_leaves(a.target_mobject))
                    keys = [id(s) for s in src_leaves] + [None] * len(tgt_leaves)
                    new += list(zip(tgt_leaves, keys))
                elif a in ins:
                    new += [(leaf, None) for leaf in _text_leaves(a.mobject) if id(leaf) not in on_screen]
            Scene.play(self, *phase, run_time=run_time, **kwargs)
            self._clock += run_time
            self._debt -= run_time
            for leaf, key in new:
                self._show(leaf, key)
                words[_string(leaf)] = text_words(leaf)
        self._idle = 0.0
        if any(words.values()):
            need = step_reading_time(list(words.values()))
            self._debt = max(self._debt, need) if only_labels else need

    def tear_down(self):
        self._hold(max(self._debt, FINAL_HOLD - self._idle))
        log = os.environ.get("MLA_PACING_LOG")
        if log:
            import json
            for rec in self._records:
                if rec["t_out"] is None:
                    rec["t_out"] = round(self._clock, 3)
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"scene": type(self).__name__, "lang": LANG, "duration": round(self._clock, 3),
                                     "records": self._records}, ensure_ascii=False) + "\n")
        super().tear_down()
