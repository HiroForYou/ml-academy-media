"""
Videos cortos del tema 1.2 (transformación y features). Short videos for topic 1.2.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/data-transformation-features/scenes.py --scene FitOnTrain --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"fit-on-train": "FitOnTrain"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Brace, Create, Cross, FadeIn, FadeOut, Indicate, RoundedRectangle, Scene,
    VGroup, Write,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import ACCENT, AMBER, INK, INK_SOFT, MUTED, OK, SURFACE, label, math, pick, tex_num  # noqa: E402

TEXT = pick({
    "es": {
        "title": "Escalar monthly_spend sin fuga",
        "wrong": "Mal: media y desviación con todo el dataset",
        "leak": "La prueba influye en el escalador: fuga",
        "right": "Bien: divide primero y ajusta solo con entrenamiento",
        "train": "entrenamiento",
        "val": "validación",
        "test": "prueba",
        "infer": "inferencia",
        "mu_all": r"\mu_{\text{todo}}",
        "mu_tr": r"\mu_{\text{train}}",
        "sigma_tr": r"\sigma_{\text{train}}",
        "apply": "Los mismos parámetros en validación, prueba e inferencia",
    },
    "en": {
        "title": "Scaling monthly_spend without leakage",
        "wrong": "Wrong: mean and std from the whole dataset",
        "leak": "The test set shapes the scaler: leakage",
        "right": "Right: split first, fit on training only",
        "train": "training",
        "val": "validation",
        "test": "test",
        "infer": "inference",
        "mu_all": r"\mu_{\text{all}}",
        "mu_tr": r"\mu_{\text{train}}",
        "sigma_tr": r"\sigma_{\text{train}}",
        "apply": "The same parameters for validation, test and inference",
    },
})

TRAIN = [42, 55, 38, 61, 47, 52]
VAL = [58, 45]
TEST = [90, 97]


def cell(value, stroke=INK_SOFT, fill=SURFACE):
    box = RoundedRectangle(width=0.95, height=0.7, corner_radius=0.08, stroke_color=stroke, stroke_width=2)
    box.set_fill(fill, opacity=1)
    return VGroup(box, label(str(value), 22, INK).move_to(box))


class FitOnTrain(Scene):
    def construct(self):
        title = label(TEXT["title"], 28, INK, "BOLD").to_edge(UP, buff=0.45)
        values = TRAIN + VAL + TEST
        cells = VGroup(*[cell(v) for v in values]).arrange(RIGHT, buff=0.12).move_to(UP * 1.4)
        self.play(FadeIn(title), FadeIn(cells, lag_ratio=0.08), run_time=1.0)

        # 1. Ajuste con todo el dataset. Fitting on the whole dataset.
        wrong = label(TEXT["wrong"], 22, ACCENT).move_to(DOWN * 0.35)
        brace_all = Brace(cells, DOWN, color=ACCENT, buff=0.12)
        mu_all = math(f"{TEXT['mu_all']} = {tex_num(np.mean(values))}", 34, ACCENT).next_to(brace_all, DOWN, buff=0.12)
        self.play(Create(brace_all), FadeIn(wrong), run_time=0.6)
        wrong.next_to(mu_all, DOWN, buff=0.3)
        self.play(Write(mu_all), wrong.animate.next_to(mu_all, DOWN, buff=0.3), run_time=0.6)
        test_cells = cells[len(TRAIN) + len(VAL):]
        leak = label(TEXT["leak"], 22, ACCENT, "BOLD").next_to(wrong, DOWN, buff=0.25)
        self.play(*[c[0].animate.set_stroke(ACCENT, width=4) for c in test_cells], FadeIn(leak), run_time=0.6)
        self.play(Indicate(test_cells, color=ACCENT, scale_factor=1.1), run_time=0.6)
        cross = Cross(VGroup(mu_all, wrong), stroke_color=ACCENT, stroke_width=5)
        self.play(Create(cross), run_time=0.4)
        self.wait(0.4)
        self.play(FadeOut(VGroup(brace_all, mu_all, wrong, leak, cross)),
                  *[c[0].animate.set_stroke(INK_SOFT, width=2) for c in test_cells], run_time=0.5)

        # 2. Dividir y ajustar con entrenamiento. Split, then fit on training.
        tr, va, te = cells[: len(TRAIN)], cells[len(TRAIN): len(TRAIN) + len(VAL)], test_cells
        self.play(tr.animate.shift(LEFT * 0.35), te.animate.shift(RIGHT * 0.35), run_time=0.5)
        for group, name, color in ((tr, TEXT["train"], OK), (va, TEXT["val"], AMBER), (te, TEXT["test"], MUTED)):
            group.tag = label(name, 17, color, "BOLD").next_to(group, UP, buff=0.15)
        self.play(*[c[0].animate.set_stroke(OK, width=3) for c in tr],
                  *[c[0].animate.set_stroke(AMBER, width=3) for c in va],
                  FadeIn(tr.tag), FadeIn(va.tag), FadeIn(te.tag), run_time=0.5)
        right = label(TEXT["right"], 22, OK).move_to(DOWN * 0.35)
        brace_tr = Brace(tr, DOWN, color=OK, buff=0.12)
        params = math(f"{TEXT['mu_tr']} = {tex_num(np.mean(TRAIN))}\\qquad{TEXT['sigma_tr']} = {tex_num(np.std(TRAIN))}",
                      32, OK).next_to(brace_tr, DOWN, buff=0.12)
        self.play(Create(brace_tr), Write(params), run_time=0.8)
        right.next_to(params, DOWN, buff=0.25).align_to(params, LEFT)
        self.play(FadeIn(right), run_time=0.4)

        formula = math(r"z = \dfrac{x - " + TEXT["mu_tr"] + "}{" + TEXT["sigma_tr"] + "}", 36, INK)
        formula.move_to(RIGHT * 3.6 + DOWN * 1.15)
        infer = cell("63", stroke=INK_SOFT, fill="#ffffff").move_to(RIGHT * 3.6 + DOWN * 3.0)
        infer_tag = label(TEXT["infer"], 17, INK_SOFT, "BOLD").next_to(infer, LEFT, buff=0.2)
        self.play(FadeIn(formula), FadeIn(infer), FadeIn(infer_tag), run_time=0.5)
        arrows = VGroup(
            Arrow(formula.get_top(), va.get_bottom(), buff=0.15, color=OK, stroke_width=3),
            Arrow(formula.get_top(), te.get_bottom(), buff=0.15, color=OK, stroke_width=3),
            Arrow(formula.get_bottom(), infer.get_top(), buff=0.12, color=OK, stroke_width=3),
        )
        self.play(Create(arrows), run_time=0.7)
        apply = label(TEXT["apply"], 22, OK, "BOLD", max_width=8.2).to_corner(DOWN + LEFT, buff=0.5)
        self.play(FadeIn(apply), Indicate(VGroup(va, te, infer), color=OK, scale_factor=1.06), run_time=0.7)
        self.wait(1.2)
