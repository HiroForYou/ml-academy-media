"""
Videos cortos del tema 3.3 (MLOps y CI/CD). Short videos for topic 3.3.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/mlops-cicd/scenes.py --scene PipelineGate --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"pipeline-gate": "PipelineGate", "canary-rollback": "CanaryRollback", "genai-pipeline": "GenAIPipeline"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, DashedLine, Dot, FadeIn, FadeOut, Line, Rectangle, RoundedRectangle,
    Transform, VGroup, VMobject,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene, same_text  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, icon_node, icon_title, label, math, node, pct, pick,
    tex_num,
)

TEXT = pick({
    "es": {
        "title": "SageMaker Pipelines: la ConditionStep decide si el modelo se registra",
        "processing": "Processing",
        "quality": "QualityCheck",
        "training": "Training",
        "evaluation": "Evaluación",
        "condition": "ConditionStep",
        "register": "RegisterModel",
        "fail": "FailStep",
        "pending": "PendingManualApproval",
        "run1": "Ejecución 1: el entrenamiento termina en Completed…",
        "run1b": "…pero AUC = 0,79 < 0,82: FailStep, no se registra nada",
        "run2": "Ejecución 2: AUC = 0,86 ≥ 0,82: se registra para aprobación",
        "takeaway": "Completed solo dice que terminó; la ConditionStep dice si es bueno",
        "title_c": "Blue/green canary: una alarma de CloudWatch revierte el despliegue",
        "blue": "Flota actual (blue)",
        "green": "Flota nueva (green)",
        "c1": "UpdateEndpoint: el 10 % del tráfico va a la flota nueva",
        "c2": "Durante la espera, CloudWatch vigila ModelLatency",
        "c3": "La alarma salta: auto-rollback, el 100 % vuelve a blue",
        "alarm": "umbral de la alarma",
        "latency": "ModelLatency (green)",
        "takeaway_c": "Sin alarmas configuradas no hay nada que dispare el rollback",
        "note": "Ilustrativo",
    },
    "en": {
        "title": "SageMaker Pipelines: the ConditionStep decides whether the model is registered",
        "processing": "Processing",
        "quality": "QualityCheck",
        "training": "Training",
        "evaluation": "Evaluation",
        "condition": "ConditionStep",
        "register": "RegisterModel",
        "fail": "FailStep",
        "pending": "PendingManualApproval",
        "run1": "Run 1: training ends in Completed…",
        "run1b": "…but AUC = 0.79 < 0.82: FailStep, nothing is registered",
        "run2": "Run 2: AUC = 0.86 ≥ 0.82: registered for approval",
        "takeaway": "Completed only says it finished; the ConditionStep says whether it is good",
        "title_c": "Blue/green canary: a CloudWatch alarm rolls the deployment back",
        "blue": "Current fleet (blue)",
        "green": "New fleet (green)",
        "c1": "UpdateEndpoint: 10% of traffic goes to the new fleet",
        "c2": "During the wait, CloudWatch watches ModelLatency",
        "c3": "The alarm fires: auto-rollback, 100% returns to blue",
        "alarm": "alarm threshold",
        "latency": "ModelLatency (green)",
        "takeaway_c": "With no alarms configured, nothing can trigger the rollback",
        "note": "Illustrative",
    },
})


class Swap:
    """Cambia un texto por otro con un fundido (sin morphing de glifos). Cross-fades one text into another."""

    def __init__(self, first=None):
        self.cur = first

    def to(self, new):
        if self.cur is not None and same_text(self.cur, new):
            return []  # mismo texto: se queda / same text: keep it on screen
        anims = [FadeIn(new)] + ([FadeOut(self.cur)] if self.cur is not None else [])
        self.cur = new
        return anims


def caption(key, color=INK_SOFT, size=20):
    return label(TEXT[key], size, color, max_width=12.4).to_edge(DOWN, buff=0.6)


def reshare(old, new):
    """Barras con Transform y porcentajes con fundido. Bars transform, percentages cross-fade."""
    anims = [Transform(old[0], new[0]), Transform(old[1], new[1]), FadeOut(old[2]), FadeOut(old[3]),
             FadeIn(new[2]), FadeIn(new[3])]
    return anims, VGroup(old[0], old[1], new[2], new[3])


class PipelineGate(PacedScene):
    def construct(self):
        title = label(TEXT["title"], 23, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        keys = ["processing", "quality", "training", "evaluation", "condition"]
        steps = [node(TEXT[k], 1.85, 0.8, size=17, stroke=AMBER if k == "condition" else INK_SOFT)
                 .move_to([-5.6 + i * 2.25, 0.8, 0]) for i, k in enumerate(keys)]
        reg = icon_node("aws/sagemaker-model", TEXT["register"], "Model Registry", 2.5, 0.95, stroke=OK,
                        title_size=16, desc_size=13, icon_height=0.55).move_to([5.45, 2.1, 0])
        fail = node(TEXT["fail"], 2.5, 0.8, size=17, stroke=ACCENT).move_to([5.45, -0.5, 0])
        # Encabezado con el logo del servicio. Header with the service logo.
        header = icon_title("aws/sagemaker-ai", "SageMaker Pipelines", 17, icon_height=0.42)
        header.move_to([-5.6, 1.95, 0]).align_to(steps[0], LEFT)
        links = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, color=GRAY, stroke_width=3,
                               max_tip_length_to_length_ratio=0.35) for a, b in zip(steps, steps[1:])])
        cond = steps[-1]
        yes = Arrow(cond.get_top(), reg.get_left(), buff=0.06, color=GRAY, stroke_width=3)
        no = Arrow(cond.get_bottom(), fail.get_left(), buff=0.06, color=GRAY, stroke_width=3)
        rule = math(r"\mathrm{AUC} \geq " + tex_num(0.82, 2), 26, INK).next_to(cond, DOWN, buff=0.75).shift(LEFT * 0.2)
        self.play(FadeIn(title), FadeIn(header), *[FadeIn(s) for s in steps], FadeIn(reg), FadeIn(fail),
                  Create(links),
                  Create(yes), Create(no), FadeIn(rule), run_time=1.0)

        def run(auc, passed, caps):
            token = Dot(steps[0].get_left(), radius=0.12, color=INK)
            self.add(token)
            cap = Swap()
            self.play(*cap.to(caption(caps[0])), token.animate.move_to(steps[0].get_top() + UP * 0.25), run_time=0.3)
            for s in steps[1:4]:
                self.play(token.animate.move_to(s.get_top() + UP * 0.25), run_time=0.3)
            auc_lbl = math(r"\mathrm{AUC} = " + tex_num(auc, 2), 26, OK if passed else ACCENT)
            auc_lbl.next_to(steps[3], DOWN, buff=0.35)
            self.play(FadeIn(auc_lbl), run_time=0.3)
            self.play(token.animate.move_to(cond.get_top() + UP * 0.25), run_time=0.3)
            target = reg if passed else fail
            extra = []
            if len(caps) > 1:
                extra += cap.to(caption(caps[1], OK if passed else ACCENT))
            self.play(token.animate.move_to(target.get_right() + RIGHT * 0.25).set_color(OK if passed else ACCENT),
                      target[0].animate.set_stroke(width=5), *extra, run_time=0.5)
            return token, auc_lbl, cap, target

        token, auc_lbl, cap, target = run(0.79, False, ["run1", "run1b"])
        self.wait(0.6)
        self.play(FadeOut(token), FadeOut(auc_lbl), FadeOut(cap.cur), target[0].animate.set_stroke(width=2),
                  run_time=0.4)

        token, auc_lbl, cap, target = run(0.86, True, ["run2"])
        tag = label(TEXT["pending"], 15, AMBER, "BOLD").next_to(reg, UP, buff=0.12).shift(LEFT * 0.4)
        self.play(FadeIn(tag), run_time=0.4)
        self.wait(0.5)
        self.play(*cap.to(caption("takeaway", INK, 21)), run_time=0.5)
        self.wait(1.2)


class CanaryRollback(PacedScene):
    def construct(self):
        title = label(TEXT["title_c"], 23, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        blue = icon_node("aws/sagemaker-ai", TEXT["blue"], "endpoint", 3.6, 0.95, stroke=INK_SOFT, title_size=18,
                         desc_size=14, icon_height=0.55).move_to([-2.6, 1.6, 0])
        green = icon_node("aws/sagemaker-ai", TEXT["green"], "endpoint", 3.6, 0.95, stroke=OK, title_size=18,
                          desc_size=14, icon_height=0.55).move_to([2.6, 1.6, 0])

        # Barra de reparto del tráfico. Traffic split bar.
        bar_w, bar_y = 9.0, 0.3
        frame = Rectangle(width=bar_w, height=0.45, stroke_color=RULE, stroke_width=2).move_to([0, bar_y, 0])

        def split(share):
            b = Rectangle(width=bar_w * (1 - share) + 1e-3, height=0.45, stroke_width=0).set_fill(INK_SOFT, 1)
            g = Rectangle(width=bar_w * share + 1e-3, height=0.45, stroke_width=0).set_fill(OK, 1)
            b.move_to(frame.get_left(), aligned_edge=LEFT)
            g.move_to(frame.get_right(), aligned_edge=RIGHT)
            txt_b = label(pct(100 - share * 100, 0), 16, INK_SOFT).next_to(frame, LEFT, buff=0.2)
            txt_g = label(pct(share * 100, 0), 16, OK).next_to(frame, RIGHT, buff=0.2)
            return VGroup(b, g, txt_b, txt_g)

        bars = split(0.0)
        self.play(FadeIn(title), FadeIn(blue), FadeIn(green), FadeIn(frame), FadeIn(bars), run_time=0.7)

        cap = Swap()
        anims, bars = reshare(bars, split(0.10))
        self.play(*cap.to(caption("c1")), *anims, run_time=0.8)

        # Mini gráfico de latencia. Mini latency chart.
        ox, oy, w, h = -3.0, -2.4, 6.0, 1.7
        axes = VGroup(Line([ox, oy, 0], [ox + w, oy, 0], color=RULE), Line([ox, oy, 0], [ox, oy + h, 0], color=RULE))
        thr_y = oy + h * 0.6
        thr = DashedLine([ox, thr_y, 0], [ox + w, thr_y, 0], color=ACCENT, dash_length=0.1)
        thr_l = icon_title("aws/cloudwatch", TEXT["alarm"], 14, ACCENT, icon_height=0.32).next_to(thr, RIGHT, buff=0.12)
        lat_l = label(TEXT["latency"], 14, MUTED).next_to(axes, LEFT, buff=0.15).shift(UP * 0.4)
        vals = [0.30, 0.33, 0.31, 0.36, 0.42, 0.55, 0.68, 0.74]
        pts = [[ox + (i + 0.5) * w / len(vals), oy + v * h, 0] for i, v in enumerate(vals)]
        curve = VMobject(color=OK, stroke_width=3).set_points_as_corners(pts)
        self.play(*cap.to(caption("c2")), Create(axes), Create(thr), FadeIn(thr_l), FadeIn(lat_l),
                  run_time=0.6)
        self.play(Create(curve), run_time=1.6)
        self.play(curve.animate.set_color(ACCENT), green[0].animate.set_stroke(ACCENT, 4), run_time=0.3)

        anims, bars = reshare(bars, split(0.0))
        self.play(*cap.to(caption("c3", ACCENT)), *anims,
                  green.animate.set_opacity(0.3), blue[0].animate.set_stroke(OK, 4), run_time=0.9)
        self.wait(0.6)
        self.play(*cap.to(caption("takeaway_c", INK, 21)), run_time=0.5)
        note = label(TEXT["note"], 14, MUTED).to_corner(DOWN + RIGHT, buff=0.25)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(1.2)


GEN = pick({
    "es": {
        "title": "CI/CD de IA generativa",
        "prompt4": "Prompt v4",
        "prompt5": "Prompt v5",
        "tests": "Pruebas",
        "gate": "Puerta 92 %",
        "deploy": "Desplegar",
        "blocked": "Bloqueado",
        "prod3": "prod = v3",
        "prod5": "prod = v5",
        "docs": "Docs S3",
        "ingest": "Ingesta",
        "rageval": "Eval. RAG",
        "c1": "Prompt nuevo: versión y pruebas con dataset fijo",
        "c2": "85 % < 92 %: bloqueado, producción sigue en v3",
        "c3": "94 % supera el umbral: se despliega la versión nueva",
        "c4": "Documentos nuevos: ingesta y reevaluación RAG",
        "c5": "Prompts y datos pasan por la misma puerta",
    },
    "en": {
        "title": "CI/CD for generative AI",
        "prompt4": "Prompt v4",
        "prompt5": "Prompt v5",
        "tests": "Tests",
        "gate": "Gate 92%",
        "deploy": "Deploy",
        "blocked": "Blocked",
        "prod3": "prod = v3",
        "prod5": "prod = v5",
        "docs": "S3 docs",
        "ingest": "Ingestion",
        "rageval": "RAG eval",
        "c1": "New prompt: version and tests on a fixed dataset",
        "c2": "85% < 92%: blocked, production stays on v3",
        "c3": "94% clears the threshold: the new version is deployed",
        "c4": "New documents: ingestion and RAG re-evaluation",
        "c5": "Prompts and data go through the same gate",
    },
})


class GenAIPipeline(PacedScene):
    def construct(self):
        title = label(GEN["title"], 22, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.4)

        def box(key, x, y, stroke=INK_SOFT, w=2.3, icon_name=None):
            if icon_name:  # servicio con su logo / service with its logo
                return icon_node(icon_name, GEN[key], None, w, 0.95, stroke=stroke, fill="#ffffff", title_size=19,
                                 icon_height=0.5).move_to([x, y, 0])
            return node(GEN[key], w, 0.95, size=22, stroke=stroke).move_to([x, y, 0])

        a = box("prompt4", -5.4, 1.3, w=2.6, icon_name="aws/bedrock")
        b = box("tests", -2.45, 1.3, w=2.6, icon_name="aws/bedrock")
        gate = box("gate", 0.9, 1.3, stroke=AMBER, w=2.7)
        deploy = box("deploy", 4.0, 1.3)
        blocked = box("blocked", 4.0, -0.15, stroke=GRAY)
        docs = box("docs", -5.4, -1.95, w=2.6, icon_name="aws/s3")
        ingest = box("ingest", -2.45, -1.95, w=2.6, icon_name="aws/bedrock")
        rageval = box("rageval", 0.9, -1.95, w=2.7, icon_name="aws/bedrock")

        def arrow(p, q, **kw):
            return Arrow(p.get_right(), q.get_left(), buff=0.05, color=GRAY, stroke_width=3, tip_length=0.18,
                         max_tip_length_to_length_ratio=0.25, **kw)

        links = VGroup(arrow(a, b), arrow(b, gate), arrow(gate, deploy), arrow(gate, blocked),
                       arrow(docs, ingest), arrow(ingest, rageval))
        sep = DashedLine([-6.5, -0.95, 0], [6.5, -0.95, 0], color=RULE, dash_length=0.12)
        self.play(FadeIn(title), *[FadeIn(m) for m in (a, b, gate, deploy, blocked, docs, ingest, rageval)],
                  Create(links), Create(sep), run_time=1.0)

        def cap(key, color=INK_SOFT, size=21):
            return label(GEN[key], size, color, max_width=12.2).to_edge(DOWN, buff=0.6)

        # Ejecución 1: la versión v4 no pasa la puerta. Run 1: v4 does not clear the gate.
        c1 = cap("c1")
        token = Dot(a.get_left() + LEFT * 0.1, radius=0.12, color=INK)
        self.add(token)
        self.play(FadeIn(c1), token.animate.move_to(a.get_top() + UP * 0.25), run_time=0.4)
        self.play(token.animate.move_to(b.get_top() + UP * 0.25), run_time=0.4)
        self.play(token.animate.move_to(gate.get_top() + UP * 0.25), run_time=0.4)
        score = label(pct(85, 0), 26, ACCENT, "BOLD").next_to(gate, UP, buff=0.4)
        self.play(FadeIn(score), run_time=0.3)

        c2 = cap("c2", ACCENT)
        keep = label(GEN["prod3"], 19, MUTED).next_to(blocked, RIGHT, buff=0.15)
        self.play(FadeOut(c1), FadeIn(c2), token.animate.move_to(blocked.get_left() + LEFT * 0.0).set_color(ACCENT),
                  blocked[0].animate.set_stroke(ACCENT, 5), FadeIn(keep), run_time=0.4)

        # Ejecución 2: la v5 supera el umbral. Run 2: v5 clears the threshold.
        c3 = cap("c3", OK)
        a5 = box("prompt5", -5.4, 1.3, w=2.6, icon_name="aws/bedrock")
        self.play(FadeOut(c2), FadeIn(c3), FadeOut(token), FadeOut(score), FadeOut(keep),
                  blocked[0].animate.set_stroke(GRAY, 2), Transform(a, a5), run_time=0.4)
        token = Dot(a.get_left() + LEFT * 0.1, radius=0.12, color=INK)
        self.add(token)
        self.play(token.animate.move_to(a.get_top() + UP * 0.25), run_time=0.4)
        self.play(token.animate.move_to(b.get_top() + UP * 0.25), run_time=0.4)
        self.play(token.animate.move_to(gate.get_top() + UP * 0.25), run_time=0.4)
        score2 = label(pct(94, 0), 26, OK, "BOLD").next_to(gate, UP, buff=0.4)
        keep5 = label(GEN["prod5"], 19, OK, "BOLD").next_to(deploy, RIGHT, buff=0.15)
        self.play(FadeIn(score2), token.animate.move_to(deploy.get_left()).set_color(OK),
                  deploy[0].animate.set_stroke(OK, 5), FadeIn(keep5), run_time=0.6)

        # Carril de documentos: ingesta y reevaluación. Documents lane: ingestion and re-evaluation.
        c4 = cap("c4")
        self.play(FadeOut(c3), FadeIn(c4), FadeOut(token), run_time=0.4)
        dot = Dot(docs.get_left() + LEFT * 0.1, radius=0.12, color=AMBER)
        self.add(dot)
        self.play(dot.animate.move_to(docs.get_top() + UP * 0.25), run_time=0.4)
        self.play(dot.animate.move_to(ingest.get_top() + UP * 0.25), run_time=0.5)
        self.play(dot.animate.move_to(rageval.get_top() + UP * 0.25), rageval[0].animate.set_stroke(OK, 5),
                  run_time=0.5)

        self.play(FadeOut(c4), FadeIn(cap("c5", OK, 22)), run_time=0.4)
        self.wait(1.2)
