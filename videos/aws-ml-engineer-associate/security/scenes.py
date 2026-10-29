"""
Videos cortos del tema 4.3 (seguridad). Short videos for topic 4.3.

    python scripts/render_video.py --lang es --file videos/aws-ml-engineer-associate/security/scenes.py --scene KmsAccessDenied --out output/x.mp4
"""

# Nombre publicado -> clase de escena. Published name -> scene class.
VIDEOS = {"kms-access-denied": "KmsAccessDenied", "guardrails-pii": "GuardrailsPii"}

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, Create, Dot, FadeIn, FadeOut, Indicate, MoveAlongPath, RoundedRectangle,
    Transform, VGroup, VMobject,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from style import PacedScene  # noqa: E402
from style import (  # noqa: E402
    ACCENT, AMBER, GRAY, INK, INK_SOFT, MUTED, OK, RULE, SURFACE, icon, icon_node, icon_title, label, node, pick,
    pulse,
)

TEXT = pick({
    "es": {
        "kms_title": "AccessDenied al leer datos cifrados con SSE-KMS",
        "request": "sm-train-fraud → s3:GetObject\nfraud-data/train/  (SSE-KMS, fraud-key)",
        "layers": ["Política de identidad\n(rol de ejecución)", "Bucket policy", "VPC endpoint\npolicy", "SCP",
                   "Key policy de\nfraud-key"],
        "rule": "Cada capa debe permitir la acción; si una falla, la solicitud falla",
        "trail": "Evento en CloudTrail",
        "event": "errorCode: AccessDenied\nuserIdentity: sm-train-fraud\nacción: kms:Decrypt · recurso: fraud-key",
        "fix": "Corrección: una declaración en la key policy solo para sm-train-fraud",
        "ok": "El trabajo lee los datos",
        "avoid": "No «arreglar» con kms:* ni Resource: \"*\": desactiva el control que lo detectó",
    },
    "en": {
        "kms_title": "AccessDenied when reading SSE-KMS encrypted data",
        "request": "sm-train-fraud → s3:GetObject\nfraud-data/train/  (SSE-KMS, fraud-key)",
        "layers": ["Identity policy\n(execution role)", "Bucket policy", "VPC endpoint\npolicy", "SCP",
                   "fraud-key\nkey policy"],
        "rule": "Every layer must allow the action; if one fails, the request fails",
        "trail": "CloudTrail event",
        "event": "errorCode: AccessDenied\nuserIdentity: sm-train-fraud\naction: kms:Decrypt · resource: fraud-key",
        "fix": "Fix: one key policy statement for sm-train-fraud only",
        "ok": "The job reads the data",
        "avoid": "Don't “fix” it with kms:* or Resource: \"*\": it disables the control that caught it",
    },
})

TEXT_G = pick({
    "es": {
        "g_title": "Bedrock Guardrails enmascara PII en la entrada y la salida",
        "user": "Prompt del usuario",
        "prompt": "Mi correo es ana@example.com,\n¿cuál es mi saldo?",
        "guard": "Guardrail\nfiltro de información sensible\nEMAIL → ANONYMIZE",
        "model": "Modelo (FM)",
        "masked": "Mi correo es {EMAIL},\n¿cuál es mi saldo?",
        "answer": "Respuesta filtrada\nal usuario",
        "log": "Invocation log · campo input",
        "log_val": "\"Mi correo es ana@example.com…\"",
        "pitfall": "El log guarda el prompt original: protégelo con CloudWatch Logs data protection o no registres el contenido",
        "note": "ApplyGuardrail aplica el mismo control a modelos fuera de Bedrock",
    },
    "en": {
        "g_title": "Bedrock Guardrails masks PII in inputs and outputs",
        "user": "User prompt",
        "prompt": "My email is ana@example.com,\nwhat is my balance?",
        "guard": "Guardrail\nsensitive information filter\nEMAIL → ANONYMIZE",
        "model": "Model (FM)",
        "masked": "My email is {EMAIL},\nwhat is my balance?",
        "answer": "Filtered response\nto the user",
        "log": "Invocation log · input field",
        "log_val": "\"My email is ana@example.com…\"",
        "pitfall": "The log keeps the original prompt: protect it with CloudWatch Logs data protection, or don't log content",
        "note": "ApplyGuardrail applies the same control to models outside Bedrock",
    },
})


