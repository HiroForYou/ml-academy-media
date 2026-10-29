"""
Videos cortos del tema 3.1 (infraestructura de despliegue). Short videos for topic 3.1.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/deployment-infrastructure/scenes.py --scene AsyncInference --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"async-inference": "AsyncInference", "mme-loading": "MmeLoading"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, FadeOut, Line, MoveAlongPath, Rectangle, RoundedRectangle,
    VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene, same_text  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, icon_node, icon_title, label, node, pick, pulse,
)

TEXT = pick({
    "es": {
        "title": "Asynchronous Inference: la solicitud viaja por S3 y una cola",
        "client": "Cliente",
        "s3_in": "S3 entrada",
        "s3_out": "S3 salida",
        "invoke": "InvokeEndpointAsync",
        "queue": "cola interna",
        "endpoint": "Endpoint asíncrono",
        "instances": "instancias",
        "instance1": "instancia",
        "sns": "SNS: éxito o error",
        "s1": "1. El expediente de 500 MB se sube a S3",
        "s2": "2. La llamada solo pasa la ubicación; responde al instante con OutputLocation",
        "s3": "3. Sin instancias, el autoescalado sube de 0 a 1",
        "s4": "4. El resultado se escribe en S3 y SNS avisa",
        "s5": "5. Sin solicitudes en cola, vuelve a 0 instancias: no pagas la noche",
        "title_mme": "Multi-model endpoint: los modelos se cargan desde S3 al primer uso",
        "container": "Contenedor compartido (memoria para 3 modelos)",
        "s3_models": "S3: modelos de clientes",
        "req": "solicitud",
        "cold": "primera llamada: carga desde S3 (más lenta)",
        "warm": "ya en memoria: respuesta rápida",
        "evict": "memoria llena: descarga un modelo poco usado",
        "takeaway": "Barato para miles de modelos poco usados, a cambio de cold starts ocasionales",
        "slot": "libre",
    },
    "en": {
        "title": "Asynchronous Inference: the request travels through S3 and a queue",
        "client": "Client",
        "s3_in": "S3 input",
        "s3_out": "S3 output",
        "invoke": "InvokeEndpointAsync",
        "queue": "internal queue",
        "endpoint": "Asynchronous endpoint",
        "instances": "instances",
        "instance1": "instance",
        "sns": "SNS: success or error",
        "s1": "1. The 500 MB file is uploaded to S3",
        "s2": "2. The call only passes the location; it returns OutputLocation at once",
        "s3": "3. With no instances, auto scaling goes from 0 to 1",
        "s4": "4. The result is written to S3 and SNS notifies",
        "s5": "5. With an empty queue it returns to 0 instances: no cost overnight",
        "title_mme": "Multi-model endpoint: models load from S3 on first use",
        "container": "Shared container (memory for 3 models)",
        "s3_models": "S3: customer models",
        "req": "request",
        "cold": "first call: loads from S3 (slower)",
        "warm": "already in memory: fast response",
        "evict": "memory full: unloads a rarely used model",
        "takeaway": "Cheap for thousands of rarely used models, at the cost of occasional cold starts",
        "slot": "free",
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


def caption(key):
    return label(TEXT[key], 20, INK_SOFT, max_width=12.4).to_edge(DOWN, buff=0.6)


class AsyncInference(PacedScene):
    def construct(self):
        title = label(TEXT["title"], 24, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        client = icon_node("aws/client", TEXT["client"], None, 2.2, 0.95, stroke=INK_SOFT, title_size=19,
                           icon_height=0.55).move_to(LEFT * 5.6 + UP * 1.3)
        s3_in = icon_node("aws/s3", TEXT["s3_in"], None, 2.3, 0.95, stroke=OK, fill="#ffffff", title_size=17,
                          icon_height=0.55).move_to(LEFT * 5.6 + DOWN * 1.1)
        queue = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.08, stroke_color=INK_SOFT, stroke_width=2)
        queue.set_fill(SURFACE, 1).move_to(LEFT * 1.25 + UP * 1.3)
        q_lbl = label(TEXT["queue"], 14, MUTED).next_to(queue, UP, buff=0.08)
        ep = RoundedRectangle(width=3.0, height=2.1, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
        ep.set_fill("#ffffff", 1).move_to(RIGHT * 2.3 + UP * 1.0)
        ep_lbl = icon_title("aws/sagemaker-ai", TEXT["endpoint"], 16, icon_height=0.38, max_width=2.8).next_to(
            ep.get_top(), DOWN, buff=0.1)
        count = label(f"0 {TEXT['instances']}", 18, ACCENT, "BOLD").move_to(ep.get_center() + DOWN * 0.55)
        s3_out = icon_node("aws/s3", TEXT["s3_out"], None, 2.3, 0.95, stroke=OK, fill="#ffffff", title_size=17,
                           icon_height=0.55).move_to(RIGHT * 5.6 + DOWN * 1.1)
        sns_t, _, sns_d = TEXT["sns"].partition(": ")
        sns = icon_node("aws/sns", f"Amazon {sns_t}", sns_d, 2.6, 0.95, stroke=AMBER, fill="#ffffff", title_size=16,
                        desc_size=14, icon_height=0.55).move_to(RIGHT * 5.6 + UP * 1.3)
        self.play(FadeIn(title), FadeIn(client), FadeIn(s3_in), FadeIn(queue), FadeIn(q_lbl), FadeIn(ep),
                  FadeIn(ep_lbl), FadeIn(count), FadeIn(s3_out), FadeIn(sns), run_time=0.8)

        # 1. Subida a S3. Upload to S3.
        cap = Swap()
        doc = RoundedRectangle(width=0.4, height=0.5, corner_radius=0.05, stroke_width=0).set_fill(ACCENT, 1)
        doc.move_to(client.get_bottom() + DOWN * 0.3)
        self.play(*cap.to(caption("s1")), FadeIn(doc), run_time=0.4)
        self.play(doc.animate.move_to(s3_in.get_top() + UP * 0.25), run_time=0.6)

        # 2. Invocación con la ubicación. Invocation with the location.
        call = Arrow(client.get_right(), queue.get_left(), buff=0.1, color=INK_SOFT, stroke_width=3)
        call_lbl = label(TEXT["invoke"], 13, INK).next_to(call, DOWN, buff=0.1)
        token = RoundedRectangle(width=0.36, height=0.36, corner_radius=0.05, stroke_width=0).set_fill(AMBER, 1)
        token.move_to(client.get_right())
        self.play(*cap.to(caption("s2")), Create(call), FadeIn(call_lbl), run_time=0.5)
        self.play(token.animate.move_to(queue.get_center()), run_time=0.5)
        self.wait(0.3)

        # 3. Escala de 0 a 1. Scale from 0 to 1.
        inst = Rectangle(width=1.0, height=0.55, stroke_width=0).set_fill(OK, 1).move_to(ep.get_center() + UP * 0.1)
        counter = Swap(count)
        count1 = label(f"1 {TEXT['instance1']}", 18, OK, "BOLD").move_to(count)
        self.play(*cap.to(caption("s3")), FadeIn(inst), *counter.to(count1), run_time=0.7)
        pull = Arrow(queue.get_right(), ep.get_left(), buff=0.1, color=INK_SOFT, stroke_width=3)
        self.play(Create(pull), token.animate.move_to(inst.get_center()), run_time=0.5)
        fetch = Line(s3_in.get_top() + UP * 0.25, inst.get_center())
        self.play(MoveAlongPath(doc, fetch), run_time=0.6)
        self.play(FadeOut(doc), FadeOut(token), inst.animate.set_fill(AMBER, 1), run_time=0.5)

        # 4. Resultado y aviso. Result and notification.
        res = RoundedRectangle(width=0.4, height=0.5, corner_radius=0.05, stroke_width=0).set_fill(OK, 1)
        res.move_to(inst.get_center())
        self.play(*cap.to(caption("s4")), inst.animate.set_fill(OK, 1), run_time=0.3)
        self.add(res)
        out_arrow = Arrow(ep.get_right() + DOWN * 0.5, s3_out.get_left(), buff=0.1, color=OK, stroke_width=3)
        note_arrow = Arrow(ep.get_right() + UP * 0.3, sns.get_left(), buff=0.1, color=AMBER, stroke_width=3)
        self.play(Create(out_arrow), res.animate.move_to(s3_out.get_top() + UP * 0.3), run_time=0.6)
        self.play(Create(note_arrow), sns.box.animate.set_stroke(AMBER, 5), run_time=0.5)
        self.wait(0.4)

        # 5. Vuelve a 0. Back to 0.
        count0 = label(f"0 {TEXT['instances']}", 18, ACCENT, "BOLD").move_to(count)
        self.play(*cap.to(caption("s5")), FadeOut(inst), *counter.to(count0), run_time=0.7)
        self.wait(1.3)


class MmeLoading(PacedScene):
    def construct(self):
        title = label(TEXT["title_mme"], 24, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        box = RoundedRectangle(width=7.4, height=2.0, corner_radius=0.14, stroke_color=INK_SOFT, stroke_width=2)
        box.set_fill(SURFACE, 1).move_to(RIGHT * 1.6 + UP * 1.1)
        box_lbl = icon_title("aws/sagemaker-ai", TEXT["container"], 16, color=INK_SOFT, icon_height=0.34).next_to(
            box, UP, buff=0.1)
        slots = []
        for i in range(3):
            s = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.08, stroke_color=GRAY, stroke_width=2)
            s.set_fill("#ffffff", 1).move_to(box.get_center() + RIGHT * (i - 1) * 2.3 + DOWN * 0.05)
            slots.append(s)
        free = [label(TEXT["slot"], 14, MUTED).move_to(s) for s in slots]
        s3 = RoundedRectangle(width=7.4, height=1.1, corner_radius=0.12, stroke_color=OK, stroke_width=2)
        s3.set_fill("#ffffff", 1).move_to(RIGHT * 1.6 + DOWN * 1.5)
        s3_lbl = icon_title("aws/s3", TEXT["s3_models"], 15, color=OK, icon_height=0.34).next_to(
            s3.get_left(), RIGHT, buff=0.15).align_to(s3, UP).shift(DOWN * 0.08)
        names = ["m-0017", "m-0420", "m-1288", "m-2051", "m-2990"]
        files = VGroup(*[label(n, 14, INK_SOFT) for n in names]).arrange(RIGHT, buff=0.35)
        files.move_to(s3.get_center() + DOWN * 0.15)
        req_col = label(TEXT["req"], 16, MUTED).move_to(LEFT * 5.4 + UP * 2.3)
        self.play(FadeIn(title), FadeIn(box), FadeIn(box_lbl), *[FadeIn(s) for s in slots],
                  *[FadeIn(f) for f in free], FadeIn(s3), FadeIn(s3_lbl), FadeIn(files), FadeIn(req_col),
                  run_time=0.8)

        loaded = {}  # slot -> (name, group)
        last_use = {}
        cap = Swap()
        calls = ["m-0017", "m-0017", "m-0420", "m-1288", "m-0017", "m-2051"]
        for step, name in enumerate(calls):
            req = node(name, 1.7, 0.6, stroke=INK_SOFT, fill="#ffffff", size=16).move_to(LEFT * 5.4 + UP * 1.4)
            self.play(FadeIn(req), run_time=0.25)
            hit = next((k for k, (n, _) in loaded.items() if n == name), None)
            if hit is not None:
                self.play(*cap.to(caption("warm")), req.animate.move_to(slots[hit].get_center()), run_time=0.45)
                self.play(loaded[hit][1][0].animate.set_stroke(OK, 5), FadeOut(req), run_time=0.3)
                self.play(loaded[hit][1][0].animate.set_stroke(OK, 2), run_time=0.15)
            else:
                empty = [k for k in range(3) if k not in loaded]
                if empty:
                    k = empty[0]
                    new = caption("cold")
                else:
                    k = min(loaded, key=lambda j: last_use[j])
                    new = caption("evict")
                    old = loaded.pop(k)[1]
                    self.play(*cap.to(new), old.animate.set_opacity(0.15), run_time=0.5)
                    self.remove(old)
                    new = caption("cold")
                self.play(*cap.to(new), req.animate.move_to(slots[k].get_center()), run_time=0.4)
                src = files[names.index(name)]
                model = RoundedRectangle(width=1.8, height=0.8, corner_radius=0.06, stroke_color=OK, stroke_width=2)
                model.set_fill("#e3f1e9", 1).move_to(src)
                txt = label(name, 15, INK).move_to(model)
                grp = VGroup(model, txt)
                if free[k] in self.mobjects:
                    self.remove(free[k])
                self.play(grp.animate.move_to(slots[k].get_center()), FadeOut(req), run_time=0.7)
                loaded[k] = (name, grp)
                hit = k
            last_use[hit] = step
            self.wait(0.9)  # pausa para ver el resultado de cada llamada / pause to see each call's result
        self.play(*cap.to(label(TEXT["takeaway"], 20, OK, "BOLD", max_width=12.4).to_edge(DOWN, buff=0.6)),
                  run_time=0.5)
        self.wait(1.2)
