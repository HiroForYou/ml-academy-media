"""
Videos cortos del tema 2.1 (enfoques de modelado). Short videos for topic 2.1.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/modeling-approaches/scenes.py --scene RagHybridFilter --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"rag-hybrid-filter": "RagHybridFilter"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Indicate, RoundedRectangle, Scene, SurroundingRectangle,
    VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, label, node, pick  # noqa: E402

TEXT = pick({
    "es": {
        "title": "Bedrock Knowledge Bases: filtro de metadatos y búsqueda híbrida",
        "query": "«¿Cómo reinicio el PX-7731-B?»",
        "filter": "filtro: region = emea",
        "chunks": [
            ("emea", "Reinicio del PX-7713"),
            ("amer", "Garantía PX-7731-B"),
            ("emea", "PX-7731-B: reinicio en frío"),
            ("apac", "Reinicio del PX-7731-B"),
            ("emea", "Tabla de errores E-40"),
            ("amer", "Instalación PX-7731-B"),
        ],
        "step1": "1. El filtro deja solo los chunks de su región",
        "step2": "2. Solo semántica: un chunk parecido, pero de otro modelo",
        "step3": "3. Híbrida (vectores + texto): encuentra el código exacto",
        "fm": "FM · RetrieveAndGenerate",
        "answer": "Respuesta + cita: manual-px7731.pdf",
        "semantic": "semántica",
        "hybrid": "híbrida",
    },
    "en": {
        "title": "Bedrock Knowledge Bases: metadata filter and hybrid search",
        "query": "“How do I restart the PX-7731-B?”",
        "filter": "filter: region = emea",
        "chunks": [
            ("emea", "Restarting the PX-7713"),
            ("amer", "PX-7731-B warranty"),
            ("emea", "PX-7731-B: cold restart"),
            ("apac", "Restarting the PX-7731-B"),
            ("emea", "E-40 error table"),
            ("amer", "PX-7731-B installation"),
        ],
        "step1": "1. The filter keeps only chunks from the user's region",
        "step2": "2. Semantic only: a similar chunk, but for another model",
        "step3": "3. Hybrid (vectors + text): finds the exact code",
        "fm": "FM · RetrieveAndGenerate",
        "answer": "Answer + citation: manual-px7731.pdf",
        "semantic": "semantic",
        "hybrid": "hybrid",
    },
})


def chunk(region, text):
    box = RoundedRectangle(width=2.95, height=0.95, corner_radius=0.1, stroke_color=INK_SOFT, stroke_width=1.8)
    box.set_fill(SURFACE, opacity=1)
    tag = label(region, 14, MUTED, "BOLD").next_to(box.get_corner(UP + LEFT), DOWN + RIGHT, buff=0.1)
    txt = label(text, 18, INK, max_width=2.7).move_to(box.get_center() + DOWN * 0.13)
    return VGroup(box, tag, txt)


class RagHybridFilter(Scene):
    def construct(self):
        title = label(TEXT["title"], 24, INK, "BOLD", max_width=12.8).to_edge(UP, buff=0.35)
        query = node(TEXT["query"], 5.6, 0.8, stroke=INK, fill="#ffffff", size=21).move_to(LEFT * 3.2 + UP * 2.35)
        flt = label(TEXT["filter"], 18, AMBER, "BOLD").next_to(query, RIGHT, buff=0.35)
        self.play(FadeIn(title), FadeIn(query), run_time=0.7)

        cards = VGroup(*[chunk(r, s) for r, s in TEXT["chunks"]])
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).move_to(LEFT * 2.1 + UP * 0.1)
        self.play(FadeIn(cards, lag_ratio=0.08), run_time=0.8)

        step = label(TEXT["step1"], 21, INK_SOFT, max_width=8.8).move_to(LEFT * 2.1 + DOWN * 2.4)
        self.play(FadeIn(flt), FadeIn(step), run_time=0.5)
        other = [c for c, (r, _) in zip(cards, TEXT["chunks"]) if r != "emea"]
        keep = [c for c, (r, _) in zip(cards, TEXT["chunks"]) if r == "emea"]
        self.play(*[c.animate.set_opacity(0.15) for c in other],
                  *[c[0].animate.set_stroke(AMBER, width=2.5) for c in keep], run_time=0.7)
        self.wait(0.4)

        # Semántica sola: el chunk de otro modelo. Semantic only: the other model's chunk.
        step2 = label(TEXT["step2"], 21, ACCENT, max_width=8.8).move_to(step)
        sem_box = SurroundingRectangle(cards[0], color=ACCENT, buff=0.06, corner_radius=0.12, stroke_width=4)
        sem_tag = label(TEXT["semantic"], 15, ACCENT, "BOLD").next_to(sem_box, UP, buff=0.05).align_to(sem_box, RIGHT)
        self.play(FadeOut(step), FadeIn(step2), Create(sem_box), FadeIn(sem_tag), run_time=0.6)
        self.wait(0.6)

        # Híbrida: el código exacto. Hybrid: the exact code.
        step3 = label(TEXT["step3"], 21, OK, "BOLD", max_width=8.8).move_to(step)
        hyb_box = SurroundingRectangle(cards[2], color=OK, buff=0.06, corner_radius=0.12, stroke_width=4)
        hyb_tag = label(TEXT["hybrid"], 15, OK, "BOLD").next_to(hyb_box, UP, buff=0.05).align_to(hyb_box, RIGHT)
        self.play(FadeOut(step2), FadeIn(step3), FadeOut(sem_box), FadeOut(sem_tag), Create(hyb_box),
                  FadeIn(hyb_tag), run_time=0.6)
        self.play(Indicate(cards[2], color=OK, scale_factor=1.05), run_time=0.5)

        # Generación con cita. Generation with a citation.
        fm = node(TEXT["fm"], 3.3, 0.9, stroke=INK_SOFT, size=18).move_to(RIGHT * 4.95 + UP * 0.1)
        arr = Arrow(hyb_box.get_right(), fm.get_left(), buff=0.1, color=OK, stroke_width=3)
        self.play(FadeIn(fm), Create(arr), run_time=0.6)
        ans = node(TEXT["answer"], 4.4, 0.8, stroke=OK, fill="#ffffff", size=17).move_to(RIGHT * 4.6 + DOWN * 1.45)
        arr2 = Arrow(fm.get_bottom(), [fm.get_bottom()[0], ans.get_top()[1], 0], buff=0.1, color=OK, stroke_width=3)
        self.play(Create(arr2), FadeIn(ans), run_time=0.7)
        self.play(Indicate(ans, color=OK, scale_factor=1.04), run_time=0.5)
        self.wait(1.2)