def mark(ok, at):
    sym = label("✓" if ok else "✗", 30, OK if ok else ACCENT, "BOLD")
    return sym.move_to(at)


# Logo de cada capa de permisos. Logo of each permission layer.
LAYER_ICONS = ["aws/iam-role", "aws/s3", "aws/vpc-endpoints", "aws/organizations", "aws/kms"]


def layer(text, icon_name):
    """Capa de permisos: logo arriba, texto debajo. Permission layer: logo on top, text below."""
    box = RoundedRectangle(width=2.3, height=1.55, corner_radius=0.12, stroke_color=INK_SOFT, stroke_width=2)
    box.set_fill(SURFACE, 1)
    ic = icon(icon_name, 0.5).next_to(box.get_top(), DOWN, buff=0.14)
    txt = label(text, 15, INK, max_width=2.05).next_to(ic, DOWN, buff=0.1)
    return VGroup(box, ic, txt)


class KmsAccessDenied(PacedScene):
    def construct(self):
        title = label(TEXT["kms_title"], 26, INK, "BOLD", max_width=12.4).to_edge(UP, buff=0.4)
        req_t, _, req_d = TEXT["request"].partition("\n")
        req = icon_node("aws/iam-role", req_t, req_d, 6.4, 1.0, stroke=INK_SOFT, fill="#ffffff", title_size=17,
                        desc_size=15, icon_height=0.55).move_to(UP * 2.15)
        layers = VGroup(*[layer(t, i) for t, i in zip(TEXT["layers"], LAYER_ICONS)]).arrange(RIGHT, buff=0.22)
        layers.move_to(DOWN * 0.1)
        rule = label(TEXT["rule"], 18, MUTED, max_width=12.4).next_to(layers, DOWN, buff=0.25)
        self.play(FadeIn(title), FadeIn(req), FadeIn(layers), run_time=0.8)
        self.play(FadeIn(rule), run_time=0.3)

        # La solicitud pasa capa por capa. The request goes layer by layer.
        token = Dot(req.get_bottom(), radius=0.11, color=AMBER)
        self.add(token)
        marks = []
        for i, lay in enumerate(layers):
            ok = i < len(layers) - 1
            path = VMobject().set_points_as_corners([token.get_center(), lay.get_top() + UP * 0.15])
            self.play(MoveAlongPath(token, path), run_time=0.35)
            m = mark(ok, lay.get_top() + UP * 0.4)
            marks.append(m)
            anims = [FadeIn(m), lay[0].animate.set_stroke(OK if ok else ACCENT, 3)]
            self.play(*anims, run_time=0.3)
        self.play(token.animate.set_color(ACCENT), pulse(layers[-1][0], ACCENT), run_time=0.6)

        trail_t = icon_title("aws/cloudtrail", TEXT["trail"], 17, icon_height=0.36)
        event = label(TEXT["event"], 15, INK_SOFT)
        card = VGroup(trail_t, event).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        frame = RoundedRectangle(width=card.width + 0.5, height=card.height + 0.35, corner_radius=0.1,
                                 stroke_color=ACCENT, stroke_width=2).set_fill(SURFACE, 1)
        frame.move_to(card)
        ev = VGroup(frame, card).move_to(DOWN * 2.3 + LEFT * 2.8)
        self.play(FadeIn(ev), run_time=0.5)
        self.wait(0.5)

        fix = label(TEXT["fix"], 17, OK, max_width=6.0).move_to(DOWN * 1.95 + RIGHT * 3.4)
        self.play(FadeIn(fix), layers[-1][0].animate.set_stroke(OK, 3),
                  Transform(marks[-1], mark(True, marks[-1].get_center())), FadeOut(token),
                  run_time=0.6)
        ok_t = label(TEXT["ok"], 19, OK, "BOLD").next_to(fix, DOWN, buff=0.2)
        self.play(FadeIn(ok_t), run_time=0.3)
        avoid = label(TEXT["avoid"], 18, ACCENT, max_width=12.4).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(avoid), run_time=0.4)
        self.wait(1.3)


