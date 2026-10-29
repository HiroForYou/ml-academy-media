"""
Videos cortos del tema 2.2 (entrenamiento y ajuste). Short videos for topic 2.2.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/training-customization/scenes.py --scene Hyperband --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"hyperband": "Hyperband", "regularization": "Regularization"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Create, DashedLine, DoubleArrow, FadeIn, FadeOut, Line, Rectangle, Transform,
    VGroup, VMobject,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene, ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, label, num, pick  # noqa: E402

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


class Hyperband(PacedScene):
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
            anims = [FadeIn(new_caption)] + ([FadeOut(caption)] if rung else [])
            grow = []
            for i in alive:
                target = Rectangle(width=epochs * unit, height=row_h * 0.62, stroke_width=0).set_fill(AMBER, 1)
                target.move_to([x0, top - (i + 0.5) * row_h, 0], aligned_edge=LEFT)
                grow.append(bars[i].animate.become(target))
                if i in values:
                    grow.append(FadeOut(values.pop(i)))
            self.play(*anims, *grow, run_time=0.9)
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
            self.beat(1.8)  # pausa para ver qué configuraciones siguen / pause to see which configurations continue

        note = label(TEXT["note"], 17, MUTED, max_width=12).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.2)


REG = pick({
    "es": {
        "title": "Regularización y brecha de generalización",
        "train": "entrenamiento",
        "val": "validación",
        "epoch": "época",
        "loss": "error",
        "gap": "brecha",
        "stop": "early stopping",
        "c1": "Sin regularizar, el entrenamiento mejora y la validación empeora",
        "c2": "L1 y L2 penalizan pesos extremos y estrechan la brecha",
        "c3": "Dropout apaga neuronas al azar y suaviza",
        "c4": "Early stopping corta en el mínimo de la validación",
        "c5": "Menos brecha, mejor generalización",
        "note": "Curvas sintéticas · ilustrativo",
    },
    "en": {
        "title": "Regularization and the generalization gap",
        "train": "training",
        "val": "validation",
        "epoch": "epoch",
        "loss": "loss",
        "gap": "gap",
        "stop": "early stopping",
        "c1": "Unregularized, training improves while validation gets worse",
        "c2": "L1 and L2 penalize extreme weights: the gap narrows",
        "c3": "Dropout switches off neurons and smooths the curve",
        "c4": "Early stopping cuts at the validation minimum",
        "c5": "Smaller gap, better generalization",
        "note": "Synthetic curves · illustrative",
    },
})


class Regularization(PacedScene):
    X0, X1 = -5.2, 5.2     # x de la época 0 y 40 / x of epoch 0 and 40
    Y0, Y1 = -1.9, 1.5     # y de error 0 y 1 / y of loss 0 and 1
    STOP = 20              # época de early stopping / early-stopping epoch

    def pt(self, e, v):
        return [self.X0 + (self.X1 - self.X0) * e / 40, self.Y0 + (self.Y1 - self.Y0) * v, 0]

    def curve(self, fn, color, upto=40):
        e = np.linspace(0, upto, 81)
        mob = VMobject(stroke_color=color, stroke_width=5)
        mob.set_points_smoothly([self.pt(x, fn(x)) for x in e])
        return mob

    @staticmethod
    def train(e, reg=False, noisy=False):
        v = (0.12 + 0.80 * np.exp(-e / 9)) if reg else (0.05 + 0.90 * np.exp(-e / 9))
        return v + (0.010 * np.sin(2.1 * e) if noisy else 0)

    @staticmethod
    def val(e, reg=False, noisy=False):
        v = (0.27 + 0.62 * np.exp(-e / 6) + 0.002 * max(e - 20, 0)) if reg else (
            0.30 + 0.60 * np.exp(-e / 6) + 0.011 * max(e - 12, 0))
        return v + (0.016 * np.sin(1.7 * e + 1) if noisy else 0)

    def gap(self, tr, va, color, epoch=40, dx=0.25):
        return DoubleArrow(self.pt(epoch, tr(epoch)), self.pt(epoch, va(epoch)), buff=0, color=color, stroke_width=4,
                           tip_length=0.15).shift(RIGHT * dx)

    def construct(self):
        T = self.train
        V = self.val
        title = label(REG["title"], 22, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.4)
        x_axis = Line(self.pt(0, 0), self.pt(40, 0), color=MUTED, stroke_width=2)
        y_axis = Line(self.pt(0, 0), self.pt(0, 1), color=MUTED, stroke_width=2)
        x_lbl = label(REG["epoch"], 16, MUTED).next_to(x_axis, DOWN, buff=0.12).align_to(x_axis, RIGHT)
        y_lbl = label(REG["loss"], 16, MUTED).next_to(y_axis, UP, buff=0.1)
        leg_t = VGroup(Line([0, 0, 0], [0.5, 0, 0], color=INK_SOFT, stroke_width=5),
                       label(REG["train"], 15, INK_SOFT)).arrange(RIGHT, buff=0.15)
        leg_v = VGroup(Line([0, 0, 0], [0.5, 0, 0], color=ACCENT, stroke_width=5),
                       label(REG["val"], 15, ACCENT)).arrange(RIGHT, buff=0.15)
        legend = VGroup(leg_t, leg_v).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.5, 0])
        self.play(FadeIn(title), FadeIn(x_axis), FadeIn(y_axis), FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(legend),
                  run_time=0.8)

        # 1. Sin regularizar: la validación sube mientras el entrenamiento baja. 1. Unregularized: validation rises.
        tr = self.curve(lambda e: T(e, noisy=True), INK_SOFT)
        va = self.curve(lambda e: V(e, noisy=True), ACCENT)
        cap = label(REG["c1"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(cap), Create(tr), Create(va), run_time=2.2)
        arrow = self.gap(lambda e: T(e, noisy=True), lambda e: V(e, noisy=True), ACCENT)
        gap_lbl = label(REG["gap"], 17, ACCENT, "BOLD").next_to(arrow, RIGHT, buff=0.12)
        self.play(FadeIn(arrow), FadeIn(gap_lbl), run_time=0.5)

        # 2. L1/L2: la brecha se estrecha. 2. L1/L2: the gap narrows.
        cap2 = label(REG["c2"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.7)
        tr2 = self.curve(lambda e: T(e, reg=True, noisy=True), INK_SOFT)
        va2 = self.curve(lambda e: V(e, reg=True, noisy=True), ACCENT)
        arrow2 = self.gap(lambda e: T(e, reg=True, noisy=True), lambda e: V(e, reg=True, noisy=True), ACCENT)
        gap_lbl2 = label(REG["gap"], 17, ACCENT, "BOLD").next_to(arrow2, RIGHT, buff=0.12)
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.4)
        self.play(Transform(tr, tr2), Transform(va, va2), Transform(arrow, arrow2), Transform(gap_lbl, gap_lbl2),
                  run_time=1.2)

        # 3. Dropout: la curva se suaviza. 3. Dropout: the curve smooths.
        cap3 = label(REG["c3"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.7)
        tr3 = self.curve(lambda e: T(e, reg=True), INK_SOFT)
        va3 = self.curve(lambda e: V(e, reg=True), ACCENT)
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.4)
        self.play(Transform(tr, tr3), Transform(va, va3), run_time=1.0)

        # 4. Early stopping: se corta en el mínimo de la validación. 4. Early stopping: cut at the validation minimum.
        cap4 = label(REG["c4"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.7)
        sx = self.pt(self.STOP, 0)[0]
        marker = DashedLine([sx, self.Y0, 0], [sx, self.Y1 + 0.1, 0], color=OK, stroke_width=4, dash_length=0.12)
        shade_top = self.pt(0, 0.5)[1]
        shade = Rectangle(width=self.X1 - sx + 0.05, height=shade_top - self.Y0 + 0.1, stroke_width=0)
        shade.set_fill("#ffffff", opacity=0.75).move_to([(sx + self.X1 + 0.05) / 2, (self.Y0 - 0.1 + shade_top) / 2, 0])
        stop_lbl = label(REG["stop"], 17, OK, "BOLD").next_to(marker, UP, buff=0.08)
        self.play(FadeOut(cap3), FadeIn(cap4), run_time=0.4)
        self.play(Create(marker), FadeIn(shade), FadeIn(stop_lbl), run_time=1.0)

        # 5. Resultado. 5. Result.
        cap5 = label(REG["c5"], 22, OK, "BOLD", max_width=12.2).to_edge(DOWN, buff=0.7)
        arrow5 = self.gap(lambda e: T(e, reg=True), lambda e: V(e, reg=True), OK, epoch=self.STOP, dx=-0.55)
        gap_lbl5 = label(REG["gap"], 17, OK, "BOLD").next_to(arrow5, DOWN, buff=0.1)
        self.play(FadeOut(cap4), FadeIn(cap5), run_time=0.4)
        self.play(Transform(arrow, arrow5), Transform(gap_lbl, gap_lbl5), run_time=0.9)
        self.wait(1.2)
