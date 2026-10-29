"""
Paleta y utilidades compartidas por las escenas de Manim de cada tema.
Palette and helpers shared by every topic's Manim scenes.

Cada videos/<course>/<topic>/scenes.py declara VIDEOS = {"nombre-publicado": "ClaseDeEscena"}
(un literal que scripts/render_all.py lee sin importar Manim) y elige sus textos con pick(TEXT).
Each scenes.py declares VIDEOS (a literal render_all.py reads without importing Manim) and picks
its on-screen text with pick(TEXT).
"""

import os

from manim import WHITE, MathTex, RoundedRectangle, Text, VGroup, config

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


def num(value, digits=1, suffix=""):
    s = f"{value:.{digits}f}"
    return (s.replace(".", ",") if LANG == "es" else s) + suffix


def pct(value, digits=1):
    return num(value, digits, " %" if LANG == "es" else "%")


def tex_num(value, digits=1):
    """Número para MathTex: la coma decimal va entre llaves para que no añada espacio.
    Number for MathTex: the decimal comma is braced so it adds no space."""
    return num(value, digits).replace(",", "{,}")
