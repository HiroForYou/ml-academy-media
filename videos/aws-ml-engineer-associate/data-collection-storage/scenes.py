"""
Videos cortos del tema 1.1 (recolectar y almacenar datos). Short videos for topic 1.1.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/data-collection-storage/scenes.py --scene StreamToS3 --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"stream-to-s3": "StreamToS3", "feature-store-event-time": "FeatureStoreEventTime"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, Cross, Dot, FadeIn, FadeOut, Indicate, Line, MoveAlongPath,
    Rectangle, RoundedRectangle, Scene, Transform, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, label, node, pick,
)

TEXT = pick({
    "es": {
        "app": "App de la tienda",
        "events": "eventos JSON",
        "kds": "Kinesis Data Streams",
        "shard": "shard",
        "firehose": "Amazon Data Firehose",
        "buffer": "búfer (tamaño o tiempo)",
        "schema": "Esquema en Glue Data Catalog",
        "convert": "JSON → Parquet",
        "s3": "Amazon S3",
        "raw": "raw/  (JSON original)",
        "curated": "dt=2026-10-22/  (Parquet)",
        "retention": "Kinesis retiene 24 h por defecto (hasta 365 días): no es el histórico",
        "history": "El histórico completo vive en S3",
        "title_fs": "Feature group: customer_id = 42",
        "incoming": "Registros que llegan",
        "online": "Online store",
        "online_sub": "solo el registro más reciente",
        "offline": "Offline store (S3)",
        "offline_sub": "todo el historial, solo anexado",
        "late": "llega tarde",
        "ignored": "09:55 < 10:05: no sobrescribe",
        "takeaway": "Online para servir · offline para entrenar",
        "spend": "gasto_24h",
    },
    "en": {
        "app": "Store app",
        "events": "JSON events",
        "kds": "Kinesis Data Streams",
        "shard": "shard",
        "firehose": "Amazon Data Firehose",
        "buffer": "buffer (size or time)",
        "schema": "Schema in Glue Data Catalog",
        "convert": "JSON → Parquet",
        "s3": "Amazon S3",
        "raw": "raw/  (original JSON)",
        "curated": "dt=2026-10-22/  (Parquet)",
        "retention": "Kinesis keeps 24 h by default (up to 365 days): it is not the history",
        "history": "The full history lives in S3",
        "title_fs": "Feature group: customer_id = 42",
        "incoming": "Incoming records",
        "online": "Online store",
        "online_sub": "latest record only",
        "offline": "Offline store (S3)",
        "offline_sub": "full history, append-only",
        "late": "arrives late",
        "ignored": "09:55 < 10:05: no overwrite",
        "takeaway": "Online to serve · offline to train",
        "spend": "spend_24h",
    },
})


class StreamToS3(Scene):
    def construct(self):
        app = node(TEXT["app"], 2.2, 1.0, size=20).move_to(LEFT * 5.6 + UP * 0.9)
        app_sub = label(TEXT["events"], 16, MUTED).next_to(app, DOWN, buff=0.15)

        kds_box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        kds_box.set_fill(SURFACE, opacity=1).move_to(LEFT * 2.2 + UP * 0.9)
        kds_title = label(TEXT["kds"], 18, INK, "BOLD", max_width=2.8).next_to(kds_box.get_top(), DOWN, buff=0.14)
        lanes = VGroup()
        for i in range(3):
            y = kds_box.get_center()[1] + 0.25 - i * 0.5
            lane = Line([kds_box.get_left()[0] + 0.25, y, 0], [kds_box.get_right()[0] - 0.25, y, 0], color=GRAY,
                        stroke_width=6)
            tag = label(f"{TEXT['shard']} {i + 1}", 12, MUTED).next_to(lane, UP, buff=0.04).align_to(lane, LEFT)
            lanes.add(VGroup(lane, tag))

        fh_box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        fh_box.set_fill(SURFACE, opacity=1).move_to(RIGHT * 1.6 + UP * 0.9)
        fh_title = label(TEXT["firehose"], 18, INK, "BOLD", max_width=2.8).next_to(fh_box.get_top(), DOWN, buff=0.14)
        buf_frame = Rectangle(width=2.3, height=0.32, stroke_color=INK_SOFT, stroke_width=1.5).move_to(
            fh_box.get_center() + UP * 0.05)
        buf_lbl = label(TEXT["buffer"], 13, MUTED).next_to(buf_frame, DOWN, buff=0.08)
        convert = label(TEXT["convert"], 16, ACCENT, "BOLD").next_to(buf_lbl, DOWN, buff=0.12)
        schema = node(TEXT["schema"], 3.0, 0.6, stroke=MUTED, fill="#ffffff", size=15).next_to(fh_box, DOWN, buff=0.55)
        schema_arrow = Arrow(schema.get_top(), fh_box.get_bottom(), buff=0.06, color=MUTED, stroke_width=2.5)

        s3_box = RoundedRectangle(width=3.1, height=2.3, corner_radius=0.12, stroke_color=OK, stroke_width=2.2)
        s3_box.set_fill("#ffffff", opacity=1).move_to(RIGHT * 5.3 + UP * 0.9)
        s3_title = label(TEXT["s3"], 18, INK, "BOLD").next_to(s3_box.get_top(), DOWN, buff=0.14)
        raw_lbl = label(TEXT["raw"], 13, INK_SOFT).move_to(s3_box.get_center() + UP * 0.25)
        cur_lbl = label(TEXT["curated"], 13, INK_SOFT).move_to(s3_box.get_center() + DOWN * 0.45)
        for lbl in (raw_lbl, cur_lbl):
            lbl.align_to(s3_box, LEFT).shift(RIGHT * 0.2)

        arrows = VGroup(
            Arrow(app.get_right(), kds_box.get_left(), buff=0.08, color=MUTED, stroke_width=3),
            Arrow(kds_box.get_right(), fh_box.get_left(), buff=0.08, color=MUTED, stroke_width=3),
            Arrow(fh_box.get_right(), s3_box.get_left(), buff=0.08, color=MUTED, stroke_width=3),
        )

        self.play(FadeIn(app), FadeIn(app_sub), FadeIn(kds_box), FadeIn(kds_title), FadeIn(lanes),
                  FadeIn(fh_box), FadeIn(fh_title), FadeIn(s3_box), FadeIn(s3_title), Create(arrows), run_time=1.0)
        self.play(FadeIn(buf_frame), FadeIn(buf_lbl), FadeIn(schema), Create(schema_arrow), FadeIn(convert),
                  FadeIn(raw_lbl), FadeIn(cur_lbl), run_time=0.7)

        # Eventos entran a los shards según la clave de partición. Events enter shards by partition key.
        rng = np.random.default_rng(4)
        fill = Rectangle(width=0.01, height=0.26, stroke_width=0).set_fill(AMBER, opacity=1)
        fill.align_to(buf_frame, LEFT).shift(RIGHT * 0.03).set_y(buf_frame.get_center()[1])
        self.add(fill)
        in_stream = VGroup()
        for wave in range(3):
            dots, paths = [], []
            for _ in range(3):
                lane = lanes[int(rng.integers(0, 3))][0]
                d = Dot(app.get_right(), radius=0.07, color=ACCENT)
                x = lane.get_start()[0] + rng.uniform(0.2, lane.get_length() - 0.2)
                dots.append(d)
                paths.append(Line(app.get_right(), [x, lane.get_center()[1], 0]))
            self.play(*[MoveAlongPath(d, p) for d, p in zip(dots, paths)], run_time=0.45)
            in_stream.add(*dots)
            # Firehose lee copias y el búfer se llena. Firehose reads copies and the buffer fills.
            copies = [d.copy() for d in dots]
            target_w = 2.24 * (wave + 1) / 3
            new_fill = Rectangle(width=target_w, height=0.26, stroke_width=0).set_fill(AMBER, opacity=1)
            new_fill.align_to(buf_frame, LEFT).shift(RIGHT * 0.03).set_y(buf_frame.get_center()[1])
            self.play(*[c.animate.move_to(buf_frame.get_center()).set_opacity(0) for c in copies],
                      Transform(fill, new_fill), run_time=0.45)
            self.remove(*copies)

        # El búfer se vacía: Parquet a dt=, JSON a raw/. Buffer flushes: Parquet to dt=, JSON to raw/.
        pq = RoundedRectangle(width=0.5, height=0.36, corner_radius=0.05, stroke_width=0).set_fill(OK, 1)
        js = RoundedRectangle(width=0.5, height=0.36, corner_radius=0.05, stroke_width=0).set_fill(GRAY, 1)
        pq.move_to(buf_frame.get_center())
        js.move_to(buf_frame.get_center())
        self.add(pq, js)
        empty = fill.copy().stretch_to_fit_width(0.01).align_to(buf_frame, LEFT)
        self.play(Transform(fill, empty), pq.animate.next_to(cur_lbl, RIGHT, buff=0.12),
                  js.animate.next_to(raw_lbl, RIGHT, buff=0.12), run_time=0.8)
        self.play(Indicate(s3_box, color=OK, scale_factor=1.04), run_time=0.5)

        # La retención de Kinesis expira; S3 conserva todo. Kinesis retention expires; S3 keeps everything.
        retention = label(TEXT["retention"], 21, ACCENT, max_width=12.5).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(retention), run_time=0.4)
        self.play(*[d.animate.set_opacity(0.0) for d in in_stream], run_time=1.0)
        history = label(TEXT["history"], 24, OK, "BOLD").to_edge(DOWN, buff=0.85)
        self.play(FadeIn(history), Indicate(VGroup(pq, js), color=OK), run_time=0.6)
        self.wait(1.2)


class FeatureStoreEventTime(Scene):
    RECORDS = [("10:00", "3", False), ("10:05", "5", False), ("09:55", "2", True)]

    def record(self, time, value, late):
        stroke = AMBER if late else INK_SOFT
        box = RoundedRectangle(width=3.4, height=0.62, corner_radius=0.08, stroke_color=stroke, stroke_width=2)
        box.set_fill("#ffffff", opacity=1)
        txt = label(f"42 · {time} · {TEXT['spend']} = {value}", 17, INK).move_to(box)
        return VGroup(box, txt)

    def construct(self):
        title = label(TEXT["title_fs"], 26, INK, "BOLD").to_edge(UP, buff=0.45)
        inc = label(TEXT["incoming"], 18, MUTED).move_to(LEFT * 4.6 + UP * 2.4)

        online = RoundedRectangle(width=4.6, height=1.5, corner_radius=0.12, stroke_color=OK, stroke_width=2.2)
        online.set_fill(SURFACE, opacity=1).move_to(RIGHT * 2.9 + UP * 1.5)
        on_t = label(TEXT["online"], 20, INK, "BOLD").next_to(online.get_top(), DOWN, buff=0.12).align_to(online, LEFT).shift(RIGHT * 0.2)
        on_s = label(TEXT["online_sub"], 14, MUTED).next_to(on_t, RIGHT, buff=0.2).align_to(on_t, DOWN)

        offline = RoundedRectangle(width=4.6, height=2.75, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2.2)
        offline.set_fill(SURFACE, opacity=1).move_to(RIGHT * 2.9 + DOWN * 1.35)
        off_t = label(TEXT["offline"], 20, INK, "BOLD").next_to(offline.get_top(), DOWN, buff=0.12).align_to(offline, LEFT).shift(RIGHT * 0.2)
        off_s = label(TEXT["offline_sub"], 14, MUTED).next_to(off_t, DOWN, buff=0.06).align_to(off_t, LEFT)

        self.play(FadeIn(title), FadeIn(inc), FadeIn(online), FadeIn(on_t), FadeIn(on_s), FadeIn(offline),
                  FadeIn(off_t), FadeIn(off_s), run_time=0.8)

        online_slot = online.get_center() + DOWN * 0.22
        current = None
        rows = []
        for i, (time, value, late) in enumerate(self.RECORDS):
            rec = self.record(time, value, late).move_to(LEFT * 4.6 + UP * (1.5 - i * 1.0))
            extra = []
            if late:
                tag = label(TEXT["late"], 15, AMBER, "BOLD").next_to(rec, DOWN, buff=0.08)
                extra.append(tag)
            self.play(FadeIn(rec, shift=RIGHT * 0.3), *[FadeIn(e) for e in extra], run_time=0.45)

            # Offline: siempre se anexa. Offline: always appended.
            row = rec.copy()
            row_target = offline.get_top() + DOWN * (1.0 + 0.55 * i)
            self.play(row.animate.scale(0.82).move_to(row_target), run_time=0.6)
            rows.append(row)

            # Online: solo si el event time es más reciente. Online: only if the event time is newer.
            if not late:
                newer = rec.copy()
                if current is None:
                    self.play(newer.animate.scale(0.9).move_to(online_slot), run_time=0.55)
                else:
                    self.play(newer.animate.scale(0.9).move_to(online_slot), FadeOut(current), run_time=0.55)
                current = newer
            else:
                ghost = rec.copy()
                self.play(ghost.animate.scale(0.9).move_to(online_slot),
                          run_time=0.5)
                cross = Cross(ghost, stroke_color=ACCENT, stroke_width=4)
                note = label(TEXT["ignored"], 16, ACCENT, "BOLD").next_to(online, DOWN, buff=0.17)
                self.play(Create(cross), FadeIn(note), run_time=0.45)
                self.play(FadeOut(ghost), FadeOut(cross), Indicate(current, color=OK, scale_factor=1.06),
                          run_time=0.6)
            self.wait(0.15)

        take = label(TEXT["takeaway"], 24, OK, "BOLD").to_edge(DOWN, buff=0.3)
        self.play(FadeIn(take), run_time=0.4)
        self.wait(1.2)
