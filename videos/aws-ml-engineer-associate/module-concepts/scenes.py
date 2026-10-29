"""Escena genérica heredada para los temas sin escenas propias (MLA_TOPIC elige el tema).
Legacy generic scene for topics without their own scenes (MLA_TOPIC picks the topic)."""

VIDEOS = {"concept-flow": "MLATopicScene"}

import os

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    RoundedRectangle,
    Scene,
    Text,
    VGroup,
    config,
)

config.background_color = WHITE
LANG = os.environ.get("MLA_LANG", "es")
TOPIC = os.environ.get("MLA_TOPIC", "data-collection-storage")

INK = "#111114"
MUTED = "#64646e"
ACCENT = "#b3132b"
OK = "#1f7a4d"
SURFACE = "#f3f3f5"

TOPICS = {
    "data-collection-storage": {
        "es": ("Datos para ML", ["Eventos", "Kinesis", "Amazon S3", "Features"], "Conserva los datos originales"),
        "en": ("Data for ML", ["Events", "Kinesis", "Amazon S3", "Features"], "Keep the raw data"),
    },
    "data-transformation-features": {
        "es": ("Preprocesamiento", ["Datos", "Dividir", "Ajustar", "Aplicar"], "Ajusta solo con entrenamiento"),
        "en": ("Preprocessing", ["Data", "Split", "Fit", "Apply"], "Fit on training data only"),
    },
    "modeling-approaches": {
        "es": ("Enfoque de modelado", ["Tarea", "Datos", "Modelo", "Evaluar"], "RAG aporta contexto recuperado"),
        "en": ("Modeling approach", ["Task", "Data", "Model", "Evaluate"], "RAG supplies retrieved context"),
    },
    "training-customization": {
        "es": ("Entrenamiento", ["Entrenar", "Validar", "Ajustar", "Probar"], "Observa la generalización"),
        "en": ("Training", ["Train", "Validate", "Tune", "Test"], "Watch generalization"),
    },
    "model-evaluation": {
        "es": ("Evaluación", ["Baseline", "Métricas", "Segmentos", "Decidir"], "Elige métricas por costo del error"),
        "en": ("Evaluation", ["Baseline", "Metrics", "Segments", "Decide"], "Choose metrics by error cost"),
    },
    "deployment-infrastructure": {
        "es": ("Inferencia", ["Solicitud", "Patrón", "Capacidad", "Respuesta"], "Lote para resultados diferidos"),
        "en": ("Inference", ["Request", "Pattern", "Capacity", "Response"], "Batch for delayed results"),
    },
    "resource-provisioning": {
        "es": ("Capacidad", ["Medir", "Objetivo", "Escalar", "Verificar"], "Prueba los picos de tráfico"),
        "en": ("Capacity", ["Measure", "Target", "Scale", "Verify"], "Test traffic peaks"),
    },
    "mlops-cicd": {
        "es": ("MLOps", ["Preparar", "Entrenar", "Evaluar", "Aprobar"], "Promueve solo candidatos válidos"),
        "en": ("MLOps", ["Prepare", "Train", "Evaluate", "Approve"], "Promote only valid candidates"),
    },
    "monitoring-inference": {
        "es": ("Monitoreo", ["Métricas", "Baseline", "Deriva", "Investigar"], "Deriva no significa fallo"),
        "en": ("Monitoring", ["Metrics", "Baseline", "Drift", "Investigate"], "Drift does not mean failure"),
    },
    "cost-performance": {
        "es": ("Costo y rendimiento", ["Carga", "Latencia", "Costo", "Calidad"], "Compara con una carga realista"),
        "en": ("Cost and performance", ["Workload", "Latency", "Cost", "Quality"], "Compare with realistic traffic"),
    },
    "security": {
        "es": ("Seguridad", ["Identidad", "Rol IAM", "Mínimo acceso", "Proteger"], "No guardes claves en el código"),
        "en": ("Security", ["Identity", "IAM role", "Least access", "Protect"], "Never keep keys in code"),
    },
}


class MLATopicScene(Scene):
    def construct(self):
        title, stages, takeaway = TOPICS[TOPIC][LANG]
        heading = Text(title, font="Sans", font_size=34, color=INK, weight="BOLD").to_edge(UP, buff=0.65)
        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.45)

        cards = VGroup()
        for index, stage in enumerate(stages):
            color = ACCENT if index == 2 else (OK if index == 3 else MUTED)
            box = RoundedRectangle(
                width=2.75, height=1.35, corner_radius=0.14,
                stroke_color=color, stroke_width=2.2,
            ).set_fill(SURFACE if index < 2 else WHITE, opacity=1)
            label = Text(stage, font="Sans", font_size=23, color=INK, weight="MEDIUM")
            if label.width > 2.42:
                label.scale_to_fit_width(2.42)
            cards.add(VGroup(box, label.move_to(box)))
        cards.arrange(RIGHT, buff=0.42).move_to(UP * 0.35)

        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrow = Arrow(
                left.get_right(), right.get_left(), buff=0.08,
                color=ACCENT, stroke_width=3, max_tip_length_to_length_ratio=0.18,
            )
            arrows.add(arrow)

        for index, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.12), run_time=0.35)
            if index < len(cards) - 1:
                self.play(Create(arrows[index]), run_time=0.3)
        self.play(Indicate(cards[-1], color=OK, scale_factor=1.04), run_time=0.55)

        note = Text(takeaway, font="Sans", font_size=23, color=ACCENT)
        if note.width > 11.4:
            note.scale_to_fit_width(11.4)
        note.to_edge(DOWN, buff=0.72)
        self.play(FadeIn(note, shift=UP * 0.12), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(VGroup(heading, cards, note, arrows)), run_time=0.25)