class GuardrailsPii(PacedScene):
    def construct(self):
        t = TEXT_G
        title = label(t["g_title"], 26, INK, "BOLD", max_width=12.4).to_edge(UP, buff=0.4)
        user_t = icon_title("aws/user", t["user"], 15, MUTED, icon_height=0.34).move_to(LEFT * 4.6 + UP * 2.3)
        prompt = node(t["prompt"], 3.8, 1.1, stroke=AMBER, fill="#ffffff", size=16).move_to(LEFT * 4.6 + UP * 1.4)
        g_t, _, g_d = t["guard"].partition("\n")
        guard = icon_node("aws/bedrock", g_t, g_d, 3.7, 1.5, stroke=OK, fill="#eaf4ee", title_size=17, desc_size=14,
                          icon_height=0.6).move_to(UP * 1.4)
        model = icon_node("aws/bedrock", t["model"], None, 2.8, 1.1, stroke=INK_SOFT, title_size=17,
                          icon_height=0.6).move_to(RIGHT * 4.8 + UP * 1.4)
        a1 = Arrow(prompt.get_right(), guard.get_left(), buff=0.08, color=MUTED, stroke_width=3)
        a2 = Arrow(guard.get_right(), model.get_left(), buff=0.08, color=MUTED, stroke_width=3)
        self.play(FadeIn(title), FadeIn(user_t), FadeIn(prompt), FadeIn(guard), FadeIn(model), Create(a1),
                  Create(a2), run_time=0.9)

        # La copia del prompt cruza el guardrail y sale enmascarada. The prompt copy crosses the guardrail masked.
        moving = prompt.copy()
        self.play(moving.animate.move_to(guard).scale(0.6).set_opacity(0.3), run_time=0.6)
        masked = node(t["masked"], 3.6, 1.0, stroke=OK, fill="#ffffff", size=15).move_to(RIGHT * 1.15 + DOWN * 0.45)
        to_masked = Arrow(guard.get_bottom(), masked.get_top() + LEFT * 1.0, buff=0.08, color=OK, stroke_width=3)
        self.play(FadeOut(moving), Create(to_masked), FadeIn(masked), pulse(guard, OK),
                  run_time=0.7)

        back = Arrow(model.get_bottom(), model.get_bottom() + DOWN * 1.4, buff=0.08, color=MUTED, stroke_width=3)
        answer = node(t["answer"], 2.8, 0.95, stroke=OK, fill="#ffffff", size=15).next_to(back, DOWN, buff=0.08)
        self.play(Create(back), FadeIn(answer), run_time=0.6)
        self.wait(0.4)

        log_t = icon_title("aws/cloudwatch-logs", t["log"], 16, icon_height=0.36)
        log_v = label(t["log_val"], 16, ACCENT)
        log = VGroup(log_t, log_v).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        frame = RoundedRectangle(width=log.width + 0.5, height=log.height + 0.35, corner_radius=0.1,
                                 stroke_color=ACCENT, stroke_width=2).set_fill(SURFACE, 1).move_to(log)
        log_card = VGroup(frame, log).move_to(LEFT * 3.6 + DOWN * 1.2)
        link = Arrow(prompt.get_bottom(), log_card.get_top(), buff=0.1, color=ACCENT, stroke_width=3)
        self.play(Create(link), FadeIn(log_card), run_time=0.6)
        pit = label(t["pitfall"], 17, ACCENT, max_width=12.4).to_edge(DOWN, buff=0.75)
        note = label(t["note"], 15, MUTED, max_width=12.4).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(pit), run_time=0.4)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(1.7)
