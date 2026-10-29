"""
Videos cortos del tema 1.3 (calidad de datos y sesgo). Short videos for topic 1.3.

    MLA_LANG=es manim -r 1280,720 --fps 30 scenes.py DQPipeline

Las fórmulas usan MathTex (requiere LaTeX, p. ej. MiKTeX o TeX Live).
Formulas use MathTex (requires LaTeX, e.g. MiKTeX or TeX Live).
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"dq-pipeline": "DQPipeline", "stratified-split": "StratifiedSplit", "smote": "Smote"}

import os  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    Indicate,
    Line,
    MathTex,
    MoveAlongPath,
    RoundedRectangle,
    Square,
    Text,
    VGroup,
    Write,
    config,
)

config.background_color = WHITE

# Nodos con logo compartidos. Shared logo nodes.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene, icon_node, icon_title, pulse  # noqa: E402

INK = "#111114"
INK_SOFT = "#3d3d45"
MUTED = "#6a6a74"
SURFACE = "#f3f3f5"
RULE = "#e2e2e6"
ACCENT = "#b3132b"
OK = "#1f7a4d"
GRAY = "#c9c9cf"

LANG = os.environ.get("MLA_LANG", "es")
# Familia genérica de Pango: usa la sans del sistema en cualquier SO. Generic Pango family: system sans on any OS.
FONT = os.environ.get("MLA_FONT", "Sans")

TEXT = {
    "es": {
        "s3": "S3 · datos crudos",
        "etl": "Trabajo Glue ETL",
        "dq": "Evaluate Data Quality",
        "train": "Zona de entrenamiento",
        "stop": "Trabajo detenido",
        "alarm": "Alarma de CloudWatch",
        "batch_ok": "Carga 1: todas las reglas pasan",
        "batch_bad": "Carga 2: IDs duplicados",
        "sorted": "Archivo ordenado por etiqueta",
        "naive": "Últimas 20 % filas como prueba",
        "train_lbl": "Entrenamiento",
        "test_lbl": "Prueba",
        "pos": "positivos",
        "shuffle": "Mezclar + dividir estratificado",
        "both": "≈ 8,6 % de positivos en ambos",
        "bad_split": "El entrenamiento no tiene positivos",
        "smote_title": "SMOTE: ejemplos sintéticos de la clase minoritaria",
        "formula": r"x_{\text{nuevo}} = x_i + \lambda\,(x_{\text{vecino}} - x_i),\quad \lambda \in [0, 1]",
        "xn": r"x_{\text{vecino}}",
        "xnew": r"x_{\text{nuevo}}",
        "only_train": "Solo sobre el conjunto de entrenamiento",
        "minority": "minoritaria",
        "synthetic": "sintético",
    },
    "en": {
        "s3": "S3 · raw data",
        "etl": "Glue ETL job",
        "dq": "Evaluate Data Quality",
        "train": "Training zone",
        "stop": "Job stopped",
        "alarm": "CloudWatch alarm",
        "batch_ok": "Load 1: every rule passes",
        "batch_bad": "Load 2: duplicate IDs",
        "sorted": "File sorted by label",
        "naive": "Last 20% of rows as test",
        "train_lbl": "Training",
        "test_lbl": "Test",
        "pos": "positive",
        "shuffle": "Shuffle + stratified split",
        "both": "≈ 8.6% positives in both",
        "bad_split": "Training has no positives",
        "smote_title": "SMOTE: synthetic minority-class samples",
        "formula": r"x_{\text{new}} = x_i + \lambda\,(x_{\text{neighbor}} - x_i),\quad \lambda \in [0, 1]",
        "xn": r"x_{\text{neighbor}}",
        "xnew": r"x_{\text{new}}",
        "only_train": "Training split only",
        "minority": "minority",
        "synthetic": "synthetic",
    },
}[LANG]


def label(text, size=24, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def math(tex, size=30, color=INK):
    return MathTex(tex, font_size=size, color=color)


def node(text, width=3.0, height=1.0, stroke=INK_SOFT, fill=SURFACE):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=stroke, stroke_width=2)
    box.set_fill(fill, opacity=1)
    txt = label(text, 22)
    if txt.width > width - 0.3:
        txt.scale_to_fit_width(width - 0.3)
    return VGroup(box, txt.move_to(box))


def pct(value):
    s = f"{value:.1f}"
    return (s.replace(".", ",") + " %") if LANG == "es" else s + "%"


class DQPipeline(PacedScene):
    def construct(self):
        s3 = icon_node("aws/s3", TEXT["s3"], None, 2.9, 1.0, stroke=INK_SOFT, title_size=18,
                       icon_height=0.55).move_to(LEFT * 5.05 + UP * 0.6)
        etl = icon_node("aws/glue", TEXT["etl"], None, 2.9, 1.0, stroke=INK_SOFT, title_size=18,
                        icon_height=0.55).move_to(LEFT * 1.4 + UP * 0.6)
        dq_box = RoundedRectangle(width=3.4, height=2.3, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        dq_box.set_fill(SURFACE, opacity=1)
        dq_t = icon_title("aws/glue-data-quality", TEXT["dq"], 18, icon_height=0.42, max_width=3.15)
        dq = VGroup(dq_box, dq_t.next_to(dq_box.get_top(), DOWN, buff=0.16)).move_to(RIGHT * 2.65 + UP * 0.6)

        rules = ['IsComplete "id"', 'IsUnique "id"', 'ColumnValues "age"']
        rule_rows = VGroup()
        for i, r in enumerate(rules):
            rule = label(r, 17, INK_SOFT).move_to(dq[0].get_center() + UP * 0.12 + DOWN * 0.42 * i)
            rule.align_to(dq[0], LEFT).shift(RIGHT * 0.25)
            rule_rows.add(VGroup(rule))

        train = icon_node("aws/s3", TEXT["train"], None, 3.0, 0.85, stroke=OK, title_size=17,
                          icon_height=0.5).move_to(RIGHT * 5.4 + UP * 2.85)
        stop = icon_node("aws/glue", TEXT["stop"], None, 3.0, 0.85, stroke=ACCENT, title_size=17,
                         icon_height=0.5).move_to(RIGHT * 5.4 + DOWN * 1.85)
        alarm = icon_title("aws/cloudwatch", TEXT["alarm"], 17, ACCENT, icon_height=0.36).next_to(stop, DOWN, buff=0.15)

        arrows = VGroup(
            Arrow(s3.get_right(), etl.get_left(), buff=0.1, color=MUTED, stroke_width=3),
            Arrow(etl.get_right(), dq.get_left(), buff=0.1, color=MUTED, stroke_width=3),
        )
        up_arrow = Arrow(dq.get_top() + RIGHT * 0.9, train.get_bottom(), buff=0.1, color=OK, stroke_width=3)
        down_arrow = Arrow(dq.get_bottom() + RIGHT * 0.9, stop.get_top(), buff=0.1, color=ACCENT, stroke_width=3)

        self.play(FadeIn(s3), FadeIn(etl), FadeIn(dq), Create(arrows), run_time=0.8)
        self.play(*[FadeIn(r[0]) for r in rule_rows], FadeIn(train), FadeIn(stop), run_time=0.6)

        caption = label(TEXT["batch_ok"], 24, OK).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(caption), run_time=0.3)
        self._run_batch(s3, etl, dq, rule_rows, [True, True, True], up_arrow, train, OK)

        caption2 = label(TEXT["batch_bad"], 24, ACCENT).to_edge(DOWN, buff=0.45)
        self.play(FadeOut(caption), FadeIn(caption2), run_time=0.3)
        self._run_batch(s3, etl, dq, rule_rows, [True, False, True], down_arrow, stop, ACCENT)
        self.play(FadeIn(alarm), stop.box.animate.set_fill("#fbeef0", 1).set_stroke(ACCENT, 4),
                  Flash(stop, color=ACCENT, line_length=0.3, flash_radius=1.7), run_time=0.8)
        self.wait(1.2)

    def _run_batch(self, s3, etl, dq, rule_rows, results, out_arrow, target, color):
        dot = Dot(s3.get_center(), radius=0.13, color=color)
        path = Line(s3.get_center(), dq.get_center())
        self.play(FadeIn(dot, scale=0.5), run_time=0.2)
        self.play(MoveAlongPath(dot, path), run_time=0.9)
        marks = VGroup()
        mark_x = dq[0].get_right()[0] - 0.22
        for row, ok in zip(rule_rows, results):
            mark = label("PASS" if ok else "FAIL", 16, OK if ok else ACCENT, "BOLD")
            mark.move_to([mark_x, row[0].get_center()[1], 0], aligned_edge=RIGHT)
            marks.add(mark)
            self.play(FadeIn(mark), run_time=0.22)
        self.play(Create(out_arrow), run_time=0.35)
        self.play(MoveAlongPath(dot, Line(dq.get_center(), out_arrow.get_end())), run_time=0.55)
        self.play(FadeOut(dot), pulse(target, color), run_time=0.6)
        if all(results):
            self.play(FadeOut(marks), FadeOut(out_arrow), run_time=0.3)


class StratifiedSplit(PacedScene):
    N = 58
    POS = 5  # 5/58 ≈ 8.6 %

    def cells(self, labels):
        group = VGroup()
        for y in labels:
            sq = Square(side_length=0.18, stroke_width=0)
            sq.set_fill(ACCENT if y else GRAY, opacity=1)
            group.add(sq)
        group.arrange(RIGHT, buff=0.03)
        return group

    def construct(self):
        labels = [0] * (self.N - self.POS) + [1] * self.POS
        strip = self.cells(labels).move_to(UP * 1.2)
        title = label(TEXT["sorted"], 26).to_edge(UP, buff=0.6)
        self.play(FadeIn(title), FadeIn(strip, lag_ratio=0.02), run_time=1.0)

        cut = int(self.N * 0.8)
        cut_x = (strip[cut - 1].get_right()[0] + strip[cut].get_left()[0]) / 2
        cut_line = Line([cut_x, 1.6, 0], [cut_x, 0.8, 0], color=INK, stroke_width=3)
        naive = label(TEXT["naive"], 22, INK_SOFT).next_to(strip, DOWN, buff=0.55)
        self.play(Create(cut_line), FadeIn(naive), run_time=0.6)

        tr_pos = sum(labels[:cut]) / cut * 100
        te_pos = sum(labels[cut:]) / (self.N - cut) * 100
        tr_lbl = label(f"{TEXT['train_lbl']}: {pct(tr_pos)} {TEXT['pos']}", 20, ACCENT)
        te_lbl = label(f"{TEXT['test_lbl']}: {pct(te_pos)} {TEXT['pos']}", 20, ACCENT)
        tr_lbl.move_to([strip[: cut].get_center()[0], 0.35, 0])
        te_lbl.move_to([strip[cut:].get_center()[0] + 0.4, 0.35, 0])
        for lbl in (tr_lbl, te_lbl):
            if lbl.get_right()[0] > 6.8:
                lbl.shift(LEFT * (lbl.get_right()[0] - 6.8))
        warn = label(TEXT["bad_split"], 24, ACCENT, "BOLD").move_to(DOWN * 0.9)
        self.play(FadeOut(naive), FadeIn(tr_lbl), FadeIn(te_lbl), run_time=0.5)
        self.play(FadeIn(warn), run_time=0.4)
        self.wait(1.0)

        # Mezclar y dividir estratificado: 4 positivos en train, 1 en test.
        rng = np.random.default_rng(3)
        pos_idx = [i for i, y in enumerate(labels) if y]
        neg_idx = [i for i, y in enumerate(labels) if not y]
        rng.shuffle(pos_idx)
        rng.shuffle(neg_idx)
        test_idx = pos_idx[:1] + neg_idx[: (self.N - cut) - 1]
        train_idx = pos_idx[1:] + neg_idx[(self.N - cut) - 1 :]
        rng.shuffle(train_idx)
        rng.shuffle(test_idx)

        new_title = label(TEXT["shuffle"], 26).to_edge(UP, buff=0.6)
        self.play(
            FadeOut(cut_line), FadeOut(tr_lbl), FadeOut(te_lbl), FadeOut(warn),
            FadeOut(title), FadeIn(new_title), run_time=0.5,
        )
        target = self.cells([labels[i] for i in train_idx + test_idx]).move_to(UP * 1.2)
        target[: len(train_idx)].shift(LEFT * 0.35)
        target[len(train_idx) :].shift(RIGHT * 0.35)
        order = train_idx + test_idx
        self.play(*[strip[i].animate.move_to(target[k]) for k, i in enumerate(order)], run_time=1.6)

        tr = sum(labels[i] for i in train_idx) / len(train_idx) * 100
        te = sum(labels[i] for i in test_idx) / len(test_idx) * 100
        tr_lbl2 = label(f"{TEXT['train_lbl']}: {pct(tr)}", 20, OK).move_to([target[: len(train_idx)].get_center()[0], 0.35, 0])
        te_lbl2 = label(f"{TEXT['test_lbl']}: {pct(te)}", 20, OK).move_to([target[len(train_idx) :].get_center()[0], 0.35, 0])
        both = label(TEXT["both"], 24, OK, "BOLD").move_to(DOWN * 0.9)
        self.play(FadeIn(tr_lbl2), FadeIn(te_lbl2), run_time=0.5)
        self.play(FadeIn(both), run_time=0.4)
        self.wait(1.4)


class Smote(PacedScene):
    def construct(self):
        rng = np.random.default_rng(11)
        title = label(TEXT["smote_title"], 26).to_edge(UP, buff=0.5)

        majority = VGroup(
            *[Dot([x, y, 0], radius=0.06, color=GRAY) for x, y in zip(rng.uniform(-6, 2, 70), rng.uniform(-2.2, 2.2, 70))]
        )
        minority_pts = np.array([[2.8, 1.2], [3.6, 0.4], [4.4, 1.5], [3.2, -0.8], [4.8, -0.3], [5.4, 0.9]])
        minority = VGroup(*[Dot([x, y, 0], radius=0.1, color=ACCENT) for x, y in minority_pts])
        legend = VGroup(
            VGroup(Dot(radius=0.1, color=ACCENT), label(TEXT["minority"], 18, INK_SOFT)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.1, color=OK), label(TEXT["synthetic"], 18, INK_SOFT)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).to_corner(UP + RIGHT, buff=0.5).shift(DOWN * 0.8)

        self.play(FadeIn(title), FadeIn(majority, lag_ratio=0.01), FadeIn(minority), FadeIn(legend), run_time=1.0)

        formula = math(TEXT["formula"], 34, INK_SOFT).to_edge(DOWN, buff=1.0)
        self.play(Write(formula), run_time=0.8)

        pairs = [(0, 1, 0.45), (2, 5, 0.6), (3, 4, 0.35), (1, 4, 0.5)]
        synthetic = VGroup()
        for k, (i, j, lam) in enumerate(pairs):
            a, b = minority[i], minority[j]
            seg = Line(a.get_center(), b.get_center(), color=MUTED, stroke_width=2)
            self.play(Indicate(a, color=ACCENT, scale_factor=1.6), Create(seg), run_time=0.45)
            new = Dot(a.get_center() + lam * (b.get_center() - a.get_center()), radius=0.1, color=OK)
            if k == 0:
                # Primera pareja: etiquetas en LaTeX. First pair: LaTeX labels.
                tags = VGroup(
                    math("x_i", 28, ACCENT).next_to(a, UP + LEFT, buff=0.08),
                    math(TEXT["xn"], 28, ACCENT).next_to(b, DOWN + RIGHT, buff=0.08),
                    math(TEXT["xnew"], 28, OK).next_to(new, RIGHT, buff=0.15),
                )
                self.play(FadeIn(new, scale=0.3), FadeIn(tags), run_time=0.5)
                self.wait(0.8)
                self.play(FadeOut(seg), FadeOut(tags), run_time=0.3)
            else:
                self.play(FadeIn(new, scale=0.3), run_time=0.35)
                self.play(FadeOut(seg), run_time=0.2)
            synthetic.add(new)

        note = label(TEXT["only_train"], 24, ACCENT, "BOLD").to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.4)
