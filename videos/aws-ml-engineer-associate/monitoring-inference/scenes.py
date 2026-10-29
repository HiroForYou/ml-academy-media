"""
Videos cortos del tema 4.1 (monitorear inferencia). Short videos for topic 4.1.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/monitoring-inference/scenes.py --scene AbTrafficShift --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"ab-traffic-shift": "AbTrafficShift", "label-delay": "LabelDelay"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, DashedLine, Dot, FadeIn, FadeOut, Line, MoveAlongPath,
    Rectangle, RoundedRectangle, Transform, VGroup, VMobject,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE, icon_node, icon_title, label, node, num, pick,
)

TEXT = pick({
    "es": {
        "ab_title": "A/B con production variants en un mismo endpoint",
        "clients": "Usuarios reales",
        "endpoint": "Endpoint de SageMaker",
        "current": "variante current",
        "candidate": "variante candidate",
        "weight": "peso",
        "p1": "Pesos 90/10: el 10 % de los usuarios recibe el modelo nuevo",
        "p2": "UpdateEndpointWeightsAndCapacities → 50/50",
        "p3": "→ 0/100: todo el tráfico al modelo nuevo",
        "no_redeploy": "Sin actualizar el endpoint · cada variante publica sus métricas en CloudWatch",
        "ld_title": "Qué señal está disponible y cuándo (etiquetas con 7 días de retraso)",
        "day": "día",
        "svc": "Métricas del servicio",
        "svc_sub": "errores, latencia, volumen",
        "drift": "Deriva de datos",
        "drift_sub": "captura vs. baseline",
        "quality": "Calidad del modelo",
        "quality_sub": "predicciones + etiquetas",
        "svc_ok": "minutos: el servicio funciona",
        "drift_alarm": "día 3: PSI alto en 2 features",
        "wait": "esperando etiquetas…",
        "join": "día 7: join por inference ID",
        "prec": "precision@5 nuevos: 0,21 → 0,12",
        "takeaway": "Sin alarma de calidad antes del día 7 no significa «sin degradación»",
        "note": "Valores del caso de ejemplo",
    },
    "en": {
        "ab_title": "A/B testing with production variants on one endpoint",
        "clients": "Real users",
        "endpoint": "SageMaker endpoint",
        "current": "variant current",
        "candidate": "variant candidate",
        "weight": "weight",
        "p1": "Weights 90/10: 10% of users get the new model",
        "p2": "UpdateEndpointWeightsAndCapacities → 50/50",
        "p3": "→ 0/100: all traffic to the new model",
        "no_redeploy": "No endpoint update · each variant publishes its own CloudWatch metrics",
        "ld_title": "Which signal is available, and when (labels arrive 7 days late)",
        "day": "day",
        "svc": "Service metrics",
        "svc_sub": "errors, latency, volume",
        "drift": "Data drift",
        "drift_sub": "capture vs. baseline",
        "quality": "Model quality",
        "quality_sub": "predictions + labels",
        "svc_ok": "minutes: the service works",
        "drift_alarm": "day 3: high PSI on 2 features",
        "wait": "waiting for labels…",
        "join": "day 7: join by inference ID",
        "prec": "precision@5 new customers: 0.21 → 0.12",
        "takeaway": "No quality alarm before day 7 does not mean “no degradation”",
        "note": "Values from the worked example",
    },
})


class AbTrafficShift(PacedScene):
    def construct(self):
        title = label(TEXT["ab_title"], 26, INK, "BOLD", max_width=12.4).to_edge(UP, buff=0.4)
        users = icon_node("aws/users", TEXT["clients"], None, 2.6, 1.0, stroke=INK_SOFT, title_size=18,
                          icon_height=0.55).move_to(LEFT * 5.4 + UP * 0.2)

        ep = RoundedRectangle(width=7.6, height=4.0, corner_radius=0.14, stroke_color=INK_SOFT, stroke_width=2)
        ep.set_fill(SURFACE, opacity=1).move_to(RIGHT * 1.9 + UP * 0.2)
        ep_t = icon_title("aws/sagemaker-ai", TEXT["endpoint"], 19, icon_height=0.42).next_to(
            ep.get_top(), DOWN, buff=0.15)
        var_a = icon_node("aws/sagemaker-model", TEXT["current"], None, 3.2, 0.9, stroke=MUTED, fill="#ffffff",
                          title_size=17, icon_height=0.55).move_to(
            ep.get_center() + RIGHT * 1.9 + UP * 0.55)
        var_b = icon_node("aws/sagemaker-model", TEXT["candidate"], None, 3.2, 0.9, stroke=OK, fill="#ffffff",
                          title_size=17, icon_height=0.55).move_to(
            ep.get_center() + RIGHT * 1.9 + DOWN * 1.0)
        router = Dot(ep.get_center() + LEFT * 2.2 + DOWN * 0.1, radius=0.1, color=INK_SOFT)
        to_a = Line(router.get_center(), var_a.get_left(), color=GRAY, stroke_width=3)
        to_b = Line(router.get_center(), var_b.get_left(), color=GRAY, stroke_width=3)
        entry = Arrow(users.get_right(), router.get_center(), buff=0.1, color=MUTED, stroke_width=3)

        def weights(a, b):
            wa = label(f"{TEXT['weight']} {a}", 16, MUTED).next_to(var_a, UP, buff=0.1)
            wb = label(f"{TEXT['weight']} {b}", 16, OK).next_to(var_b, DOWN, buff=0.1)
            return VGroup(wa, wb)

        w = weights(num(0.9), num(0.1))
        self.play(FadeIn(title), FadeIn(users), FadeIn(ep), FadeIn(ep_t), FadeIn(var_a), FadeIn(var_b),
                  FadeIn(router), Create(to_a), Create(to_b), Create(entry), FadeIn(w), run_time=1.0)

        caption = label(TEXT["p1"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.85)
        self.play(FadeIn(caption), run_time=0.3)

        def burst(n_b, total=10):
            dots, anims = [], []
            for i in range(total):
                go_b = i < n_b
                d = Dot(users.get_right(), radius=0.08, color=OK if go_b else INK_SOFT)
                target = var_b.get_left() if go_b else var_a.get_left()
                path = VMobject().set_points_as_corners([users.get_right(), router.get_center(), target])
                dots.append(d)
                anims.append(MoveAlongPath(d, path, run_time=1.1))
            for k in range(0, total, 5):
                self.play(*anims[k:k + 5], run_time=0.55)
            self.play(*[FadeOut(d) for d in dots], run_time=0.2)

        # 9 de 10 a current, 1 de 10 a candidate. 9 of 10 to current, 1 of 10 to candidate.
        burst(1)
        for text, (a, b), n_b in ((TEXT["p2"], (num(0.5), num(0.5)), 5), (TEXT["p3"], ("0", "1"), 10)):
            new_w = weights(a, b)
            new_c = label(text, 21, ACCENT if n_b == 5 else INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.85)
            anims = [Transform(w, new_w), FadeOut(caption), FadeIn(new_c)]
            if n_b == 10:
                anims += [to_a.animate.set_color(RULE), var_a.animate.set_opacity(0.45)]
            self.play(*anims, run_time=0.6)
            caption = new_c
            burst(n_b)

        note = label(TEXT["no_redeploy"], 18, OK, max_width=12.2).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.2)


class LabelDelay(PacedScene):
    def construct(self):
        title = label(TEXT["ld_title"], 24, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.4)
        x0, unit = -2.6, 0.82  # día 0 a 10 / day 0 to 10
        rows_y = [1.6, 0.1, -1.4]
        axis_y = -2.35
        axis = Line([x0, axis_y, 0], [x0 + 10 * unit, axis_y, 0], color=INK_SOFT)
        ticks = VGroup()
        for d in range(0, 11):
            x = x0 + d * unit
            ticks.add(Line([x, axis_y - 0.06, 0], [x, axis_y + 0.06, 0], color=INK_SOFT))
            ticks.add(label(str(d), 15, MUTED).move_to([x, axis_y - 0.28, 0]))
        day_lbl = label(TEXT["day"], 15, MUTED).move_to([x0 + 10 * unit + 0.45, axis_y - 0.28, 0])
        names = VGroup()
        for y, k in zip(rows_y, ("svc", "drift", "quality")):
            n = label(TEXT[k], 19, INK, "BOLD", max_width=3.2)
            s = label(TEXT[k + "_sub"], 14, MUTED, max_width=3.2)
            g = VGroup(n, s).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            g.move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            names.add(g)
        lanes = VGroup(*[Line([x0, y, 0], [x0 + 10 * unit, y, 0], color=RULE, stroke_width=10) for y in rows_y])
        self.play(FadeIn(title), Create(axis), FadeIn(ticks), FadeIn(day_lbl), FadeIn(names), FadeIn(lanes),
                  run_time=0.9)

        def bar(row, start, end, color):
            r = Rectangle(width=max((end - start) * unit, 0.01), height=0.26, stroke_width=0).set_fill(color, 1)
            return r.move_to([x0 + start * unit, rows_y[row], 0], aligned_edge=LEFT)

        # Día 0 a 10 en barrido; cada señal aparece cuando existe. Sweep day 0 to 10.
        svc = bar(0, 0, 0.01, OK)
        self.add(svc)
        self.play(Transform(svc, bar(0, 0, 3, OK)), run_time=0.8)
        svc_t = label(TEXT["svc_ok"], 15, OK).next_to(bar(0, 0, 3, OK), UP, buff=0.1).align_to(svc, LEFT)
        self.play(FadeIn(svc_t), run_time=0.3)

        drift = bar(1, 3, 3.01, AMBER)
        self.add(drift)
        marker = DashedLine([x0 + 3 * unit, rows_y[1] + 0.35, 0], [x0 + 3 * unit, axis_y, 0], color=AMBER,
                            dash_length=0.08)
        drift_t = label(TEXT["drift_alarm"], 15, INK_SOFT).next_to(drift, UP, buff=0.12).align_to(drift, LEFT)
        wait_t = label(TEXT["wait"], 15, MUTED).move_to([x0 + 3.5 * unit, rows_y[2] + 0.32, 0], aligned_edge=LEFT)
        self.play(Transform(svc, bar(0, 0, 7, OK)), Transform(drift, bar(1, 3, 7, AMBER)), Create(marker),
                  FadeIn(drift_t), FadeIn(wait_t), run_time=1.2)

        join_line = DashedLine([x0 + 7 * unit, rows_y[0] + 0.35, 0], [x0 + 7 * unit, axis_y, 0], color=ACCENT,
                               dash_length=0.08)
        qual = bar(2, 7, 7.01, ACCENT)
        self.add(qual)
        join_t = label(TEXT["join"], 15, ACCENT).next_to(qual, UP, buff=0.12).align_to(qual, LEFT)
        self.play(FadeOut(wait_t), Create(join_line), FadeIn(join_t), run_time=0.5)
        prec = label(TEXT["prec"], 15, ACCENT).next_to(bar(2, 7, 10, ACCENT), DOWN, buff=0.14)
        prec.align_to(qual, LEFT).shift(LEFT * 1.4)
        self.play(Transform(svc, bar(0, 0, 10, OK)), Transform(drift, bar(1, 3, 10, AMBER)),
                  Transform(qual, bar(2, 7, 10, ACCENT)), FadeIn(prec), run_time=1.0)

        take = label(TEXT["takeaway"], 20, INK, "BOLD", max_width=12.4).to_edge(DOWN, buff=0.45)
        note = label(TEXT["note"], 14, MUTED).to_corner(DOWN + RIGHT, buff=0.15)
        self.play(FadeIn(take), FadeIn(note), run_time=0.5)
        self.wait(1.3)
