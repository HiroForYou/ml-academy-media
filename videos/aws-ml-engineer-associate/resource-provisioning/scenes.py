"""
Videos cortos del tema 3.2 (aprovisionar recursos). Short videos for topic 3.2.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/resource-provisioning/scenes.py --scene PrivateEndpoint --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"private-endpoint": "PrivateEndpoint"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Create, Cross, DashedVMobject, FadeIn, FadeOut, Line, MoveAlongPath,
    RoundedRectangle, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene, same_text  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, SURFACE, icon_node, icon_title, label, node, pick,
)

TEXT = pick({
    "es": {
        "title": "Endpoint en subredes privadas: cada camino necesita un endpoint de VPC",
        "vpc": "VPC sin acceso a internet",
        "subnet_a": "subred privada (AZ a)",
        "subnet_b": "subred privada (AZ b)",
        "container": "contenedor del modelo",
        "app": "app de la VPC",
        "s3": "Amazon S3\nmodel.tar.gz",
        "runtime": "API de SageMaker Runtime",
        "s1": "Con VpcConfig, el contenedor no alcanza S3: el endpoint falla al crearse",
        "gw": "gateway endpoint de S3",
        "s2": "Gateway endpoint de S3: el contenedor descarga ModelDataUrl",
        "ifc": "interface endpoint (PrivateLink)",
        "s3_": "Interface endpoint de SageMaker Runtime: InvokeEndpoint sin pasar por internet",
        "end": "Sin NAT gateway: solo los caminos que el modelo necesita",
        "download": "descarga",
    },
    "en": {
        "title": "Endpoint in private subnets: each path needs a VPC endpoint",
        "vpc": "VPC with no internet access",
        "subnet_a": "private subnet (AZ a)",
        "subnet_b": "private subnet (AZ b)",
        "container": "model container",
        "app": "app in the VPC",
        "s3": "Amazon S3\nmodel.tar.gz",
        "runtime": "SageMaker Runtime API",
        "s1": "With VpcConfig, the container cannot reach S3: endpoint creation fails",
        "gw": "S3 gateway endpoint",
        "s2": "S3 gateway endpoint: the container downloads ModelDataUrl",
        "ifc": "interface endpoint (PrivateLink)",
        "s3_": "SageMaker Runtime interface endpoint: InvokeEndpoint without the internet",
        "end": "No NAT gateway: only the paths the model needs",
        "download": "download",
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


def caption(key, color=INK_SOFT):
    return label(TEXT[key], 20, color, max_width=12.4).to_edge(DOWN, buff=0.5)


class PrivateEndpoint(PacedScene):
    def construct(self):
        title = label(TEXT["title"], 23, INK, "BOLD", max_width=12.6).to_edge(UP, buff=0.35)
        vpc = RoundedRectangle(width=8.0, height=4.6, corner_radius=0.16, stroke_color=INK_SOFT, stroke_width=2)
        vpc.set_fill("#ffffff", 1).move_to(LEFT * 2.2 + UP * 0.15)
        vpc_l = icon_title("aws/vpc", TEXT["vpc"], 16, INK_SOFT, icon_height=0.36).next_to(
            vpc.get_corner(UP + LEFT), DOWN + RIGHT, buff=0.12)
        subs = VGroup()
        for i, key in enumerate(("subnet_a", "subnet_b")):
            s = RoundedRectangle(width=3.0, height=3.4, corner_radius=0.1, stroke_color=GRAY, stroke_width=1.5)
            s.set_fill(SURFACE, 1).move_to(vpc.get_center() + LEFT * 1.75 + RIGHT * i * 3.3 + DOWN * 0.35)
            subs.add(VGroup(s, label(TEXT[key], 13, MUTED).next_to(s.get_top(), DOWN, buff=0.1)))
        cont = icon_node("aws/sagemaker-model", TEXT["container"], None, 2.7, 0.9, stroke=INK_SOFT, fill="#ffffff",
                         title_size=15, icon_height=0.5)
        cont.move_to(subs[0][0].get_center() + UP * 0.35)
        cont2 = icon_node("aws/sagemaker-model", TEXT["container"], None, 2.7, 0.9, stroke=INK_SOFT, fill="#ffffff",
                          title_size=15, icon_height=0.5)
        cont2.move_to(subs[1][0].get_center() + UP * 0.35)
        app = icon_node("aws/application", TEXT["app"], None, 2.2, 0.75, stroke=INK_SOFT, fill="#ffffff",
                        title_size=15, icon_height=0.42)
        app.move_to(subs[1][0].get_center() + DOWN * 1.0)
        s3_t, _, s3_d = TEXT["s3"].partition("\n")
        s3 = icon_node("aws/s3", s3_t, s3_d, 2.6, 1.1, stroke=OK, fill="#ffffff", title_size=17, desc_size=14,
                       icon_height=0.6).move_to(RIGHT * 5.4 + UP * 1.5)
        rt = icon_node("aws/sagemaker-ai", TEXT["runtime"], None, 2.6, 1.0, stroke=INK_SOFT, fill="#ffffff",
                       title_size=15, icon_height=0.55).move_to(RIGHT * 5.4 + DOWN * 1.2)
        self.play(FadeIn(title), FadeIn(vpc), FadeIn(vpc_l), FadeIn(subs), FadeIn(cont), FadeIn(cont2),
                  FadeIn(app), FadeIn(s3), FadeIn(rt), run_time=0.8)

        # 1. Sin endpoint de S3: falla. Without an S3 endpoint: it fails.
        cap = Swap()
        attempt = DashedVMobject(Line(cont2.get_right(), s3.get_left(), color=ACCENT, stroke_width=3), num_dashes=18)
        cross = Cross(scale_factor=0.25, stroke_color=ACCENT, stroke_width=6).move_to(vpc.get_right() + UP * 0.9)
        self.play(*cap.to(caption("s1", ACCENT)), Create(attempt), run_time=0.6)
        self.play(FadeIn(cross), cont[0].animate.set_stroke(ACCENT), cont2[0].animate.set_stroke(ACCENT), run_time=0.5)
        self.wait(0.6)

        # 2. Gateway endpoint de S3. S3 gateway endpoint.
        gw = icon_node("aws/vpc-endpoints", TEXT["gw"], None, 2.4, 0.75, stroke=OK, fill="#e3f1e9", title_size=13,
                       icon_height=0.45).move_to(vpc.get_right() + UP * 1.5)
        self.play(*cap.to(caption("s2", OK)), FadeOut(attempt), FadeOut(cross), FadeIn(gw), run_time=0.6)
        route = VGroup(Line(s3.get_left(), gw.get_right(), color=OK, stroke_width=3),
                       Line(gw.get_left(), cont2.get_corner(UP + RIGHT) + LEFT * 0.5, color=OK, stroke_width=3))
        self.play(Create(route), run_time=0.5)
        pkgs = []
        for c in (cont, cont2):
            p = RoundedRectangle(width=0.35, height=0.3, corner_radius=0.04, stroke_width=0).set_fill(OK, 1)
            p.move_to(s3.get_left())
            pkgs.append((p, c))
            self.add(p)
        self.play(*[MoveAlongPath(p, Line(s3.get_left(), gw.get_center())) for p, _ in pkgs], run_time=0.5)
        self.play(*[p.animate.move_to(c.get_top() + DOWN * 0.05) for p, c in pkgs], run_time=0.6)
        self.play(*[FadeOut(p) for p, _ in pkgs], cont[0].animate.set_stroke(OK), cont2[0].animate.set_stroke(OK),
                  run_time=0.4)

        # 3. Interface endpoint para invocar. Interface endpoint to invoke.
        ifc = icon_node("aws/privatelink", TEXT["ifc"], None, 2.6, 0.75, stroke=AMBER, fill="#fff4d6", title_size=13,
                        icon_height=0.45).move_to(vpc.get_right() + DOWN * 1.2)
        self.play(*cap.to(caption("s3_", INK_SOFT)), FadeIn(ifc), run_time=0.6)
        call = VGroup(Line(app.get_right(), ifc.get_left(), color=AMBER, stroke_width=3),
                      Line(ifc.get_right(), rt.get_left(), color=AMBER, stroke_width=3))
        self.play(Create(call), run_time=0.5)
        dot = RoundedRectangle(width=0.3, height=0.3, corner_radius=0.05, stroke_width=0).set_fill(AMBER, 1)
        dot.move_to(app.get_right())
        self.add(dot)
        self.play(MoveAlongPath(dot, Line(app.get_right(), ifc.get_left())), run_time=0.4)
        self.play(MoveAlongPath(dot, Line(ifc.get_right(), rt.get_left())), run_time=0.4)
        self.play(FadeOut(dot), rt[0].animate.set_stroke(OK, 4), run_time=0.3)

        self.play(*cap.to(caption("end", OK)), run_time=0.5)
        self.wait(1.2)
