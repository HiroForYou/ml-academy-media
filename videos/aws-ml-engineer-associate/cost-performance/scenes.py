"""
Videos cortos del tema 4.2 (costo y rendimiento). Short videos for topic 4.2.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/cost-performance/scenes.py --scene PromptCaching --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"prompt-caching": "PromptCaching", "target-tracking": "TargetTracking"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Create, Cross, DashedLine, FadeIn, FadeOut, FadeTransform, Line, Rectangle, RoundedRectangle,
    Transform, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE, icon_title, label, num, pick,
)

TEXT = pick({
    "es": {
        "pc_title": "Prompt caching en Bedrock: el prefijo estático va primero",
        "system": "system prompt estático · 5000 tokens",
        "question": "pregunta · 40",
        "req": "solicitud",
        "write": "CacheWriteInputTokenCount = 5000",
        "read": "CacheReadInputTokenCount = 5000",
        "write_sub": "la escritura en caché puede costar más",
        "read_sub": "la lectura de caché cuesta menos",
        "bad": "Si la parte variable va primero, el prefijo cambia en cada solicitud",
        "miss": "sin acierto: CacheReadInputTokenCount = 0",
        "takeaway": "Checkpoint de caché después del contenido estático; lo variable al final",
        "tt_title": "Target tracking: mantener InvocationsPerInstance cerca del objetivo",
        "target": "objetivo: 100 por instancia",
        "traffic": "Tráfico",
        "per_min": "invocaciones/min",
        "inst": "instancia",
        "s1": "200/min con 2 instancias: 100 por instancia",
        "s2": "El tráfico sube a 400/min: 200 por instancia, sobre el objetivo",
        "s3": "Scale-out a 4 instancias: vuelve a 100 por instancia",
        "s4": "Baja a 150/min: tras el cooldown, scale-in a 2 instancias",
        "note": "Ilustrativo · capacidad mínima de una variante ≥ 1 · cooldown predeterminado 300 s",
    },
    "en": {
        "pc_title": "Prompt caching in Bedrock: the static prefix goes first",
        "system": "static system prompt · 5000 tokens",
        "question": "question · 40",
        "req": "request",
        "write": "CacheWriteInputTokenCount = 5000",
        "read": "CacheReadInputTokenCount = 5000",
        "write_sub": "cache writes can cost more",
        "read_sub": "cache reads cost less",
        "bad": "If the variable part goes first, the prefix changes on every request",
        "miss": "no hit: CacheReadInputTokenCount = 0",
        "takeaway": "Cache checkpoint after the static content; the variable part at the end",
        "tt_title": "Target tracking: keep InvocationsPerInstance near the target",
        "target": "target: 100 per instance",
        "traffic": "Traffic",
        "per_min": "invocations/min",
        "inst": "instance",
        "s1": "200/min on 2 instances: 100 per instance",
        "s2": "Traffic rises to 400/min: 200 per instance, above target",
        "s3": "Scale out to 4 instances: back to 100 per instance",
        "s4": "Drops to 150/min: after the cooldown, scale in to 2 instances",
        "note": "Illustrative · a variant's minimum capacity ≥ 1 · default cooldown 300 s",
    },
})


def block(text, width, fill, stroke, color=INK, size=15):
    box = RoundedRectangle(width=width, height=0.55, corner_radius=0.08, stroke_color=stroke, stroke_width=2)
    box.set_fill(fill, opacity=1)
    return VGroup(box, label(text, size, color, max_width=width - 0.2).move_to(box))


class PromptCaching(PacedScene):
    def construct(self):
        title = icon_title("aws/bedrock", TEXT["pc_title"], 26, icon_height=0.6, max_width=12.4).to_edge(UP, buff=0.35)
        self.play(FadeIn(title), run_time=0.5)
        x0 = -6.2
        rows = []
        for i in range(3):
            y = 2.0 - i * 1.05
            tag = label(f"{TEXT['req']} {i + 1}", 15, MUTED).move_to([x0, y, 0], aligned_edge=LEFT)
            sysb = block(TEXT["system"], 4.4, SURFACE, INK_SOFT).move_to([x0 + 1.55, y, 0], aligned_edge=LEFT)
            q = block(TEXT["question"], 1.6, "#ffffff", AMBER).next_to(sysb, RIGHT, buff=0.08)
            rows.append(VGroup(tag, sysb, q))

        metric_x = 1.95
        for i, row in enumerate(rows):
            self.play(FadeIn(row), run_time=0.45)
            sysb = row[1]
            if i == 0:
                self.play(sysb[0].animate.set_stroke(AMBER, 3), run_time=0.3)
                m = label(TEXT["write"], 16, INK).move_to([metric_x, row.get_y() + 0.13, 0], aligned_edge=LEFT)
                s = label(TEXT["write_sub"], 13, MUTED).next_to(m, DOWN, buff=0.06).align_to(m, LEFT)
            else:
                self.play(sysb[0].animate.set_fill(OK, 0.25).set_stroke(OK, 3), run_time=0.3)
                m = label(TEXT["read"], 16, OK).move_to([metric_x, row.get_y() + 0.13, 0], aligned_edge=LEFT)
                s = label(TEXT["read_sub"], 13, MUTED).next_to(m, DOWN, buff=0.06).align_to(m, LEFT)
            self.play(FadeIn(m), FadeIn(s), run_time=0.35)

        sep = Line([x0, -1.15, 0], [6.2, -1.15, 0], color=RULE)
        bad = label(TEXT["bad"], 18, ACCENT, max_width=12.4).move_to([0, -1.5, 0])
        y = -2.2
        q = block(TEXT["question"], 1.6, "#ffffff", AMBER).move_to([x0 + 1.55, y, 0], aligned_edge=LEFT)
        sysb = block(TEXT["system"], 4.4, SURFACE, INK_SOFT).next_to(q, RIGHT, buff=0.08)
        self.play(Create(sep), FadeIn(bad), FadeIn(q), FadeIn(sysb), run_time=0.6)
        miss = label(TEXT["miss"], 16, ACCENT).move_to([metric_x, y, 0], aligned_edge=LEFT)
        cross = Cross(sysb, stroke_color=ACCENT, stroke_width=3)
        self.play(Create(cross), FadeIn(miss), run_time=0.5)

        take = label(TEXT["takeaway"], 19, INK, "BOLD", max_width=12.4).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(take), run_time=0.4)
        self.wait(1.3)


class TargetTracking(PacedScene):
    def construct(self):
        title = icon_title("aws/application-auto-scaling", TEXT["tt_title"], 25, icon_height=0.6, max_width=12.4).to_edge(UP, buff=0.35)
        base_y, scale = -1.6, 0.0155  # alto por invocación/min / height per invocation/min
        target_y = base_y + 100 * scale
        target = DashedLine([-4.6, target_y, 0], [6.6, target_y, 0], color=OK, dash_length=0.1)
        target_t = label(TEXT["target"], 14, OK).next_to(target, DOWN, buff=0.08).align_to(target, RIGHT)
        floor = Line([-4.6, base_y, 0], [6.4, base_y, 0], color=RULE)

        traffic_t = label(TEXT["traffic"], 17, INK_SOFT, "BOLD").move_to([-5.7, 1.5, 0])
        self.play(FadeIn(title), Create(floor), Create(target), FadeIn(target_t), FadeIn(traffic_t), run_time=0.8)

        def traffic(value):
            v = label(str(value), 30, INK, "BOLD").move_to([-5.7, 0.8, 0])
            u = label(TEXT["per_min"], 13, MUTED).next_to(v, DOWN, buff=0.08)
            return VGroup(v, u)

        def fleet(n, per):
            g = VGroup()
            for i in range(n):
                x = -3.6 + i * 2.5
                color = ACCENT if per > 120 else INK_SOFT
                bar = Rectangle(width=1.1, height=max(per * scale, 0.02), stroke_width=0)
                bar.set_fill(AMBER if per > 120 else GRAY, 1).move_to([x, base_y, 0], aligned_edge=DOWN)
                val = label(num(per, 0 if per == int(per) else 1), 17, color).next_to(bar, UP, buff=0.08)
                name = label(f"{TEXT['inst']} {i + 1}", 14, MUTED).move_to([x, base_y - 0.3, 0])
                g.add(VGroup(bar, val, name))
            return g

        def caption(key, color=INK_SOFT):
            return label(TEXT[key], 20, color, max_width=12.2).to_edge(DOWN, buff=0.85)

        tr = traffic(200)
        fl = fleet(2, 100)
        cap = caption("s1")
        self.play(FadeIn(tr), FadeIn(fl), FadeIn(cap), run_time=0.7)
        self.wait(0.6)

        new_fl = fleet(2, 200)
        self.play(Transform(tr, traffic(400)), Transform(fl, new_fl), FadeTransform(cap, new_cap := caption("s2", ACCENT)),
                  run_time=0.9)
        self.wait(0.6)

        four = fleet(4, 100)
        cap = new_cap
        self.play(FadeOut(fl), FadeIn(four), FadeTransform(cap, new_cap := caption("s3", OK)), run_time=0.9)
        cap = new_cap
        self.wait(0.6)

        two = fleet(2, 75)
        low = fleet(4, 37.5)
        self.play(Transform(tr, traffic(150)), Transform(four, low), run_time=0.7)
        self.play(FadeOut(four), FadeIn(two), FadeTransform(cap, caption("s4")), run_time=0.9)

        note = label(TEXT["note"], 15, MUTED, max_width=12.2).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.2)
