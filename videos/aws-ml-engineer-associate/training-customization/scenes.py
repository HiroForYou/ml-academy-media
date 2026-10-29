"""
Videos cortos del tema 2.2 (entrenamiento y ajuste). Short videos for topic 2.2.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/training-customization/scenes.py --scene Hyperband --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"hyperband": "Hyperband"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Create, DashedLine, FadeIn, FadeOut, Line, Rectangle, Scene, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, label, num, pick  # noqa: E402

TEXT = pick({
    "es": {
        "title": "Hyperband en AMT: más epochs para las configuraciones prometedoras",
        "epochs": "epochs",
        "config": "config",
        "r1": "Todas entrenan 1 epoch; se detienen las 6 peores",
        "r2": "Las 3 mejores siguen hasta 3 epochs; se detienen 2",
        "r3": "La mejor recibe el presupuesto completo: 9 epochs",
        "stopped": "detenido",
        "note": "Usa métricas por epoch · early stopping de AMT en OFF · ilustrativo",
    },
    "en": {
        "title": "Hyperband in AMT: more epochs for promising configurations",
        "epochs": "epochs",
        "config": "config",
        "r1": "All train 1 epoch; the 6 worst are stopped",
        "r2": "The top 3 continue to 3 epochs; 2 are stopped",
        "r3": "The best gets the full budget: 9 epochs",
        "stopped": "stopped",
        "note": "Uses per-epoch metrics · AMT early stopping OFF · illustrative",
    },
})

# AUC de validación por configuración tras 1, 3 y 9 epochs (ilustrativo).
# Validation AUC per configuration after 1, 3 and 9 epochs (illustrative).
AUC = [
    (0.71, None, None), (0.78, 0.82, None), (0.69, None, None),
    (0.80, 0.85, 0.88), (0.74, None, None), (0.66, None, None),
    (0.77, 0.80, None), (0.72, None, None), (0.70, None, None),
]


class Hyperband(Scene):
    def construct(self):
        title = label(TEXT["title"], 24, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        x0, unit, row_h = -4.2, 0.95, 0.5
        top = 2.3
        axis = Line([x0, top - 9 * row_h - 0.05, 0], [x0 + 9 * unit, top - 9 * row_h - 0.05, 0], color=RULE)
        ticks = VGroup()
        for e in (1, 3, 9):
            x = x0 + e * unit
            ticks.add(DashedLine([x, top + 0.25, 0], [x, top - 9 * row_h - 0.05, 0], color=GRAY, dash_length=0.08))
            ticks.add(label(str(e), 16, MUTED).move_to([x, top - 9 * row_h - 0.3, 0]))
        ep_lbl = label(TEXT["epochs"], 16, MUTED).move_to([x0 + 9 * unit + 0.6, top - 9 * row_h - 0.3, 0])
        names = VGroup(*[label(f"{TEXT['config']} {i + 1}", 16, INK_SOFT).move_to(
            [x0 - 0.75, top - (i + 0.5) * row_h, 0]) for i in range(9)])
        self.play(FadeIn(title), Create(axis), FadeIn(ticks), FadeIn(ep_lbl), FadeIn(names), run_time=0.8)

        bars = []
        for i in range(9):
            b = Rectangle(width=0.01, height=row_h * 0.62, stroke_width=0).set_fill(AMBER, 1)
            b.move_to([x0, top - (i + 0.5) * row_h, 0], aligned_edge=LEFT)
            bars.append(b)
        self.add(*bars)

        caption = label(TEXT["r1"], 21, INK_SOFT, max_width=12).to_edge(DOWN, buff=0.75)
        values = {}
        alive = list(range(9))
        for rung, (epochs, keep, text) in enumerate(((1, 3, "r1"), (3, 1, "r2"), (9, 1, "r3"))):
            new_caption = label(TEXT[text], 21, INK_SOFT, max_width=12).to_edge(DOWN, buff=0.75)
            anims = [FadeIn(new_caption)] if rung == 0 else [caption.animate.become(new_caption)]
            grow = []
            for i in alive:
                target = Rectangle(width=epochs * unit, height=row_h * 0.62, stroke_width=0).set_fill(AMBER, 1)
                target.move_to([x0, top - (i + 0.5) * row_h, 0], aligned_edge=LEFT)
                grow.append(bars[i].animate.become(target))
                if i in values:
                    grow.append(FadeOut(values.pop(i)))
            self.play(*anims, *grow, run_time=0.9)
            if rung == 0:
                caption = new_caption
            # Valor de la métrica al final del tramo. Metric value at the end of the rung.
            shows = []
            for i in alive:
                v = AUC[i][rung]
                if i in values:
                    self.remove(values[i])
                values[i] = label(num(v, 2), 15, INK).next_to(bars[i], RIGHT, buff=0.1)
                shows.append(FadeIn(values[i]))
            self.play(*shows, run_time=0.35)
            ranked = sorted(alive, key=lambda i: AUC[i][rung], reverse=True)
            if rung < 2:
                losers = ranked[keep:]
                stops = []
                for i in losers:
                    stops.append(bars[i].animate.set_fill(GRAY, 1))
                    stops.append(values[i].animate.set_color(MUTED))
                tags = [label(TEXT["stopped"], 13, ACCENT).next_to(values[i], RIGHT, buff=0.12) for i in losers]
                self.play(*stops, *[FadeIn(tg) for tg in tags], run_time=0.6)
                alive = ranked[:keep]
            else:
                self.play(bars[alive[0]].animate.set_fill(OK, 1), values[alive[0]].animate.set_color(OK),
                          run_time=0.5)
            self.wait(0.3)

        note = label(TEXT["note"], 17, MUTED, max_width=12).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.2)
