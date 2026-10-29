"""
Videos cortos del tema 2.3 (evaluar el rendimiento). Short videos for topic 2.3.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/model-evaluation/scenes.py --scene ShadowTest --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"shadow-test": "ShadowTest"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, Line, MoveAlongPath, Rectangle,
    RoundedRectangle, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, icon_node, icon_title, label, node, pick,
)

TEXT = pick({
    "es": {
        "title": "Shadow test: el candidato recibe tráfico real, pero no responde al usuario",
        "client": "Clientes",
        "endpoint": "Endpoint de SageMaker AI",
        "prod": "Variante de producción",
        "prod_sub": "responde al 100 %",
        "shadow": "Variante shadow",
        "shadow_sub": "copia del 20 % (traffic sampling)",
        "log": "respuestas registradas,\nno enviadas",
        "panel": "Panel del shadow test (7 días)",
        "latency": "ModelLatency p50",
        "errors": "Invocation5XXErrors",
        "prod_s": "producción",
        "shadow_s": "shadow",
        "deploy": "Deploy shadow variant → el candidato pasa a producción",
        "note": "Valores ilustrativos",
    },
    "en": {
        "title": "Shadow test: the candidate gets real traffic but never answers the user",
        "client": "Clients",
        "endpoint": "SageMaker AI endpoint",
        "prod": "Production variant",
        "prod_sub": "answers 100%",
        "shadow": "Shadow variant",
        "shadow_sub": "20% copy (traffic sampling)",
        "log": "responses logged,\nnot returned",
        "panel": "Shadow test dashboard (7 days)",
        "latency": "ModelLatency p50",
        "errors": "Invocation5XXErrors",
        "prod_s": "production",
        "shadow_s": "shadow",
        "deploy": "Deploy shadow variant → the candidate becomes production",
        "note": "Illustrative values",
    },
})


class ShadowTest(PacedScene):
    def construct(self):
        title = label(TEXT["title"], 23, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        client = icon_node("aws/users", TEXT["client"], None, 2.2, 1.0, stroke=INK_SOFT, title_size=19,
                           icon_height=0.55).move_to(LEFT * 5.6 + UP * 0.6)

        ep = RoundedRectangle(width=5.6, height=3.6, corner_radius=0.14, stroke_color=INK_SOFT, stroke_width=2)
        ep.set_fill("#ffffff", opacity=1).move_to(LEFT * 0.6 + UP * 0.35)
        ep_t = icon_title("aws/sagemaker-ai", TEXT["endpoint"], 17, color=INK_SOFT, icon_height=0.38).next_to(
            ep.get_top(), DOWN, buff=0.12)
        prod = icon_node("aws/sagemaker-model", TEXT["prod"], None, 3.6, 0.85, stroke=OK, title_size=17,
                         icon_height=0.55).move_to(ep.get_center() + UP * 0.65 + RIGHT * 0.6)
        prod_s = label(TEXT["prod_sub"], 14, OK).next_to(prod, DOWN, buff=0.06)
        shadow = icon_node("aws/sagemaker-shadow-testing", TEXT["shadow"], None, 3.6, 0.85, stroke=AMBER,
                           title_size=17, icon_height=0.55).move_to(ep.get_center() + DOWN * 0.95 + RIGHT * 0.6)
        shadow_s = label(TEXT["shadow_sub"], 14, INK_SOFT).next_to(shadow, DOWN, buff=0.06)
        router = Dot(ep.get_left() + RIGHT * 0.55, radius=0.09, color=INK_SOFT)

        log = icon_node("aws/logs", TEXT["log"].split("\n")[0], TEXT["log"].split("\n")[1], 3.0, 1.1, stroke=GRAY,
                        title_size=13, desc_size=13, title_color=MUTED, desc_color=MUTED, icon_height=0.5)
        log.move_to(RIGHT * 5.15 + DOWN * 0.6)
        log_t = VGroup()

        wires = VGroup(
            Line(client.get_right(), router.get_center(), color=GRAY, stroke_width=3),
            Line(router.get_center(), prod.get_left(), color=GRAY, stroke_width=3),
            Line(router.get_center(), shadow.get_left(), color=GRAY, stroke_width=3),
            Arrow(shadow.get_right(), log.get_left(), buff=0.08, color=GRAY, stroke_width=3),
        )
        self.play(FadeIn(title), FadeIn(client), FadeIn(ep), FadeIn(ep_t), run_time=0.6)
        self.play(FadeIn(prod), FadeIn(prod_s), FadeIn(shadow), FadeIn(shadow_s), FadeIn(router), Create(wires),
                  FadeIn(log), FadeIn(log_t), run_time=0.8)

        # Cinco solicitudes; una de cada cinco se copia a shadow. Five requests; one in five is copied to shadow.
        for i in range(5):
            req = Dot(client.get_right(), radius=0.08, color=INK)
            path_in = Line(client.get_right(), router.get_center())
            self.play(MoveAlongPath(req, path_in), run_time=0.25)
            anims = [req.animate.move_to(prod.get_left())]
            copy = None
            if i == 2:
                copy = Dot(router.get_center(), radius=0.08, color=AMBER)
                anims.append(copy.animate.move_to(shadow.get_left()))
            self.play(*anims, run_time=0.25)
            resp = Dot(prod.get_left(), radius=0.08, color=OK)
            self.remove(req)
            back = [MoveAlongPath(resp, Line(prod.get_left(), client.get_right()))]
            if copy is not None:
                back.append(copy.animate.move_to(log.get_center()).set_opacity(0.3))
            self.play(*back, run_time=0.35)
            self.remove(resp)
            if copy is not None:
                self.remove(copy)
        self.play(client[0].animate.set_stroke(OK, 4), run_time=0.4)

        # Panel de comparación. Comparison dashboard.
        scene = VGroup(client, ep, ep_t, prod, prod_s, shadow, shadow_s, router, wires, log, log_t)
        self.play(scene.animate.scale(0.62).to_edge(LEFT, buff=0.4).shift(UP * 0.4), run_time=0.6)
        px = 3.5
        panel_t = label(TEXT["panel"], 18, INK, "BOLD").move_to([px, 1.9, 0])
        rows = VGroup()
        metrics = [(TEXT["latency"], (42, 38), ("42 ms", "38 ms"), 50), (TEXT["errors"], (3, 2), ("3", "2"), 5)]
        for r, (name, vals, txts, scale) in enumerate(metrics):
            y = 1.1 - r * 1.55
            rows.add(label(name, 16, INK_SOFT).move_to([px, y, 0]))
            for k, (v, txt, col, who) in enumerate(zip(vals, txts, (OK, AMBER), (TEXT["prod_s"], TEXT["shadow_s"]))):
                yy = y - 0.45 - k * 0.42
                w = 2.6 * v / scale
                bar = Rectangle(width=w, height=0.28, stroke_width=0).set_fill(col, 1)
                bar.move_to([px - 0.9, yy, 0], aligned_edge=LEFT)
                rows.add(label(who, 13, MUTED).next_to(bar, LEFT, buff=0.12))
                rows.add(bar, label(txt, 13, INK).next_to(bar, RIGHT, buff=0.1))
        self.play(FadeIn(panel_t), FadeIn(rows), run_time=0.8)
        self.wait(0.6)

        deploy = label(TEXT["deploy"], 21, OK, "BOLD", max_width=12.4).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(deploy), shadow[0].animate.set_stroke(OK), prod[0].animate.set_stroke(GRAY),
                  run_time=0.6)
        note = label(TEXT["note"], 15, MUTED).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(1.2)
