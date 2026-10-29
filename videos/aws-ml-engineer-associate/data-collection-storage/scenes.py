"""
Videos cortos del tema 1.1 (recolectar y almacenar datos). Short videos for topic 1.1.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/data-collection-storage/scenes.py --scene StreamToS3 --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {
    "stream-to-s3": "StreamToS3",
    "feature-store-event-time": "FeatureStoreEventTime",
    "athena-partitions": "AthenaPartitions",
}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, Cross, Dot, FadeIn, FadeOut, Indicate, Line, MoveAlongPath,
    Rectangle, RoundedRectangle, Transform, VGroup,
)
from manim import DashedVMobject  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, icon_node, icon_title, label, node, pick, pulse,
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


class StreamToS3(PacedScene):
    def construct(self):
        app = icon_node("aws/application", TEXT["app"], TEXT["events"], 2.7, 1.1, stroke=INK_SOFT, title_size=17,
                        desc_size=14, icon_height=0.5).move_to(LEFT * 5.6 + UP * 0.9)
        app_sub = VGroup()

        kds_box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        kds_box.set_fill(SURFACE, opacity=1).move_to(LEFT * 2.2 + UP * 0.9)
        kds_title = icon_title("aws/kinesis-data-streams", TEXT["kds"], 16, max_width=2.8).next_to(
            kds_box.get_top(), DOWN, buff=0.12)
        lanes = VGroup()
        for i in range(3):
            y = kds_box.get_center()[1] + 0.12 - i * 0.48
            lane = Line([kds_box.get_left()[0] + 0.25, y, 0], [kds_box.get_right()[0] - 0.25, y, 0], color=GRAY,
                        stroke_width=6)
            tag = label(f"{TEXT['shard']} {i + 1}", 12, MUTED).next_to(lane, UP, buff=0.04).align_to(lane, LEFT)
            lanes.add(VGroup(lane, tag))

        fh_box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        fh_box.set_fill(SURFACE, opacity=1).move_to(RIGHT * 1.6 + UP * 0.9)
        fh_title = icon_title("aws/data-firehose", TEXT["firehose"], 16, max_width=2.8).next_to(
            fh_box.get_top(), DOWN, buff=0.12)
        buf_frame = Rectangle(width=2.3, height=0.32, stroke_color=INK_SOFT, stroke_width=1.5).move_to(
            fh_box.get_center() + DOWN * 0.08)
        buf_lbl = label(TEXT["buffer"], 13, MUTED).next_to(buf_frame, DOWN, buff=0.08)
        convert = label(TEXT["convert"], 16, ACCENT, "BOLD").next_to(buf_lbl, DOWN, buff=0.12)
        schema = icon_node("aws/glue", TEXT["schema"], None, 3.4, 0.75, stroke=MUTED, fill="#ffffff", title_size=14,
                           icon_height=0.45).next_to(fh_box, DOWN, buff=0.5)
        schema_arrow = Arrow(schema.get_top(), fh_box.get_bottom(), buff=0.06, color=MUTED, stroke_width=2.5)

        s3_box = RoundedRectangle(width=3.1, height=2.3, corner_radius=0.12, stroke_color=OK, stroke_width=2.2)
        s3_box.set_fill("#ffffff", opacity=1).move_to(RIGHT * 5.2 + UP * 0.9)
        s3_title = icon_title("aws/s3", TEXT["s3"], 16).next_to(s3_box.get_top(), DOWN, buff=0.12)
        raw_lbl = label(TEXT["raw"], 13, INK_SOFT).move_to(s3_box.get_center() + UP * 0.12)
        cur_lbl = label(TEXT["curated"], 13, INK_SOFT).move_to(s3_box.get_center() + DOWN * 0.55)
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
        self.play(pulse(s3_box, OK), run_time=0.6)

        # La retención de Kinesis expira; S3 conserva todo. Kinesis retention expires; S3 keeps everything.
        retention = label(TEXT["retention"], 21, ACCENT, max_width=12.5).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(retention), run_time=0.4)
        self.play(*[d.animate.set_opacity(0.0) for d in in_stream], run_time=1.0)
        history = label(TEXT["history"], 24, OK, "BOLD").to_edge(DOWN, buff=0.85)
        self.play(FadeIn(history), Indicate(VGroup(pq, js), color=OK), run_time=0.6)
        self.wait(1.2)


class FeatureStoreEventTime(PacedScene):
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
        on_t = icon_title("aws/sagemaker-ai", TEXT["online"], 20, icon_height=0.36).next_to(online.get_top(), DOWN, buff=0.12).align_to(online, LEFT).shift(RIGHT * 0.2)
        on_s = label(TEXT["online_sub"], 14, MUTED).next_to(on_t, RIGHT, buff=0.16).align_to(on_t[1], DOWN)

        offline = RoundedRectangle(width=4.6, height=2.75, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2.2)
        offline.set_fill(SURFACE, opacity=1).move_to(RIGHT * 2.9 + DOWN * 1.35)
        off_t = icon_title("aws/s3", TEXT["offline"], 20, icon_height=0.36).next_to(offline.get_top(), DOWN, buff=0.12).align_to(offline, LEFT).shift(RIGHT * 0.2)
        off_s = label(TEXT["offline_sub"], 14, MUTED).next_to(off_t, DOWN, buff=0.06).align_to(off_t[1], LEFT)

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
            row_target = offline.get_top() + DOWN * (1.1 + 0.55 * i)
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


ATHENA = pick({
    "es": {
        "title": "Athena: particiones y datos escaneados",
        "scanned": "datos escaneados",
        "q1": "FROM eventos",
        "q2": "… WHERE month = 10",
        "c1": "Sin filtro, Athena escanea todos los objetos",
        "c2": "Con WHERE por partición lee solo month=10: menos datos, menos costo",
        "c4": "Partición nueva: MSCK REPAIR TABLE o ALTER TABLE ADD PARTITION",
        "c5": "Con partition projection no se registran",
        "projection": "projection",
        "note": "Ilustrativo: 10 GB por partición",
    },
    "en": {
        "title": "Athena: partitions and data scanned",
        "scanned": "data scanned",
        "q1": "FROM events",
        "q2": "… WHERE month = 10",
        "c1": "Without a filter, Athena scans every object",
        "c2": "With a partition WHERE it reads only month=10: less data, lower cost",
        "c4": "New partition: MSCK REPAIR TABLE or ALTER TABLE ADD PARTITION",
        "c5": "With partition projection, nothing to register",
        "projection": "projection",
        "note": "Illustrative: 10 GB per partition",
    },
})


class AthenaPartitions(PacedScene):
    MONTHS = ["07", "08", "09", "10"]
    COLS = [-4.4, -3.0, -1.6, -0.2, 1.2]  # x de cada hueco de día / x of each day slot
    ROW_Y = [1.6, 0.7, -0.2, -1.1]

    def part_box(self, x, y, fill=SURFACE, stroke=INK_SOFT):
        box = RoundedRectangle(width=1.2, height=0.62, corner_radius=0.08, stroke_color=stroke, stroke_width=2)
        box.set_fill(fill, opacity=1).move_to([x, y, 0])
        return box

    def construct(self):
        title = icon_title("aws/athena", ATHENA["title"], 24, icon_height=0.6, max_width=12.6).to_edge(UP, buff=0.35)
        s3_head = icon_title("aws/s3", "S3", 16, MUTED, icon_height=0.42).move_to([-5.5, 2.45, 0])

        rows = []
        row_lbls = VGroup()
        for m, y in zip(self.MONTHS, self.ROW_Y):
            row_lbls.add(label(f"month={m}", 16, MUTED).move_to([-6.1, y, 0]))
            rows.append([self.part_box(x, y) for x in self.COLS[:3]])
        # Consulta y medidor a la derecha. Query and meter on the right.
        q_box = RoundedRectangle(width=4.2, height=0.62, corner_radius=0.08, stroke_color=INK_SOFT, stroke_width=2)
        q_box.set_fill("#ffffff", opacity=1).move_to([4.6, 1.6, 0])
        q = label(ATHENA["q1"], 17, INK).move_to(q_box)
        meter_lbl = label(ATHENA["scanned"], 17, MUTED).move_to([4.6, 0.55, 0])
        frame = Rectangle(width=3.6, height=0.4, stroke_color=INK_SOFT, stroke_width=2).move_to([4.6, 0.0, 0])
        fill = Rectangle(width=0.01, height=0.32, stroke_width=0).set_fill(AMBER, 1)
        fill.align_to(frame, LEFT).shift(RIGHT * 0.04).set_y(frame.get_center()[1])
        value = label("120 GB", 28, ACCENT, "BOLD").move_to([4.6, -0.75, 0])
        self.add(fill)
        grid = VGroup(*[b for r in rows for b in r])
        self.play(FadeIn(title), FadeIn(s3_head), FadeIn(row_lbls), FadeIn(grid), FadeIn(q_box), FadeIn(q), FadeIn(meter_lbl),
                  FadeIn(frame), run_time=0.9)

        # 1. Sin poda: se escanean las cuatro filas. 1. No pruning: all four rows are scanned.
        cap = label(ATHENA["c1"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.75)
        self.play(FadeIn(cap), run_time=0.5)
        for i, r in enumerate(rows):
            new_fill = Rectangle(width=3.5 * (i + 1) / 4, height=0.32, stroke_width=0).set_fill(AMBER, 1)
            new_fill.align_to(frame, LEFT).shift(RIGHT * 0.04).set_y(frame.get_center()[1])
            extra = [FadeIn(value)] if i == 3 else []
            self.play(*[b.animate.set_fill(AMBER, 1) for b in r], Transform(fill, new_fill), *extra, run_time=0.5)

        # 2. Con WHERE sobre la partición solo se lee month=10. 2. With a partition WHERE only month=10 is read.
        cap2 = label(ATHENA["c2"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.75)
        reset = Rectangle(width=0.01, height=0.32, stroke_width=0).set_fill(OK, 1)
        reset.align_to(frame, LEFT).shift(RIGHT * 0.04).set_y(frame.get_center()[1])
        self.play(FadeOut(cap), *[b.animate.set_fill(SURFACE, 1).set_stroke(INK_SOFT) for r in rows for b in r],
                  Transform(fill, reset), FadeOut(value),
                  run_time=0.6)
        self.play(FadeIn(cap2), Transform(q, label(ATHENA["q2"], 17, ACCENT, "BOLD").move_to(q_box)), run_time=0.6)
        dim = [b.animate.set_opacity(0.35) for r in rows[:3] for b in r]
        low = Rectangle(width=3.5 * 0.25, height=0.32, stroke_width=0).set_fill(OK, 1)
        low.align_to(frame, LEFT).shift(RIGHT * 0.04).set_y(frame.get_center()[1])
        value_low = label("30 GB", 28, OK, "BOLD").move_to(value)
        self.play(*dim, *[b.animate.set_fill(OK, 1).set_stroke(OK) for b in rows[3]], Transform(fill, low),
                  FadeIn(value_low), run_time=0.8)


        # 3. Partición nueva: hay que registrarla. 3. New partition: it must be registered.
        new1 = DashedVMobject(self.part_box(self.COLS[3], self.ROW_Y[3], fill="#ffffff", stroke=AMBER), num_dashes=24)
        new1_solid = self.part_box(self.COLS[3], self.ROW_Y[3], fill=OK, stroke=OK)
        cap4 = label(ATHENA["c4"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.75)
        self.play(FadeOut(cap2), FadeIn(cap4), FadeIn(new1), run_time=0.6)
        self.beat(0.5)
        self.play(FadeOut(new1), FadeIn(new1_solid), run_time=0.6)

        # 4. Con projection no hay que registrarla. 4. With projection nothing to register.
        cap5 = label(ATHENA["c5"], 21, INK_SOFT, max_width=12.2).to_edge(DOWN, buff=0.75)
        new2 = self.part_box(self.COLS[4], self.ROW_Y[3], fill=OK, stroke=OK)
        tag = label(ATHENA["projection"], 15, OK, "BOLD").next_to(new2, DOWN, buff=0.08)
        self.play(FadeOut(cap4), FadeIn(cap5), run_time=0.5)
        self.play(FadeIn(new2, scale=0.8), FadeIn(tag), run_time=0.6)
        self.wait(1.2)
